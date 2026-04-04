#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import signal
import sys
import tempfile
import time
import textwrap
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fcntl

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path(
    os.environ.get("CLAUDE_PLUGIN_DATA_DIR")
    or os.environ.get("BUDDYHUB_DATA_ROOT")
    or (Path.home() / ".claude" / "plugins" / "data" / "buddyhub")
)
RUNTIME_FILE = DATA_ROOT / "runtime.json"
SESSIONS_FILE = DATA_ROOT / "sessions.json"
OWNERSHIP_FILE = DATA_ROOT / "ownership.json"
STATE_LOCK_FILE = DATA_ROOT / "state.lock"
LEGACY_PID_FILE = DATA_ROOT / "sidecar.pid"
LEGACY_UI_REQUEST_FILE = DATA_ROOT / "ui-request.json"
LEGACY_LOG_FILE = DATA_ROOT / "sidecar.log"

STALE_SESSION_SECONDS = 120
IDLE_TIMEOUT_SECONDS = 30
PLUGIN_REF = "buddyhub@buddyhub"

TOOL_STATE_MAP = {
    "Read": "reading",
    "Glob": "reading",
    "Grep": "reading",
    "Edit": "coding",
    "Write": "coding",
    "MultiEdit": "coding",
    "NotebookEdit": "coding",
    "Bash": "running",
    "WebFetch": "browsing",
    "WebSearch": "browsing",
    "AskUserQuestion": "waiting",
    "Task": "thinking",
}

VISIBLE_STATES = {
    "idle",
    "thinking",
    "reading",
    "coding",
    "running",
    "browsing",
    "waiting",
    "done",
    "error",
}

LIFECYCLE_STATES = {
    "installed",
    "enabled",
    "paused",
    "disabled",
    "error",
    "uninstalled",
}

BUDDY_EXPRESSIONS = {
    "idle": {
        "headline": "idle",
        "subtitle": "resting quietly",
        "token": "idle",
    },
    "thinking": {
        "headline": "thinking...",
        "subtitle": "working through your request",
        "token": "think",
    },
    "reading": {
        "headline": "reading",
        "subtitle": "looking through files",
        "token": "read",
    },
    "coding": {
        "headline": "coding",
        "subtitle": "making changes",
        "token": "edit",
    },
    "running": {
        "headline": "running",
        "subtitle": "executing commands",
        "token": "run",
    },
    "browsing": {
        "headline": "browsing",
        "subtitle": "checking the web",
        "token": "web",
    },
    "waiting": {
        "headline": "waiting",
        "subtitle": "needs your input",
        "token": "wait",
    },
    "done": {
        "headline": "done",
        "subtitle": "finished this step",
        "token": "done",
    },
    "error": {
        "headline": "error",
        "subtitle": "something went wrong",
        "token": "err",
    },
    "paused": {
        "headline": "paused",
        "subtitle": "taking a short nap",
        "token": "pause",
    },
    "disabled": {
        "headline": "disabled",
        "subtitle": "off duty",
        "token": "off",
    },
}

NATIVE_CONTROL_STATUS = {
    "mode": "experimental",
    "writable": False,
    "field": "companionReaction",
    "reason": (
        "No supported third-party plugin path has been confirmed for writing the "
        "official Buddy's native reaction state."
    ),
}


def ensure_data_root() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def now_ts() -> float:
    return time.time()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, payload: Any) -> None:
    ensure_data_root()
    fd, tmp_name = tempfile.mkstemp(
        prefix=f"{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True))
            handle.flush()
            os.fsync(handle.fileno())
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)


@contextmanager
def state_lock() -> Any:
    ensure_data_root()
    with STATE_LOCK_FILE.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def plugin_version() -> str:
    plugin_meta = read_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", {})
    return str(plugin_meta.get("version", "0.1.0"))


def default_runtime() -> dict[str, Any]:
    return {
        "plugin": "buddyhub",
        "version": plugin_version(),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "lifecycle_state": "enabled",
        "current_state": "idle",
        "active_session_id": None,
        "last_event": None,
        "last_update_ts": 0.0,
        "statusline_enabled": False,
        "buddy_name": None,
        "identity": {
            "available": False,
            "source": None,
            "name": None,
            "species": None,
            "rarity": None,
            "shiny": None
        }
    }


def default_sessions() -> dict[str, Any]:
    return {"version": 1, "sessions": {}}


def load_runtime() -> dict[str, Any]:
    runtime = default_runtime()
    runtime.update(read_json(RUNTIME_FILE, {}))
    if runtime.get("lifecycle_state") not in LIFECYCLE_STATES:
        runtime["lifecycle_state"] = "enabled"
    return runtime


def save_runtime(runtime: dict[str, Any]) -> None:
    runtime["updated_at"] = now_iso()
    write_json(RUNTIME_FILE, runtime)


def load_sessions() -> dict[str, Any]:
    sessions = default_sessions()
    sessions.update(read_json(SESSIONS_FILE, {}))
    sessions.setdefault("sessions", {})
    return sessions


def save_sessions(sessions: dict[str, Any]) -> None:
    write_json(SESSIONS_FILE, sessions)


def ensure_ownership_manifest() -> dict[str, Any]:
    ensure_data_root()
    manifest = read_json(OWNERSHIP_FILE, None)
    if manifest is None:
        manifest = {
            "plugin": "buddyhub",
            "version": plugin_version(),
            "created_at": now_iso(),
            "data_root": str(DATA_ROOT),
            "owned_files": [
                str(RUNTIME_FILE),
                str(SESSIONS_FILE),
                str(OWNERSHIP_FILE),
                str(STATE_LOCK_FILE),
            ],
            "runtime_assets": [],
            "config_integrations": {
                "plugin_hooks": "managed by Claude Code plugin install",
                "status_line": None,
            },
        }
        write_json(OWNERSHIP_FILE, manifest)
    return manifest


def read_hook_payload() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def detect_session_id(payload: dict[str, Any]) -> str:
    return str(
        payload.get("session_id")
        or os.environ.get("CLAUDE_SESSION_ID")
        or "unknown-session"
    )


def session_project_name(payload: dict[str, Any]) -> str | None:
    cwd = payload.get("cwd")
    if not cwd:
        return None
    return Path(cwd).name


def runtime_state_for_event(event_name: str, payload: dict[str, Any]) -> str:
    if event_name == "SessionStart":
        return "idle"
    if event_name == "SessionEnd":
        return "idle"
    if event_name == "UserPromptSubmit":
        return "thinking"
    if event_name == "Notification":
        return "waiting"
    if event_name == "Stop":
        return "done"
    if event_name == "PostToolUse":
        return "thinking"
    if event_name == "PreToolUse":
        tool_name = str(payload.get("tool_name") or os.environ.get("CLAUDE_TOOL_NAME") or "")
        return TOOL_STATE_MAP.get(tool_name, "thinking")
    return "thinking"


def prune_stale_sessions(sessions: dict[str, Any]) -> None:
    current_time = now_ts()
    for session in sessions.get("sessions", {}).values():
        last_update = float(session.get("last_update_ts", 0))
        stale = current_time - last_update > STALE_SESSION_SECONDS
        session["stale"] = stale
        if stale:
            session["active"] = False
            if session.get("state") in {"done", "waiting"}:
                session["state"] = "idle"


def choose_active_session(runtime: dict[str, Any], sessions: dict[str, Any]) -> str | None:
    session_map = sessions.get("sessions", {})
    pinned = runtime.get("active_session_id")
    if pinned and pinned in session_map and session_map[pinned].get("active") and not session_map[pinned].get("stale"):
        return pinned

    valid = [
        session
        for session in session_map.values()
        if session.get("active") and not session.get("stale")
    ]
    if not valid:
        return None
    valid.sort(key=lambda item: float(item.get("last_update_ts", 0)), reverse=True)
    return str(valid[0]["session_id"])


def recompute_runtime_state(runtime: dict[str, Any], sessions: dict[str, Any]) -> None:
    prune_stale_sessions(sessions)
    active_session_id = choose_active_session(runtime, sessions)
    runtime["active_session_id"] = active_session_id
    if runtime.get("lifecycle_state") == "paused":
        runtime["current_state"] = "idle"
        return
    if runtime.get("lifecycle_state") == "disabled":
        runtime["current_state"] = "idle"
        return
    if not active_session_id:
        runtime["current_state"] = "idle"
        return

    active = sessions["sessions"].get(active_session_id, {})
    last_update = float(active.get("last_update_ts", 0))
    if now_ts() - last_update > IDLE_TIMEOUT_SECONDS:
        runtime["current_state"] = "idle"
    else:
        runtime["current_state"] = str(active.get("state", "idle"))
    if runtime["current_state"] not in VISIBLE_STATES:
        runtime["current_state"] = "idle"


def empty_identity() -> dict[str, Any]:
    return {
        "available": False,
        "source": None,
        "name": None,
        "species": None,
        "rarity": None,
        "shiny": None,
    }


def read_companion_intro(transcript_path: str | None) -> dict[str, Any] | None:
    if not transcript_path:
        return None

    path = Path(transcript_path)
    if not path.exists() or not path.is_file():
        return None

    try:
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    record = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue
                if record.get("type") != "attachment":
                    continue
                attachment = record.get("attachment") or {}
                if attachment.get("type") != "companion_intro":
                    continue
                name = attachment.get("name")
                species = attachment.get("species")
                if not (name or species):
                    continue
                return {
                    "available": True,
                    "source": "transcript:companion_intro",
                    "name": name,
                    "species": species,
                    "rarity": None,
                    "shiny": None,
                }
    except OSError:
        return None

    return None


def resolve_buddy_identity(runtime: dict[str, Any], sessions: dict[str, Any]) -> dict[str, Any]:
    session_map = sessions.get("sessions", {})
    candidate_sessions: list[dict[str, Any]] = []

    active_session_id = runtime.get("active_session_id")
    if active_session_id and active_session_id in session_map:
        candidate_sessions.append(session_map[active_session_id])

    remaining_sessions = [
        session
        for session in session_map.values()
        if session.get("session_id") != active_session_id
    ]
    remaining_sessions.sort(key=lambda item: float(item.get("last_update_ts", 0)), reverse=True)
    candidate_sessions.extend(remaining_sessions)

    seen_paths: set[str] = set()
    for session in candidate_sessions:
        transcript_path = session.get("transcript_path")
        if not transcript_path or transcript_path in seen_paths:
            continue
        seen_paths.add(transcript_path)
        identity = read_companion_intro(transcript_path)
        if identity:
            return identity

    return empty_identity()


def record_hook_event(event_name: str, payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ensure_ownership_manifest()
    with state_lock():
        runtime = load_runtime()
        sessions = load_sessions()
        session_id = detect_session_id(payload)
        session_map = sessions.setdefault("sessions", {})
        session_record = session_map.setdefault(
            session_id,
            {
                "session_id": session_id,
                "created_at": now_iso(),
                "active": True,
                "stale": False,
                "project_name": session_project_name(payload),
                "cwd": payload.get("cwd"),
                "transcript_path": payload.get("transcript_path"),
            },
        )
        session_record["session_id"] = session_id
        session_record["cwd"] = payload.get("cwd", session_record.get("cwd"))
        session_record["transcript_path"] = payload.get("transcript_path", session_record.get("transcript_path"))
        session_record["project_name"] = session_project_name(payload) or session_record.get("project_name")
        session_record["last_event"] = event_name
        session_record["last_update_ts"] = now_ts()
        session_record["updated_at"] = now_iso()
        session_record["tool_name"] = payload.get("tool_name")
        session_record["source"] = payload.get("source")
        session_record["reason"] = payload.get("reason")
        session_record["active"] = event_name != "SessionEnd"
        session_record["stale"] = False
        session_record["state"] = runtime_state_for_event(event_name, payload)

        runtime["last_event"] = event_name
        runtime["last_update_ts"] = session_record["last_update_ts"]
        if event_name == "SessionStart":
            runtime["lifecycle_state"] = runtime.get("lifecycle_state", "enabled")
        recompute_runtime_state(runtime, sessions)
        runtime["identity"] = resolve_buddy_identity(runtime, sessions)
        runtime["buddy_name"] = runtime["identity"].get("name")
        save_sessions(sessions)
        save_runtime(runtime)
        return runtime, sessions


def pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def read_legacy_pid() -> int | None:
    try:
        return int(LEGACY_PID_FILE.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def stop_legacy_runtime() -> bool:
    pid = read_legacy_pid()
    if not pid:
        if LEGACY_PID_FILE.exists():
            LEGACY_PID_FILE.unlink(missing_ok=True)
        return False
    if not pid_is_alive(pid):
        LEGACY_PID_FILE.unlink(missing_ok=True)
        return False
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass
    for _ in range(20):
        if not pid_is_alive(pid):
            break
        time.sleep(0.05)
    LEGACY_PID_FILE.unlink(missing_ok=True)
    return True


def set_lifecycle_state(new_state: str) -> dict[str, Any]:
    with state_lock():
        runtime = load_runtime()
        if new_state not in LIFECYCLE_STATES:
            raise ValueError(f"Unsupported lifecycle state: {new_state}")
        runtime["lifecycle_state"] = new_state
        recompute_runtime_state(runtime, load_sessions())
        save_runtime(runtime)
        return runtime


def update_runtime_preferences(**changes: Any) -> dict[str, Any]:
    with state_lock():
        runtime = load_runtime()
        runtime.update(changes)
        save_runtime(runtime)
        return runtime


def display_state(runtime: dict[str, Any]) -> str:
    lifecycle = str(runtime.get("lifecycle_state", "enabled"))
    if lifecycle in {"paused", "disabled", "error"}:
        return lifecycle
    state = str(runtime.get("current_state", "idle"))
    if state in BUDDY_EXPRESSIONS:
        return state
    return "idle"


def buddy_expression(runtime: dict[str, Any]) -> dict[str, str]:
    return BUDDY_EXPRESSIONS[display_state(runtime)]


def render_buddy_bubble(runtime: dict[str, Any], *, compact: bool = False) -> list[str]:
    expression = buddy_expression(runtime)
    width = 20 if compact else 26
    wrapped: list[str] = []
    for raw in (expression["headline"], expression["subtitle"]):
        wrapped.extend(textwrap.wrap(raw, width=width) or [""])

    bubble_width = max(len(line) for line in wrapped)
    cap = "-" * (bubble_width + 2)
    lines = [f"      .{cap}."]
    for line in wrapped:
        lines.append(f"      | {line:<{bubble_width}} |")
    lines.append(f"      '{cap}'")
    return lines


def render_identity_card(runtime: dict[str, Any], *, compact: bool = False) -> list[str]:
    identity = runtime.get("identity", {})
    if identity.get("available"):
        details = [
            identity.get("name") or "Current Claude Buddy",
            f"species: {identity.get('species') or 'unknown'}",
        ]
        if not compact:
            details.append("verified: companion_intro")
    else:
        details = [
            "Current Claude Buddy",
            "identity unavailable",
            "waiting for companion_intro",
        ]

    panel_width = max(len(line) for line in details)
    return [
        f"      +{'-' * (panel_width + 2)}+",
        *[f"      | {line:<{panel_width}} |" for line in details],
        f"      +{'-' * (panel_width + 2)}+",
    ]


def render_buddy_scene(info: dict[str, Any], *, compact: bool = False) -> str:
    runtime = info["runtime"]
    active_session = info["active_session"] or {}
    identity = runtime.get("identity", {})
    state = display_state(runtime)
    name = identity.get("name") or "Current Claude Buddy"
    project = active_session.get("project_name")
    last_event = runtime.get("last_event") or "none"
    lifecycle = runtime.get("lifecycle_state", "enabled")
    if identity.get("available"):
        identity_line = (
            f"Identity source: `{identity.get('source')}`\n"
            "Unverified Buddy fields remain hidden in V1."
        )
    else:
        identity_line = "Identity source not available yet."

    native_status = (
        "Official Buddy native control is still experimental.\n"
        f"`{NATIVE_CONTROL_STATUS['field']}` is not writable from a confirmed third-party plugin path yet."
    )

    lines = [
        "# BuddyHub",
        "",
        *render_identity_card(runtime, compact=compact),
        "",
        f"Detected official Buddy: `{name}`",
        f"Observed Buddy state: `{state}`",
        f"Lifecycle: `{lifecycle}`",
    ]

    if project:
        lines.append(f"Watching project: `{project}`")
    else:
        lines.append("Waiting between tasks.")

    lines.append(f"Recent event: `{last_event}`")

    if not compact:
        lines.append(identity_line)
        lines.append(native_status)

        if runtime.get("statusline_enabled", False):
            lines.append("Status line sync is on.")

        lines.extend(
            [
                "",
                "Quick actions:",
                "- `/buddyhub:status`",
                "- `/buddyhub:pause`",
                "- `/buddyhub:doctor`",
            ]
        )
    else:
        lines.extend(
            [
                identity_line,
                native_status,
                f"Status line sync: `{str(runtime.get('statusline_enabled', False)).lower()}`",
            ]
        )
    return "\n".join(lines)


def render_buddy_statusline(info: dict[str, Any]) -> str:
    runtime = info["runtime"]
    active_session = info["active_session"] or {}
    state = display_state(runtime)
    identity = runtime.get("identity", {})
    project = active_session.get("project_name")
    suffix = f" | {project}" if project else ""
    subject = identity.get("name") or "Claude Buddy"
    if identity.get("species"):
        subject = f"{subject} | {identity['species']}"
    return f"{subject} | {state}{suffix}"


def snapshot() -> dict[str, Any]:
    ensure_ownership_manifest()
    with state_lock():
        runtime = load_runtime()
        sessions = load_sessions()
        recompute_runtime_state(runtime, sessions)
        runtime["identity"] = resolve_buddy_identity(runtime, sessions)
        runtime["buddy_name"] = runtime["identity"].get("name")
        save_sessions(sessions)
        save_runtime(runtime)
        active_session_id = runtime.get("active_session_id")
        active_session = sessions.get("sessions", {}).get(active_session_id) if active_session_id else None
    return {
        "runtime": runtime,
        "sessions": sessions,
        "active_session": active_session,
        "paths": {
            "data_root": str(DATA_ROOT),
            "runtime_file": str(RUNTIME_FILE),
            "sessions_file": str(SESSIONS_FILE),
            "ownership_file": str(OWNERSHIP_FILE),
            "statusline_script": str(PLUGIN_ROOT / "scripts" / "statusline.py"),
        },
    }


def human_status_report() -> str:
    info = snapshot()
    runtime = info["runtime"]
    active_session = info["active_session"] or {}
    lines = [
        render_buddy_scene(info, compact=True),
        "",
        "Commands",
        "",
        "- `/buddyhub:help`",
        "- `/buddyhub:status`",
        "- `/buddyhub:pause`",
        "- `/buddyhub:resume`",
        "- `/buddyhub:disable`",
        "- `/buddyhub:open`",
        "- `/buddyhub:uninstall`",
        "- `/buddyhub:doctor`",
        "- `/buddyhub:statusline-on`",
        "- `/buddyhub:statusline-off`",
        "- `/buddyhub:pet-install`",
        "",
        "Runtime",
        "",
        f"- Active session: `{runtime.get('active_session_id') or 'none'}`",
        f"- Project: `{active_session.get('project_name') or 'unknown'}`",
        f"- Last update: `{runtime.get('updated_at') or 'none'}`",
        f"- Data root: `{info['paths']['data_root']}`",
        "",
        "Status line",
        "",
        "BuddyHub uses Claude Code text surfaces as the primary UI.",
        "The official Buddy's native reaction path is still experimental from a third-party plugin.",
        "The optional status line script lives at:",
        f"- `{info['paths']['statusline_script']}`",
    ]
    return "\n".join(lines)


def diagnose() -> dict[str, Any]:
    info = snapshot()
    identity = info["runtime"].get("identity", {})
    diagnostics = {
        "ui_mode": "tui-first",
        "lifecycle_state": info["runtime"].get("lifecycle_state"),
        "current_state": info["runtime"].get("current_state"),
        "statusline_enabled": info["runtime"].get("statusline_enabled", False),
        "ownership_manifest_exists": OWNERSHIP_FILE.exists(),
        "runtime_file_exists": RUNTIME_FILE.exists(),
        "sessions_file_exists": SESSIONS_FILE.exists(),
        "legacy_runtime_assets_present": any(
            path.exists() for path in (LEGACY_PID_FILE, LEGACY_UI_REQUEST_FILE, LEGACY_LOG_FILE)
        ),
        "active_session_id": info["runtime"].get("active_session_id"),
        "active_project": (info["active_session"] or {}).get("project_name"),
        "identity_available": identity.get("available", False),
        "identity_source": identity.get("source"),
        "buddy_name": identity.get("name"),
        "buddy_species": identity.get("species"),
        "native_control_mode": NATIVE_CONTROL_STATUS["mode"],
        "native_control_writable": NATIVE_CONTROL_STATUS["writable"],
        "native_control_field": NATIVE_CONTROL_STATUS["field"],
        "native_control_reason": NATIVE_CONTROL_STATUS["reason"],
    }
    diagnostics["claude_cli_available"] = shutil_which("claude") is not None
    return diagnostics


def shutil_which(binary: str) -> str | None:
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path_dir) / binary
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None

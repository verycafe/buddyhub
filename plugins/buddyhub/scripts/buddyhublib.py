#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
import hashlib
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_CONFIG_ROOT = Path.home() / ".claude"
CLAUDE_PROJECTS_ROOT = CLAUDE_CONFIG_ROOT / "projects"
CLAUDE_VERSIONS_ROOT = Path.home() / ".local" / "share" / "claude" / "versions"
DATA_ROOT = Path(
    os.environ.get("CLAUDE_PLUGIN_DATA_DIR")
    or os.environ.get("BUDDYHUB_DATA_ROOT")
    or (Path.home() / ".claude" / "plugins" / "data" / "buddyhub")
)
OWNERSHIP_FILE = DATA_ROOT / "ownership.json"
NATIVE_PATCH_STATE_FILE = DATA_ROOT / "native-patch.json"
NATIVE_BACKUP_ROOT = DATA_ROOT / "native-backups"
NATIVE_WORK_ROOT = DATA_ROOT / "native-work"

PLUGIN_REF = "buddyhub@buddyhub"

SUPPORTED_PATCH_PROFILES: dict[str, dict[str, Any]] = {
    "2.1.92": {
        "profile_id": "blob_tophat_preview",
        "description": "Add a tophat row to the official blob Buddy frames.",
        "species": "blob",
        "element": "tophat",
        "replacements": [
            {
                "old": b'[uk_]:[["            ","   .----.   "',
                "new": b'[uk_]:[["   [___]    ","   .----.   "',
                "expected_matches": 2,
            },
            {
                "old": b'["            ","  .------.  "',
                "new": b'["   [___]    ","  .------.  "',
                "expected_matches": 2,
            },
            {
                "old": b'["            ","    .--.    "',
                "new": b'["   [___]    ","    .--.    "',
                "expected_matches": 2,
            },
        ],
    }
}

def ensure_data_root() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


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


def sha1_file(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def parse_semver(name: str) -> tuple[int, int, int] | None:
    parts = name.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def plugin_version() -> str:
    plugin_meta = read_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", {})
    return str(plugin_meta.get("version", "0.1.0"))


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
                str(OWNERSHIP_FILE),
                str(NATIVE_PATCH_STATE_FILE),
            ],
            "runtime_assets": [
                str(NATIVE_BACKUP_ROOT),
                str(NATIVE_WORK_ROOT),
            ],
            "config_integrations": {
                "native_patch_target": None,
            },
        }
        write_json(OWNERSHIP_FILE, manifest)
    return manifest


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
                attachment: dict[str, Any] | None = None
                if record.get("type") == "attachment":
                    candidate = record.get("attachment") or {}
                    if candidate.get("type") == "companion_intro":
                        attachment = candidate
                elif record.get("type") == "companion_intro":
                    attachment = record
                if not attachment:
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

def default_native_patch_state() -> dict[str, Any]:
    return {
        "version": 1,
        "rehearsal": None,
        "installed": None,
    }


def load_native_patch_state() -> dict[str, Any]:
    state = default_native_patch_state()
    state.update(read_json(NATIVE_PATCH_STATE_FILE, {}))
    return state


def save_native_patch_state(state: dict[str, Any]) -> None:
    write_json(NATIVE_PATCH_STATE_FILE, state)


def current_identity_from_projects() -> dict[str, Any]:
    if not CLAUDE_PROJECTS_ROOT.exists():
        return empty_identity()

    candidates: list[tuple[float, Path]] = []
    for path in CLAUDE_PROJECTS_ROOT.rglob("*.jsonl"):
        try:
            candidates.append((path.stat().st_mtime, path))
        except OSError:
            continue

    candidates.sort(key=lambda item: item[0], reverse=True)
    for _, path in candidates:
        identity = read_companion_intro(str(path))
        if identity:
            identity["transcript_path"] = str(path)
            return identity
    return empty_identity()


def detect_native_target() -> dict[str, Any]:
    override = os.environ.get("BUDDYHUB_CLAUDE_BINARY")
    result: dict[str, Any] = {
        "platform": sys.platform,
        "target_detected": False,
        "target_path": None,
        "target_version": None,
        "target_sha1": None,
        "install_root": None,
        "detection_mode": None,
        "profile_supported": False,
        "profile_id": None,
        "profile_description": None,
        "profile_species": None,
        "reason": None,
    }

    if override:
        candidate = Path(override).expanduser()
        result["detection_mode"] = "env"
        if candidate.exists() and candidate.is_file():
            version = candidate.name
            profile = SUPPORTED_PATCH_PROFILES.get(version)
            result.update(
                {
                    "target_detected": True,
                    "target_path": str(candidate),
                    "target_version": version,
                    "target_sha1": sha1_file(candidate),
                    "profile_supported": profile is not None,
                    "profile_id": profile.get("profile_id") if profile else None,
                    "profile_description": profile.get("description") if profile else None,
                    "profile_species": profile.get("species") if profile else None,
                    "reason": None if profile else "No supported patch profile for this binary version.",
                }
            )
            return result
        result["reason"] = "BUDDYHUB_CLAUDE_BINARY does not point to a readable file."
        return result

    if sys.platform != "darwin":
        result["reason"] = "Automatic native-target detection is currently validated only on macOS."
        return result

    result["install_root"] = str(CLAUDE_VERSIONS_ROOT)
    result["detection_mode"] = "macos-versions-dir"

    if not CLAUDE_VERSIONS_ROOT.exists():
        result["reason"] = "Claude versions directory does not exist on this machine."
        return result

    candidates: list[tuple[tuple[int, int, int], Path]] = []
    for path in CLAUDE_VERSIONS_ROOT.iterdir():
        if not path.is_file():
            continue
        semver = parse_semver(path.name)
        if semver is None:
            continue
        candidates.append((semver, path))

    if not candidates:
        result["reason"] = "No versioned Claude executable was found in the versions directory."
        return result

    candidates.sort(key=lambda item: item[0], reverse=True)
    _, target = candidates[0]
    version = target.name
    profile = SUPPORTED_PATCH_PROFILES.get(version)
    result.update(
        {
            "target_detected": True,
            "target_path": str(target),
            "target_version": version,
            "target_sha1": sha1_file(target),
            "profile_supported": profile is not None,
            "profile_id": profile.get("profile_id") if profile else None,
            "profile_description": profile.get("description") if profile else None,
            "profile_species": profile.get("species") if profile else None,
            "reason": None if profile else "No supported patch profile for the detected Claude version.",
        }
    )
    return result


def ensure_native_backup(target_path: Path, version: str) -> dict[str, Any]:
    ensure_data_root()
    NATIVE_BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    source_sha1 = sha1_file(target_path)
    backup_dir = NATIVE_BACKUP_ROOT / version
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{target_path.name}.{source_sha1}.bak"
    created = False
    if not backup_path.exists():
        shutil.copy2(target_path, backup_path)
        created = True
    return {
        "backup_path": str(backup_path),
        "created": created,
        "source_sha1": source_sha1,
    }


def existing_native_backup(target_path: Path, version: str) -> dict[str, Any] | None:
    source_sha1 = sha1_file(target_path)
    backup_path = NATIVE_BACKUP_ROOT / version / f"{target_path.name}.{source_sha1}.bak"
    if not backup_path.exists():
        return None
    return {
        "backup_path": str(backup_path),
        "created": False,
        "source_sha1": source_sha1,
    }


def rehearsal_copy_path(version: str) -> Path:
    return NATIVE_WORK_ROOT / version / f"claude-{version}-patched"


def apply_patch_profile_to_binary(binary_path: Path, profile: dict[str, Any]) -> list[dict[str, Any]]:
    data = binary_path.read_bytes()
    results: list[dict[str, Any]] = []
    for replacement in profile["replacements"]:
        old = replacement["old"]
        new = replacement["new"]
        expected_matches = replacement["expected_matches"]
        actual_matches = data.count(old)
        if actual_matches != expected_matches:
            raise RuntimeError(
                f"Patch profile mismatch for {profile['profile_id']}: expected {expected_matches} matches, got {actual_matches}."
            )
        data = data.replace(old, new)
        results.append(
            {
                "expected_matches": expected_matches,
                "actual_matches": actual_matches,
                "old_preview": old.decode("utf-8", "replace"),
                "new_preview": new.decode("utf-8", "replace"),
            }
        )
    binary_path.write_bytes(data)
    return results


def codesign_binary(binary_path: Path) -> dict[str, Any]:
    if sys.platform != "darwin":
        return {
            "required": False,
            "attempted": False,
            "ok": True,
            "output": None,
        }

    result = subprocess.run(  # noqa: S603
        ["codesign", "-f", "-s", "-", str(binary_path)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return {
        "required": True,
        "attempted": True,
        "ok": result.returncode == 0,
        "output": output.strip() or None,
    }


def verify_binary_launch(binary_path: Path) -> dict[str, Any]:
    result = subprocess.run(  # noqa: S603
        [str(binary_path), "--version"],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "output": output.strip() or None,
    }


def restore_binary_from_backup(target_path: Path, backup_path: Path) -> dict[str, Any]:
    shutil.copy2(backup_path, target_path)
    target_path.chmod(backup_path.stat().st_mode)
    launch_result = verify_binary_launch(target_path)
    return {
        "target_path": str(target_path),
        "backup_path": str(backup_path),
        "launch_check": launch_result,
    }


def inspect_native_patch(*, create_manifest: bool = False) -> dict[str, Any]:
    if create_manifest:
        ensure_ownership_manifest()
    detection = detect_native_target()
    identity = current_identity_from_projects()
    patch_state = load_native_patch_state()

    rehearsal = patch_state.get("rehearsal") or {}
    installed = patch_state.get("installed") or {}
    rehearsal_path = rehearsal.get("patched_copy_path")
    rehearsal_exists = bool(rehearsal_path and Path(rehearsal_path).exists())
    installed_present = bool(installed)
    target_appears_patched = bool(
        installed
        and detection.get("target_detected")
        and detection.get("target_path") == installed.get("target_path")
        and detection.get("target_sha1") == installed.get("patched_sha1")
    )

    backup = None
    if detection.get("target_detected") and detection.get("target_path") and detection.get("target_version"):
        backup = existing_native_backup(Path(detection["target_path"]), str(detection["target_version"]))

    profile_species = detection.get("profile_species")
    identity_species = identity.get("species")
    if not profile_species:
        profile_match = False
        profile_match_reason = detection.get("reason") or "No supported patch profile was found."
    elif not identity.get("available"):
        profile_match = False
        profile_match_reason = "Current Buddy identity is not verified yet."
    elif identity_species != profile_species:
        profile_match = False
        profile_match_reason = (
            f"Current Buddy species is {identity_species or 'unknown'}, but the available patch profile targets {profile_species}."
        )
    else:
        profile_match = True
        profile_match_reason = "Detected Buddy identity matches the available visual patch profile."

    return {
        "detection": detection,
        "identity": identity,
        "backup": backup,
        "patch_state": patch_state,
        "rehearsal_exists": rehearsal_exists,
        "rehearsal_path": rehearsal_path,
        "installed_present": installed_present,
        "target_appears_patched": target_appears_patched,
        "profile_match": profile_match,
        "profile_match_reason": profile_match_reason,
        "data_root": str(DATA_ROOT),
        "backup_root": str(NATIVE_BACKUP_ROOT),
        "work_root": str(NATIVE_WORK_ROOT),
        "patch_state_file": str(NATIVE_PATCH_STATE_FILE),
    }


def apply_rehearsal_patch() -> dict[str, Any]:
    ensure_ownership_manifest()
    inspection = inspect_native_patch(create_manifest=True)
    detection = inspection["detection"]

    if not detection.get("target_detected"):
        raise RuntimeError(detection.get("reason") or "No Claude Code target was detected.")
    if not detection.get("profile_supported"):
        raise RuntimeError(detection.get("reason") or "No supported patch profile is available.")
    if not inspection.get("profile_match"):
        raise RuntimeError(inspection.get("profile_match_reason") or "Patch profile does not match the current Buddy identity.")

    target_path = Path(str(detection["target_path"]))
    version = str(detection["target_version"])
    profile = SUPPORTED_PATCH_PROFILES[version]
    backup = ensure_native_backup(target_path, version)

    patched_copy = rehearsal_copy_path(version)
    patched_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target_path, patched_copy)
    patched_copy.chmod(target_path.stat().st_mode)

    patch_results = apply_patch_profile_to_binary(patched_copy, profile)
    codesign_result = codesign_binary(patched_copy)
    if not codesign_result["ok"]:
        raise RuntimeError(codesign_result["output"] or "codesign failed")
    launch_result = verify_binary_launch(patched_copy)
    if not launch_result["ok"]:
        raise RuntimeError(launch_result["output"] or "patched binary failed launch verification")

    patch_state = load_native_patch_state()
    patch_state["rehearsal"] = {
        "applied_at": now_iso(),
        "target_path": str(target_path),
        "target_version": version,
        "profile_id": profile["profile_id"],
        "profile_species": profile["species"],
        "backup_path": backup["backup_path"],
        "source_sha1": backup["source_sha1"],
        "patched_copy_path": str(patched_copy),
        "patched_sha1": sha1_file(patched_copy),
        "launch_check_output": launch_result["output"],
        "mode": "rehearsal",
    }
    save_native_patch_state(patch_state)

    return {
        "mode": "rehearsal",
        "target_path": str(target_path),
        "target_version": version,
        "profile_id": profile["profile_id"],
        "profile_description": profile["description"],
        "profile_species": profile["species"],
        "backup_path": backup["backup_path"],
        "backup_created": backup["created"],
        "patched_copy_path": str(patched_copy),
        "patched_sha1": sha1_file(patched_copy),
        "patch_results": patch_results,
        "codesign": codesign_result,
        "launch_check": launch_result,
        "manual_visual_check_required": True,
    }


def apply_installed_patch() -> dict[str, Any]:
    ensure_ownership_manifest()
    inspection = inspect_native_patch(create_manifest=True)
    detection = inspection["detection"]

    if not detection.get("target_detected"):
        raise RuntimeError(detection.get("reason") or "No Claude Code target was detected.")
    if not detection.get("profile_supported"):
        raise RuntimeError(detection.get("reason") or "No supported patch profile is available.")
    if not inspection.get("profile_match"):
        raise RuntimeError(inspection.get("profile_match_reason") or "Patch profile does not match the current Buddy identity.")

    target_path = Path(str(detection["target_path"]))
    version = str(detection["target_version"])
    profile = SUPPORTED_PATCH_PROFILES[version]
    if inspection.get("target_appears_patched"):
        raise RuntimeError(
            "Installed visual patch already appears to be present on the detected Claude target. "
            "Run restore first if you want to re-apply from a clean original binary."
        )
    backup = ensure_native_backup(target_path, version)

    try:
        patch_results = apply_patch_profile_to_binary(target_path, profile)
        codesign_result = codesign_binary(target_path)
        if not codesign_result["ok"]:
            raise RuntimeError(codesign_result["output"] or "codesign failed")
        launch_result = verify_binary_launch(target_path)
        if not launch_result["ok"]:
            raise RuntimeError(launch_result["output"] or "patched binary failed launch verification")
    except Exception as exc:
        restore_result = restore_binary_from_backup(target_path, Path(backup["backup_path"]))
        raise RuntimeError(
            f"Installed patch failed and backup restore was attempted: {exc}. "
            f"Restore launch ok={restore_result['launch_check']['ok']}"
        ) from exc

    patch_state = load_native_patch_state()
    patch_state["installed"] = {
        "applied_at": now_iso(),
        "target_path": str(target_path),
        "target_version": version,
        "profile_id": profile["profile_id"],
        "profile_species": profile["species"],
        "backup_path": backup["backup_path"],
        "source_sha1": backup["source_sha1"],
        "patched_sha1": sha1_file(target_path),
        "launch_check_output": launch_result["output"],
        "mode": "installed",
    }
    save_native_patch_state(patch_state)

    return {
        "mode": "installed",
        "target_path": str(target_path),
        "target_version": version,
        "profile_id": profile["profile_id"],
        "profile_description": profile["description"],
        "profile_species": profile["species"],
        "backup_path": backup["backup_path"],
        "backup_created": backup["created"],
        "patched_sha1": sha1_file(target_path),
        "patch_results": patch_results,
        "codesign": codesign_result,
        "launch_check": launch_result,
        "manual_visual_check_required": True,
    }


def restore_native_patch() -> dict[str, Any]:
    ensure_ownership_manifest()
    patch_state = load_native_patch_state()
    rehearsal = patch_state.get("rehearsal") or {}
    installed = patch_state.get("installed") or {}
    removed_paths: list[str] = []
    restored_target = None

    patched_copy_path = rehearsal.get("patched_copy_path")
    if patched_copy_path:
        path = Path(patched_copy_path)
        if path.exists():
            path.unlink()
            removed_paths.append(str(path))
            try:
                path.parent.rmdir()
                removed_paths.append(str(path.parent))
            except OSError:
                pass

    target_path = installed.get("target_path")
    backup_path = installed.get("backup_path")
    if target_path and backup_path:
        target = Path(target_path)
        backup = Path(backup_path)
        if target.exists() and backup.exists():
            restored_target = restore_binary_from_backup(target, backup)

    patch_state["rehearsal"] = None
    patch_state["installed"] = None
    save_native_patch_state(patch_state)

    return {
        "removed_paths": removed_paths,
        "backup_retained": bool((rehearsal.get("backup_path") or installed.get("backup_path"))),
        "backup_path": rehearsal.get("backup_path") or installed.get("backup_path"),
        "restored_target": restored_target,
        "restored_at": now_iso(),
    }

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from buddyhublib import (  # noqa: E402
    DATA_ROOT,
    PLUGIN_REF,
    diagnose,
    ensure_ownership_manifest,
    human_status_report,
    load_runtime,
    now_iso,
    read_hook_payload,
    record_hook_event,
    render_buddy_scene,
    render_buddy_statusline,
    set_lifecycle_state,
    snapshot,
    stop_legacy_runtime,
    update_runtime_preferences,
)


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def cmd_help(_: argparse.Namespace) -> int:
    print(human_status_report())
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    info = snapshot()
    if args.json:
        print_json(info)
        return 0
    print(render_buddy_scene(info, compact=True))
    return 0


def cmd_pause(_: argparse.Namespace) -> int:
    runtime = set_lifecycle_state("paused")
    print(
        "\n".join(
            [
                "# BuddyHub Paused",
                "",
                f"- Lifecycle: `{runtime['lifecycle_state']}`",
                "- Automatic Buddy updates are paused.",
                "- Claude Code remains unaffected.",
                "- Run `/buddyhub:resume` to turn BuddyHub back on.",
            ]
        )
    )
    return 0


def cmd_resume(_: argparse.Namespace) -> int:
    runtime = set_lifecycle_state("enabled")
    print(
        "\n".join(
            [
                "# BuddyHub Resumed",
                "",
                f"- Lifecycle: `{runtime['lifecycle_state']}`",
                "- BuddyHub is active again.",
                "- Use `/buddyhub:open` for the detailed text view.",
            ]
        )
    )
    return 0


def cmd_disable(_: argparse.Namespace) -> int:
    runtime = set_lifecycle_state("disabled")
    print(
        "\n".join(
            [
                "# BuddyHub Disabled",
                "",
                f"- Lifecycle: `{runtime['lifecycle_state']}`",
                "- BuddyHub has been turned off without uninstalling files.",
                "- Run `/buddyhub:resume` to enable it again.",
            ]
        )
    )
    return 0


def cmd_open(_: argparse.Namespace) -> int:
    info = snapshot()
    print(render_buddy_scene(info))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    payload = diagnose()
    if args.json:
        print_json(payload)
        return 0

    lines = [
        "# BuddyHub Doctor",
        "",
        f"- UI mode: `{payload['ui_mode']}`",
        f"- Lifecycle: `{payload['lifecycle_state']}`",
        f"- Buddy state: `{payload['current_state']}`",
        f"- Status line sync: `{str(payload['statusline_enabled']).lower()}`",
        f"- Legacy runtime assets present: `{str(payload['legacy_runtime_assets_present']).lower()}`",
        f"- Claude CLI available: `{str(payload['claude_cli_available']).lower()}`",
        f"- Ownership manifest exists: `{str(payload['ownership_manifest_exists']).lower()}`",
        f"- Runtime file exists: `{str(payload['runtime_file_exists']).lower()}`",
        f"- Sessions file exists: `{str(payload['sessions_file_exists']).lower()}`",
        f"- Active session: `{payload['active_session_id'] or 'none'}`",
        f"- Active project: `{payload['active_project'] or 'unknown'}`",
    ]
    print("\n".join(lines))
    return 0


def cmd_hook(args: argparse.Namespace) -> int:
    try:
        payload = read_hook_payload()
        event_name = args.event or payload.get("hook_event_name") or "unknown"
        record_hook_event(event_name, payload)
    except Exception as exc:  # noqa: BLE001
        print(f"BuddyHub hook degraded safely: {exc}", file=sys.stderr)
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    set_lifecycle_state("disabled")
    stop_legacy_runtime()
    removed_paths = []
    if DATA_ROOT.exists():
        for path in sorted(DATA_ROOT.iterdir(), reverse=True):
            if path.is_file():
                path.unlink(missing_ok=True)
                removed_paths.append(str(path))
        try:
            DATA_ROOT.rmdir()
            removed_paths.append(str(DATA_ROOT))
        except OSError:
            pass

    uninstall_result = {
        "attempted_plugin_uninstall": False,
        "plugin_uninstall_ok": False,
        "plugin_uninstall_output": None,
    }

    if not args.skip_plugin_remove:
        uninstall_result["attempted_plugin_uninstall"] = True
        try:
            result = subprocess.run(  # noqa: S603
                ["claude", "plugin", "uninstall", args.plugin_ref],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            combined = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
            uninstall_result["plugin_uninstall_ok"] = result.returncode == 0
            uninstall_result["plugin_uninstall_output"] = combined.strip() or None
        except Exception as exc:  # noqa: BLE001
            uninstall_result["plugin_uninstall_output"] = str(exc)

    if args.json:
        print_json(
            {
                "removed_paths": removed_paths,
                "cleanup_completed_at": now_iso(),
                **uninstall_result,
            }
        )
        return 0

    lines = [
        "# BuddyHub Uninstall",
        "",
        "- BuddyHub runtime cleanup completed.",
        f"- Removed paths: `{len(removed_paths)}`",
    ]

    if uninstall_result["attempted_plugin_uninstall"]:
        lines.append(f"- Plugin uninstall attempted: `{str(uninstall_result['plugin_uninstall_ok']).lower()}`")
        if uninstall_result["plugin_uninstall_output"]:
            lines.extend(["", "## Plugin uninstall output", "", "```text", uninstall_result["plugin_uninstall_output"], "```"])

    if not uninstall_result["plugin_uninstall_ok"]:
        lines.extend(
            [
                "",
                "## Final removal step",
                "",
                "If the plugin package still appears installed, run:",
                "",
                f"```bash\nclaude plugin uninstall {args.plugin_ref}\n```",
            ]
        )

    print("\n".join(lines))
    return 0


def cmd_statusline_on(_: argparse.Namespace) -> int:
    runtime = update_runtime_preferences(statusline_enabled=True)
    info = snapshot()
    print(
        "\n".join(
            [
                "# BuddyHub Status Line Requested",
                "",
                f"- Status line sync: `{str(runtime.get('statusline_enabled', False)).lower()}`",
                "- BuddyHub will provide status line output via the script below.",
                "- To surface it in Claude Code, point your Claude Code status line command at this script:",
                f"- `{info['paths']['statusline_script']}`",
            ]
        )
    )
    return 0


def cmd_statusline_off(_: argparse.Namespace) -> int:
    runtime = update_runtime_preferences(statusline_enabled=False)
    print(
        "\n".join(
            [
                "# BuddyHub Status Line Disabled",
                "",
                f"- Status line sync: `{str(runtime.get('statusline_enabled', False)).lower()}`",
                "- BuddyHub will no longer report status line mode as requested.",
            ]
        )
    )
    return 0


def cmd_statusline(_: argparse.Namespace) -> int:
    info = snapshot()
    print(render_buddy_statusline(info))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BuddyHub runtime controller")
    subparsers = parser.add_subparsers(dest="command", required=True)

    help_parser = subparsers.add_parser("help")
    help_parser.set_defaults(func=cmd_help)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--json", action="store_true")
    status_parser.set_defaults(func=cmd_status)

    pause_parser = subparsers.add_parser("pause")
    pause_parser.set_defaults(func=cmd_pause)

    resume_parser = subparsers.add_parser("resume")
    resume_parser.set_defaults(func=cmd_resume)

    disable_parser = subparsers.add_parser("disable")
    disable_parser.set_defaults(func=cmd_disable)

    open_parser = subparsers.add_parser("open")
    open_parser.set_defaults(func=cmd_open)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.set_defaults(func=cmd_doctor)

    hook_parser = subparsers.add_parser("hook")
    hook_parser.add_argument("event")
    hook_parser.set_defaults(func=cmd_hook)

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("--skip-plugin-remove", action="store_true")
    uninstall_parser.add_argument("--plugin-ref", default=PLUGIN_REF)
    uninstall_parser.add_argument("--json", action="store_true")
    uninstall_parser.set_defaults(func=cmd_uninstall)

    statusline_on_parser = subparsers.add_parser("statusline-on")
    statusline_on_parser.set_defaults(func=cmd_statusline_on)

    statusline_off_parser = subparsers.add_parser("statusline-off")
    statusline_off_parser.set_defaults(func=cmd_statusline_off)

    statusline_parser = subparsers.add_parser("statusline")
    statusline_parser.set_defaults(func=cmd_statusline)

    return parser


def main() -> int:
    ensure_ownership_manifest()
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

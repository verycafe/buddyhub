#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from buddyhublib import (  # noqa: E402
    DATA_ROOT,
    PLUGIN_REF,
    apply_installed_patch,
    apply_rehearsal_patch,
    inspect_native_patch,
    now_iso,
    restore_native_patch,
)


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def cmd_help(_: argparse.Namespace) -> int:
    inspection = inspect_native_patch()
    detection = inspection["detection"]
    identity = inspection["identity"]
    lines = [
        "# BuddyHub",
        "",
        "- Focus: native visual enhancement for the official bottom-right Claude Code Buddy.",
        "- Out of scope for this phase: runtime state, hooks, status line, and parallel Buddy UIs.",
        "- Current verified Buddy identity is preserved; BuddyHub does not invent a replacement pet.",
        "",
        "Commands",
        "",
        "- `/buddyhub:help`",
        "- `/buddyhub:inspect`",
        "- `/buddyhub:apply`",
        "- `/buddyhub:restore`",
        "- `/buddyhub:doctor`",
        "- `/buddyhub:uninstall`",
        "",
        "Current detection",
        "",
        f"- Platform: `{detection['platform']}`",
        f"- Target detected: `{str(detection['target_detected']).lower()}`",
        f"- Target version: `{detection.get('target_version') or 'unknown'}`",
        f"- Verified Buddy: `{identity.get('name') or 'unknown'} / {identity.get('species') or 'unknown'}`",
    ]
    if detection.get("target_path"):
        lines.append(f"- Target path: `{detection['target_path']}`")
    if detection.get("reason"):
        lines.append(f"- Detection note: {detection['reason']}")
    print("\n".join(lines))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    info = inspect_native_patch()
    if args.json:
        print_json(info)
        return 0

    detection = info["detection"]
    identity = info["identity"]
    backup = info["backup"] or {}
    lines = [
        "# BuddyHub Inspect",
        "",
        f"- Platform: `{detection['platform']}`",
        f"- Target detected: `{str(detection['target_detected']).lower()}`",
        f"- Detection mode: `{detection.get('detection_mode') or 'unknown'}`",
        f"- Target version: `{detection.get('target_version') or 'unknown'}`",
        f"- Patch profile supported: `{str(detection.get('profile_supported', False)).lower()}`",
        f"- Patch profile: `{detection.get('profile_id') or 'none'}`",
        f"- Patch target species: `{detection.get('profile_species') or 'unknown'}`",
        f"- Verified Buddy name: `{identity.get('name') or 'unknown'}`",
        f"- Verified Buddy species: `{identity.get('species') or 'unknown'}`",
        f"- Profile matches current Buddy: `{str(info['profile_match']).lower()}`",
    ]
    if detection.get("target_path"):
        lines.append(f"- Target path: `{detection['target_path']}`")
    if detection.get("target_sha1"):
        lines.append(f"- Target sha1: `{detection['target_sha1']}`")
    if backup.get("backup_path"):
        lines.append(f"- Backup path: `{backup['backup_path']}`")
    lines.append(f"- Rehearsal copy exists: `{str(info['rehearsal_exists']).lower()}`")
    if info.get("rehearsal_path"):
        lines.append(f"- Rehearsal copy path: `{info['rehearsal_path']}`")
    lines.extend(
        [
            "",
            "Profile match note",
            "",
            info["profile_match_reason"],
        ]
    )
    print("\n".join(lines))
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    if args.target == "installed":
        result = apply_installed_patch()
    else:
        result = apply_rehearsal_patch()
    if args.json:
        print_json(result)
        return 0

    lines = [
        "# BuddyHub Apply",
        "",
        f"- Mode: `{result['mode']}`",
        f"- Target version: `{result['target_version']}`",
        f"- Target path: `{result['target_path']}`",
        f"- Patch profile: `{result['profile_id']}`",
        f"- Patch target species: `{result['profile_species']}`",
        f"- Backup created: `{str(result['backup_created']).lower()}`",
        f"- Backup path: `{result['backup_path']}`",
        f"- Patched target sha1: `{result['patched_sha1']}`",
        f"- Launch verification: `{str(result['launch_check']['ok']).lower()}`",
    ]
    if result.get("patched_copy_path"):
        lines.append(f"- Patched copy: `{result['patched_copy_path']}`")
    if result["launch_check"].get("output"):
        lines.extend(
            [
                "",
                "## Launch output",
                "",
                "```text",
                result["launch_check"]["output"],
                "```",
            ]
        )
    lines.extend(
        [
            "",
            "## Next step",
            "",
        ]
    )
    if result["mode"] == "rehearsal":
        lines.extend(
            [
                "- This command patches a rehearsal copy only. It does not modify your installed Claude Code binary.",
                f"- Launch `{result['patched_copy_path']}` manually and verify the official bottom-right Buddy visually changed.",
            ]
        )
    else:
        lines.extend(
            [
                "- This command patched the detected Claude Code target directly after creating a backup.",
                "- Restart Claude Code and visually verify the official bottom-right Buddy changed.",
                "- Use `/buddyhub:restore` if you want to roll the target back to the original binary.",
            ]
        )
    print("\n".join(lines))
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    result = restore_native_patch()
    if args.json:
        print_json(result)
        return 0

    lines = [
        "# BuddyHub Restore",
        "",
        f"- Removed paths: `{len(result['removed_paths'])}`",
        f"- Backup retained: `{str(result['backup_retained']).lower()}`",
        f"- Backup path: `{result.get('backup_path') or 'none'}`",
    ]
    if result["removed_paths"]:
        lines.extend(
            [
                "",
                "## Removed",
                "",
                *[f"- `{path}`" for path in result["removed_paths"]],
            ]
        )
    print("\n".join(lines))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    payload = inspect_native_patch()
    if args.json:
        print_json(payload)
        return 0

    detection = payload["detection"]
    identity = payload["identity"]
    rehearsal = (payload["patch_state"] or {}).get("rehearsal") or {}
    lines = [
        "# BuddyHub Doctor",
        "",
        f"- Platform: `{detection['platform']}`",
        f"- Target detected: `{str(detection['target_detected']).lower()}`",
        f"- Target path: `{detection.get('target_path') or 'unknown'}`",
        f"- Target version: `{detection.get('target_version') or 'unknown'}`",
        f"- Target sha1: `{detection.get('target_sha1') or 'unknown'}`",
        f"- Profile supported: `{str(detection.get('profile_supported', False)).lower()}`",
        f"- Profile id: `{detection.get('profile_id') or 'none'}`",
        f"- Profile species: `{detection.get('profile_species') or 'unknown'}`",
        f"- Verified Buddy name: `{identity.get('name') or 'unknown'}`",
        f"- Verified Buddy species: `{identity.get('species') or 'unknown'}`",
        f"- Identity source: `{identity.get('source') or 'unknown'}`",
        f"- Profile matches current Buddy: `{str(payload['profile_match']).lower()}`",
        f"- Rehearsal copy exists: `{str(payload['rehearsal_exists']).lower()}`",
        f"- Rehearsal copy path: `{payload.get('rehearsal_path') or 'none'}`",
        f"- Installed patch present: `{str(bool((payload.get('patch_state') or {}).get('installed'))).lower()}`",
        f"- Backup path: `{(payload.get('backup') or {}).get('backup_path') or 'none'}`",
        f"- Patch state file: `{payload['patch_state_file']}`",
        f"- Data root: `{payload['data_root']}`",
        f"- Backup root: `{payload['backup_root']}`",
        f"- Work root: `{payload['work_root']}`",
        f"- Claude CLI available: `{str(shutil.which('claude') is not None).lower()}`",
    ]
    if detection.get("reason"):
        lines.append(f"- Detection note: {detection['reason']}")
    if rehearsal.get("launch_check_output"):
        lines.extend(
            [
                "",
                "## Rehearsal launch output",
                "",
                "```text",
                rehearsal["launch_check_output"],
                "```",
            ]
        )
    lines.extend(["", "## Profile match note", "", payload["profile_match_reason"]])
    print("\n".join(lines))
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    restore_result = restore_native_patch()
    removed_paths = list(restore_result["removed_paths"])
    if DATA_ROOT.exists():
        shutil.rmtree(DATA_ROOT)
        removed_paths.append(str(DATA_ROOT))

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
                "restore_result": restore_result,
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
        f"- Rehearsal backup retained: `{str(restore_result['backup_retained']).lower()}`",
        f"- Rehearsal backup path: `{restore_result.get('backup_path') or 'none'}`",
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

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BuddyHub native Buddy patch helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    help_parser = subparsers.add_parser("help")
    help_parser.set_defaults(func=cmd_help)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--json", action="store_true")
    inspect_parser.set_defaults(func=cmd_inspect)

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--target", choices=("rehearsal", "installed"), default="rehearsal")
    apply_parser.add_argument("--json", action="store_true")
    apply_parser.set_defaults(func=cmd_apply)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--json", action="store_true")
    restore_parser.set_defaults(func=cmd_restore)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.set_defaults(func=cmd_doctor)

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("--skip-plugin-remove", action="store_true")
    uninstall_parser.add_argument("--plugin-ref", default=PLUGIN_REF)
    uninstall_parser.add_argument("--json", action="store_true")
    uninstall_parser.set_defaults(func=cmd_uninstall)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001
        print(f"BuddyHub error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

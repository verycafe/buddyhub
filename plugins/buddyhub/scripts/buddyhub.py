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
    COLOR_PRESETS,
    ELEMENT_CATALOG,
    PLUGIN_REF,
    apply_installed_patch,
    apply_rehearsal_patch,
    load_customization_settings,
    inspect_native_patch,
    now_iso,
    preview_lines_for_customization,
    restore_native_patch,
    update_customization_settings,
)


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def profile_summary(profile: dict | None) -> dict | None:
    if not profile:
        return None
    color_patch = profile.get("color_patch") or {}
    return {
        "profile_id": profile.get("profile_id"),
        "description": profile.get("description"),
        "species": profile.get("species"),
        "element_id": profile.get("element_id"),
        "slot": profile.get("slot"),
        "supports_colors": profile.get("supports_colors", []),
        "nickname_supported": bool(profile.get("nickname_supported")),
        "active_color_id": profile.get("active_color_id"),
        "color_patch_id": color_patch.get("color_id"),
    }


def customization_for_json(customization: dict) -> dict:
    payload = dict(customization)
    payload["profile"] = profile_summary(customization.get("profile"))
    return payload


def read_hook_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def emit_hook_response(
    *,
    continue_run: bool = True,
    suppress_output: bool = True,
    system_message: str | None = None,
) -> None:
    payload: dict[str, object] = {
        "continue": continue_run,
        "suppressOutput": suppress_output,
    }
    if system_message:
        payload["systemMessage"] = system_message
    print_json(payload)


def cmd_help(_: argparse.Namespace) -> int:
    inspection = inspect_native_patch()
    detection = inspection["detection"]
    identity = inspection["identity"]
    companion_config = inspection["companion_config"]
    settings = inspection["settings"]
    effective_settings = inspection.get("effective_settings") or settings
    customization = inspection["customization"]
    current_profile = inspection.get("current_profile") or {}
    lines = [
        "# BuddyHub",
        "",
        "- Focus: native visual customization for the official bottom-right Claude Code Buddy.",
        "- Out of scope for this phase: runtime state, hooks, status line, and parallel Buddy UIs.",
        "- Current verified Buddy identity is preserved; BuddyHub does not invent a replacement pet.",
        "- Apply writes the current saved customization into the Claude Code target and then requires a restart.",
        "",
        "Commands",
        "",
        "- `/buddyhub:help`",
        "- `/buddyhub:settings`",
        "- `/buddyhub:color`",
        "- `/buddyhub:color-green`",
        "- `/buddyhub:color-orange`",
        "- `/buddyhub:color-blue`",
        "- `/buddyhub:color-pink`",
        "- `/buddyhub:color-purple`",
        "- `/buddyhub:color-red`",
        "- `/buddyhub:color-black`",
        "- `/buddyhub:clear-color`",
        "- `/buddyhub:nickname <short-name>`",
        "- `/buddyhub:clear-nickname`",
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
        f"- Current display name source: `{companion_config.get('name') or 'unknown'}` from `{companion_config.get('path')}`",
        f"- Saved element: `{settings.get('element_id') or 'none'}`",
        f"- Saved color: `{settings.get('color_id') or 'none'}`",
        f"- Saved nickname: `{settings.get('nickname') or 'none'}`",
        f"- Effective element: `{effective_settings.get('element_id') or 'none'}`",
        f"- Effective color: `{effective_settings.get('color_id') or 'none'}`",
        f"- Effective nickname: `{effective_settings.get('nickname') or 'none'}`",
        f"- Apply ready: `{str(customization.get('can_apply', False)).lower()}`",
    ]
    if current_profile.get("profile_id"):
        lines.append(f"- Current installed element: `{current_profile.get('element_id')}`")
    if detection.get("target_path"):
        lines.append(f"- Target path: `{detection['target_path']}`")
    if customization.get("apply_blockers"):
        lines.append(f"- Apply note: {'; '.join(customization['apply_blockers'])}")
    elif customization.get("apply_warnings"):
        lines.append(f"- Apply note: {'; '.join(customization['apply_warnings'])}")
    elif customization.get("profile_reason"):
        lines.append(f"- Apply note: {customization['profile_reason']}")
    print("\n".join(lines))
    return 0


def cmd_settings(args: argparse.Namespace) -> int:
    if args.reset:
        settings = update_customization_settings(reset=True)
    elif any(
        value is not None
        for value in (args.element, args.color, args.nickname)
    ) or args.clear_nickname or args.clear_color:
        settings = update_customization_settings(
            element_id=args.element,
            color_id=args.color,
            nickname=args.nickname,
            clear_nickname=args.clear_nickname,
            clear_color=args.clear_color,
        )
    else:
        settings = load_customization_settings()

    inspection = inspect_native_patch()
    detection = inspection["detection"]
    identity = inspection["identity"]
    companion_config = inspection["companion_config"]
    customization = inspection["customization"]
    effective_settings = inspection.get("effective_settings") or customization["effective_settings"]
    runtime_overrides = inspection.get("runtime_overrides") or {}
    current_profile = inspection.get("current_profile") or {}
    preview_lines = preview_lines_for_customization(customization)

    if args.json:
        print_json(
            {
                "settings": settings,
                "effective_settings": effective_settings,
                "runtime_overrides": runtime_overrides,
                "identity": identity,
                "companion_config": companion_config,
                "detection": detection,
                "customization": customization_for_json(customization),
                "current_profile": current_profile,
                "preview_lines": preview_lines,
            }
        )
        return 0

    lines = [
        "# BuddyHub Settings",
        "",
        "Slash-command settings menu for official Buddy color and nickname.",
        "",
        f"- Color: `{settings.get('color_id') or 'none'}`",
        f"- Nickname: `{settings.get('nickname') or 'none'}`",
        f"- Effective color on apply: `{effective_settings.get('color_id') or 'none'}`",
        f"- Effective nickname on apply: `{effective_settings.get('nickname') or 'none'}`",
        "",
        "Commands",
        "",
        "- `/buddyhub:color`",
        "- `/buddyhub:color-green`",
        "- `/buddyhub:color-orange`",
        "- `/buddyhub:color-blue`",
        "- `/buddyhub:color-pink`",
        "- `/buddyhub:color-purple`",
        "- `/buddyhub:color-red`",
        "- `/buddyhub:color-black`",
        "- `/buddyhub:clear-color`",
        "- `/buddyhub:nickname <short-name>`",
        "- `/buddyhub:clear-nickname`",
        "- `/buddyhub:inspect`",
        "- `/buddyhub:apply`",
    ]

    blockers = customization.get("apply_blockers") or []
    if blockers:
        lines.extend(["", "Current blockers", "", *[f"- {blocker}" for blocker in blockers]])
    warnings = customization.get("apply_warnings") or []
    if warnings:
        lines.extend(["", "Pending unsupported settings", "", *[f"- {warning}" for warning in warnings]])
    if runtime_overrides.get("has_any_value"):
        lines.extend(
            [
                "",
                "Native `/config` overrides",
                "",
                f"- Color toggles enabled: `{', '.join(runtime_overrides.get('selected_colors') or []) or 'none'}`",
                f"- Nickname from native menu: `{runtime_overrides.get('nickname') or 'blank'}`",
            ]
        )
    lines.extend(
        [
            "",
            "Quick status",
            "",
            f"- Verified Buddy: `{identity.get('name') or 'unknown'} / {identity.get('species') or 'unknown'}`",
            f"- Current displayed name: `{companion_config.get('name') or 'unknown'}`",
            f"- Apply ready: `{str(customization.get('can_apply', False)).lower()}`",
            "- Use `/buddyhub:inspect` for full diagnostics and preview details.",
        ]
    )
    print("\n".join(lines))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    info = inspect_native_patch()
    if args.json:
        payload = dict(info)
        payload["customization"] = customization_for_json(info["customization"])
        payload["effective_profile"] = profile_summary(info.get("effective_profile"))
        print_json(payload)
        return 0

    detection = info["detection"]
    identity = info["identity"]
    companion_config = info["companion_config"]
    settings = info["settings"]
    effective_settings = info.get("effective_settings") or settings
    runtime_overrides = info.get("runtime_overrides") or {}
    customization = info["customization"]
    current_profile = info.get("current_profile") or {}
    selected_target_status = info.get("selected_target_status") or {}
    surface_sync = info.get("surface_sync") or {}
    backup = info["backup"] or {}
    lines = [
        "# BuddyHub Inspect",
        "",
        f"- Platform: `{detection['platform']}`",
        f"- Target detected: `{str(detection['target_detected']).lower()}`",
        f"- Detection mode: `{detection.get('detection_mode') or 'unknown'}`",
        f"- Target version: `{detection.get('target_version') or 'unknown'}`",
        f"- Patch profile supported: `{str(detection.get('profile_supported', False)).lower()}`",
        f"- Default profile: `{detection.get('profile_id') or 'none'}`",
        f"- Verified Buddy name: `{identity.get('name') or 'unknown'}`",
        f"- Verified Buddy species: `{identity.get('species') or 'unknown'}`",
        f"- Current displayed name: `{companion_config.get('name') or 'unknown'}`",
        f"- Name config path: `{companion_config.get('path')}`",
        f"- Saved element: `{settings.get('element_id') or 'none'}`",
        f"- Saved color: `{settings.get('color_id') or 'none'}`",
        f"- Saved nickname: `{settings.get('nickname') or 'none'}`",
        f"- Effective element on apply: `{effective_settings.get('element_id') or 'none'}`",
        f"- Effective color on apply: `{effective_settings.get('color_id') or 'none'}`",
        f"- Effective nickname on apply: `{effective_settings.get('nickname') or 'none'}`",
        f"- Selected customization can apply: `{str(info['profile_match']).lower()}`",
        f"- Selected target patch status: `{selected_target_status.get('status') or 'unknown'}`",
    ]
    if runtime_overrides.get("has_any_value"):
        lines.append(f"- Native menu source: `{runtime_overrides.get('source')}`")
        lines.append(f"- Native element toggles: `{', '.join(runtime_overrides.get('selected_elements') or []) or 'none'}`")
        lines.append(f"- Native color toggles: `{', '.join(runtime_overrides.get('selected_colors') or []) or 'none'}`")
        lines.append(f"- Native nickname: `{runtime_overrides.get('nickname') or 'blank'}`")
    if surface_sync.get("surfaces"):
        labels = ", ".join(item["label"] for item in surface_sync["surfaces"])
        lines.append(f"- Synced official surfaces: `{labels}`")
        lines.append(f"- Element sync across surfaces: `{str(bool(surface_sync.get('element_sync'))).lower()}`")
        lines.append(f"- Color sync across surfaces: `{str(bool(surface_sync.get('color_sync'))).lower()}`")
        lines.append(f"- Nickname sync across surfaces: `{str(bool(surface_sync.get('nickname_sync'))).lower()}`")
    if surface_sync.get("name_source"):
        lines.append(f"- Name sync source: `{surface_sync['name_source']}`")
    if surface_sync.get("color_source"):
        lines.append(f"- Color sync source: `{surface_sync['color_source']}`")
    if current_profile.get("profile_id"):
        lines.append(f"- Current installed Buddy element: `{current_profile.get('element_id')}`")
        lines.append(f"- Current installed profile id: `{current_profile.get('profile_id')}`")
    if detection.get("target_path"):
        lines.append(f"- Target path: `{detection['target_path']}`")
    if detection.get("target_sha1"):
        lines.append(f"- Target sha1: `{detection['target_sha1']}`")
    if backup.get("backup_path"):
        lines.append(f"- Backup path: `{backup['backup_path']}`")
    lines.append(f"- Rehearsal copy exists: `{str(info['rehearsal_exists']).lower()}`")
    if info.get("rehearsal_path"):
        lines.append(f"- Rehearsal copy path: `{info['rehearsal_path']}`")
    if customization.get("profile"):
        lines.append(f"- Selected profile: `{customization['profile']['profile_id']}`")
    lines.extend(
        [
            "",
            "Apply note",
            "",
            info["profile_match_reason"],
        ]
    )
    if customization.get("apply_warnings"):
        lines.extend(["", "Pending unsupported settings", "", *[f"- {warning}" for warning in customization["apply_warnings"]]])
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
        f"- Saved element: `{result['saved_settings'].get('element_id') or 'none'}`",
        f"- Saved color: `{result['saved_settings'].get('color_id') or 'none'}`",
        f"- Saved nickname: `{result['saved_settings'].get('nickname') or 'none'}`",
        f"- Applied element: `{result['settings'].get('element_id') or 'none'}`",
        f"- Applied color: `{result['settings'].get('color_id') or 'none'}`",
        f"- Applied nickname: `{result['settings'].get('nickname') or 'none'}`",
        f"- Backup created: `{str(result['backup_created']).lower()}`",
        f"- Backup path: `{result['backup_path']}`",
        f"- Patched target sha1: `{result['patched_sha1']}`",
        f"- Launch verification: `{str(result['launch_check']['ok']).lower()}`",
    ]
    surface_sync = result.get("surface_sync") or {}
    if surface_sync.get("surfaces"):
        labels = ", ".join(item["label"] for item in surface_sync["surfaces"])
        lines.append(f"- Synced official surfaces: `{labels}`")
        lines.append(f"- Element sync across surfaces: `{str(bool(surface_sync.get('element_sync'))).lower()}`")
        lines.append(f"- Color sync across surfaces: `{str(bool(surface_sync.get('color_sync'))).lower()}`")
        lines.append(f"- Nickname sync across surfaces: `{str(bool(surface_sync.get('nickname_sync'))).lower()}`")
    if surface_sync.get("name_source"):
        lines.append(f"- Name sync source: `{surface_sync['name_source']}`")
    if surface_sync.get("color_source"):
        lines.append(f"- Color sync source: `{surface_sync['color_source']}`")
    companion_name_patch = result.get("companion_name_patch") or {}
    if companion_name_patch:
        lines.append(f"- Displayed name sync: `{companion_name_patch.get('mode')}`")
        lines.append(f"- Display name config: `{companion_name_patch.get('config_path')}`")
        if companion_name_patch.get("applied_name"):
            lines.append(f"- Applied display name: `{companion_name_patch['applied_name']}`")
    if result.get("already_present"):
        lines.append("- Target already matched the selected official Buddy element. BuddyHub refreshed its installed patch record to match the actual binary on disk.")
    if result.get("target_restored_from_backup"):
        lines.append("- Target was first restored from backup so the new element could replace an older patch cleanly.")
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
    if result.get("apply_warnings"):
        lines.extend(["", "## Pending unsupported settings", "", *[f"- {warning}" for warning in result["apply_warnings"]]])
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
                (
                    "- The detected Claude Code target was already using the selected Buddy element."
                    if result.get("already_present")
                    else "- This command patched the detected Claude Code target directly after creating a backup."
                ),
                (
                    "- Restart Claude Code only if it was already open and you need the running app to reload the current Buddy."
                    if result.get("already_present")
                    else "- Restart Claude Code. The currently running process will not hot-reload this Buddy visual change."
                ),
                (
                    "- After restart, verify both the official bottom-right Buddy and the `/buddy` card still match the selected element, color, and displayed name."
                    if result.get("already_present")
                    else "- After restart, visually verify both the official bottom-right Buddy and the `/buddy` card changed."
                ),
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
    if result.get("restored_companion_name"):
        lines.append(f"- Restored display name config: `{result['restored_companion_name']['config_path']}`")
    if result.get("restored_surfaces"):
        lines.append(f"- Restored official surfaces: `{', '.join(result['restored_surfaces'])}`")
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
        json_payload = dict(payload)
        json_payload["customization"] = customization_for_json(payload["customization"])
        json_payload["effective_profile"] = profile_summary(payload.get("effective_profile"))
        print_json(json_payload)
        return 0

    detection = payload["detection"]
    identity = payload["identity"]
    companion_config = payload["companion_config"]
    settings = payload["settings"]
    effective_settings = payload.get("effective_settings") or settings
    runtime_overrides = payload.get("runtime_overrides") or {}
    customization = payload["customization"]
    current_profile = payload.get("current_profile") or {}
    selected_target_status = payload.get("selected_target_status") or {}
    surface_sync = payload.get("surface_sync") or {}
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
        f"- Default profile id: `{detection.get('profile_id') or 'none'}`",
        f"- Verified Buddy name: `{identity.get('name') or 'unknown'}`",
        f"- Verified Buddy species: `{identity.get('species') or 'unknown'}`",
        f"- Identity source: `{identity.get('source') or 'unknown'}`",
        f"- Current displayed name: `{companion_config.get('name') or 'unknown'}`",
        f"- Name config path: `{companion_config.get('path')}`",
        f"- Saved element: `{settings.get('element_id') or 'none'}`",
        f"- Saved color: `{settings.get('color_id') or 'none'}`",
        f"- Saved nickname: `{settings.get('nickname') or 'none'}`",
        f"- Effective element on apply: `{effective_settings.get('element_id') or 'none'}`",
        f"- Effective color on apply: `{effective_settings.get('color_id') or 'none'}`",
        f"- Effective nickname on apply: `{effective_settings.get('nickname') or 'none'}`",
        f"- Selected customization can apply: `{str(payload['profile_match']).lower()}`",
        f"- Selected profile id: `{(customization.get('profile') or {}).get('profile_id') or 'none'}`",
        f"- Selected target patch status: `{selected_target_status.get('status') or 'unknown'}`",
        f"- Current installed Buddy element: `{current_profile.get('element_id') or 'none'}`",
        f"- Current installed profile id: `{current_profile.get('profile_id') or 'none'}`",
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
    if runtime_overrides.get("has_any_value"):
        lines.append(f"- Native menu source: `{runtime_overrides.get('source')}`")
        lines.append(f"- Native element toggles: `{', '.join(runtime_overrides.get('selected_elements') or []) or 'none'}`")
        lines.append(f"- Native color toggles: `{', '.join(runtime_overrides.get('selected_colors') or []) or 'none'}`")
        lines.append(f"- Native nickname: `{runtime_overrides.get('nickname') or 'blank'}`")
    if surface_sync.get("surfaces"):
        labels = ", ".join(item["label"] for item in surface_sync["surfaces"])
        lines.append(f"- Synced official surfaces: `{labels}`")
        lines.append(f"- Element sync across surfaces: `{str(bool(surface_sync.get('element_sync'))).lower()}`")
        lines.append(f"- Color sync across surfaces: `{str(bool(surface_sync.get('color_sync'))).lower()}`")
        lines.append(f"- Nickname sync across surfaces: `{str(bool(surface_sync.get('nickname_sync'))).lower()}`")
    if surface_sync.get("name_source"):
        lines.append(f"- Name sync source: `{surface_sync['name_source']}`")
    if surface_sync.get("color_source"):
        lines.append(f"- Color sync source: `{surface_sync['color_source']}`")
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
    lines.extend(["", "## Apply note", "", payload["profile_match_reason"]])
    if customization.get("apply_blockers"):
        lines.extend(["", "## Apply blockers", "", *[f"- {blocker}" for blocker in customization["apply_blockers"]]])
    if customization.get("apply_warnings"):
        lines.extend(["", "## Pending unsupported settings", "", *[f"- {warning}" for warning in customization["apply_warnings"]]])
    print("\n".join(lines))
    return 0


def cmd_hook(args: argparse.Namespace) -> int:
    payload = read_hook_payload()
    event_name = args.event or payload.get("hook_event_name") or "unknown"
    if event_name != "SessionStart":
        emit_hook_response()
        return 0

    try:
        inspection = inspect_native_patch(create_manifest=True)
        customization = inspection["customization"]
        settings = inspection.get("effective_settings") or inspection["settings"]
        detection = inspection["detection"]
        already_patched = inspection.get("target_appears_patched", False)

        if not detection.get("target_detected") or not detection.get("profile_supported"):
            emit_hook_response()
            return 0

        if already_patched:
            emit_hook_response()
            return 0

        if not customization.get("can_apply"):
            selected_values = []
            if settings.get("element_id"):
                selected_values.append(f"element={settings['element_id']}")
            if settings.get("color_id"):
                selected_values.append(f"color={settings['color_id']}")
            if settings.get("nickname"):
                selected_values.append(f"nickname={settings['nickname']}")
            if selected_values:
                emit_hook_response(
                    suppress_output=False,
                    system_message=(
                        "BuddyHub found current Buddy customization settings that cannot be auto-applied on this target: "
                        + ", ".join(selected_values)
                        + ". Ask the user to review `/buddyhub:settings` before continuing."
                    ),
                )
            else:
                emit_hook_response()
            return 0

        result = apply_installed_patch()
        warning_suffix = ""
        if result.get("apply_warnings"):
            warning_suffix = " Some current settings remain pending: " + "; ".join(result["apply_warnings"])
        emit_hook_response(
            suppress_output=False,
            system_message=(
                "BuddyHub auto-applied the current official Buddy customization "
                f"(`{result['settings'].get('element_id') or 'none'}`) to the detected Claude Code target. "
                "Ask the user to restart Claude Code to see the updated bottom-right Buddy."
                + warning_suffix
            ),
        )
    except Exception as exc:  # noqa: BLE001
        emit_hook_response(
            suppress_output=False,
            system_message=(
                "BuddyHub could not auto-apply the current official Buddy customization: "
                f"{exc}. Ask the user to run `/buddyhub:doctor` or `/buddyhub:settings`."
            ),
        )
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

    settings_parser = subparsers.add_parser("settings")
    settings_parser.add_argument("--element", choices=sorted(ELEMENT_CATALOG.keys()))
    settings_parser.add_argument("--color", choices=sorted(COLOR_PRESETS.keys()))
    settings_parser.add_argument("--nickname")
    settings_parser.add_argument("--clear-color", action="store_true")
    settings_parser.add_argument("--clear-nickname", action="store_true")
    settings_parser.add_argument("--reset", action="store_true")
    settings_parser.add_argument("--json", action="store_true")
    settings_parser.set_defaults(func=cmd_settings)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--json", action="store_true")
    inspect_parser.set_defaults(func=cmd_inspect)

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--target", choices=("rehearsal", "installed"), default="installed")
    apply_parser.add_argument("--json", action="store_true")
    apply_parser.set_defaults(func=cmd_apply)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--json", action="store_true")
    restore_parser.set_defaults(func=cmd_restore)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.set_defaults(func=cmd_doctor)

    hook_parser = subparsers.add_parser("hook")
    hook_parser.add_argument("event", nargs="?")
    hook_parser.set_defaults(func=cmd_hook)

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

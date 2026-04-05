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
CLAUDE_JSON_FILE = Path(
    os.environ.get("BUDDYHUB_CLAUDE_JSON")
    or (Path.home() / ".claude.json")
)
DATA_ROOT = Path(
    os.environ.get("CLAUDE_PLUGIN_DATA_DIR")
    or os.environ.get("BUDDYHUB_DATA_ROOT")
    or (Path.home() / ".claude" / "plugins" / "data" / "buddyhub")
)
OWNERSHIP_FILE = DATA_ROOT / "ownership.json"
NATIVE_PATCH_STATE_FILE = DATA_ROOT / "native-patch.json"
CUSTOMIZATION_SETTINGS_FILE = DATA_ROOT / "customization-settings.json"
NATIVE_BACKUP_ROOT = DATA_ROOT / "native-backups"
NATIVE_WORK_ROOT = DATA_ROOT / "native-work"
CONFIG_BACKUP_ROOT = DATA_ROOT / "config-backups"

PLUGIN_REF = "buddyhub@buddyhub"

ELEMENT_CATALOG: dict[str, dict[str, Any]] = {
    "tophat": {
        "element_id": "tophat",
        "label": "Top Hat",
        "slot": "top",
        "description": "Structured hat placed above the Buddy head with minimal overlap.",
        "status": "available",
    },
    "coffee": {
        "element_id": "coffee",
        "label": "Coffee Cup",
        "slot": "front",
        "description": "Small cup accessory positioned on the Buddy chest/front instead of above the head.",
        "status": "available",
    },
    "keyboard": {
        "element_id": "keyboard",
        "label": "Keyboard",
        "slot": "side",
        "description": "Small keyboard prop intended for the lower-side area near the Buddy base.",
        "status": "planned",
    },
    "book": {
        "element_id": "book",
        "label": "Book",
        "slot": "top",
        "description": "Compact book-like accessory positioned above the head.",
        "status": "available",
    },
}

COLOR_PRESETS: dict[str, dict[str, Any]] = {
    "orange": {"color_id": "orange", "label": "Orange", "hex": "#f28c28"},
    "pink": {"color_id": "pink", "label": "Pink", "hex": "#ff74b8"},
    "blue": {"color_id": "blue", "label": "Blue", "hex": "#5aa7ff"},
    "green": {"color_id": "green", "label": "Green", "hex": "#4ecb71"},
    "red": {"color_id": "red", "label": "Red", "hex": "#ff5b5b"},
    "black": {"color_id": "black", "label": "Black", "hex": "#111111"},
    "white": {"color_id": "white", "label": "White", "hex": "#f5f5f5"},
    "purple": {"color_id": "purple", "label": "Purple", "hex": "#9a67ff"},
}

USERCONFIG_ELEMENT_KEYS: dict[str, str] = {
    "element_tophat": "tophat",
    "element_coffee": "coffee",
    "element_book": "book",
}

USERCONFIG_COLOR_KEYS: dict[str, str] = {
    "color_green": "green",
    "color_orange": "orange",
    "color_blue": "blue",
    "color_pink": "pink",
    "color_purple": "purple",
    "color_red": "red",
    "color_black": "black",
}

USERCONFIG_NICKNAME_KEY = "nickname"

COLOR_PATCH_PRESETS: dict[str, dict[str, dict[str, Any]]] = {
    "2.1.92": {
        "green": {
            "color_id": "green",
            "label": "Green",
            "description": "Keep the current verified default green Buddy accent.",
            "replacements": [],
        },
        "orange": {
            "color_id": "orange",
            "label": "Orange",
            "description": "Remap the current uncommon Buddy accent token from green to orange/yellow.",
            "replacements": [
                {
                    "old": b'uncommon:"success"',
                    "new": b'uncommon:"warning"',
                    "expected_matches": 2,
                }
            ],
        },
        "blue": {
            "color_id": "blue",
            "label": "Blue",
            "description": "Retint the active success RGB token to a verified blue accent on the current target.",
            "replacements": [
                {
                    "old": b'success:"rgb(78,186,101)"',
                    "new": b'success:"rgb(78,120,255)"',
                    "expected_matches": 2,
                }
            ],
        },
        "pink": {
            "color_id": "pink",
            "label": "Pink",
            "description": "Retint the active success RGB token to a verified pink accent on the current target.",
            "replacements": [
                {
                    "old": b'success:"rgb(78,186,101)"',
                    "new": b'success:"rgb(255,80,120)"',
                    "expected_matches": 2,
                }
            ],
        },
        "purple": {
            "color_id": "purple",
            "label": "Purple",
            "description": "Retint the active success RGB token to a verified purple accent on the current target.",
            "replacements": [
                {
                    "old": b'success:"rgb(78,186,101)"',
                    "new": b'success:"rgb(180,80,255)"',
                    "expected_matches": 2,
                }
            ],
        },
        "red": {
            "color_id": "red",
            "label": "Red",
            "description": "Retint the active success RGB token to a verified red accent on the current target.",
            "replacements": [
                {
                    "old": b'success:"rgb(78,186,101)"',
                    "new": b'success:"rgb(255,060,60)"',
                    "expected_matches": 2,
                }
            ],
        },
        "black": {
            "color_id": "black",
            "label": "Black",
            "description": "Retint the active success RGB token to a verified black accent on the current target.",
            "replacements": [
                {
                    "old": b'success:"rgb(78,186,101)"',
                    "new": b'success:"rgb(000,000,00)"',
                    "expected_matches": 2,
                }
            ],
        }
    }
}

OFFICIAL_BUDDY_SURFACES: list[dict[str, str]] = [
    {
        "surface_id": "bottom_right_buddy",
        "label": "Bottom-right Buddy",
    },
    {
        "surface_id": "slash_buddy_card",
        "label": "/buddy card",
    },
]

DEFAULT_SETTINGS: dict[str, Any] = {
    "version": 1,
    "element_id": "tophat",
    "color_id": None,
    "nickname": None,
    "updated_at": None,
}

_BLOB_FRAME_REPLACEMENTS: list[tuple[bytes, bytes, int]] = [
    (
        b'[uk_]:[["            ","   .----.   "',
        b'[uk_]:[["{TOP_ROW}","   .----.   "',
        2,
    ),
    (
        b'["            ","  .------.  "',
        b'["{TOP_ROW}","  .------.  "',
        2,
    ),
    (
        b'["            ","    .--.    "',
        b'["{TOP_ROW}","    .--.    "',
        2,
    ),
]

_BLOB_BODY_ROW_REPLACEMENTS: list[tuple[bytes, bytes, int]] = [
    (
        b'","  (      )  ","   `----\\xB4   "',
        b'","{BODY_ROW}","   `----\\xB4   "',
        2,
    ),
    (
        b'"," (        ) ","  `------\\xB4  "',
        b'","{BODY_ROW}","  `------\\xB4  "',
        2,
    ),
    (
        b'","   (    )   ","    `--\\xB4    "',
        b'","{BODY_ROW}","    `--\\xB4    "',
        2,
    ),
]


def blob_top_row_profile(
    *,
    profile_id: str,
    description: str,
    element_id: str,
    top_row: str,
) -> dict[str, Any]:
    top_row_bytes = top_row.encode("utf-8")
    replacements = []
    for old, new_template, expected in _BLOB_FRAME_REPLACEMENTS:
        replacements.append(
            {
                "old": old,
                "new": new_template.replace(b"{TOP_ROW}", top_row_bytes),
                "expected_matches": expected,
            }
        )
    return {
        "profile_id": profile_id,
        "description": description,
        "species": "blob",
        "element_id": element_id,
        "slot": "top",
        "supports_colors": ["green", "orange", "blue", "pink", "purple", "red", "black"],
        "nickname_supported": False,
        "preview_lines": [
            top_row,
            "   .----.   ",
            "  ( @  @ )  ",
            "  (      )  ",
            "   `----\u00b4   ",
        ],
        "replacements": replacements,
    }


def blob_body_row_profile(
    *,
    profile_id: str,
    description: str,
    element_id: str,
    body_rows: tuple[str, str, str],
) -> dict[str, Any]:
    replacements = []
    for (old, new_template, expected), body_row in zip(_BLOB_BODY_ROW_REPLACEMENTS, body_rows, strict=True):
        replacements.append(
            {
                "old": old,
                "new": new_template.replace(b"{BODY_ROW}", body_row.encode("utf-8")),
                "expected_matches": expected,
            }
        )
    return {
        "profile_id": profile_id,
        "description": description,
        "species": "blob",
        "element_id": element_id,
        "slot": "front",
        "supports_colors": ["green", "orange", "blue", "pink", "purple", "red", "black"],
        "nickname_supported": False,
        "preview_lines": [
            "            ",
            "   .----.   ",
            "  ( @  @ )  ",
            body_rows[0],
            "   `----\u00b4   ",
        ],
        "replacements": replacements,
    }


SUPPORTED_PATCH_PROFILES: dict[str, list[dict[str, Any]]] = {
    "2.1.92": [
        blob_top_row_profile(
            profile_id="blob_tophat_preview",
            description="Add a centered top hat row to the official blob Buddy frames.",
            element_id="tophat",
            top_row="   _/|\\_    ",
        ),
        blob_body_row_profile(
            profile_id="blob_coffee_preview",
            description="Add a compact coffee cup accessory on the front of the official blob Buddy.",
            element_id="coffee",
            body_rows=(
                "  ( [_]o )  ",
                " (  [_]o  ) ",
                "   ([_]o)   ",
            ),
        ),
        blob_top_row_profile(
            profile_id="blob_book_preview",
            description="Add a compact open-book accessory near the upper-left of the official blob Buddy.",
            element_id="book",
            top_row="  /___\\     ",
        ),
    ]
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


def write_json_document(path: Path, payload: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(
        prefix=f"{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, ensure_ascii=False))
            handle.write("\n")
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
                str(CUSTOMIZATION_SETTINGS_FILE),
            ],
            "runtime_assets": [
                str(NATIVE_BACKUP_ROOT),
                str(NATIVE_WORK_ROOT),
                str(CONFIG_BACKUP_ROOT),
            ],
            "config_integrations": {
                "native_patch_target": None,
                "companion_name_source": str(CLAUDE_JSON_FILE),
            },
        }
        write_json(OWNERSHIP_FILE, manifest)
    else:
        owned_files = manifest.setdefault("owned_files", [])
        for owned_path in (str(OWNERSHIP_FILE), str(NATIVE_PATCH_STATE_FILE), str(CUSTOMIZATION_SETTINGS_FILE)):
            if owned_path not in owned_files:
                owned_files.append(owned_path)
        runtime_assets = manifest.setdefault("runtime_assets", [])
        for runtime_path in (str(NATIVE_BACKUP_ROOT), str(NATIVE_WORK_ROOT), str(CONFIG_BACKUP_ROOT)):
            if runtime_path not in runtime_assets:
                runtime_assets.append(runtime_path)
        config_integrations = manifest.setdefault("config_integrations", {})
        config_integrations["companion_name_source"] = str(CLAUDE_JSON_FILE)
        write_json(OWNERSHIP_FILE, manifest)
    return manifest


def default_customization_settings() -> dict[str, Any]:
    return dict(DEFAULT_SETTINGS)


def normalize_nickname(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def sanitize_customization_settings(raw: dict[str, Any] | None) -> dict[str, Any]:
    settings = default_customization_settings()
    if raw:
        settings.update(raw)

    element_id = settings.get("element_id")
    if element_id not in ELEMENT_CATALOG:
        element_id = DEFAULT_SETTINGS["element_id"]

    color_id = settings.get("color_id")
    if color_id not in COLOR_PRESETS:
        color_id = None

    settings["element_id"] = element_id
    settings["color_id"] = color_id
    settings["nickname"] = normalize_nickname(settings.get("nickname"))
    settings["version"] = DEFAULT_SETTINGS["version"]
    return settings


def load_customization_settings() -> dict[str, Any]:
    return sanitize_customization_settings(read_json(CUSTOMIZATION_SETTINGS_FILE, {}))


def save_customization_settings(settings: dict[str, Any]) -> dict[str, Any]:
    normalized = sanitize_customization_settings(settings)
    normalized["updated_at"] = now_iso()
    write_json(CUSTOMIZATION_SETTINGS_FILE, normalized)
    return normalized


def update_customization_settings(
    *,
    element_id: str | None = None,
    color_id: str | None = None,
    nickname: str | None = None,
    clear_color: bool = False,
    clear_nickname: bool = False,
    reset: bool = False,
) -> dict[str, Any]:
    settings = default_customization_settings() if reset else load_customization_settings()
    if element_id is not None:
        if element_id not in ELEMENT_CATALOG:
            raise RuntimeError(f"Unknown element_id: {element_id}")
        settings["element_id"] = element_id
    if color_id is not None:
        if color_id not in COLOR_PRESETS:
            raise RuntimeError(f"Unknown color_id: {color_id}")
        settings["color_id"] = color_id
    if clear_color:
        settings["color_id"] = None
    if nickname is not None:
        settings["nickname"] = normalize_nickname(nickname)
    if clear_nickname:
        settings["nickname"] = None
    return save_customization_settings(settings)


def plugin_option_env_name(option_key: str) -> str:
    normalized = option_key.replace("-", "_").upper()
    return f"CLAUDE_PLUGIN_OPTION_{normalized}"


def parse_plugin_option_bool(option_key: str) -> bool | None:
    raw = os.environ.get(plugin_option_env_name(option_key))
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off", ""}:
        return False
    return None


def read_plugin_option_string(option_key: str) -> str | None:
    raw = os.environ.get(plugin_option_env_name(option_key))
    if raw is None:
        return None
    return raw


def load_userconfig_runtime_overrides() -> dict[str, Any]:
    selected_elements = [
        element_id
        for option_key, element_id in USERCONFIG_ELEMENT_KEYS.items()
        if parse_plugin_option_bool(option_key) is True
    ]
    selected_colors = [
        color_id
        for option_key, color_id in USERCONFIG_COLOR_KEYS.items()
        if parse_plugin_option_bool(option_key) is True
    ]
    nickname = normalize_nickname(read_plugin_option_string(USERCONFIG_NICKNAME_KEY))
    nickname_present = read_plugin_option_string(USERCONFIG_NICKNAME_KEY) is not None
    return {
        "source": "manifest.userConfig",
        "selected_elements": selected_elements,
        "selected_colors": selected_colors,
        "nickname": nickname,
        "nickname_present": nickname_present,
        "has_any_value": bool(selected_elements or selected_colors or nickname_present),
    }


def merge_customization_settings_with_userconfig(
    settings: dict[str, Any],
    runtime_overrides: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str], list[str]]:
    overrides = runtime_overrides or load_userconfig_runtime_overrides()
    merged = dict(settings)
    blockers: list[str] = []
    warnings: list[str] = []

    selected_elements = overrides.get("selected_elements") or []
    selected_colors = overrides.get("selected_colors") or []

    if len(selected_elements) > 1:
        blockers.append(
            "Multiple BuddyHub element toggles are enabled in `/config`. Enable exactly one element there."
        )
    elif len(selected_elements) == 1:
        merged["element_id"] = selected_elements[0]

    if len(selected_colors) > 1:
        blockers.append(
            "Multiple BuddyHub color toggles are enabled in `/config`. Enable at most one color there."
        )
    elif len(selected_colors) == 1:
        merged["color_id"] = selected_colors[0]

    if overrides.get("nickname_present"):
        merged["nickname"] = overrides.get("nickname")
        if overrides.get("nickname") is None:
            warnings.append(
                "BuddyHub native Nickname is blank in `/config`, so the official Buddy name will stay unchanged."
            )

    return sanitize_customization_settings(merged), blockers, warnings


def profiles_for_version(version: str | None) -> list[dict[str, Any]]:
    if not version:
        return []
    return SUPPORTED_PATCH_PROFILES.get(version, [])


def color_patch_preset_for(version: str | None, color_id: str | None) -> dict[str, Any] | None:
    if not version or not color_id:
        return None
    return COLOR_PATCH_PRESETS.get(version, {}).get(color_id)


def compose_patch_profile(
    *,
    profile: dict[str, Any],
    version: str | None,
    color_id: str | None,
) -> dict[str, Any]:
    composed = dict(profile)
    replacements = list(profile.get("replacements", []))
    color_patch = color_patch_preset_for(version, color_id)
    if color_patch:
        replacements.extend(color_patch.get("replacements", []))
    composed["replacements"] = replacements
    composed["active_color_id"] = color_id
    composed["color_patch"] = color_patch
    return composed


def select_patch_profile(
    detection: dict[str, Any],
    identity: dict[str, Any],
    settings: dict[str, Any],
) -> tuple[dict[str, Any] | None, str]:
    version = detection.get("target_version")
    if not version:
        return None, "No Claude Code version was detected."

    species = identity.get("species")
    if not species:
        return None, "Current Buddy species is not verified yet."

    element_id = settings.get("element_id")
    for profile in profiles_for_version(str(version)):
        if profile.get("species") == species and profile.get("element_id") == element_id:
            return profile, "Selected element matches a verified patch profile for the current Buddy."

    if element_id not in ELEMENT_CATALOG:
        return None, f"Selected element {element_id!r} is not in the element catalog."
    if not profiles_for_version(str(version)):
        return None, "No supported patch profiles were found for the detected Claude Code version."
    return None, (
        f"Selected element `{element_id}` does not have a verified patch profile for "
        f"Buddy species `{species}` on Claude Code `{version}`."
    )


def customization_support(
    detection: dict[str, Any],
    identity: dict[str, Any],
    settings: dict[str, Any],
    companion_config: dict[str, Any],
    *,
    saved_settings: dict[str, Any] | None = None,
    runtime_overrides: dict[str, Any] | None = None,
    runtime_blockers: list[str] | None = None,
    runtime_warnings: list[str] | None = None,
) -> dict[str, Any]:
    profile, profile_reason = select_patch_profile(detection, identity, settings)
    selected_element = ELEMENT_CATALOG[settings["element_id"]]
    selected_color = COLOR_PRESETS.get(settings.get("color_id"))
    selected_nickname = normalize_nickname(settings.get("nickname"))

    element_options: list[dict[str, Any]] = []
    version = detection.get("target_version")
    species = identity.get("species")
    for element_id, item in ELEMENT_CATALOG.items():
        available = False
        reason = "Planned catalog item. No verified patch profile yet."
        for profile_candidate in profiles_for_version(str(version) if version else None):
            if (
                profile_candidate.get("element_id") == element_id
                and profile_candidate.get("species") == species
            ):
                available = True
                reason = "Verified patch profile exists for the current Buddy and Claude version."
                break
        element_options.append(
            {
                **item,
                "available": available,
                "reason": reason,
                "selected": settings["element_id"] == element_id,
            }
        )

    version = detection.get("target_version")

    color_options: list[dict[str, Any]] = []
    for color_id, item in COLOR_PRESETS.items():
        supported = bool(
            profile
            and color_id in profile.get("supports_colors", [])
            and color_patch_preset_for(str(version) if version else None, color_id)
        )
        color_options.append(
            {
                **item,
                "available": supported,
                "reason": (
                    "Validated color patch exists for the selected profile."
                    if supported
                    else "No validated color patch slot exists for the current selected profile."
                ),
                "selected": settings.get("color_id") == color_id,
            }
        )

    nickname_supported = bool(companion_config.get("available"))
    nickname_reason = (
        f"BuddyHub can update the displayed companion name through `{companion_config['path']}`."
        if nickname_supported
        else "No verified companion config file with a writable `companion.name` field was found."
    )

    can_apply = profile is not None
    blockers: list[str] = list(runtime_blockers or [])
    warnings: list[str] = list(runtime_warnings or [])
    effective_settings = dict(settings)
    if profile is None:
        blockers.append(profile_reason)
        can_apply = False
    if selected_color and not any(item["selected"] and item["available"] for item in color_options):
        warnings.append(
            f"Selected color `{selected_color['label']}` is not validated for the current target and will not be applied."
        )
        effective_settings["color_id"] = None
    if selected_nickname and not nickname_supported:
        warnings.append("Nickname display is not verified for the current target and will not be applied.")
        effective_settings["nickname"] = None

    return {
        "settings": settings,
        "saved_settings": saved_settings or settings,
        "effective_settings": effective_settings,
        "runtime_overrides": runtime_overrides or {},
        "profile": profile,
        "profile_reason": profile_reason,
        "element_options": element_options,
        "color_options": color_options,
        "nickname_supported": nickname_supported,
        "nickname_reason": nickname_reason,
        "selected_element": selected_element,
        "selected_color": selected_color,
        "selected_nickname": selected_nickname,
        "can_apply": can_apply,
        "apply_blockers": blockers,
        "apply_warnings": warnings,
    }


def preview_lines_for_customization(customization: dict[str, Any]) -> list[str] | None:
    profile = customization.get("profile") or {}
    preview_lines = profile.get("preview_lines")
    if preview_lines:
        return list(preview_lines)
    return None


def empty_identity() -> dict[str, Any]:
    return {
        "available": False,
        "source": None,
        "name": None,
        "species": None,
        "rarity": None,
        "shiny": None,
    }


def read_companion_config() -> dict[str, Any]:
    path = CLAUDE_JSON_FILE
    result = {
        "path": str(path),
        "exists": path.exists(),
        "available": False,
        "name": None,
        "personality": None,
        "reason": None,
    }
    if not path.exists():
        result["reason"] = "Claude runtime config file was not found."
        return result
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        result["reason"] = f"Could not read Claude runtime config: {exc}"
        return result
    companion = data.get("companion")
    if not isinstance(companion, dict):
        result["reason"] = "Claude runtime config does not contain a companion object."
        return result
    name = companion.get("name")
    result["name"] = name
    result["personality"] = companion.get("personality")
    result["available"] = isinstance(name, str) and bool(name.strip())
    if not result["available"]:
        result["reason"] = "Claude runtime config does not expose a usable companion.name field."
    return result


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


def ensure_companion_config_backup(config_path: Path) -> dict[str, Any]:
    ensure_data_root()
    CONFIG_BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    source_sha1 = sha1_file(config_path)
    backup_path = CONFIG_BACKUP_ROOT / f"{config_path.name}.{source_sha1}.bak"
    created = False
    if not backup_path.exists():
        shutil.copy2(config_path, backup_path)
        created = True
    return {
        "backup_path": str(backup_path),
        "created": created,
        "source_sha1": source_sha1,
    }


def apply_companion_name_override(config_path: Path, nickname: str) -> dict[str, Any]:
    backup = ensure_companion_config_backup(config_path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    companion = data.setdefault("companion", {})
    if not isinstance(companion, dict):
        raise RuntimeError("Claude runtime config companion field is not an object.")
    previous_name = companion.get("name")
    companion["name"] = nickname
    write_json_document(config_path, data)
    return {
        "config_path": str(config_path),
        "backup_path": backup["backup_path"],
        "backup_created": backup["created"],
        "source_sha1": backup["source_sha1"],
        "previous_name": previous_name,
        "applied_name": nickname,
        "current_sha1": sha1_file(config_path),
    }


def restore_companion_config_from_backup(config_path: Path, backup_path: Path) -> dict[str, Any]:
    shutil.copy2(backup_path, config_path)
    return {
        "config_path": str(config_path),
        "backup_path": str(backup_path),
        "restored_sha1": sha1_file(config_path),
    }


def sync_companion_name_override(
    *,
    inspection: dict[str, Any],
    applied_settings: dict[str, Any],
) -> dict[str, Any] | None:
    config_info = inspection.get("companion_config") or {}
    config_path_value = config_info.get("path")
    if not config_path_value:
        return None
    config_path = Path(str(config_path_value))
    if not config_path.exists():
        return None
    desired_name = normalize_nickname(applied_settings.get("nickname"))
    installed = (inspection.get("patch_state") or {}).get("installed") or {}
    previous_patch = installed.get("companion_name_patch") or {}
    previous_backup = previous_patch.get("backup_path")

    if desired_name:
        result = apply_companion_name_override(config_path, desired_name)
        result["mode"] = "applied"
        return result

    if previous_backup:
        backup_path = Path(str(previous_backup))
        if backup_path.exists():
            result = restore_companion_config_from_backup(config_path, backup_path)
            result["mode"] = "restored"
            return result
    return None


def official_surface_sync_summary(
    *,
    companion_config: dict[str, Any],
    effective_profile: dict[str, Any] | None,
    applied_settings: dict[str, Any],
) -> dict[str, Any]:
    selected_color = applied_settings.get("color_id")
    selected_nickname = normalize_nickname(applied_settings.get("nickname"))
    color_patch = (effective_profile or {}).get("color_patch") or {}
    color_sync = selected_color is None or bool(color_patch) or selected_color == "green"
    nickname_sync = selected_nickname is None or bool(companion_config.get("available"))
    return {
        "surfaces": list(OFFICIAL_BUDDY_SURFACES),
        "element_sync": bool(effective_profile),
        "color_sync": color_sync,
        "nickname_sync": nickname_sync,
        "name_source": str(CLAUDE_JSON_FILE) if nickname_sync else None,
        "color_source": "Claude Code native color tokens in the installed binary" if color_sync else None,
    }


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
            profiles = profiles_for_version(version)
            default_profile = profiles[0] if profiles else None
            result.update(
                {
                    "target_detected": True,
                    "target_path": str(candidate),
                    "target_version": version,
                    "target_sha1": sha1_file(candidate),
                    "profile_supported": bool(default_profile),
                    "profile_id": default_profile.get("profile_id") if default_profile else None,
                    "profile_description": default_profile.get("description") if default_profile else None,
                    "profile_species": default_profile.get("species") if default_profile else None,
                    "reason": None if default_profile else "No supported patch profile for this binary version.",
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
    profiles = profiles_for_version(version)
    default_profile = profiles[0] if profiles else None
    result.update(
        {
            "target_detected": True,
            "target_path": str(target),
            "target_version": version,
            "target_sha1": sha1_file(target),
            "profile_supported": bool(default_profile),
            "profile_id": default_profile.get("profile_id") if default_profile else None,
            "profile_description": default_profile.get("description") if default_profile else None,
            "profile_species": default_profile.get("species") if default_profile else None,
            "reason": None if default_profile else "No supported patch profile for the detected Claude version.",
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


def backup_metadata_from_path(backup_path: Path) -> dict[str, Any]:
    return {
        "backup_path": str(backup_path),
        "created": False,
        "source_sha1": sha1_file(backup_path),
    }


def resolve_patch_base_backup(
    inspection: dict[str, Any],
    target_path: Path,
    version: str,
) -> Path | None:
    installed = (inspection.get("patch_state") or {}).get("installed") or {}
    rehearsal = (inspection.get("patch_state") or {}).get("rehearsal") or {}
    backup_candidates = [
        installed.get("backup_path"),
        rehearsal.get("backup_path"),
        (inspection.get("backup") or {}).get("backup_path"),
    ]
    for candidate in backup_candidates:
        if not candidate:
            continue
        backup_path = Path(str(candidate))
        if backup_path.exists():
            return backup_path
    fallback = NATIVE_BACKUP_ROOT / version / f"{target_path.name}.{sha1_file(target_path)}.bak"
    if fallback.exists():
        return fallback
    return None


def detect_current_profile(
    target_path: Path,
    version: str | None,
    species: str | None,
) -> dict[str, Any] | None:
    if not version or not species:
        return None
    for profile in profiles_for_version(version):
        if profile.get("species") != species:
            continue
        status = patch_profile_status(target_path, profile)
        if status["status"] == "patched":
            return {
                "profile_id": profile["profile_id"],
                "element_id": profile["element_id"],
                "description": profile["description"],
                "status": status["status"],
            }
    return None


def rehearsal_copy_path(version: str) -> Path:
    return NATIVE_WORK_ROOT / version / f"claude-{version}-patched"


def patch_profile_status(binary_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    data = binary_path.read_bytes()
    replacement_states: list[dict[str, Any]] = []
    unpatched_checks = 0
    patched_checks = 0

    for replacement in profile["replacements"]:
        old = replacement["old"]
        new = replacement["new"]
        expected = replacement["expected_matches"]
        old_matches = data.count(old)
        new_matches = data.count(new)
        state = "mixed"
        if old_matches == expected and new_matches == 0:
            state = "unpatched"
            unpatched_checks += 1
        elif old_matches == 0 and new_matches == expected:
            state = "patched"
            patched_checks += 1
        replacement_states.append(
            {
                "expected_matches": expected,
                "old_matches": old_matches,
                "new_matches": new_matches,
                "state": state,
            }
        )

    if unpatched_checks == len(profile["replacements"]):
        overall = "unpatched"
    elif patched_checks == len(profile["replacements"]):
        overall = "patched"
    else:
        overall = "mixed"

    return {
        "status": overall,
        "checks": replacement_states,
    }


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
    companion_config = read_companion_config()
    saved_settings = load_customization_settings()
    runtime_overrides = load_userconfig_runtime_overrides()
    settings, runtime_blockers, runtime_warnings = merge_customization_settings_with_userconfig(
        saved_settings,
        runtime_overrides,
    )
    patch_state = load_native_patch_state()
    customization = customization_support(
        detection,
        identity,
        settings,
        companion_config,
        saved_settings=saved_settings,
        runtime_overrides=runtime_overrides,
        runtime_blockers=runtime_blockers,
        runtime_warnings=runtime_warnings,
    )
    selected_profile = customization.get("profile")

    rehearsal = patch_state.get("rehearsal") or {}
    installed = patch_state.get("installed") or {}
    rehearsal_path = rehearsal.get("patched_copy_path")
    rehearsal_exists = bool(rehearsal_path and Path(rehearsal_path).exists())
    installed_present = bool(installed)

    selected_target_status = None
    effective_profile = None
    if detection.get("target_detected") and detection.get("target_path") and selected_profile:
        effective_profile = compose_patch_profile(
            profile=selected_profile,
            version=detection.get("target_version"),
            color_id=customization["effective_settings"].get("color_id"),
        )
        selected_target_status = patch_profile_status(Path(detection["target_path"]), effective_profile)
    surface_sync = official_surface_sync_summary(
        companion_config=companion_config,
        effective_profile=effective_profile,
        applied_settings=customization["effective_settings"],
    )

    current_profile = None
    if detection.get("target_detected") and detection.get("target_path"):
        current_profile = detect_current_profile(
            Path(detection["target_path"]),
            detection.get("target_version"),
            identity.get("species"),
        )

    target_appears_patched = bool(
        selected_target_status and selected_target_status["status"] == "patched"
    )

    backup = None
    if detection.get("target_detected") and detection.get("target_path") and detection.get("target_version"):
        backup = existing_native_backup(Path(detection["target_path"]), str(detection["target_version"]))

    profile_match = customization["can_apply"]
    if customization["can_apply"]:
        if customization.get("apply_warnings"):
            profile_match_reason = (
                "Current effective customization can be applied, but some unsupported settings will remain pending: "
                + "; ".join(customization["apply_warnings"])
            )
        else:
            profile_match_reason = "Current effective customization maps to a verified patch profile."
    else:
        profile_match_reason = "; ".join(customization["apply_blockers"] or [customization["profile_reason"]])

    return {
        "detection": detection,
        "identity": identity,
        "companion_config": companion_config,
        "settings": saved_settings,
        "effective_settings": settings,
        "runtime_overrides": runtime_overrides,
        "customization": customization,
        "effective_profile": effective_profile,
        "backup": backup,
        "patch_state": patch_state,
        "surface_sync": surface_sync,
        "selected_target_status": selected_target_status,
        "current_profile": current_profile,
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
    if not inspection.get("profile_match"):
        raise RuntimeError(inspection.get("profile_match_reason") or "Saved customization cannot be applied to the current Buddy identity.")

    target_path = Path(str(detection["target_path"]))
    version = str(detection["target_version"])
    customization = inspection["customization"]
    profile = customization["profile"]
    if not profile:
        raise RuntimeError("No verified patch profile is available for the saved customization.")
    effective_profile = inspection.get("effective_profile") or compose_patch_profile(
        profile=profile,
        version=version,
        color_id=customization["effective_settings"].get("color_id"),
    )
    target_status = inspection.get("selected_target_status") or {}
    if target_status.get("status") == "patched":
        raise RuntimeError(
            "The detected Claude target already appears to contain the selected visual customization. "
            "Run restore first if you need a clean original binary."
        )
    base_source = target_path
    if target_status.get("status") == "mixed":
        backup_path = resolve_patch_base_backup(inspection, target_path, version)
        if not backup_path:
            raise RuntimeError(
                "The detected Claude target is in a mixed patch state for the selected customization, "
                "and no clean backup was found to rebase from."
            )
        backup = backup_metadata_from_path(backup_path)
        base_source = backup_path
    else:
        backup = ensure_native_backup(target_path, version)

    patched_copy = rehearsal_copy_path(version)
    patched_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(base_source, patched_copy)
    patched_copy.chmod(base_source.stat().st_mode)

    patch_results = apply_patch_profile_to_binary(patched_copy, effective_profile)
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
        "saved_settings": inspection["settings"],
        "effective_settings": customization["effective_settings"],
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
        "settings": customization["effective_settings"],
        "saved_settings": inspection["settings"],
        "apply_warnings": customization.get("apply_warnings") or [],
        "backup_path": backup["backup_path"],
        "backup_created": backup["created"],
        "patched_copy_path": str(patched_copy),
        "patched_sha1": sha1_file(patched_copy),
        "patch_results": patch_results,
        "codesign": codesign_result,
        "launch_check": launch_result,
        "manual_visual_check_required": True,
        "companion_name_patch": None,
        "surface_sync": inspection.get("surface_sync"),
    }


def apply_installed_patch() -> dict[str, Any]:
    ensure_ownership_manifest()
    inspection = inspect_native_patch(create_manifest=True)
    detection = inspection["detection"]

    if not detection.get("target_detected"):
        raise RuntimeError(detection.get("reason") or "No Claude Code target was detected.")
    if not inspection.get("profile_match"):
        raise RuntimeError(inspection.get("profile_match_reason") or "Saved customization cannot be applied to the current Buddy identity.")

    target_path = Path(str(detection["target_path"]))
    version = str(detection["target_version"])
    customization = inspection["customization"]
    profile = customization["profile"]
    if not profile:
        raise RuntimeError("No verified patch profile is available for the saved customization.")
    effective_profile = inspection.get("effective_profile") or compose_patch_profile(
        profile=profile,
        version=version,
        color_id=customization["effective_settings"].get("color_id"),
    )
    target_status = inspection.get("selected_target_status") or {}
    installed_state = (inspection.get("patch_state") or {}).get("installed") or {}
    installed_effective_settings = installed_state.get("effective_settings") or {}
    visual_settings_changed = any(
        installed_effective_settings.get(key) != customization["effective_settings"].get(key)
        for key in ("element_id", "color_id")
    )
    if target_status.get("status") == "patched" and not visual_settings_changed:
        backup_path = resolve_patch_base_backup(inspection, target_path, version)
        backup = backup_metadata_from_path(backup_path) if backup_path else None
        launch_result = verify_binary_launch(target_path)
        companion_name_patch = sync_companion_name_override(
            inspection=inspection,
            applied_settings=customization["effective_settings"],
        )
        patch_state = load_native_patch_state()
        patch_state["installed"] = {
            "applied_at": now_iso(),
            "target_path": str(target_path),
            "target_version": version,
            "profile_id": profile["profile_id"],
            "profile_species": profile["species"],
            "saved_settings": inspection["settings"],
            "effective_settings": customization["effective_settings"],
            "backup_path": backup["backup_path"] if backup else None,
            "source_sha1": backup["source_sha1"] if backup else None,
            "patched_sha1": sha1_file(target_path),
            "launch_check_output": launch_result["output"],
            "companion_name_patch": companion_name_patch,
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
            "settings": customization["effective_settings"],
            "saved_settings": inspection["settings"],
            "apply_warnings": customization.get("apply_warnings") or [],
            "backup_path": backup["backup_path"] if backup else None,
            "backup_created": False,
            "patched_sha1": sha1_file(target_path),
            "target_restored_from_backup": False,
            "patch_results": [],
            "codesign": {
                "required": sys.platform == "darwin",
                "attempted": False,
                "ok": True,
                "output": None,
            },
            "launch_check": launch_result,
            "manual_visual_check_required": False,
            "already_present": True,
            "companion_name_patch": companion_name_patch,
            "surface_sync": inspection.get("surface_sync"),
        }
    target_restored_from_backup = False
    if target_status.get("status") in {"mixed", "patched"}:
        backup_path = resolve_patch_base_backup(inspection, target_path, version)
        if not backup_path:
            raise RuntimeError(
                "The detected Claude target already contains a visual patch, "
                "and no clean backup was found to rebase from."
            )
        backup = backup_metadata_from_path(backup_path)
    else:
        backup = ensure_native_backup(target_path, version)

    try:
        if target_status.get("status") == "mixed":
            backup_path = Path(backup["backup_path"])
            shutil.copy2(backup_path, target_path)
            target_path.chmod(backup_path.stat().st_mode)
            target_restored_from_backup = True
        patch_results = apply_patch_profile_to_binary(target_path, effective_profile)
        codesign_result = codesign_binary(target_path)
        if not codesign_result["ok"]:
            raise RuntimeError(codesign_result["output"] or "codesign failed")
        launch_result = verify_binary_launch(target_path)
        if not launch_result["ok"]:
            raise RuntimeError(launch_result["output"] or "patched binary failed launch verification")
        companion_name_patch = sync_companion_name_override(
            inspection=inspection,
            applied_settings=customization["effective_settings"],
        )
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
        "saved_settings": inspection["settings"],
        "effective_settings": customization["effective_settings"],
        "backup_path": backup["backup_path"],
        "source_sha1": backup["source_sha1"],
        "patched_sha1": sha1_file(target_path),
        "launch_check_output": launch_result["output"],
        "companion_name_patch": companion_name_patch,
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
        "settings": customization["effective_settings"],
        "saved_settings": inspection["settings"],
        "apply_warnings": customization.get("apply_warnings") or [],
        "backup_path": backup["backup_path"],
        "backup_created": backup["created"],
        "patched_sha1": sha1_file(target_path),
        "target_restored_from_backup": target_restored_from_backup,
        "patch_results": patch_results,
        "codesign": codesign_result,
        "launch_check": launch_result,
        "manual_visual_check_required": True,
        "companion_name_patch": companion_name_patch,
        "surface_sync": inspection.get("surface_sync"),
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

    restored_companion_name = None
    companion_name_patch = installed.get("companion_name_patch") or {}
    config_path_value = companion_name_patch.get("config_path")
    config_backup_value = companion_name_patch.get("backup_path")
    if config_path_value and config_backup_value:
        config_path = Path(str(config_path_value))
        config_backup = Path(str(config_backup_value))
        if config_path.exists() and config_backup.exists():
            restored_companion_name = restore_companion_config_from_backup(config_path, config_backup)

    patch_state["rehearsal"] = None
    patch_state["installed"] = None
    save_native_patch_state(patch_state)

    return {
        "removed_paths": removed_paths,
        "backup_retained": bool((rehearsal.get("backup_path") or installed.get("backup_path"))),
        "backup_path": rehearsal.get("backup_path") or installed.get("backup_path"),
        "restored_target": restored_target,
        "restored_companion_name": restored_companion_name,
        "restored_surfaces": [item["label"] for item in OFFICIAL_BUDDY_SURFACES],
        "restored_at": now_iso(),
    }

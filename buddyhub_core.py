#!/usr/bin/env python3
from __future__ import annotations

import json
import locale
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
import hashlib
import importlib.metadata
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parent
CLAUDE_CONFIG_ROOT = Path.home() / ".claude"
CLAUDE_PROJECTS_ROOT = CLAUDE_CONFIG_ROOT / "projects"
CLAUDE_VERSIONS_ROOT = Path.home() / ".local" / "share" / "claude" / "versions"
CLAUDE_JSON_FILE = Path(
    os.environ.get("BUDDYHUB_CLAUDE_JSON")
    or (Path.home() / ".claude.json")
)
DATA_ROOT = Path(
    os.environ.get("BUDDYHUB_DATA_ROOT")
    or (Path.home() / ".buddyhub")
)
LEGACY_PLUGIN_DATA_ROOT = Path.home() / ".claude" / "plugins" / "data" / "buddyhub"
OWNERSHIP_FILE = DATA_ROOT / "ownership.json"
NATIVE_PATCH_STATE_FILE = DATA_ROOT / "native-patch.json"
CUSTOMIZATION_SETTINGS_FILE = DATA_ROOT / "customization-settings.json"
NATIVE_BACKUP_ROOT = DATA_ROOT / "native-backups"
NATIVE_WORK_ROOT = DATA_ROOT / "native-work"
CONFIG_BACKUP_ROOT = DATA_ROOT / "config-backups"
UNINSTALL_SCRIPT_FILE = DATA_ROOT / "uninstall.sh"
LEGACY_PLUGIN_TRACE_PATHS = [
    Path.home() / ".claude" / "plugins" / "cache" / "buddyhub",
    Path.home() / ".claude" / "plugins" / "marketplaces" / "buddyhub",
    Path.home() / ".claude" / "plugins" / "data" / "buddyhub",
    Path.home() / ".claude" / "plugins" / "data" / "buddyhub-buddyhub",
    Path.home() / ".claude" / "plugins" / "data" / "buddyhub-inline",
]

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

LANGUAGE_PRESETS: dict[str, dict[str, str]] = {
    "zh_cn": {"language_id": "zh_cn", "label": "中文"},
    "en": {"language_id": "en", "label": "English"},
    "ja": {"language_id": "ja", "label": "日本語"},
    "ko": {"language_id": "ko", "label": "韩语"},
    "de": {"language_id": "de", "label": "Deutsch"},
    "fr": {"language_id": "fr", "label": "Français"},
    "ru": {"language_id": "ru", "label": "Русский"},
}

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
    "element_id": None,
    "color_id": None,
    "nickname": None,
    "language_id": "en",
    "claude_binary_path": None,
    "claude_json_path": None,
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

BASE_SPECIES_PREVIEW_LINES: dict[str, list[str]] = {
    "blob": [
        "            ",
        "   .----.   ",
        "  ( @  @ )  ",
        "  (      )  ",
        "   `----´   ",
    ]
}

def ensure_data_root() -> None:
    migrate_legacy_data_root()
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def migrate_legacy_data_root() -> bool:
    if DATA_ROOT == LEGACY_PLUGIN_DATA_ROOT:
        return False
    if DATA_ROOT.exists():
        return False
    if not LEGACY_PLUGIN_DATA_ROOT.exists():
        return False
    DATA_ROOT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(LEGACY_PLUGIN_DATA_ROOT, DATA_ROOT, dirs_exist_ok=True)
    return True


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


def app_version() -> str:
    try:
        return importlib.metadata.version("buddyhub")
    except importlib.metadata.PackageNotFoundError:
        pass

    pyproject = APP_ROOT / "pyproject.toml"
    if pyproject.exists():
        try:
            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
            return str(data.get("project", {}).get("version", "0.1.0"))
        except (OSError, tomllib.TOMLDecodeError):
            pass

    package_json = APP_ROOT / "package.json"
    if package_json.exists():
        try:
            return str(read_json(package_json, {}).get("version", "0.1.0"))
        except OSError:
            pass
    return "0.1.0"


def install_context() -> dict[str, Any]:
    module_root = APP_ROOT
    module_path = str(module_root)
    source = "unknown"
    uninstall_commands: list[list[str]] = []

    if module_root.exists() and (module_root / ".git").exists():
        source = "source_checkout"
    elif "node_modules" in module_root.parts:
        source = "npm"
        uninstall_commands.append(["npm", "uninstall", "-g", "buddyhub"])
    elif "site-packages" in module_root.parts or "dist-packages" in module_root.parts:
        source = "pip"
        uninstall_commands.append([sys.executable, "-m", "pip", "uninstall", "-y", "buddyhub"])
    elif "Cellar" in module_root.parts or "Homebrew" in module_path:
        source = "brew"
        uninstall_commands.append(["brew", "uninstall", "buddyhub"])
    else:
        uninstall_commands.extend(
            [
                ["brew", "uninstall", "buddyhub"],
                ["npm", "uninstall", "-g", "buddyhub"],
                [sys.executable, "-m", "pip", "uninstall", "-y", "buddyhub"],
            ]
        )

    return {
        "source": source,
        "module_root": str(module_root),
        "uninstall_commands": uninstall_commands,
    }


def remove_path(path: Path) -> list[str]:
    removed: list[str] = []
    if not path.exists():
        return removed
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    removed.append(str(path))
    parent = path.parent
    while parent != parent.parent:
        try:
            parent.rmdir()
        except OSError:
            break
        removed.append(str(parent))
        parent = parent.parent
    return removed


def cleanup_legacy_plugin_traces() -> list[str]:
    removed: list[str] = []
    for path in LEGACY_PLUGIN_TRACE_PATHS:
        removed.extend(remove_path(path))
    return removed


def render_uninstall_script(
    *,
    remove_data_root: bool = True,
) -> str:
    cleanup_paths = list(LEGACY_PLUGIN_TRACE_PATHS)
    if remove_data_root:
        cleanup_paths.append(DATA_ROOT)
    cleanup_commands = "\n".join(
        f"rm -rf {shlex.quote(str(path))}" for path in cleanup_paths
    )
    uninstall_lines = []
    for command in install_context()["uninstall_commands"]:
        uninstall_lines.append(" ".join(shlex.quote(part) for part in command) + " >/dev/null 2>&1 || true")
    uninstall_body = "\n".join(uninstall_lines)
    return f"""#!/bin/zsh
sleep 1
{cleanup_commands}
rm -f {shlex.quote(str(UNINSTALL_SCRIPT_FILE))}
{uninstall_body}
"""


def schedule_self_uninstall(*, remove_data_root: bool = True) -> dict[str, Any]:
    ensure_data_root()
    script = render_uninstall_script(remove_data_root=remove_data_root)
    UNINSTALL_SCRIPT_FILE.write_text(script, encoding="utf-8")
    UNINSTALL_SCRIPT_FILE.chmod(0o700)
    process = subprocess.Popen(  # noqa: S603
        ["/bin/zsh", str(UNINSTALL_SCRIPT_FILE)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return {
        "script_path": str(UNINSTALL_SCRIPT_FILE),
        "pid": process.pid,
        "install_context": install_context(),
        "cleanup_paths": [str(path) for path in LEGACY_PLUGIN_TRACE_PATHS] + ([str(DATA_ROOT)] if remove_data_root else []),
    }


def ensure_ownership_manifest() -> dict[str, Any]:
    ensure_data_root()
    manifest = read_json(OWNERSHIP_FILE, None)
    if manifest is None:
        manifest = {
            "app": "buddyhub",
            "version": app_version(),
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
    settings = dict(DEFAULT_SETTINGS)
    settings["language_id"] = detect_system_language_id()
    return settings


def normalize_nickname(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = "".join(ch for ch in str(value) if ch >= " " and ch != "\x7f").strip()
    return cleaned or None


def normalize_optional_path(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    if not cleaned:
        return None
    return str(Path(cleaned).expanduser())


def is_generic_locale(value: str | None) -> bool:
    if not value:
        return True
    normalized = str(value).strip().split(".")[0].split("@")[0].replace("-", "_").lower()
    return normalized in {"c", "posix"}


def detect_system_language_id() -> str:
    candidates = [
        os.environ.get("LC_ALL"),
        os.environ.get("LC_MESSAGES"),
        os.environ.get("LANGUAGE"),
        os.environ.get("LANG"),
        locale.getlocale()[0],
    ]
    normalized = ""
    for candidate in candidates:
        if candidate and not is_generic_locale(candidate):
            normalized = str(candidate)
            break
    normalized = normalized.split(".")[0].split("@")[0].replace("-", "_").lower()
    if normalized.startswith("zh"):
        return "zh_cn"
    if normalized.startswith("ja"):
        return "ja"
    if normalized.startswith("ko"):
        return "ko"
    if normalized.startswith("de"):
        return "de"
    if normalized.startswith("fr"):
        return "fr"
    if normalized.startswith("ru"):
        return "ru"
    return "en"


def version_from_target_path(path: Path) -> str | None:
    direct = parse_semver(path.name)
    if direct is not None:
        return path.name
    stem = parse_semver(path.stem)
    if stem is not None:
        return path.stem
    parent = parse_semver(path.parent.name)
    if parent is not None:
        return path.parent.name
    return None


def candidate_versions_roots() -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        roots.append(("xdg-versions-dir", Path(xdg_data_home).expanduser() / "claude" / "versions"))
    roots.append(("home-local-share-versions", CLAUDE_VERSIONS_ROOT))
    return roots


def versioned_binaries_in_root(root: Path) -> list[tuple[tuple[int, int, int], Path, str]]:
    candidates: list[tuple[tuple[int, int, int], Path, str]] = []
    if not root.exists() or not root.is_dir():
        return candidates
    for path in root.iterdir():
        if path.is_file():
            version = version_from_target_path(path)
            semver = parse_semver(version) if version else None
            if semver is not None:
                candidates.append((semver, path, version))
            continue
        if not path.is_dir():
            continue
        semver = parse_semver(path.name)
        if semver is None:
            continue
        for binary_name in ("claude", "claude.exe"):
            candidate = path / binary_name
            if candidate.exists() and candidate.is_file():
                candidates.append((semver, candidate, path.name))
                break
    return candidates


def detect_target_from_binary_path(
    candidate: Path,
    *,
    detection_mode: str,
    install_root: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "platform": sys.platform,
        "target_detected": False,
        "target_path": None,
        "target_version": None,
        "target_sha1": None,
        "install_root": install_root,
        "detection_mode": detection_mode,
        "profile_supported": False,
        "profile_id": None,
        "profile_description": None,
        "profile_species": None,
        "reason": None,
    }
    if not candidate.exists() or not candidate.is_file():
        result["reason"] = "Configured Claude binary path does not point to a readable file."
        return result
    version = version_from_target_path(candidate)
    if not version:
        result["reason"] = "Detected Claude binary path does not expose a versioned target that BuddyHub can patch."
        return result
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


def detect_target_from_launcher() -> dict[str, Any] | None:
    command_names = ["claude"]
    if sys.platform == "win32":
        command_names.append("claude.exe")
    seen: set[str] = set()
    for command_name in command_names:
        launcher = shutil.which(command_name)
        if not launcher:
            continue
        launcher_path = Path(launcher).expanduser()
        candidates = [launcher_path]
        try:
            resolved = launcher_path.resolve()
        except OSError:
            resolved = launcher_path
        if resolved != launcher_path:
            candidates.insert(0, resolved)
        for candidate in candidates:
            candidate_key = str(candidate)
            if candidate_key in seen:
                continue
            seen.add(candidate_key)
            version = version_from_target_path(candidate)
            if not version:
                continue
            return detect_target_from_binary_path(
                candidate,
                detection_mode="launcher-resolve",
                install_root=str(candidate.parent),
            )
    return None


def sanitize_customization_settings(raw: dict[str, Any] | None) -> dict[str, Any]:
    settings = default_customization_settings()
    if raw:
        settings.update(raw)

    element_id = settings.get("element_id")
    if element_id is not None and element_id not in ELEMENT_CATALOG:
        element_id = DEFAULT_SETTINGS["element_id"]

    color_id = settings.get("color_id")
    if color_id not in COLOR_PRESETS:
        color_id = None

    language_id = settings.get("language_id")
    if language_id not in LANGUAGE_PRESETS:
        language_id = detect_system_language_id()

    claude_binary_path = normalize_optional_path(settings.get("claude_binary_path"))
    claude_json_path = normalize_optional_path(settings.get("claude_json_path"))

    settings["element_id"] = element_id
    settings["color_id"] = color_id
    settings["nickname"] = normalize_nickname(settings.get("nickname"))
    settings["language_id"] = language_id
    settings["claude_binary_path"] = claude_binary_path
    settings["claude_json_path"] = claude_json_path
    settings["version"] = DEFAULT_SETTINGS["version"]
    return settings


def load_customization_settings() -> dict[str, Any]:
    ensure_data_root()
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
    language_id: str | None = None,
    claude_binary_path: str | None = None,
    claude_json_path: str | None = None,
    clear_element: bool = False,
    clear_color: bool = False,
    clear_nickname: bool = False,
    clear_claude_binary_path: bool = False,
    clear_claude_json_path: bool = False,
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
    if language_id is not None:
        if language_id not in LANGUAGE_PRESETS:
            raise RuntimeError(f"Unknown language_id: {language_id}")
        settings["language_id"] = language_id
    if claude_binary_path is not None:
        settings["claude_binary_path"] = normalize_optional_path(claude_binary_path)
    if claude_json_path is not None:
        settings["claude_json_path"] = normalize_optional_path(claude_json_path)
    if clear_element:
        settings["element_id"] = None
    if clear_color:
        settings["color_id"] = None
    if nickname is not None:
        settings["nickname"] = normalize_nickname(nickname)
    if clear_nickname:
        settings["nickname"] = None
    if clear_claude_binary_path:
        settings["claude_binary_path"] = None
    if clear_claude_json_path:
        settings["claude_json_path"] = None
    return save_customization_settings(settings)


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


def base_profile_for_species(
    *,
    version: str | None,
    species: str,
) -> dict[str, Any]:
    preview_lines = default_preview_lines_for_species(species) or []
    supported_colors = [
        color_id
        for color_id in ("green", "orange", "blue", "pink", "purple", "red", "black")
        if color_patch_preset_for(version, color_id)
    ]
    return {
        "profile_id": f"{species}_base_preview",
        "description": "Keep the official Buddy base frame without adding an extra element.",
        "species": species,
        "element_id": None,
        "slot": "base",
        "supports_colors": supported_colors,
        "nickname_supported": False,
        "preview_lines": preview_lines,
        "replacements": [],
    }


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
    if element_id is None:
        return (
            base_profile_for_species(version=str(version), species=str(species)),
            "No additive element selected. BuddyHub will keep the official Buddy frame and only apply supported overlays such as color.",
        )
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
) -> dict[str, Any]:
    profile, profile_reason = select_patch_profile(detection, identity, settings)
    selected_element = ELEMENT_CATALOG.get(settings["element_id"]) or {
        "element_id": None,
        "label": "None",
        "slot": "base",
        "description": "Keep the official Buddy frame without adding an element.",
        "status": "available",
    }
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
    blockers: list[str] = []
    warnings: list[str] = []
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
        "saved_settings": settings,
        "effective_settings": effective_settings,
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


def default_preview_lines_for_species(species: str | None) -> list[str] | None:
    if not species:
        return None
    preview = BASE_SPECIES_PREVIEW_LINES.get(species)
    if preview:
        return list(preview)
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


def read_companion_config(settings: dict[str, Any] | None = None) -> dict[str, Any]:
    override = normalize_optional_path(os.environ.get("BUDDYHUB_CLAUDE_JSON"))
    configured = normalize_optional_path((settings or {}).get("claude_json_path"))
    path = Path(override or configured or str(CLAUDE_JSON_FILE))
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
    ensure_data_root()
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


def detect_native_target(settings: dict[str, Any] | None = None) -> dict[str, Any]:
    override = normalize_optional_path(os.environ.get("BUDDYHUB_CLAUDE_BINARY"))
    configured = normalize_optional_path((settings or {}).get("claude_binary_path"))
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

    if override or configured:
        candidate = Path(override or configured).expanduser()
        detected = detect_target_from_binary_path(
            candidate,
            detection_mode="env" if override else "settings",
            install_root=str(candidate.parent),
        )
        if not detected.get("target_detected"):
            detected["reason"] = (
                "Configured Claude binary path does not point to a readable versioned Claude binary."
                if configured and not override
                else "BUDDYHUB_CLAUDE_BINARY does not point to a readable versioned Claude binary."
            )
        return detected

    launcher_detection = detect_target_from_launcher()
    if launcher_detection:
        return launcher_detection

    root_candidates = candidate_versions_roots()
    for detection_mode, root in root_candidates:
        candidates = versioned_binaries_in_root(root)
        if not candidates:
            continue
        candidates.sort(key=lambda item: item[0], reverse=True)
        _, target, _ = candidates[0]
        return detect_target_from_binary_path(
            target,
            detection_mode=detection_mode,
            install_root=str(root),
        )

    if sys.platform == "darwin":
        result["install_root"] = str(CLAUDE_VERSIONS_ROOT)
        result["detection_mode"] = "macos-versions-dir"
        if not CLAUDE_VERSIONS_ROOT.exists():
            result["reason"] = "BuddyHub could not find the Claude versions directory. Try Setup and use `which claude` to locate the installed launcher target."
        else:
            result["reason"] = "No versioned Claude executable was found automatically. Try Setup and use `which claude` to locate the installed launcher target."
        return result

    if sys.platform.startswith("linux"):
        result["detection_mode"] = "linux-launcher-or-versions"
        result["reason"] = "BuddyHub could not resolve the installed Claude binary automatically on this Linux machine. Try Setup and use `which claude` or `claude doctor` as a reference."
        return result

    if sys.platform == "win32":
        result["detection_mode"] = "windows-launcher"
        result["reason"] = "BuddyHub could not resolve the installed Claude binary automatically on this Windows machine. Try Setup and use `where claude` or `claude doctor` as a reference."
        return result

    result["reason"] = "BuddyHub could not resolve the installed Claude binary automatically on this platform. Use Setup to enter the Claude binary path."
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


def candidate_native_backups(target_path: Path, version: str) -> list[Path]:
    backup_dir = NATIVE_BACKUP_ROOT / version
    if not backup_dir.exists():
        return []
    return sorted(
        (
            path
            for path in backup_dir.glob(f"{target_path.name}.*.bak")
            if path.is_file()
        ),
        key=lambda path: path.name,
    )


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
    discovered = candidate_native_backups(target_path, version)
    if len(discovered) == 1:
        return discovered[0]
    for candidate in discovered:
        source_sha1 = candidate.name.removeprefix(f"{target_path.name}.").removesuffix(".bak")
        if source_sha1 and source_sha1 != sha1_file(target_path):
            return candidate
    if discovered:
        return discovered[0]
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
                "preview_lines": list(profile.get("preview_lines") or []),
                "supports_colors": list(profile.get("supports_colors") or []),
                "slot": profile.get("slot"),
                "status": status["status"],
            }
    return None


def detect_current_color_id(
    target_path: Path,
    version: str | None,
) -> str | None:
    if not version:
        return None
    presets = COLOR_PATCH_PRESETS.get(version, {})
    patched_colors: list[str] = []
    mixed_detected = False
    for color_id, preset in presets.items():
        if color_id == "green":
            continue
        status = patch_profile_status(
            target_path,
            {
                "profile_id": f"color_{color_id}",
                "replacements": preset.get("replacements", []),
            },
        )
        if status["status"] == "patched":
            patched_colors.append(color_id)
        elif status["status"] == "mixed":
            mixed_detected = True
    if len(patched_colors) == 1:
        return patched_colors[0]
    if mixed_detected or len(patched_colors) > 1:
        return None
    return "green"


def current_visual_state(
    *,
    detection: dict[str, Any],
    identity: dict[str, Any],
    companion_config: dict[str, Any],
    current_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    preview_lines = None
    element_id = None
    if current_profile:
        preview_lines = list(current_profile.get("preview_lines") or [])
        element_id = current_profile.get("element_id")
    if not preview_lines:
        preview_lines = default_preview_lines_for_species(identity.get("species"))
    color_id = None
    if detection.get("target_detected") and detection.get("target_path"):
        color_id = detect_current_color_id(
            Path(detection["target_path"]),
            detection.get("target_version"),
        )
    return {
        "name": companion_config.get("name") or identity.get("name"),
        "species": identity.get("species"),
        "element_id": element_id,
        "color_id": color_id,
        "preview_lines": preview_lines,
    }


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
    saved_settings = load_customization_settings()
    detection = detect_native_target(saved_settings)
    identity = current_identity_from_projects()
    companion_config = read_companion_config(saved_settings)
    settings = dict(saved_settings)
    patch_state = load_native_patch_state()
    customization = customization_support(
        detection,
        identity,
        settings,
        companion_config,
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
    current_visual = current_visual_state(
        detection=detection,
        identity=identity,
        companion_config=companion_config,
        current_profile=current_profile,
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
        "customization": customization,
        "effective_profile": effective_profile,
        "backup": backup,
        "patch_state": patch_state,
        "surface_sync": surface_sync,
        "selected_target_status": selected_target_status,
        "current_profile": current_profile,
        "current_visual": current_visual,
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
    current_profile = inspection.get("current_profile") or {}
    current_visual = inspection.get("current_visual") or {}
    desired_effective_settings = customization["effective_settings"]
    desired_element_id = desired_effective_settings.get("element_id")
    desired_color_id = desired_effective_settings.get("color_id") or "green"
    current_element_id = current_profile.get("element_id")
    current_color_id = current_visual.get("color_id") or "green"
    actual_visual_matches = (
        current_element_id == desired_element_id
        and current_color_id == desired_color_id
    )
    if installed_effective_settings:
        visual_settings_changed = any(
            installed_effective_settings.get(key) != desired_effective_settings.get(key)
            for key in ("element_id", "color_id")
        )
    else:
        visual_settings_changed = not actual_visual_matches
    if target_status.get("status") == "patched" and not visual_settings_changed:
        backup_path = resolve_patch_base_backup(inspection, target_path, version)
        backup = backup_metadata_from_path(backup_path) if backup_path else None
        launch_result = verify_binary_launch(target_path)
        companion_name_patch = sync_companion_name_override(
            inspection=inspection,
            applied_settings=desired_effective_settings,
        )
        patch_state = load_native_patch_state()
        patch_state["installed"] = {
            "applied_at": now_iso(),
            "target_path": str(target_path),
            "target_version": version,
            "profile_id": profile["profile_id"],
            "profile_species": profile["species"],
            "saved_settings": inspection["settings"],
            "effective_settings": desired_effective_settings,
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
            "settings": desired_effective_settings,
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

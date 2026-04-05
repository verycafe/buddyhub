#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any

from buddyhub_core import COLOR_PRESETS, LANGUAGE_PRESETS
from buddyhub_tui import BuddyHubTUI, LANGUAGE_ORDER, TOP_LEVEL_MENU


def serialize_state(app: BuddyHubTUI) -> dict[str, Any]:
    return {
        "settings": app.settings,
        "current_visual": app.current_visual,
        "draft_visual": app.draft_visual,
        "screen": app.screen,
        "needs_setup": app.needs_setup(),
        "message": app.message,
        "result_card": app.result_card,
        "exit_notice": app.exit_notice,
    }


def ui_model() -> dict[str, Any]:
    return {
        "languages": [
            {
                "language_id": language_id,
                "label": LANGUAGE_PRESETS[language_id]["label"],
            }
            for language_id in LANGUAGE_ORDER
        ],
        "colors": [
            {
                "color_id": color_id,
                "label": COLOR_PRESETS[color_id]["label"],
                "hex": COLOR_PRESETS[color_id]["hex"],
            }
            for color_id in ("green", "orange", "blue", "pink", "purple", "red", "black", "white")
            if color_id in COLOR_PRESETS
        ],
        "top_level_menu": list(TOP_LEVEL_MENU),
    }


def ok_payload(*, app: BuddyHubTUI | None = None, result: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": True}
    if app is not None:
        payload["state"] = serialize_state(app)
    if result is not None:
        payload["result"] = result
    return payload


def run_action(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "dump-ui-model":
        return {"ok": True, "ui": ui_model()}

    app = BuddyHubTUI()

    if args.command == "dump-state":
        return ok_payload(app=app)

    if args.command == "dump-prototype":
        return {"ok": True, "state": serialize_state(app), "ui": ui_model()}

    if args.command == "set-language":
        app.save_language(args.language_id)
        return ok_payload(app=app, result={"action": "set-language", "language_id": args.language_id})

    if args.command == "set-color":
        if args.color_id == "default":
            app.save_color(None)
            return ok_payload(app=app, result={"action": "set-color", "color_id": None})
        app.save_color(args.color_id)
        return ok_payload(app=app, result={"action": "set-color", "color_id": args.color_id})

    if args.command == "set-nickname":
        app.save_nickname(args.nickname)
        return ok_payload(app=app, result={"action": "set-nickname", "nickname": args.nickname})

    if args.command == "clear-nickname":
        app.clear_nickname()
        return ok_payload(app=app, result={"action": "clear-nickname"})

    if args.command == "apply":
        app.do_apply()
        return ok_payload(app=app, result={"action": "apply", "result_card": app.result_card})

    if args.command == "restore":
        app.do_restore()
        return ok_payload(app=app, result={"action": "restore", "result_card": app.result_card})

    raise RuntimeError(f"Unknown command: {args.command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BuddyHub JSON bridge for alternate frontends")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("dump-state")
    subparsers.add_parser("dump-ui-model")
    subparsers.add_parser("dump-prototype")

    parser_language = subparsers.add_parser("set-language")
    parser_language.add_argument("language_id", choices=LANGUAGE_ORDER)

    parser_color = subparsers.add_parser("set-color")
    parser_color.add_argument("color_id", choices=["default", "green", "orange", "blue", "pink", "purple", "red", "black", "white"])

    parser_nickname = subparsers.add_parser("set-nickname")
    parser_nickname.add_argument("nickname")

    subparsers.add_parser("clear-nickname")
    subparsers.add_parser("apply")
    subparsers.add_parser("restore")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = run_action(args)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any

from buddyhub_core import (
    LANGUAGE_ORDER,
    bridge_apply,
    bridge_restore,
    bridge_set_color,
    bridge_set_language,
    bridge_set_nickname,
    bridge_state,
    bridge_ui_model,
)


def ok_payload(*, state: dict[str, Any] | None = None, result: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": True}
    if state is not None:
        payload["state"] = state
    if result is not None:
        payload["result"] = result
    return payload


def run_action(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "dump-ui-model":
        return {"ok": True, "ui": bridge_ui_model()}

    if args.command == "dump-state":
        return ok_payload(state=bridge_state())

    if args.command == "dump-prototype":
        return {"ok": True, "state": bridge_state(), "ui": bridge_ui_model()}

    if args.command == "set-language":
        payload = bridge_set_language(args.language_id)
        return ok_payload(state=payload["state"], result=payload["result"])

    if args.command == "set-color":
        if args.color_id == "default":
            payload = bridge_set_color(None)
        else:
            payload = bridge_set_color(args.color_id)
        return ok_payload(state=payload["state"], result=payload["result"])

    if args.command == "set-nickname":
        payload = bridge_set_nickname(args.nickname)
        return ok_payload(state=payload["state"], result=payload["result"])

    if args.command == "clear-nickname":
        payload = bridge_set_nickname(None)
        return ok_payload(state=payload["state"], result={"action": "clear-nickname"})

    if args.command == "apply":
        payload = bridge_apply()
        return ok_payload(state=payload["state"], result=payload["result"])

    if args.command == "restore":
        payload = bridge_restore()
        return ok_payload(state=payload["state"], result=payload["result"])

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

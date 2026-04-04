#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from buddyhublib import snapshot  # noqa: E402


def main() -> int:
    _ = sys.stdin.read()
    info = snapshot()
    runtime = info["runtime"]
    active_session = info["active_session"] or {}
    lifecycle = runtime.get("lifecycle_state", "enabled")
    if lifecycle in {"paused", "disabled"}:
        print(f"Buddy: {lifecycle}")
        return 0
    project = active_session.get("project_name")
    suffix = f" | {project}" if project else ""
    print(f"Buddy: {runtime.get('buddy_name', 'Buddy')} | {runtime.get('current_state', 'idle')}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

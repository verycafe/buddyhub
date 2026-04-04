#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from buddyhublib import render_buddy_statusline, snapshot  # noqa: E402


def main() -> int:
    _ = sys.stdin.read()
    info = snapshot()
    print(render_buddy_statusline(info))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

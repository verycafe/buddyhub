# BuddyHub

[中文说明](./README.zh-CN.md)

BuddyHub is a reactive Buddy plugin for Claude Code.

V1 is `TUI-first`:

- hook-driven state tracking
- `/buddyhub:status` compact state view
- `/buddyhub:open` detailed text view
- optional Claude Code status line integration
- safe pause, resume, disable, and uninstall flows

BuddyHub does not require:

- external GUI windows
- terminal-specific graphics
- tmux

## Install Goal

BuddyHub is designed to be installed through a Claude Code marketplace flow:

```text
/plugin marketplace add verycafe/buddyhub
/plugin install buddyhub@buddyhub
```

## Main Commands

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:open`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:doctor`
- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`
- `/buddyhub:uninstall`

## Status Line

BuddyHub ships a status line script at:

- [plugins/buddyhub/scripts/statusline.py](/Users/tvwoo/Projects/buddyhub/plugins/buddyhub/scripts/statusline.py)

V1 does not auto-edit Claude Code settings. Use `/buddyhub:statusline-on` to get the script path, then wire it into Claude Code manually.

## Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## Current State

What is already in place:

- marketplace manifest
- plugin manifest
- command surface
- hook-driven state runtime
- local testing guide

What still needs real-world verification:

- real Claude Code install in a logged-in session
- real hook payload behavior inside Claude Code
- manual status line wiring
- at least one cross-terminal smoke pass

## License

BuddyHub is licensed under `AGPL-3.0-only` (GNU Affero General Public
License v3.0 only). If you distribute modified versions, or let users
interact with modified versions over a network, you must provide the
corresponding source under AGPLv3. See
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE).

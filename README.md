# BuddyHub

[中文说明](./README.zh-CN.md)

BuddyHub is a Buddy enhancement plugin for Claude Code.

BuddyHub is intended to enhance the user's current Claude Buddy, not replace it with a BuddyHub-defined pet.

Current product status:

- BuddyHub can verify the current official Buddy identity
- BuddyHub can track Claude-side runtime state
- BuddyHub has not yet unlocked third-party native control of the official bottom-right Buddy

Core product rule:

- the real target is the official Claude Code Buddy already shown in the bottom-right UI
- text commands and status-line output are diagnostic/supporting surfaces only
- text output alone does not count as product completion

Current repo state:

- hook-driven state tracking
- verified Buddy identity reading
- `/buddyhub:status` compact diagnostic view
- `/buddyhub:open` detailed diagnostic view
- optional Claude Code status line integration
- safe pause, resume, disable, and uninstall flows

Identity rule:

- verified Buddy identity fields may be shown
- unavailable Buddy identity fields must stay unavailable
- BuddyHub must not fabricate a generic Buddy appearance and present it as the user's Buddy

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
- `/buddyhub:pet-install`
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
- diagnostic text/status surfaces

What still needs real-world verification:

- a plugin-accessible control path to the official native Buddy
- visible enhancement of the official bottom-right Buddy
- real hook-to-native-Buddy state propagation
- manual status line wiring
- at least one cross-terminal smoke pass for diagnostic surfaces

## License

BuddyHub is licensed under `AGPL-3.0-only` (GNU Affero General Public
License v3.0 only). If you distribute modified versions, or let users
interact with modified versions over a network, you must provide the
corresponding source under AGPLv3. See
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE).

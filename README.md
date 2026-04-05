# BuddyHub

[中文说明](./README.zh-CN.md)

BuddyHub is a standalone TUI configurator for the official Claude Code Buddy.

It lets you adjust the real Buddy shown in Claude Code, preview the result, apply the change, restore it, and uninstall BuddyHub from one menu.

## Install

Install directly from GitHub with `npm`:

```bash
npm install -g github:verycafe/buddyhub
```

Then launch BuddyHub:

```bash
buddyhub
```

## Menu

Current top-level menu:
- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Uninstall`
- `Quit`

Current scope:
- element switching is hidden in this phase
- BuddyHub keeps the currently installed element as-is, or keeps `none` if no element is installed
- this phase only exposes `Color` and `Nickname` as user-editable draft settings

The TUI reads the current installed Buddy first and shows a live preview panel on the right side.

After `Apply`, restart Claude Code to reload the official Buddy.

`Uninstall` is fully automatic:
- it restores the Buddy first if BuddyHub has an active patch
- removes old Claude plugin traces such as `~/.claude/plugins/.../buddyhub*`
- removes BuddyHub standalone data under `~/.buddyhub`
- schedules npm uninstall in the background for the current BuddyHub install

## Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## License

BuddyHub is licensed under `AGPL-3.0-only` (GNU Affero General Public
License v3.0 only). If you distribute modified versions, or let users
interact with modified versions over a network, you must provide the
corresponding source under AGPLv3. See
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE).

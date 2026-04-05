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

On first launch, BuddyHub uses the system locale for the menu language when it can detect one cleanly.

## Platform Detection

- BuddyHub first tries to detect Claude automatically by resolving the installed `claude` launcher on `PATH`
- On macOS and Linux, BuddyHub also scans the standard Claude versions directory when available
- If auto-detection is still incomplete, BuddyHub opens `Setup` and guides the user to enter:
  - the Claude executable path
  - the Claude config path

BuddyHub keeps those override paths in its own settings and reuses them on later launches.

Setup also shows path-finding hints such as:

- `which claude` on macOS/Linux
- `where claude` on Windows
- `claude doctor` as an extra reference

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
- this phase only exposes `Color` and `Nickname` as user-editable settings

The TUI reads the current installed Buddy first and shows a live preview panel on the right side.

After `Apply`, restart Claude Code to reload the official Buddy.

`Uninstall` is fully automatic:
- it restores the Buddy first if BuddyHub has an active patch
- removes old Claude plugin traces such as `~/.claude/plugins/.../buddyhub*`
- removes BuddyHub standalone data under `~/.buddyhub`
- schedules npm uninstall in the background for the current BuddyHub install

## Docs

- [V0.2/README.md](/Users/tvwoo/Projects/buddyhub/V0.2/README.md)
- [V0.2/PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)
- [V0.2/specs/README.md](/Users/tvwoo/Projects/buddyhub/V0.2/specs/README.md)
- [V0.2/SPEC-STATUS.md](/Users/tvwoo/Projects/buddyhub/V0.2/SPEC-STATUS.md)
- [V0.1/README.md](/Users/tvwoo/Projects/buddyhub/V0.1/README.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## License

BuddyHub is licensed under `AGPL-3.0-only` (GNU Affero General Public
License v3.0 only). If you distribute modified versions, or let users
interact with modified versions over a network, you must provide the
corresponding source under AGPLv3. See
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE).

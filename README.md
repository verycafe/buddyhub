# BuddyHub

[中文说明](./README.zh-CN.md)

BuddyHub is a native visual-customization project for the official Claude Code Buddy.

Its target is only the existing Buddy in the bottom-right Claude Code UI.

## Current Direction

BuddyHub is now focused on one problem only:

- enhance the user's real official Buddy with configurable additive visual elements
- provide a standalone TUI menu for color and optional nickname behavior while keeping element switching hidden in the current release
- apply the saved customization and prompt the user to restart Claude Code

BuddyHub is not currently focused on:

- Claude runtime state tracking
- status-line-first UX
- hook-driven Buddy behavior
- parallel text Buddy products

## What We Have Already Proven

- the official Buddy visual tables are embedded in the Claude Code executable
- on the current macOS machine, the validated example binary is:
  - `/Users/tvwoo/.local/share/claude/versions/2.1.92`
- patching a workspace copy of that binary changed the official bottom-right Buddy itself
- the current verified additive element set for `blob` includes:
  - `tophat`
  - `coffee`
  - `book`
- the current verified color presets are:
  - `green`
  - `orange`
  - `blue`
  - `pink`
  - `purple`
  - `red`
  - `black`
- the current unverified preset still shown as unavailable is:
  - `white`
- the official displayed Buddy name can be overridden safely through:
  - `~/.claude.json` `companion.name`
- the bottom-right Buddy and the `/buddy` companion card share the same displayed-name and verified color sources
- `~/.claude/pet` is not the main delivery path for the official Buddy visual enhancement goal

## Product Rule

The product counts as successful only when the official Claude Code Buddy itself is visually enhanced.

Text output, diagnostics, or helper commands do not count as the product UI.

## Current Repo Focus

- native Buddy visual research
- version-sensitive binary patching
- external TUI menu for Buddy customization
- backup and restore safety
- verification of official Buddy visual changes

## Current TUI Entry

Run the standalone BuddyHub menu with:

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub
```

## Install Without a Publisher Account

BuddyHub can now be installed directly from GitHub without publishing to PyPI, npm, or Homebrew first.

### pip

Install from GitHub:

```bash
python3 -m pip install "git+https://github.com/verycafe/buddyhub.git"
```

Then run:

```bash
buddyhub
```

### npm

Install from GitHub:

```bash
npm install -g github:verycafe/buddyhub
```

Then run:

```bash
buddyhub
```

### brew

Tap the repository, then install:

```bash
brew tap verycafe/buddyhub https://github.com/verycafe/buddyhub
brew install verycafe/buddyhub/buddyhub
```

Then run:

```bash
buddyhub
```

Current top-level menu:
- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Quit`

Current scope note:
- element switching is hidden in this phase
- BuddyHub keeps the currently installed element as-is, or keeps `none` if no element is installed
- this phase only exposes `Color` and `Nickname` as user-editable draft settings

The TUI reads the current installed Buddy state first, then shows:
- `Installed State`
- `Draft State`
- `Installed Preview`
- `Draft Preview`

After `Apply` or `Restore`, the TUI shows a dedicated result card instead of relying on a single footer line.
The result card also summarizes which visible Buddy properties changed, such as:
- `Display name`
- `Color`

For a quick non-interactive check:

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub --dump-state
```

## Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## Important Scope Note

The currently validated native path is an implementation detail for the current machine and install.

It is not yet documented as a stable public Claude Code API or a guaranteed cross-platform path.

## License

BuddyHub is licensed under `AGPL-3.0-only` (GNU Affero General Public
License v3.0 only). If you distribute modified versions, or let users
interact with modified versions over a network, you must provide the
corresponding source under AGPLv3. See
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE).

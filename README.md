# BuddyHub

[中文说明](./README.zh-CN.md)

BuddyHub is a native visual-customization project for the official Claude Code Buddy.

Its target is only the existing Buddy in the bottom-right Claude Code UI.

## Current Direction

BuddyHub is now focused on one problem only:

- enhance the user's real official Buddy with configurable additive visual elements
- provide a guided customization flow for element, color, and optional nickname behavior
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
- `~/.claude/pet` is not the main delivery path for the official Buddy visual enhancement goal

## Product Rule

The product counts as successful only when the official Claude Code Buddy itself is visually enhanced.

Text output, diagnostics, or helper commands do not count as the product UI.

## Current Repo Focus

- native Buddy visual research
- version-sensitive binary patching
- additive element catalog, settings model, and guided settings flow
- backup and restore safety
- verification of official Buddy visual changes

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

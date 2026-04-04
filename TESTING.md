# BuddyHub Testing Guide

- Status: Draft v0.1
- Date: 2026-04-04
- Scope: BuddyHub V1 TUI-first plugin verification

## 1. Goal

This document defines the first real-world test pass for BuddyHub.

The purpose is to verify that:

- the plugin installs correctly in Claude Code
- text commands work in a real Claude session
- hook-driven state changes update BuddyHub state
- Buddy identity is read from a real Claude source rather than invented by BuddyHub
- the optional status line can be connected manually
- BuddyHub can be paused, resumed, disabled, and uninstalled safely

## 2. Current Product Shape

BuddyHub V1 is `TUI-first`.

Primary UI surfaces:

- `/buddyhub:status`
- `/buddyhub:open`
- Claude Code status line via [statusline.py](/Users/tvwoo/Projects/buddyhub/plugins/buddyhub/scripts/statusline.py)

BuddyHub V1 does not require:

- external GUI windows
- terminal-specific graphics
- tmux

## 3. Prerequisites

Before running the first real test pass, confirm:

1. Claude Code is installed and logged in.
2. The current machine can run Claude Code plugins.
3. The current repo is available locally at [/Users/tvwoo/Projects/buddyhub](/Users/tvwoo/Projects/buddyhub).
4. The user can add a custom marketplace and install a plugin from it.

## 4. Install Path To Test

Expected installation flow:

```text
/plugin marketplace add verycafe/buddyhub
/plugin install buddyhub@buddyhub
```

Expected outcome:

- BuddyHub installs without manual file copying.
- BuddyHub commands become available in Claude Code.
- BuddyHub creates runtime data only after first use or first hook event.

## 5. Status Line Setup To Test

BuddyHub does not auto-edit Claude Code settings in V1.

Test flow:

1. Run `/buddyhub:statusline-on`
2. Copy the script path shown by the command
3. Configure Claude Code status line to call that script
4. Verify the status line renders one short Buddy line

Expected output pattern:

```text
Crumpet | blob | idle
Crumpet | blob | reading | buddyhub
identity unavailable | paused
```

## 6. Core Smoke Tests

### 6.1 Command discovery

Run:

- `/buddyhub:help`

Verify:

- command list is visible
- TUI-first wording is visible
- status line script path is shown

### 6.2 Compact state view

Run:

- `/buddyhub:status`

Verify:

- lifecycle is shown
- Buddy state is shown
- active session/project fields are present
- last update time is present

### 6.3 Detail view

Run:

- `/buddyhub:open`

Verify:

- richer text detail view is shown
- quick actions are shown
- identity section degrades gracefully when unavailable
- Buddy name/species match the current Claude Buddy source when available
- no fabricated rarity, shiny, hat, eye, or stats are shown when unavailable
- no generic Buddy body is presented as the user's actual Buddy

### 6.4 Lifecycle controls

Run:

- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`

Verify:

- each command returns a clear confirmation
- Claude Code remains usable after each command
- `/buddyhub:status` reflects the lifecycle change

### 6.5 Status line request controls

Run:

- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

Verify:

- request state toggles correctly
- no hidden config changes are made automatically

## 7. Hook-Driven Runtime Tests

These tests must be run in a real Claude Code session, not only by local script simulation.

### 7.1 Read path

Cause Claude Code to read files.

Verify:

- Buddy state becomes `reading`
- `/buddyhub:status` reflects the update
- status line updates if configured

### 7.2 Edit path

Cause Claude Code to edit files.

Verify:

- Buddy state becomes `coding`

### 7.3 Bash path

Cause Claude Code to run a shell command.

Verify:

- Buddy state becomes `running`

### 7.4 Stop path

Allow Claude Code to finish a task.

Verify:

- Buddy state becomes `done`
- the state later settles safely

### 7.5 Session end path

End the session or start a fresh one.

Verify:

- inactive session no longer keeps driving current Buddy state
- state falls back safely to `idle` when appropriate

### 7.6 Identity source path

Verify in a real Claude Code session:

- BuddyHub reads the current Buddy identity from a real Claude source such as transcript attachment metadata when available
- displayed `name/species` match the current Claude Buddy
- fields not present in the source remain `unknown` or `unavailable`
- reverse-engineered schema fields are not shown as if they were confirmed user values

## 8. Safety Tests

### 8.1 Fail-open command behavior

If a BuddyHub command fails internally:

- Claude Code should still continue working
- the user should still be able to continue the session

### 8.2 Disable without uninstall

Run:

- `/buddyhub:disable`

Verify:

- plugin remains installed
- BuddyHub stops active updates
- `/buddyhub:resume` restores operation

### 8.3 Uninstall path

Run:

- `/buddyhub:uninstall`

Verify:

- cleanup is explained clearly
- BuddyHub data files are removed
- plugin removal is attempted or clearly guided
- Claude Code remains usable

## 9. Expected Data Paths

Default runtime path:

```text
~/.claude/plugins/data/buddyhub
```

Expected runtime files:

- `runtime.json`
- `sessions.json`
- `ownership.json`
- `state.lock`

Legacy runtime leftovers may exist from earlier experimental builds:

- `sidecar.pid`
- `ui-request.json`
- `sidecar.log`

These are not required for V1.

## 10. What Is Already Verified Locally

The following has already been verified in local script-level testing:

- Python scripts compile
- marketplace manifest validates
- plugin manifest validates
- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:open`
- `/buddyhub:doctor`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`
- `statusline.py`
- simulated hook mapping for `Read -> reading`
- uninstall cleanup in a temporary data directory

## 11. Remaining Work Before We Can Say "Ready For User Testing"

The main remaining gaps are not local implementation blockers. They are real-environment verification tasks:

1. Real Claude Code installation test in a logged-in session
2. Real hook payload verification inside Claude Code
3. Manual status line wiring test in Claude Code settings
4. At least one cross-terminal smoke pass

Recommended first terminal matrix:

- Ghostty
- one other terminal, such as Terminal.app or iTerm2

## 12. Suggested First Test Sequence

If we want the shortest useful first manual pass, do this:

1. Install BuddyHub from the local marketplace flow
2. Run `/buddyhub:help`
3. Run `/buddyhub:status`
4. Run `/buddyhub:open`
5. Turn on status line request mode
6. Wire the status line script manually
7. Trigger one file read, one edit, and one bash command
8. Run `/buddyhub:pause`
9. Run `/buddyhub:resume`
10. Run `/buddyhub:disable`
11. Run `/buddyhub:uninstall`

If all of these pass in a real Claude session, BuddyHub is ready for the next iteration.

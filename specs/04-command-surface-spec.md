# Buddy Command Surface Spec

- Status: Draft v0.3
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum command surface for BuddyHub.

Commands focus on:

- understanding current state
- controlling lifecycle
- troubleshooting
- supporting research and verification of the official Buddy enhancement path

## 2. Command Design Principles

Commands must be:

- short
- explicit
- understandable without reading source code
- safe to run in any normal Claude Code terminal session

BuddyHub uses namespaced commands such as `/buddyhub:*`.

Important rule:

- commands are supporting tools
- commands must not be treated as the core Buddy UI
- the core Buddy UI goal remains enhancement of the official bottom-right Buddy
- command success does not imply native Buddy enhancement success

## 3. Required Commands

BuddyHub must include at least:

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:open`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:uninstall`
- `/buddyhub:doctor`

## 4. Required Diagnostic Commands

### 4.1 `/buddyhub:help`

Must show:

- what BuddyHub is
- current BuddyHub state summary
- Buddy identity preservation rule
- the rule that official native Buddy enhancement is the real target
- the available commands
- where the status line script lives

### 4.2 `/buddyhub:status`

Must show a compact diagnostic summary:

- lifecycle status
- current Buddy state
- verified Buddy name/species when available
- status line requested mode
- active session
- current project
- last update time
- whether the official native Buddy enhancement path is confirmed, experimental, or unavailable

### 4.3 `/buddyhub:open`

Must open the richer diagnostic detail view.

It must not require any GUI.

It should show:

- lifecycle
- Buddy state
- Buddy name
- project/session context
- last event and update time
- quick actions
- verified identity fields only when available
- current native-control-path status when known

It must not:

- invent rarity, shiny, hat, eye, or stats
- render a generic Buddy body as if it were the user's Buddy
- present itself as the finished Buddy product if the native official Buddy is not being enhanced
- hide the fact that native Buddy control is currently blocked or experimental

## 5. Lifecycle Commands

### 5.1 `/buddyhub:pause`

Must suspend automatic BuddyHub updates without breaking Claude Code.

### 5.2 `/buddyhub:resume`

Must restore automatic BuddyHub updates.

### 5.3 `/buddyhub:disable`

Must explicitly turn BuddyHub off without uninstalling it.

### 5.4 `/buddyhub:uninstall`

Must remain the single user-facing uninstall entrypoint.

## 6. Diagnostic Commands

### 6.1 `/buddyhub:doctor`

Must help diagnose:

- lifecycle state
- current Buddy state
- status line requested mode
- configuration or runtime file presence
- native Buddy control-path status when known
- legacy runtime leftovers when relevant

## 7. Optional Commands

BuddyHub may additionally include:

- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

These are supporting diagnostic tools only. They do not replace native Buddy enhancement.

## 8. Acceptance Criteria

This spec is satisfied when:

1. The user can discover BuddyHub via `/buddyhub:help`.
2. The user can inspect compact diagnostic state via `/buddyhub:status`.
3. The user can open a richer diagnostic detail view via `/buddyhub:open`.
4. The user can pause, resume, disable, and uninstall BuddyHub.
5. The user can diagnose BuddyHub without any GUI dependency.
6. Command output never substitutes an invented Buddy identity for the user's current Buddy.
7. Command output never claims to satisfy the product goal if the official native Buddy is not actually being enhanced.

Current blocker note:

- if commands work but native `companionReaction` cannot be written from a third-party plugin, command output must make that limitation explicit

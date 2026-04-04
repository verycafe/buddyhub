# Buddy Command Surface Spec

- Status: Draft v0.2
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum command surface for BuddyHub V1.

V1 commands focus on:

- understanding current state
- controlling lifecycle
- exposing a text-first Buddy UI
- troubleshooting

## 2. Command Design Principles

Commands must be:

- short
- explicit
- understandable without reading source code
- safe to run in any normal Claude Code terminal session

V1 uses namespaced commands such as `/buddyhub:*`.

## 3. Required Commands

V1 must include at least:

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:open`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:uninstall`
- `/buddyhub:doctor`

## 4. Required UI Commands

### 4.1 `/buddyhub:help`

Must show:

- what BuddyHub is
- current BuddyHub state summary
- the available commands
- where the status line script lives

### 4.2 `/buddyhub:status`

Must show a compact text summary:

- lifecycle status
- current Buddy state
- status line requested mode
- active session
- current project
- last update time

### 4.3 `/buddyhub:open`

Must open the richer text detail view.

It must not require any GUI.

It should show:

- lifecycle
- Buddy state
- Buddy name
- project/session context
- last event and update time
- quick actions
- verified identity fields only when available

## 5. Lifecycle Commands

### 5.1 `/buddyhub:pause`

Must suspend automatic Buddy updates without breaking Claude Code.

### 5.2 `/buddyhub:resume`

Must restore automatic Buddy updates.

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
- legacy runtime leftovers when relevant

## 7. Optional Commands

V1 may additionally include:

- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

These are recommended because status line is the primary ambient UI in V1.

## 8. Acceptance Criteria

This spec is satisfied when:

1. The user can discover BuddyHub via `/buddyhub:help`.
2. The user can inspect compact state via `/buddyhub:status`.
3. The user can open a richer text detail view via `/buddyhub:open`.
4. The user can pause, resume, disable, and uninstall BuddyHub.
5. The user can diagnose BuddyHub without any GUI dependency.

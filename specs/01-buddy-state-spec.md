# Buddy State Spec

- Status: Draft v0.1
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum state model for BuddyHub V1.

This spec covers:

- Claude-observed runtime states
- BuddyHub lifecycle states
- mapping rules
- state priority
- fallback behavior

This spec does not define:

- final sprite art
- exact file paths
- MCP-based memory states

## 2. Goals

BuddyHub must turn observable Claude Code behavior into a small, stable Buddy state machine.

The model must be:

- easy to reason about
- robust against partial failures
- independent from undocumented Claude internals

## 3. Inputs

BuddyHub V1 may use the following inputs:

- Claude Code hook events
- hook event metadata
- Claude session identity metadata when available
- workspace or project identity when available
- local state files written by BuddyHub
- optional status line context
- explicit command inspection requests

V1 must not require:

- tmux
- hidden Claude internal APIs
- cloud services

## 4. BuddyHub Lifecycle States

BuddyHub itself has these lifecycle states:

- `installed`
- `enabled`
- `paused`
- `disabled`
- `error`
- `uninstalled`

### 4.1 Definitions

- `installed`: plugin assets exist and BuddyHub is available
- `enabled`: BuddyHub is active and allowed to update UI
- `paused`: BuddyHub remains installed but stops automatic Buddy activity
- `disabled`: BuddyHub is explicitly turned off by the user
- `error`: BuddyHub encountered an internal failure; Claude Code must continue to work
- `uninstalled`: BuddyHub is removed and no longer active

## 4.2 Session Ownership Model

BuddyHub V1 must treat state as session-scoped first, not globally flat.

Minimum model:

- one per-session state record
- one active-session pointer for display purposes

Each per-session state record should be attributable to:

- `session_id` when available
- process or runtime instance identifier when available
- workspace or project identity when available

Why this is required:

- multiple Claude Code sessions may coexist
- a single global last-writer state is not reliable enough

## 5. Claude Runtime States

V1 defines these visible Buddy states:

- `idle`
- `thinking`
- `reading`
- `coding`
- `running`
- `browsing`
- `waiting`
- `done`
- `error`

## 6. Source-to-State Mapping

### 6.1 Hook-driven mappings

The initial state mapping should follow the current validated local prototype pattern:

- `Read|Glob|Grep -> reading`
- `Edit|Write|NotebookEdit -> coding`
- `Bash -> running`
- `WebFetch|WebSearch -> browsing`
- `AskUserQuestion -> waiting`
- `Task -> thinking` or `exploring-like thinking`
- unknown tool activity -> `thinking`

### 6.2 Non-tool mappings

- `PostToolUse -> thinking`
- `Stop -> done`
- `Notification -> waiting`

### 6.3 Session lifecycle mappings

V1 must explicitly handle session lifecycle transitions.

Required rules:

- `SessionStart -> idle` or a short initialization state that resolves to `idle`
- `SessionEnd -> idle` and mark the session inactive
- a finished session must not continue driving the Buddy indefinitely

If a session becomes unavailable without a clean end event:

- the session must age out based on staleness rules

### 6.4 Idle timeout

If no state update is received within a configurable inactivity window, Buddy transitions to `idle`.

V1 requirement:

- idle timeout must exist
- timeout value must be configurable later
- timeout failure must not crash BuddyHub

### 6.5 Stale state invalidation

BuddyHub must invalidate stale session state.

Required behavior:

- stale runtime state must not survive forever
- `done` and `waiting` states must eventually expire to `idle` if their source session is no longer active
- if the active-session pointer refers to a missing or expired session, BuddyHub must select another valid session or fall back to `idle`

This rule exists partly to protect against:

- abrupt Claude exits
- stale local files
- transcript resets or session continuity breaks
- `/clear`-like session resets that invalidate prior volatile context

## 7. State Priority Rules

When multiple candidate states exist, apply this order:

1. lifecycle override states
2. explicit error state
3. transient interaction state
4. active session Claude runtime state
5. idle fallback

### 7.1 Lifecycle override behavior

- If BuddyHub is `paused`, UI must show `paused` or hide dynamic updates
- If BuddyHub is `disabled`, UI must not continue active runtime reporting beyond explicit command output
- If BuddyHub is in `error`, UI may show a degraded error indicator, but must not loop aggressively

### 7.2 Transient UI states

The UI may temporarily enter interaction-only states such as:

- clicked
- hovered
- petted

These must never overwrite lifecycle truth.

They are display-only overlays.

### 7.3 Active session selection

V1 must define how one session becomes the display-driving session.

Default rule:

- if only one valid session exists, use it
- if multiple valid sessions exist, use the most recently updated active session
- if the user explicitly opens or inspects a session, that session may become the display-driving session until it expires or focus changes

If no valid session can be selected:

- fall back to `idle`

## 8. State Persistence

V1 must persist enough information to recover current state safely after short restarts.

Minimum persisted fields:

- current Buddy runtime state
- last update timestamp
- last known source event
- BuddyHub lifecycle state
- `session_id` when available
- workspace or project identity when available
- active-session pointer or equivalent

Persistence requirements:

- format must be machine-readable
- writes must be low-cost
- corrupt state must fail open
- per-session records must not overwrite each other blindly

## 9. Failure Behavior

### 9.1 Invalid state data

If state data is missing or malformed:

- BuddyHub must not crash Claude Code
- Buddy should fall back to `idle` or a safe blank state

### 9.2 Missing hook events

If hooks are unavailable or temporarily not firing:

- BuddyHub must degrade gracefully
- text surfaces may continue showing the last safe state until timeout
- status line must remain optional and independent

### 9.3 Session continuity breaks

If session continuity breaks unexpectedly, for example because a session is reset or replaced:

- BuddyHub must not keep trusting stale volatile state indefinitely
- the affected session may be reinitialized as a new logical session
- display should fall back to `idle` or another valid active session

### 9.4 Text UI surface unavailable

If one BuddyHub UI surface is unavailable:

- lifecycle state may remain valid
- Claude Code must continue unaffected
- another text surface such as `/buddyhub:status` or `/buddyhub:open` must still work if possible

## 10. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub can represent the required lifecycle states.
2. BuddyHub can represent the required Claude runtime states.
3. Hook events can be mapped into Buddy states without undocumented APIs.
4. Missing or corrupt state data does not break Claude Code.
5. Idle fallback exists and works predictably.
6. Multiple concurrent sessions do not blindly overwrite one another's state.
7. Session start, end, and stale-session cleanup rules are defined and recover gracefully.

# Buddy UI Spec

- Status: Draft v0.2
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define BuddyHub V1 UI surfaces and interaction behavior.

BuddyHub V1 is `TUI-first`.

This spec covers:

- Claude Code status line output
- text detail view
- compact status output
- command-driven control surfaces

This spec does not cover:

- external GUI windows
- legacy desktop visual modes
- terminal-specific graphics protocols
- internal Claude Code UI injection

## 2. UI Strategy

BuddyHub V1 must work across different terminal products without depending on terminal-specific GUI behavior.

Therefore the primary UI surfaces are:

1. `status line`
2. `text detail view`
3. `compact status output`

All of them must work with ordinary text rendering.

BuddyHub may use generic state indicators, but it must not present a fabricated surrogate creature as if it were the user's actual Buddy.

## 3. Supported UI Surfaces

### 3.1 Status line

The status line is the default ambient UI surface.

Requirements:

- one concise line
- low interruption
- no cursor tricks
- no terminal-specific graphics requirements

Example:

- `Crumpet | blob | thinking | repo-name`

### 3.2 Text detail view

The text detail view is opened via `/buddyhub:open`.

It must show:

- Buddy name
- lifecycle status
- current Buddy state
- active session when available
- current project when available
- last event
- last update time
- quick actions

If verified Buddy identity exists, it may additionally show:

- species
- rarity
- shiny status

If identity is unavailable, the view must say so explicitly and must not invent values.

The detail view must also follow these appearance rules:

- it may render generic state indicators
- it must not render a generic Buddy body as a stand-in for the user's actual Buddy appearance
- if only `name/species` are verified, the UI must stop there
- if `hat/eye/rarity/shiny/stats` are unverified, the UI must not synthesize them

### 3.3 Compact status output

The compact status output is `/buddyhub:status`.

It should stay shorter than the detail view and focus on:

- lifecycle
- current state
- verified Buddy identity when available
- status line requested mode
- active session/project
- last update time

## 4. Control Rules

V1 UI must respect these rules:

- the user can use BuddyHub without any GUI surface
- the user can access all primary state through text commands
- the user can request status line mode explicitly
- UI output must degrade gracefully when optional integrations are not configured

## 5. Terminal Compatibility

BuddyHub V1 must assume users may run Claude Code in different terminal products.

Therefore V1 must not require:

- Ghostty-specific features
- iTerm-specific features
- Kitty graphics protocol
- tmux
- external desktop automation

The design target is:

- if the terminal can render ordinary Claude Code text output, BuddyHub UI should still work

## 6. Status Line Sync Spec

### 6.1 Role

Status line sync is the primary ambient Buddy surface in V1.

### 6.2 Display rules

Status line output must:

- stay on one line
- remain readable at a glance
- not pretend advanced UI exists when it does not
- not imply a fabricated Buddy appearance

### 6.3 Control

BuddyHub must provide a way to request status line mode and a way to turn that request off.

V1 command surface:

- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

## 7. Explicit Non-Goals

V1 UI does not guarantee:

- floating windows
- embedded widgets
- native Buddy graphics
- cross-terminal pixel rendering
- invented Buddy appearance fallback

## 8. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub can be used entirely through text UI.
2. `/buddyhub:status` provides a compact current-state view.
3. `/buddyhub:open` provides a richer text detail view.
4. Status line output remains available as an optional ambient surface.
5. No GUI surface is required to use BuddyHub.
6. The UI strategy does not depend on a specific terminal product.
7. The UI never replaces the user's Buddy identity with an invented generic Buddy.

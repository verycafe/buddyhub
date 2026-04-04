# Buddy UI Spec

- Status: Draft v0.3
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define BuddyHub UI surfaces and interaction behavior.

BuddyHub's primary product target is the official Claude Code Buddy already shown in the bottom-right UI.

This spec covers:

- the official native Buddy surface
- supporting diagnostic text views
- optional status line output
- command-driven lifecycle and diagnostic surfaces

This spec does not cover:

- external GUI windows
- legacy desktop visual modes
- terminal-specific graphics protocols
- surrogate Buddy products that replace the official native Buddy

## 2. UI Strategy

BuddyHub must enhance the user's existing official Buddy, not create a second Buddy that competes with it.

Therefore the UI hierarchy is:

1. `official native Buddy in Claude Code's bottom-right UI`
2. `diagnostic text detail view`
3. `diagnostic compact status output`
4. `optional status line`

Text surfaces may exist for debugging and verification, but they do not satisfy the product goal by themselves.

## 3. Supported UI Surfaces

### 3.1 Official native Buddy surface

The primary BuddyHub UI surface is the official Claude Code Buddy that Claude Code renders in the bottom-right UI.

Requirements:

- BuddyHub must enhance this existing native surface rather than replacing it
- the enhanced state must be visibly attached to the user's real Buddy identity
- BuddyHub must not render a second surrogate Buddy and call that the product
- success criteria require visible native Buddy dynamics, not only text output

This spec does not yet assume a confirmed technical control path to the native surface.

Until such a path is confirmed:

- any text surfaces are diagnostic only
- the product is still incomplete against the main UI goal
- the repository should explicitly describe this as a native-control-path blocker, not as a finished MVP

### 3.2 Diagnostic text detail view

The text detail view is opened via `/buddyhub:open`.

It is a supporting diagnostic surface, not the primary product UI.

It must show:

- Buddy name
- lifecycle status
- current Buddy state
- active session when available
- current project when available
- last event
- last update time
- quick actions
- current native-control-path status when known

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

### 3.3 Diagnostic compact status output

The compact status output is `/buddyhub:status`.

It is a supporting diagnostic surface, not the primary product UI.

It should stay shorter than the detail view and focus on:

- lifecycle
- current state
- verified Buddy identity when available
- status line requested mode
- active session/project
- last update time
- whether the official native Buddy enhancement path is confirmed, experimental, or unavailable

### 3.4 Optional status line

Status line output is optional and diagnostic.

It may summarize state, but it must not be treated as the core Buddy experience.

## 4. Control Rules

BuddyHub UI must respect these rules:

- the user can inspect BuddyHub through text commands even while the native Buddy path is under development
- text commands must help diagnose whether native Buddy enhancement is working
- the user can request status line mode explicitly
- UI output must degrade gracefully when optional integrations are not configured
- no diagnostic surface may be presented as equivalent to native official Buddy enhancement

## 5. Terminal Compatibility

BuddyHub must assume users may run Claude Code in different terminal products.

Therefore supporting diagnostic surfaces must not require:

- Ghostty-specific features
- iTerm-specific features
- Kitty graphics protocol
- tmux
- external desktop automation

The design target for supporting diagnostic surfaces is:

- if the terminal can render ordinary Claude Code text output, BuddyHub diagnostics should still work

## 6. Status Line Sync Spec

### 6.1 Role

Status line sync is a supporting diagnostic surface, not the primary Buddy experience.

### 6.2 Display rules

Status line output must:

- stay on one line
- remain readable at a glance
- not pretend advanced UI exists when it does not
- not imply a fabricated Buddy appearance

### 6.3 Control

BuddyHub must provide a way to request status line mode and a way to turn that request off.

Command surface:

- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

## 7. Explicit Non-Goals

BuddyHub UI does not guarantee:

- floating windows
- a second Buddy UI as the shipped product
- cross-terminal pixel rendering
- invented Buddy appearance fallback

BuddyHub must not redefine the product as a text Buddy if native official Buddy enhancement remains unresolved.

## 8. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub visibly enhances the official Claude Code Buddy in the native bottom-right UI.
2. Native Buddy dynamics are driven by verified Buddy identity and Claude activity state.
3. `/buddyhub:status` provides a compact diagnostic current-state view.
4. `/buddyhub:open` provides a richer diagnostic detail view.
5. Status line output remains optional and secondary.
6. The UI strategy does not depend on a specific terminal product for its diagnostic surfaces.
7. The UI never replaces the user's Buddy identity with an invented generic Buddy.
8. Text output alone does not count as meeting the primary UI requirement.

Current blocker note:

- as of 2026-04-04, no supported third-party plugin path has been confirmed for writing native `companionReaction`
- therefore this spec remains blocked at the native-control layer even if diagnostic text views are working

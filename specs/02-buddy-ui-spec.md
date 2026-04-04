# Buddy UI and Settings Spec

- Status: Draft v0.5
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the user-facing UI contract for BuddyHub.

## 2. Primary Product UI

BuddyHub has only one primary product UI surface:

- the official Claude Code Buddy already rendered in the bottom-right UI

This is the product surface.

## 3. What Counts As UI Success

UI success means:

- the user looks at the existing bottom-right official Buddy
- the Buddy is visually different because BuddyHub enhanced its native elements
- the change remains attached to the user's real Buddy identity

UI success does not mean:

- a text page changed
- a diagnostic command worked
- a status line was updated

## 4. Allowed UI Enhancements

V1 may enhance:

- additive top-row elements such as hats, coffee, books, or similar accessories
- additive face or side embellishments
- verified native color changes
- verified nickname display near the official Buddy label

V1 should prefer enhancements that feel like added accessories rather than species replacement.

## 5. Disallowed UI Directions

BuddyHub UI must not become:

- a parallel text Buddy
- a floating pet window
- a surrogate ASCII pet
- a TUI-first replacement for the official Buddy

## 6. Secondary Control Surface

BuddyHub must provide a settings surface as a control UI.

This settings surface is not the product target itself.

Its job is to let the user:

- choose an element
- choose a color preset
- set or clear a nickname
- view preview output
- apply changes
- restore the original visual

For the current public Claude Code plugin surface, this settings UI is expected to be a guided configuration flow.

It must not assume the public plugin config dialog already supports:

- dropdown-style element choices
- native color swatches
- live official Buddy preview inside the dialog

## 7. Preview Rules

BuddyHub must provide preview behavior, but preview must be described honestly.

V1 may support:

- static preview generated from known patch profiles
- rehearsal-target preview
- preview cards that represent the chosen element and color combination

V1 must not claim:

- that the currently running Claude Code process has live-updated itself
- that the official Buddy is already changed before restart and verification

## 8. Restart Reality

Because the current patch path modifies the installed Claude Code binary, the expected user experience is:

1. apply customization
2. show explicit restart guidance
3. restart Claude Code
4. see the official Buddy update

This restart requirement is part of the UI contract for this phase.

## 9. Platform Reality

The official Buddy UI is native to Claude Code.

Therefore:

- BuddyHub does not define its own cross-terminal rendering strategy for the product UI
- terminal compatibility matters for diagnostics and settings only
- the product UI target is whatever Claude Code itself renders

## 10. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub enhances the official bottom-right Buddy itself.
2. The official Buddy remains in its native location.
3. No second Buddy UI is introduced as the product.
4. A settings surface exists for customization control.
5. Preview is available without overstating live-update support.
6. Restart is clearly surfaced as part of apply behavior.

# Buddy UI Spec

- Status: Draft v0.4
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the single UI target for BuddyHub.

## 2. Primary UI Surface

BuddyHub has only one primary UI surface:

- the official Claude Code Buddy already rendered in the bottom-right UI

This is the product surface.

## 3. What Counts As UI Success

UI success means:

- the user looks at the existing bottom-right official Buddy
- the Buddy is visually different because BuddyHub enhanced its native elements
- the change is attached to the user's real Buddy identity

UI success does not mean:

- a text page changed
- a diagnostic command worked
- a status line was updated

## 4. Allowed UI Enhancements

V1 may enhance:

- top-row elements such as hats or accessories
- species-specific frame details
- face or eye-related visual details
- other small native embellishments already attached to the official Buddy render path

## 5. Disallowed UI Directions

BuddyHub UI must not become:

- a parallel text Buddy
- a floating pet window
- a surrogate ASCII pet
- a TUI-first replacement for the official Buddy

## 6. Diagnostic Surfaces

Diagnostic surfaces may still exist, but they are not the product UI.

They may help answer:

- which Buddy identity is currently verified
- which installed Claude version is being targeted
- whether a visual patch has been applied
- whether restore is needed

They must never be described as equivalent to the official Buddy enhancement itself.

## 7. Platform Reality

The official Buddy UI is native to Claude Code.

Therefore:

- BuddyHub does not define its own cross-terminal rendering strategy for the product UI
- terminal compatibility matters for diagnostics only
- the product UI target is whatever Claude Code itself renders

## 8. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub enhances the official bottom-right Buddy itself.
2. The official Buddy remains in its native location.
3. No second Buddy UI is introduced as the product.
4. Diagnostic text is treated as secondary.
5. Visual enhancement stays attached to the user's real Buddy identity.

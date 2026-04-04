# Buddy Visual Element Spec

- Status: Draft v0.2
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum visual-element model for BuddyHub.

This spec covers:

- official Buddy identity inputs
- native visual element targets
- patchable visual slots
- version-sensitive patch rules
- visual verification rules

This spec does not cover:

- Claude runtime state
- reaction/state machines
- hook mappings
- status line rendering

## 2. Core Rule

BuddyHub V1 must modify only the official Buddy's visual elements.

It must not redefine the product as:

- a state tracker
- a text Buddy
- a status-line companion

## 3. Identity Inputs

BuddyHub may use only verified identity inputs tied to the current user Buddy.

Currently validated real inputs include:

- `name`
- `species`

Unvalidated fields must remain unavailable until a real runtime source is proven.

These fields are known from research but are not yet treated as verified runtime inputs by default:

- `rarity`
- `shiny`
- `hat`
- `eye`
- `stats`

## 4. Visual Targets

BuddyHub targets the official native Buddy rendered by Claude Code in the bottom-right UI.

The visual source of truth is the Claude Code executable for the current installed version.

On the current macOS machine, the validated example target file is:

- `/Users/tvwoo/.local/share/claude/versions/2.1.92`

This path is implementation-specific, not a guaranteed cross-platform contract.

## 5. Native Visual Slots

Current research and local binary inspection indicate the official Buddy visual system includes:

- per-species frame tables
- hat/accessory mappings
- eye-injected frame rendering

Local binary symbols already found include:

- `YS7`
- `yj5`
- `zo_()`

These are treated as native visual slots, not public APIs.

## 6. Allowed Visual Modifications

V1 may modify:

- hat or top-row accessory elements
- species frame details
- eye-dependent visual details
- other small visual embellishments that remain attached to the user's real Buddy

V1 must not:

- create a second Buddy body
- replace the user's Buddy with a fabricated generic pet
- introduce a separate visual surface and claim success

## 7. Patch Rules

Any visual modification must obey all of the following:

1. Patch only a version-matched target.
2. Patch only a known pattern.
3. Fail if the expected match count is wrong.
4. Modify the smallest possible byte range.
5. Re-sign or otherwise restore runnability when required by platform rules.

## 8. Verification Rules

A visual patch counts as validated only when:

1. the target binary is still runnable
2. Claude Code starts successfully
3. the bottom-right official Buddy visibly changes
4. the change occurs on the official Buddy, not a parallel UI

Text inspection alone is not enough.

## 9. Failure Behavior

If any of the following occur:

- version mismatch
- pattern mismatch
- signature failure
- launch failure
- no visible official Buddy change

BuddyHub must treat the patch as failed and stop.

## 10. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub identifies a real official Buddy target.
2. BuddyHub patches only native visual elements.
3. BuddyHub preserves the user's Buddy identity.
4. BuddyHub does not depend on runtime state logic.
5. A patched binary copy shows a visible change on the official Buddy.

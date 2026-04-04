# Buddy Visual Customization Model Spec

- Status: Draft v0.3
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum visual customization model for BuddyHub.

This spec covers:

- official Buddy identity inputs
- additive visual element slots
- color preset rules
- nickname rules
- patchable visual slots
- version-sensitive patch rules

This spec does not cover:

- Claude runtime state
- reaction/state machines
- hook mappings
- text Buddy rendering

## 2. Core Rule

BuddyHub V1 must customize only the official Buddy's visual presentation.

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

## 4. Customization Inputs

BuddyHub V1 must support these user-facing customization inputs:

- `element_id`
- `color_id`
- `nickname`

`nickname` is an optional additive field.

It must not replace the verified real Buddy `name`.

## 5. Native Visual Targets

BuddyHub targets the official native Buddy rendered by Claude Code in the bottom-right UI.

The visual source of truth is the Claude Code executable for the current installed version.

On the current macOS machine, the validated example target file is:

- `/Users/tvwoo/.local/share/claude/versions/2.1.92`

This path is implementation-specific, not a guaranteed cross-platform contract.

## 6. Native Visual Slots

Current research and local binary inspection indicate the official Buddy visual system includes:

- per-species frame tables
- hat/accessory mappings
- eye-injected frame rendering
- additional render-time color usage

Local binary symbols already found include:

- `YS7`
- `yj5`
- `zo_()`

These are treated as native visual slots, not public APIs.

## 7. Additive Element Model

V1 should prefer additive elements over species-specific body replacement.

The base element slot model is:

- `top`
- `face`
- `side`
- `label`

Each element must declare:

- slot
- anchor behavior
- expected overlap
- supported species scope
- whether it can be tinted by color presets

## 8. Initial Element Catalog

V1 should define a first-party element catalog that can expand over time.

The initial catalog should be built from these product examples:

- hats
- coffee
- keyboard

Additional examples may include:

- halo
- glasses
- book

Each element must be designed so that:

1. it reads as an addition to the user's existing Buddy
2. it does not hide the Buddy's identity
3. it fits reasonably across supported species

## 9. Color Preset Model

BuddyHub V1 should expose a discrete preset list, not arbitrary freeform color entry.

The initial preset list is:

- orange
- pink
- blue
- green
- red
- black
- purple

A preset may be offered only when the current patch target has a validated color slot for it.

## 10. Nickname Model

Nickname behavior must follow all of the following:

1. The real Buddy `name` remains the source-of-truth identity.
2. `nickname` is a user-defined additive display value.
3. If no verified native label patch point exists on the current version, nickname display must be unavailable or experimental.
4. BuddyHub must not claim the nickname is active on the official Buddy unless the native display patch is verified.

## 11. Patch Rules

Any visual customization patch must obey all of the following:

1. Patch only a version-matched target.
2. Patch only a known pattern.
3. Fail if the expected match count is wrong.
4. Modify the smallest possible byte range.
5. Re-sign or otherwise restore runnability when required by platform rules.
6. Avoid replacing the underlying Buddy identity body when an additive slot is sufficient.

## 12. Validation Rules

A customization feature counts as validated only when:

1. the target binary is still runnable
2. Claude Code starts successfully
3. the bottom-right official Buddy visibly reflects the intended additive change
4. the change occurs on the official Buddy, not a parallel UI

Text inspection alone is not enough.

## 13. Failure Behavior

If any of the following occur:

- version mismatch
- pattern mismatch
- signature failure
- launch failure
- no visible official Buddy change
- nickname/color slot not actually proven

BuddyHub must treat the patch as failed or unavailable and stop.

## 14. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub identifies a real official Buddy target.
2. BuddyHub supports additive visual customization inputs.
3. BuddyHub preserves the user's Buddy identity.
4. BuddyHub does not depend on runtime state logic.
5. At least one additive element profile is verified on the official Buddy.
6. Color presets are gated by real validated patch points.
7. Nickname display is either verified or explicitly unavailable.

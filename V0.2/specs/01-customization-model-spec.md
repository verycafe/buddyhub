# BuddyHub V0.2 Customization Model Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define the active user-facing customization model for BuddyHub V0.2.

## 2. Current User-Editable Fields

BuddyHub V0.2 publicly exposes only:

- `language_id`
- `color_id`
- `nickname`

## 3. Hidden Fields

The settings model may still carry `element_id`, but V0.2 does not expose element switching in the public menu.

Rules:

- if the installed Buddy already has an element, BuddyHub preserves it
- if the installed Buddy has no element, BuddyHub must keep it as `none`
- BuddyHub must not silently inject a default element such as `tophat`

## 4. Identity Sources

Current source-of-truth inputs are:

- Buddy identity from transcript inspection
- displayed name from Claude runtime config
- current visual state from installed Claude binary inspection

## 5. Color Rules

Current verified public presets are:

- `green`
- `orange`
- `blue`
- `pink`
- `purple`
- `red`
- `black`

Current unavailable preset:

- `white`

If a color is unavailable on the current target, the menu must show that explicitly and block selection.

## 6. Nickname Rules

- nickname is an additive display override
- nickname must stay synchronized between the bottom-right Buddy and the `/buddy` card
- nickname must be reversible on restore
- nickname input must ignore control characters and empty whitespace-only values

## 7. Language Rules

Supported language IDs:

- `zh_cn`
- `en`
- `ja`
- `ko`
- `de`
- `fr`
- `ru`

The first clean launch should prefer system language detection when no saved setting exists.

## 8. Acceptance

This spec is satisfied when:

1. saved settings sanitize invalid values
2. hidden element state is preserved without silent fallback
3. nickname and color act as the only public Buddy customization fields in this phase

# BuddyHub V0.2 TUI Menu And Preview Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define the current standalone TUI interaction contract.

## 2. Top-Level Menu

The active top-level menu is:

- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Uninstall`
- `Quit`

The left side should show menu structure only.

It should not duplicate current user values that are already visible in the preview area.

## 3. Input Rules

- `Up/Down` moves selection
- `Enter` enters a submenu or executes the selected action
- `Esc` returns from submenu or input screens
- `q` may also return or exit where appropriate

## 4. Language Menu

Entering `Language` opens a second-level selection menu.

Selecting a language should switch the full TUI immediately.

## 5. Color Menu

Entering `Color` opens a second-level selection menu.

The color list should:

- show current availability
- differentiate unavailable colors
- update preview immediately while browsing

## 6. Nickname Screen

Entering `Nickname` opens a text input view.

Rules:

- the input field starts empty
- typing should update the preview immediately
- `Enter` saves the nickname draft
- `Esc` returns without forcing a save

## 7. Preview Rules

The right side should show one primary Buddy preview card, not duplicated draft cards.

The preview should feel closer to the official `/buddy` card:

- name
- species
- current preview color
- full Buddy shape
- compact supporting metadata

The preview must be based on the real installed Buddy state plus the current in-menu selection.

## 8. Result Screen

`Apply`, `Restore`, and `Uninstall` should show a result screen with:

- status
- summary
- next-step guidance

## 9. Acceptance

This spec is satisfied when:

1. menu navigation works with keyboard only
2. `Enter` and `Esc` behave predictably across submenus
3. nickname input works as a real text field
4. preview reflects the real installed Buddy instead of a fake default mascot

# BuddyHub V0.2 TUI Menu And Preview Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define the current standalone TUI interaction contract.

V0.2 当前的 UI 迁移方向是：

- Ink 作为目标公开 UI
- 现有 Python `curses` TUI 作为过渡实现和行为参考
- 在 Ink 完整覆盖公开菜单前，Python TUI 仍可作为稳定参考面

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

`DEV` 分支上的 Ink 原型必须遵守同样的菜单层级规则。

在 Ink 成为公开入口前，还必须满足：

- 不绕过 `Setup`
- 不暴露未接通的公开菜单能力
- 不在 Ink 本地重新发明一套 preview / menu contract

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
- consume canonical availability data from the bridge/core layer instead of local guesses

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

Ink UI 与 Python TUI 都必须遵守这个规则。

Ink 不得在预览卡中泄露当前隐藏范围之外的公开能力信息，例如：

- hidden element switching controls
- 与当前用户决策无关的内部帮助字段

## 8. Result Screen

`Apply`, `Restore`, and `Uninstall` should show a result screen with:

- status
- summary
- next-step guidance

当前迁移阶段允许：

- Ink 通过 JSON bridge 复用 Python 核心行为
- 但不允许 Ink 自己重新发明另一套 apply/restore 规则

## 9. Acceptance

This spec is satisfied when:

1. menu navigation works with keyboard only
2. `Enter` and `Esc` behave predictably across submenus
3. nickname input works as a real text field
4. preview reflects the real installed Buddy instead of a fake default mascot
5. Ink 原型与 Python 稳定实现在公开菜单语义上保持一致
6. Ink 不会在本地保存一个与 canonical availability model 冲突的颜色选择

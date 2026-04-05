# BuddyHub V0.2 Platform Detection And Setup Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define how BuddyHub finds Claude automatically and when it falls back to `Setup`.

## 2. Detection Order

BuddyHub should detect in this order:

1. explicit environment override
2. saved BuddyHub override path
3. `claude` launcher on `PATH`
4. standard Claude versions roots
5. `Setup` fallback

## 3. Platform Coverage

Current intended behavior:

- macOS: automatic detection should work when launcher or versions root is available
- Linux: automatic detection should try launcher and known versions roots
- Windows: automatic detection should at least try launcher resolution

If automatic detection is incomplete, BuddyHub must enter `Setup` instead of silently failing.

`DEV` 分支 Ink 迁移阶段也必须遵守这条规则：

- if `needs_setup` is true, Ink must not boot straight into the normal main menu

## 4. Setup Screen

`Setup` must let the user enter:

- Claude executable path
- Claude config path

It must also show path-finding hints:

- `which claude` on macOS/Linux
- `where claude` on Windows
- `claude doctor` as an extra reference

## 5. Reuse Rules

Saved override paths must be reused on later launches until the user changes them.

## 6. Language Default

On a clean first launch with no saved settings:

- BuddyHub should use the detected system language if supported
- generic locales such as `C` or `POSIX` must not override a real `LANG` value

## 7. Acceptance

This spec is satisfied when:

1. automatic detection is attempted before `Setup`
2. detection failure leads to a guided `Setup`
3. saved override paths are persisted and reused
4. system-language defaulting works on clean first launch
5. Ink 与 Python UI 在 `needs_setup` 判定上保持一致

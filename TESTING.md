# BuddyHub Testing Guide

- Status: Draft v0.4
- Date: 2026-04-05
- Scope: standalone TUI for official Buddy customization

## 1. Goal

This document defines the real test path for BuddyHub's current phase.

The purpose is to verify that:

- BuddyHub can read the real installed Claude Code Buddy state on the local machine
- BuddyHub falls back to a guided `Setup` screen when automatic file detection is incomplete
- BuddyHub defaults to the system language on first launch when a supported locale is available
- the standalone TUI menu can switch language, color, and nickname draft values
- the preview is based on the installed Buddy plus saved draft settings
- hidden element state is preserved exactly as installed, or stays `none` on a clean Buddy
- apply safely updates the official Buddy name and verified color customization
- restore safely returns the official Buddy to its original state

This phase does not test:

- legacy plugin settings surfaces
- plugin slash commands
- runtime Buddy state tracking

## 2. Current Validated Example

On the current macOS machine, the validated example system target is:

- `/Users/tvwoo/.local/share/claude/versions/2.1.92`

The current real Buddy data sources are:

- Buddy name: `/Users/tvwoo/.claude.json`
- Buddy identity and visual patch state: the installed Claude binary plus BuddyHub inspection logic

## 3. Entry Point

Run the standalone BuddyHub menu with:

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub
```

For non-interactive verification helpers:

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub --dump-language de
/Users/tvwoo/Projects/buddyhub/buddyhub --dump-state
```

## 4. Setup Fallback Test

When BuddyHub cannot fully detect Claude Code paths, it should enter `Setup` automatically.

Verify:

- BuddyHub starts in `Setup`
- the setup menu lets the user choose:
  - `Claude binary path`
  - `Claude config path`
  - `Retry detection`
  - `Continue`
  - `Quit`
- saving a valid binary path and config path allows BuddyHub to re-run detection
- the saved override paths are reused on the next launch

## 5. System-Language Default Test

On first launch with no saved BuddyHub settings, verify:

- supported locales such as `de_DE.UTF-8` default to `de`
- supported locales such as `zh_CN.UTF-8` default to `zh_cn`
- generic shell locales such as `C`, `C.UTF-8`, or `POSIX` do not override a real language setting from `LANG`
- after the first launch, an explicitly saved language still wins over automatic detection

## 6. Safe Test Order

The required order is:

1. inspect the currently installed Buddy state
2. launch the standalone TUI
3. verify language switching
4. verify color draft changes in preview
5. verify nickname draft changes in preview
6. apply the draft
7. restart Claude Code
8. verify the official bottom-right Buddy changed
9. verify `/buddy` matches name and color
10. restore the original state
11. verify the standalone TUI result card appears for apply and restore
12. verify `Uninstall` restores, removes old plugin traces, and exits automatically

## 7. Installed-State Detection Test

Before interacting with the menu, verify BuddyHub can read the real installed Buddy:

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub --dump-state
```

Verify:

- `current_visual.name` matches the current Buddy name
- `current_visual.species` matches the current Buddy species
- `current_visual.element_id` reflects the installed additive element, or `null` when the Buddy has no added element
- `current_visual.color_id` reflects the installed verified color
- `draft_visual` starts from the installed state and only adds saved draft changes
- if the Buddy has no installed element, `draft_visual.element_id` stays `null` and does not silently fall back to `tophat`

## 8. Language Menu Test

Launch the TUI and enter the `Language` menu.

Verify:

- the top-level menu contains:
  - `Language`
  - `Color`
  - `Nickname`
  - `Apply`
  - `Restore`
  - `Uninstall`
  - `Quit`
- selecting a language immediately changes the menu labels
- the preview section titles also switch language

Validated language IDs:

- `zh_cn`
- `en`
- `ja`
- `zh_hans`
- `de`
- `fr`
- `ru`

## 9. Color Menu Test

Enter the `Color` menu.

Verify:

- the menu shows a default entry plus the verified color presets
- each color row has a visible color marker or colored line treatment
- the current saved color is tagged as current
- unavailable colors are visibly marked as unavailable

Current expected verified colors:

- `green`
- `orange`
- `blue`
- `pink`
- `purple`
- `red`
- `black`

Current expected unavailable color:

- `white`

When a verified color is selected, verify:

- the draft preview updates immediately
- the draft state reflects the chosen color
- `Apply` can use the chosen color

When `white` is selected, verify:

- BuddyHub blocks the selection
- the saved color does not change silently
- the status message clearly indicates that the color is unavailable

## 10. Nickname Test

Enter the `Nickname` screen.

Verify:

- typing updates the input buffer
- pressing `Enter` saves the nickname into the draft
- the draft preview name updates immediately
- the installed preview remains unchanged until apply
- clearing the nickname returns the draft preview to the installed Buddy name

## 11. Apply Test

After selecting a verified color or nickname:

1. choose `Apply`
2. fully quit Claude Code
3. reopen Claude Code

Verify:

- the standalone TUI shows an apply result card immediately
- the apply result card summarizes the changed visible Buddy properties, such as display name and color
- the official bottom-right Buddy changed
- the displayed Buddy name matches the saved nickname, if set
- the Buddy color matches the saved verified preset
- the `/buddy` companion card shows the same name and color source after restart

## 12. Restore Test

From the standalone TUI, choose `Restore`.

Then:

1. fully quit Claude Code
2. reopen Claude Code

Verify:

- the standalone TUI shows a restore result card immediately
- the restore result card summarizes the reverted visible Buddy properties, such as display name and color
- the original Buddy name is restored
- the original Buddy color is restored
- the original binary patch state is restored
- the `/buddy` companion card returns to the original name/color source as well

## 13. Uninstall Test

From the standalone TUI, choose `Uninstall`.

Verify:

- BuddyHub restores the official Buddy first when a patch is present
- old Claude plugin traces under `~/.claude/plugins/.../buddyhub*` are removed automatically
- the standalone BuddyHub data root is removed automatically
- BuddyHub exits on its own without asking the user to run a separate uninstall command
- if BuddyHub was installed through a package manager, the background uninstall job is scheduled automatically

## 14. Failure Tests

### 14.1 Unsupported color

Verify:

- selecting `white` does not silently become active
- BuddyHub reports the color as unavailable

### 14.2 Apply on already-matching state

Verify:

- if the current installed Buddy already matches the saved draft, apply succeeds cleanly
- BuddyHub does not require a stale local patch record to recognize the installed state

### 12.3 Restore when nothing is patched

Verify:

- BuddyHub fails safely or reports a clean no-op
- no unrelated files are modified

### 12.4 Nickname restore

Verify:

- restore returns the displayed name to the value stored in `/Users/tvwoo/.claude.json` before customization

## 12. Current Out Of Scope

Do not treat these as blockers for this phase:

- element switching in the standalone menu
- adding a default element when none is installed
- runtime state tracking
- status line

## 13. Acceptance Criteria

This phase is complete when:

1. the standalone TUI reads the real installed Buddy state
2. language switching changes the full menu and preview labels
3. color and nickname draft changes update the preview immediately
4. apply changes the official Buddy after Claude Code restart
5. restore returns the official Buddy to its original state
6. unsupported colors fail safely

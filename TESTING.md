# BuddyHub Testing Guide

- Status: Draft v0.3
- Date: 2026-04-05
- Scope: official Buddy visual-element enhancement only

## 1. Goal

This document defines the real test path for BuddyHub's current phase.

The purpose is to verify that:

- BuddyHub can identify the installed Claude Code binary
- BuddyHub can load the saved customization settings
- BuddyHub can back up that binary safely
- BuddyHub can patch a native Buddy visual element
- BuddyHub can auto-apply the saved customization on `SessionStart`
- the official bottom-right Buddy visibly changes
- the original binary can be restored safely

This phase does not test:

- runtime state tracking
- status line
- text Buddy views

## 2. Current Validated Example

On the current macOS machine, the validated example system target is:

- `/Users/tvwoo/.local/share/claude/versions/2.1.92`

Current research has already proven that changing the native visual table in a workspace copy of this binary changes the official Buddy render.

## 3. Prerequisites

Before running the first system-level test pass, confirm:

1. Claude Code is installed locally.
2. Claude Code starts successfully before any BuddyHub patching.
3. The current repo is available at [/Users/tvwoo/Projects/buddyhub](/Users/tvwoo/Projects/buddyhub).
4. A safe backup path is available.

## 4. Safe Test Order

The required order is:

1. inspect target binary and current Buddy identity
2. review current settings and preview behavior
3. copy target into the workspace or `/tmp` for rehearsal
4. patch the rehearsal target
5. re-sign if required
6. launch the patched target and verify the official Buddy changes
7. only after that, patch the system install
8. verify restart guidance
9. verify restore flow

## 5. Settings Test

### 5.1 Settings inspection

Verify:

- `/buddyhub:settings` shows the current selected element, color, and nickname
- unsupported settings are marked unavailable or blocked
- preview is presented as advisory, not as live-applied output

### 5.2 Settings mutation

Verify:

- selecting a supported element is saved
- switching from one supported element to another reuses the clean backup and does not require a manual restore step in between
- selecting verified `green`, `orange`, `blue`, `pink`, `purple`, `red`, or `black` is saved and can be applied
- selecting `white` is saved but remains pending
- setting a nickname is saved and can be applied through `~/.claude.json` on the current validated macOS target
- `/buddyhub:settings --reset` returns to the default supported configuration

## 6. Rehearsal Test

### 6.1 Binary copy

Create a workspace copy of the installed Claude Code binary.

Verify:

- the copy matches the system binary before patching

### 6.2 Patch apply

Apply a minimal visual patch to the workspace copy only.

Verify:

- the expected native pattern is found
- the patch changes the copy hash
- the binary remains runnable after re-signing if required

### 6.3 Official Buddy verification

Launch the patched workspace copy.

Verify:

- the bottom-right official Buddy visibly changes
- the change is on the official Buddy itself, not a parallel UI

## 7. SessionStart Auto-Apply Test

Verify:

- a `SessionStart` hook can auto-apply the saved supported customization
- the hook emits restart guidance
- the hook auto-applies supported element and `orange` settings
- the hook leaves unsupported color settings pending
- already-patched targets are detected cleanly and not patched again
- the same saved nickname/color source remains consistent between the bottom-right Buddy and the `/buddy` companion card after restart

## 8. System Install Test

Only after rehearsal succeeds, test the real installed Claude Code binary.

### 8.1 Backup

Verify:

- the original system binary is backed up first

### 8.2 Patch

Verify:

- the patch is applied only to the intended version
- BuddyHub refuses to patch if the match pattern is wrong
- BuddyHub uses the saved supported settings, not hardcoded assumptions
- BuddyHub can switch between supported elements on the same target by restoring from the clean backup before re-applying

### 8.3 Launch

Verify:

- Claude Code launches
- the official Buddy visually changes as expected
- the `/buddy` companion card shows the same verified displayed name and color source
- the user is told to restart Claude Code after apply

### 8.4 Restore

Verify:

- the original system binary is restored successfully
- Claude Code returns to its original Buddy visuals
- the `/buddy` companion card returns to the original name/color source as well

## 9. Failure Tests

### 9.1 Version mismatch

Verify:

- BuddyHub refuses to patch unsupported versions

### 9.2 Pattern mismatch

Verify:

- BuddyHub refuses to patch if the expected native match count is wrong

### 9.3 Signature failure

Verify:

- BuddyHub reports failure clearly
- the user still has a valid restore path

### 9.4 Unsupported setting

Verify:

- unverified color selections remain pending and do not silently become active
- nickname restore returns the displayed name to the original Claude config value
- BuddyHub does not silently claim unsupported settings are active
- BuddyHub does not let the bottom-right Buddy and the `/buddy` companion card drift onto different nickname/color sources

### 9.5 Launch failure

Verify:

- BuddyHub can restore the original binary
- Claude Code becomes usable again after restore

## 10. Current Out Of Scope

Do not treat these as blockers for this phase:

- runtime Buddy state
- `thinking / coding / running`
- status line
- text command polish

## 11. Acceptance Criteria

This phase is complete when:

1. a native visual element change is validated on the official Buddy
2. saved settings drive apply behavior
3. `SessionStart` can auto-apply a supported customization
4. the system binary can be backed up and restored safely
5. unsupported versions and unsupported settings fail safely
6. BuddyHub does not rely on a parallel Buddy UI

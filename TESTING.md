# BuddyHub Testing Guide

- Status: Draft v0.2
- Date: 2026-04-05
- Scope: official Buddy visual-element enhancement only

## 1. Goal

This document defines the real test path for BuddyHub's current phase.

The purpose is to verify that:

- BuddyHub can identify the installed Claude Code binary
- BuddyHub can back up that binary safely
- BuddyHub can patch a native Buddy visual element
- the official bottom-right Buddy visibly changes
- the original binary can be restored safely

This phase does not test:

- runtime state tracking
- hooks
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

1. detect target binary
2. copy target into the workspace for rehearsal
3. patch the workspace copy
4. re-sign if required
5. launch the patched copy and verify the official Buddy changes
6. only after that, consider patching the system install
7. verify restore flow

## 5. Rehearsal Test

### 5.1 Binary copy

Create a workspace copy of the installed Claude Code binary.

Verify:

- the copy matches the system binary before patching

### 5.2 Patch apply

Apply a minimal visual patch to the workspace copy only.

Verify:

- the expected native pattern is found
- the patch changes the copy hash
- the binary remains runnable after re-signing if required

### 5.3 Official Buddy verification

Launch the patched workspace copy.

Verify:

- the bottom-right official Buddy visibly changes
- the change is on the official Buddy itself, not a parallel UI

## 6. System Install Test

Only after rehearsal succeeds, test the real installed Claude Code binary.

### 6.1 Backup

Verify:

- the original system binary is backed up first

### 6.2 Patch

Verify:

- the patch is applied only to the intended version
- BuddyHub refuses to patch if the match pattern is wrong

### 6.3 Launch

Verify:

- Claude Code launches
- the official Buddy visually changes as expected

### 6.4 Restore

Verify:

- the original system binary is restored successfully
- Claude Code returns to its original Buddy visuals

## 7. Failure Tests

### 7.1 Version mismatch

Verify:

- BuddyHub refuses to patch unsupported versions

### 7.2 Pattern mismatch

Verify:

- BuddyHub refuses to patch if the expected native match count is wrong

### 7.3 Signature failure

Verify:

- BuddyHub reports failure clearly
- the user still has a valid restore path

### 7.4 Launch failure

Verify:

- BuddyHub can restore the original binary
- Claude Code becomes usable again after restore

## 8. Current Out Of Scope

Do not treat these as blockers for this phase:

- runtime Buddy state
- `thinking / coding / running`
- hooks
- status line
- text command polish

## 9. Acceptance Criteria

This phase is complete when:

1. a native visual element change is validated on the official Buddy
2. the system binary can be backed up and restored safely
3. unsupported versions fail safely
4. BuddyHub does not rely on a parallel Buddy UI

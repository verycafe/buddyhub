# Buddy Command Surface Spec

- Status: Draft v0.5
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum command surface that supports official Buddy visual customization.

Commands are supporting tools.

They exist to:

- open customization settings
- inspect the current install
- back up and patch the native Buddy target
- restore the original file
- diagnose failures

## 2. Command Design Principles

Commands must be:

- explicit
- low-risk
- reversible where applicable
- honest about platform and version limits

Commands must not:

- pretend a text command itself is the product
- imply Buddy enhancement succeeded before the official Buddy visibly changes

## 3. Required Commands

BuddyHub V1 should include at least these user-facing capabilities:

- help
- settings
- inspect
- apply
- restore
- doctor
- uninstall

The exact invocation layer may evolve, but these functions are the required command surface.

## 4. Required Command Behavior

### 4.1 Help

Must explain:

- that BuddyHub targets the official bottom-right Buddy
- that the current phase is visual customization only
- that runtime states are out of scope for this phase
- which operations are safe to run

### 4.2 Settings

Must let the user:

- choose an element
- choose a color preset
- set or clear a nickname
- access preview behavior
- apply or restore

If a setting is unsupported on the current target, settings must say so explicitly.

In the current validated public plugin surface, `settings` is expected to behave as a guided flow rather than a guaranteed native dropdown dialog.

That guided flow must:

- inspect the current saved configuration first
- present explicit element and color choices
- save the selected values through BuddyHub commands
- show an honest preview after each change
- state explicitly when nickname is supported through Claude runtime config and when color remains unavailable

### 4.3 Inspect

Must show:

- detected platform
- detected Claude version
- detected target path
- current verified Buddy identity when available
- whether the requested customization is supported on the current target

### 4.4 Apply

Must:

- create or confirm backup
- apply the current selected native visual customization
- apply the saved nickname override only when the Claude runtime config path is verified
- perform verification
- report success only if the target patch was actually written
- tell the user to restart Claude Code

### 4.5 Restore

Must:

- restore the original binary from backup
- restore the original displayed Buddy name from config backup when nickname override was applied
- verify the restored target is usable

### 4.6 Doctor

Must help diagnose:

- unsupported version
- path mismatch
- signature issues
- failed patch application
- failed launch verification
- unsupported element, color, or nickname slots

### 4.7 Uninstall

Must:

- clean BuddyHub-owned tooling or metadata
- guide or perform restore if BuddyHub has patched the user's install

## 5. Explicit Non-Goals

This phase does not require command support for:

- runtime state reporting
- status line toggles
- hook-driven Buddy activity
- text Buddy rendering

## 6. Acceptance Criteria

This spec is satisfied when:

1. The user can open a customization settings flow.
2. The user can inspect whether their Claude install is patchable.
3. The user can apply the selected customization through a clear command path.
4. The user is clearly told to restart Claude Code after apply.
5. The user can restore the original install through a clear command path.
6. Commands never substitute for real official Buddy enhancement.

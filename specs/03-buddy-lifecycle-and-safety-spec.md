# Buddy Lifecycle and Safety Spec

- Status: Draft v0.1
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define how BuddyHub is installed, enabled, paused, resumed, disabled, and uninstalled, with strict safety guarantees.

This is a hard-requirement spec.

## 2. Core Rule

BuddyHub must never compromise the user's ability to use Claude Code normally.

If BuddyHub fails, Claude Code must continue to function.

## 3. Lifecycle Operations

V1 must support the following user-visible lifecycle operations:

1. install
2. enable
3. pause
4. resume
5. disable
6. uninstall
7. diagnose

## 4. Install Spec

### 4.1 Requirements

Installation must:

- use the official Claude Code plugin distribution path
- produce a predictable post-install state
- not require manual file copying

### 4.2 Post-install outcome

After install, the user must be able to determine:

- whether BuddyHub is active
- whether the text UI is available
- how to pause or disable it
- how to uninstall it

### 4.3 Ownership manifest

Installation must create or maintain a BuddyHub-owned ownership record.

This record must be sufficient to answer:

- which config fragments BuddyHub added
- which files BuddyHub created
- which runtime assets BuddyHub owns
- which cleanup actions are safe during uninstall

The ownership record must be namespaced and machine-readable.

## 5. Enable and Resume Spec

Enable or resume must:

- allow Buddy updates again
- permit status line sync if configured
- permit text UI commands immediately

Enable and resume must not:

- require reinstall
- overwrite unrelated Claude settings

## 6. Pause and Disable Spec

Pause or disable must:

- stop automatic Buddy activity
- stop Buddy-driven updates if requested
- preserve Claude Code normal behavior

Pause or disable must not:

- corrupt BuddyHub installation
- delete user data unexpectedly
- break unrelated hooks or status line behavior

Pause and disable should be distinguishable:

- `pause` is reversible runtime suspension
- `disable` is explicit user shutdown of BuddyHub behavior

## 7. Uninstall Spec

### 7.1 Product requirement

BuddyHub must provide a safe uninstall path that is understandable to users and low-risk to execute.

### 7.2 Uninstall effects

Uninstall must:

- stop BuddyHub runtime processes
- remove BuddyHub-owned active integration points where applicable
- clean BuddyHub cache and temporary state
- preserve the user's unrelated Claude configuration

### 7.2.1 Single-entry uninstall requirement

V1 must provide one clear user-facing uninstall entrypoint.

This entrypoint may:

- execute the full uninstall directly, or
- run BuddyHub cleanup and then guide the final platform removal step in a single explicit flow

But it must not require the user to manually discover internal files first.

### 7.3 Cleanup boundary

BuddyHub must clearly distinguish:

- removable caches
- removable generated state
- user-retained data, if any

### 7.3.1 Configuration rollback

BuddyHub must be able to roll back only the configuration it owns.

This requires:

- ownership-aware insertion of hooks or status-line references
- sufficient metadata to remove BuddyHub fragments without deleting unrelated user config
- a safe merge or patch strategy instead of whole-file overwrite whenever possible

### 7.3.2 Snapshot or patch history

If BuddyHub edits shared config files, V1 must preserve enough rollback information to restore the pre-BuddyHub state of BuddyHub-owned sections.

Acceptable approaches include:

- config fragment ownership records
- patch descriptors
- targeted reversible edits

Blind destructive overwrite is not acceptable.

### 7.4 Recovery safety

If uninstall cleanup partially fails:

- Claude Code must remain usable
- BuddyHub must not leave the system in a blocked state

## 8. Hook Safety Spec

### 8.1 Timing

Hook handlers must be lightweight.

They must:

- exit quickly
- avoid expensive synchronous work
- avoid high-latency network work in V1

### 8.2 Failure mode

If a BuddyHub hook errors:

- it must fail open where possible
- it must not permanently block Claude workflow
- it must not trap the user in repeated prompts or loops

## 9. Text UI Safety Spec

The BuddyHub UI must be treated as optional text furniture, not a dependency of Claude Code.

Requirements:

- if status line integration is missing, Claude Code still works
- if a BuddyHub text command fails, Claude Code still works
- if optional legacy runtime leftovers exist, they must not be required for V1

## 10. Configuration Safety Spec

BuddyHub-owned settings and references must be:

- namespaced
- discoverable
- reversible
- removable
- attributable to BuddyHub ownership metadata

BuddyHub must avoid:

- overwriting unrelated user customizations
- assuming ownership of the full hooks config
- assuming ownership of the full status line config without a safe merge strategy

## 11. Data Safety Spec

BuddyHub must document:

- what files it writes
- where they live
- which ones are safe to delete
- which ones are required to preserve user state

BuddyHub must also distinguish:

- BuddyHub-owned runtime data
- Claude-owned Buddy identity or transcript data that BuddyHub only reads

BuddyHub must not delete or mutate Claude-owned Buddy identity sources during normal operation or uninstall.

V1 must not hide essential uninstall knowledge in source code only.

## 12. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub can be installed without manual file copying.
2. BuddyHub can be paused or disabled without uninstall.
3. BuddyHub can be resumed without reinstall.
4. BuddyHub has a clearly documented safe uninstall path.
5. Hook or BuddyHub UI failure does not make Claude Code unusable.
6. BuddyHub does not overwrite unrelated Claude Code settings as a normal operation.
7. BuddyHub records enough ownership metadata to safely remove only its own integration points.

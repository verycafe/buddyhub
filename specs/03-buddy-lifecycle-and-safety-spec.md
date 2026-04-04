# Buddy Lifecycle and Safety Spec

- Status: Draft v0.2
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define how BuddyHub safely detects, backs up, patches, verifies, restores, and removes native Buddy visual enhancements.

This is a hard-requirement spec.

## 2. Core Rule

BuddyHub must never compromise the user's ability to launch or use Claude Code normally.

If patching fails, BuddyHub must fail safe.

## 3. Lifecycle Operations

V1 must support these user-visible operations:

1. detect
2. backup
3. patch
4. verify
5. restore
6. uninstall
7. diagnose

## 4. Detect Spec

BuddyHub must determine:

- platform
- install type when possible
- target Claude Code version
- target binary path
- whether the current version matches a supported patch profile

If any of these are unknown, BuddyHub must stop before patching.

## 5. Backup Spec

Before modifying any system Claude binary, BuddyHub must create a backup of the original target file.

The backup record must be sufficient to answer:

- which file was backed up
- which version it belonged to
- when the backup was created
- how restore should find it

Patching without backup is not acceptable.

## 6. Patch Spec

Patch apply must:

- use a version-specific pattern
- use a minimal replacement
- fail if the expected match count is wrong
- avoid unrelated binary changes

Patch apply must not:

- blindly overwrite unmatched files
- assume all systems share one path
- assume one patch fits all Claude Code versions

## 7. Verification Spec

After patching, BuddyHub must verify:

- the binary is still runnable
- signature handling is complete for the current platform if needed
- Claude Code can launch
- the official bottom-right Buddy visibly reflects the expected visual element change

If any verification step fails, BuddyHub must recommend or perform restore.

## 8. Restore Spec

Restore must:

- replace the patched binary with the saved original
- preserve user data outside the patched target
- leave Claude Code in a launchable state

Restore must not require the user to manually discover internal files first.

## 9. Uninstall Spec

Uninstall for this phase means:

- remove BuddyHub-owned tooling or metadata
- restore the original Claude binary if BuddyHub had patched it
- leave unrelated Claude settings and user data untouched

## 10. Safety Constraints

BuddyHub must:

- avoid modifying `~/.claude/pet` as if it were the official Buddy control path
- avoid assuming `~/.local/share/claude/versions/...` is universal across all platforms
- avoid treating internal implementation details as public API contracts
- stop when pattern detection is ambiguous

## 11. Cross-Platform Rule

Path and patch logic must be treated as platform- and install-specific.

V1 may validate one platform first, but it must not document that path as universally stable.

## 12. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub can safely identify whether a target install is patchable.
2. BuddyHub never patches without backup.
3. BuddyHub can apply a minimal native visual patch.
4. BuddyHub can verify that the official Buddy changed.
5. BuddyHub can restore the original binary safely.
6. Failure paths leave Claude Code usable.

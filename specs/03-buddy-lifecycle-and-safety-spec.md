# Buddy Lifecycle and Safety Spec

- Status: Draft v0.3
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define how BuddyHub safely auto-applies, backs up, patches, verifies, restores, and removes native Buddy visual customizations.

This is a hard-requirement spec.

## 2. Core Rule

BuddyHub must never compromise the user's ability to launch or use Claude Code normally.

If patching fails, BuddyHub must fail safe.

## 3. Lifecycle Operations

V1 must support these user-visible operations:

1. detect
2. load settings
3. backup
4. patch
5. verify
6. prompt restart
7. restore
8. uninstall
9. diagnose

## 4. Install and Upgrade Behavior

On install or upgrade, BuddyHub should:

1. detect the supported Claude Code target
2. load the user's saved customization
3. auto-apply that customization when the target is supported
4. clearly tell the user that Claude Code must be restarted

If the target is unsupported or no safe patch profile exists, BuddyHub must stop and explain why.

## 5. Detect Spec

BuddyHub must determine:

- platform
- install type when possible
- target Claude Code version
- target binary path
- whether the current version matches a supported patch profile
- whether requested customization slots are actually supported on the current target

If any required part is unknown, BuddyHub must stop before patching.

## 6. Settings Load Spec

Before patching, BuddyHub must load the current user choices for:

- element
- color preset
- nickname

Unsupported settings must not be silently forced into the patch.

## 7. Backup Spec

Before modifying any system Claude binary, BuddyHub must create or confirm a backup of the original target file.

Before modifying the displayed Buddy name through Claude runtime config, BuddyHub must create or confirm a backup of that config file.

The backup record must be sufficient to answer:

- which file was backed up
- which version it belonged to
- when the backup was created
- how restore should find it

Patching without backup is not acceptable.

## 8. Patch Spec

Patch apply must:

- use a version-specific pattern
- use a minimal replacement
- fail if the expected match count is wrong
- avoid unrelated binary changes
- apply only the supported subset of user settings
- keep the bottom-right Buddy and the `/buddy` companion card aligned when a setting shares one native source

Patch apply must not:

- blindly overwrite unmatched files
- assume all systems share one path
- assume one patch fits all Claude Code versions
- claim unsupported nickname or color settings are active

## 9. Verification Spec

After patching, BuddyHub must verify:

- the binary is still runnable
- signature handling is complete for the current platform if needed
- Claude Code can launch
- the expected patch bytes are present

If any verification step fails, BuddyHub must recommend or perform restore.

If visual confirmation still depends on a restart, BuddyHub must say so explicitly.

## 10. Restart Prompt Spec

After a successful apply, BuddyHub must tell the user:

- the target file was patched
- the running Claude Code process will not necessarily reflect the change yet
- Claude Code must be restarted to see the official Buddy update

This guidance must be treated as required product behavior, not an optional note.

## 11. Restore Spec

Restore must:

- replace the patched binary with the saved original
- restore the saved Claude runtime config if BuddyHub changed the displayed Buddy name
- preserve user data outside the patched target
- leave Claude Code in a launchable state
- restore both the bottom-right Buddy and the `/buddy` companion card to the original name/color source when those sources were modified

Restore must not require the user to manually discover internal files first.

## 12. Uninstall Spec

Uninstall for this phase means:

- remove BuddyHub-owned tooling or metadata
- restore the original Claude binary if BuddyHub had patched it
- leave unrelated Claude settings and user data untouched

## 13. Safety Constraints

BuddyHub must:

- avoid modifying `~/.claude/pet` as if it were the official Buddy control path
- avoid assuming `~/.local/share/claude/versions/...` is universal across all platforms
- avoid treating internal implementation details as public API contracts
- stop when pattern detection is ambiguous
- avoid exposing unverified features as if they were production-ready

## 14. Cross-Platform Rule

Path and patch logic must be treated as platform- and install-specific.

V1 may validate one platform first, but it must not document that path as universally stable.

## 15. Acceptance Criteria

This spec is satisfied when:

1. BuddyHub can safely identify whether a target install is patchable.
2. BuddyHub auto-applies the saved customization when the target is supported.
3. BuddyHub never patches without backup.
4. BuddyHub can apply a minimal native visual patch.
5. BuddyHub can verify that the patch landed in the target.
6. BuddyHub clearly prompts for restart after apply.
7. BuddyHub can restore the original binary safely.
8. BuddyHub can restore the original displayed Buddy name safely when nickname override was applied.
9. Failure paths leave Claude Code usable.

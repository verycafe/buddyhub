# BuddyHub V0.2 Apply Restore And Uninstall Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define the safe mutation lifecycle for BuddyHub V0.2.

## 2. Apply

`Apply` must:

- load the current saved settings
- resolve the active Claude target
- create or recover a clean backup
- apply the verified visual patch
- apply nickname override when supported
- verify the target remains runnable
- tell the user to restart Claude Code

## 3. Restore

`Restore` must:

- restore the original Claude binary from backup
- restore the original displayed name when BuddyHub changed it
- clear BuddyHub patch-state records
- leave Claude Code runnable

## 4. Uninstall

`Uninstall` must:

- trigger restore first if needed
- remove BuddyHub-owned data
- remove old Claude plugin traces
- schedule package-manager uninstall automatically

The user should not need a second manual uninstall command.

## 5. Failure Rules

If a target already contains a visual patch and BuddyHub cannot find a clean backup, BuddyHub must fail loudly and explain why.

If a clean backup can be recovered automatically, BuddyHub should use it.

## 6. Acceptance

This spec is satisfied when:

1. BuddyHub never patches without a recoverable path
2. restore returns both Buddy surfaces to the original name/color source
3. uninstall is automatic from the menu

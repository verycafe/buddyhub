# Specs Folder

This folder stores implementation-facing product specs for BuddyHub.

## Current Direction

The repository is now focused on one product target:

- visual enhancement of the official Claude Code Buddy

The specs no longer treat runtime-state-driven Buddy behavior as the main product.

## Current Specs

- [01-buddy-state-spec.md](/Users/tvwoo/Projects/buddyhub/specs/01-buddy-state-spec.md): native visual-element model, identity inputs, patch rules, and visual verification
- [02-buddy-ui-spec.md](/Users/tvwoo/Projects/buddyhub/specs/02-buddy-ui-spec.md): official Buddy as the only product UI target
- [03-buddy-lifecycle-and-safety-spec.md](/Users/tvwoo/Projects/buddyhub/specs/03-buddy-lifecycle-and-safety-spec.md): detect, backup, patch, verify, restore, uninstall, and safety guarantees
- [04-command-surface-spec.md](/Users/tvwoo/Projects/buddyhub/specs/04-command-surface-spec.md): helper command functions for inspect, apply, restore, diagnose, and uninstall

## Relationship To Other Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md) defines the product goal and scope
- [research](/Users/tvwoo/Projects/buddyhub/research) stores exploratory and reference material
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md) defines the native visual enhancement test flow

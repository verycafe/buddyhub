# Specs Folder

This folder stores implementation-facing product specs for BuddyHub.

## Current Direction

The repository is now focused on one product target:

- visual customization of the official Claude Code Buddy

The current phase is not about runtime-state-driven Buddy behavior.

It is about:

- auto-applying a selected visual customization
- prompting the user to restart Claude Code
- configuring additive elements, colors, and optional nickname behavior

## Current Specs

- [01-buddy-state-spec.md](/Users/tvwoo/Projects/buddyhub/specs/01-buddy-state-spec.md): visual customization model, identity inputs, element slots, color presets, nickname rules, and validation boundaries
- [02-buddy-ui-spec.md](/Users/tvwoo/Projects/buddyhub/specs/02-buddy-ui-spec.md): official Buddy as the only product UI target plus settings and preview behavior
- [03-buddy-lifecycle-and-safety-spec.md](/Users/tvwoo/Projects/buddyhub/specs/03-buddy-lifecycle-and-safety-spec.md): auto-apply, backup, patch, verify, restart prompt, restore, uninstall, and safety guarantees
- [04-command-surface-spec.md](/Users/tvwoo/Projects/buddyhub/specs/04-command-surface-spec.md): command surface for settings, inspect, apply, restore, diagnose, and uninstall

## Relationship To Other Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md) defines the product goal and scope
- [research](/Users/tvwoo/Projects/buddyhub/research) stores exploratory and reference material
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md) defines the native visual enhancement test flow

# Specs Folder

This folder stores executable product specifications for BuddyHub.

## Purpose

These docs translate the PRD into implementation-facing specs.

Each spec should define:

- scope
- inputs
- outputs
- constraints
- failure behavior
- acceptance criteria

## Current Specs

- [01-buddy-state-spec.md](/Users/tvwoo/Projects/buddyhub/specs/01-buddy-state-spec.md): Claude state model, Buddy state model, mappings, and fallback behavior
- [02-buddy-ui-spec.md](/Users/tvwoo/Projects/buddyhub/specs/02-buddy-ui-spec.md): official native Buddy enhancement goal, plus diagnostic text/status surfaces
- [03-buddy-lifecycle-and-safety-spec.md](/Users/tvwoo/Projects/buddyhub/specs/03-buddy-lifecycle-and-safety-spec.md): install, enable, pause, resume, uninstall, cleanup, and safety guarantees
- [04-command-surface-spec.md](/Users/tvwoo/Projects/buddyhub/specs/04-command-surface-spec.md): user-facing diagnostic and lifecycle command surface

## Relationship To Other Docs

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md) defines product goals and boundaries
- [research](/Users/tvwoo/Projects/buddyhub/research) stores exploratory and reference material
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md) defines the first real-world manual test pass
- `specs/` defines what the product must do in implementable terms

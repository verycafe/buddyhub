---
description: Open BuddyHub native settings guidance
disable-model-invocation: true
---

# BuddyHub Settings

BuddyHub settings now live in Claude Code's native config menu.

## Native Menu

1. Run `/config`
2. Search for `BuddyHub`
3. Configure:
   - at most one Color toggle
   - optional Nickname
4. Run `/buddyhub:apply`
5. Restart Claude Code

## Notes

- `/buddyhub:settings` is now a fast help/menu entry and does not run a long inspection script.
- The current release exposes only Color and Nickname in the native menu.
- Element switching is hidden in this version.
- Use `/buddyhub:inspect` to see the current saved settings, native menu overrides, effective settings, and blockers.

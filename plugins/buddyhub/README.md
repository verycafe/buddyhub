# BuddyHub Plugin

BuddyHub is a reactive Buddy companion for Claude Code.

It must enhance the user's current Claude Buddy identity rather than substituting a BuddyHub-defined generic pet.

## Included Surfaces

- Hook-driven state tracking
- TUI status and detail commands
- Lifecycle controls
- Optional status line script

## Main Commands

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:open`
- `/buddyhub:uninstall`
- `/buddyhub:doctor`
- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`

## Data Location

BuddyHub writes runtime data to:

`~/.claude/plugins/data/buddyhub`

## Notes

- BuddyHub is designed to fail open: Claude Code should keep working if BuddyHub fails.
- The status line script is provided, but this version does not auto-edit Claude Code settings; use `/buddyhub:statusline-on` to get the script path and wire it up manually.
- BuddyHub V1 is TUI-first and does not require any GUI surface.
- BuddyHub must not fabricate unavailable Buddy identity fields or present a generic body as the user's Buddy.
- First-round manual verification is documented in [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md).

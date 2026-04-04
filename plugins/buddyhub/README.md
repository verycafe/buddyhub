# BuddyHub Plugin

BuddyHub is a Buddy enhancement plugin for Claude Code.

It must enhance the user's current Claude Buddy identity rather than substituting a BuddyHub-defined generic pet.

Current product status:

- identity sync is verified from Claude transcripts
- Claude-side runtime state tracking is implemented
- native control of the official bottom-right Buddy remains experimental

Important:

- the product target is the official Claude Code Buddy already rendered in the bottom-right UI
- the text commands below are diagnostic/supporting tools
- they are not the primary Buddy experience

## Included Surfaces

- Hook-driven state tracking
- Diagnostic status and detail commands
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
- `/buddyhub:pet-install`

## Data Location

BuddyHub writes runtime data to:

`~/.claude/plugins/data/buddyhub`

## Notes

- BuddyHub is designed to fail open: Claude Code should keep working if BuddyHub fails.
- The status line script is provided, but this version does not auto-edit Claude Code settings; use `/buddyhub:statusline-on` to get the script path and wire it up manually.
- The desktop pet runtime can be refreshed from the plugin package with `/buddyhub:pet-install`.
- Text output is diagnostic only and must not be mistaken for the finished Buddy product.
- BuddyHub must not fabricate unavailable Buddy identity fields or present a generic body as the user's Buddy.
- First-round manual verification is documented in [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md).

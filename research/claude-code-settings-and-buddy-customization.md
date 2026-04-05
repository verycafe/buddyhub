# Claude Code Settings And Buddy Customization Notes

- Status: Living document
- Date created: 2026-04-05
- Scope: Claude Code option/config architecture as it matters to BuddyHub, plus implementation lessons from official Buddy nickname/color/element work

## Purpose

This file records the settings and customization lessons that turned out to matter in practice while building BuddyHub.

It should help answer three recurring questions:

1. Which Claude Code configuration surfaces are real and verified for third-party plugins?
2. Which official Buddy properties can actually be customized today, and from which source-of-truth files?
3. Which product and implementation mistakes should BuddyHub avoid repeating?

## Source Quality

- `Official docs/changelog`: public Anthropic or Claude Code documentation and local cached changelog
- `Local runtime`: verified directly on this machine from real files or real Claude Code behavior
- `Reverse-engineered`: binary/string/source-map level evidence, useful but not automatically a public plugin API
- `Product lesson`: conclusion from implementation and testing work in this repository

## What Matters From Claude Code's Settings Architecture

### 1. `manifest.userConfig` is the only verified native plugin settings surface

For BuddyHub, the single most useful verified setting mechanism is plugin `manifest.userConfig`.

Why it matters:

- it shows up in Claude Code's native `/config` flow
- it supports real plugin-owned settings without inventing a parallel settings store
- it is the only native menu-like configuration surface we have actually verified for third-party plugins

Confidence: `Official` + `Local runtime`

Relevant evidence:

- [/Users/tvwoo/.claude/cache/changelog.md](/Users/tvwoo/.claude/cache/changelog.md)
- historical BuddyHub plugin manifest from the now-removed plugin prototype

### 2. Slash commands are real, but command output is not a verified native control surface

BuddyHub can ship slash commands through `commands/*.md`, but that does not mean the command body can render a first-party clickable menu.

What is verified:

- slash commands work
- command files can run scripts
- command files can render text

What is not verified:

- a third-party plugin command rendering a true built-in clickable menu or tabbed local UI inside `/buddyhub:settings`

Product implication:

- do not promise a clickable native menu inside command output unless it is proven
- do not confuse a text page or chat-guided flow with a native setting surface

Confidence: `Official` + `Local runtime` + `Product lesson`

Relevant evidence:

- the historical BuddyHub plugin command prototype used plain command files and text output
- [/Users/tvwoo/.claude/cache/changelog.md](/Users/tvwoo/.claude/cache/changelog.md)

### 2.1 Hierarchical menus for third-party plugin commands are not yet verified

The desired BuddyHub UX is:

- user enters `/buddyhub`
- Claude Code shows a first-level menu
- choosing an item opens a second-level menu such as colors

As of this research pass, BuddyHub does not have verified evidence that third-party plugins can render that style of hierarchical native menu from a plugin command.

What was verified instead:

- plugin commands are file/content-backed slash commands
- command metadata supports fields such as `description`, `argumentHint`, `allowedTools`, and related prompt metadata
- plugin `userConfig` is a verified native settings surface

What was not found in verified plugin-facing schema evidence:

- a plugin command field for nested menus
- a plugin command field for command-body click menus
- a plugin-exposed way to declare `type:"local-jsx"` for third-party commands

Product implication:

- BuddyHub must not claim `/buddyhub` can currently be turned into a first-party-feeling hierarchical menu unless that behavior is directly proven
- if a menu UX is required, an external TUI is currently the only BuddyHub path we have fully productized

Confidence: `Official` + `Local runtime` + `Reverse-engineered`

Relevant evidence:

- [/Users/tvwoo/.claude/cache/changelog.md](/Users/tvwoo/.claude/cache/changelog.md)
- [/Users/tvwoo/.local/share/claude/versions/2.1.92](/Users/tvwoo/.local/share/claude/versions/2.1.92)

### 3. Internal `local-jsx` exists, but plugin access is not proven

Claude Code clearly contains internal local UI mechanisms, including `local-jsx` behavior used by first-party features such as `/buddy`.

However, BuddyHub has not verified that third-party plugins can safely and officially attach to that same internal surface.

Product implication:

- treat `local-jsx` as a research lead, not a shipped plugin capability
- do not design product UX around undocumented internal UI hooks until proven

Confidence: `Reverse-engineered`

Relevant evidence:

- [/Users/tvwoo/.local/share/claude/versions/2.1.92](/Users/tvwoo/.local/share/claude/versions/2.1.92)
- [/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md](/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md)

### 4. Configuration precedence matters

The user-provided Claude Code architecture analysis was useful because it reinforced a pattern we repeatedly hit in practice:

- command/session overrides
- runtime environment injection
- project or plugin-level saved settings
- global Claude config

BuddyHub should keep these layers distinct instead of pretending there is only one source of truth.

Product implication:

- saved BuddyHub settings and effective BuddyHub settings are not always the same thing
- runtime overrides from native config should be visible in diagnostics
- restore logic must know which source it changed

Confidence: `Product lesson`

## Verified Source-Of-Truth Map For Official Buddy Customization

### 1. Official Buddy identity

Current real Buddy identity can be read from Claude transcript `companion_intro` entries.

What this gives today:

- real `name`
- real `species`

What it does not reliably provide today:

- a fully verified live source for all rarity/hat/eye/stat values across all surfaces

Confidence: `Local runtime`

Relevant evidence:

- [/Users/tvwoo/.claude/projects](/Users/tvwoo/.claude/projects)
- [/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md](/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md)

### 2. Official Buddy displayed name

The bottom-right Buddy label and the `/buddy` card name are driven by Claude's companion runtime config in:

- [/Users/tvwoo/.claude.json](/Users/tvwoo/.claude.json)

Verified field:

- `companion.name`

BuddyHub implementation lesson:

- nickname support is real
- nickname apply must back up `~/.claude.json`
- restore must put the original name back

Confidence: `Local runtime`

### 3. Official Buddy visual elements and color tokens

The official Buddy's native sprite/visual tables and color-token mappings live in the Claude Code binary itself:

- [/Users/tvwoo/.local/share/claude/versions/2.1.92](/Users/tvwoo/.local/share/claude/versions/2.1.92)

This means:

- official Buddy visual customization is a native patch problem
- it is not driven by a simple external sprite JSON file
- `~/.claude/pet` is not the source-of-truth for the official bottom-right Buddy

Confidence: `Local runtime` + `Reverse-engineered`

## Implementation Lessons From BuddyHub

### 1. Never replace the user's Buddy with a generic Buddy

The product target is the user's real official Buddy, not a BuddyHub-owned stand-in.

Bad path:

- invent a generic pet shape
- present a parallel text Buddy as if it were the official Buddy

Correct path:

- read the real Buddy identity
- enhance the official Buddy surfaces only

Confidence: `Product lesson`

### 2. Unsupported settings must not block supported ones

We hit a real bug where nickname support was not fully wired, and that incorrectly blocked applying a verified visual element.

Correct rule:

- if `color` or `nickname` is unsupported on the current target, mark it pending/unavailable
- do not prevent a supported element patch from applying

Confidence: `Product lesson`

### 3. Additive elements must be semantically designed, not templated

Users do not want every element to look like a square placeholder.

Bad path:

- reuse the same tiny box-like shape for hat, coffee, and other accessories

Correct path:

- each element must have its own visual logic
- placement should match its meaning
- examples:
  - hat above the head
  - coffee near the chest or hand area
  - scene props can live at the side or above, depending on composition

Confidence: `Product lesson`

### 4. Native settings UX must stay honest

We repeatedly learned that a long text settings page or chat-guided prompt is not the same thing as a native options UI.

Correct rule:

- if the UI is really an external TUI, say that directly
- do not market a text output page as a native menu
- do not promise clickable in-command controls until proven

Confidence: `Product lesson`

### 5. The bottom-right Buddy and `/buddy` card must not drift apart

When BuddyHub changes an official source such as companion name or native color token mapping, both official surfaces should stay aligned:

- bottom-right Buddy
- `/buddy` card

The apply and restore paths should treat them as one sync problem when they share one source.

Confidence: `Product lesson` + `Local runtime`

## Current Verified Capability Boundary

### Verified on the current macOS target

- detect the real official Buddy identity source
- patch official Buddy visual elements in the Claude binary
- patch a verified set of official Buddy color presets through native color-token mappings
- set and restore the displayed Buddy nickname through `~/.claude.json`
- keep bottom-right Buddy and `/buddy` card aligned when they share the same verified source

### Not yet verified or not yet productized

- arbitrary RGB/freeform color picking
- a fully verified `white` preset
- a third-party plugin command rendering a true clickable native menu in the command body
- a fully documented public plugin API for internal `local-jsx` Buddy UI
- arbitrary new Buddy schema fields beyond the currently verified sources

## Why The User-Provided Claude Code Settings Report Was Useful

The long architecture report was useful mainly in these ways:

- it reinforced that Claude Code uses layered configuration, not one flat config file
- it pointed directly at plugin settings architecture as a useful research lead, even though BuddyHub no longer ships as a Claude plugin
- it made clear that internal UI/state systems are much richer than the public plugin surface
- it supported a more disciplined distinction between:
  - public plugin capability
  - internal Claude capability
  - reverse-engineered hints

The report was less useful as a direct implementation contract because:

- reverse-engineered architecture does not automatically become a supported third-party API
- BuddyHub still needs local verification for each customization path

Confidence: `Product lesson`

## Current Product Rule For Future Work

When designing future BuddyHub customization:

1. Prefer verified native settings surfaces over improvised text flows.
2. Only expose a setting publicly when apply and restore are both proven.
3. Treat binary patch points and Claude runtime config as separate sources with separate backups.
4. Never claim a preview is native unless it is actually using a verified native surface.
5. Keep the official Buddy as the only product object.

## Related Files

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [claude-code-buddy.md](/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md)
- [specs/01-buddy-state-spec.md](/Users/tvwoo/Projects/buddyhub/specs/01-buddy-state-spec.md)
- [specs/04-command-surface-spec.md](/Users/tvwoo/Projects/buddyhub/specs/04-command-surface-spec.md)

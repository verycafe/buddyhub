# BuddyHub Research Notes

- Status: Living document
- Date created: 2026-04-04
- Scope: Claude Code Buddy, adjacent Claude Code extension capabilities, and local runtime evidence

## Purpose

This file is the long-term research notebook for BuddyHub.

Use it to:

- store high-signal research findings
- separate official facts from reverse-engineered findings
- keep source links in one place
- capture open questions before they turn into product assumptions

When adding new material, prefer this format:

1. `Date`
2. `Topic`
3. `Finding`
4. `Source`
5. `Confidence`
6. `Why it matters`

## Confidence Legend

- `Official`: confirmed by Anthropic or Claude Code docs
- `Local runtime`: confirmed from files on this machine
- `Reverse-engineered`: extracted from leaked or mirrored code, not official API
- `Community analysis`: third-party interpretation, useful but lower confidence
- `Inference`: reasoned conclusion from available evidence

## Source Index

### Official docs

- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Submit a Claude plugin](https://claude.com/docs/plugins/submit)

### Reverse-engineered and community sources

- [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)
- [Gitverse mirror / claude-code](https://gitverse.ru/Ingw/claude-code)

### Local runtime evidence on this machine

- [/Users/tvwoo/.claude/pet/hook.sh](/Users/tvwoo/.claude/pet/hook.sh)
- [/Users/tvwoo/.claude/pet/pet.py](/Users/tvwoo/.claude/pet/pet.py)
- [/Users/tvwoo/.claude/pet/state.json](/Users/tvwoo/.claude/pet/state.json)

## Claude Code Buddy: Current Understanding

### Summary

As of 2026-04-04, no official public Buddy-specific API or Buddy-specific schema was found in Anthropic or Claude Code docs during this research round.

What is publicly documented today is the surrounding extension surface:

- plugins
- plugin marketplaces
- hooks
- MCP
- related command and integration mechanisms

Buddy-specific structure currently comes mainly from reverse-engineered sources and local runtime experiments.

Confidence: `Inference`

## Officially Confirmed Adjacent Capabilities

### Plugin and marketplace support

Claude Code officially supports:

- installable plugins
- self-hosted plugin marketplaces
- plugin distribution through git-hosted marketplace catalogs

Why it matters:

- BuddyHub can be distributed as a real Claude Code plugin
- BuddyHub does not need Anthropic's official marketplace to start
- installation can be productized instead of manual file copying

Confidence: `Official`
Source: [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

### Hook support

Claude Code officially supports hook events that can react to session or tool activity.

Why it matters:

- Buddy state can be driven by Claude Code activity
- a lightweight Buddy can exist even without deep internal UI access

Confidence: `Official`
Source: [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)

### MCP support

Claude Code officially supports MCP, including local process-based MCP servers.

Why it matters:

- BuddyHub can add structured memory and tools later
- MVP does not need a remote backend

Confidence: `Official`
Source: [Claude Code MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)

## Reverse-Engineered Buddy Schema

### High-confidence extracted fields

The reverse-engineered `buddy-app` gist exposes a companion schema with the following fields:

- `rarity`
- `species`
- `eye`
- `hat`
- `shiny`
- `stats`

The same extracted viewer also shows named stat categories and rendering logic.

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Stat names

The extracted Buddy stat names are:

- `DEBUGGING`
- `PATIENCE`
- `CHAOS`
- `WISDOM`
- `SNARK`

These appear in `STAT_NAMES` in the extracted code.

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Rarity system

The extracted rarity levels are:

- `common`
- `uncommon`
- `rare`
- `epic`
- `legendary`

The extracted code also includes:

- rarity weights
- rarity floor values
- rarity star rendering
- rarity color rendering

This suggests rarity is not only cosmetic; it appears to influence stat generation floors.

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Species list

The extracted species list contains 18 entries:

- `duck`
- `goose`
- `blob`
- `cat`
- `dragon`
- `octopus`
- `owl`
- `penguin`
- `turtle`
- `snail`
- `ghost`
- `axolotl`
- `capybara`
- `cactus`
- `robot`
- `rabbit`
- `mushroom`
- `chonk`

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Eye and hat variants

The extracted code contains:

- 6 eye variants
- 8 hat variants

Observed eye symbols:

- `·`
- `✦`
- `×`
- `◉`
- `@`
- `°`

Observed hat values:

- `none`
- `crown`
- `tophat`
- `propeller`
- `halo`
- `wizard`
- `beanie`
- `tinyduck`

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Shiny variant

The extracted code includes:

- a `shiny` boolean
- a shiny roll threshold of `rng() < 0.01`

This implies a 1% shiny probability in the extracted implementation.

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Deterministic generation

The extracted code shows:

- `mulberry32` for pseudo-random generation
- `hashString(userId + SALT)` as the seed
- `SALT = "friend-2026-401"`

This strongly suggests Buddy generation is deterministic per user identifier in the extracted implementation.

Confidence: `Reverse-engineered`
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

### Stat roll shape

The extracted stat generation logic includes:

- a rarity-based floor
- one `peak` stat
- one `dump` stat
- middle-range rolls for the remaining stats

Why it matters:

- Buddies are likely intended to have strengths and weaknesses
- task fit may be represented as soft preference, not total lockout

The second point is still an inference; the generation shape itself is directly visible in the extracted code.

Confidence: `Reverse-engineered` for the roll shape, `Inference` for task-fit interpretation
Source: [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)

## Reverse-Engineered Buddy UI Patterns

### Viewer-level UI elements seen in extracted material

The extracted viewer and related community references indicate Buddy is presented with a compact, character-based visual style and supporting metadata such as:

- name
- rarity stars
- shiny marker
- species label
- visible stat bars
- eye and hat styling

Community references also describe Buddy as living near the Claude Code input area and behaving like a companion.

Confidence: `Reverse-engineered` for the viewer fields, `Community analysis` for the broader placement description
Sources:

- [raya-ac buddy-app gist](https://gist.github.com/raya-ac/5adcfe03d5229bf9e84da3a54dc06889)
- [Gitverse mirror / claude-code](https://gitverse.ru/Ingw/claude-code)

### Important caveat

We do not currently have an official public extension point that guarantees third-party plugins can inject a custom Buddy widget directly into Claude Code's internal input-area UI.

Why it matters:

- BuddyHub should not assume native in-input embedding is available
- V1 should prefer a nearby or external companion display that is controllable today

Confidence: `Inference`

## Local Runtime Evidence: Existing Pet Prototype

### What exists locally

This machine already contains a working local pet runtime under `/Users/tvwoo/.claude/pet/`.

Observed files:

- [/Users/tvwoo/.claude/pet/hook.sh](/Users/tvwoo/.claude/pet/hook.sh)
- [/Users/tvwoo/.claude/pet/pet.py](/Users/tvwoo/.claude/pet/pet.py)
- [/Users/tvwoo/.claude/pet/state.json](/Users/tvwoo/.claude/pet/state.json)

Confidence: `Local runtime`

### State bridge behavior

The local hook script writes Buddy state into `state.json` based on Claude Code hook activity.

Relevant implementation details:

- `write_state()` writes `state`, `tool`, and `timestamp`
- `PreToolUse` maps tools to Buddy states
- `PostToolUse` returns to `thinking`
- `Stop` sets `done`
- `Notification` sets `waiting`

Observed state mapping in the local script:

- `Read|Glob|Grep -> reading`
- `Edit|Write|NotebookEdit -> coding`
- `Bash -> running`
- `WebFetch|WebSearch -> browsing`
- `AskUserQuestion -> waiting`
- `Task -> exploring`
- fallback -> `thinking`

Why it matters:

- a reactive Buddy can be built without privileged internal model hooks
- Claude activity can already be translated into a visual companion state machine

Confidence: `Local runtime`
Source: [/Users/tvwoo/.claude/pet/hook.sh](/Users/tvwoo/.claude/pet/hook.sh)

### Desktop pet renderer behavior

The local `pet.py` script implements a desktop companion window using:

- `tkinter`
- `Pillow`
- sprite animation frames from `sprites.py`
- polling of `state.json`

Observed rendering behavior:

- always-on-top floating window
- animated sprite
- state label text
- auto-return to idle after timeout
- hover, click, drag, and pet-like interactions

Observed display states in `STATE_LABELS`:

- `idle`
- `thinking`
- `coding`
- `reading`
- `running`
- `waiting`
- `error`
- `done`
- `browsing`
- `exploring`
- `clicked`
- `dragged`
- `petted`

Why it matters:

- the simplest strong BuddyHub MVP is already visible in local prototype form
- the state-driven Buddy concept is proven independently of official internal Buddy APIs

Confidence: `Local runtime`
Source: [/Users/tvwoo/.claude/pet/pet.py](/Users/tvwoo/.claude/pet/pet.py)

## Product Implications for BuddyHub

### What is safe to build first

A strong first version can focus on:

- showing a Buddy visually
- reacting to Claude Code activity states
- keeping state mapping simple and reliable
- avoiding undocumented internal UI hooks

Confidence: `Inference`

### Recommended V1 framing

Recommended V1 definition:

`A reactive Claude companion that visibly mirrors Claude Code's current working state.`

This can be built before:

- full long-term memory
- cloud sync
- complex task-routing logic
- native internal Claude UI embedding

Confidence: `Inference`

### What should not be assumed yet

Do not assume the following until directly confirmed:

- direct access to the user's official Buddy record
- stable access to official Buddy species or stat data from the Claude runtime
- a documented third-party Buddy UI injection API
- official support for rendering a plugin's custom companion inside Claude's exact native Buddy slot

Confidence: `Inference`

## Open Questions

1. Is there any local Claude Code runtime file on this machine that stores the official Buddy identity, stats, or companion seed?
2. Can Claude Code plugin APIs expose a status-line or adjacent surface that is sufficient for a compact in-app Buddy?
3. Should BuddyHub V1 render as:
   - a desktop floating Buddy
   - a terminal/status-line Buddy
   - both
4. If BuddyHub later mirrors the leaked Buddy schema, which fields are required for compatibility and which are only cosmetic?
5. Should BuddyHub preserve the leaked stat names as-is, or abstract them behind user-facing labels?

## Research Log

### 2026-04-04 - Initial Buddy schema pass

Finding:

- official public Buddy API not found
- reverse-engineered schema indicates rarity, species, eye, hat, shiny, and five stats
- local runtime prototype proves state-driven Buddy behavior is practical today

Why it matters:

- BuddyHub can ship a useful V1 without waiting for undocumented platform features

Confidence:

- mixed: `Official`, `Reverse-engineered`, `Local runtime`, and `Inference`

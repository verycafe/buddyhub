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

We do not currently have an official public extension point that guarantees third-party plugins can inject or directly control the native Buddy widget that Claude Code renders in the bottom-right UI.

Why it matters:

- knowing the Buddy schema is not the same as knowing how to drive the official Buddy runtime
- BuddyHub must not confuse "we understand the Buddy" with "plugins can control the Buddy"

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

## Local Runtime Evidence: Claude Transcript Buddy Identity

### Transcript attachment source

Claude session transcripts on this machine contain a `companion_intro` attachment.

Observed attachment shape:

```json
{"type":"companion_intro","name":"Crumpet","species":"blob"}
```

Observed fields confirmed locally so far:

- `name`
- `species`

Observed example paths:

- [/Users/tvwoo/.claude/projects/-Users-tvwoo-Projects-buddyhub/fcd69059-d2d2-46e3-b049-9f91753d762f.jsonl](/Users/tvwoo/.claude/projects/-Users-tvwoo-Projects-buddyhub/fcd69059-d2d2-46e3-b049-9f91753d762f.jsonl)
- [/Users/tvwoo/.claude/projects/-Users-tvwoo/af3ef4ed-784d-418a-aef1-2649f3aa942a.jsonl](/Users/tvwoo/.claude/projects/-Users-tvwoo/af3ef4ed-784d-418a-aef1-2649f3aa942a.jsonl)

Why it matters:

- BuddyHub can read a real current-user Buddy identity source today
- BuddyHub should build enhancement on top of this source instead of substituting a generic Buddy

Confidence: `Local runtime`

### Important boundary

The transcript attachment source currently confirms `name` and `species`, but this research pass has not yet confirmed a stable local runtime source for:

- `rarity`
- `shiny`
- `hat`
- `eye`
- `stats`

Why it matters:

- reverse-engineered schema and runtime availability are different things
- BuddyHub should use reverse-engineered schema as a compatibility map, not as permission to fabricate missing user values

Confidence: `Local runtime` for the observed transcript shape, `Inference` for the product rule derived from it

## Official Buddy Control Surface Findings

### Official plugin docs do not expose Buddy UI control

The official Claude Code plugin docs currently document third-party plugin components such as:

- commands and skills
- agents
- hooks
- MCP servers
- LSP servers
- `settings.json`
- `bin/`

This research pass did not find an official plugin component for:

- `local-jsx`
- `setAppState`
- `companionReaction`
- direct native Buddy UI control

Why it matters:

- a normal plugin cannot assume it can define or call the same internal Buddy UI command type used by Claude Code itself
- the existence of plugin commands does not imply access to native Buddy rendering

Confidence: `Official`
Sources:

- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

### Local Claude binary shows an internal Buddy control path

Inspection of the local Claude Code 2.1.92 binary strings on this machine shows:

- a built-in `/buddy` command implemented as `type:"local-jsx"`
- internal companion intro generation from the current Buddy record
- internal writes to `companionReaction`
- internal writes to `companionPetAt`
- use of in-process `setAppState(...)` to update Buddy UI state

Why it matters:

- the official Buddy is definitely controlled by an internal app-state path
- this is evidence that the native Buddy can become more dynamic
- but it is not evidence that third-party plugins can reach that path

Confidence: `Local runtime`
Sources:

- [/Users/tvwoo/.local/share/claude/versions/2.1.92](/Users/tvwoo/.local/share/claude/versions/2.1.92)
- [/tmp/claude-2.1.92.strings](/tmp/claude-2.1.92.strings)

### Native control path includes a Buddy reaction API and app-state write

This round of local binary inspection found a more specific native pipeline:

- `_S7(...)` inspects recent conversation state and tool-result context
- `Oo_(...)` posts to an internal endpoint:
  - `/api/organizations/{orgUuid}/claude_code/buddy_react`
- the returned reaction string is then written into native app state:
  - `setAppState(... companionReaction: reaction ...)`

The same area also shows:

- native hatch flow
- native pet flow
- native mute state

Why it matters:

- official Buddy dynamics are not just transcript metadata
- they depend on native in-process state mutation
- a third-party plugin would need some way to reach that same native state write path

Confidence: `Local runtime` + `Reverse-engineered`
Sources:

- [/tmp/claude-2.1.92.strings](/tmp/claude-2.1.92.strings)

### Transcript access is identity-level, not control-level

On this machine, Claude transcripts expose `companion_intro` attachments containing:

- `name`
- `species`

This research pass did not find transcript events that let a third-party plugin set:

- `companionReaction`
- a native Buddy animation state
- a native Buddy emotion or bubble state

Why it matters:

- transcript parsing is enough to verify the user's Buddy identity
- transcript parsing is not currently enough to drive the official Buddy UI

Confidence: `Local runtime`

### Current blocker

BuddyHub's intended product target is:

- enhance the official Claude Code Buddy already shown in the bottom-right UI

This research pass confirms:

- we understand a large part of the Buddy schema
- we can read the current Buddy identity from transcripts
- we can see an internal native Buddy control path in the Claude binary

But it does not yet confirm:

- a supported third-party plugin path to set the native Buddy's `companionReaction`
- a supported third-party plugin path to invoke first-party `local-jsx` Buddy behavior from BuddyHub
- a writable config or runtime file on disk that safely controls the native Buddy widget

Why it matters:

- BuddyHub must not claim success just because `/buddyhub:open` or `/buddyhub:status` render text
- until the official Buddy control path is reachable, text output is diagnostic tooling, not the finished product

Confidence: `Inference`

### First-party auth is confirmed locally

This machine currently reports:

- `claude auth status --json`
  - `loggedIn: true`
  - `authMethod: oauth_token`
  - `apiProvider: firstParty`

Local telemetry samples on this machine also repeatedly include:

- `provider: "firstParty"`

Why it matters:

- the current blocker is not "wrong auth provider"
- the failure to enhance the native Buddy cannot be explained by non-first-party auth alone
- the unresolved problem is native control-path reachability from third-party plugin code

Confidence: `Local runtime`
Sources:

- `claude auth status --json`
- [/Users/tvwoo/.claude/settings.json](/Users/tvwoo/.claude/settings.json)
- `/Users/tvwoo/.claude/telemetry/*.json`

## Product Implications for BuddyHub

### What is safe to build first

The following are safe as research and diagnostic tools:

- hook-driven state capture
- verified Buddy identity capture
- compact debug commands
- optional status-line summaries

These are useful for investigation, but they do not satisfy the core product goal by themselves.

Confidence: `Inference`

### Recommended product framing

Recommended BuddyHub definition:

`A Claude Code plugin that enhances the user's official native Buddy in the bottom-right UI with more visible, verified dynamics driven by Claude activity.`

Important implementation rule:

- text commands and status-line output may exist as support tooling
- they must not be treated as the primary Buddy experience or as completion criteria

Confidence: `Inference`

### What should not be assumed yet

Do not assume the following until directly confirmed:

- direct access to the user's official Buddy record
- stable access to official Buddy species or stat data from the Claude runtime beyond `companion_intro`
- a documented third-party Buddy UI injection API
- a documented third-party way to write native `companionReaction`
- permission to fabricate missing Buddy appearance or identity fields from reverse-engineered defaults

Confidence: `Inference`

## Open Questions

1. Is there any local Claude Code runtime file on this machine that stores the official Buddy identity, stats, or companion seed?
2. Is there any supported plugin-accessible path to the internal native Buddy control surface, especially `companionReaction`?
3. Can a third-party plugin define or reach `local-jsx` command behavior, or is that strictly first-party/internal?
4. If BuddyHub later mirrors more of the leaked Buddy schema, which fields are required for compatibility and which are only cosmetic?
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

### 2026-04-04 - Official Buddy control surface pass

Finding:

- official plugin docs expose commands, skills, hooks, MCP, LSP, settings, and `bin`, but no Buddy-specific UI control surface
- local Claude Code 2.1.92 binary contains a built-in `local-jsx` `/buddy` command and internal `companionReaction` updates through `setAppState(...)`
- transcripts on this machine expose `companion_intro` but not a writable native Buddy reaction channel

Why it matters:

- BuddyHub's real target is the official bottom-right Buddy, not a parallel text pet
- current BuddyHub text commands are diagnostic aids only
- the core technical question is now whether a third-party plugin can reach the internal native Buddy control path without patching Claude Code

Confidence:

- mixed: `Official`, `Local runtime`, and `Inference`

### 2026-04-04 - Native reaction pipeline and auth gate follow-up

Finding:

- local auth status confirms `apiProvider = firstParty`
- no current shell evidence was found for `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- the local Claude binary shows the native Buddy reaction pipeline as:
  - `_S7(...) -> Oo_(...) -> setAppState(... companionReaction ...)`
- the reaction request goes through an internal Buddy endpoint rather than transcript writes alone

Why it matters:

- BuddyHub is not blocked on identity lookup anymore
- BuddyHub is blocked on native control-path access
- a standard third-party plugin still has no confirmed way to write the official Buddy's `companionReaction`

Confidence:

- mixed: `Local runtime`, `Reverse-engineered`, and `Inference`

### 2026-04-05 - Public plugin settings surface pass

Finding:

- local Claude changelog explicitly states: `Plugin options (manifest.userConfig) now available externally`
- `claude plugin validate` accepts `manifest.userConfig` as a record of fields with at least:
  - `title`
  - `description`
  - `type`
  - `default`
  - `required`
  - `sensitive`
- the same validator rejects:
  - `label`
  - `choices`
  - `placeholder`
- the accepted field types are consistent with local binary schema strings indicating:
  - `string`
  - `number`
  - `boolean`
  - `directory`
  - `file`
- no official marketplace plugin on this machine currently demonstrates a richer public `userConfig` example

Why it matters:

- Claude Code does expose a public plugin configuration surface
- but the currently verified public surface looks like a basic config dialog, not a rich option-picker with dropdowns, swatches, or live Buddy preview
- BuddyHub should not assume that public plugin config alone can deliver the desired native-looking element/color preview UX

Confidence:

- mixed: `Official` (local changelog), `Local runtime`, and `Inference`

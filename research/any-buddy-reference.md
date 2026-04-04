# any-buddy Reference Notes

- Date: 2026-04-04
- Project: [cpaczek/any-buddy](https://github.com/cpaczek/any-buddy)
- Scope: what BuddyHub can learn from `any-buddy`, and what does not transfer

## High-Level Take

`any-buddy` is relevant to BuddyHub, but mostly as a reference for:

- native Buddy identity hacking
- patch safety and recovery mechanics
- cross-platform install/runtime detection
- a polished customization flow around Claude Code Buddy traits

It is **not** a direct answer to BuddyHub's current blocker.

BuddyHub's unresolved problem is:

- enhancing the official bottom-right Buddy's live native behavior and reactions

`any-buddy` mainly addresses a different problem:

- changing which Buddy you get by changing the salt used for deterministic Buddy generation

That distinction matters.

## What `any-buddy` Actually Does

According to the repository README and technical notes:

- it lets the user choose Buddy identity traits such as species, rarity, eyes, hat, shiny, name, and personality
- it brute-forces a replacement salt string that yields the desired Buddy for the user's real Claude user ID
- it patches the Claude Code binary or JS bundle in place
- it can optionally install a `SessionStart` hook that silently reapplies the patch after Claude Code updates

Sources:

- [README](https://github.com/cpaczek/any-buddy)
- [HOW_IT_WORKS.md](https://github.com/cpaczek/any-buddy/blob/main/HOW_IT_WORKS.md)

## Why This Matters For BuddyHub

This project is strong evidence that:

- the official Buddy identity path can be influenced at the native Claude Code level
- identity customization does not require a supported third-party plugin API if you are willing to patch Claude Code itself
- update-resilient Buddy customization is feasible with backup, restore, and auto-reapply mechanisms

However:

- this is a binary-patch strategy
- it is outside the normal plugin surface
- it changes Claude Code installation artifacts

So it is useful as a research signal, but not something BuddyHub should copy blindly.

## Lessons Worth Borrowing

### 1. Draw a hard line between identity and runtime behavior

`any-buddy` is clear about the fact that it is changing deterministic Buddy generation, not inventing a second UI pet.

Why it matters for BuddyHub:

- we should keep separating:
  - official Buddy identity
  - official Buddy native runtime reactions
  - BuddyHub diagnostic surfaces

This is especially important after earlier product drift where a text Buddy view was starting to masquerade as the product itself.

### 2. Recovery and reversibility are first-class

`any-buddy` emphasizes:

- backup before patching
- restore command
- auto-repair after Claude Code updates
- verification after patching

Why it matters for BuddyHub:

- if BuddyHub ever touches native Claude artifacts, restore and rollback must be designed before the patch path ships
- "safe uninstall" and "do not break Claude Code" cannot be hand-wavy requirements

### 3. Use atomic file replacement

The project documents:

- patching through temp file write + atomic rename
- verifying the result afterward
- keeping a backup of the original artifact

Why it matters for BuddyHub:

- if we ever patch native assets, this is the minimum acceptable write discipline
- this matches BuddyHub's existing safety posture better than ad hoc in-place mutation

### 4. Build for update churn

`any-buddy` explicitly handles the fact that Claude Code updates will overwrite native changes.

It uses:

- saved local state
- an optional `SessionStart` hook
- fast re-apply logic

Why it matters for BuddyHub:

- any native enhancement strategy has to survive Claude Code updates
- even if we do not patch the binary, we should think in terms of:
  - detect drift
  - repair safely
  - keep repair optional and visible to the user

### 5. Strong fallback UX matters

The project supports:

- interactive Bun/OpenTUI flow when available
- simpler sequential prompts when not

Why it matters for BuddyHub:

- terminal capability differences are real
- if we build any richer TUI layer later, graceful fallback matters more than visual ambition

### 6. Clear platform-specific handling

The project documents different behavior for:

- Linux
- macOS
- Windows

And notes macOS-specific re-signing after patching.

Why it matters for BuddyHub:

- native Claude modification is not a single implementation problem
- macOS code-signing and path detection must be treated explicitly, not assumed away

### 7. Explicit limits build trust

`any-buddy` lists known limitations such as:

- Bun being preferred or required for best behavior
- update dependence on the salt remaining stable
- exact stat values still being seed-determined

Why it matters for BuddyHub:

- we should continue being explicit about what is verified, experimental, or unavailable
- this is especially important when dealing with unsupported native paths

## Lessons We Should Not Copy Directly

### 1. Binary patching as the default product path

This is the biggest caution.

BuddyHub's current product requirements include:

- safe install
- safe disable
- safe uninstall
- do not interfere with normal Claude Code use

A binary-patch approach pushes directly against those constraints.

Possible implication:

- if BuddyHub ever explores native patching, it should likely be a clearly labeled experimental track, not the default install path

### 2. Automatic modification of user config without ownership discipline

`any-buddy` adds an optional `SessionStart` hook in `~/.claude/settings.json`.

That is understandable for its use case, but for BuddyHub we already care deeply about:

- ownership manifest
- reversible cleanup
- non-destructive uninstall

So the lesson is not "auto-edit settings freely".

The lesson is:

- if we touch settings, we need precise ownership and rollback rules

### 3. Solving a different problem and mistaking it for ours

`any-buddy` solves:

- "I want a different official Buddy identity"

BuddyHub currently needs to solve:

- "I want richer live behavior in the existing official Buddy"

Those overlap, but they are not the same.

## Most Important Boundary

This repo does **not** appear to solve the main BuddyHub blocker:

- writing live native Buddy reaction state such as `companionReaction`

From the public repo materials examined here, `any-buddy` focuses on:

- salt search
- identity selection
- binary patching
- restore/reapply

It does **not** appear to document:

- a plugin-accessible path to official native Buddy reactions
- a confirmed third-party write path to `companionReaction`
- a mechanism for richer live official Buddy animation logic

So the direct conclusion is:

- `any-buddy` is useful for native identity customization research
- `any-buddy` is not yet evidence that the official Buddy's live reaction path is controllable from a third-party plugin

## Concrete Takeaways For BuddyHub

If BuddyHub continues on the current path, the best takeaways are:

1. Keep the product model honest: official Buddy first, diagnostics second.
2. If native patching is explored, make it explicit, reversible, and off by default.
3. Treat backup, restore, and update-reapply as mandatory architecture, not cleanup work.
4. Keep platform handling explicit, especially macOS signing concerns.
5. Do not mistake identity customization for live native behavior control.

## Sources

- [cpaczek/any-buddy README](https://github.com/cpaczek/any-buddy)
- [cpaczek/any-buddy HOW_IT_WORKS.md](https://github.com/cpaczek/any-buddy/blob/main/HOW_IT_WORKS.md)
- [cpaczek/any-buddy package.json](https://raw.githubusercontent.com/cpaczek/any-buddy/main/package.json)

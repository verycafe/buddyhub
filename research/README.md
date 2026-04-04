# Research Folder

This folder stores research materials for BuddyHub.

## Purpose

Use this folder for:

- competitive research
- Claude Code capability notes
- reverse-engineering findings
- local runtime observations
- UI references
- product and technical investigation notes

## Current Files

- [claude-code-buddy.md](/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md): current working notes for Claude Code Buddy attributes, UI, state handling, and related evidence
- [recon-reference.md](/Users/tvwoo/Projects/buddyhub/research/recon-reference.md): analysis of `gavraz/recon`, focused on mechanisms and patterns BuddyHub can learn from
- [any-buddy-reference.md](/Users/tvwoo/Projects/buddyhub/research/any-buddy-reference.md): analysis of `cpaczek/any-buddy`, focused on native Buddy identity patching, recovery mechanics, and what does or does not transfer to BuddyHub

## Suggested Conventions

- Keep one topic per file when possible.
- Prefer descriptive filenames such as:
  - `claude-code-buddy.md`
  - `recon-reference.md`
  - `any-buddy-reference.md`
  - `plugin-distribution.md`
  - `ui-placement-notes.md`
- Put links, source quality, and confidence notes into each file.
- Separate official facts from reverse-engineered findings.

## Directory Rule

Product definition documents such as [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md) stay in the repository root.

Exploratory and accumulating materials go into this `research/` folder.

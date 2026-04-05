# BuddyHub Repo Rules

This repository now uses versioned product docs.

## Current Source Of Truth

Before doing product, UX, install, or workflow changes, read these current docs first:

- `V0.2/PRD.md`
- `V0.2/specs/README.md`
- every file under `V0.2/specs/`
- `V0.2/SPEC-STATUS.md`

## Version Rules

- `V0.2/` is the active development version.
- `V0.1/` is an archive snapshot and should be treated as read-only history.
- Root `PRD.md` and root `specs/README.md` are index files only, not the active product source of truth.

## Status Rule

When a spec reaches a meaningful milestone or completion state, update:

- `V0.2/SPEC-STATUS.md`

Do not mark a spec done unless implementation and verification evidence exist.

## Research Rule

Reference and investigation notes belong under:

- `research/`

Add new external-library or architecture notes there instead of mixing them into active PRD or spec files.

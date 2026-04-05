# BuddyHub V0.2 Install And Distribution Spec

- Status: Active
- Derived from: [../PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)

## 1. Purpose

Define the public installation contract for the current phase.

## 2. Public Install Path

V0.2 publicly documents only one install path:

```bash
npm install -g github:verycafe/buddyhub
```

After install, the user runs:

```bash
buddyhub
```

## 3. Packaging Rule

The current public package is a standalone CLI.

The menu experience must start from the `buddyhub` command itself.

## 4. Current Non-Goals

This phase does not require public documentation for:

- `pip`
- `brew`
- legacy Claude plugin installation

Those paths may exist historically or internally, but they are not the public install story for V0.2.

## 5. Acceptance

This spec is satisfied when:

1. npm install gives the user a runnable `buddyhub` command
2. the README documents npm as the public install path
3. launch enters the standalone menu, not a plugin command surface

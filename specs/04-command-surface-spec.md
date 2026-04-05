# Buddy Command Surface Spec

- Status: Draft v0.5
- Derived from: [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)

## 1. Purpose

Define the minimum external control surface that supports official Buddy visual customization.

The standalone TUI menu is the primary control surface.

It exists to:

- open customization settings
- inspect the current install
- back up and patch the native Buddy target
- restore the original file
- uninstall BuddyHub cleanly
- diagnose failures

## 2. Surface Design Principles

The control surface must be:

- explicit
- low-risk
- reversible where applicable
- honest about platform and version limits

The control surface must not:

- pretend a text command itself is the product
- imply Buddy enhancement succeeded before the official Buddy visibly changes

## 3. Required Surface Entries

BuddyHub V1 should include at least these user-facing entries:

- language
- color
- nickname
- apply
- restore
- uninstall
- quit

The exact launch path may evolve, but these functions are the required standalone surface.

## 4. Required Behavior

### 4.1 Language

Must let the user switch the full TUI language immediately.

### 4.2 Color

Must let the user:

- choose a color preset
- preview the draft instantly
- see whether a color is unavailable

If a color is unsupported on the current target, the menu must say so explicitly.

### 4.3 Nickname

Must let the user:

- enter a nickname directly
- clear the nickname
- preview the draft name immediately

### 4.4 Apply

Must:

- create or confirm backup
- apply the current selected native visual customization
- apply the saved nickname override only when the Claude runtime config path is verified
- perform verification
- report success only if the target patch was actually written
- tell the user to restart Claude Code
- make it explicit that the bottom-right Buddy and `/buddy` card will share the same verified nickname/color source after restart

### 4.5 Restore

Must:

- restore the original binary from backup
- restore the original displayed Buddy name from config backup when nickname override was applied
- verify the restored target is usable
- state that restore returns both the bottom-right Buddy and the `/buddy` card to the original source

### 4.6 Uninstall

Must:

- perform restore automatically when BuddyHub has patched the user's install
- clean BuddyHub-owned metadata automatically
- clean old Claude plugin traces automatically
- schedule package-manager uninstall automatically when BuddyHub was installed through pip/npm/brew
- avoid asking the user to run a second uninstall command by hand

## 5. Explicit Non-Goals

This phase does not require support for:

- runtime state reporting
- plugin slash commands
- Claude `/config` plugin menus
- status line toggles
- hook-driven Buddy activity
- text Buddy rendering

## 6. Acceptance Criteria

This spec is satisfied when:

1. The user can open a standalone TUI settings flow.
2. The user can choose language, color, and nickname from that menu.
3. The user can apply the selected customization through a clear menu path.
4. The user is clearly told to restart Claude Code after apply.
5. The user can restore the original install through a clear menu path.
6. The user can uninstall BuddyHub without manual follow-up shell commands.
7. The menu never substitutes for real official Buddy enhancement.

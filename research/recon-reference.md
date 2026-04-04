# Recon Reference Notes

- Date: 2026-04-04
- Project: [gavraz/recon](https://github.com/gavraz/recon)
- Positioning: tmux-native dashboard for managing Claude Code agents
- Relevance to BuddyHub: does not use Claude Code Buddy itself, but contains several strong interaction, status, and orchestration patterns worth learning

## Summary

`recon` is not a Buddy clone.

It is a terminal-native operations layer for multiple Claude Code sessions. Its value is not in reproducing Claude Code internals, but in turning existing Claude runtime signals into:

- a lightweight state model
- a visual ambient dashboard
- a fast operator workflow

For BuddyHub, the key lesson is:

`You do not need privileged internal Buddy APIs to build a compelling companion experience if you can reliably observe Claude's state and turn it into a strong visual language.`

## Source Quality

- Primary source: [gavraz/recon README](https://github.com/gavraz/recon)
- Confidence: `High` for features and architecture explicitly stated in the README

## What Recon Is Doing Well

## 1. It turns agent state into ambient characters

Recon has a `Tamagotchi View` where each Claude Code session becomes a pixel-art creature in a room.

The README describes these states:

- `Working`
- `Input`
- `Idle`
- `New`

And maps them to creature forms such as:

- happy blob with sparkles
- angry blob
- sleeping blob
- egg

Why this matters:

- It proves that state can be made emotionally legible without needing full anthropomorphic depth.
- Users can glance at a side monitor and know which agents are busy, blocked, or idle.
- This is directly relevant to BuddyHub's planned reactive Buddy behavior.

What BuddyHub can learn:

- represent Claude state visually, not just textually
- keep the state vocabulary small and immediately readable
- let the visual state carry meaning before opening any detail panel

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 2. It builds on observable runtime artifacts instead of hidden APIs

Recon's architecture is intentionally practical. The README says it reads:

- `tmux list-panes` for PID and session name
- `~/.claude/sessions/{PID}.json`
- `~/.claude/projects/.../*.jsonl`
- `tmux capture-pane` for the Claude Code status bar text

Why this matters:

- This is a very strong pattern for BuddyHub.
- It avoids pretending there is a formal agent-management API when there is not.
- It uses stable-enough local artifacts as the source of truth.

What BuddyHub can learn:

- prefer local runtime evidence over undocumented assumptions
- build around files, hooks, and visible terminal output where possible
- do not block product development on hidden Claude internals

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 3. It uses a minimal state detector

Recon determines session status by inspecting the Claude Code status bar text at the bottom of each tmux pane.

Its README lists examples:

- `esc to interrupt` => `Working`
- `Esc to cancel` => `Input`
- anything else => `Idle`
- `(0 tokens)` => `New`

Why this matters:

- The detection logic is intentionally small and robust.
- It shows that a good ambient product does not need perfect semantic understanding to feel useful.

What BuddyHub can learn:

- start with a small state machine
- map observable cues into strong Buddy states
- optimize for reliability before nuance

This aligns well with our current local pet prototype, which already maps Claude hook/tool activity into states like `reading`, `coding`, `running`, `browsing`, `thinking`, and `done`.

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 4. It separates overview view from detail view

Recon provides at least two major views:

- `Table View` for operational detail
- `Tamagotchi View` for ambient understanding

Why this matters:

- This is one of the clearest product lessons for BuddyHub.
- Users need both:
  - a compact emotional or visual overview
  - a detailed operational view when they want specifics

What BuddyHub can learn:

- keep a compact Buddy display for passive awareness
- provide a detailed Buddy status card or inspection panel for active use
- do not force one view to do both jobs

For BuddyHub this could translate into:

- ambient Buddy display near the Claude input area or in a sidecar
- detail view showing current state, trait summary, recent actions, and memory/context

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 5. It organizes agents spatially by repository

Recon groups agents by git repository into rooms. Worktrees of the same repo share a room, while monorepo sub-projects can get their own room.

Why this matters:

- This is a very smart mental model.
- It gives visual structure to a potentially messy multi-agent environment.

What BuddyHub can learn:

- project context should be a first-class organizing principle
- if BuddyHub later supports multiple sessions or project memories, the UI should group by project, not by raw process
- even for a single Buddy, "room" can be a useful metaphor for project-specific states

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 6. It is keyboard-first and low-friction

Recon is designed to open from tmux popups and be operated entirely with keys.

Examples from the README:

- popup keybindings through `tmux.conf`
- quick navigation
- quick switching
- quick next-input jump
- kill selected session

Why this matters:

- The product stays close to the user's existing flow.
- It behaves like a terminal-native layer, not a separate app that steals attention.

What BuddyHub can learn:

- installation and invocation should be friction-light
- Buddy interactions should work well from commands and small popups
- avoid requiring a heavyweight separate dashboard for basic use

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 7. It supports session lifecycle operations, not just visualization

Recon is not only a viewer. Its commands include:

- `launch`
- `new`
- `resume`
- `next`
- `park`
- `unpark`
- `json`

Why this matters:

- This is a reminder that observability tools become much more valuable when they can also act.
- Even a Buddy can become more useful if it is not only decorative.

What BuddyHub can learn:

- the Buddy should eventually do more than animate
- even if V1 is state-reactive, later versions should expose action verbs
- structured command surfaces matter

Examples for BuddyHub later:

- resume last context
- recall current project memory
- export recent state
- open the next item needing attention

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## 8. It documents limitations honestly

Recon explicitly documents a limitation around Claude Code's `/clear`, saying that it can create stale tracking data because session mapping does not update the way recon expects.

Why this matters:

- This is good product hygiene.
- Tools that sit beside Claude Code need to be explicit about what they infer, what they know, and where they can drift.

What BuddyHub can learn:

- document all runtime assumptions
- clearly label inferred Buddy state versus confirmed state
- include a troubleshooting section from the beginning

Source: [gavraz/recon README](https://github.com/gavraz/recon)

## Most Valuable Mechanisms for BuddyHub

If we distill recon into the pieces most worth borrowing, the strongest ones are:

1. `State-first design`
Turn runtime signals into a small, meaningful state machine.

2. `Ambient view + detailed view`
Let users glance first, inspect second.

3. `Observable-runtime integration`
Build from tmux, files, hooks, and visible UI text instead of undocumented APIs.

4. `Project-based grouping`
Organize intelligence around repos and project context.

5. `Keyboard-native workflow`
Stay close to the terminal instead of pulling users into a separate heavy GUI.

6. `Operations, not only aesthetics`
Make the system progressively more useful, not just more charming.

## Where Recon Does Not Map Directly

Recon and BuddyHub are adjacent, but not identical.

Recon is primarily:

- multi-session management
- tmux-centric orchestration
- dashboarding for many agents

BuddyHub is currently shaping up as:

- a reactive Buddy layer
- one user's companion experience
- Claude-state visualization
- later, memory and lightweight action surfaces

This means we should borrow the mechanisms, not copy the product whole.

## Recommended Adaptation for BuddyHub

### For V1

Borrow from recon:

- a compact state machine
- a glanceable visual Buddy
- a secondary detailed status view
- clear mapping from Claude activity to visible Buddy state

Do not borrow yet:

- multi-agent session board
- tmux-heavy session orchestration
- advanced lifecycle commands like park/unpark

### For Later

Potential later borrowings:

- project-grouped rooms or spaces
- queue or "needs attention" surfaces
- structured JSON status export
- session resume and context switching helpers

## Practical Product Takeaway

Recon is valuable reference material because it demonstrates a strong principle:

`Terminal-native AI tooling becomes much more compelling when system state is made visible, spatial, and emotionally legible.`

That principle is highly relevant to BuddyHub.

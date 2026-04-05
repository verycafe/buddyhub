# Ink Reference Notes

- Date: 2026-04-05
- Project: [vadimdemedes/ink](https://github.com/vadimdemedes/ink)
- Source quality: official repository README
- Relevance: candidate UI framework for replacing BuddyHub's current Python `curses` TUI layer

## Summary

Ink is a React renderer for terminal applications.

It gives CLI apps:

- component-based UI
- Flexbox layout through Yoga
- richer text and color rendering
- React hooks for input and focus
- better testing and accessibility primitives than a hand-written `curses` screen

## Why It Matters For BuddyHub

BuddyHub currently ships:

- a Python core runtime: `buddyhub_core.py`
- a Python `curses` TUI: `buddyhub_tui.py`

The TUI file is already large and hand-manages:

- layout
- keyboard routing
- submenu transitions
- color fallback logic
- preview rendering

Ink is relevant because it could replace only the UI layer while leaving BuddyHub's patching and detection logic in Python or behind a bridge.

## Verified Takeaways From The Ink README

### 1. Ink is built for interactive CLI apps

The official README describes Ink as "React for CLIs" and shows `render(<App />)` as the primary entry.

Why it matters:

- BuddyHub's current menu and preview surface maps well to a component tree
- future menu refinements become easier than maintaining a large imperative `curses` renderer

### 2. Ink uses Yoga and Flexbox-style layout

The README states that Ink uses Yoga for layout and supports CSS-like flex properties through `<Box>`.

Why it matters:

- BuddyHub has a left menu column and a right preview column
- the current TUI manually calculates these regions
- Ink would make this split-pane layout much easier to evolve

### 3. Ink has native input hooks

The README documents hooks such as:

- `useInput`
- `useFocus`
- `useFocusManager`
- `useWindowSize`

Why it matters:

- BuddyHub currently handles `Enter`, `Esc`, arrow keys, and text input manually
- Ink would provide a better state-driven interaction model for first-level and second-level menus

### 4. Ink supports richer terminal color usage

The README shows `<Text color="green">`, hex colors, and `rgb(...)` colors.

Why it matters:

- BuddyHub currently spends a lot of code on terminal color fallback and `curses` pair management
- Ink would likely give BuddyHub a clearer path to more faithful preview colors

### 5. Ink has accessibility support

The README includes screen-reader support and ARIA-like attributes.

Why it matters:

- BuddyHub currently has no comparable accessibility layer in the Python TUI
- if BuddyHub keeps growing as a real user-facing configurator, accessibility matters

### 6. Claude Code itself is listed as an Ink user

The official Ink README's "Who's Using Ink?" list includes Claude Code.

Why it matters:

- this does not prove plugin access to Claude Code internal UI
- but it does prove Ink is a credible fit for a sophisticated terminal product in the same ecosystem

## Migration Judgment

The strongest migration shape would be:

1. keep `buddyhub_core.py` as the source of truth for:
   - detection
   - settings
   - patching
   - restore
   - uninstall
2. replace only `buddyhub_tui.py` with an Ink frontend
3. keep `npm` as the public install path

This is safer than rewriting the patch engine itself.

## Risks

- Ink would shift the UI layer from Python to Node/React
- BuddyHub would need a bridge between the Ink frontend and the Python core
- packaging becomes more npm-centric than the current hybrid structure

## Recommendation

Ink looks like a strong candidate for BuddyHub's next UI iteration.

The right scope is:

- migrate the TUI layer
- do not rewrite the patching core first

## Source

- [vadimdemedes/ink](https://github.com/vadimdemedes/ink)

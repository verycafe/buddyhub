---
description: Configure official Buddy visual customization with a guided selection flow
allowed-tools: Bash(python3:*)
argument-hint: "[optional freeform customization request]"
---

Configure BuddyHub's visual customization for the official bottom-right Claude Code Buddy.

Workflow:
1. First run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --json` to inspect the current verified Buddy, saved settings, available options, blockers, and preview lines.
2. Use that JSON as the source of truth for the rest of the interaction.
3. Guide the user through choices for:
   - additive element
   - color preset
   - nickname
4. Prefer a concise choice-style interaction:
   - If a native choice/selection UI is available to you, use it.
   - Otherwise ask one short question at a time with a flat numbered list of available options.
5. When the user chooses a value, persist it with the exact BuddyHub command:
   - element: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --element <value>`
   - color: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --color <value>`
   - nickname: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --nickname "<value>"`
   - clear nickname: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --clear-nickname`
   - reset: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --reset`
6. After each saved change, rerun `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --json` and show the latest preview.
7. Show preview lines in a fenced `text` block whenever they are available.
8. Never claim unsupported settings are active. Rely on:
   - `customization.can_apply`
   - `customization.apply_blockers`
   - `customization.color_options[*].available`
   - `customization.nickname_supported`
9. Only run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" apply --target installed` if the user explicitly asks to make the new look live.
10. After apply, remind the user that Claude Code must be restarted before the official Buddy visibly changes.

Output rules:
- Be concise and guide the user step by step.
- Keep the focus on the official Buddy only.
- Do not mention old TUI/state/statusline concepts.
- Do not paraphrase JSON fields incorrectly.

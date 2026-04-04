---
description: Open BuddyHub visual customization settings for the official Claude Code Buddy
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings $ARGUMENTS`

Present the command output directly to the user.
- Preserve headings, bullets, booleans, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Preserve the exact current settings, availability notes, preview notes, and restart guidance.
- Do not call any additional tools.

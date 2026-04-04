---
description: Install or refresh the BuddyHub pet runtime under ~/.claude/pet
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" pet-install`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not call any additional tools.

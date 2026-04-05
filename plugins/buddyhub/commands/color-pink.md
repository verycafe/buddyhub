---
description: Set BuddyHub color to Pink
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings --color pink`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, booleans, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not call any additional tools.

---
description: Show deterministic official Buddy customization settings and commands
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" settings`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, booleans, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not pretend unsupported color or nickname settings are active.
- Do not call any additional tools.

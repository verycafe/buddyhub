---
description: Pause BuddyHub without uninstalling it
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" pause`

Present the command output directly to the user.
- Preserve headings, bullets, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not call any additional tools.

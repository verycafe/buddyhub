---
description: Apply the current native Buddy visual patch to the detected Claude Code install
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" apply --target installed`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, booleans, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Preserve whether the command applied to the installed target or a rehearsal copy.
- Do not call any additional tools.

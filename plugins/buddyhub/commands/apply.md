---
description: Apply the current native Buddy visual patch to a safe rehearsal copy
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" apply`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, booleans, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Make it clear the command output is rehearsal-copy focused if the command says so.
- Do not call any additional tools.

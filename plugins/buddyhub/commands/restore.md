---
description: Remove the rehearsal patch copy and keep the original backup available
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" restore`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not call any additional tools.

---
description: Inspect the current Claude install, Buddy identity, and patch profile support
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" inspect`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not call any additional tools.

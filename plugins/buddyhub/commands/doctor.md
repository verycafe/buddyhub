---
description: Diagnose BuddyHub runtime, text UI mode, and cleanup state
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" doctor`

Present the command output directly to the user.
- Preserve headings, bullets, booleans, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not suggest commands that are not present in the output.
- Do not call any additional tools.

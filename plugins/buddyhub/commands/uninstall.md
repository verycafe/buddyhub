---
description: Clean up BuddyHub native patch artifacts and remove the plugin safely
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" uninstall`

Present the command output directly to the user.
- Preserve headings, bullets, JSON, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not run any additional cleanup steps or tool calls beyond this command.

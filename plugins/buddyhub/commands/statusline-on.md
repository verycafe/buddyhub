---
description: Request BuddyHub status line mode and show the status line script path
model: haiku
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/buddyhub.py" statusline-on`

Present the command output directly to the user.
- Preserve headings, bullets, file paths, and code formatting.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not inspect files or attempt to edit Claude Code settings yourself.
- Do not call any additional tools.

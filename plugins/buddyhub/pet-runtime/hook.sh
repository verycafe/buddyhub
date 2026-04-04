#!/bin/bash
# Claude Code Hook: writes pet state based on tool usage
# Install: add to Claude Code hooks in settings.json

STATE_FILE="$HOME/.claude/pet/state.json"
mkdir -p "$(dirname "$STATE_FILE")"

write_state() {
    local state="$1"
    local activity="$2"
    local tool="${CLAUDE_TOOL_NAME:-unknown}"
    cat > "$STATE_FILE" << EOF
{"state":"$state","tool":"$tool","activity":"$activity","timestamp":$(date +%s)}
EOF
}

EVENT="${CLAUDE_HOOK_EVENT:-}"

case "$EVENT" in
    SessionStart)
        write_state "waking" "waking up"
        ;;
    UserPromptSubmit)
        write_state "listening" "listening closely"
        ;;
    PreToolUse)
        case "$CLAUDE_TOOL_NAME" in
            Read|Glob|Grep)          write_state "studying" "studying the codebase" ;;
            Edit|Write|NotebookEdit) write_state "coding" "making changes" ;;
            Bash)                    write_state "debugging" "working in the terminal" ;;
            WebFetch|WebSearch)      write_state "researching" "researching context" ;;
            AskUserQuestion)         write_state "waiting" "waiting on you" ;;
            Task)                    write_state "exploring" "exploring a task" ;;
            *)                       write_state "thinking" "thinking through next steps" ;;
        esac
        ;;
    PostToolUse)
        write_state "coffee" "taking a coffee break"
        ;;
    Stop)
        write_state "celebrating" "celebrating a finished step"
        ;;
    Notification)
        write_state "waiting" "waiting on you"
        ;;
    SessionEnd)
        write_state "sleeping" "curling up for a nap"
        ;;
esac

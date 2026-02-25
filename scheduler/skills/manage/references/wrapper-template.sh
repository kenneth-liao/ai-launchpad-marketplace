#!/bin/bash
set -euo pipefail

# --- Config (injected by scheduler.py) ---
TASK_ID="{id}"
TASK_TYPE="{type}"
TASK_TARGET='{target}'
MAX_TURNS={max_turns}
TIMEOUT_MINUTES={timeout_minutes}
WORKDIR="{working_directory}"

# --- Environment ---
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Optional: load API key if available (not required for subscription auth)
API_KEY="$(security find-generic-password -s 'anthropic-api-key' -w 2>/dev/null || echo '')"
if [ -n "$API_KEY" ]; then
  export ANTHROPIC_API_KEY="$API_KEY"
fi

# --- Paths ---
DATE=$(date '+%Y-%m-%d')
RESULT_DIR="$HOME/.claude/scheduler/results/$DATE"
LOG_FILE="$HOME/.claude/scheduler/logs/$DATE-$TASK_ID.log"
RESULT_FILE="$RESULT_DIR/$TASK_ID.md"
mkdir -p "$RESULT_DIR" "$(dirname "$LOG_FILE")"

# --- Execute ---
START_TIME=$(date +%s)
echo "=== $TASK_ID started at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

cd "$WORKDIR"

EXIT_CODE=0
case "$TASK_TYPE" in
  skill)
    timeout "${TIMEOUT_MINUTES}m" claude -p "/$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
  prompt)
    timeout "${TIMEOUT_MINUTES}m" claude -p "$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
  script)
    timeout "${TIMEOUT_MINUTES}m" bash "$TASK_TARGET" \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
esac

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# --- Log ---
echo "=== Completed: exit=$EXIT_CODE duration=${DURATION}s ===" >> "$LOG_FILE"

# --- Notify ---
if [ $EXIT_CODE -eq 0 ]; then
  osascript -e "display notification \"Completed in ${DURATION}s\" with title \"Scheduler: $TASK_ID\" sound name \"Glass\""
else
  osascript -e "display notification \"Failed (exit $EXIT_CODE). Check logs.\" with title \"Scheduler: $TASK_ID\" sound name \"Basso\""
fi

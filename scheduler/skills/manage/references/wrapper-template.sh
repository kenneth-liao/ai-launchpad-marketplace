#!/bin/bash
set -euo pipefail

# --- Config (injected by scheduler.py) ---
TASK_ID="{id}"
TASK_TYPE="{type}"
TASK_TARGET='{target}'
MAX_TURNS={max_turns}
TIMEOUT_MINUTES={timeout_minutes}
WORKDIR="{working_directory}"
RUN_ONCE="{run_once}"
SCHEDULER_PY="{scheduler_py}"

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
LOCK_FILE="$HOME/.claude/scheduler/.lock-$TASK_ID"
mkdir -p "$RESULT_DIR" "$(dirname "$LOG_FILE")"

# --- Lock: skip if already running ---
if [ -f "$LOCK_FILE" ]; then
  LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
  if [ -n "$LOCK_PID" ] && kill -0 "$LOCK_PID" 2>/dev/null; then
    echo "[$(date '+%H:%M:%S')] SKIPPED — previous run (pid $LOCK_PID) still active" >> "$LOG_FILE"
    exit 0
  fi
  # Stale lock — previous run died without cleanup
  rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# --- Timeout helper (macOS-compatible, no GNU coreutils needed) ---
run_with_timeout() {
  local timeout_secs=$1
  shift
  "$@" &
  local pid=$!
  ( sleep "$timeout_secs" && kill -TERM "$pid" 2>/dev/null ) &
  local watchdog=$!
  wait "$pid" 2>/dev/null
  local exit_code=$?
  kill "$watchdog" 2>/dev/null
  wait "$watchdog" 2>/dev/null
  return $exit_code
}

TIMEOUT_SECONDS=$((TIMEOUT_MINUTES * 60))

# --- Logging helper ---
log() { echo "[$(date '+%H:%M:%S')] $*" >> "$LOG_FILE"; }

# --- Execute ---
START_TIME=$(date +%s)
log "START  task=$TASK_ID type=$TASK_TYPE turns=$MAX_TURNS timeout=${TIMEOUT_MINUTES}m"
log "TARGET ${TASK_TARGET:0:120}$([ ${#TASK_TARGET} -gt 120 ] && echo '...')"

cd "$WORKDIR"

EXIT_CODE=0
case "$TASK_TYPE" in
  skill)
    run_with_timeout "$TIMEOUT_SECONDS" claude -p "/$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
  prompt)
    run_with_timeout "$TIMEOUT_SECONDS" claude -p "$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
  script)
    run_with_timeout "$TIMEOUT_SECONDS" bash "$TASK_TARGET" \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
esac

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
RESULT_BYTES=$(wc -c < "$RESULT_FILE" 2>/dev/null | tr -d ' ')
RESULT_LINES=$(wc -l < "$RESULT_FILE" 2>/dev/null | tr -d ' ')

# --- Log summary ---
if [ $EXIT_CODE -eq 0 ]; then
  log "DONE   exit=0 duration=${DURATION}s result=${RESULT_BYTES}B/${RESULT_LINES}L"
  # Log first 3 non-empty lines as preview
  PREVIEW=$(grep -m3 '.' "$RESULT_FILE" 2>/dev/null | head -c 300 || echo "(empty)")
  log "PREVIEW $PREVIEW"
else
  log "FAIL   exit=$EXIT_CODE duration=${DURATION}s result=${RESULT_BYTES}B"
fi

# --- Notify ---
if [ $EXIT_CODE -eq 0 ]; then
  osascript -e "display notification \"Completed in ${DURATION}s (${RESULT_LINES} lines)\" with title \"Scheduler: $TASK_ID\" sound name \"Glass\""
else
  osascript -e "display notification \"Failed (exit $EXIT_CODE). Check logs.\" with title \"Scheduler: $TASK_ID\" sound name \"Basso\""
fi

# --- One-off: self-complete after successful run ---
if [ "$RUN_ONCE" = "true" ] && [ $EXIT_CODE -eq 0 ]; then
  log "RUN_ONCE — marking task as completed"
  uv run "$SCHEDULER_PY" complete --id "$TASK_ID" >> "$LOG_FILE" 2>&1 || true
fi

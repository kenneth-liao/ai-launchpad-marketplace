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
ALLOWED_TOOLS='{allowed_tools}'
PERMISSION_MODE='{permission_mode}'
SKIP_PERMISSIONS='{skip_permissions}'

# --- Environment ---
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"

# Optional: load API key if available (not required for subscription auth)
# Try secret-tool (GNOME Keyring) first, then file fallback
API_KEY="$(secret-tool lookup service anthropic-api-key 2>/dev/null || echo '')"
if [ -z "$API_KEY" ] && [ -f "$HOME/.config/anthropic/api-key" ]; then
  API_KEY="$(cat "$HOME/.config/anthropic/api-key" 2>/dev/null || echo '')"
fi
if [ -n "$API_KEY" ]; then
  export ANTHROPIC_API_KEY="$API_KEY"
fi

# --- Paths ---
SCHEDULER_DIR="{scheduler_dir}"
OUTPUT_DIR="{output_directory}"

DATE=$(date '+%Y-%m-%d')
TIMESTAMP=$(date '+%H%M%S')
if [ -n "$OUTPUT_DIR" ]; then
  RESULT_DIR="$OUTPUT_DIR"
  RESULT_FILE="$RESULT_DIR/$TASK_ID.md"
else
  RESULT_DIR="$SCHEDULER_DIR/results/$DATE"
  RESULT_FILE="$RESULT_DIR/$TASK_ID-$TIMESTAMP.md"
fi
LOG_FILE="$SCHEDULER_DIR/logs/$DATE-$TASK_ID.log"
LOCK_FILE="$SCHEDULER_DIR/.lock-$TASK_ID"
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

# --- Timeout helper ---
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

# --- Permission flags ---
PERM_ARGS=()
if [ "$SKIP_PERMISSIONS" = "true" ]; then
  PERM_ARGS+=(--dangerously-skip-permissions)
elif [ -n "$PERMISSION_MODE" ]; then
  PERM_ARGS+=(--permission-mode "$PERMISSION_MODE")
fi
if [ -n "$ALLOWED_TOOLS" ]; then
  PERM_ARGS+=(--allowedTools "$ALLOWED_TOOLS")
fi

# --- Logging helper ---
log() { echo "[$(date '+%H:%M:%S')] $*" >> "$LOG_FILE"; }

# --- Execute ---
START_TIME=$(date +%s)
log "START  task=$TASK_ID type=$TASK_TYPE turns=$MAX_TURNS timeout=${TIMEOUT_MINUTES}m perms=${#PERM_ARGS[@]}flags"
log "TARGET ${TASK_TARGET:0:120}$([ ${#TASK_TARGET} -gt 120 ] && echo '...')"

cd "$WORKDIR"

EXIT_CODE=0
case "$TASK_TYPE" in
  skill)
    run_with_timeout "$TIMEOUT_SECONDS" claude -p "/$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text "${PERM_ARGS[@]}" \
      > "$RESULT_FILE" 2>> "$LOG_FILE" || EXIT_CODE=$?
    ;;
  prompt)
    run_with_timeout "$TIMEOUT_SECONDS" claude -p "$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text "${PERM_ARGS[@]}" \
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

# --- Update registry with run results ---
log "UPDATE update-last-run exit=$EXIT_CODE duration=${DURATION}s"
uv run "$SCHEDULER_PY" update-last-run \
  --id "$TASK_ID" \
  --exit-code $EXIT_CODE \
  --duration $DURATION \
  --result-file "$RESULT_FILE" >> "$LOG_FILE" 2>&1 || true

# --- Notify ---
if [ $EXIT_CODE -eq 0 ]; then
  notify-send "Scheduler: $TASK_ID" "Completed in ${DURATION}s (${RESULT_LINES} lines)" 2>/dev/null || true
else
  notify-send -u critical "Scheduler: $TASK_ID" "Failed (exit $EXIT_CODE). Check logs." 2>/dev/null || true
fi

# --- One-off: self-complete after successful run ---
if [ "$RUN_ONCE" = "true" ] && [ $EXIT_CODE -eq 0 ]; then
  log "RUN_ONCE — marking task as completed"
  uv run "$SCHEDULER_PY" complete --id "$TASK_ID" >> "$LOG_FILE" 2>&1 || true
fi

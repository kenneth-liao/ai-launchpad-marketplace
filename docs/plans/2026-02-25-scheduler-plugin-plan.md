# Scheduler Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a `scheduler` plugin that manages launchd-based scheduled tasks (skills, prompts, scripts) through a conversational Claude Code skill.

**Architecture:** A new `scheduler/` plugin with one orchestrator skill (`scheduler:manage`) backed by a PEP 723 Python engine (`scheduler.py`) that manages a JSON task registry, generates per-task wrapper shell scripts and launchd plist files, and interacts with `launchctl` for lifecycle management.

**Tech Stack:** Python 3.10+ (via `uv run`), `croniter` for cron parsing, `argparse` for CLI, macOS `launchd`/`launchctl`, bash wrapper scripts, `osascript` for notifications.

**Design Doc:** `docs/plans/2026-02-25-scheduler-plugin-design.md`

---

## Task 1: Plugin Scaffolding

**Files:**
- Create: `scheduler/.claude-plugin/plugin.json`
- Create: `scheduler/README.md`
- Create: `scheduler/skills/manage/SKILL.md` (placeholder)
- Create: `scheduler/skills/manage/scripts/scheduler.py` (placeholder)
- Create: `scheduler/skills/manage/references/wrapper-template.sh`
- Modify: `.claude-plugin/marketplace.json` — add scheduler entry

**Step 1: Create plugin directory structure**

```bash
mkdir -p scheduler/.claude-plugin
mkdir -p scheduler/skills/manage/scripts
mkdir -p scheduler/skills/manage/references
```

**Step 2: Create plugin.json**

Create `scheduler/.claude-plugin/plugin.json`:

```json
{
  "name": "scheduler",
  "description": "A plugin for scheduling automated Claude Code tasks — manages launchd-based recurring execution of skills, prompts, and scripts with safety controls and notifications",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

**Step 3: Create README.md**

Create `scheduler/README.md`:

```markdown
# Scheduler Plugin

Schedule automated Claude Code tasks using macOS launchd. Manage recurring execution of marketplace skills, freeform prompts, and shell scripts with safety controls and desktop notifications.

## Skills

### manage

Conversational orchestrator for scheduling tasks. Invoke via `/schedule`.

**Operations:**
- Add a new scheduled task (skill, prompt, or script)
- List all scheduled tasks
- Pause/resume a task
- Remove a task
- View results from a task
- View logs for a task
- Run a task now (test)

## How It Works

1. Tasks are defined in a JSON registry at `~/.claude/scheduler/registry.json`
2. Each task gets a wrapper shell script at `~/.claude/scheduler/wrappers/{id}.sh`
3. Each task gets a launchd plist at `~/Library/LaunchAgents/com.ailaunchpad.scheduler.{id}.plist`
4. launchd fires the wrapper at the scheduled time
5. The wrapper runs `claude -p` (for skills/prompts) or `bash` (for scripts)
6. Results saved to `~/.claude/scheduler/results/YYYY-MM-DD/{id}.md`
7. Desktop notification on completion or failure

## Requirements

- macOS (uses launchd)
- Claude Code CLI (`claude` in PATH)
- `uv` for running the Python engine
```

**Step 4: Create placeholder SKILL.md**

Create `scheduler/skills/manage/SKILL.md` with just the frontmatter for now:

```markdown
---
name: manage
description: Manage scheduled Claude Code tasks — add, list, pause, resume, remove, view results, and test launchd-based recurring execution of skills, prompts, and scripts. Invoke via /schedule.
---

# Scheduler — placeholder (will be replaced in Task 5)
```

**Step 5: Create placeholder scheduler.py**

Create `scheduler/skills/manage/scripts/scheduler.py`:

```python
#!/usr/bin/env python3
"""Scheduler engine — placeholder (will be replaced in Task 2)."""
print("scheduler.py placeholder")
```

**Step 6: Create wrapper-template.sh**

Create `scheduler/skills/manage/references/wrapper-template.sh` with the full template from the design doc. Use literal `{id}`, `{type}`, `{target}`, `{max_turns}`, `{timeout_minutes}`, `{working_directory}` as placeholders that `scheduler.py` will string-replace:

```bash
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
```

Note: The `TASK_TARGET` uses single quotes in the template so prompts with double quotes don't break. The Python engine must handle proper escaping when substituting.

**Step 7: Add to marketplace.json**

Add to the `plugins` array in `.claude-plugin/marketplace.json`:

```json
{
  "name": "scheduler",
  "source": "./scheduler",
  "description": "A plugin for scheduling automated Claude Code tasks using macOS launchd"
}
```

**Step 8: Commit**

```bash
git add scheduler/ .claude-plugin/marketplace.json
git commit -m "feat(scheduler): scaffold plugin structure with wrapper template"
```

---

## Task 2: Python Engine — Registry CRUD

**Files:**
- Create: `scheduler/skills/manage/scripts/scheduler.py` (replace placeholder)
- Test: `.tests/test_scheduler_registry.py`

This task implements the registry management: `add`, `list`, `get`, `remove`, and `update-last-run` — everything except launchd interaction (Task 3) and plist/wrapper generation (Task 3).

**Step 1: Write tests for registry operations**

Create `.tests/test_scheduler_registry.py`:

```python
"""Tests for scheduler.py registry CRUD operations."""
import json
import subprocess
import tempfile
import os
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scheduler" / "skills" / "manage" / "scripts" / "scheduler.py")


def run_scheduler(*args, scheduler_dir=None, env_extra=None):
    """Run scheduler.py with args, return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    if scheduler_dir:
        env["SCHEDULER_DIR"] = str(scheduler_dir)
    # Skip launchctl calls in tests
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    if env_extra:
        env.update(env_extra)
    result = subprocess.run(
        ["uv", "run", SCRIPT] + list(args),
        capture_output=True, text=True, env=env
    )
    return result.stdout, result.stderr, result.returncode


def test_list_empty():
    """List with no tasks returns empty array."""
    with tempfile.TemporaryDirectory() as d:
        stdout, _, rc = run_scheduler("list", scheduler_dir=d)
        assert rc == 0
        data = json.loads(stdout)
        assert data == []


def test_add_and_list():
    """Add a task, then list it."""
    with tempfile.TemporaryDirectory() as d:
        _, _, rc = run_scheduler(
            "add", "--id", "test-task", "--name", "Test Task",
            "--type", "prompt", "--target", "Hello world",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        assert rc == 0

        stdout, _, rc = run_scheduler("list", scheduler_dir=d)
        assert rc == 0
        tasks = json.loads(stdout)
        assert len(tasks) == 1
        assert tasks[0]["id"] == "test-task"
        assert tasks[0]["status"] == "active"


def test_add_duplicate_id_fails():
    """Adding a task with an existing ID fails."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "dupe", "--name", "First",
            "--type", "prompt", "--target", "test",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        _, stderr, rc = run_scheduler(
            "add", "--id", "dupe", "--name", "Second",
            "--type", "prompt", "--target", "test2",
            "--cron", "0 10 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        assert rc != 0
        assert "already exists" in stderr.lower()


def test_add_invalid_cron_fails():
    """Adding a task with invalid cron expression fails."""
    with tempfile.TemporaryDirectory() as d:
        _, stderr, rc = run_scheduler(
            "add", "--id", "bad-cron", "--name", "Bad Cron",
            "--type", "prompt", "--target", "test",
            "--cron", "not-a-cron", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        assert rc != 0
        assert "cron" in stderr.lower() or "invalid" in stderr.lower()


def test_get_existing():
    """Get a specific task by ID."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "my-task", "--name", "My Task",
            "--type", "skill", "--target", "substack:generate-note-ideas",
            "--cron", "0 8 * * 1", "--max-turns", "20",
            "--timeout", "15", "--workdir", "/tmp",
            scheduler_dir=d
        )
        stdout, _, rc = run_scheduler("get", "--id", "my-task", scheduler_dir=d)
        assert rc == 0
        task = json.loads(stdout)
        assert task["id"] == "my-task"
        assert task["type"] == "skill"
        assert task["target"] == "substack:generate-note-ideas"
        assert task["schedule"]["cron"] == "0 8 * * 1"
        assert task["safety"]["max_turns"] == 20


def test_get_nonexistent_fails():
    """Get a non-existent task fails."""
    with tempfile.TemporaryDirectory() as d:
        _, stderr, rc = run_scheduler("get", "--id", "nope", scheduler_dir=d)
        assert rc != 0
        assert "not found" in stderr.lower()


def test_remove():
    """Remove deletes task from registry."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "rm-me", "--name", "Remove Me",
            "--type", "prompt", "--target", "test",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        _, _, rc = run_scheduler("remove", "--id", "rm-me", scheduler_dir=d)
        assert rc == 0

        stdout, _, _ = run_scheduler("list", scheduler_dir=d)
        tasks = json.loads(stdout)
        assert len(tasks) == 0


def test_remove_nonexistent_fails():
    """Remove a non-existent task fails."""
    with tempfile.TemporaryDirectory() as d:
        _, stderr, rc = run_scheduler("remove", "--id", "nope", scheduler_dir=d)
        assert rc != 0


def test_update_last_run():
    """update-last-run updates the task's last_run field."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "update-me", "--name", "Update Me",
            "--type", "prompt", "--target", "test",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        _, _, rc = run_scheduler(
            "update-last-run", "--id", "update-me",
            "--exit-code", "0", "--duration", "42",
            "--result-file", "/tmp/result.md",
            scheduler_dir=d
        )
        assert rc == 0

        stdout, _, _ = run_scheduler("get", "--id", "update-me", scheduler_dir=d)
        task = json.loads(stdout)
        assert task["last_run"]["exit_code"] == 0
        assert task["last_run"]["duration_seconds"] == 42


def test_add_all_three_types():
    """Can add skill, prompt, and script type tasks."""
    with tempfile.TemporaryDirectory() as d:
        for task_type, target in [
            ("skill", "substack:create-note"),
            ("prompt", "Summarize my YouTube comments"),
            ("script", "/tmp/test.sh"),
        ]:
            _, _, rc = run_scheduler(
                "add", "--id", f"type-{task_type}", "--name", f"Type {task_type}",
                "--type", task_type, "--target", target,
                "--cron", "0 9 * * *", "--max-turns", "10",
                "--timeout", "5", "--workdir", "/tmp",
                scheduler_dir=d
            )
            assert rc == 0, f"Failed to add {task_type} task"

        stdout, _, _ = run_scheduler("list", scheduler_dir=d)
        tasks = json.loads(stdout)
        assert len(tasks) == 3
```

**Step 2: Run tests to verify they fail**

```bash
cd /Users/kennethliao/projects/ai-launchpad-marketplace
uv run pytest .tests/test_scheduler_registry.py -v
```

Expected: FAIL — scheduler.py is a placeholder.

**Step 3: Implement scheduler.py — registry CRUD**

Replace `scheduler/skills/manage/scripts/scheduler.py` with the full implementation. Key structure:

```python
#!/usr/bin/env python3
"""
Scheduler Engine — manages launchd-based scheduled tasks for Claude Code.

Usage:
    uv run scheduler.py add --id ID --name NAME --type TYPE --target TARGET ...
    uv run scheduler.py list
    uv run scheduler.py get --id ID
    uv run scheduler.py remove --id ID
    uv run scheduler.py pause --id ID
    uv run scheduler.py resume --id ID
    uv run scheduler.py run --id ID
    uv run scheduler.py logs --id ID
    uv run scheduler.py results --id ID [--all]
    uv run scheduler.py update-last-run --id ID --exit-code N --duration S --result-file PATH
    uv run scheduler.py repair
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "croniter>=2.0.0",
# ]
# ///

import argparse
import json
import os
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from croniter import croniter


# --- Paths ---

def get_scheduler_dir() -> Path:
    """Return scheduler data directory. Override with SCHEDULER_DIR env var for testing."""
    return Path(os.environ.get("SCHEDULER_DIR", Path.home() / ".claude" / "scheduler"))


def get_launch_agents_dir() -> Path:
    return Path.home() / "Library" / "LaunchAgents"


def get_registry_path() -> Path:
    return get_scheduler_dir() / "registry.json"


PLIST_PREFIX = "com.ailaunchpad.scheduler"


# --- Registry ---

def load_registry() -> dict:
    path = get_registry_path()
    if not path.exists():
        return {"version": 1, "tasks": {}}
    with open(path) as f:
        return json.load(f)


def save_registry(registry: dict):
    path = get_registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(registry, f, indent=2)


# --- Cron Helpers ---

def validate_cron(expr: str) -> bool:
    try:
        croniter(expr)
        return True
    except (ValueError, KeyError):
        return False


def humanize_cron(expr: str) -> str:
    """Return a human-readable description of a cron expression."""
    # Basic humanization for common patterns
    parts = expr.split()
    if len(parts) != 5:
        return expr

    minute, hour, dom, month, dow = parts
    days = {
        "0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday",
        "4": "Thursday", "5": "Friday", "6": "Saturday", "7": "Sunday",
    }

    time_str = f"{int(hour)}:{minute.zfill(2)} AM" if int(hour) < 12 else f"{int(hour)-12 if int(hour) > 12 else 12}:{minute.zfill(2)} PM"
    if int(hour) == 0:
        time_str = f"12:{minute.zfill(2)} AM"

    if dow != "*" and dom == "*" and month == "*":
        if "," in dow:
            day_names = [days.get(d, d) for d in dow.split(",")]
            return f"Every {', '.join(day_names)} at {time_str}"
        if "-" in dow:
            start, end = dow.split("-")
            return f"Every {days.get(start, start)}-{days.get(end, end)} at {time_str}"
        return f"Every {days.get(dow, dow)} at {time_str}"

    if dow == "*" and dom == "*" and month == "*":
        return f"Every day at {time_str}"

    return expr  # fallback


def next_run_str(expr: str) -> str:
    """Return the next run time as a human-readable string."""
    cron = croniter(expr, datetime.now())
    next_dt = cron.get_next(datetime)
    return next_dt.strftime("%A %B %-d at %-I:%M %p")


# --- Commands ---

def cmd_add(args):
    if not validate_cron(args.cron):
        print(f"Error: Invalid cron expression: {args.cron}", file=sys.stderr)
        sys.exit(1)

    registry = load_registry()
    if args.id in registry["tasks"]:
        print(f"Error: Task '{args.id}' already exists. Choose a different ID.", file=sys.stderr)
        sys.exit(1)

    if args.type not in ("skill", "prompt", "script"):
        print(f"Error: Invalid type '{args.type}'. Must be skill, prompt, or script.", file=sys.stderr)
        sys.exit(1)

    task = {
        "id": args.id,
        "name": args.name,
        "type": args.type,
        "target": args.target,
        "working_directory": args.workdir,
        "schedule": {
            "cron": args.cron,
            "human": humanize_cron(args.cron),
        },
        "safety": {
            "max_turns": int(args.max_turns),
            "timeout_minutes": int(args.timeout),
        },
        "status": "active",
        "created_at": datetime.now().astimezone().isoformat(),
        "last_run": None,
    }

    registry["tasks"][args.id] = task
    save_registry(registry)

    # Generate wrapper and plist (Task 3 will implement these)
    generate_wrapper(task)
    generate_plist(task)
    launchctl_load(args.id)

    print(json.dumps(task, indent=2))


def cmd_list(args):
    registry = load_registry()
    tasks = list(registry["tasks"].values())
    print(json.dumps(tasks, indent=2))


def cmd_get(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(registry["tasks"][args.id], indent=2))


def cmd_remove(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    launchctl_unload(args.id)
    delete_plist(args.id)
    delete_wrapper(args.id)

    del registry["tasks"][args.id]
    save_registry(registry)
    print(json.dumps({"removed": args.id}))


def cmd_pause(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)
    if registry["tasks"][args.id]["status"] == "paused":
        print(f"Task '{args.id}' is already paused.", file=sys.stderr)
        sys.exit(1)

    launchctl_unload(args.id)
    registry["tasks"][args.id]["status"] = "paused"
    save_registry(registry)
    print(json.dumps({"paused": args.id}))


def cmd_resume(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)
    if registry["tasks"][args.id]["status"] == "active":
        print(f"Task '{args.id}' is already active.", file=sys.stderr)
        sys.exit(1)

    launchctl_load(args.id)
    registry["tasks"][args.id]["status"] = "active"
    save_registry(registry)
    print(json.dumps({"resumed": args.id}))


def cmd_run(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    wrapper = get_scheduler_dir() / "wrappers" / f"{args.id}.sh"
    if not wrapper.exists():
        print(f"Error: Wrapper script not found at {wrapper}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(["bash", str(wrapper)], capture_output=False)
    sys.exit(result.returncode)


def cmd_logs(args):
    log_dir = get_scheduler_dir() / "logs"
    if not log_dir.exists():
        print("No logs found.")
        return

    # Find all log files for this task, sorted newest first
    log_files = sorted(log_dir.glob(f"*-{args.id}.log"), reverse=True)
    if not log_files:
        print(f"No logs found for task '{args.id}'.")
        return

    # Show the 3 most recent log files
    for log_file in log_files[:3]:
        print(f"--- {log_file.name} ---")
        print(log_file.read_text())
        print()


def cmd_results(args):
    results_dir = get_scheduler_dir() / "results"
    if not results_dir.exists():
        print(f"No results found for task '{args.id}'.")
        return

    # Find all result files for this task
    result_files = []
    for date_dir in sorted(results_dir.iterdir(), reverse=True):
        if date_dir.is_dir():
            result_file = date_dir / f"{args.id}.md"
            if result_file.exists():
                result_files.append(result_file)

    if not result_files:
        print(f"No results found for task '{args.id}'.")
        return

    if hasattr(args, 'all') and args.all:
        # List all result files
        for rf in result_files:
            print(rf)
    else:
        # Show latest result
        print(result_files[0].read_text())


def cmd_update_last_run(args):
    registry = load_registry()
    if args.id not in registry["tasks"]:
        print(f"Error: Task '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    registry["tasks"][args.id]["last_run"] = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "exit_code": int(args.exit_code),
        "duration_seconds": int(args.duration),
        "result_file": args.result_file,
    }

    # Update status to error if exit code is non-zero
    if int(args.exit_code) != 0:
        registry["tasks"][args.id]["status"] = "error"

    save_registry(registry)
    print(json.dumps(registry["tasks"][args.id]["last_run"]))


def cmd_repair(args):
    registry = load_registry()
    repaired = []

    for task_id, task in registry["tasks"].items():
        if task["status"] != "active":
            continue

        plist_path = get_launch_agents_dir() / f"{PLIST_PREFIX}.{task_id}.plist"
        wrapper_path = get_scheduler_dir() / "wrappers" / f"{task_id}.sh"

        if not wrapper_path.exists():
            generate_wrapper(task)
            repaired.append(f"Regenerated wrapper for '{task_id}'")

        if not plist_path.exists():
            generate_plist(task)
            launchctl_load(task_id)
            repaired.append(f"Regenerated plist for '{task_id}'")

    if repaired:
        for msg in repaired:
            print(msg)
    else:
        print("All tasks OK. Nothing to repair.")


# --- File Generation ---

def generate_wrapper(task: dict):
    """Generate a wrapper shell script from the template."""
    template_path = Path(__file__).parent.parent / "references" / "wrapper-template.sh"
    template = template_path.read_text()

    # Escape single quotes in target for bash safety
    escaped_target = task["target"].replace("'", "'\\''")

    wrapper = template.replace("{id}", task["id"])
    wrapper = wrapper.replace("{type}", task["type"])
    wrapper = wrapper.replace("{target}", escaped_target)
    wrapper = wrapper.replace("{max_turns}", str(task["safety"]["max_turns"]))
    wrapper = wrapper.replace("{timeout_minutes}", str(task["safety"]["timeout_minutes"]))
    wrapper = wrapper.replace("{working_directory}", task["working_directory"])

    wrapper_path = get_scheduler_dir() / "wrappers" / f"{task['id']}.sh"
    wrapper_path.parent.mkdir(parents=True, exist_ok=True)
    wrapper_path.write_text(wrapper)
    wrapper_path.chmod(wrapper_path.stat().st_mode | stat.S_IEXEC)


def generate_plist(task: dict):
    """Generate a launchd plist file for the task."""
    cron_parts = task["schedule"]["cron"].split()
    minute, hour, dom, month, dow = cron_parts

    # Build StartCalendarInterval
    calendar_interval = ""

    if dow != "*":
        # Day of week specified — may be single, comma-separated, or range
        dow_values = []
        if "," in dow:
            dow_values = [int(d) for d in dow.split(",")]
        elif "-" in dow:
            start, end = dow.split("-")
            dow_values = list(range(int(start), int(end) + 1))
        else:
            dow_values = [int(dow)]

        if len(dow_values) == 1:
            calendar_interval = f"""    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key><integer>{dow_values[0]}</integer>
        <key>Hour</key><integer>{int(hour)}</integer>
        <key>Minute</key><integer>{int(minute)}</integer>
    </dict>"""
        else:
            entries = []
            for d in dow_values:
                entries.append(f"""        <dict>
            <key>Weekday</key><integer>{d}</integer>
            <key>Hour</key><integer>{int(hour)}</integer>
            <key>Minute</key><integer>{int(minute)}</integer>
        </dict>""")
            calendar_interval = f"""    <key>StartCalendarInterval</key>
    <array>
{chr(10).join(entries)}
    </array>"""
    else:
        # No day-of-week — just hour and minute (every day)
        interval_dict = []
        if month != "*":
            interval_dict.append(f"        <key>Month</key><integer>{int(month)}</integer>")
        if dom != "*":
            interval_dict.append(f"        <key>Day</key><integer>{int(dom)}</integer>")
        if hour != "*":
            interval_dict.append(f"        <key>Hour</key><integer>{int(hour)}</integer>")
        if minute != "*":
            interval_dict.append(f"        <key>Minute</key><integer>{int(minute)}</integer>")

        calendar_interval = f"""    <key>StartCalendarInterval</key>
    <dict>
{chr(10).join(interval_dict)}
    </dict>"""

    wrapper_path = get_scheduler_dir() / "wrappers" / f"{task['id']}.sh"
    log_prefix = get_scheduler_dir() / "logs"
    label = f"{PLIST_PREFIX}.{task['id']}"

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>{wrapper_path}</string>
    </array>
{calendar_interval}
    <key>StandardOutPath</key>
    <string>{log_prefix}/{task['id']}.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{log_prefix}/{task['id']}.stderr.log</string>
</dict>
</plist>
"""

    plist_path = get_launch_agents_dir() / f"{label}.plist"
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    plist_path.write_text(plist)


def delete_plist(task_id: str):
    plist_path = get_launch_agents_dir() / f"{PLIST_PREFIX}.{task_id}.plist"
    if plist_path.exists():
        plist_path.unlink()


def delete_wrapper(task_id: str):
    wrapper_path = get_scheduler_dir() / "wrappers" / f"{task_id}.sh"
    if wrapper_path.exists():
        wrapper_path.unlink()


# --- launchctl ---

def skip_launchctl() -> bool:
    return os.environ.get("SCHEDULER_SKIP_LAUNCHCTL") == "1"


def get_uid() -> int:
    return os.getuid()


def launchctl_load(task_id: str):
    if skip_launchctl():
        return
    label = f"{PLIST_PREFIX}.{task_id}"
    plist_path = get_launch_agents_dir() / f"{label}.plist"
    try:
        subprocess.run(
            ["launchctl", "bootstrap", f"gui/{get_uid()}", str(plist_path)],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        # May already be loaded — try legacy load
        subprocess.run(
            ["launchctl", "load", str(plist_path)],
            capture_output=True, text=True
        )


def launchctl_unload(task_id: str):
    if skip_launchctl():
        return
    label = f"{PLIST_PREFIX}.{task_id}"
    try:
        subprocess.run(
            ["launchctl", "bootout", f"gui/{get_uid()}/{label}"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        # May not be loaded — try legacy unload
        plist_path = get_launch_agents_dir() / f"{label}.plist"
        subprocess.run(
            ["launchctl", "unload", str(plist_path)],
            capture_output=True, text=True
        )


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Scheduler engine for Claude Code tasks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = subparsers.add_parser("add", help="Add a new scheduled task")
    p_add.add_argument("--id", required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--type", required=True, choices=["skill", "prompt", "script"])
    p_add.add_argument("--target", required=True)
    p_add.add_argument("--cron", required=True)
    p_add.add_argument("--max-turns", default="20")
    p_add.add_argument("--timeout", default="15")
    p_add.add_argument("--workdir", default=str(Path.cwd()))

    # list
    subparsers.add_parser("list", help="List all scheduled tasks")

    # get
    p_get = subparsers.add_parser("get", help="Get a specific task")
    p_get.add_argument("--id", required=True)

    # remove
    p_rm = subparsers.add_parser("remove", help="Remove a scheduled task")
    p_rm.add_argument("--id", required=True)

    # pause
    p_pause = subparsers.add_parser("pause", help="Pause a scheduled task")
    p_pause.add_argument("--id", required=True)

    # resume
    p_resume = subparsers.add_parser("resume", help="Resume a paused task")
    p_resume.add_argument("--id", required=True)

    # run
    p_run = subparsers.add_parser("run", help="Run a task immediately (for testing)")
    p_run.add_argument("--id", required=True)

    # logs
    p_logs = subparsers.add_parser("logs", help="View logs for a task")
    p_logs.add_argument("--id", required=True)

    # results
    p_results = subparsers.add_parser("results", help="View results for a task")
    p_results.add_argument("--id", required=True)
    p_results.add_argument("--all", action="store_true", help="List all result files")

    # update-last-run
    p_ulr = subparsers.add_parser("update-last-run", help="Update last run metadata")
    p_ulr.add_argument("--id", required=True)
    p_ulr.add_argument("--exit-code", required=True)
    p_ulr.add_argument("--duration", required=True)
    p_ulr.add_argument("--result-file", required=True)

    # repair
    subparsers.add_parser("repair", help="Repair missing plists/wrappers")

    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "get": cmd_get,
        "remove": cmd_remove,
        "pause": cmd_pause,
        "resume": cmd_resume,
        "run": cmd_run,
        "logs": cmd_logs,
        "results": cmd_results,
        "update-last-run": cmd_update_last_run,
        "repair": cmd_repair,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

```bash
cd /Users/kennethliao/projects/ai-launchpad-marketplace
uv run pytest .tests/test_scheduler_registry.py -v
```

Expected: All 10 tests PASS.

**Step 5: Commit**

```bash
git add scheduler/skills/manage/scripts/scheduler.py .tests/test_scheduler_registry.py
git commit -m "feat(scheduler): implement Python engine with registry CRUD and launchd management"
```

---

## Task 3: Wrapper + Plist Generation Tests

**Files:**
- Create: `.tests/test_scheduler_generation.py`

This task verifies that the wrapper script and plist generation work correctly. The implementation already exists from Task 2 — this adds dedicated tests.

**Step 1: Write tests for wrapper and plist generation**

Create `.tests/test_scheduler_generation.py`:

```python
"""Tests for wrapper script and plist generation."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scheduler" / "skills" / "manage" / "scripts" / "scheduler.py")


def run_scheduler(*args, scheduler_dir=None):
    env = os.environ.copy()
    if scheduler_dir:
        env["SCHEDULER_DIR"] = str(scheduler_dir)
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    result = subprocess.run(
        ["uv", "run", SCRIPT] + list(args),
        capture_output=True, text=True, env=env
    )
    return result.stdout, result.stderr, result.returncode


def test_wrapper_generated_on_add():
    """Adding a task creates a wrapper script."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "wrap-test", "--name", "Wrapper Test",
            "--type", "prompt", "--target", "Hello world",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        wrapper = Path(d) / "wrappers" / "wrap-test.sh"
        assert wrapper.exists(), "Wrapper script was not created"
        content = wrapper.read_text()
        assert 'TASK_ID="wrap-test"' in content
        assert 'TASK_TYPE="prompt"' in content
        assert "Hello world" in content
        assert "MAX_TURNS=10" in content
        assert "TIMEOUT_MINUTES=5" in content


def test_wrapper_is_executable():
    """Wrapper script has execute permission."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "exec-test", "--name", "Exec Test",
            "--type", "skill", "--target", "substack:create-note",
            "--cron", "0 8 * * 1", "--max-turns", "20",
            "--timeout", "15", "--workdir", "/tmp",
            scheduler_dir=d
        )
        wrapper = Path(d) / "wrappers" / "exec-test.sh"
        assert os.access(wrapper, os.X_OK), "Wrapper is not executable"


def test_wrapper_escapes_single_quotes_in_target():
    """Prompt targets with single quotes are properly escaped."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "quote-test", "--name", "Quote Test",
            "--type", "prompt", "--target", "What's the best strategy?",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        wrapper = Path(d) / "wrappers" / "quote-test.sh"
        content = wrapper.read_text()
        # Should not have unescaped single quote
        assert "What'\\''s" in content or "What's" not in content.split("TASK_TARGET=")[1].split("\n")[0]


def test_plist_generated_on_add():
    """Adding a task creates a plist file."""
    with tempfile.TemporaryDirectory() as d:
        # Override LaunchAgents dir to temp
        run_scheduler(
            "add", "--id", "plist-test", "--name", "Plist Test",
            "--type", "prompt", "--target", "Hello",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        plist = Path.home() / "Library" / "LaunchAgents" / "com.ailaunchpad.scheduler.plist-test.plist"
        assert plist.exists(), f"Plist was not created at {plist}"
        content = plist.read_text()
        assert "com.ailaunchpad.scheduler.plist-test" in content
        assert "<integer>9</integer>" in content  # Hour
        assert "<integer>0</integer>" in content  # Minute
        # Clean up
        plist.unlink()


def test_plist_weekday_schedule():
    """Plist correctly handles weekday cron expressions."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "weekday-test", "--name", "Weekday Test",
            "--type", "prompt", "--target", "Hello",
            "--cron", "30 8 * * 1", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        plist = Path.home() / "Library" / "LaunchAgents" / "com.ailaunchpad.scheduler.weekday-test.plist"
        content = plist.read_text()
        assert "Weekday" in content
        assert "<integer>1</integer>" in content  # Monday
        assert "<integer>8</integer>" in content  # Hour
        assert "<integer>30</integer>" in content  # Minute
        plist.unlink()


def test_remove_deletes_wrapper_and_plist():
    """Remove cleans up wrapper and plist files."""
    with tempfile.TemporaryDirectory() as d:
        run_scheduler(
            "add", "--id", "rm-files-test", "--name", "RM Test",
            "--type", "prompt", "--target", "Hello",
            "--cron", "0 9 * * *", "--max-turns", "10",
            "--timeout", "5", "--workdir", "/tmp",
            scheduler_dir=d
        )
        wrapper = Path(d) / "wrappers" / "rm-files-test.sh"
        plist = Path.home() / "Library" / "LaunchAgents" / "com.ailaunchpad.scheduler.rm-files-test.plist"
        assert wrapper.exists()
        assert plist.exists()

        run_scheduler("remove", "--id", "rm-files-test", scheduler_dir=d)
        assert not wrapper.exists(), "Wrapper was not deleted"
        assert not plist.exists(), "Plist was not deleted"
```

**Step 2: Run tests**

```bash
uv run pytest .tests/test_scheduler_generation.py -v
```

Expected: All PASS. If any fail, fix the generation logic in scheduler.py.

**Step 3: Commit**

```bash
git add .tests/test_scheduler_generation.py
git commit -m "test(scheduler): add wrapper and plist generation tests"
```

---

## Task 4: Pause/Resume and Repair Tests

**Files:**
- Create: `.tests/test_scheduler_lifecycle.py`

**Step 1: Write tests for pause, resume, and repair**

Create `.tests/test_scheduler_lifecycle.py`:

```python
"""Tests for scheduler lifecycle operations: pause, resume, repair."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scheduler" / "skills" / "manage" / "scripts" / "scheduler.py")


def run_scheduler(*args, scheduler_dir=None):
    env = os.environ.copy()
    if scheduler_dir:
        env["SCHEDULER_DIR"] = str(scheduler_dir)
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    result = subprocess.run(
        ["uv", "run", SCRIPT] + list(args),
        capture_output=True, text=True, env=env
    )
    return result.stdout, result.stderr, result.returncode


def add_task(scheduler_dir, task_id="test-task"):
    run_scheduler(
        "add", "--id", task_id, "--name", "Test",
        "--type", "prompt", "--target", "hello",
        "--cron", "0 9 * * *", "--max-turns", "10",
        "--timeout", "5", "--workdir", "/tmp",
        scheduler_dir=scheduler_dir
    )
    # Clean up any generated plists
    plist = Path.home() / "Library" / "LaunchAgents" / f"com.ailaunchpad.scheduler.{task_id}.plist"
    return plist


def cleanup_plist(task_id):
    plist = Path.home() / "Library" / "LaunchAgents" / f"com.ailaunchpad.scheduler.{task_id}.plist"
    if plist.exists():
        plist.unlink()


def test_pause_changes_status():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "pause-test")
        try:
            _, _, rc = run_scheduler("pause", "--id", "pause-test", scheduler_dir=d)
            assert rc == 0
            stdout, _, _ = run_scheduler("get", "--id", "pause-test", scheduler_dir=d)
            task = json.loads(stdout)
            assert task["status"] == "paused"
        finally:
            cleanup_plist("pause-test")


def test_resume_changes_status():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "resume-test")
        try:
            run_scheduler("pause", "--id", "resume-test", scheduler_dir=d)
            _, _, rc = run_scheduler("resume", "--id", "resume-test", scheduler_dir=d)
            assert rc == 0
            stdout, _, _ = run_scheduler("get", "--id", "resume-test", scheduler_dir=d)
            task = json.loads(stdout)
            assert task["status"] == "active"
        finally:
            cleanup_plist("resume-test")


def test_pause_already_paused_fails():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "double-pause")
        try:
            run_scheduler("pause", "--id", "double-pause", scheduler_dir=d)
            _, stderr, rc = run_scheduler("pause", "--id", "double-pause", scheduler_dir=d)
            assert rc != 0
            assert "already paused" in stderr.lower()
        finally:
            cleanup_plist("double-pause")


def test_resume_already_active_fails():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "double-resume")
        try:
            _, stderr, rc = run_scheduler("resume", "--id", "double-resume", scheduler_dir=d)
            assert rc != 0
            assert "already active" in stderr.lower()
        finally:
            cleanup_plist("double-resume")


def test_repair_regenerates_missing_wrapper():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "repair-test")
        try:
            wrapper = Path(d) / "wrappers" / "repair-test.sh"
            assert wrapper.exists()
            wrapper.unlink()
            assert not wrapper.exists()

            stdout, _, rc = run_scheduler("repair", scheduler_dir=d)
            assert rc == 0
            assert wrapper.exists(), "Repair did not regenerate wrapper"
            assert "regenerated wrapper" in stdout.lower()
        finally:
            cleanup_plist("repair-test")


def test_update_last_run_error_sets_status():
    with tempfile.TemporaryDirectory() as d:
        plist = add_task(d, "error-test")
        try:
            run_scheduler(
                "update-last-run", "--id", "error-test",
                "--exit-code", "1", "--duration", "10",
                "--result-file", "/tmp/error.md",
                scheduler_dir=d
            )
            stdout, _, _ = run_scheduler("get", "--id", "error-test", scheduler_dir=d)
            task = json.loads(stdout)
            assert task["status"] == "error"
            assert task["last_run"]["exit_code"] == 1
        finally:
            cleanup_plist("error-test")
```

**Step 2: Run tests**

```bash
uv run pytest .tests/test_scheduler_lifecycle.py -v
```

Expected: All PASS.

**Step 3: Commit**

```bash
git add .tests/test_scheduler_lifecycle.py
git commit -m "test(scheduler): add lifecycle and repair tests"
```

---

## Task 5: SKILL.md — The Orchestrator

**Files:**
- Modify: `scheduler/skills/manage/SKILL.md` (replace placeholder)

**Step 1: Write the full SKILL.md**

Replace `scheduler/skills/manage/SKILL.md`:

```markdown
---
name: manage
description: Manage scheduled Claude Code tasks — add, list, pause, resume, remove, view results, and test launchd-based recurring execution of skills, prompts, and scripts. Invoke via /schedule.
---

# Scheduler

Manage automated, recurring Claude Code tasks using macOS launchd. Schedule marketplace skills, freeform prompts, or shell scripts to run on a cron schedule with safety controls and desktop notifications.

## Overview

This orchestrator manages the full lifecycle of scheduled tasks. It delegates all operations to `scheduler.py` and presents results conversationally.

**Core Principle**: This is a thin orchestrator. All scheduling logic, file generation, and launchctl interaction are handled by `scheduler.py`. This skill manages the conversational flow only.

## When to Use

Use this skill when:
- Scheduling a recurring task (skill, prompt, or script)
- Listing, pausing, resuming, or removing scheduled tasks
- Viewing results or logs from past scheduled runs
- Testing a scheduled task before activating it

## Prerequisites

- macOS (uses launchd for scheduling)
- `claude` CLI in PATH (for skill and prompt tasks)
- `uv` installed (for running scheduler.py)

## First-Time Setup

On first invocation, check if the scheduler directory exists:

```bash
ls ~/.claude/scheduler/registry.json
```

If it does not exist, the first `add` command will create it automatically. No manual setup needed.

## Workflow

When the user invokes `/schedule`, present the operation menu:

1. **Add** a new scheduled task
2. **List** all scheduled tasks
3. **Pause** a task
4. **Resume** a paused task
5. **Remove** a task
6. **Results** — view output from a task
7. **Logs** — view execution logs
8. **Run now** — test a task immediately

Then execute the selected operation below.

### Operation: Add

Walk the user through each field conversationally:

**Step 1: Task name**
Ask: "What should this task be called?"
Generate a slug ID from the name (e.g., "Weekly note ideas" → `weekly-note-ideas`).

**Step 2: Task type**
Ask: "What type of task?"
- **Skill** — invoke a marketplace skill (e.g., `substack:generate-note-ideas`)
- **Prompt** — run a freeform Claude prompt
- **Script** — execute a shell script

**Step 3: Target**
Based on type:
- Skill: Ask which skill. Suggest relevant installed skills if possible.
- Prompt: Ask for the prompt text.
- Script: Ask for the absolute path to the script.

**Step 4: Schedule**
Ask: "What schedule? You can use natural language or a cron expression."
Examples: "Every Monday at 8am", "Daily at 9:00", "Every weekday at 7:30am", "0 8 * * 1"

Convert natural language to a cron expression. Confirm with the user:
"That's `0 8 * * 1` — Every Monday at 8:00 AM. Correct?"

**Step 5: Safety limits**
Ask: "Safety limits? Defaults are max 20 turns, 15 minute timeout."
Let user accept defaults or customize.

**Step 6: Confirm and create**
Present a summary table:

| Field | Value |
|-------|-------|
| ID | weekly-note-ideas |
| Name | Weekly note ideas |
| Type | Skill |
| Target | substack:generate-note-ideas |
| Schedule | Every Monday at 8:00 AM (0 8 * * 1) |
| Max turns | 20 |
| Timeout | 15 min |
| Working dir | {current project directory} |

Ask: "Create this task?"

On confirmation, run:
```bash
uv run <skill_dir>/scripts/scheduler.py add \
  --id "weekly-note-ideas" \
  --name "Weekly note ideas" \
  --type skill \
  --target "substack:generate-note-ideas" \
  --cron "0 8 * * 1" \
  --max-turns 20 \
  --timeout 15 \
  --workdir "{cwd}"
```

Report: "Created and activated! Next run: {next run time}."

### Operation: List

Run:
```bash
uv run <skill_dir>/scripts/scheduler.py list
```

Present as a formatted table:

| ID | Name | Type | Schedule | Status | Last Run |
|----|------|------|----------|--------|----------|

If no tasks exist, say "No scheduled tasks yet. Use Add to create one."

### Operation: Pause

1. Run `list` to show active tasks
2. Ask which task to pause
3. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py pause --id "{task_id}"
```
4. Confirm: "Paused '{task_id}'. It won't run until you resume it."

### Operation: Resume

1. Run `list` to show paused tasks
2. Ask which task to resume
3. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py resume --id "{task_id}"
```
4. Confirm: "Resumed '{task_id}'. Next run: {next time}."

### Operation: Remove

1. Run `list` to show all tasks
2. Ask which task to remove
3. **Confirm**: "This will stop the schedule and delete the wrapper/plist. Results and logs are kept. Proceed?"
4. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py remove --id "{task_id}"
```
5. Confirm: "Removed '{task_id}'."

### Operation: Results

1. Ask which task (or show list if unclear)
2. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py results --id "{task_id}"
```
3. Display the latest result content inline

To list all results:
```bash
uv run <skill_dir>/scripts/scheduler.py results --id "{task_id}" --all
```

### Operation: Logs

1. Ask which task
2. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py logs --id "{task_id}"
```
3. Display recent log entries

### Operation: Run Now

1. Ask which task to test
2. Warn: "This runs the task immediately in the foreground. It will use your Claude session."
3. Run:
```bash
uv run <skill_dir>/scripts/scheduler.py run --id "{task_id}"
```
4. Show output as it streams

## Cron Expression Reference

For converting natural language to cron:

| Natural Language | Cron Expression |
|-----------------|-----------------|
| Every day at 9am | `0 9 * * *` |
| Every Monday at 8am | `0 8 * * 1` |
| Every weekday at 7:30am | `30 7 * * 1-5` |
| Every Sunday at midnight | `0 0 * * 0` |
| Every hour | `0 * * * *` |
| Every 1st of the month at 6am | `0 6 1 * *` |
| Twice daily (9am, 5pm) | Two tasks needed |

## Error Recovery

**"Task already exists"**: Suggest a different ID or remove the existing one first.
**"Invalid cron expression"**: Show the cron reference table and ask again.
**"Wrapper not found"**: Run repair:
```bash
uv run <skill_dir>/scripts/scheduler.py repair
```
**"Task failed (check logs)"**: Use the Logs operation to show what went wrong.

## Notes

- **Sleep behavior**: launchd catches up one missed run on wake. If multiple intervals were missed, only one run fires.
- **Working directory**: Defaults to the current project. Tasks that use marketplace skills should point to the marketplace project directory.
- **Auth**: Works with Claude subscription login (default) or API key from Keychain (optional).
- **Results**: Saved as markdown at `~/.claude/scheduler/results/YYYY-MM-DD/{id}.md`.
- **Logs**: Saved at `~/.claude/scheduler/logs/YYYY-MM-DD-{id}.log`.

## Quality Checklist

- [ ] Task type correctly identified (skill/prompt/script)
- [ ] Cron expression validated and confirmed with user
- [ ] Summary table presented before creating
- [ ] scheduler.py command executed successfully
- [ ] User informed of next run time (for add/resume)
- [ ] Confirmation requested before destructive operations (remove)
```

**Step 2: Verify SKILL.md is under 500 lines**

```bash
wc -l scheduler/skills/manage/SKILL.md
```

Expected: Under 500 lines.

**Step 3: Commit**

```bash
git add scheduler/skills/manage/SKILL.md
git commit -m "feat(scheduler): write orchestrator SKILL.md with full conversational flow"
```

---

## Task 6: Integration Test — Full Add/List/Remove Cycle

**Files:**
- Create: `.tests/test_scheduler_integration.py`

**Step 1: Write integration test**

Create `.tests/test_scheduler_integration.py`:

```python
"""Integration test: full add → list → get → pause → resume → remove cycle."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parents[1] / "scheduler" / "skills" / "manage" / "scripts" / "scheduler.py")


def run_scheduler(*args, scheduler_dir=None):
    env = os.environ.copy()
    if scheduler_dir:
        env["SCHEDULER_DIR"] = str(scheduler_dir)
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    result = subprocess.run(
        ["uv", "run", SCRIPT] + list(args),
        capture_output=True, text=True, env=env
    )
    return result.stdout, result.stderr, result.returncode


def cleanup_plist(task_id):
    plist = Path.home() / "Library" / "LaunchAgents" / f"com.ailaunchpad.scheduler.{task_id}.plist"
    if plist.exists():
        plist.unlink()


def test_full_lifecycle():
    """Full lifecycle: add → list → get → pause → resume → update-last-run → remove."""
    with tempfile.TemporaryDirectory() as d:
        task_id = "lifecycle-test"
        try:
            # Add
            stdout, _, rc = run_scheduler(
                "add", "--id", task_id, "--name", "Full Lifecycle Test",
                "--type", "skill", "--target", "substack:generate-note-ideas",
                "--cron", "0 8 * * 1", "--max-turns", "20",
                "--timeout", "15", "--workdir", "/tmp",
                scheduler_dir=d
            )
            assert rc == 0
            task = json.loads(stdout)
            assert task["id"] == task_id
            assert task["status"] == "active"

            # List
            stdout, _, rc = run_scheduler("list", scheduler_dir=d)
            assert rc == 0
            tasks = json.loads(stdout)
            assert len(tasks) == 1

            # Get
            stdout, _, rc = run_scheduler("get", "--id", task_id, scheduler_dir=d)
            assert rc == 0
            task = json.loads(stdout)
            assert task["schedule"]["cron"] == "0 8 * * 1"
            assert "Monday" in task["schedule"]["human"]

            # Verify files exist
            wrapper = Path(d) / "wrappers" / f"{task_id}.sh"
            plist = Path.home() / "Library" / "LaunchAgents" / f"com.ailaunchpad.scheduler.{task_id}.plist"
            assert wrapper.exists()
            assert plist.exists()

            # Pause
            _, _, rc = run_scheduler("pause", "--id", task_id, scheduler_dir=d)
            assert rc == 0
            stdout, _, _ = run_scheduler("get", "--id", task_id, scheduler_dir=d)
            assert json.loads(stdout)["status"] == "paused"

            # Resume
            _, _, rc = run_scheduler("resume", "--id", task_id, scheduler_dir=d)
            assert rc == 0
            stdout, _, _ = run_scheduler("get", "--id", task_id, scheduler_dir=d)
            assert json.loads(stdout)["status"] == "active"

            # Update last run (success)
            _, _, rc = run_scheduler(
                "update-last-run", "--id", task_id,
                "--exit-code", "0", "--duration", "60",
                "--result-file", f"{d}/results/2026-02-25/{task_id}.md",
                scheduler_dir=d
            )
            assert rc == 0
            stdout, _, _ = run_scheduler("get", "--id", task_id, scheduler_dir=d)
            task = json.loads(stdout)
            assert task["last_run"]["exit_code"] == 0
            assert task["last_run"]["duration_seconds"] == 60

            # Remove
            _, _, rc = run_scheduler("remove", "--id", task_id, scheduler_dir=d)
            assert rc == 0

            # Verify removed
            stdout, _, _ = run_scheduler("list", scheduler_dir=d)
            assert json.loads(stdout) == []
            assert not wrapper.exists()
            assert not plist.exists()

        finally:
            cleanup_plist(task_id)


def test_multiple_tasks():
    """Can manage multiple tasks simultaneously."""
    with tempfile.TemporaryDirectory() as d:
        task_ids = ["task-a", "task-b", "task-c"]
        try:
            for tid in task_ids:
                _, _, rc = run_scheduler(
                    "add", "--id", tid, "--name", f"Task {tid}",
                    "--type", "prompt", "--target", f"Prompt for {tid}",
                    "--cron", "0 9 * * *", "--max-turns", "10",
                    "--timeout", "5", "--workdir", "/tmp",
                    scheduler_dir=d
                )
                assert rc == 0

            stdout, _, _ = run_scheduler("list", scheduler_dir=d)
            tasks = json.loads(stdout)
            assert len(tasks) == 3

            # Pause one
            run_scheduler("pause", "--id", "task-b", scheduler_dir=d)

            # Remove one
            run_scheduler("remove", "--id", "task-c", scheduler_dir=d)

            stdout, _, _ = run_scheduler("list", scheduler_dir=d)
            tasks = json.loads(stdout)
            assert len(tasks) == 2
            statuses = {t["id"]: t["status"] for t in tasks}
            assert statuses["task-a"] == "active"
            assert statuses["task-b"] == "paused"

        finally:
            for tid in task_ids:
                cleanup_plist(tid)
```

**Step 2: Run all tests**

```bash
uv run pytest .tests/test_scheduler_*.py -v
```

Expected: All PASS.

**Step 3: Commit**

```bash
git add .tests/test_scheduler_integration.py
git commit -m "test(scheduler): add integration tests for full lifecycle"
```

---

## Task 7: Final Review and Polish

**Files:**
- Verify: All files in `scheduler/` directory
- Verify: `.claude-plugin/marketplace.json` entry
- Verify: All tests pass

**Step 1: Run full test suite**

```bash
uv run pytest .tests/test_scheduler_*.py -v --tb=short
```

Expected: All tests pass.

**Step 2: Verify plugin structure is complete**

```bash
ls -la scheduler/.claude-plugin/plugin.json
ls -la scheduler/README.md
ls -la scheduler/skills/manage/SKILL.md
ls -la scheduler/skills/manage/scripts/scheduler.py
ls -la scheduler/skills/manage/references/wrapper-template.sh
```

All files should exist.

**Step 3: Verify SKILL.md line count**

```bash
wc -l scheduler/skills/manage/SKILL.md
```

Must be under 500 lines.

**Step 4: Verify marketplace registration**

```bash
cat .claude-plugin/marketplace.json | python3 -c "import json,sys; d=json.load(sys.stdin); names=[p['name'] for p in d['plugins']]; assert 'scheduler' in names, 'scheduler not in marketplace'; print('OK: scheduler registered')"
```

**Step 5: Manual smoke test (optional)**

Test adding a task to verify launchd integration works end-to-end:

```bash
cd /Users/kennethliao/projects/ai-launchpad-marketplace
uv run scheduler/skills/manage/scripts/scheduler.py add \
  --id "smoke-test" \
  --name "Smoke Test" \
  --type "prompt" \
  --target "Say hello" \
  --cron "0 9 * * *" \
  --max-turns 5 \
  --timeout 2 \
  --workdir "/tmp"

# Verify launchd loaded it
launchctl list | grep ailaunchpad

# Clean up
uv run scheduler/skills/manage/scripts/scheduler.py remove --id "smoke-test"
```

**Step 6: Final commit**

If any polish was needed:
```bash
git add -A scheduler/ .tests/
git commit -m "chore(scheduler): final review and polish"
```

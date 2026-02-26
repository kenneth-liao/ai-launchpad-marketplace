#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["croniter>=2.0.0"]
# ///
"""Scheduler engine — registry CRUD, wrapper/plist generation, launchctl interaction.

Manages scheduled tasks for AI Launchpad via macOS LaunchAgents.
All CRUD commands output JSON to stdout; errors go to stderr.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

from croniter import croniter

# ---------------------------------------------------------------------------
# Constants / paths
# ---------------------------------------------------------------------------

SCHEDULER_DIR = Path(os.environ.get("SCHEDULER_DIR", str(Path.home() / ".claude" / "scheduler")))
REGISTRY_FILE = SCHEDULER_DIR / "registry.json"
WRAPPERS_DIR = SCHEDULER_DIR / "wrappers"
LOGS_DIR = SCHEDULER_DIR / "logs"
RESULTS_DIR = SCHEDULER_DIR / "results"
PLIST_DIR = Path(os.environ.get(
    "SCHEDULER_PLIST_DIR",
    str(Path.home() / "Library" / "LaunchAgents")
))
PLIST_PREFIX = "com.ailaunchpad.scheduler"

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "references" / "wrapper-template.sh"

SKIP_LAUNCHCTL = os.environ.get("SCHEDULER_SKIP_LAUNCHCTL", "0") == "1"

# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------


def _ensure_dirs() -> None:
    """Create scheduler directories if they don't exist."""
    for d in (SCHEDULER_DIR, WRAPPERS_DIR, LOGS_DIR, RESULTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def _load_registry() -> dict:
    """Load the registry from disk, creating a fresh one if needed."""
    _ensure_dirs()
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {"version": 1, "tasks": {}}


def _save_registry(registry: dict) -> None:
    """Persist the registry to disk."""
    _ensure_dirs()
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def _error(msg: str) -> None:
    """Print error to stderr and exit with code 1."""
    print(msg, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Cron helpers
# ---------------------------------------------------------------------------

WEEKDAY_NAMES = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                 4: "Thursday", 5: "Friday", 6: "Saturday"}


def _validate_cron(expr: str) -> None:
    """Raise if *expr* is not a valid 5-field cron expression."""
    if not croniter.is_valid(expr):
        _error(f"Invalid cron expression: {expr}")


def _humanize_cron(expr: str) -> str:
    """Best-effort conversion of a cron expression to a human-readable string."""
    parts = expr.split()
    if len(parts) != 5:
        return expr
    minute, hour, dom, month, dow = parts

    time_str = ""
    if minute != "*" and hour != "*":
        h = int(hour)
        m = int(minute)
        ampm = "AM" if h < 12 else "PM"
        display_h = h % 12 or 12
        time_str = f"{display_h}:{m:02d} {ampm}"

    # Every minute
    if all(p == "*" for p in parts):
        return "Every minute"

    # Every N minutes
    if minute.startswith("*/") and hour == "*" and dom == "*" and month == "*" and dow == "*":
        return f"Every {minute[2:]} minutes"

    # Every hour
    if hour == "*" and dom == "*" and month == "*" and dow == "*":
        if minute != "*":
            return f"Every hour at minute {minute}"
        return "Every hour"

    # Daily
    if dom == "*" and month == "*" and dow == "*" and time_str:
        return f"Every day at {time_str}"

    # Specific weekday(s)
    if dom == "*" and month == "*" and dow != "*" and time_str:
        # parse dow — could be single, comma-separated, or range
        day_strs = _expand_dow(dow)
        if day_strs:
            return f"Every {', '.join(day_strs)} at {time_str}"

    # Specific day of month
    if dom != "*" and month == "*" and dow == "*" and time_str:
        return f"Day {dom} of every month at {time_str}"

    return expr


def _expand_dow(dow_field: str) -> list[str]:
    """Expand a dow field like '1', '1,3,5', or '1-5' into weekday names."""
    nums: list[int] = []
    for part in dow_field.split(","):
        if "-" in part:
            lo, hi = part.split("-", 1)
            nums.extend(range(int(lo), int(hi) + 1))
        else:
            nums.append(int(part))
    return [WEEKDAY_NAMES.get(n, str(n)) for n in nums]


# ---------------------------------------------------------------------------
# Plist helpers
# ---------------------------------------------------------------------------


def _cron_to_calendar_interval(expr: str) -> list[dict]:
    """Convert a 5-field cron expression to a list of StartCalendarInterval dicts.

    Each dict may contain: Minute, Hour, Day, Month, Weekday.
    Wildcard fields are omitted (meaning "every").
    Supports step syntax (e.g. ``*/2``, ``1-30/5``) and comma-separated lists.
    Produces the Cartesian product of all multi-value fields so that
    launchd fires at every specified combination.
    """
    parts = expr.split()
    minute, hour, dom, month, dow = parts

    # Ranges used for expanding step syntax against wildcards
    FIELD_RANGES: dict[str, tuple[int, int]] = {
        "minute": (0, 59),
        "hour": (0, 23),
        "dom": (1, 31),
        "month": (1, 12),
        "dow": (0, 6),
    }

    def _parse_field(field: str, field_name: str) -> list[int] | None:
        """Parse a single cron field into a sorted list of ints, or None for '*'."""
        if field == "*":
            return None
        nums: list[int] = []
        for part in field.split(","):
            # Handle step syntax: */N or A-B/N
            if "/" in part:
                range_part, step_str = part.split("/", 1)
                step = int(step_str)
                if range_part == "*":
                    lo, hi = FIELD_RANGES[field_name]
                elif "-" in range_part:
                    lo_s, hi_s = range_part.split("-", 1)
                    lo, hi = int(lo_s), int(hi_s)
                else:
                    lo = int(range_part)
                    hi = FIELD_RANGES[field_name][1]
                nums.extend(range(lo, hi + 1, step))
            elif "-" in part:
                lo, hi = part.split("-", 1)
                nums.extend(range(int(lo), int(hi) + 1))
            else:
                nums.append(int(part))
        return sorted(set(nums))

    minute_vals = _parse_field(minute, "minute")
    hour_vals = _parse_field(hour, "hour")
    dom_vals = _parse_field(dom, "dom")
    month_vals = _parse_field(month, "month")
    dow_vals = _parse_field(dow, "dow")

    # Build the Cartesian product of all multi-value fields.
    # Fields that are None (wildcard) are omitted from the dict, which
    # tells launchd "every value" for that field.
    field_specs: list[tuple[str, list[int] | None]] = [
        ("Minute", minute_vals),
        ("Hour", hour_vals),
        ("Day", dom_vals),
        ("Month", month_vals),
        ("Weekday", dow_vals),
    ]

    intervals: list[dict] = [{}]
    for key, vals in field_specs:
        if vals is None:
            continue  # wildcard — omit from dict
        expanded: list[dict] = []
        for existing in intervals:
            for v in vals:
                entry = dict(existing)
                entry[key] = v
                expanded.append(entry)
        intervals = expanded

    return intervals if intervals else [{}]


def _interval_to_plist_xml(interval: dict) -> str:
    """Render a single StartCalendarInterval dict as plist XML."""
    lines = ["        <dict>"]
    for key in ("Minute", "Hour", "Day", "Month", "Weekday"):
        if key in interval:
            lines.append(f"            <key>{key}</key>")
            lines.append(f"            <integer>{interval[key]}</integer>")
    lines.append("        </dict>")
    return "\n".join(lines)


def _generate_plist(task_id: str, wrapper_path: Path) -> Path:
    """Generate a LaunchAgent plist for the given task and return its path."""
    registry = _load_registry()
    task = registry["tasks"][task_id]
    cron_expr = task["schedule"]["cron"]

    intervals = _cron_to_calendar_interval(cron_expr)

    # Build StartCalendarInterval block
    if len(intervals) == 1:
        cal_block = f"    <key>StartCalendarInterval</key>\n{_interval_to_plist_xml(intervals[0])}"
    else:
        inner = "\n".join(_interval_to_plist_xml(iv) for iv in intervals)
        cal_block = f"    <key>StartCalendarInterval</key>\n    <array>\n{inner}\n    </array>"

    label = f"{PLIST_PREFIX}.{task_id}"
    stdout_log = str(LOGS_DIR / f"{task_id}.stdout.log")
    stderr_log = str(LOGS_DIR / f"{task_id}.stderr.log")

    plist_xml = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
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
        {cal_block}
            <key>StandardOutPath</key>
            <string>{stdout_log}</string>
            <key>StandardErrorPath</key>
            <string>{stderr_log}</string>
        </dict>
        </plist>
    """)

    PLIST_DIR.mkdir(parents=True, exist_ok=True)
    plist_path = PLIST_DIR / f"{label}.plist"
    plist_path.write_text(plist_xml)
    return plist_path


# ---------------------------------------------------------------------------
# Wrapper generation
# ---------------------------------------------------------------------------


def _generate_wrapper(task: dict) -> Path:
    """Generate a bash wrapper script from the template for the given task."""
    template = TEMPLATE_PATH.read_text()
    # Escape single quotes in target since it's enclosed in single quotes in template
    escaped_target = task["target"].replace("'", "'\\''")

    wrapper = template.replace("{id}", task["id"])
    wrapper = wrapper.replace("{type}", task["type"])
    wrapper = wrapper.replace("{target}", escaped_target)
    wrapper = wrapper.replace("{max_turns}", str(task["safety"]["max_turns"]))
    wrapper = wrapper.replace("{timeout_minutes}", str(task["safety"]["timeout_minutes"]))
    wrapper = wrapper.replace("{working_directory}", task["working_directory"])
    wrapper = wrapper.replace("{run_once}", "true" if task.get("run_once") else "false")
    wrapper = wrapper.replace("{scheduler_py}", str(Path(__file__).resolve()))

    WRAPPERS_DIR.mkdir(parents=True, exist_ok=True)
    wrapper_path = WRAPPERS_DIR / f"{task['id']}.sh"
    wrapper_path.write_text(wrapper)
    wrapper_path.chmod(0o755)
    return wrapper_path


# ---------------------------------------------------------------------------
# Launchctl helpers
# ---------------------------------------------------------------------------


def _plist_path(task_id: str) -> Path:
    """Return the plist path for a given task ID."""
    return PLIST_DIR / f"{PLIST_PREFIX}.{task_id}.plist"


def _launchctl_load(plist_path: Path) -> None:
    """Load a plist via launchctl. Skipped when SCHEDULER_SKIP_LAUNCHCTL=1."""
    if SKIP_LAUNCHCTL:
        return
    uid = os.getuid()
    result = subprocess.run(
        ["launchctl", "bootstrap", f"gui/{uid}", str(plist_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        # Fallback to legacy load
        subprocess.run(
            ["launchctl", "load", str(plist_path)],
            capture_output=True, text=True,
        )


def _launchctl_unload(plist_path: Path) -> None:
    """Unload a plist via launchctl. Skipped when SCHEDULER_SKIP_LAUNCHCTL=1."""
    if SKIP_LAUNCHCTL:
        return
    uid = os.getuid()
    label = plist_path.stem  # e.g. com.ailaunchpad.scheduler.my-task
    result = subprocess.run(
        ["launchctl", "bootout", f"gui/{uid}/{label}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        # Fallback to legacy unload
        subprocess.run(
            ["launchctl", "unload", str(plist_path)],
            capture_output=True, text=True,
        )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new scheduled task."""
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', args.id):
        _error(f"Invalid task ID '{args.id}'. Use only letters, numbers, hyphens, and underscores.")

    _validate_cron(args.cron)

    if args.type not in ("skill", "prompt", "script"):
        _error(f"Invalid type '{args.type}'. Must be one of: skill, prompt, script")

    registry = _load_registry()

    if args.id in registry["tasks"]:
        _error(f"Task '{args.id}' already exists. Use a different ID.")

    now = datetime.now(timezone.utc).isoformat()

    task = {
        "id": args.id,
        "name": args.name,
        "type": args.type,
        "target": args.target,
        "working_directory": args.working_directory,
        "schedule": {
            "cron": args.cron,
            "human": _humanize_cron(args.cron),
        },
        "safety": {
            "max_turns": args.max_turns,
            "timeout_minutes": args.timeout_minutes,
        },
        "run_once": args.run_once,
        "status": "active",
        "created_at": now,
        "last_run": None,
    }

    registry["tasks"][args.id] = task
    _save_registry(registry)

    # Generate wrapper and plist
    wrapper_path = _generate_wrapper(task)
    _generate_plist(args.id, wrapper_path)
    _launchctl_load(_plist_path(args.id))

    print(json.dumps(task, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    """List all tasks."""
    registry = _load_registry()
    tasks = list(registry["tasks"].values())
    print(json.dumps(tasks, indent=2))


def cmd_get(args: argparse.Namespace) -> None:
    """Get details of a specific task."""
    registry = _load_registry()
    task = registry["tasks"].get(args.id)
    if task is None:
        _error(f"Task '{args.id}' not found.")
    print(json.dumps(task, indent=2))


def cmd_remove(args: argparse.Namespace) -> None:
    """Remove a task from the registry."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    # Unload plist
    plist = _plist_path(args.id)
    if plist.exists():
        _launchctl_unload(plist)
        plist.unlink()

    # Remove wrapper
    wrapper = WRAPPERS_DIR / f"{args.id}.sh"
    if wrapper.exists():
        wrapper.unlink()

    task = registry["tasks"].pop(args.id)
    _save_registry(registry)

    print(json.dumps({"removed": args.id}, indent=2))


def cmd_pause(args: argparse.Namespace) -> None:
    """Pause a task (unload from launchctl)."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    if registry["tasks"][args.id]["status"] == "paused":
        _error(f"Task '{args.id}' is already paused.")

    plist = _plist_path(args.id)
    if plist.exists():
        _launchctl_unload(plist)

    registry["tasks"][args.id]["status"] = "paused"
    _save_registry(registry)
    print(json.dumps(registry["tasks"][args.id], indent=2))


def cmd_resume(args: argparse.Namespace) -> None:
    """Resume a paused task (load into launchctl)."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    if registry["tasks"][args.id]["status"] == "active":
        _error(f"Task '{args.id}' is already active.")

    plist = _plist_path(args.id)
    if plist.exists():
        _launchctl_load(plist)

    registry["tasks"][args.id]["status"] = "active"
    _save_registry(registry)
    print(json.dumps(registry["tasks"][args.id], indent=2))


def cmd_complete(args: argparse.Namespace) -> None:
    """Mark a task as completed and unload from launchctl.

    Used by run-once wrappers to self-deactivate after successful execution.
    Unlike 'pause', this sets status to 'completed' to indicate the task
    finished naturally rather than being manually paused.
    """
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    plist = _plist_path(args.id)
    if plist.exists():
        _launchctl_unload(plist)

    registry["tasks"][args.id]["status"] = "completed"
    _save_registry(registry)
    print(json.dumps(registry["tasks"][args.id], indent=2))


def cmd_run(args: argparse.Namespace) -> None:
    """Execute a task's wrapper script directly."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    wrapper = WRAPPERS_DIR / f"{args.id}.sh"
    if not wrapper.exists():
        _error(f"Wrapper script not found for task '{args.id}'. Run 'repair' first.")

    result = subprocess.run(
        ["/bin/bash", str(wrapper)],
        capture_output=False,
    )
    sys.exit(result.returncode)


def cmd_logs(args: argparse.Namespace) -> None:
    """Show recent log files for a task."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    # Find log files matching *-{id}.log
    log_files = sorted(LOGS_DIR.glob(f"*-{args.id}.log"), reverse=True)[:3]

    if not log_files:
        print(f"No log files found for task '{args.id}'.", file=sys.stderr)
        return

    for log_file in log_files:
        print(f"\n=== {log_file.name} ===")
        print(log_file.read_text())


def cmd_results(args: argparse.Namespace) -> None:
    """Show result files for a task."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    # Find result files matching {id}.md in any date subdirectory
    result_files = sorted(RESULTS_DIR.glob(f"*/{args.id}.md"), reverse=True)

    if not result_files:
        print(f"No result files found for task '{args.id}'.", file=sys.stderr)
        return

    if args.all:
        for rf in result_files:
            print(f"\n=== {rf.parent.name}/{rf.name} ===")
            print(rf.read_text())
    else:
        latest = result_files[0]
        print(f"=== {latest.parent.name}/{latest.name} ===")
        print(latest.read_text())


def cmd_update_last_run(args: argparse.Namespace) -> None:
    """Update the last_run field of a task."""
    registry = _load_registry()
    if args.id not in registry["tasks"]:
        _error(f"Task '{args.id}' not found.")

    now = datetime.now(timezone.utc).isoformat()

    last_run = {
        "timestamp": now,
        "exit_code": args.exit_code,
        "duration_seconds": args.duration,
        "result_file": args.result_file,
    }

    registry["tasks"][args.id]["last_run"] = last_run

    # Set status to error if exit code is non-zero
    if args.exit_code != 0:
        registry["tasks"][args.id]["status"] = "error"

    _save_registry(registry)
    print(json.dumps(registry["tasks"][args.id], indent=2))


def cmd_repair(args: argparse.Namespace) -> None:
    """Regenerate missing wrapper scripts and plist files for active tasks."""
    registry = _load_registry()
    issues_fixed = 0

    for task_id, task in registry["tasks"].items():
        if task["status"] != "active":
            continue

        wrapper_path = WRAPPERS_DIR / f"{task_id}.sh"
        plist = _plist_path(task_id)

        if not wrapper_path.exists():
            _generate_wrapper(task)
            print(f"Regenerated wrapper for '{task_id}'")
            issues_fixed += 1

        if not plist.exists():
            _generate_plist(task_id, wrapper_path)
            _launchctl_load(plist)
            print(f"Regenerated plist for '{task_id}'")
            issues_fixed += 1

    if issues_fixed > 0:
        print(f"Repair complete: {issues_fixed} issue(s) fixed.")
    else:
        print("Repair complete: no issues found.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Launchpad Scheduler Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- add ---
    p_add = subparsers.add_parser("add", help="Add a new scheduled task")
    p_add.add_argument("--id", required=True, help="Unique task identifier")
    p_add.add_argument("--name", required=True, help="Human-readable task name")
    p_add.add_argument("--type", required=True, choices=["skill", "prompt", "script"],
                       help="Task type")
    p_add.add_argument("--target", required=True, help="Skill name, prompt text, or script path")
    p_add.add_argument("--cron", required=True, help="Cron schedule expression (5 fields)")
    p_add.add_argument("--working-directory", required=True, help="Working directory for task")
    p_add.add_argument("--max-turns", type=int, default=20, help="Max Claude turns (default: 20)")
    p_add.add_argument("--timeout-minutes", type=int, default=15,
                       help="Timeout in minutes (default: 15)")
    p_add.add_argument("--run-once", action="store_true", default=False,
                       help="Run once then auto-complete (one-off task)")
    p_add.set_defaults(func=cmd_add)

    # --- list ---
    p_list = subparsers.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=cmd_list)

    # --- get ---
    p_get = subparsers.add_parser("get", help="Get task details")
    p_get.add_argument("--id", required=True, help="Task ID")
    p_get.set_defaults(func=cmd_get)

    # --- remove ---
    p_remove = subparsers.add_parser("remove", help="Remove a task")
    p_remove.add_argument("--id", required=True, help="Task ID")
    p_remove.set_defaults(func=cmd_remove)

    # --- pause ---
    p_pause = subparsers.add_parser("pause", help="Pause a task")
    p_pause.add_argument("--id", required=True, help="Task ID")
    p_pause.set_defaults(func=cmd_pause)

    # --- resume ---
    p_resume = subparsers.add_parser("resume", help="Resume a paused task")
    p_resume.add_argument("--id", required=True, help="Task ID")
    p_resume.set_defaults(func=cmd_resume)

    # --- complete ---
    p_complete = subparsers.add_parser("complete", help="Mark a task as completed and unload")
    p_complete.add_argument("--id", required=True, help="Task ID")
    p_complete.set_defaults(func=cmd_complete)

    # --- run ---
    p_run = subparsers.add_parser("run", help="Execute a task immediately")
    p_run.add_argument("--id", required=True, help="Task ID")
    p_run.set_defaults(func=cmd_run)

    # --- logs ---
    p_logs = subparsers.add_parser("logs", help="Show recent logs for a task")
    p_logs.add_argument("--id", required=True, help="Task ID")
    p_logs.set_defaults(func=cmd_logs)

    # --- results ---
    p_results = subparsers.add_parser("results", help="Show results for a task")
    p_results.add_argument("--id", required=True, help="Task ID")
    p_results.add_argument("--all", action="store_true", help="Show all results")
    p_results.set_defaults(func=cmd_results)

    # --- update-last-run ---
    p_ulr = subparsers.add_parser("update-last-run", help="Update last run info")
    p_ulr.add_argument("--id", required=True, help="Task ID")
    p_ulr.add_argument("--exit-code", type=int, required=True, help="Exit code")
    p_ulr.add_argument("--duration", type=int, required=True, help="Duration in seconds")
    p_ulr.add_argument("--result-file", required=True, help="Path to result file")
    p_ulr.set_defaults(func=cmd_update_last_run)

    # --- repair ---
    p_repair = subparsers.add_parser("repair", help="Regenerate missing wrappers/plists")
    p_repair.set_defaults(func=cmd_repair)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

---
name: manage
description: Manage scheduled Claude Code tasks — add (recurring or one-off), list, pause, resume, remove, view results, and test execution of skills, prompts, and scripts. Cross-platform (macOS, Linux, Windows). Invoke via /schedule.
---

# Scheduler

Manage automated Claude Code tasks across macOS, Linux, and Windows. Schedule marketplace skills, freeform prompts, or shell scripts to run on a recurring cron schedule or as one-off tasks, with safety controls and desktop notifications.

## Platform Support

| Platform | Scheduler | Notifications | API Key Storage |
|----------|-----------|---------------|-----------------|
| macOS | launchd (plist + launchctl) | osascript (native) | Keychain (`security` CLI) |
| Linux | systemd user timers (.service + .timer) | notify-send (libnotify) | secret-tool (GNOME Keyring) or `~/.config/anthropic/api-key` |
| Windows | Task Scheduler (schtasks.exe + XML) | BurntToast / Windows toast | Windows Credential Manager or `%USERPROFILE%\.config\anthropic\api-key` |

The platform is auto-detected at runtime. Tasks record which platform they were created on.

## Overview

This orchestrator manages the full lifecycle of scheduled tasks. It delegates all operations to `scheduler.py` and presents results conversationally.

**Core Principle**: This is a thin orchestrator. All scheduling logic, file generation, and platform scheduler interaction are handled by `scheduler.py` with platform-specific backends. This skill manages the conversational flow only.

## When to Use

Use this skill when:
- Scheduling a recurring or one-off task (skill, prompt, or script)
- Listing, pausing, resuming, or removing scheduled tasks
- Viewing results or logs from past scheduled runs
- Testing a scheduled task before activating it

## Prerequisites

- macOS, Linux, or Windows
- `claude` CLI in PATH (for skill and prompt tasks)
- `uv` installed (for running scheduler.py)
- **Linux only**: `systemctl --user` available (systemd with user session)
- **Windows only**: PowerShell 5.1+ and Task Scheduler access

## First-Time Setup

On first invocation, verify `claude` is authenticated and in PATH:

```bash
claude -p "hello" --max-turns 1 --output-format text
```

If this fails, guide the user to run `claude login` before proceeding.

Also check if the scheduler directory exists. The scheduler uses project-level storage by default — it looks for `.git` or `CLAUDE.md` to find the project root, then stores state at `<project>/.claude/scheduler/`:

```bash
ls .claude/scheduler/registry.json
```

If it does not exist, the first `add` command will create it automatically. No manual setup needed. You can override the location with the `SCHEDULER_DIR` environment variable, or fall back to `~/.claude/scheduler/` when outside a project.

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

**Step 4: Frequency**
Ask: "Recurring or one-off?"
- **Recurring** — runs on a schedule until paused or removed
- **One-off** — runs once at the specified time, then auto-completes

**Step 5: Schedule**
Ask: "What schedule? You can use natural language or a cron expression."
Examples: "Every Monday at 8am", "Daily at 9:00", "Every weekday at 7:30am", "Tomorrow at 9am", "0 8 * * 1"

Convert natural language to a cron expression. For one-off tasks, convert the target datetime to a specific cron (e.g., "tomorrow at 9am" on Feb 25 → `0 9 26 2 *`).

Confirm with the user:
"That's `0 8 * * 1` — Every Monday at 8:00 AM. Correct?"

**Step 6: Safety limits**
Ask: "Safety limits? Defaults are max 20 turns, 15 minute timeout."
Let user accept defaults or customize.

**Step 6a: Output directory (optional)**
Ask: "Want results saved to a specific directory? Default is the scheduler's results folder."
If the user provides a path, it will be resolved to an absolute path and used as the flat output directory (no date subdirectories). If skipped, results go to `<scheduler_dir>/results/YYYY-MM-DD/{id}.md`.

**Step 6b: Permissions (skip for script-type tasks)**
Scheduled tasks run non-interactively — Claude Code can't ask the user to approve tool use. Without pre-approved permissions, tools that need approval will fail silently.

Ask: "What permissions should this task have?"
Offer these presets:
- **Default** — no extra permissions (works if you have `bypassPermissions` set globally)
- **Readonly** — read files, search, browse web (safe for research/reporting tasks)
- **Research** — read files, search, web browse, curl (for data gathering)
- **Full edit** — read, write, edit files, git, npm, uv, python, web (for code maintenance tasks)
- **Bypass** — skip all permission checks (`--dangerously-skip-permissions`)
- **Custom** — specify individual tool names

For **custom**, prompt for individual tool specs (e.g., `Read`, `Write`, `Bash(git *)`) separated by spaces.

Show the selected permission mode in the confirmation summary table.

CLI flags:
- `--permission-preset readonly|full-edit|research|bypass`
- `--permission-mode default|acceptEdits|plan|dontAsk|bypassPermissions`
- `--allowed-tools Read Write 'Bash(git *)'` (individual tool specs)

**Step 7: Confirm and create**
Present a summary table:

| Field | Value |
|-------|-------|
| ID | weekly-note-ideas |
| Name | Weekly note ideas |
| Type | Skill |
| Target | substack:generate-note-ideas |
| Frequency | Recurring |
| Schedule | Every Monday at 8:00 AM (0 8 * * 1) |
| Max turns | 20 |
| Timeout | 15 min |
| Working dir | {current project directory} |
| Output dir | (default) |
| Permissions | (default) / readonly / research / full-edit / bypass / custom |

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
  --timeout-minutes 15 \
  --working-directory "{cwd}"
```

For one-off tasks, add the `--run-once` flag. You can also specify `--output-directory` and `--permission-preset`:
```bash
uv run <skill_dir>/scripts/scheduler.py add \
  --id "morning-news-pulse" \
  --name "Morning news pulse" \
  --type prompt \
  --target "Research today's AI news" \
  --cron "0 9 26 2 *" \
  --max-turns 20 \
  --timeout-minutes 15 \
  --run-once \
  --permission-preset research \
  --output-directory "/path/to/output" \
  --working-directory "{cwd}"
```

Report: "Created and activated! Next run: {next run time}."
For one-off tasks, add: "This will auto-complete after running."

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
3. **Confirm**: "This will stop the schedule and delete the wrapper and schedule artifacts. Results and logs are kept. Proceed?"
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

### Operation: Cleanup

Delete old log and result files to reclaim disk space:

```bash
uv run <skill_dir>/scripts/scheduler.py cleanup --max-days 30
```

The `--max-days` flag controls the retention period (default: 30 days). Log files are cleaned by modification time; result date-directories are cleaned by directory name.

**Tip**: You can schedule cleanup itself as a recurring task:
```bash
uv run <skill_dir>/scripts/scheduler.py add \
  --id scheduler-cleanup \
  --name "Scheduler Cleanup" \
  --type script \
  --target "<skill_dir>/scripts/cleanup-wrapper.sh" \
  --cron "0 3 * * 0" \
  --working-directory "{cwd}"
```

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
**"Task succeeded but output is empty"**: Likely a permission issue. Scheduled tasks run non-interactively and can't prompt for tool approval. Add a permission preset (e.g., `--permission-preset readonly` for read-only tasks) and regenerate wrappers with `repair --force`.
**"Wrapper needs permission update"**: After changing a task's permissions in the registry, run `repair --force` to regenerate all wrappers with the new settings.

## Notes

- **Permissions**: Scheduled tasks run non-interactively via `claude -p` — there's no user to approve tool use. Without pre-configured permissions, any tool needing approval fails silently. Use `--permission-preset` (readonly, research, full-edit, bypass) or `--allowed-tools` to pre-approve the tools a task needs. The `bypass` preset uses `--dangerously-skip-permissions` to skip all checks. After adding permissions to existing tasks, run `repair --force` to regenerate wrappers.
- **One-off tasks**: Tasks created with `--run-once` auto-complete after their first successful run. They remain in the registry with status `completed` so results and logs are preserved. They can be removed later with the Remove operation.
- **Lock file**: The wrapper uses a PID-based lock to prevent concurrent runs of the same task. If a previous run is still active, the new run is skipped. On Windows, the lock uses `Get-Process` instead of `kill -0`.
- **Sleep/missed run behavior**: All platforms catch up on missed runs. macOS launchd fires one missed run on wake. Linux systemd timers use `Persistent=true`. Windows Task Scheduler uses `StartWhenAvailable=true`.
- **Working directory**: Defaults to the current project. Tasks that use marketplace skills should point to the marketplace project directory.
- **Auth**: Works with Claude subscription login (default) or platform-specific API key storage (macOS Keychain, Linux GNOME Keyring or file, Windows Credential Manager or file).
- **Project-level storage**: By default, the scheduler stores state at `<project>/.claude/scheduler/` when run inside a project (detected via `.git` or `CLAUDE.md`). Override with the `SCHEDULER_DIR` env var or fall back to `~/.claude/scheduler/` when outside a project.
- **Results**: Saved as markdown at `<scheduler_dir>/results/YYYY-MM-DD/{id}-HHMMSS.md` (timestamped to prevent same-day overwrites). If `--output-directory` was specified, results go to `<output_dir>/{id}.md` (stable filenames, no date subdirectories). Legacy `{id}.md` files are still found by the results command.
- **Logs**: Saved at `<scheduler_dir>/logs/YYYY-MM-DD-{id}.log`.
- **Cleanup**: Use `cleanup --max-days N` to delete old logs and result directories. Defaults to 30 days.
- **Platform field**: Each task records which platform it was created on. The `repair` command can detect mismatches (e.g. a macOS task on Linux) and reinstall using the current platform's backend.
- **Upgrading from v1**: The registry auto-migrates from v1 to v2 on first load, adding a `platform` field to existing tasks. Wrapper templates differ per platform; to apply the correct template, run `repair` or remove and re-add tasks.

## Quality Checklist

- [ ] Task type correctly identified (skill/prompt/script)
- [ ] Cron expression validated and confirmed with user
- [ ] Summary table presented before creating
- [ ] scheduler.py command executed successfully
- [ ] User informed of next run time (for add/resume)
- [ ] Confirmation requested before destructive operations (remove)

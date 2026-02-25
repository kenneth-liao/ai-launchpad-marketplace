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

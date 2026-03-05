# Changelog

All notable changes to the Scheduler plugin.

## [1.1.2] - 2026-03-05

### Fixed

- Updated old plugin references after creator-stack consolidation

### Changed

- Improved skill tone consistency and structural fixes

## [1.1.0] - 2026-03-02

### Added

- **Session log capture** for macOS, Linux, and Windows wrappers
- **Date-organized logs** with task-first, then date directory structure
- `cmd_logs` and `cmd_cleanup` commands for log management

### Changed

- Documented session log capture, log organization, and repair workflow in README

## [1.0.3] - 2026-03-01

### Fixed

- Replaced "Run Now" with deferred scheduling for Claude Code compatibility
- Unset `CLAUDECODE` env var to prevent worktree creation in scheduled tasks

## [1.0.2] - 2026-02-27

### Fixed

- Added `~/.local/bin` to macOS wrapper PATH for `uv` discovery
- Fixed skill invocation command in docs and added example prompt

### Changed

- Updated marketplace and plugin documentation

## [1.0.1] - 2026-02-26

### Added

- **Per-task permission handling** for non-interactive runs
- **Use cases reference** document for automation ideas
- **Cross-platform support** -- macOS (launchd), Linux (systemd), Windows (Task Scheduler)

### Fixed

- Reliability improvements: registry feedback, timestamped results, atomic writes, cleanup

## [1.0.0] - 2026-02-25

### Added

- **`manage` skill** -- Conversational orchestrator for scheduling Claude Code tasks
- **`scheduler.py` engine** -- Core registry CRUD with add, list, pause, resume, remove, view results
- **One-off and recurring tasks** with cron expression support
- **Project-level storage** and per-task output directories
- **Lock file** and structured logging
- **Platform detection** via `platform_detect.py`
- **macOS backend** with launchd/plist wrapper template

### Fixed

- Replaced GNU `timeout` with macOS-compatible timeout function
- Plist isolation, idempotency guards, repair output, ID validation

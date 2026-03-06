# Changelog

All notable changes to the Plugin Tools plugin.

## [1.2.0] - 2026-03-06

### Added

- **`/test-skill` skill** -- Run or generate test suites for any skill (task, discipline, or orchestrator). Features auto-detection of skill type, test generation from skill content, subagent-based execution with parallel eval runs, regression tracking via snapshots.json, and skill-creator-compatible JSON schemas. Supports interactive (subagent) and headless (CLI) execution modes.
- **Test suite integration in `/upgrade-plugin`** -- Phase 2 (Audit) now checks for test coverage gaps. Phase 5 (Verify) offers to run test suites for modified skills and surfaces regressions before approval.

## [1.1.0] - 2026-03-06

### Added

- **Obsolescence detection in `/upgrade-plugin`** -- New Phase 1.5 (Obsolescence Screen) evaluates whether each skill/agent is Active, Augmented, or Superseded by platform/model improvements. Superseded components skip structural audit and appear in a new "Recommend Removal" plan tier. New research task 1F fetches model capability updates from Anthropic.

## [1.0.0] - 2026-03-06

### Added

- **`/upgrade-plugin` skill** -- Upgrade any plugin's skills, hooks, and patterns to align with latest Claude Code capabilities. Features discovery-driven documentation research, full plugin component audit, and structured upgrade planning with approval gates. Migrated from legacy `.claude/commands/` to proper skill format.

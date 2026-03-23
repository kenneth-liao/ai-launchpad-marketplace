# Changelog

All notable changes to the Plugin Tools plugin.

## [1.4.0] - 2026-03-23

### Removed

- **`/test-skill` archived** -- Moved to `archive/test-skill/`. Superseded by Anthropic's official `skill-creator` evals framework, which provides richer grading (claims extraction, eval feedback, execution metrics), baseline comparison, browser-based review UI, and iterative improvement loops. The archived skill retains its reference files (test-generation.md, schemas.md) for future reference. Discipline skill pressure-testing concepts may be revisited as a skill-creator extension if needed.

### Changed

- **Plugin description** -- Removed "test skills" from description since test-skill is archived
- **`/upgrade-plugin`** -- Test suite integration references in Phase 2/5 may reference archived skill; use skill-creator evals instead

## [1.3.0] - 2026-03-22

### Added

- **`/skill-retro` skill** -- Analyze how skills performed in a session and apply improvements. Features session JSONL preprocessing (Node.js, zero dependencies), sub-agent-based analysis across three dimensions (trigger accuracy, execution quality, gap coverage), smart source location resolution (project-level, user-level, installed plugins, marketplace repos), and parallel implementation via skill-creator. Designed for context efficiency — all heavy work runs in sub-agents.

## [1.2.1] - 2026-03-06

### Fixed

- **`/test-skill` grader instructions** -- Added guidance that simulated execution is expected and valid. Graders now evaluate based on correct command construction, not whether commands were actually run against a live backend. Fixes false negatives on skills that delegate to scripts (e.g., scheduler:manage).

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

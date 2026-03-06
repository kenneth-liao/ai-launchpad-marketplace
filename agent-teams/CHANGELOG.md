# Changelog

All notable changes to the Agent Teams plugin.

## [1.1.0] - 2026-03-06

### Added

- **Task management event type** -- `generate.py` now classifies TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop as dedicated `task_management` events (distinct from generic tool calls)
- **Team config discovery** -- `generate.py` reads `~/.claude/teams/{team-name}/config.json` for richer teammate metadata (model, agent type)
- **2 new rubric categories** in `analyze-team-session`:
  - **Task Dependencies** -- evaluates whether task dependency tracking was used effectively
  - **Quality Gates** -- evaluates use of TaskCompleted hooks, TeammateIdle hooks, and plan approval workflows
- **Rubric reference file** -- extracted evaluation rubric to `references/rubric.md` for progressive disclosure

### Changed

- **`${CLAUDE_SKILL_DIR}`** -- `view-team-session` now uses the auto-resolved variable instead of a manual `{SKILL_DIR}` placeholder
- **Skill frontmatter** -- both skills now include `user-invocable: true` and `argument-hint`
- **Improved triggering** -- `view-team-session` description expanded with additional trigger phrases ("show me what my agents did", "session replay", "team timeline")
- **Cost Efficiency rubric** expanded to **Model Selection & Cost Efficiency** -- now evaluates per-teammate model selection (Opus vs Sonnet vs Haiku)
- **Lead Orchestration rubric** updated to evaluate plan approval workflow usage
- **Doc URL discovery** -- `analyze-team-session` now uses WebSearch-first approach with fallback to known URLs, more resilient to URL changes
- **plugin.json** -- added `repository`, `license`, `keywords` fields; bumped to 1.1.0

## [1.0.0] - 2026-02-20

### Added

- **`view-team-session` skill** -- Generate self-contained HTML viewers from Claude Code session JSONL logs. Supports solo and team sessions with full conversation timeline, filtering, search, and collapsible tool calls.
- **`analyze-team-session` skill** -- Analyze agent team session exports against official best practices. Produces structured reports with suitability verdict, 8-category scorecard, actionable recommendations, and improved prompt rewrite.
- **HTML template** for session viewer with built-in CSS/JS
- **`generate.py`** script for JSONL-to-HTML conversion

### Changed

- Added `uv` dependency setup instructions to README (2026-02-23)
- Added session viewer screenshot to README (2026-02-23)
- Added optional tmux installation and setup instructions (2026-02-23)
- Added cross-references between analyze and view skills (2026-03-05)

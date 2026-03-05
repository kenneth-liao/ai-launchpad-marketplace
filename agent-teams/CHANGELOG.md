# Changelog

All notable changes to the Agent Teams plugin.

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

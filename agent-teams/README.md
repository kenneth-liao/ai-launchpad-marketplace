# Agent Teams Plugin

Developer tools for Claude Code agent team sessions. View session timelines, analyze team effectiveness, and evaluate against official best practices.

## Skills

### view-team-session (Task)

Generate a self-contained HTML viewer from Claude Code session JSONL logs. Works for both solo and team sessions, showing the full conversation timeline with filtering, search, and collapsible tool calls.

- **Trigger**: "view a session", "visualize a conversation", "replay a session"
- **Output**: Self-contained HTML file at `.claude/output/<session-id>.html`
- **Requires**: Python 3.10+ (via `uv run`)

### analyze-team-session (Task)

Analyze an agent team session export against the official Claude Code agent teams best practices. Produces a structured report with suitability verdict, 8-category scorecard, actionable recommendations, and an improved prompt rewrite.

- **Trigger**: "analyze this team session", "review my agent team run", "what went wrong with this session"
- **Output**: Markdown report at `.claude/output/<team-name>-analysis.md`
- **Requires**: WebFetch access to official docs

## Architecture Note

These are developer tools producing technical output. Voice and brand composition hooks are intentionally omitted — analysis reports and HTML viewers are not audience-facing content.

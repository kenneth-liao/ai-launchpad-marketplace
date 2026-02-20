# Integration Design: view-team-session + analyze-team-session -> agent-teams plugin

## Summary

Two related skills from the newsletter project — `view-team-session` (HTML session viewer with Python generator) and `analyze-team-session` (rubric-based session analysis) — integrate into a new `agent-teams/` foundation plugin. Both are TASK skills that do one thing well. Neither requires decomposition: they are already focused, single-purpose skills. A new plugin is needed because no existing plugin covers the "Claude Code agent teams" domain.

## Architecture

```
agent-teams/                          (NEW PLUGIN — foundation)
├── .claude-plugin/plugin.json
├── README.md
└── skills/
    ├── view-team-session/            (Task: generate HTML viewer)
    │   ├── SKILL.md
    │   ├── scripts/generate.py       (Python JSONL parser + HTML embedder)
    │   └── assets/template.html      (Self-contained HTML/CSS/JS viewer)
    └── analyze-team-session/         (Task: rubric-based analysis)
        └── SKILL.md
```

No orchestrator needed — these skills are invoked independently by the user, not sequenced together.

## Content Split

### 1. Task Skill: `agent-teams/skills/view-team-session/SKILL.md`

The skill definition describing how to generate HTML viewers from JSONL session logs. Covers usage instructions, session ID discovery, and output format. Moved from `temp/view-team-session/SKILL.md` with path references updated to remove project-specific hardcoded paths.

### 2. Script: `agent-teams/skills/view-team-session/scripts/generate.py`

Python script (432 lines) that discovers JSONL files, parses conversation events, handles agent team DM deduplication, and embeds data into the HTML template. Moved as-is — the script uses `Path(__file__).parent` for relative path resolution, so it works regardless of install location.

### 3. Asset: `agent-teams/skills/view-team-session/assets/template.html`

Self-contained HTML template (934 lines) with embedded CSS and JavaScript providing the session viewer UI: dark theme, agent-colored timeline, sidebar filtering, collapsible tool calls, markdown rendering, and markdown export. Moved as-is — no path dependencies.

### 4. Task Skill: `agent-teams/skills/analyze-team-session/SKILL.md`

The skill definition containing the complete 8-category rubric for evaluating agent team sessions against official best practices. Covers suitability, context sharing, task sizing, communication quality, file conflict avoidance, lead orchestration, cost efficiency, and cleanup. Fetches authoritative docs at runtime via WebFetch. Moved as-is — no path dependencies.

## Files to Create/Modify

| Action | File | Purpose |
|--------|------|---------|
| Create | `agent-teams/.claude-plugin/plugin.json` | Plugin metadata (v1.0.0) |
| Create | `agent-teams/README.md` | Plugin documentation |
| Create | `agent-teams/skills/view-team-session/SKILL.md` | Skill definition (updated paths) |
| Create | `agent-teams/skills/view-team-session/scripts/generate.py` | JSONL parser + HTML generator |
| Create | `agent-teams/skills/view-team-session/assets/template.html` | HTML viewer template |
| Create | `agent-teams/skills/analyze-team-session/SKILL.md` | Analysis skill definition |
| Delete | `temp/view-team-session/` | Source directory (after integration) |
| Delete | `temp/analyze-team-session/` | Source directory (after integration) |

## Functionality Preservation

| Original Capability | Destination | Notes |
|---------------------|-------------|-------|
| Generate HTML viewer from session ID | `agent-teams:view-team-session` | Identical — SKILL.md + scripts + assets |
| Auto-discover team JSONL files via teamName | `agent-teams:view-team-session` scripts/generate.py | Identical — no changes to script |
| Deduplicate inter-agent DMs | `agent-teams:view-team-session` scripts/generate.py | Identical — sender-copy dedup logic preserved |
| Session ID discovery helpers | `agent-teams:view-team-session` SKILL.md | Generalized — removed newsletter-specific project path |
| Dark theme viewer with filtering/search | `agent-teams:view-team-session` assets/template.html | Identical — template unchanged |
| Export filtered view as markdown | `agent-teams:view-team-session` assets/template.html | Identical — export function preserved |
| 8-category rubric evaluation | `agent-teams:analyze-team-session` | Identical — all 8 categories preserved |
| Fetch official docs via WebFetch | `agent-teams:analyze-team-session` | Identical — runtime doc fetching preserved |
| Structured analysis report output | `agent-teams:analyze-team-session` | Identical — report template preserved |
| Improved prompt rewrite | `agent-teams:analyze-team-session` | Identical — rewrite section preserved |
| Quality checklist and pitfall docs | Both skills | Identical — all checklists preserved |

## Design Decisions

1. **New plugin rather than extending an existing one.** No existing plugin covers "Claude Code agent teams." Research is about business/competitor analysis, not session analysis. Personal-assistant is Elle's memory. These skills form a coherent domain that warrants its own plugin.

2. **No decomposition needed.** Each skill does exactly one thing: view-team-session generates viewers, analyze-team-session evaluates sessions. Neither bundles unrelated concerns. The split rule does not apply.

3. **Voice and brand hooks omitted.** These are developer tools producing technical output (HTML viewers, analysis reports with rubric scores). They are not audience-facing content or branded assets. Applying voice transformation to a technical rubric evaluation would be inappropriate. This is a documented exception, not an oversight.

4. **Scripts and assets kept as skill subdirectories.** The `scripts/` and `assets/` directories in view-team-session are analogous to `references/` in content skills — supporting files that the skill depends on. They follow the same flat structure pattern.

5. **Hardcoded newsletter project path generalized.** The view-team-session SKILL.md referenced `~/.claude/projects/-Users-kennethliao-projects-ai-launchpad-newsletter/` for session discovery. Updated to use a generic `~/.claude/projects/<project>/` pattern since the skill works across any project.

6. **generate.py docstring path updated.** The script's usage comment referenced the old `.claude/skills/view-team-session/` path. Updated to use `{SKILL_DIR}` placeholder matching the SKILL.md pattern.

## Patterns Followed

- **Taxonomy decision tree**: Both skills classified as Task (question 3: "does it do one specific thing well?")
- **One plugin, one domain**: New plugin for a new domain rather than shoehorning into an existing plugin
- **Under 500 lines**: view-team-session SKILL.md (66 lines), analyze-team-session SKILL.md (221 lines)
- **Frontmatter with name and description**: Both skills have proper frontmatter
- **Quality checklist**: Both skills include verification checklists
- **Supporting files in skill subdirectories**: Scripts/assets pattern matches references/ pattern
- **Composition hooks documented exception**: Voice/brand omission explicitly justified (developer tools, not content creation)

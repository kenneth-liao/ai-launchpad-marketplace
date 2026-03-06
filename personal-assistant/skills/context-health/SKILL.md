---
name: context-health
description: Audit your Elle context system for staleness, contradictions, bloat, and missing data. Use when context feels stale, after major life changes, or periodically for maintenance. Also use when you notice Elle's responses feel generic or out of date.
user-invocable: true
model: claude-sonnet-4-6
---

# Context Health Audit

Audit the Elle context system at `~/.claude/.context/core/` for data quality issues.

## Audit Checklist

Run each check in order. Report findings as a summary table at the end.

### 1. Staleness Check

Read `~/.claude/.context/core/triggers.md`:
- Flag any dates in the past that haven't been cleaned up
- Flag events more than 30 days old

Read `~/.claude/.context/core/session.md`:
- Flag if "Current Focus" references work from a different session
- Flag if last-modified date is more than 7 days ago

Read `~/.claude/.context/core/projects.md`:
- Flag any "Active" projects that haven't been referenced in recent sessions

### 2. Bloat Check

For each file in `~/.claude/.context/core/`:
- Count lines (warn if > 100 lines)
- Count empty `<guide>` sections that could be filled with real data
- Flag excessive placeholder text

```bash
wc -l ~/.claude/.context/core/*.md
```

### 3. Contradiction Check

Read `~/.claude/.context/core/preferences.md` and `~/.claude/.context/core/rules.md`:
- Look for contradictions between preferences and rules
- Look for duplicate or near-duplicate entries
- Flag rules that may no longer apply

### 4. Gap Check

For each file, check if key sections are still placeholder text:
- `identity.md` -- Basic Info, Professional, Personal Life
- `preferences.md` -- Communication, Working Style
- `relationships.md` -- any entries at all?
- `triggers.md` -- any upcoming events?
- `workflows.md` -- any workflows defined?

### 5. Sync Check

Compare `~/.claude/rules/elle-core.md` against source files:
- Is the timestamp recent?
- Do the rules in elle-core.md match rules.md?
- Do the projects in elle-core.md match projects.md?

```bash
head -5 ~/.claude/rules/elle-core.md
grep "Last synced" ~/.claude/rules/elle-core.md
```

If out of sync, recommend running `/sync-context`.

### 6. Improvements Check

Read `~/.claude/.context/core/improvements.md`:
- Flag Active Proposals older than 30 days without status change
- Flag Friction Log entries with 2+ occurrences not yet promoted
- Report total pending proposals

### 7. System Freshness Check

Locate the evolve skill's platform capabilities reference:

```bash
EVOLVE_REF=""
# Source mode (marketplace repo)
if [ -f "<cwd>/personal-assistant/skills/evolve/references/platform-capabilities.md" ]; then
  EVOLVE_REF="<cwd>/personal-assistant/skills/evolve/references/platform-capabilities.md"
else
  # Deployed mode (plugin cache)
  EVOLVE_REF=$(find ~/.claude/plugins/cache -path "*/personal-assistant/*/skills/evolve/references/platform-capabilities.md" 2>/dev/null | sort -V | tail -1)
fi
```

If found, read the `## System State` section and check:
- Flag if "Last evolve run" is > 60 days ago or missing
- Flag if "Claude Code version at last audit" is "unknown" or differs from current
- Flag if "Platform docs last fetched" is > 60 days ago
- If System State section doesn't exist, flag as "never audited"

If reference file not found, skip with note: "Evolve reference files not found -- cannot check system freshness"

Recommend running `/evolve` if any flags are raised.

## Report Format

Present findings as:

| Check | Status | Details |
|-------|--------|---------|
| Staleness | OK / Warning | [specific issues] |
| Bloat | OK / Warning | [file: line count] |
| Contradictions | OK / Warning | [specific conflicts] |
| Gaps | OK / Warning | [empty sections] |
| Sync | OK / Warning | [sync status] |
| Improvements | OK / Warning | [stale proposals] |
| System Freshness | OK / Warning | [evolve run recency, version drift] |

**Recommended actions:** List specific fixes the user can take, prioritized by impact.

---
name: evolve
description: Research-driven self-upgrade pipeline for the Elle personal assistant. Fetches latest Claude Code features, audits Elle's architecture, plans upgrades, executes them, and verifies results. Use after Claude Code updates, when exploring new features, or periodically. Also use when the user says "let's modernize Elle", "evolve Elle", or "what Claude Code features are we missing".
user-invocable: true
---

# Evolve -- Research-Driven Self-Upgrade Pipeline

This skill researches the latest Claude Code platform state, audits Elle against it, plans upgrades, executes them, and verifies results. It auto-updates the reference files in this skill's `references/` directory to keep the knowledge base current between runs.

## Context Detection

Determine execution mode before doing anything else.

**Check:** Does `<cwd>/personal-assistant/.claude-plugin/plugin.json` exist AND does `<cwd>/.git` exist AND does `<cwd>/CONVENTIONS.md` exist?

- **YES -- Source Mode.** Operating in the marketplace repo where Elle is maintained. Operate on skill files, hooks, and references directly. Bump version and update CHANGELOG when done.

- **NO -- Deployed Mode.** Show this disclaimer:

  > **Note:** Evolve is designed to run from Elle's source repo where the plugin is maintained. Running here will audit and modify your installed copy at `~/.claude/plugins/cache/...`. These changes will be overwritten on the next plugin update.
  >
  > To run from source, navigate to your marketplace repo.
  >
  > Proceed with deployed copy?

  Wait for confirmation. If declined, stop.

Set `ELLE_ROOT`:
- Source mode: `<cwd>/personal-assistant`
- Deployed mode: the installed plugin path (find via the highest version directory in `~/.claude/plugins/cache/ai-launchpad/personal-assistant/`)

## Phase 1: Research

Run four research tasks in parallel using subagents. Each subagent summarizes its findings.

### 1A. Claude Code Changelog

Fetch latest Claude Code releases:

```
WebFetch: https://github.com/anthropics/claude-code/releases
```

Also check the raw changelog:

```
WebFetch: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
```

Extract from the last 3-5 releases:
- New tool capabilities or parameters
- New hook events or rule features
- Changes to skill loading, triggering, or frontmatter
- New agent/subagent patterns
- Deprecations or breaking changes
- Performance improvements relevant to skill design

### 1B. Anthropic Documentation

Search for and fetch latest Claude Code docs:

```
WebSearch: "Claude Code skills hooks rules" site:docs.anthropic.com
WebFetch: https://docs.anthropic.com/en/docs/claude-code/skills
WebFetch: https://docs.anthropic.com/en/docs/claude-code/hooks
```

Look for:
- Skill best practices and writing guidelines
- Hook configuration patterns
- Rules and context delivery mechanisms
- New features not covered in the changelog
- Model-specific guidance

### 1C. Skill-Creator Best Practices

Find and read the installed skill-creator:

```
Glob: ~/.claude/plugins/cache/*/skill-creator/*/skills/skill-creator/SKILL.md
```

Extract:
- Current skill writing patterns
- Progressive disclosure guidelines (line limits, reference files)
- Description optimization guidance (triggering, "pushy" descriptions)
- Testing and evaluation patterns

### 1D. Superpowers & Platform Patterns

Check official plugins for patterns worth adopting:

```
Glob: ~/.claude/plugins/cache/*/superpowers/*/skills/*/SKILL.md
```

Note structural patterns, frontmatter conventions, or composition techniques.

### Research Output

After all research completes, compile a Research Summary with sections:
- **New Claude Code Features** (from changelog + docs)
- **Updated Skill Best Practices** (from skill-creator)
- **Platform Patterns** (from superpowers and other plugins)
- **Deprecations & Breaking Changes**

In source mode: save to `<cwd>/.docs/upgrade-research/personal-assistant-<date>.md`

In deployed mode: present in-session only.

## Phase 2: Audit

### 2A. Skill Inventory

For each skill in `${ELLE_ROOT}/skills/`, read the SKILL.md and evaluate:
- Frontmatter fields (follows latest conventions from Phase 1?)
- Line count (warn if over 500)
- Whether it uses `references/` or `scripts/` for progressive disclosure
- Composition patterns (`plugin:skill` syntax used correctly?)
- Hardcoded paths or stale assumptions

### 2B. Architecture Audit

Check the deployed system state:

```bash
cat ${ELLE_ROOT}/hooks/hooks.json
ls -la ~/.claude/rules/elle-core.md
ls ~/.claude/.context/core/
cat ~/.claude/settings.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('hooks',{}), indent=2))" 2>/dev/null
```

Verify:
- SessionStart hooks registered (not UserPromptSubmit)
- elle-core.md exists in rules/
- No duplicate notification hooks between plugin and settings.json
- Output style set correctly
- All expected context files present

### 2C. Gap Analysis

Compare current state against Phase 1 research:

| Category | Check |
|----------|-------|
| Skill structure | Frontmatter follows latest conventions? Under 500 lines? Progressive disclosure? |
| Descriptions | Triggering descriptions specific enough per skill-creator guidance? |
| Patterns | Uses latest Claude Code features? No deprecated patterns? |
| Composition | Follows `plugin:skill` invocation syntax? |
| Hook design | Non-blocking? SessionStart < 2 seconds? Uses `additionalContext`? |

### 2D. Reference Freshness

Compare `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` and `best-practices.md` against research findings. Flag entries that are:
- Outdated (platform has changed)
- Missing (new capabilities not listed)
- Wrong (deprecated patterns still listed as current)

## Phase 3: Plan

Present a structured upgrade plan:

```
## Upgrade Plan: personal-assistant (Elle)

### Summary
- Current version: [from plugin.json]
- Proposed version: [with semver justification]
- Skills affected: N
- Reference files to update: N

### High Priority (Breaking/Deprecated)
1. [Change]
   - **Why**: [What's wrong or deprecated]
   - **What**: [Specific change]
   - **Risk**: [What could break]

### Medium Priority (New Features)
1. [Change]
   - **Why**: [What capability this enables]
   - **What**: [Specific change]

### Low Priority (Polish)
1. [Change]

### Not Recommended
- [Considered but rejected, and why]
```

<REQUIRED>
Wait for user approval before proceeding to Phase 4. The user may adjust priorities, skip items, or add their own.
</REQUIRED>

## Phase 4: Execute

Apply approved changes:

1. **One file at a time** -- read the full file before editing
2. **Preserve intent** -- upgrade patterns without changing what skills do
3. **Explain reasoning** -- prefer explaining why over heavy-handed MUSTs
4. **Keep prompts lean** -- remove things that aren't pulling their weight

### Reference File Updates

Update `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` and `best-practices.md` with findings from Phase 1. These files serve as "last known state" for future evolve runs.

### Version and Changelog (Source Mode Only)

After all changes:
- Bump version in `${ELLE_ROOT}/.claude-plugin/plugin.json` per semver
- Update `${ELLE_ROOT}/CHANGELOG.md` in Keep a Changelog format

## Phase 5: Verify

### Validation Checks

```bash
for skill in $(find ${ELLE_ROOT}/skills -name "SKILL.md"); do
  echo "=== $skill ==="
  wc -l "$skill"
  head -5 "$skill"
  echo ""
done
```

1. **Diff review** (source mode) -- show `git diff` for user review
2. **Frontmatter check** -- all skills have valid frontmatter with name and description
3. **Line count** -- no SKILL.md over 500 lines
4. **Cross-reference check** -- any `plugin:skill` references still valid
5. **Convention check** -- changes follow CONVENTIONS.md

### Deferred Findings

For recommendations the user deferred or rejected, log to `~/.claude/.context/core/improvements.md` as Active Proposals:

```
### ENHANCEMENT evolve-deferred -- [Short description]
- **Evidence**: Evolve audit [date] -- [what was found]
- **Current behavior**: [what exists now]
- **Proposed change**: [what was recommended]
- **Status**: Deferred
- **Source**: Evolve audit
```

### Final Summary

Report:
- Changes made (with file paths)
- Version bump applied (if source mode)
- CHANGELOG entry (if source mode)
- Reference files updated
- Deferred items logged to improvements.md
- Any manual follow-up needed

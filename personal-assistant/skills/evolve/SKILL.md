---
name: evolve
description: Research-driven self-upgrade pipeline for the Elle personal assistant. Fetches latest Claude Code features, audits Elle's architecture, plans upgrades, executes them, and verifies results. Use after Claude Code updates, when exploring new features, or periodically. Also use when the user says "let's modernize Elle", "evolve Elle", or "what Claude Code features are we missing".
user-invocable: true
disable-model-invocation: true
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

Run six research tasks in parallel using subagents. Each subagent summarizes its findings.

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

### 1B. Claude Code Documentation (Discovery-Driven)

Discover the Claude Code documentation landscape. Do NOT hardcode doc page URLs -- discover them dynamically.

1. Find available documentation:
   ```
   WebSearch: "Claude Code" site:docs.anthropic.com
   WebFetch: https://docs.anthropic.com/en/docs/claude-code/overview
   ```

2. From the search results and overview page, identify and fetch pages covering these categories:
   - **Core infrastructure**: skills, hooks, rules, CLAUDE.md
   - **Agent capabilities**: subagents/Agent tool, agent teams
   - **Plugin system**: commands, output styles, MCP servers, plugin architecture
   - **Memory & context**: auto memory, context management
   - **Configuration**: settings, permissions, tool gating
   - **Workflow**: worktrees, session management

3. For each fetched page, extract:
   - Current best practices and recommended patterns
   - New features not in `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md`
   - Deprecated patterns Elle might still use
   - Capabilities Elle doesn't leverage yet

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

### 1E. Plugin Architecture

Understand the full plugin specification and what Elle could be using:

1. Read the marketplace conventions (source mode only):
   ```
   Read: <cwd>/CONVENTIONS.md
   ```

2. Examine other installed plugins for structural patterns:
   ```
   Glob: ~/.claude/plugins/cache/*/*/skills/*/SKILL.md
   Bash: ls ~/.claude/plugins/cache/*/*/ | head -50
   ```
   Focus on: plugin.json fields, agents/ directories, MCP server integration, output style patterns.

3. Compare Elle's plugin structure against the full spec:
   - What directories does Elle have vs. what's available?
   - What plugin.json fields exist vs. what Elle uses?
   - Are other plugins using agents/ or MCP servers effectively?

### 1F. Model Capability Assessment

Check for model-level improvements that may supersede Elle's skills:

1. Search for recent Anthropic model releases:
   ```
   WebSearch: "Anthropic Claude" model release OR capability update site:anthropic.com
   WebSearch: "Claude" new capabilities 2026
   ```

2. Fetch the models overview page:
   ```
   WebFetch: https://docs.anthropic.com/en/docs/about-claude/models
   ```

3. Extract capabilities relevant to skill obsolescence:
   - Built-in tool use improvements (web search, code execution)
   - Reasoning and planning improvements
   - Multi-step task handling
   - Areas where dedicated prompting/orchestration adds less value

4. Compare against Elle's skill inventory:
   - For each skill, ask: "Does the model now do this well enough without specialized prompting?"
   - Flag skills where the answer is "yes" or "probably"

5. Cross-reference against `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` Model Capabilities table to detect changes since last run.

### Research Output

After all research completes, compile a Research Summary with sections:
- **New Claude Code Features** (from changelog + docs)
- **Updated Skill Best Practices** (from skill-creator)
- **Platform Patterns** (from superpowers and other plugins)
- **Plugin Architecture Gaps** (capabilities Elle doesn't use yet)
- **Deprecations & Breaking Changes**
- **Model Capability Overlap** (skills potentially superseded by model improvements)

In source mode: save to `<cwd>/.docs/upgrade-research/personal-assistant-<date>.md`

In deployed mode: present in-session only.

## Phase 1.5: Obsolescence Screen

Using research findings from Phase 1 (especially 1A, 1B, and 1F), evaluate whether each skill, agent, and major component in Elle is still necessary.

### Classification

For each skill and agent, assign one of:

| Rating | Meaning | Action |
|--------|---------|--------|
| **Active** | Platform/model doesn't replicate this. Skill adds clear value. | Proceed to structural audit in Phase 2 |
| **Augmented** | Platform/model handles the basics, but skill adds meaningful structure, guardrails, or workflow orchestration on top. | Audit normally, but note what the platform handles natively |
| **Superseded** | Platform/model now does this natively with comparable quality. Skill adds marginal value over a direct prompt. | Skip structural audit. Recommend removal in Phase 3 plan. |

### How to Evaluate

For each skill, answer these three questions:

1. **What does this skill do that a direct prompt to Claude cannot?**
   If the answer is only "it saves typing a prompt" -- likely Superseded.

2. **Does this skill enforce a process, workflow, or multi-step structure?**
   Process skills (TDD, debugging, code review) remain valuable even when the model can do each step -- the skill enforces discipline. Likely Active.

3. **Has the platform added a native feature that replaces this skill's core function?**
   Example: Claude Code added native web search -> a "web research" skill that just wraps web search is Superseded. But a "competitor analysis" skill that orchestrates multiple searches into a structured report may be Augmented.

### Output

Present results as a table:

| Component | Type | Rating | Rationale |
|-----------|------|--------|-----------|
| [name] | skill/agent | Active/Augmented/Superseded | [1-line reason] |

If any component is rated **Superseded**, flag it for the user:

> **Obsolescence flag:** [N] component(s) appear superseded by platform/model capabilities. These will appear in the "Recommend Removal" section of the upgrade plan. Review the rationale -- override to Active or Augmented if you disagree.

Proceed to Phase 2, skipping structural audit for Superseded components.

## Phase 2: Audit

### 2A. Skill Inventory

For each skill in `${ELLE_ROOT}/skills/`, read the SKILL.md and evaluate:
- Frontmatter fields (follows latest conventions from Phase 1?)
- Line count (warn if over 500)
- Whether it uses `references/` or `scripts/` for progressive disclosure
- Composition patterns (`plugin:skill` syntax used correctly?)
- Hardcoded paths or stale assumptions
- Obsolescence rating from Phase 1.5 (skip detailed audit for Superseded components)

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
| Plugin architecture | Using all beneficial plugin components (agents, MCP, output styles)? |
| System state | Platform capabilities and best practices references current? |

### 2D. Reference Freshness

Compare `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` and `best-practices.md` against research findings. Flag entries that are:
- Outdated (platform has changed)
- Missing (new capabilities not listed)
- Wrong (deprecated patterns still listed as current)

### 2E. Full Plugin Inventory

Check all plugin components, not just skills:

```bash
echo "=== Skills ===" && ls ${ELLE_ROOT}/skills/
echo "=== Hooks ===" && cat ${ELLE_ROOT}/hooks/hooks.json 2>/dev/null
echo "=== Output Styles ===" && ls ${ELLE_ROOT}/output-styles/ 2>/dev/null
echo "=== Plugin.json ===" && cat ${ELLE_ROOT}/.claude-plugin/plugin.json
echo "=== Agents ===" && ls ${ELLE_ROOT}/agents/ 2>/dev/null || echo "No agents/ directory"
```

Evaluate:
- **Output styles**: leveraging latest features? Under 120 lines?
- **Plugin.json**: all available fields used correctly?
- **Missing components**: would agents/ or MCP servers benefit Elle?
- **Structural patterns**: anything other plugins do that Elle should adopt?

### 2F. System State Check

Read `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` System State section:
- Last evolve run date -- flag if > 60 days ago
- Claude Code version at last audit -- compare against latest from Phase 1A
- Elle version -- compare against plugin.json
- Platform docs last fetched -- flag if > 60 days ago

If System State section is missing, flag as "first evolve run" and note that all findings are new.

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

### Superseded (Recommend Removal)
Components flagged as Superseded in Phase 1.5. Review before approving removal.

1. [Component name] ([type])
   - **What it does**: [1-line summary]
   - **What replaces it**: [platform feature or model capability]
   - **Migration**: [user-facing steps if any -- update docs, remove references]
   - **Risk**: [what's lost if removed]

### Medium Priority (New Features)
1. [Change]
   - **Why**: [What capability this enables]
   - **What**: [Specific change]

### Low Priority (Polish)
1. [Change]

### Not Recommended
- [Considered but rejected, and why]
```

For removed components in source mode:
- Add CHANGELOG entry under "Removed"
- Version bump: MINOR if user-invocable skill, PATCH if internal-only component

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

### Model Capabilities Update

Update the Model Capabilities table in `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` with findings from Phase 1F. Add new capabilities, update proficiency levels, and revise skill design implications.

### System State Update

After all changes are applied, update the System State section in `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md`:

| Field | Value |
|-------|-------|
| Elle version | [from plugin.json after bump] |
| Last evolve run | [today's date] |
| Claude Code version at last audit | [latest version from Phase 1A research] |
| Platform docs last fetched | [today's date] |
| Model capabilities last assessed | [today's date] |

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

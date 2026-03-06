---
name: upgrade-plugin
description: Upgrade a plugin's skills, hooks, and patterns to align with latest Claude Code capabilities and best practices. Use when a plugin needs modernization, after Claude Code updates, or when the user says "upgrade plugin", "modernize plugin", or "update plugin to latest patterns".
user-invocable: true
disable-model-invocation: true
---

# Upgrade Plugin

Upgrade a plugin's skills, hooks, and patterns to align with the latest Claude Code capabilities, model features, and skill-writing best practices.

**Arguments:** $ARGUMENTS -- plugin name (e.g., `creator-stack`, `scheduler`) and optional focus areas. If no plugin specified, ask which one.

## Locate Target Plugin

Find the plugin to upgrade:

1. Check `<cwd>/<plugin-name>/.claude-plugin/plugin.json` (source mode -- marketplace repo)
2. If not found, check `~/.claude/plugins/cache/*/<plugin-name>/` (installed mode)

If neither found, list available plugins and ask the user to clarify.

Set `PLUGIN_ROOT` to the resolved path.

---

## Phase 1: Research Latest Context

Run six research tasks in parallel using subagents. Each subagent summarizes its findings.

### 1A. Claude Code Changelog

Fetch the latest Claude Code releases:

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
   - New features relevant to the target plugin
   - Deprecated patterns the plugin might still use
   - Capabilities the plugin doesn't leverage yet

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

Understand the full plugin specification and what the target plugin could be using:

1. Read the marketplace conventions (if in source mode):
   ```
   Read: <cwd>/CONVENTIONS.md
   ```

2. Examine other installed plugins for structural patterns:
   ```
   Glob: ~/.claude/plugins/cache/*/*/skills/*/SKILL.md
   Bash: ls ~/.claude/plugins/cache/*/*/ | head -50
   ```
   Focus on: plugin.json fields, agents/ directories, MCP server integration, output style patterns.

3. Compare the target plugin's structure against the full spec:
   - What directories does it have vs. what's available?
   - What plugin.json fields exist vs. what it uses?
   - Are other plugins using components this one doesn't?

### 1F. Model Capability Assessment

Check for model-level improvements that may supersede skills in the target plugin:

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

4. Compare against the target plugin's skill inventory:
   - For each skill, ask: "Does the model now do this well enough without specialized prompting?"
   - Flag skills where the answer is "yes" or "probably"

### Research Output

After all research completes, compile a Research Summary with sections:
- **New Claude Code Features** (from changelog + docs)
- **Updated Skill Best Practices** (from skill-creator)
- **Platform Patterns** (from superpowers and other plugins)
- **Plugin Architecture Gaps** (capabilities the target plugin doesn't use yet)
- **Deprecations & Breaking Changes**
- **Model Capability Overlap** (skills potentially superseded by model improvements)

Save to `<cwd>/.docs/upgrade-research/<plugin-name>-<date>.md` for reference.

---

## Phase 1.5: Obsolescence Screen

Using research findings from Phase 1 (especially 1A, 1B, and 1F), evaluate whether each skill, agent, and major component in the target plugin is still necessary.

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

---

## Phase 2: Audit Current Plugin

Read the target plugin's full structure and evaluate against the research findings.

### 2A. Plugin Inventory

```bash
echo "=== Plugin.json ===" && cat ${PLUGIN_ROOT}/.claude-plugin/plugin.json
echo "=== Skills ===" && find ${PLUGIN_ROOT}/skills -name "SKILL.md" -type f 2>/dev/null
echo "=== Hooks ===" && cat ${PLUGIN_ROOT}/hooks/hooks.json 2>/dev/null || echo "No hooks"
echo "=== Output Styles ===" && ls ${PLUGIN_ROOT}/output-styles/ 2>/dev/null || echo "No output styles"
echo "=== Agents ===" && ls ${PLUGIN_ROOT}/agents/ 2>/dev/null || echo "No agents"
echo "=== Test Suites ===" && find ${PLUGIN_ROOT}/skills -path "*/tests/evals.json" -type f 2>/dev/null || echo "No test suites"
echo "=== All Files ===" && find ${PLUGIN_ROOT} -type f -not -path "*/.DS_Store" -not -path "*/node_modules/*"
```

For each skill, read and note:
- Frontmatter fields (name, description, user-invocable, etc.)
- Line count (should be under 500)
- Whether it uses references/ or scripts/
- Composition patterns (does it invoke other skills?)
- Any hardcoded paths or assumptions
- Obsolescence rating from Phase 1.5 (skip detailed audit for Superseded components)

For other components, evaluate:
- **Output styles**: under 120 lines? Leveraging latest features?
- **Plugin.json**: all available fields used correctly?
- **Hooks**: using latest events? Non-blocking?
- **Missing components**: would agents/ or MCP servers benefit this plugin?

### 2B. Gap Analysis

Compare current state against research findings:

| Category | Check |
|----------|-------|
| Skill structure | Frontmatter follows latest conventions? Under 500 lines? Progressive disclosure? |
| Descriptions | Triggering descriptions specific enough per skill-creator guidance? |
| Patterns | Uses latest Claude Code features? No deprecated patterns? |
| Composition | Follows `plugin:skill` invocation syntax? Voice/brand hooks applied correctly? |
| Scripts | Bundled scripts use best practices? No reinventing common patterns? |
| Plugin architecture | Using all beneficial plugin components (agents, MCP, output styles)? |
| Component coverage | All existing components up to date with latest conventions? |
| Test coverage | Skills have `tests/evals.json`? Flag untested skills as a gap. |

### 2C. Project Conventions Check

Read and verify against marketplace conventions:

```
Read: <cwd>/CONVENTIONS.md
Read: <cwd>/CLAUDE.md
```

Ensure the plugin follows:
- Single-responsibility skill design
- Correct skill categorization (Task / Orchestrator / Knowledge)
- Voice and brand hook presence where required
- Flat layout with no nested SKILL.md files

---

## Phase 3: Upgrade Plan

Present a structured upgrade plan organized by priority:

```
## Upgrade Plan: <plugin-name>

### Summary
- Current version: X.Y.Z
- Proposed version: X.Y.Z (justify MAJOR/MINOR/PATCH)
- Total changes: N skills affected
- Components affected: [skills, hooks, output styles, plugin.json]

### High Priority (Breaking/Deprecated)
1. [Change description]
   - **Why**: [What's wrong or deprecated]
   - **What**: [Specific change to make]
   - **Risk**: [What could break]

### Superseded (Recommend Removal)
Components flagged as Superseded in Phase 1.5. Review before approving removal.

1. [Component name] ([type])
   - **What it does**: [1-line summary]
   - **What replaces it**: [platform feature or model capability]
   - **Migration**: [user-facing steps if any -- update docs, remove references]
   - **Risk**: [what's lost if removed]

### Medium Priority (New Features/Improvements)
1. [Change description]
   - **Why**: [What new capability this enables]
   - **What**: [Specific change to make]

### Low Priority (Polish/Optimization)
1. [Change description]

### Not Recommended
- [Things considered but rejected, and why]
```

<REQUIRED>
Wait for user approval before proceeding. The user may adjust priorities, skip items, or add their own.
</REQUIRED>

---

## Phase 4: Execute Upgrades

Apply approved changes systematically:

1. **One file at a time** -- read the full file before editing
2. **Preserve intent** -- upgrade patterns without changing what the skill does
3. **Explain reasoning** -- prefer explaining why over heavy-handed MUSTs
4. **Keep prompts lean** -- remove things that aren't pulling their weight

### For each file being upgraded:
- Read the current file fully
- Apply the approved changes
- Verify line count stays under limits (500 for SKILL.md, 120 for output styles)
- Check that frontmatter is correct
- Ensure composition references use `plugin:skill` syntax

### Version Bump

After all changes:
- Update `plugin.json` version according to semver
- Update `CHANGELOG.md` with all changes in Keep a Changelog format

---

## Phase 5: Verify

Before declaring done:

```bash
for skill in $(find ${PLUGIN_ROOT}/skills -name "SKILL.md"); do
  echo "=== $skill ==="
  wc -l "$skill"
  head -5 "$skill"
  echo ""
done
```

1. **Diff review** -- show `git diff` of all changes for user review
2. **Frontmatter check** -- verify all skills have valid frontmatter
3. **Line count check** -- no SKILL.md over 500 lines
4. **Convention check** -- all changes follow CONVENTIONS.md
5. **Cross-reference check** -- any `plugin:skill` references still valid
6. **Test suite check** -- If any modified skills have `tests/evals.json`, offer to run them:
   - "N skills were modified. M have test suites. Run them now?"
   - If user approves, invoke `plugin-tools:test-skill` for each skill with tests
   - Surface any regressions before the user approves the upgrade

Present a final summary:
- Changes made (with file paths)
- Version bump applied
- CHANGELOG entry
- Any manual follow-up needed

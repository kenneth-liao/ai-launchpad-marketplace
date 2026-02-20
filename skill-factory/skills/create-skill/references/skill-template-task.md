# Task Skill Template

Use this template when creating a new **Task** skill. Task skills do one thing well -- they research, write, generate, design, or analyze. They are the workhorses of the framework.

Fill in all sections. Replace `{placeholder}` values with skill-specific content. Remove `<!-- comments -->` before finalizing.

---

## Template

```markdown
---
name: {skill-name}
description: "{One sentence: what it does, when to use it, what it produces. Be specific -- this determines when Claude uses the skill.}"
---

# {Skill Title}

## Overview

<!-- 2-3 sentences. State what single thing this skill does well. -->

**Core Principle**: {The one non-negotiable rule for this skill.}

## When to Use

Use this skill when:
- {Trigger condition 1}
- {Trigger condition 2}
- {Trigger condition 3}

## Prerequisites

<!-- CONDITIONAL: Include this section only for script-bearing task skills. Remove for standard task skills. -->

This skill requires [`uv`](https://docs.astral.sh/uv/) for zero-setup script execution.

**Check:** Run `uv --version` to verify installation.

**If not installed:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Scripts

<!-- CONDITIONAL: Include this section only for script-bearing task skills. Remove for standard task skills. -->

All executable scripts live in `scripts/` and use [PEP 723](https://peps.python.org/pep-0723/) inline dependencies for zero-setup execution:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "{dependency-name}>=version",
# ]
# ///
```

**Execution:** Always use `uv run`, never raw `python3`:
```bash
uv run <skill_dir>/scripts/{script_name}.py [args]
```

**Why uv + PEP 723:** Zero setup (dependencies auto-install on first run), portable (no virtualenv management), reproducible (exact dependencies declared inline per script).

### Script Conventions

| Convention | Rule |
|---|---|
| Location | `scripts/` directory within skill |
| Dependencies | PEP 723 inline block in every `.py` file |
| Execution | `uv run` only, never `python3` directly |
| Return format | Consistent dict: `{success, path/data, error, metadata}` |
| CLI interface | argparse with clear `--help` |
| Python API | Functions importable for downstream skill integration |
| Error handling | Automatic retry with exponential backoff where appropriate |
| Path handling | Absolute paths, auto-create output directories |

### Downstream Integration

Other skills consume script-bearing skills via two patterns:

**CLI pattern** (simple, preferred):
```bash
uv run <skill_dir>/scripts/{script}.py "args" --flag value
```

**Python import pattern** (programmatic access):
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("<skill_dir>/scripts")))
from {script} import {function}
result = {function}(args)
```

## Content Type Resolution

<!-- Include if the skill handles multiple content types. Omit for single-type skills. -->

| Content Type | Reference File | Key Focus |
|---|---|---|
| {Type 1} | `references/{type-1-reference}.md` | {What this reference provides} |
| {Type 2} | `references/{type-2-reference}.md` | {What this reference provides} |

**MANDATORY**: Read the relevant reference file before proceeding.

## Workflow

### Step 1: {First Action}

### Step 2: {Second Action}

### Step 3: {Third Action}

### Step 4: Verify Against Checklist

### Step 5: Present and Refine

## Voice Application

ALWAYS invoke `writing:voice` before finalizing any written output. Voice is applied after the structural draft is complete but before brand compliance.

**Invocation point**: After drafting is complete, before presenting to the user.

## Brand Compliance

When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns.

**Invocation point**: After voice application, as the final quality gate.

## Quality Checklist

- [ ] {Skill-specific check 1}
- [ ] {Skill-specific check 2}
- [ ] `writing:voice` invoked and voice rules applied
- [ ] `branding-kit:brand-guidelines` invoked and brand compliance verified
- [ ] No placeholder content or unresolved TODOs

## Common Pitfalls

1. **{Pitfall 1}**: {What goes wrong and how to avoid it.}
2. **{Pitfall 2}**: {What goes wrong and how to avoid it.}
3. **{Pitfall 3}**: {What goes wrong and how to avoid it.}
```

---

## Template Rules

1. **Frontmatter description is critical** -- It determines when Claude triggers the skill.
2. **One thing well** -- If the workflow has more than 7 steps, consider splitting.
3. **Voice hook is mandatory** -- Every task skill producing written output must invoke `writing:voice`.
4. **Brand hook is mandatory** -- Every task skill producing branded assets must invoke `branding-kit:brand-guidelines`.
5. **References for platform knowledge** -- Platform-specific patterns go in `references/`, not in SKILL.md.
6. **Quality checklist is mandatory** -- Every task skill must include a verification checklist.
7. **Under 500 lines** -- If SKILL.md exceeds this, move detailed content to reference files.
8. **Script-bearing skills use uv** -- If the skill includes Python scripts, they must use PEP 723 inline dependencies and `uv run` execution. Never reference `python3` or `pip install` as the primary execution method.

## Examples from the System

- `writing:copywriting` -- Content Type Resolution table, 7-step workflow, voice and brand hooks
- `content-strategy:title` -- Platform references, verification checklist, rejection criteria
- `content-strategy:hook` -- Forbidden patterns, hook patterns, quality verification
- `content-strategy:research` -- Platform-agnostic design, subagent support, output structure
- `visual-design:thumbnail` -- Skill integration (`art:nanobanana`), brand compliance, reference images
- `art:nanobanana` -- Script-bearing task skill: `scripts/` directory, PEP 723 inline deps, uv prerequisite check, CLI + Python API

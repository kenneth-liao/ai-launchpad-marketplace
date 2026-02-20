# Design: UV Script Architecture for Skill-Factory

## Summary

Add a **script-bearing task skill** variant to the skill-factory framework. When a task skill includes executable Python scripts, the framework activates a conditional section that enforces `uv` + PEP 723 inline dependencies for zero-setup, portable script execution. Three files are modified; no new files, categories, or templates are created.

## Motivation

The `art:nanobanana` skill demonstrates a powerful pattern: Python scripts with PEP 723 inline dependencies executed via `uv run`. This gives skills:

- **Zero setup** — dependencies install automatically on first run
- **Portability** — no virtualenv management, no pip install steps
- **Reproducibility** — exact dependencies declared inline per script

This pattern is not captured in the skill-factory framework today. New skill authors have no guidance on how to structure skills with executable scripts, leading to inconsistent dependency management.

## Architecture

```
skill-factory/skills/create-skill/
├── SKILL.md                          # Step 1: adds script detection question
│                                     # Step 6: loads script variant
├── references/
│   ├── taxonomy.md                   # Adds script-bearing sub-classification
│   ├── skill-template-task.md        # Adds conditional Scripts Architecture section
│   └── (other files unchanged)
```

## Design Decisions

1. **uv + Python only** — No multi-runtime support (Node/npx, shell). Keeps framework focused. Other runtimes can be added later if needed.

2. **Conditional section, not separate template** — The script-bearing variant is an optional section within the existing task template, not a new template. Avoids template proliferation.

3. **Task template only** — Only task skills get the scripts section. Orchestrators delegate (no scripts), knowledge/personality don't execute code.

4. **Check + install instructions, not auto-install** — If uv is missing, the skill tells the user how to install it. Respects user control over their system.

5. **Sub-classification, not new category** — Script-bearing is a variant of Task, not a 6th taxonomy category. The taxonomy stays at 5 categories.

## Changes

### 1. Taxonomy Update (`references/taxonomy.md`)

Add a sub-classification question under the Task category:

> After classifying as Task, ask: "Does this task skill include executable Python scripts (API wrappers, data processors, image generators, etc.)?"
>
> If yes → **Script-Bearing Task Skill**: requires `scripts/` directory, PEP 723 inline dependencies, `uv` prerequisite check, and script documentation in SKILL.md.
>
> If no → Standard Task Skill (no changes).

### 2. Task Template Update (`references/skill-template-task.md`)

Add a conditional section activated for script-bearing task skills. Inserted after "When to Use", before "Workflow":

#### Prerequisites Section

```markdown
## Prerequisites

This skill requires [uv](https://docs.astral.sh/uv/) for zero-setup script execution.

**Check:** Run `uv --version` to verify installation.

**If not installed:**
\`\`\`bash
curl -LsSf https://astral.sh/uv/install.sh | sh
\`\`\`
```

#### Scripts Section

```markdown
## Scripts

All executable scripts live in `scripts/` and use PEP 723 inline dependencies:

\`\`\`python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "dependency-name>=version",
# ]
# ///
\`\`\`

**Execution:** Always use `uv run`, never raw `python3`:
\`\`\`bash
uv run <skill_dir>/scripts/script_name.py [args]
\`\`\`
```

#### Script Conventions Table

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

#### Downstream Integration Patterns

Two patterns for how other skills consume script-bearing skills:

1. **CLI pattern** — `uv run <skill_dir>/scripts/script.py "args"`
2. **Python import pattern** — `sys.path.insert` + import for programmatic access

### 3. Create-Skill Workflow Update (`SKILL.md`)

**Step 1** — Add after existing questions:
> "Does this skill include executable Python scripts?"

**Step 6** — When loading template for script-bearing task skills:
1. Load `skill-template-task.md`
2. Activate the conditional Scripts Architecture section
3. Generated SKILL.md includes: Prerequisites, Scripts, Script Conventions, and integration patterns

**Step 8** — Add validation rules for script-bearing task skills:

| Rule | Check |
|---|---|
| `scripts/` directory exists | Skill directory contains `scripts/` |
| PEP 723 block present | Every `.py` in `scripts/` has `# /// script` block |
| `requires-python` specified | PEP 723 block includes Python version constraint |
| `dependencies` specified | PEP 723 block includes dependency list |
| No raw python3 | SKILL.md never references `python3` directly — always `uv run` |
| Prerequisites section present | SKILL.md includes uv prerequisite check |
| Return format documented | Script API returns consistent dict structure |
| CLI documented | `--help` usage documented in SKILL.md |

## Files to Modify

| Action | File | Purpose |
|--------|------|---------|
| Modify | `skill-factory/skills/create-skill/SKILL.md` | Add script detection (Step 1), template variant (Step 6), validation rules (Step 8) |
| Modify | `skill-factory/skills/create-skill/references/taxonomy.md` | Add script-bearing sub-classification under Task |
| Modify | `skill-factory/skills/create-skill/references/skill-template-task.md` | Add conditional Scripts Architecture section |

## Patterns Followed

- Conditional section within existing template (no template proliferation)
- Sub-classification within existing category (no taxonomy expansion)
- Validation rules are additive (existing rules unchanged)
- art:nanobanana as the reference implementation of this pattern

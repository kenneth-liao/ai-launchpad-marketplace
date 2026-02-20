# UV Script Architecture Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add script-bearing task skill support (uv + PEP 723) to the skill-factory framework.

**Architecture:** Three files are modified to add a conditional "script-bearing" variant to the task skill workflow. Step 1 of create-skill detects scripts, taxonomy gains a sub-classification, and the task template gains a conditional Scripts Architecture section. Validation rules enforce the pattern.

**Tech Stack:** Markdown skill files (no code changes, pure documentation/framework updates)

---

### Task 1: Update Taxonomy with Script-Bearing Sub-Classification

**Files:**
- Modify: `skill-factory/skills/create-skill/references/taxonomy.md:22-26`

**Step 1: Read the current Task category section**

Verify the current content at lines 22-26:
```markdown
### Task

**What it is**: Does one thing well. Researches, writes, generates, designs. The workhorses of the system.
**Key signal**: Produces a specific output (content, visual, analysis). Invoked by users or orchestrators.
**Examples**: `writing:copywriting`, `content-strategy:research`, `content-strategy:title`, `content-strategy:hook`, `visual-design:thumbnail`, `visual-design:social-graphic`
**Plugin home**: Foundation plugins (`writing/`, `content-strategy/`, `visual-design/`).
```

**Step 2: Add Script-Bearing variant to the Task category**

After the existing Task section (line 27, before `### Orchestrator`), insert:

```markdown

#### Script-Bearing Task Skills

Some task skills include executable Python scripts (API wrappers, data processors, image generators). These are still Task skills, but they require additional structure:

**Key signal**: The skill's output depends on running Python scripts via `uv run`.
**Additional requirements**: `scripts/` directory, PEP 723 inline dependencies, `uv` prerequisite check.
**Example**: `art:nanobanana` — image generation via Python scripts with google-genai dependency.

After classifying a skill as Task, ask: "Does this task skill include executable Python scripts?" If yes, apply the script-bearing variant during template application (Step 6).
```

**Step 3: Add script-bearing note to the Quick Reference table**

Update the Task row in the Quick Reference table (line 85) to add the script-bearing column info. Change:

```markdown
| Task | Content, visuals, analysis | Users or orchestrators | Voice hook, brand hook, quality checklist |
```

To:

```markdown
| Task | Content, visuals, analysis | Users or orchestrators | Voice hook, brand hook, quality checklist. If script-bearing: `scripts/`, PEP 723, uv prerequisite |
```

**Step 4: Verify the file**

Read the full file and confirm:
- Script-bearing variant is under Task, not a new top-level category
- Decision tree is unchanged (still 5 categories)
- Quick reference table reflects the variant

**Step 5: Commit**

```bash
git add skill-factory/skills/create-skill/references/taxonomy.md
git commit -m "docs(skill-factory): add script-bearing task skill sub-classification to taxonomy"
```

---

### Task 2: Add Scripts Architecture Section to Task Template

**Files:**
- Modify: `skill-factory/skills/create-skill/references/skill-template-task.md:30-41`

**Step 1: Read the current template**

Verify current content. The conditional section will be inserted between "When to Use" (ends ~line 31) and "Content Type Resolution" (starts ~line 33).

**Step 2: Insert the conditional Scripts Architecture section**

After the "When to Use" section (after line 31 `- {Trigger condition 3}`), insert:

````markdown

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
````

**Step 3: Add a new Template Rule for scripts**

After the existing Template Rules (line 92 `7. **Under 500 lines**...`), add:

```markdown
8. **Script-bearing skills use uv** -- If the skill includes Python scripts, they must use PEP 723 inline dependencies and `uv run` execution. Never reference `python3` or `pip install` as the primary execution method.
```

**Step 4: Add nanobanana as a script-bearing example**

After the existing Examples from the System (line 100 `- \`visual-design:thumbnail\`...`), add:

```markdown
- `art:nanobanana` -- Script-bearing task skill: `scripts/` directory, PEP 723 inline deps, uv prerequisite check, CLI + Python API
```

**Step 5: Verify the file**

Read the full file and confirm:
- Conditional sections are clearly marked with `<!-- CONDITIONAL -->` comments
- Template still flows logically for both standard and script-bearing task skills
- File is well under 500 lines

**Step 6: Commit**

```bash
git add skill-factory/skills/create-skill/references/skill-template-task.md
git commit -m "docs(skill-factory): add script-bearing sections to task skill template"
```

---

### Task 3: Update Create-Skill Workflow (Step 1, Step 6, Step 8)

**Files:**
- Modify: `skill-factory/skills/create-skill/SKILL.md:27-36` (Step 1)
- Modify: `skill-factory/skills/create-skill/SKILL.md:95-107` (Step 6)
- Modify: `skill-factory/skills/create-skill/SKILL.md:128-173` (Step 8)

**Step 1: Add script detection question to Step 1**

After line 36 (`If the user's description suggests the skill is trying to do two things...`), add:

```markdown

If the skill is classified as a **Task** in Step 2, also ask:
- **Scripts**: Does the skill include executable Python scripts (API wrappers, data processors, image generators)? If yes, this is a **script-bearing task skill** and will use the uv + PEP 723 architecture in Step 6.
```

**Step 2: Update Step 6 to handle script-bearing variant**

After line 107 (`**MANDATORY**: Read the template file before generating the skill.`), add:

```markdown

**For script-bearing task skills**: After loading `references/skill-template-task.md`, activate the conditional sections marked `<!-- CONDITIONAL -->`. These add:
- Prerequisites section with `uv` check and install instructions
- Scripts section with PEP 723 pattern and script conventions
- Downstream Integration patterns for CLI and Python API consumption

Use `art:nanobanana` as the reference implementation for this pattern.
```

**Step 3: Add script-bearing validation rules to Step 8**

After the existing Task skills validation (line 145, after `- [ ] Does one thing well -- not trying to be two skills`), add:

```markdown

For **Script-bearing task skills** (in addition to standard Task validation):
- [ ] `scripts/` directory exists in the skill directory
- [ ] Every `.py` file in `scripts/` contains a PEP 723 inline dependency block (`# /// script`)
- [ ] PEP 723 block includes `requires-python` version constraint
- [ ] PEP 723 block includes `dependencies` list (can be empty `[]`)
- [ ] SKILL.md never references `python3` as the primary execution method -- always `uv run`
- [ ] Prerequisites section present with `uv` check and install instructions
- [ ] Script return format documented (consistent dict structure)
- [ ] CLI usage with `--help` documented in SKILL.md
```

**Step 4: Add script-related pitfall**

After line 218 (pitfall 7 `**Skipping validation**...`), add:

```markdown
8. **Raw python3 in script-bearing skills**: Using `python3 script.py` instead of `uv run script.py`. The uv + PEP 723 pattern is the standard for zero-setup portability. Always use `uv run`.
```

**Step 5: Verify the file**

Read the full file and confirm:
- Step 1 mentions script detection
- Step 6 describes the conditional template activation
- Step 8 has the new validation rules clearly separated under "Script-bearing task skills"
- New pitfall added
- File is still under 500 lines (currently 236, additions add ~30 lines = ~266 total)

**Step 6: Commit**

```bash
git add skill-factory/skills/create-skill/SKILL.md
git commit -m "feat(skill-factory): add uv script architecture to create-skill workflow"
```

---

### Task 4: Verify and Update Plugin Version

**Files:**
- Modify: `skill-factory/.claude-plugin/plugin.json`
- Modify: `skill-factory/README.md`

**Step 1: Read current plugin.json**

Read `skill-factory/.claude-plugin/plugin.json` and note the current version.

**Step 2: Bump the version**

Increment the minor version (e.g., `1.1.0` -> `1.2.0`) to reflect the new framework capability.

**Step 3: Read and update README**

Read `skill-factory/README.md`. Add a note about the script-bearing task skill support under the create-skill description. Keep it brief — one sentence mentioning uv + PEP 723 support for task skills with Python scripts.

**Step 4: Commit**

```bash
git add skill-factory/.claude-plugin/plugin.json skill-factory/README.md
git commit -m "chore(skill-factory): bump version for uv script architecture support"
```

---

### Task 5: Final Validation

**Step 1: Read all modified files end-to-end**

Read these three files completely:
1. `skill-factory/skills/create-skill/SKILL.md`
2. `skill-factory/skills/create-skill/references/taxonomy.md`
3. `skill-factory/skills/create-skill/references/skill-template-task.md`

**Step 2: Cross-reference with design doc**

Read `docs/plans/2026-02-20-uv-script-architecture-design.md` and verify every design decision is reflected in the implementation:

- [ ] Taxonomy has script-bearing sub-classification under Task
- [ ] Task template has conditional Prerequisites section with uv check
- [ ] Task template has conditional Scripts section with PEP 723 pattern
- [ ] Task template has script conventions table
- [ ] Task template has downstream integration patterns
- [ ] Create-skill Step 1 asks about scripts
- [ ] Create-skill Step 6 describes conditional template activation
- [ ] Create-skill Step 8 has 8 script-bearing validation rules
- [ ] No new categories added (still 5)
- [ ] No new template files created
- [ ] All files under 500 lines

**Step 3: Verify against nanobanana as reference**

Spot-check that the patterns described in the template match what `art:nanobanana` actually does:
- PEP 723 block format matches `art/skills/nanobanana/scripts/generate.py` lines 15-20
- uv run execution pattern matches `art/skills/nanobanana/SKILL.md` quick start section
- Prerequisites pattern matches `art/skills/nanobanana/SKILL.md` prerequisites section

**Step 4: Report completion**

Confirm all validation passes. The skill-factory now supports script-bearing task skills.

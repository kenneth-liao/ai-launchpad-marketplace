# Integrate-Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a meta-skill in `skill-factory/` that formalizes integrating skills from any source into the composable skill architecture.

**Architecture:** Single SKILL.md file in `skill-factory/skills/integrate-skill/`, no reference files (reads from `create-skill/references/`). Plugin version bump and README update.

**Tech Stack:** Markdown (SKILL.md), JSON (plugin.json)

**Design Doc:** `docs/plans/2026-02-20-integrate-skill-design.md`

---

### Task 1: Load Skill Authoring Best Practices

**Step 1: Invoke skill-creator:skill-creator**

Invoke `skill-creator:skill-creator` to load skill authoring best practices. Apply its guidance to all subsequent tasks. This corresponds to create-skill Step 4.

**Step 2: Invoke superpowers:writing-skills**

Invoke `superpowers:writing-skills` to load skill file structure guidance. Apply its patterns to all subsequent tasks. This corresponds to create-skill Step 5.

**Step 3: Read the meta template reference**

Meta skills use `create-skill` itself as the reference pattern (per create-skill Step 6). Read `skill-factory/skills/create-skill/SKILL.md` to understand the structure a meta skill should follow.

---

### Task 2: Write the SKILL.md

**Files:**
- Create: `skill-factory/skills/integrate-skill/SKILL.md`

**Step 1: Create the skill directory**

```bash
mkdir -p skill-factory/skills/integrate-skill
```

**Step 2: Write SKILL.md**

Write the SKILL.md with all sections from the design doc. The skill must include:

- **Frontmatter**: `name: integrate-skill`, description from design doc
- **Overview**: What the skill does, core principle (zero loss of function)
- **When to Use**: Migrating from other projects, temp/, external repos, standalone files
- **Workflow**: 7 steps (Ingest → Analyze → Design Doc → User Approval → Execute → Verify → Cleanup)
  - Step 1 (Ingest): Read all source files from any location
  - Step 2 (Analyze): MANDATORY read of `taxonomy.md`, classify each piece, map to existing plugins, check for redundancy, flag potential loss
  - Step 3 (Design Doc): Produce integration design doc with content split, files table, functionality preservation table. Save to `docs/plans/YYYY-MM-DD-<topic>-integration-design.md`
  - Step 4 (Approval): Present design doc, get explicit approval. Hard gate — do NOT proceed without approval
  - Step 5 (Execute): Invoke `skill-factory:create-skill` for each SKILL.md piece. Create reference files directly. Create new plugins if needed. Bump plugin versions
  - Step 6 (Verify): Run create-skill Step 8 validation. Walk functionality preservation table. Check for legacy syntax
  - Step 7 (Cleanup): List source files, user confirms, delete, commit
- **Quality Checklist**: 12 items from design doc
- **Common Pitfalls**: 5 items from design doc

**Structural constraints:**
- Under 500 lines
- Flat structure (no `references/` subdirectory needed)
- Imperative/infinitive verb form in headings
- No placeholder content

---

### Task 3: Validate Against Framework Rules

**Step 1: Check structural validation**

Verify the SKILL.md against create-skill Step 8:
- [ ] SKILL.md is under 500 lines
- [ ] Directory structure is flat (just `skills/integrate-skill/SKILL.md`)
- [ ] Frontmatter includes `name` and `description`
- [ ] Description clearly states what the skill does and when to use it

**Step 2: Check meta-specific validation**

- [ ] Serves the framework itself (creates, maintains, or validates other skills)
- [ ] References framework documentation as needed

**Step 3: Check composition validation**

- [ ] Uses `plugin:skill` invocation syntax for `skill-factory:create-skill`
- [ ] Does NOT include voice or brand hooks (meta skills don't produce content)
- [ ] No platform-specific content inline (none expected for meta skill)

**Step 4: Fix any issues found**

If any validation check fails, edit the SKILL.md to fix it before proceeding.

---

### Task 4: Update Plugin Metadata

**Files:**
- Modify: `skill-factory/.claude-plugin/plugin.json`
- Modify: `skill-factory/README.md`

**Step 1: Bump plugin version**

Edit `skill-factory/.claude-plugin/plugin.json`:
- Change `"version": "1.0.0"` to `"version": "1.1.0"`

**Step 2: Update README.md**

Add the integrate-skill to the Skills section and Directory Structure in `skill-factory/README.md`:

Add after the `create-skill` entry in Skills section:

```markdown
### integrate-skill (Meta Skill)

Guided workflow for integrating existing skills from any source into the composable architecture. Analyzes source skills, decomposes content across the correct plugins, and delegates generation to create-skill.

Workflow:
1. Ingest source skill from any location
2. Analyze and decompose using taxonomy decision tree
3. Produce integration design doc with content split plan
4. Get user approval before execution
5. Execute integration (invoke create-skill for each piece)
6. Verify against framework rules
7. Propose cleanup and commit
```

Add to Directory Structure:

```markdown
    └── integrate-skill/
        └── SKILL.md
```

---

### Task 5: Commit

**Step 1: Stage files**

```bash
git add skill-factory/skills/integrate-skill/SKILL.md skill-factory/.claude-plugin/plugin.json skill-factory/README.md
```

**Step 2: Commit**

```bash
git commit -m "feat(skill-factory): add integrate-skill for migrating external skills

Adds a meta-skill that formalizes the process of integrating skills
from any source into the composable skill architecture. Delegates
skill generation to create-skill and ensures zero loss of function.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Step 3: Verify commit**

```bash
git status
git log --oneline -3
```

Expected: Clean working tree, new commit visible.

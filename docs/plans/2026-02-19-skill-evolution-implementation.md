# Skill Evolution Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create the `skill-evolution` meta plugin with a `retrospective` skill that captures session friction and writes improvement notes to auto-memory and skill proposals.

**Architecture:** New plugin `skill-evolution/` at project root, following the same structure as `skill-factory/`. Single skill `retrospective/` with SKILL.md. No scripts, no references directory needed — this is a pure process skill.

**Tech Stack:** Markdown (SKILL.md), plugin.json, no code dependencies.

**Design doc:** `docs/plans/2026-02-19-skill-evolution-design.md`

---

### Task 1: Create the plugin directory structure

**Files:**
- Create: `skill-evolution/.claude-plugin/plugin.json`
- Create: `skill-evolution/README.md`
- Create: `skill-evolution/skills/retrospective/SKILL.md`

**Step 1: Create plugin.json**

Create `skill-evolution/.claude-plugin/plugin.json`:

```json
{
  "name": "skill-evolution",
  "description": "A meta-plugin for self-improving skills over time. Captures session friction, identifies skill gaps and deficiencies, and writes improvement notes to auto-memory.",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

**Step 2: Create README.md**

Create `skill-evolution/README.md`:

```markdown
# skill-evolution/

A meta-plugin for self-improving skills over time. Captures session friction, identifies skill gaps and deficiencies, and writes improvement notes to auto-memory and skill improvement proposals.

## Purpose

As Claude Code executes skills across sessions, mistakes and gaps emerge. This plugin closes the feedback loop by:

- Detecting user friction signals in real-time (corrections, redos, frustration)
- Running interactive retrospectives at end of session
- Writing confirmed findings to auto-memory (MEMORY.md) for immediate effect
- Drafting skill improvement proposals for user review

## Skills

### retrospective (Meta Skill)

Two-mode meta skill:

1. **Real-time friction capture** (passive): Recognizes user correction/frustration mid-session and mentally catalogs friction moments without interrupting workflow.
2. **Interactive retrospective** (active): Triggered by user via `/retrospective`. Reviews session, classifies findings, presents interactively for user confirmation, writes to memory.

## Directory Structure

skill-evolution/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── retrospective/
        └── SKILL.md
```

**Step 3: Commit plugin scaffold**

```bash
git add skill-evolution/.claude-plugin/plugin.json skill-evolution/README.md
git commit -m "feat: scaffold skill-evolution plugin"
```

---

### Task 2: Write the retrospective SKILL.md

This is the core deliverable. The SKILL.md must follow the meta skill pattern (use `skill-factory/skills/create-skill/SKILL.md` as reference) and encode the full design from `docs/plans/2026-02-19-skill-evolution-design.md`.

**Files:**
- Create: `skill-evolution/skills/retrospective/SKILL.md`

**Step 1: Write the SKILL.md**

Create `skill-evolution/skills/retrospective/SKILL.md` with this content:

```markdown
---
name: retrospective
description: Use when ending a working session to capture lessons learned, when the user corrects Claude or asks to redo work, when the user expresses frustration with output quality, or when user triggers /retrospective
---

# Retrospective

## Overview

A meta skill that helps Claude Code improve itself over time. Captures friction from working sessions and writes confirmed findings to auto-memory and skill improvement proposals.

**Core Principle**: Only log what the user confirms. Observable friction is the only valid signal — never guess or infer problems that didn't surface.

## When to Use

Use this skill when:
- User triggers `/retrospective` at end of a session
- User corrects Claude's output mid-session
- User asks Claude to redo work
- User expresses frustration or dissatisfaction
- Same topic required 3+ back-and-forth rounds without resolution
- User overrides Claude's approach ("Don't do it that way", "Skip that step")

Do NOT use when:
- Normal iterative refinement ("Make the font bigger" is collaboration, not friction)
- User is exploring options (asking for alternatives is not a correction)
- User changes their mind about direction (that's new input, not a mistake)

## Two Modes

### Mode 1: Real-Time Friction Capture (Passive)

When you detect a friction signal mid-session, do NOT interrupt the workflow. Mentally note:

1. **What skill was active** (or what task was being performed)
2. **What the user expected** vs what Claude produced
3. **The user's actual words** (the correction)
4. **Root cause category**: wrong output, missed requirement, unnecessary step, wrong skill invoked, or skill gap

Hold these notes in working memory. Do not write to disk until the retrospective.

### Friction Signals

| Signal | Example |
|--------|---------|
| User asks to redo | "No, redo this", "Try again", "That's not what I meant" |
| User corrects output | "Actually it should be X", "Change this to Y" |
| User expresses frustration | "This isn't right", "You keep doing X", "I already told you" |
| Excessive back-and-forth | 3+ rounds on the same topic without resolution |
| User overrides approach | "Don't do it that way", "Skip that step", "Just do X" |

### Mode 2: Interactive Retrospective (Active)

Triggered by user via `/retrospective`. Execute all steps in order.

#### Step 1: Scan conversation for friction

Review the full session. Identify every instance where a friction signal occurred. Include both:
- Friction moments captured in real-time (Mode 1)
- Friction moments found on retrospective review (hindsight)

#### Step 2: Classify each friction moment

For each, determine:

| Category | Description | Output Target |
|----------|-------------|---------------|
| **Skill Gap** | No skill exists for what went wrong | `memory/skill-proposals.md` |
| **Skill Deficiency** | Skill exists but missed something | `memory/skill-proposals.md` |
| **Process Mistake** | Claude didn't follow existing skill properly | `MEMORY.md` |
| **Preference Learned** | User has a preference Claude didn't know | `MEMORY.md` |
| **Context Gap** | Claude lacked project-specific knowledge | `MEMORY.md` |

Also identify: which skill was active, root cause in 1-2 sentences.

#### Step 3: Prioritize findings

- Rank by impact (time wasted, output quality, user frustration level)
- Select top 5 maximum — forces prioritization, prevents fatigue
- If two findings share the same root cause, merge them
- Drop low-impact items

#### Step 4: Present findings interactively

For each finding (one at a time), present:

1. **What happened**: Quote the user's actual words
2. **Category**: Which of the 5 categories
3. **Root cause**: Why it happened (1-2 sentences)
4. **Proposed action**: What to write and where

Ask the user: confirm, reject, or refine. Only confirmed findings proceed to writing.

#### Step 5: Read existing memory files

Before writing anything, read:
- `MEMORY.md` in the project's auto-memory directory
- `memory/skill-proposals.md` (if it exists)

Check for:
- **Duplicates**: Skip if already captured
- **Contradictions**: Present both to user, ask which is correct
- **Line count**: If MEMORY.md exceeds 150 lines, flag for consolidation before adding

#### Step 6: Write confirmed findings

**MEMORY.md format** (for Process, Preference, Context entries):

```
## [Category]: [Short imperative description]
- [Actionable note, 1 line]
- [Evidence: what friction triggered this]
```

Rules:
- 1-3 bullet points max per entry
- Include friction evidence so future Claude understands why
- No timestamps — stale entries get removed in future retrospectives

**memory/skill-proposals.md format** (for Skill Gap, Skill Deficiency entries):

```
## [ENHANCEMENT|NEW SKILL] skill-name — Short description
- **Evidence**: [The friction moment that motivated this]
- **Current behavior**: [What happens now]
- **Proposed change**: [What should change]
- **Affected section**: [Which part of the SKILL.md]
- **Status**: Proposed
```

Rules:
- Must include Evidence and Status
- Enhancement proposals reference specific section/step of existing skill
- New skill proposals include category and plugin per composable architecture
- Status values: `Proposed` | `Accepted` | `Applied` | `Rejected`

#### Step 7: Present summary

Show the user:
- How many findings captured vs rejected
- What was written to MEMORY.md (quoted)
- What was written to skill-proposals.md (quoted)
- Any pending proposals from previous sessions worth reviewing now

If no friction was found: report "Clean session — nothing to capture" and exit.

## Anti-Patterns

- Do NOT present more than 5 findings per retrospective
- Do NOT write anything the user hasn't confirmed
- Do NOT log normal iterative refinement as friction
- Do NOT propose skill changes for one-off issues — same root cause should appear in 2+ friction moments before proposing a skill edit (single occurrences go to MEMORY.md as process notes)
- Do NOT propose edits to superpowers skills (third-party, not user-owned) — note observations in MEMORY.md only
- Do NOT silently write to memory mid-session — all writes happen during the retrospective after user confirmation

## Memory Management

- Before writing, check existing MEMORY.md for duplicates and contradictions
- If MEMORY.md exceeds 150 lines, flag for consolidation before adding new entries
- Entries in skill-proposals.md marked `Applied` or `Rejected` can be archived to `memory/skill-proposals-archive.md`
- Memory is project-scoped — findings from one project don't bleed into another

## Relationship to Other Meta Skills

```
skill-factory:create-skill     → Creates new skills (blueprint)
skill-creator:skill-creator    → Guides skill creation (assistant)
superpowers:writing-skills     → Tests and deploys skills (TDD)
skill-evolution:retrospective  → Identifies what needs improving (feedback loop)
```

This skill completes the skill lifecycle: create → test → deploy → observe → improve.
```

**Step 2: Verify SKILL.md is under 500 lines**

Run: `wc -l skill-evolution/skills/retrospective/SKILL.md`
Expected: Under 500 lines

**Step 3: Validate against meta skill checklist**

Verify:
- [ ] Frontmatter has `name` and `description` (name: retrospective, description starts with "Use when...")
- [ ] Description is third-person, describes triggering conditions only, no workflow summary
- [ ] Overview states core principle
- [ ] Serves the framework itself (identifies improvements to other skills)
- [ ] No composition hooks needed (meta skill, not content-producing)
- [ ] Under 500 lines

**Step 4: Commit the SKILL.md**

```bash
git add skill-evolution/skills/retrospective/SKILL.md
git commit -m "feat: add retrospective skill for self-improving skills"
```

---

### Task 3: Register the plugin in the marketplace

The plugin needs to be registered so Claude Code discovers it.

**Files:**
- Modify: Check how other plugins are registered (look at README.md or any registration file at project root)

**Step 1: Check existing registration pattern**

Read `README.md` at project root to see how plugins are listed/registered.

**Step 2: Add skill-evolution to the registry**

Follow the same pattern as existing plugins. Add the skill-evolution entry.

**Step 3: Commit registration**

```bash
git add README.md
git commit -m "feat: register skill-evolution plugin in marketplace"
```

---

### Task 4: Final verification

**Step 1: Verify directory structure is correct**

Run: `find skill-evolution -type f | sort`

Expected:
```
skill-evolution/.claude-plugin/plugin.json
skill-evolution/README.md
skill-evolution/skills/retrospective/SKILL.md
```

**Step 2: Verify plugin.json is valid JSON**

Run: `python3 -c "import json; json.load(open('skill-evolution/.claude-plugin/plugin.json'))"`
Expected: No error

**Step 3: Verify SKILL.md frontmatter**

Run: `head -4 skill-evolution/skills/retrospective/SKILL.md`

Expected:
```
---
name: retrospective
description: Use when ending a working session...
---
```

**Step 4: Run git log to verify all commits**

Run: `git log --oneline -5`

Expected: 3 new commits (scaffold, skill, registration)

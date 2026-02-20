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

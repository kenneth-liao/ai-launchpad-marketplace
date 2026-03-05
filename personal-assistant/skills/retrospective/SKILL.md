---
name: retrospective
description: Use when ending a working session to capture lessons learned, when the user corrects Claude or asks to redo work, when the user expresses frustration with output quality, or when user triggers /retrospective
---

# Retrospective

## Overview

A meta skill that helps Elle actively improve over time. Captures friction from working sessions, routes findings to the correct context file, and closes the loop on past proposals.

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

#### Step 2: Classify and route each friction moment

For each friction moment, walk through this decision tree in order. The tree is ordered by scope — cross-project corrections first (most impactful), then project-specific knowledge, then skill improvements (which need pattern validation before acting on):

```
1. Is this a correction about Claude's behavior?
   YES → rules.md (cross-project, immediate)

2. Is this a user preference Claude didn't know?
   YES → preferences.md (cross-project, replace)

3. Is this a workflow/process the user follows?
   YES → workflows.md (cross-project)

4. Is this specific to this project/codebase?
   YES → auto memory MEMORY.md (project-scoped)

5. Is this a skill deficiency or gap?
   → Check improvements.md for prior occurrences
   → 0 prior: friction note in improvements.md Friction Log
   → 1+ prior: promote to/update Active Proposals in improvements.md
```

Classify each finding into one of these categories with its routing target:

| Category | Description | Destination |
|----------|-------------|-------------|
| **Behavioral Correction** | Claude did something the user corrected | `~/.claude/.context/core/rules.md` |
| **Preference Discovered** | User has a preference Claude didn't know | `~/.claude/.context/core/preferences.md` |
| **Workflow Captured** | User follows a process Claude should know | `~/.claude/.context/core/workflows.md` |
| **Project-Specific** | Knowledge specific to this codebase/project | Auto memory `MEMORY.md` |
| **Skill Friction (1st)** | Skill issue, no prior occurrences | `~/.claude/.context/core/improvements.md` Friction Log |
| **Skill Friction (2nd+)** | Skill issue, matches prior friction | `~/.claude/.context/core/improvements.md` Active Proposals |

Also identify: which skill was active, root cause in 1-2 sentences.

#### Step 3: Prioritize findings

- Rank by impact (time wasted, output quality, user frustration level)
- Select top 5 maximum — forces prioritization, prevents fatigue
- Allow up to 7 if findings span 4+ different destinations
- If two findings share the same root cause, merge them
- Drop low-impact items

#### Step 4: Present findings interactively

For each finding (one at a time), present:

1. **What happened**: Quote the user's actual words
2. **Category**: Which of the 6 categories
3. **Root cause**: Why it happened (1-2 sentences)
4. **Proposed action**: What to write and where (show the destination file)

Ask the user: confirm, reject, or refine. Only confirmed findings proceed to writing.

#### Step 5: Check existing files before writing

Before writing anything, read ALL potential destinations:

- `~/.claude/.context/core/rules.md`
- `~/.claude/.context/core/preferences.md`
- `~/.claude/.context/core/workflows.md`
- `~/.claude/.context/core/improvements.md`
- Project auto memory `MEMORY.md`

Check for:
- **Duplicates**: Skip if already captured
- **Contradictions**: Present both to user, ask which is correct
- **Context-update overlap**: Check what was already captured this session by context-update — skip duplicates
- **Line count**: If improvements.md exceeds 100 lines, flag for consolidation before adding

If the context system is not initialized (`~/.claude/.context/` doesn't exist), fall back to `MEMORY.md` only and suggest running `/personal-assistant:setup`.

#### Step 6: Write confirmed findings

Route each confirmed finding to its classified destination with format appropriate to that file:

**rules.md** (for Behavioral Corrections):
```
- [RULE]: [Actionable imperative — what to always/never do]
  - Source: Retrospective [date] — [brief friction context]
```

**After writing to rules.md or preferences.md**: Prompt the user: "Rules/preferences changed. Run `/sync-context` to update elle-core.md?"

**preferences.md** (for Preferences Discovered):
Replace the relevant preference entry, or add a new one under the appropriate section. Follow the file's existing format.

**workflows.md** (for Workflows Captured):
Add under the appropriate section following the file's existing format.

**MEMORY.md** (for Project-Specific findings):
```
## [Category]: [Short imperative description]
- [Actionable note, 1 line]
- [Evidence: what friction triggered this]
```
Rules: 1-3 bullet points max per entry. Include friction evidence.

**improvements.md Friction Log** (for Skill Friction, 1st occurrence):
Add a row to the Friction Log table:
```
| [Date] | [Project] | [Skill/Area] | [Friction Summary] | 1 |
```

**improvements.md Active Proposals** (for Skill Friction, 2nd+ occurrences):
```
### [ENHANCEMENT|NEW SKILL] skill-name — Short description
- **Evidence**: [Friction moments that motivated this, with dates]
- **Projects**: [Which projects encountered this]
- **Current behavior**: [What happens now]
- **Proposed change**: [What should change]
- **Affected section**: [Which part of the SKILL.md or system]
- **Status**: Proposed
- **Promoted**: [Date]
```

**Third-party skills** (superpowers, external plugins): Log friction notes in improvements.md for pattern tracking, but mark proposals with "External skill — workaround via rules.md" and add a corresponding rule for the immediate workaround.

#### Step 7: Verify applied proposals

Check `~/.claude/.context/core/improvements.md` for proposals with status `Applied`.

For each:
- Scan the current session for friction related to that proposal
- If no recurrence observed in this session, note it (after 2-3 sessions without recurrence, mark as Verified and move to Applied & Verified section)
- If friction recurred, update status to "Needs Revision" and create a follow-up note

#### Step 8: Journal and summary

Write session summary to `~/.claude/.context/core/journal.md` (append at TOP, newest first).

Show the user:
- How many findings captured vs rejected
- What was written and to which files (quoted)
- Any proposals verified or flagged for revision
- Any pending Active Proposals from previous sessions worth reviewing now

If no friction was found: report "Clean session — nothing to capture" and exit.

## Common Mistakes and Why They Matter

**Over-reporting kills trust.** If you dump 10 findings on the user, they'll stop confirming any of them. Cap at 5 (up to 7 only when spanning 4+ destinations) and prioritize ruthlessly — the user needs to feel each finding is worth their time.

**Writing without confirmation breaks the social contract.** The retrospective works because the user trusts that nothing gets written without their say-so. If you silently write mid-session or skip confirmation, the user loses trust in the entire context system.

**Misrouting creates invisible debt.** The routing tree exists because each context file has a different scope and lifecycle:
- Behavioral corrections in MEMORY.md get lost when the project ends — they belong in rules.md because they apply everywhere
- Preferences in improvements.md clutter the improvement tracker — they belong in preferences.md where they get applied immediately
- Skill proposals in project-scoped `memory/skill-proposals.md` can't aggregate cross-project patterns — they belong in improvements.md

**Premature proposals waste energy.** A single friction moment could be a fluke. The friction log exists to collect first occurrences cheaply — only promote to Active Proposals when the same root cause surfaces 2+ times, which signals a real pattern worth investing in.

**Duplicating context-update work creates noise.** The context-update process may have already captured corrections or preferences from this session. Check before writing to avoid contradictory or redundant entries.

**Confusing iteration with friction undermines accuracy.** "Make the font bigger" is collaboration. "You keep ignoring what I said" is friction. The distinction matters — logging normal refinement as friction inflates the signal and desensitizes the system.

## Memory Management

- Before writing, check all destination files for duplicates and contradictions
- If improvements.md exceeds 100 lines, flag for consolidation before adding new entries
- Proposals in improvements.md marked `Verified` can be pruned after 3 months
- Friction Log entries that have been promoted to Active Proposals can be removed
- improvements.md is cross-project — friction from all projects aggregates here, enabling pattern detection

## Relationship to Other Skills

```
skill-creator:skill-creator         → Guides skill creation (assistant)
superpowers:writing-skills          → Tests and deploys skills (TDD)
personal-assistant:retrospective    → Identifies what needs improving (feedback loop)
personal-assistant:update-context   → Handles routine context updates (avoid duplication)
personal-assistant:sync-context     → Regenerates elle-core.md after rule changes
```

This skill completes the skill lifecycle: create → test → deploy → observe → improve.

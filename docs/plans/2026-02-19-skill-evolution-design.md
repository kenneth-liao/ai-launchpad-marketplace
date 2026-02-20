# Skill Evolution — Self-Improving Skills Meta Skill

## Overview

A meta skill that helps Claude Code improve itself over time by capturing lessons from user friction and proposing skill improvements. One skill, two modes: passive real-time friction capture and active interactive retrospective.

**Skill name**: `skill-evolution:retrospective`
**Category**: Meta
**Plugin**: `skill-evolution/` (new plugin in marketplace)

## Requirements

| Decision | Choice |
|----------|--------|
| **Trigger** | Hybrid: post-session retrospective (`/retrospective`) + real-time on user correction |
| **Output** | Auto-memory (MEMORY.md) + skill improvement proposals file |
| **Threshold** | User friction signals only — observable evidence required |
| **Scope** | Memory notes + drafted skill proposals (user applies manually) |
| **Retro format** | Interactive — Claude presents findings, user confirms before writing |

## Approach

Single skill with two modes (Approach A over alternatives of two separate skills or hooks-based). Simplest architecture, no new patterns needed, fits existing composable framework.

## Section 1: Skill Identity & Classification

- **Name**: `skill-evolution` (verb-first per convention)
- **Plugin**: New plugin `skill-evolution` in the marketplace
- **Category**: Meta — observes and improves other skills, not user content
- **Two modes**: Real-time friction capture (passive) + interactive retrospective (active, `/retrospective`)
- **Invocation**: `skill-evolution:retrospective`
- **Description (CSO)**: Use when ending a working session to capture lessons learned, or when the user corrects Claude, asks to redo work, or expresses frustration with output quality. Also use when user triggers /retrospective.
- **Composition hooks**: None — meta skill, not content-producing

## Section 2: Real-Time Friction Capture

Passive mode that runs mid-session when Claude detects user friction.

### Friction Signals

| Signal | Example |
|--------|---------|
| User asks to redo | "No, redo this", "Try again", "That's not what I meant" |
| User corrects output | "Actually it should be X", "Change this to Y" |
| User expresses frustration | "This isn't right", "You keep doing X", "I already told you" |
| Excessive back-and-forth | 3+ rounds on the same topic without resolution |
| User overrides approach | "Don't do it that way", "Skip that step", "Just do X" |

### Behavior

- Does NOT interrupt the workflow
- Mentally notes: what skill was active, what user expected vs what Claude produced, the correction, and root cause category
- Notes held in working memory (conversation context) — nothing written to disk until retrospective
- Zero-risk: no files touched, no workflow interrupted

### Anti-Pattern

Do NOT fire on normal iterative refinement. "Can you make the font bigger?" is collaboration, not friction. The signal must indicate Claude got something wrong, not that the user is refining a preference.

## Section 3: Interactive Retrospective

Active mode triggered by user via `/retrospective`.

### Process Flow

```
User triggers /retrospective
        |
Scan full conversation for friction moments
        |
Friction found? -- No --> Report clean session, exit
        |
       Yes
        |
Classify each (5 categories)
        |
Prioritize, select top 5 max
        |
Present findings one at a time
        |
User confirms/rejects/refines each
        |
Read existing memory files (check duplicates/contradictions)
        |
Write confirmed findings
        |
Present summary
```

### Finding Categories

| Category | Description | Output Target |
|----------|-------------|---------------|
| **Skill Gap** | No skill exists for what went wrong | `memory/skill-proposals.md` |
| **Skill Deficiency** | Skill exists but missed something | `memory/skill-proposals.md` |
| **Process Mistake** | Claude didn't follow existing skill | `MEMORY.md` |
| **Preference Learned** | User has preference Claude didn't know | `MEMORY.md` |
| **Context Gap** | Claude lacked project-specific knowledge | `MEMORY.md` |

### Interactive Presentation

For each finding, present:
1. **What happened**: Quote user's actual words (the friction moment)
2. **Category**: Which of the 5 above
3. **Root cause**: Why it happened (1-2 sentences)
4. **Proposed action**: What to write and where

User confirms, rejects, or refines. Only confirmed findings get written.

## Section 4: Output Format & Memory Management

### MEMORY.md Entries

Format: `## [Category]: [Short imperative description]` with 1-3 bullet points max.

```markdown
## Process: Always confirm output format before generating
- When user asks for content, confirm the expected format/structure before drafting
- Friction: User had to redo newsletter draft because Claude assumed wrong section structure
```

Rules:
- Categories: `Process`, `Preference`, `Context`, `Skill Gap`, `Skill Deficiency`
- 1-3 bullet points max per entry
- Include friction evidence so future Claude understands why
- No timestamps

### memory/skill-proposals.md Entries

Format: `## [ENHANCEMENT|NEW SKILL|DEPRECATION] skill-name — Short description`

```markdown
## [ENHANCEMENT] content-strategy:research — Add pricing analysis step
- **Evidence**: User corrected research output twice for missing competitor pricing depth
- **Current behavior**: Research skill analyzes content landscape, gaps, and positioning
- **Proposed change**: Add step between competitor analysis and gap analysis
- **Affected section**: Key Process Steps, between steps 3 and 4
- **Status**: Proposed
```

Rules:
- Must include Evidence, Status (`Proposed` | `Accepted` | `Applied` | `Rejected`)
- Enhancement proposals reference specific section/step of existing skill
- New skill proposals include category and plugin placement per composable architecture

### Memory Management Guardrails

- Before writing, read existing MEMORY.md — check for duplicates and contradictions
- If contradiction found, present both to user, ask which is correct
- If MEMORY.md exceeds 150 lines, flag for consolidation before adding new entries
- skill-proposals.md has no line limit (it's a backlog)
- Applied/Rejected proposals can be archived to `memory/skill-proposals-archive.md`

## Section 5: Retrospective Checklist

1. **Scan conversation for friction moments** — all friction signals from Section 2, both real-time captured and newly found on review
2. **Classify each friction moment** — category, which skill was active, root cause
3. **Prioritize findings** — rank by impact, select top 5 max, merge shared root causes
4. **Present findings interactively** — one at a time, user confirms/rejects/refines
5. **Read existing memory files** — check duplicates, contradictions, line count
6. **Write confirmed findings** — MEMORY.md for process/preference/context, skill-proposals.md for gaps/deficiencies
7. **Present summary** — counts, what was written, pending proposals from previous sessions

### Anti-Patterns

- Do NOT present more than 5 findings
- Do NOT write anything the user hasn't confirmed
- Do NOT log normal iteration (preference refinement, not mistakes)
- Do NOT propose skill changes for one-off issues — same root cause must appear in 2+ friction moments before proposing a skill edit

## Section 6: Integration & Edge Cases

### Composable Architecture Fit

| Aspect | Decision |
|--------|----------|
| Plugin | `skill-evolution/` (new) |
| Skill file | `skill-evolution/skills/retrospective/SKILL.md` |
| Category | Meta |
| Composition hooks | None |
| Invokes | No other skills |
| Invoked by | User only |

### What This Skill Is NOT

- Not an orchestrator (doesn't sequence other skills)
- Not a foundation skill (doesn't produce content)
- Not always-on (recognition pattern, not background process)
- Not a replacement for `superpowers:verification-before-completion` (that prevents false claims; this captures why things went wrong)
- Not a replacement for `superpowers:writing-skills` (that creates/tests skills; this identifies what needs changing)

### Skill Lifecycle Position

```
skill-factory:create-skill     -> Creates new skills (blueprint)
skill-creator:skill-creator    -> Guides skill creation (assistant)
superpowers:writing-skills     -> Tests and deploys skills (TDD)
skill-evolution:retrospective  -> Identifies what needs improving (feedback loop)
```

### Edge Cases

1. **Clean session**: Report "clean session, nothing to capture" and exit
2. **User error, not Claude error**: User realizes during review that friction was their unclear instructions. Finding gets rejected. Interactive gate handles it.
3. **MEMORY.md at 150+ lines**: Flag before writing, propose consolidation (merge/remove stale entries), user approves before new entries added
4. **Friction involves superpowers skill**: Capture in MEMORY.md as process note. Do NOT propose edits to superpowers skills (third-party). Note "superpowers:X could benefit from Y" in MEMORY.md only.
5. **Multiple projects**: Memory is project-scoped. No cross-project bleed. User manually copies universal findings if needed.
6. **Mid-session retrospective**: Reviews conversation so far. Can run multiple times. Only surfaces new friction since last retrospective.

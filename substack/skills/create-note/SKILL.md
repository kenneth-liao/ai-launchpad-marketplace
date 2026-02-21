---
name: create-note
description: Create high-engagement Substack Notes for standalone audience engagement, authority-building, and newsletter promotion. This is a thin orchestrator — it sequences content-strategy:research and writing:copywriting invocations for Substack Note creation.
---

# Create Substack Note

## Overview

This orchestrator creates Substack Notes by sequencing `content-strategy:research` for strategic context and `writing:copywriting` for content generation. It handles newsletter context awareness, note type selection, and output management -- all actual content generation and strategy are delegated to the foundation skills and their references.

**Core Principle**: This is a thin orchestrator. Strategy lives in `content-strategy:research` via `references/substack-notes-strategy.md`. Templates and formatting live in `writing:copywriting` via `references/substack-notes.md`. This skill manages the workflow sequence, newsletter context, and user decisions only.

## When to Use

Use this skill when:
- Writing a standalone Substack Note for audience engagement
- Promoting a newsletter issue through Notes
- Building engagement between newsletter issues
- Sharing insights, hot takes, or behind-the-scenes content
- Creating any short-form Substack content

## Prerequisites

**Optional**: A recent newsletter issue directory at `./newsletter/issues/[issue_name]/` with a `plan.md` file. This is only needed for issue-linked notes. Standalone notes do not require an issue directory.

## Workflow

Execute all steps below in order.

### Step 0: Newsletter Context Check

Check if the user has specified a newsletter issue or if an issue directory exists at `./newsletter/issues/[issue_name]/`.

**If issue directory exists:**
- Read `plan.md` for issue topic, title, and context
- Suggest a lifecycle phase based on context:
  - Issue not yet published -> **pre-newsletter**
  - Issue just published -> **issue day**
  - Issue published 3-7 days ago -> **post-newsletter**
- Use this context to inform the research invocation in Step 1

**If no issue directory:**
- Default to **between issues** mode
- Notes will focus on engagement, authority-building, or value delivery
- Any note type is available

### Step 1: Invoke `content-strategy:research`

**MANDATORY**: Invoke `content-strategy:research` with `references/substack-notes-strategy.md` to determine the strategic context for this note.

Provide:
- The lifecycle phase (from Step 0 or user input)
- The topic
- The user's stated goal (engagement, promotion, authority, connection, quick value, transparency, positioning)

The research skill will apply the strategy framework to determine:
- Optimal note type ranking for the context
- Cadence awareness
- Strategic rationale for the approach

NOTE: This is a lighter research invocation -- the orchestrator is asking research to apply the strategy framework to the user's context, not to do full competitor analysis.

### Step 2: Present Note Type Options

Based on the research output, present the ranked note type options to the user:

1. **Single-Punch Wisdom** -- one sharp insight
2. **Income Proof Story** -- results-driven credibility
3. **Pattern Observation** -- trend or pattern spotted
4. **Contrarian Statement** -- against-the-grain take
5. **Problem -> Solution** -- actionable fix
6. **Build-in-Public Update** -- transparency and progress
7. **List-Based Tactical** -- quick-hit value list
8. **Vulnerable Personal Story** -- authentic connection
9. **Newsletter Teaser** -- drive issue reads
10. **Direct Advice** -- straight recommendation

Include the research skill's recommendation for which type best fits the context. User selects their preferred type.

**Default to Short (3-5 sentences)** unless the message demands more.

### Step 3: Invoke `writing:copywriting`

**MANDATORY**: Invoke `writing:copywriting` with `references/substack-notes.md` to draft the note.

Provide:
- The selected note type from Step 2
- The strategic context from Step 1
- The newsletter context from Step 0 (if applicable)
- The lifecycle phase and user's stated goal

The `writing:copywriting` skill will automatically invoke `writing:voice` for voice consistency. The reference file contains all templates, formatting rules, and structural formulas.

### Step 4: Quality Checklist

Verify the drafted note against all eight criteria before presenting to the user:

- [ ] Follows structural formula for chosen note type
- [ ] Opens with strong hook (first line grabs attention)
- [ ] Length matches type guideline
- [ ] Ends with engagement hook (not formulaic)
- [ ] Specific, not vague (numbers, examples, concrete details)
- [ ] Standalone value (interesting without clicking any link)
- [ ] NOT a generic link dump
- [ ] Note type matches the stated goal

If any criterion fails, request a revision from `writing:copywriting` before presenting to the user.

### Step 5: Save Output

Present the final note to the user for approval.

**If issue directory exists:**
- After user approval, append to `./newsletter/issues/[issue_name]/notes.md`

**If no issue directory:**
- Present the final note inline to the user

## Output Format

When saving to `notes.md`, use this structure:

```markdown
## [Type] Note - [Date]

**Type:** [Note type name]
**Context:** [Standalone / Pre-newsletter / Issue Day / Post-newsletter / Between Issues]
**Goal:** [Engagement / Authority / Connection / Promotion / Quick Value / Transparency / Positioning]

### Note Content

[Final note text]

### Notes

- Suggested timing: [from research]
- Engagement hook type: [question / agree-disagree / share / reply]
```

Multiple notes are appended to the same file with a horizontal rule separator (`---`) between entries.

## Quality Checklist

Verify completion before finalizing:
- [ ] Newsletter context checked (Step 0)
- [ ] `content-strategy:research` invoked with `references/substack-notes-strategy.md` -- strategic context determined
- [ ] Note type options presented and user selection received
- [ ] `writing:copywriting` invoked with `references/substack-notes.md` -- note drafted
- [ ] Voice consistency maintained (handled by writing skill's `writing:voice` invocation)
- [ ] All 8 quality criteria passed (Step 4)
- [ ] Note presented to user for approval
- [ ] Output saved to issue directory or presented inline

## Common Pitfalls to Avoid

1. **Writing templates inline**: All templates live in `references/substack-notes.md` -- do not duplicate them in this orchestrator
2. **Embedding strategy logic**: All strategy lives in `references/substack-notes-strategy.md` -- do not hardcode timing, cadence, or algorithm advice here
3. **Skipping foundation skill invocations**: Both `content-strategy:research` and `writing:copywriting` must be invoked -- do not generate notes directly
4. **Ignoring newsletter context**: Always check for an issue directory first -- it changes the entire strategic approach
5. **Defaulting to "new issue out" link dumps**: The research and writing skills are specifically designed to avoid generic link dumps -- trust the foundation skills
6. **Skipping the quality checklist**: Every note must pass all 8 criteria before presenting to the user

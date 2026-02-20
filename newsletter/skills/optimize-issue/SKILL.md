---
name: optimize-issue
description: "Orchestrate foundation skills to optimize a newsletter draft or write a full issue from an outline. Use when asked to 'optimize this draft', 'polish this newsletter', 'write from this outline', 'improve this issue', or when transforming an existing newsletter draft or outline into a publication-ready issue. This is distinct from plan-issue which starts from a topic — optimize-issue starts from existing content."
---

# Optimize Newsletter Issue

Orchestrate foundation skills to transform outlines into full drafts or optimize rough drafts into high-performing newsletter issues. This is a thin orchestrator — it sequences skill invocations and manages the user review workflow, but delegates all content generation to foundation skills.

**Core Principle**: This is a thin orchestrator. Never write newsletter content manually. Always delegate to the appropriate foundation skill.

## When to Use

Use this skill when:
- Transforming an outline into a full newsletter draft
- Optimizing or polishing an existing rough draft
- The user has newsletter content that needs quality improvement
- Converting notes or bullet points into a publication-ready issue

Do NOT use this skill when:
- Starting from a topic with no existing content (use `newsletter:plan-issue` instead)
- Creating visual assets for a newsletter (use `visual-design:newsletter-visuals`)

## Prerequisites

**MANDATORY**: Existing content must be available. Either:
1. A newsletter outline (bullet points, topic structure, notes), OR
2. A rough draft that needs optimization

## Newsletter Workflow

Execute all steps below in order.

### Step 1: Assess the Input

Determine the input type and issue type:

- **Outline**: Bullet points, topic structure, or notes → full draft workflow
- **Rough draft**: Existing prose that needs optimization → audit and optimize workflow

Present the assessment to the user: input type, detected issue type, and the workflow that follows.

### Step 2: Draft or Optimize Content

**From outline:**
1. **MANDATORY**: Invoke `writing:copywriting` with content type "newsletter" to write the full draft.
   - Pass the outline as source material
   - The copywriting skill loads `references/newsletter.md` for section rules, issue types, and writing conventions
2. The draft follows the Newsletter Arc: Hook → Context → Value → Close

**From rough draft:**
1. **MANDATORY**: Invoke `writing:copywriting` with content type "newsletter" to audit and optimize each section.
   - Pass the draft as source material with instruction to optimize
   - The copywriting skill checks against section rules and body writing rules
2. Present findings: what works, what needs improvement, and specific recommendations
3. Rewrite/optimize sections that fall short

### Step 3: Generate Subject Lines

1. **MANDATORY**: Invoke `content-strategy:title` with content type "newsletter" to generate 3 subject line options.
   - Pass the draft content as context
   - The title skill loads `references/newsletter-subject-lines.md` for formulas and rules
2. Each option includes preview text (subtitle)
3. Document all options with star ratings and recommendation

### Step 4: Generate Opening Hook

1. **MANDATORY**: Invoke `content-strategy:hook` with content type "newsletter" to generate 2-3 hook options.
   - Pass the selected subject line and draft content as context
   - The hook skill loads `references/newsletter-hooks.md` for hook patterns
2. Each hook must extend curiosity from the subject line (not repeat it)
3. Document all options with rationale

### Step 5: Present Options and Get User Selection

1. Present subject line options with star ratings
2. Present hook options with rationale
3. Present the full draft (or optimized draft)
4. Ask the user to select subject line + hook

**CRITICAL**: Present ALL options. Do not select on the user's behalf.

### Step 6: Run Pre-Publish Checklist

1. **MANDATORY**: Read `references/pre-publish-checklist.md`
2. Run through every check against the final draft
3. Flag any items that don't pass
4. Present results to the user with specific fixes for any failures

### Step 7: Finalize

1. Assemble the final issue: selected subject line + preview text + selected hook + optimized body + close + P.S.
2. Present the complete, publication-ready issue to the user

## Output Structure

Present the final issue in this structure:

```markdown
# [Subject Line]
*[Preview Text]*

[Opening Hook]

[Body Content - sections with subheadings]

[Close]

P.S. [Secondary CTA or personal touch]
```

## Execution Guidelines

**NEVER** generate content manually. Always delegate:
- `writing:copywriting` for all newsletter prose (drafting and optimization)
- `content-strategy:title` for subject line generation
- `content-strategy:hook` for opening hook generation
- `writing:voice` is invoked automatically by the copywriting skill

**CRITICAL**: Always present ALL options with star ratings and rationale.

## Quality Checklist

- [ ] Input type assessed (outline vs. draft)
- [ ] `writing:copywriting` invoked for content generation/optimization
- [ ] `content-strategy:title` invoked for subject lines (3 options generated)
- [ ] `content-strategy:hook` invoked for opening hooks (2-3 options generated)
- [ ] All options presented with star ratings
- [ ] User selected subject line and hook
- [ ] Pre-publish checklist run (all items pass or flagged)
- [ ] Final issue assembled and presented
- [ ] No content generated manually by this orchestrator

## Common Pitfalls

1. **Writing content manually**: Generating newsletter prose instead of delegating to `writing:copywriting`.
2. **Single option**: Presenting one subject line or hook instead of multiple options.
3. **Skipping the pre-publish checklist**: The checklist catches issues the draft workflow misses.
4. **Fat orchestrator**: Adding copywriting techniques, section rules, or formatting guidance here instead of keeping them in foundation skill references.

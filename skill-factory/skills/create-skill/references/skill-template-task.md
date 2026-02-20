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

## Examples from the System

- `writing:copywriting` -- Content Type Resolution table, 7-step workflow, voice and brand hooks
- `content-strategy:title` -- Platform references, verification checklist, rejection criteria
- `content-strategy:hook` -- Forbidden patterns, hook patterns, quality verification
- `content-strategy:research` -- Platform-agnostic design, subagent support, output structure
- `visual-design:thumbnail` -- Skill integration (`art:nanobanana`), brand compliance, reference images

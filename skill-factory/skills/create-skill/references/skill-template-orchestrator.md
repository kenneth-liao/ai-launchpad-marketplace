# Orchestrator Skill Template

Use this template when creating a new **Orchestrator** skill. Orchestrators sequence task skills for a platform-specific workflow, managing user selection between steps.

**This skill is a THIN ORCHESTRATOR. It delegates to task skills -- it does NOT implement anything itself.**

Fill in all sections. Replace `{placeholder}` values with skill-specific content. Remove `<!-- comments -->` before finalizing.

---

## Template

```markdown
---
name: {skill-name}
description: "{Orchestrate foundation skills to [workflow purpose]. This is a thin orchestrator -- it sequences skill invocations and manages the user selection workflow, but delegates all content generation to foundation skills.}"
---

# {Skill Title}

## Overview

<!-- 2-3 sentences. State explicitly that this is a thin orchestrator. -->

**Core Principle**: This is a thin orchestrator. Never {generate content type} manually. Always delegate to the appropriate foundation skill.

## When to Use

Use this skill when:
- {Trigger condition 1}
- {Trigger condition 2}
- {Trigger condition 3}

## Prerequisites

**MANDATORY**: {What must be available before starting.} Either:
1. {Existing source material option}, OR
2. Invoke `{plugin:skill}` to produce it first

## {Platform} Workflow

Execute all steps below in order.

### Step 1: {Setup / Load Context}

### Step 2: {First Skill Invocation}

1. **MANDATORY**: Invoke `{plugin:skill-1}` to {produce first output}.
2. Document all options with star ratings.

### Step 3: {Second Skill Invocation}

1. **MANDATORY**: Invoke `{plugin:skill-2}` to {produce second output}.
2. Document all options.

### Step 4: Present Options and Get User Selection

1. Present all options with star ratings and rationale.
2. Ask user to select. Update plan file.

**CRITICAL**: Present ALL options. Do not select on the user's behalf.

### Step N: Finalize Plan

## Output Structure

Save the plan to `{output-path}`. The plan file must follow this structure:

\```markdown
# {Plan Title}: [Topic]

## {Section 1}
## {Section 2}
## Final Plan
- **{Selection 1}**: [User's selection]
- **{Selection 2}**: [User's selection]
\```

## Execution Guidelines

**NEVER** generate content manually. Always delegate:
- `{plugin:skill-1}` for {output type 1}
- `{plugin:skill-2}` for {output type 2}

**CRITICAL**: Always present ALL options with star ratings.

## Quality Checklist

- [ ] Prerequisites met (source material loaded)
- [ ] `{plugin:skill-1}` invoked
- [ ] `{plugin:skill-2}` invoked
- [ ] User selected from presented options
- [ ] Plan file complete
- [ ] Recommendations backed by rationale

## Common Pitfalls to Avoid

1. **Skipping Skill Invocation**: Generating content manually instead of delegating.
2. **Single Option**: Presenting one recommendation instead of multiple.
3. **Fat Orchestrator**: Implementing content logic instead of delegating.
4. **No Rationale**: Recommendations without explanation.
```

---

## Template Rules

1. **Thin, thin, thin** -- Only workflow sequence and platform decisions. All content generation is delegated.
2. **Every content step is a skill invocation** -- No exceptions.
3. **Use `plugin:skill` syntax** -- e.g., `content-strategy:title`, `writing:copywriting`.
4. **Multiple options always** -- Every selection point presents all options with star ratings.
5. **Plan file required** -- Orchestrators save output to a structured plan file.
6. **Under 500 lines** -- If SKILL.md exceeds this, delegate more.

## Examples from the System

- `youtube:plan-video` -- Sequences research, title, thumbnail, hook, and outline for YouTube
- `youtube:repurpose-video` -- Sequences copywriting invocations across platforms
- `substack:plan-issue` -- Sequences research, draft, subject line, hook, and social posts

## Key Difference from Task Skills

| Aspect | Task Skill | Orchestrator Skill |
|---|---|---|
| Produces content | Yes | No (delegates) |
| Invokes other skills | Sometimes (voice, brand) | Always (entire workflow) |
| Has voice/brand hooks | Yes | No (task skills handle it) |
| Platform-specific | Sometimes | Always |
| User selection workflow | Rarely | Core feature |

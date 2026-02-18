---
name: plan-issue
description: "Orchestrate foundation skills to plan a complete newsletter issue including research, draft, subject line, opening hook, and social promotion posts. This is a thin orchestrator — it sequences skill invocations and manages the user review workflow."
---

# Plan Newsletter Issue

## Overview

This skill takes a topic and produces a complete newsletter issue plan with draft content, subject line options, opening hook options, and social promotion posts. It is a thin orchestrator — every content generation step delegates to a foundation skill. This skill contains workflow sequence and platform-specific decisions only, not implementation logic.

## When to Use

Use this skill when:
- Planning a new newsletter issue from a topic or idea
- Repurposing existing content (video transcript, notes, research) into a newsletter
- Creating a content plan for Substack or another newsletter platform

## Prerequisites

A topic or source material is required. This can be:
- A topic idea or keyword
- A video transcript to repurpose
- Existing notes or research
- A URL or document to build from

If research already exists or the user is repurposing existing content, the research step can be skipped.

## Planning Workflow

Execute all steps below sequentially. Add these as ToDos to track progress.

### Step 1: Research the Topic

**Invoke `content-strategy:research`** to understand the content landscape and identify the best angle for the newsletter issue.

- Pass the topic, audience context, and any source material to the research skill.
- The research skill will analyze competitors, identify gaps, and produce actionable insights.

**Skip condition**: Skip this step if the user provides existing research, or if working from existing content (e.g., repurposing a video transcript). Note the reason for skipping in the plan.

### Step 2: Draft the Newsletter Issue

**Invoke `writing:copywriting`** to draft the full newsletter issue.

- The copywriting skill will automatically load `references/newsletter.md` for newsletter structure and conventions.
- The copywriting skill will automatically invoke `writing:voice` for voice consistency.
- Pass the research findings (or source material) and topic context.
- The draft should follow the newsletter reference structure including sections, formatting, and CTAs.

### Step 3: Generate Subject Line Options

**Invoke `content-strategy:title`** to generate 3-5 subject line options.

- The title skill will automatically load `references/newsletter-subject-lines.md` for subject line patterns.
- Each option must include:
  - Subject line text
  - Preview text (the snippet shown in email clients)
  - Rationale for why it will perform well
  - Star rating (1-3 stars) indicating recommendation strength

### Step 4: Generate Opening Hook Options

**Invoke `content-strategy:hook`** to generate 2-3 opening paragraph options.

- The hook skill will automatically load `references/newsletter-hooks.md` for opening patterns.
- Each option must include:
  - Full opening paragraph text
  - Hook strategy description
  - Rationale and alignment with the selected subject line
  - Star rating (1-3 stars) indicating recommendation strength

### Step 5: Generate Social Promotion Posts

**Invoke `writing:copywriting`** separately for each platform:

1. **Twitter/X thread** — the copywriting skill loads `references/twitter.md` for thread structure and character limits.
2. **LinkedIn post** — the copywriting skill loads `references/linkedin.md` for post conventions.
3. **Substack Note** — the copywriting skill loads `references/substack-notes.md` for note formatting.

Each promotion post should tease the newsletter content and drive subscriptions/reads.

### Step 6: Generate Header Image (Optional)

**Invoke `visual-design:social-graphic`** to generate a newsletter header image.

- Only invoke if the user requests a header image or if the newsletter platform benefits from one.
- If not requested, mark as "Not requested" in the plan.

### Step 7: Present Complete Plan

Present the full plan to the user for review. Include all options with star ratings so the user can make informed selections.

## Output Structure

Save the plan to `./newsletter/issues/[issue_name]/plan.md`. Create the directory if it doesn't exist. Use a slugified version of the topic as the issue name (e.g., `ai-coding-assistants`).

The plan file must follow this structure:

```markdown
# Newsletter Issue Plan: [Topic]

## Research Summary
[Key findings and angle — or "Based on [source material]" if repurposing]

## Subject Lines
[3-5 options with preview text, rationale, and star ratings]

## Opening Hook Options
[2-3 opening paragraphs with strategy, rationale, and star ratings]

## Draft Issue
[Full newsletter draft following newsletter.md structure]

## Social Promotion
### Twitter/X Thread
[Thread draft]
### LinkedIn Post
[Post draft]
### Substack Note
[Note draft]

## Header Image
[Generated image or "Not requested"]
```

## Execution Guidelines

### Always Invoke Foundation Skills

**NEVER** generate content manually. Always delegate to the appropriate skill:
- `content-strategy:research` for research
- `writing:copywriting` for all written content (newsletter draft and social posts)
- `content-strategy:title` for subject lines
- `content-strategy:hook` for opening hooks
- `visual-design:social-graphic` for header images

### Provide Multiple Options

**CRITICAL**: Present all options with star ratings so the user can choose. Do not select a single option on the user's behalf.

### Back Recommendations with Research

When rating options with stars:
- Reference research findings or source material insights
- Explain why a particular angle or framing will resonate
- Note how the option addresses identified content gaps

## Quality Checklist

Verify completion before presenting the plan:
- [ ] Research conducted (or source material loaded)
- [ ] `content-strategy:research` invoked (or skipped with reason)
- [ ] `writing:copywriting` invoked for newsletter draft
- [ ] `content-strategy:title` invoked for subject lines
- [ ] `content-strategy:hook` invoked for opening hooks
- [ ] `writing:copywriting` invoked for social promotion posts
- [ ] All written content goes through `writing:voice` (handled by copywriting skill)
- [ ] Complete plan presented to user

## Common Pitfalls to Avoid

1. **Writing content directly**: Drafting newsletter text or social posts without invoking the copywriting skill. Always delegate.
2. **Skipping research without reason**: If research is skipped, document why (e.g., "Repurposing video transcript provided by user").
3. **Single option only**: Presenting one subject line or one hook. Always provide multiple options with ratings.
4. **Missing social promotion**: Forgetting one of the three platforms (Twitter/X, LinkedIn, Substack Notes).
5. **No voice consistency**: The copywriting skill handles this automatically via `writing:voice`, but verify the output reads consistently.

## Example Execution

**Scenario**: User asks to plan a newsletter about "Building AI agents with memory"

1. **Research**: Invoke `content-strategy:research` with topic "AI agents with memory" to identify content gaps and angles.
2. **Draft**: Invoke `writing:copywriting` with research findings to produce the full newsletter draft.
3. **Subject lines**: Invoke `content-strategy:title` to generate 4 subject line options with preview text.
4. **Opening hooks**: Invoke `content-strategy:hook` to generate 3 opening paragraph options.
5. **Social posts**: Invoke `writing:copywriting` three times for Twitter/X thread, LinkedIn post, and Substack Note.
6. **Header image**: User did not request one — mark "Not requested."
7. **Present plan**: Save to `./newsletter/issues/ai-agents-with-memory/plan.md` and present to user.

**Result**: Complete newsletter issue plan with multiple options at each decision point, all backed by research insights and generated through specialized foundation skills.

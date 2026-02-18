---
name: copywriting
description: Generalized writing skill that produces written content for any platform and format. Determines content type from context, loads platform-specific references, drafts content, and applies voice and brand compliance.
---

# Copywriting

Generalized writing skill for producing written content across all platforms and formats. This skill handles the structure, format, and platform conventions for each content type. Voice and brand compliance are applied through explicit skill invocation.

## Content Type Resolution

Based on the user's request, determine which content type applies and load the corresponding reference file for platform-specific structure and conventions.

| Content Type | Reference File | Key Patterns |
|---|---|---|
| Newsletter issue | `references/newsletter.md` | Substack structure, sections, CTAs |
| YouTube script | `references/youtube-script.md` | Hook, intro, content, CTA, outro |
| Guide/cheatsheet | `references/guide.md` | Problem, framework, steps, takeaway |
| Sales/product copy | `references/sales-page.md` | Headline, problem, solution, proof, CTA |
| Twitter/X post | `references/twitter.md` | Character limits, thread structure |
| LinkedIn post | `references/linkedin.md` | Professional tone, post structure |
| Substack Note | `references/substack-notes.md` | Short-form, engagement hooks |

If the content type is ambiguous, ask the user to clarify before proceeding.

## Standard Workflow

Follow this sequence for every content production task:

### 1. Determine Content Type

Identify the content type from the user's request. Match against the table above. If the request spans multiple types (e.g., "write a newsletter and a Twitter thread promoting it"), handle each as a separate content piece using the appropriate reference.

### 2. Load Platform Reference

Read the corresponding reference file from `references/`. This provides the structural template, length guidelines, and platform-specific conventions for the content type.

### 3. Gather Context

Before drafting, ensure you have:
- **Topic:** What the content is about
- **Audience:** Who this is for (default: Kenny's newsletter/YouTube audience — builders using AI tools)
- **Key message:** The one thing the reader should take away
- **Supporting material:** Any research, notes, screenshots, or rough drafts the user provides
- **Constraints:** Word count, deadline, specific sections to include/exclude

Ask the user for any missing critical context. Don't guess at the topic or key message.

### 4. Draft Content

Write the first draft following the platform reference structure. Focus on:
- Correct structure for the content type
- Complete coverage of the topic
- Supporting evidence and examples
- Appropriate length per platform guidelines

Do NOT worry about voice at this stage — structure and substance come first.

### 5. Apply Voice

Invoke the `writing:voice` skill to transform the draft into Kenny's authentic voice. This is an explicit invocation — the voice skill applies all voice rules, anti-patterns, and formatting conventions.

The voice skill handles: parenthetical asides, sentence rhythm, fragments, casual vocabulary, counterpoint patterns, functional headers, and raw-over-polished quality.

### 6. Brand Compliance Check

Invoke the `branding-kit:brand-guidelines` skill to verify the content meets brand standards. This covers: visual identity references, brand terminology, tone alignment, and any brand-specific constraints.

### 7. Present to User

Deliver the final draft with:
- The complete content piece
- A brief note on any decisions made (structure choices, sections included/excluded)
- Specific questions if any part needs user input

## Voice Application

This skill explicitly invokes `writing:voice` as part of every content production workflow. Voice is applied after the structural draft is complete but before brand compliance.

**Why voice is separate:** Keeping voice rules in a dedicated personality skill means they stay consistent across all content types. The copywriting skill handles *what* to write and *how to structure it*. The voice skill handles *how it sounds*.

**Invocation point:** Step 5 of the standard workflow. Never skip this step.

## Brand Compliance

This skill explicitly invokes `branding-kit:brand-guidelines` as the final quality gate before presenting content to the user.

**Why brand compliance is separate:** Brand guidelines (logos, colors, terminology, visual identity) are maintained centrally in the branding-kit plugin. This skill delegates that check rather than duplicating brand rules.

**Invocation point:** Step 6 of the standard workflow. Runs after voice application.

## Quality Checklist

Before presenting final content, verify:

- [ ] Content type correctly identified and appropriate reference loaded
- [ ] Platform structure followed (correct sections, length, formatting)
- [ ] Topic fully covered with supporting evidence
- [ ] `writing:voice` invoked and voice rules applied
- [ ] `branding-kit:brand-guidelines` invoked and brand compliance verified
- [ ] No placeholder content or unresolved TODOs
- [ ] Links, references, and technical details are accurate
- [ ] Content is the appropriate length for the platform
- [ ] CTA is present and appropriate for the content type

---
name: extract-ideas
description: Extract structured content ideas from published material. Use when you have source material (transcripts, newsletters, notes, web trends) and need to mine it for repurposable angles, map raw material to content types, or identify underused content types. Not for competitor research (use creator-stack:research) or writing finished content (use creator-stack:write).
---

# Content Ideation

## Overview

This skill extracts structured content ideas from published source material. It reads existing content (transcripts, newsletters, notes, web trends), identifies note-worthy angles using platform-specific extraction frameworks, and outputs quality-filtered ideas in a structured format.

**Core Principle**: Extract, don't invent. Every idea must trace back to specific source material. This skill mines what already exists — it does not conduct competitor research or analyze content landscapes. That is what `creator-stack:research` does.

## When to Use

Use this skill when:
- You have published source material and need to extract repurposable ideas from it
- An orchestrator provides content (transcripts, articles, notes history) and asks for structured idea generation
- You need to map raw material to specific content types using an extraction framework
- You want to identify underused content types and bias toward variety

## When NOT to Use

Do NOT use this skill when:
- You need to research a topic, analyze competitors, or find content gaps — use `creator-stack:research`
- You need to write finished content from an idea — use `creator-stack:write`
- You need to generate titles or hooks — use `creator-stack:title` or `creator-stack:hook`
- You have no source material to extract from — ideation requires inputs

## Platform-Specific Reference Loading

This skill is generalized. Platform-specific extraction frameworks, content type taxonomies, quality criteria, and output formats live in reference files under `references/`.

| Platform | Reference File | Loaded By |
|---|---|---|
| Substack Notes | `references/substack-notes-ideation.md` | `creator-stack:ideate-notes` |

When invoked, read the reference file provided by the orchestrator. The reference defines:
- **Extraction categories** — what to look for in source material
- **Source-to-type mapping** — which content types emerge from which sources
- **Quality criteria** — pass/fail checklist for every idea
- **Output format** — structured fields for each idea
- **Volume target** — how many ideas to generate per run

## Ideation Subagents

You can invoke ideation subagents using the `Agent` tool with `run_in_background: true` to extract ideas from different sources in parallel. Each agent prompt should focus on a single source (one transcript, one newsletter issue, one trend cluster) and include the relevant extraction categories from the reference.

Bias toward using the `Agent` tool for multi-source extraction rather than processing all sources sequentially. Parallel extraction greatly improves performance and prevents context bleed between sources.

Each subagent should receive:
- The source material to extract from
- The extraction categories from the reference file
- The source-to-type mapping for that source type
- The quality criteria checklist
- Past content history for duplicate prevention

## Ideation Workflow

Execute all steps below to complete the ideation.

### Step 1: Receive and Organize Source Material

Receive source material from the orchestrator. Organize by source type:
- YouTube transcripts, titles, descriptions, comments
- Newsletter issue content
- Past notes/posts history (for gap analysis)
- Web trend findings

If no source material is provided, stop and ask the orchestrator or user for inputs. This skill cannot ideate from nothing.

### Step 2: Extract Angles Using Reference Categories

Read the reference file's extraction categories. For each source, systematically scan for angles matching each category.

Document each raw extraction with:
- The category it matches (e.g., "Surprising Data Points", "Quotable One-Liners")
- The specific passage or data point from the source
- The source reference (video title + ID, newsletter title + URL, etc.)

Do not filter at this stage — capture everything that matches. Filtering happens in Step 6.

### Step 3: Map Extractions to Content Types

Use the reference file's source-to-type mapping table to assign each extraction a content type.

- Focus on primary types first — these are the most natural fit for each source
- Check secondary types only if primary types don't yield enough strong ideas
- Flag extractions that don't cleanly map to any type — these may need rework or removal

### Step 4: Gap Analysis Against Content History

If past content history is available:

1. Tally how many times each content type has been used recently
2. Identify the 2-3 types with the fewest recent uses
3. Bias extraction toward underused types — actively look for angles that fill gaps
4. Flag gap-filling ideas in their rationale so the user understands the strategic reasoning

If no content history is available, skip gap analysis and distribute across types naturally.

### Step 5: Integrate Trending Topics

If web trend findings are provided:

1. Cross-reference trends with the user's published content for unique angles
2. Prioritize trends where the user has direct experience (highest priority) over opinion-only takes (skip)
3. Only include trend-based ideas where the user adds genuine insight — not "me too" takes

Use the reference file's trending topic integration framework if available.

### Step 6: Quality-Filter Every Idea

Run each candidate idea through the reference file's quality criteria checklist. Apply criteria in order — if an idea fails an early criterion, skip the rest and rework or discard.

Common quality gates (reference file may specify additional):
- Standalone value — interesting without consuming the original source
- Specificity — includes concrete details, not vague generalities
- Single idea — one core message per idea
- Maps to a content type — fits cleanly into the taxonomy
- Not a rehash — substantially different from past content
- Engagement angle — gives readers a reason to interact

### Step 7: Output Structured Ideas

Format surviving ideas using the reference file's output structure. Each idea should include all required fields (typically: topic, type, source, pitch, rationale).

Respect the reference file's volume target. If fewer ideas survive quality filtering than the minimum, note this honestly rather than padding with weak ideas.

## Voice Application

Before finalizing any written output, invoke the `creator-stack:voice` skill to apply voice rules. Idea pitches and rationales should reflect the user's authentic voice, not generic content strategy language.

## Brand Compliance

When creating assets for The AI Launchpad, invoke `creator-stack:brand-guidelines` to resolve the correct design system and check anti-patterns.

## Quality Checklist

Verify completion before finalizing ideation:
- [ ] Source material received and organized by type (Step 1)
- [ ] All extraction categories from reference applied to each source (Step 2)
- [ ] Extractions mapped to content types using reference's mapping table (Step 3)
- [ ] Gap analysis completed against content history (Step 4)
- [ ] Trending topics integrated with proximity scoring (Step 5)
- [ ] Every idea passed reference's quality criteria (Step 6)
- [ ] Ideas formatted in reference's output structure (Step 7)
- [ ] At least 3 different content types represented in the batch
- [ ] Volume within reference's target range
- [ ] Voice skill applied to final output

## Common Pitfalls to Avoid

1. **Inventing ideas without source material**: Every idea must trace to a specific source. If you can't point to the passage, data point, or trend that inspired it, the idea is fabricated — not extracted.
2. **Running competitor research**: This skill extracts from the user's own content and provided trends. Competitor analysis is `creator-stack:research` territory.
3. **Skipping gap analysis**: Content type variety prevents audience fatigue. Always check history and bias toward underused types.
4. **Forcing weak ideas to hit volume targets**: If sources don't yield enough strong ideas, say so. Five strong ideas beat eight padded ones.
5. **Ignoring the reference file**: The reference file IS the extraction framework. Don't improvise your own categories, criteria, or output format — use what the reference specifies.
6. **Processing all sources sequentially**: Use `Agent` tool subagents for parallel extraction across sources. Sequential processing is slower and causes context bleed between unrelated sources.

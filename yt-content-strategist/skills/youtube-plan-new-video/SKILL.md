---
name: youtube-plan-new-video
description: Generate a complete video plan with optimized title, thumbnail, and hook concepts based on research. Orchestrates specialized skills (youtube-title, youtube-thumbnail, youtube-video-hook) to create production-ready video plans. Use after research is complete or when the user wants to plan a new video.
---

# YouTube Video Planning

## Overview

This skill generates complete video plans by orchestrating specialized skills to create optimized titles, thumbnails, and hooks. It takes research as input and produces a production-ready plan with all creative elements needed to maximize video performance.

**Core Principle**: Leverage specialized skills to ensure proven patterns for CTR (title/thumbnail) and retention (hook). Never generate these elements manually.

## When to Use

Use this skill when:
- Research has been completed and you need to generate title/thumbnail/hook concepts
- The user asks to plan a new video
- You need to create production-ready creative elements
- You want to generate multiple options for the user to choose from

## Prerequisites

**MANDATORY**: Research for the new video must be completed first. Either:
1. Research file exists at `./youtube/episode/[episode_number]_[topic_short_name]/`, OR
2. Invoke `youtube-research-video-topic` skill to conduct research first

## Planning Workflow

Execute all steps below to complete the video plan.

### Step 0: Load Research

Read the research file for this episode:
- Location: `./youtube/episode/[episode_number]_[topic_short_name]/research.md`

If research doesn't exist, invoke `youtube-research-video-topic` skill first.

### Step 1: Generate Title Options

**MANDATORY**: Invoke `youtube-title` skill to generate optimized titles.

Execute these actions:
1. **Invoke `youtube-title` skill** with:
   - Video topic
   - Target audience
   - Content gaps and unique value proposition from research
   - Competitor insights

2. Review generated titles (should get 3-5 options)

3. Document all title options in the plan file

**Why this is mandatory**: Ensures proven CTR patterns, curiosity generation, and data-backed title structures.

**NOTE**: You MUST complete title generation before proceeding to thumbnails, as thumbnails need to complement the titles.

### Step 2: Generate Thumbnail Concepts

**MANDATORY**: Invoke `youtube-thumbnail` skill to generate thumbnail concepts.

Execute these actions:
1. **Invoke `youtube-thumbnail` skill** with:
   - Each title option from Step 1
   - Video topic and angle
   - Target audience

2. Review generated thumbnail concepts (should get 2 concepts per title)

3. Document all title/thumbnail pairings in the plan file

**Why this is mandatory**: Ensures visual complementarity with titles, proven design patterns, and curiosity amplification.

### Step 3: Generate Hook Strategy

**MANDATORY**: Invoke `youtube-video-hook` skill to generate retention-optimized hooks.

Execute these actions:
1. **Invoke `youtube-video-hook` skill** with:
   - Selected title (or top title option)
   - Thumbnail description
   - Video topic
   - Curiosity created by title/thumbnail

2. Review generated hook options

3. Document hook strategies in the plan file

**Why this is mandatory**: Ensures hooks extend curiosity (not repeat title), avoid forbidden patterns, and maximize retention.

### Step 4: Create Recommended Combinations

Analyze all generated options and create 2-3 recommended combinations:
- Title + Thumbnail + Hook that work together
- Rationale for each combination
- Pros/cons of each approach

Document these recommendations in the plan file.

### Step 5: High-Level Content Outline

Create and document strategic roadmap:
- Break video into sections (Hook, Intro, Main Content, Outro)
- List key points and estimated durations
- Identify critical demonstrations/examples
- Note transitions

Keep it strategic: Structure and key points only, not detailed scripts. Do not assume any specific content that should be covered/demonstrated, leave that to the content creator. The goal here is to provide a high-level structure that can be fleshed out by the content creator. Focus on what's important to cover from the viewer's perspective.

### Step 6: Finalize Production Plan

Create a new plan file in `./youtube/` with:
- All title options
- All thumbnail concepts
- All hook strategies
- Recommended combinations
- Next steps for production

### Step 7: Finalize Plan with User's Feedback

After generating the complete plan, present a high-level summary of the plan to the user with your overall recommendation. Once you get the user's final selection, update the plan with the user's final selection.

In the final selection, include the following:
- **Title**: [Selected title]
- **Thumbnails**: 
   - ![Thumbnail A](/path/to/thumbnail_a.png)
      Thumbnail A Description
   - ![Thumbnail B](/path/to/thumbnail_b.png)
      Thumbnail B Description
   - ![Thumbnail C](/path/to/thumbnail_c.png)
      Thumbnail C Description
- **Hook**: [Selected hook strategy]
- **Rationale**: [Why this combination works]
- **Pros**: [Strengths]
- **Cons**: [Potential weaknesses]

Thumbnails should be the actual generated images embedded in the markdown file. Note, if you have not already, generate variations of the selected thumbnail for AB testing. A final selection should **ALWAYS** have 3 thumbnails to test. 

## Output Structure

Create a new plan file at: `./youtube/episode/[episode_number]_[topic_short_name]/plan.md`

The plan file should contain:
```markdown
# Video Plan: [Video Topic]

**Created**: [Date]
**Research File**: [Link to research file]

## Title Options
[Generated by youtube-title skill - include all 3-5 options with rationale]

## Thumbnail Concepts
[Generated by youtube-thumbnail skill - include all concepts with descriptions]

### Title/Thumbnail Pairings
1. **Title**: [Title 1]
   **Thumbnail A**: [Description]
   **Thumbnail B**: [Description]

2. **Title**: [Title 2]
   ...

## Hook Strategies
[Generated by youtube-video-hook skill - include all options]

## Recommended Combinations
### Option 1: [Name]
- **Title**: [Title]
- **Thumbnail**: [Description]
- **Hook**: [Hook strategy]
- **Rationale**: [Why this combination works]
- **Pros**: [Strengths]
- **Cons**: [Potential weaknesses]

### Option 2: [Name]
...

## Final Selection

### Selected Option: [Name]
- **Title**: [Title]
- **Thumbnails**: 
   - ![Thumbnail A](/path/to/thumbnail_a.png)
      Thumbnail A Description
   - ![Thumbnail B](/path/to/thumbnail_b.png)
      Thumbnail B Description
   - ![Thumbnail C](/path/to/thumbnail_c.png)
      Thumbnail C Description
- **Hook**: [Hook strategy]
- **Rationale**: [Why this combination works]
- **Pros**: [Strengths]
- **Cons**: [Potential weaknesses]

## Skills Used Verification
- ✅ youtube-title skill invoked
- ✅ youtube-thumbnail skill invoked
- ✅ youtube-video-hook skill invoked

## Production Status
**Status**: Plan Complete - Ready for Production
**Updated**: [Date]
```

## Execution Guidelines

### Always Invoke Specialized Skills

**NEVER** generate titles, thumbnails, or hooks manually. Always invoke:
- `youtube-title` for title generation
- `youtube-thumbnail` for thumbnail concepts
- `youtube-video-hook` for hook strategies

### Provide Multiple Options

Generate and present multiple options for the user:
- 3-5 title options
- 2 thumbnail concepts per title
- 2-3 hook strategies
- 2-3 recommended combinations

**CRITICAL**: Always include ALL options so the user can make an informed decision. Do not simply select one option and tell the user to use it.

### Ensure Complementarity

Verify that title/thumbnail/hook work together:
- Thumbnail complements title visually
- Hook extends curiosity (doesn't repeat title)
- All elements align with the unique value proposition

### Back Recommendations with Research

When recommending combinations:
- Reference content gaps from research
- Cite competitor insights
- Explain how the combination addresses the opportunity

## Integration with Other Skills

This skill orchestrates specialized skills. Invoke them in this order:

**youtube-research-video-topic** (Prerequisites): Invoke if research doesn't exist

**youtube-title** (Step 1): Invoke to generate 3-5 optimized title options following proven CTR patterns

**youtube-thumbnail** (Step 2): Invoke to generate thumbnail concepts that complement titles visually

**youtube-video-hook** (Step 3): Invoke to generate hook strategies using proven retention patterns

**Planning Skill Role**: Orchestrate specialized skills and synthesize their outputs into cohesive video plans.

## Quality Checklist

Verify completion before finalizing plan:
- [ ] Research file loaded and reviewed
- [ ] **youtube-title skill invoked** - 3-5 options generated
- [ ] **youtube-thumbnail skill invoked** - Concepts for each title
- [ ] **youtube-video-hook skill invoked** - Hook strategies generated
- [ ] 2-3 recommended combinations created with rationale
- [ ] All options documented (not just one recommendation)
- [ ] Title/thumbnail/hook complementarity verified
- [ ] Recommendations backed by research insights

## Tools to Use

Execute planning using these tools:

**Skill Invocations** (MANDATORY):
- `youtube-research-video-topic` - Invoke if research doesn't exist
- `youtube-title` - Invoke to generate title options
- `youtube-thumbnail` - Invoke to generate thumbnail concepts
- `youtube-video-hook` - Invoke to generate hook strategies

## Common Pitfalls to Avoid

1. **Skipping Skill Invocation**: Generating titles/thumbnails/hooks manually → Must invoke specialized skills
2. **Single Option**: Only providing one recommendation → Provide 2-3 combinations with all options
3. **Missing Research**: Starting without research → Load research or invoke research skill first
4. **Ignoring Complementarity**: Title/thumbnail/hook don't work together → Verify alignment
5. **No Rationale**: Recommendations without explanation → Back with research insights

## Example Execution

**Scenario**: User requests plan for video about "Building AI agents with memory" (research already complete)

Execute workflow:
1. Load research → Read `18_ai_agents_with_memory.md`, extract ⭐⭐⭐ gap for practical memory implementation
2. Invoke `youtube-title` skill → Generate 5 title options focused on practical implementation
3. Invoke `youtube-thumbnail` skill → Generate 2 concepts for each title (10 total)
4. Invoke `youtube-video-hook` skill → Generate 3 hook strategies
5. Create combinations → Recommend 3 title/thumbnail/hook combinations with rationale
6. Create plan file → Save all options and recommendations to `./youtube/episode/[episode_number]_[topic_short_name]/plan.md`

**Result**: Production-ready plan with multiple options for the user to choose from, all backed by research and generated using proven patterns.

**CRITICAL**: Present all options to the user, not just your top recommendation. The user should make the final decision.

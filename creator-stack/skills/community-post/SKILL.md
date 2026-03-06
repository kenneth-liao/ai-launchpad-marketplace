---
name: community-post
description: "Create YouTube community posts that drive views and audience engagement. Use when asked to create a community post, promote a video on the community tab, run a poll, or engage the YouTube audience between uploads. Also use when the user mentions 'community tab', 'YouTube poll', or 'post to community'."
---

# Create Community Post

## Overview

This orchestrator creates YouTube community posts by sequencing `creator-stack:research` for strategic context and `creator-stack:write` for content generation. It handles episode awareness, post type selection, and output management — all actual content generation and strategy are delegated to the foundation skills.

**Core Principle**: This is a thin orchestrator. Strategy lives in `creator-stack:research` (via its `references/youtube-community-strategy.md`). Templates and formatting live in `creator-stack:write` (via its `references/youtube-community-post.md`). This skill manages the workflow sequence, episode context, and user decisions only.

## How Reference Delegation Works

Both foundation skills own their own reference files. When you invoke `creator-stack:research` and specify "youtube community post" as context, it loads its strategy reference. When you invoke `creator-stack:write` with content type "youtube community post", it loads its template reference. Those files live in each skill's directory, not here.

## When to Use

Use this skill when:
- Promoting a new or upcoming video through the community tab
- Maintaining audience engagement between video uploads
- Running audience research polls to inform future content
- Driving conversions (affiliate links, memberships, newsletter signups)
- Creating any community tab content for a YouTube channel

## Prerequisites

**Optional**: An episode directory at `./youtube/episode/[episode_number]_[topic_short_name]/` with a `plan.md` file. This is only needed for video-linked posts (pre-release, launch day, post-launch). Between-video engagement posts do not require an episode directory.

## Workflow

Execute all steps below in order.

### Step 0: Episode Context Check

Check if the user has specified an episode or if an episode directory exists at `./youtube/episode/[episode_number]_[topic_short_name]/`.

**If episode directory exists:**
- Read `plan.md` for video title, topic, and context
- Suggest a lifecycle phase based on context:
  - Video not yet published → **pre-release**
  - Video just published → **launch day**
  - Video published 3-7 days ago → **post-launch**
- Use this context to inform the research invocation in Step 1

**If no episode directory:**
- Default to **between videos** mode
- Posts will focus on engagement, audience research, or value delivery

### Step 1: Invoke Research for Strategic Context

Invoke `creator-stack:research` with the community post context to determine strategy.

Provide:
- The lifecycle phase (from Step 0 or user input)
- The video topic (if applicable)
- The user's stated goal (engagement, promotion, research, conversion)

The research skill applies the strategy framework to determine:
- Optimal post type ranking for the context
- Timing recommendations
- Strategic rationale for the approach

NOTE: This is a lighter research invocation — asking research to apply the strategy framework to the user's context, not to do full competitor analysis.

### Step 2: Present Post Type Options

Based on the research output, present the ranked post type options to the user:

1. **Poll** (text or image) — highest engagement
2. **Video teaser/clip** — high engagement
3. **GIF** — medium-high engagement
4. **Image** — medium engagement
5. **Quiz** — medium engagement
6. **Text-only** — lowest engagement

Include the research skill's recommendation for which type best fits the context. User selects their preferred type.

**Default to polls when unsure** — they have the lowest friction and highest engagement.

### Step 3: Invoke Writing Skill for Content

Invoke `creator-stack:write` with content type "youtube community post" to draft the post.

Provide:
- The selected post type from Step 2
- The strategic context from Step 1
- The episode context from Step 0 (if applicable)
- The lifecycle phase and user's stated goal

The writing skill automatically invokes `creator-stack:voice` for voice consistency. Its reference file contains all templates, formatting rules, and the 288-character hook rule.

### Step 4: Quality Checklist

Verify the drafted post against all eight criteria before presenting to the user:

- [ ] Hook lands within 288 characters (visible preview cutoff)
- [ ] Total length is 150-400 characters
- [ ] Ends with a CTA (question, poll, or link)
- [ ] Conversational tone — not corporate or automated
- [ ] First person, direct address ("I" and "you")
- [ ] Mobile-friendly — short paragraphs, line breaks between ideas
- [ ] NOT a generic "new video out" link dump
- [ ] Post type matches the stated purpose/phase

If any criterion fails, request a revision from `creator-stack:write` before presenting to the user.

### Step 5: Save Output

Present the final post to the user for approval.

**If episode directory exists:**
- After user approval, append to `./youtube/episode/[episode_number]_[topic_short_name]/community-posts.md`

**If no episode directory:**
- Present the final post inline to the user

## Output Format

When saving to `community-posts.md`, use this structure:

```markdown
# Community Posts - Episode [Number]: [Topic]

## [Phase] Post - [Date]

**Type:** [Poll / Teaser / GIF / Image / Quiz / Text]
**Phase:** [Pre-release / Launch Day / Post-Launch / Between Videos]
**Goal:** [Engagement / Promotion / Research / Conversion]

### Post Content

[Final post text]

### Notes

- Suggested timing: [from research]
- CTA type: [question / poll / link]
```

Multiple posts for the same episode are appended to the same file with a horizontal rule separator (`---`) between entries.

## Quality Checklist

Verify completion before finalizing:
- [ ] Episode context checked (Step 0)
- [ ] `creator-stack:research` invoked — strategic context determined
- [ ] Post type options presented and user selection received
- [ ] `creator-stack:write` invoked — post drafted
- [ ] Voice consistency maintained (handled by writing skill)
- [ ] All 8 quality criteria passed (Step 4)
- [ ] Post presented to user for approval
- [ ] Output saved to episode directory or presented inline

## Common Pitfalls

1. **Writing templates inline**: All templates live in the writing skill's `references/youtube-community-post.md` — don't duplicate them here.
2. **Embedding strategy logic**: All strategy lives in research's `references/youtube-community-strategy.md` — don't hardcode timing, cadence, or algorithm advice here.
3. **Skipping foundation skill invocations**: Both research and writing skills should be invoked — they have the proven patterns and quality logic.
4. **Ignoring episode context**: Always check for an episode directory first — it changes the entire strategic approach.
5. **Defaulting to "new video out" posts**: The research and writing skills are specifically designed to avoid generic link dumps — trust the foundation skills.
6. **Skipping the quality checklist**: Every post should pass all 8 criteria before presenting to the user.

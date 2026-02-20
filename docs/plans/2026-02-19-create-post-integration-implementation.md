# Create-Post Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate the imported `temp/create-youtube-post` skill into the marketplace as a thin YouTube orchestrator (`youtube:create-post`) that delegates to existing foundation skills.

**Architecture:** The imported skill's content splits into three locations: (1) a thin orchestrator at `youtube/skills/create-post/SKILL.md`, (2) a strategy reference at `content-strategy/skills/research/references/youtube-community-strategy.md`, and (3) a writing reference at `writing/skills/copywriting/references/youtube-community-post.md`. The orchestrator follows the same pattern as `youtube:repurpose-video`.

**Tech Stack:** Claude Code skill framework (SKILL.md files, reference files, plugin.json)

**Design Doc:** `docs/plans/2026-02-19-create-post-integration-design.md`

---

### Task 1: Create the writing reference file

**Files:**
- Create: `writing/skills/copywriting/references/youtube-community-post.md`

**Step 1: Create the reference file**

Extract writing-specific content from the imported skill into a new reference file. This includes:
- The 9 post templates (topic poll, video teaser, launch day promo, quick tip, behind-the-scenes, resurface old video, commitment poll, hot take, audience research)
- The 288-character preview rule
- Post structure (hook, body, CTA) and optimal length (150-400 characters)
- CTA patterns by goal (poll, video promo, engagement, conversion, commitment)
- Formatting rules (mobile-first, conversational tone, first person)
- Common mistakes to avoid (9 ranked by damage)
- Post types with engagement rankings (poll highest, text-only lowest)

Follow the pattern of existing reference files like `writing/skills/copywriting/references/twitter.md`:
- Start with a `# YouTube Community Post Conventions` header
- Include a note that voice rules are handled by `writing:voice`
- Focus on structure, templates, and platform-specific conventions
- Keep it under 300 lines

Source material:
- Templates and formatting rules from `temp/create-youtube-post/SKILL.md` (lines 56-180)
- Post types detail from `temp/create-youtube-post/reference/youtube-posts-reference.md` (lines 23-71)
- CTA strategy detail from `temp/create-youtube-post/reference/youtube-posts-reference.md` (lines 130-155)
- Formatting rules from `temp/create-youtube-post/reference/youtube-posts-reference.md` (lines 157-183)
- Mistakes to avoid from `temp/create-youtube-post/reference/youtube-posts-reference.md` (lines 273-287)

**Step 2: Update the copywriting SKILL.md content type table**

In `writing/skills/copywriting/SKILL.md`, add a new row to the Content Type Resolution table (line 23):

Add after the Substack Note row:
```
| YouTube community post | `references/youtube-community-post.md` | 288-char rule, templates, CTAs |
```

**Step 3: Commit**

```bash
git add writing/skills/copywriting/references/youtube-community-post.md writing/skills/copywriting/SKILL.md
git commit -m "feat(writing): add youtube community post reference for copywriting"
```

---

### Task 2: Create the strategy reference file

**Files:**
- Create: `content-strategy/skills/research/references/youtube-community-strategy.md`

**Step 1: Create the reference file**

Extract strategy content from the imported skill's reference file. This includes:
- 3-Phase Video Cycle (pre-release, launch day, post-launch) with goals and example posts
- Between-videos filler content strategy
- Algorithm impact (5 key effects: channel activity signal, home feed distribution, returning viewer rate, sustained cadence, pre-video priming)
- Posting cadence (2-3/week optimal, weekly mix suggestions)
- Timing strategies (12-3pm, 5-8pm, analytics-based)
- The Poll-to-Video Pipeline (audience feedback loop)
- Conversion best practices (affiliates, memberships, products, email, courses, 80/20 rule)
- Measurement framework (6 metrics: impressions, engagement rate, poll votes, comments, link clicks, subscriber change)

Follow the pattern of `content-strategy/skills/research/references/research-frameworks.md`:
- Start with a `# YouTube Community Post Strategy` header
- Focus on strategic decisions, data, and frameworks
- Include source citations from the original reference
- Keep it under 300 lines

Source material:
- Video cycle from `temp/create-youtube-post/reference/youtube-posts-reference.md` (lines 74-127)
- Algorithm impact from lines 225-234
- Posting cadence from lines 186-206
- Timing from lines 208-222
- Poll-to-Video Pipeline from lines 236-254
- Conversion from lines 256-269
- Measurement from lines 290-303
- Sources from lines 306-319

**Step 2: Commit**

```bash
git add content-strategy/skills/research/references/youtube-community-strategy.md
git commit -m "feat(content-strategy): add youtube community post strategy reference"
```

---

### Task 3: Create the orchestrator skill

**Files:**
- Create: `youtube/skills/create-post/SKILL.md`

**Step 1: Create the orchestrator SKILL.md**

Write a thin orchestrator following the pattern of `youtube/skills/repurpose-video/SKILL.md`. The orchestrator should:

**Frontmatter:**
```yaml
---
name: create-post
description: Create high-engagement YouTube community posts that drive views, build audience loyalty, and maximize conversion. This is a thin orchestrator — it sequences content-strategy:research and writing:copywriting invocations for community post creation.
---
```

**Sections to include:**
1. Overview (thin orchestrator principle, what it does)
2. When to Use (promoting a video, between-video engagement, audience research, conversion)
3. Prerequisites (optional: episode directory for video-linked posts)
4. Workflow:
   - Step 0: Episode Context Check — check if episode directory exists at `./youtube/episode/[num]_[topic]/`. If yes, read `plan.md` for video title, topic, and context. Suggest lifecycle phase based on context. If no, default to "between videos" mode.
   - Step 1: Invoke `content-strategy:research` with `references/youtube-community-strategy.md` — determine optimal phase, timing, post type ranking, and strategic context.
   - Step 2: Present post type options to user (poll, teaser, GIF, image, quiz, text-only) with engagement rankings. User selects.
   - Step 3: Invoke `writing:copywriting` with `references/youtube-community-post.md` — draft the post using the selected template. The copywriting skill auto-invokes `writing:voice`.
   - Step 4: Quality checklist (8-point verification from imported skill)
   - Step 5: Save output — if episode directory exists, save to `./youtube/episode/[num]_[topic]/community-posts.md`. Otherwise, present inline.
5. Output format (markdown template for saved file)
6. Quality checklist
7. Common pitfalls to avoid

**Keep the orchestrator thin.** It should NOT contain templates, formatting rules, or strategy — those live in the reference files. The orchestrator manages workflow sequence, episode awareness, and user decisions only.

Target: under 200 lines (matching repurpose-video at 157 lines).

**Step 2: Commit**

```bash
git add youtube/skills/create-post/SKILL.md
git commit -m "feat(youtube): add create-post orchestrator skill"
```

---

### Task 4: Update plugin versions

**Files:**
- Modify: `youtube/.claude-plugin/plugin.json`
- Modify: `content-strategy/.claude-plugin/plugin.json`
- Modify: `writing/.claude-plugin/plugin.json`

**Step 1: Bump youtube plugin version**

In `youtube/.claude-plugin/plugin.json`, change `"version": "1.0.0"` to `"version": "1.1.0"` (minor bump — new skill added).

**Step 2: Bump content-strategy plugin version**

In `content-strategy/.claude-plugin/plugin.json`, change `"version": "1.0.0"` to `"version": "1.1.0"` (minor bump — new reference file added).

**Step 3: Bump writing plugin version**

In `writing/.claude-plugin/plugin.json`, change `"version": "1.0.0"` to `"version": "1.1.0"` (minor bump — new reference file added, content type table updated).

**Step 4: Commit**

```bash
git add youtube/.claude-plugin/plugin.json content-strategy/.claude-plugin/plugin.json writing/.claude-plugin/plugin.json
git commit -m "chore: bump plugin versions for create-post integration"
```

---

### Task 5: Clean up and final commit

**Files:**
- Delete: `temp/create-youtube-post/` (entire directory)

**Step 1: Delete the temp directory**

Remove the imported skill now that its content has been integrated:
```bash
rm -rf temp/create-youtube-post
```

**Step 2: Verify the integration**

Check that all files are in place:
```bash
ls youtube/skills/create-post/SKILL.md
ls content-strategy/skills/research/references/youtube-community-strategy.md
ls writing/skills/copywriting/references/youtube-community-post.md
```

Verify the orchestrator SKILL.md references the correct skills:
- Contains `content-strategy:research`
- Contains `writing:copywriting`
- Contains `references/youtube-community-strategy.md`
- Contains `references/youtube-community-post.md`
- Contains `writing:voice` (mentioned as auto-invoked by copywriting)

Verify the copywriting SKILL.md content type table includes the new row.

**Step 3: Commit cleanup**

```bash
git add -A
git commit -m "chore: remove temp/create-youtube-post after integration"
```

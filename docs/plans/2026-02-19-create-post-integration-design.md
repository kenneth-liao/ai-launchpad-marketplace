# Design: Integrate create-youtube-post as youtube:create-post

## Summary

Integrate the imported `temp/create-youtube-post` skill into the marketplace as a thin YouTube orchestrator (`youtube:create-post`) that delegates to existing foundation skills. The imported skill's content splits across three locations following the composable architecture.

## Architecture

```
youtube:create-post (ORCHESTRATOR)
│
├─ Step 0: Episode context check
│   ├─ Episode dir exists → load plan.md, suggest lifecycle phase
│   └─ No episode → "between videos" mode
│
├─ Step 1: Invoke content-strategy:research
│   └─ loads youtube-community-strategy.md
│   └─ determines optimal phase, timing, post type ranking
│
├─ Step 2: User selects post type
│   └─ poll, teaser, GIF, image, quiz, text-only
│
├─ Step 3: Invoke writing:copywriting
│   └─ auto-loads youtube-community-post.md (templates, 288-char rule)
│   └─ auto-invokes writing:voice
│
├─ Step 4: Quality checklist (8-point verification)
│
└─ Output: save to episode dir or standalone
```

## Content Split

The imported skill's content (SKILL.md + reference/youtube-posts-reference.md) splits into three files:

### 1. Orchestrator: `youtube/skills/create-post/SKILL.md`

Thin workflow sequencing only:
- Episode directory awareness (check for existing plan.md, suggest lifecycle phase)
- Workflow steps (research → type selection → draft → quality check)
- Post type menu (poll, teaser, GIF, image, quiz, text-only) with engagement rankings
- Quality checklist (8-point verification)
- Output format and save location

### 2. Strategy reference: `content-strategy/skills/research/references/youtube-community-strategy.md`

Strategic content loaded by content-strategy:research:
- 3-Phase Video Cycle (pre-release, launch day, post-launch) + between-videos
- Algorithm impact (5 key effects)
- Posting cadence (2-3/week optimal)
- Timing strategies (12-3pm, 5-8pm, analytics-based)
- Conversion tactics (affiliates, memberships, products, email, courses, 80/20 rule)
- Measurement framework (6 metrics)
- Poll-to-Video Pipeline (audience feedback loop)

### 3. Writing reference: `writing/skills/copywriting/references/youtube-community-post.md`

Writing patterns loaded by writing:copywriting:
- 9 post templates (topic poll, video teaser, launch day promo, quick tip, behind-the-scenes, resurface old video, commitment poll, hot take, audience research)
- 288-character preview rule
- Post structure (hook → body → CTA)
- Optimal length (150-400 characters)
- CTA patterns by goal
- Formatting rules (mobile-first, conversational tone, first person)
- Common mistakes to avoid (9 ranked by damage)

## Files to Create/Modify

| Action | File | Purpose |
|--------|------|---------|
| Create | `youtube/skills/create-post/SKILL.md` | Thin orchestrator |
| Create | `content-strategy/skills/research/references/youtube-community-strategy.md` | Strategy reference |
| Create | `writing/skills/copywriting/references/youtube-community-post.md` | Writing reference |
| Update | `youtube/.claude-plugin/plugin.json` | Bump version |
| Update | `content-strategy/.claude-plugin/plugin.json` | Bump version |
| Update | `writing/.claude-plugin/plugin.json` | Bump version |
| Delete | `temp/create-youtube-post/` | Clean up after integration |

## Design Decisions

1. **Orchestrator placement**: youtube/ plugin — community posts are YouTube-specific and lifecycle-aware
2. **Writing delegation**: Templates and formatting → writing:copywriting reference, not inline in orchestrator
3. **Strategy delegation**: Lifecycle, timing, algorithm → content-strategy:research reference
4. **Episode awareness**: Orchestrator checks for episode directories, loads plan.md for context, suggests lifecycle phase
5. **Voice/brand reuse**: writing:copywriting already invokes writing:voice and branding-kit:brand-guidelines — no extra hooks needed

## Patterns Followed

- Thin orchestrator pattern (matches repurpose-video, plan-video)
- Reference file pattern for platform-specific content
- Episode directory convention (`./youtube/episode/[num]_[topic]/`)
- Quality checklist pattern
- Explicit skill invocation (not ambient activation)
- SKILL.md under 500 lines
- Flat structure (max 2 levels)

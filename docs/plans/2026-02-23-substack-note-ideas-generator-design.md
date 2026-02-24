# Substack Note Ideas Generator — Design

## Overview

A new orchestrator skill (`substack:generate-note-ideas`) that scans published content sources, tracks what's been processed, and generates a batch of high-quality Substack Note ideas. Sits upstream of `substack:create-note` — ideation vs execution, cleanly separated.

## Skill Identity

| Field | Value |
|-------|-------|
| **Name** | `generate-note-ideas` |
| **Plugin** | `substack` |
| **Category** | Orchestrator |
| **Trigger** | "generate Substack note ideas", "give me note ideas", "what should I post on Notes" |

## Architecture

### Approach: Orchestrator + New Reference File

A thin orchestrator that delegates all strategic work to `content-strategy:research` via a new ideation reference file. This follows the same composition pattern as `create-note` (which uses `substack-notes-strategy.md`) and keeps the orchestrator free of content generation logic.

### Files to Create

| File | Type | Purpose |
|------|------|---------|
| `substack/skills/generate-note-ideas/SKILL.md` | Orchestrator skill | Workflow definition |
| `content-strategy/skills/research/references/substack-notes-ideation.md` | Reference | Teaches research skill how to extract note ideas from published content |

### Runtime Output Files (not committed)

| File | Purpose |
|------|---------|
| `./substack/notes/ideas.md` | Append-only ideas log |
| `./substack/notes/processed-log.md` | Source-level tracking to prevent redundant scans |

## Content Sources

All sources are **published content**, fetched via APIs — not local files.

### YouTube (via YouTube MCP tools)
- `get_channel_details` → user's channel
- `search_videos` → recent published videos
- `get_video_transcript` → full transcript for new videos
- `get_video_details` → title, description, stats

### Substack Newsletter (via web fetch)
- Fetch user's Substack archive page → discover published issues
- Web fetch each new issue URL → full content

### Substack Notes History (via web fetch)
- Fetch user's Notes feed → see what's already been posted
- Feeds gap analysis (overrepresented types/topics)

### Web Trends (via web search)
- Search trending topics in user's niche
- Always runs regardless of new source availability

## Processed Log

Source-level tracking at `./substack/notes/processed-log.md`:

```markdown
# Processed Content Log

## YouTube Videos
| Video ID | Title | Scanned | Ideas Generated |
|----------|-------|---------|-----------------|
| abc123 | AI Debugging Myths | 2026-02-23 | 3 |

## Newsletter Issues
| URL | Title | Scanned | Ideas Generated |
|-----|-------|---------|-----------------|
| https://example.substack.com/p/topic | Topic Title | 2026-02-23 | 2 |

## Substack Notes Scanned
| Last Scan Date | Notes Reviewed | Gap Analysis |
|----------------|----------------|-------------|
| 2026-02-23 | 15 | Missing: Build-in-Public, Income Proof |
```

## Orchestrator Workflow

### Step 0: Load Processed Log
- Read `./substack/notes/processed-log.md` (create if doesn't exist)
- Get list of already-processed video IDs and newsletter issue URLs

### Step 1: Fetch Published Content
- **YouTube:** Use MCP tools to get recent videos from user's channel. Compare video IDs against processed log. For new videos: fetch transcript and details.
- **Substack Newsletter:** Web fetch archive page. Compare issue URLs against processed log. For new issues: web fetch full content.
- **Substack Notes:** Web fetch user's Notes feed for gap analysis and duplicate prevention.
- **Web Trends:** Web search for trending topics in user's niche. Always runs.

### Step 2: Invoke `content-strategy:research` with Ideation Reference
- Pass all loaded source material and past notes history
- Reference: `references/substack-notes-ideation.md`
- Research skill extracts note-worthy angles and returns structured ideas

### Step 3: Present Ideas to User
- Present batch of 5-10 ideas in structured format
- Each idea: topic, suggested note type, source, one-line pitch, strategic rationale
- User can approve, remove ideas, or request more

### Step 4: Save Output
- Append approved ideas to `./substack/notes/ideas.md`
- Update `./substack/notes/processed-log.md` with newly scanned sources
- Each idea entry is timestamped with source reference

### Step 5: Handoff Suggestion
- Suggest user can invoke `substack:create-note` to write any approved idea
- No automatic invocation — user decides when to write

## Ideas Output Format

```markdown
# Substack Note Ideas

## Run: 2026-02-23

### Idea 1
**Topic:** Why most AI coding tools fail at debugging
**Type:** Contrarian Statement
**Source:** YouTube — "AI Debugging Myths" (video ID: abc123)
**Pitch:** Challenge the assumption that AI can replace systematic debugging.
**Rationale:** High engagement potential — contrarian takes on AI are restackable.

---

### Idea 2
**Topic:** 3 MCP patterns I use every day
**Type:** List-Based Tactical
**Source:** Newsletter — "Building with MCP Servers"
**Pitch:** Extract the three most actionable MCP patterns into a standalone note.
**Rationale:** Tactical lists drive saves and restacks.

---
(5-10 ideas per run)
```

## Ideation Reference File

`content-strategy/skills/research/references/substack-notes-ideation.md` contains:

1. **Angle extraction framework** — How to read transcripts, newsletters, and repurposed content to identify note-worthy moments:
   - Surprising data points or counterintuitive findings
   - Quotable one-liners buried in longer content
   - Behind-the-scenes process details
   - Unanswered questions or reader curiosities
   - Mini-lessons that stand alone (2-5 sentences)
   - Contrarian takes embedded in nuanced discussions

2. **Source-to-type mapping** — Which note types naturally emerge from which sources:
   - YouTube transcript → Pattern Observation, Contrarian Statement, Problem→Solution
   - Newsletter issue → Newsletter Teaser, Single-Punch Wisdom, List-Based Tactical
   - Past notes history → Gap analysis (underused types)
   - Web trends → Hot Take, Direct Advice tied to timely topics

3. **Idea quality criteria** — What makes a good idea:
   - Standalone value (doesn't require watching video or reading issue)
   - Specificity (numbers, concrete examples)
   - One idea per note
   - Maps cleanly to one of the 10 note types
   - Not a rehash of something already covered in past notes

4. **Trending topic integration** — How to blend web/niche trends with existing content

5. **Output format** — Structured idea format (topic, type, source, pitch, rationale)

## Relationship to Existing Skills

```
generate-note-ideas  →  ideas.md (batch of 5-10 ideas)
        ↓
User picks an idea
        ↓
create-note  →  actual written note (via research + copywriting + voice)
```

- `generate-note-ideas` is **upstream** of `create-note`
- It never writes actual notes — only generates ideas
- `create-note` remains unchanged
- Both are orchestrators in the `substack` plugin

## Key Behaviors

- **No new sources:** Still runs web trend analysis and past-notes gap analysis
- **Idempotent:** Running twice without new content won't produce duplicate ideas (processed log prevents it)
- **Incremental:** Each run only processes new sources since last run
- **Non-destructive:** Append-only output — never overwrites previous ideas

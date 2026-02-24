# Substack Note Ideas Generator — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create an orchestrator skill that scans published YouTube videos and Substack content via APIs, tracks processed sources, and generates batches of Substack Note ideas for later execution with `create-note`.

**Architecture:** Thin orchestrator (`substack:generate-note-ideas`) delegates ideation logic to `content-strategy:research` via a new reference file (`substack-notes-ideation.md`). Source tracking via a processed log file prevents redundant API calls across runs.

**Tech Stack:** Claude Code skills (SKILL.md), YouTube MCP tools, web fetch, markdown files

**Design doc:** `docs/plans/2026-02-23-substack-note-ideas-generator-design.md`

---

### Task 1: Create the Ideation Reference File

This reference file teaches `content-strategy:research` how to extract note-worthy angles from published content sources. It's the strategic brain of the skill.

**Files:**
- Create: `content-strategy/skills/research/references/substack-notes-ideation.md`

**Step 1: Study existing reference patterns**

Read these files to understand the reference file conventions:
- `content-strategy/skills/research/references/substack-notes-strategy.md` (companion strategy reference)
- `content-strategy/skills/research/references/youtube-community-strategy.md` (similar pattern for YouTube)
- `writing/skills/copywriting/references/substack-notes.md` (note types and templates)

**Step 2: Write the ideation reference file**

Create `content-strategy/skills/research/references/substack-notes-ideation.md` with these sections:

1. **Header** — State purpose: "Strategic frameworks for extracting Substack Note ideas from published content sources. Used by `content-strategy:research` when invoked by `substack:generate-note-ideas`."

2. **Angle Extraction Framework** — How to read a YouTube transcript, newsletter issue, or other content and identify note-worthy moments:
   - Surprising data points or counterintuitive findings
   - Quotable one-liners buried in longer content
   - Behind-the-scenes process details the audience hasn't seen
   - Unanswered questions or reader/viewer curiosities (from comments)
   - "Mini-lessons" that can stand alone in 2-5 sentences
   - Contrarian takes embedded in nuanced discussions
   - Specific numbers, results, or metrics that are shareable
   - Process steps that can be extracted as standalone tips

3. **Source-to-Type Mapping** — Table mapping content source types to the note types that naturally emerge from them:
   - YouTube transcript → Pattern Observation, Contrarian Statement, Problem→Solution, Single-Punch Wisdom
   - YouTube comments → Direct Advice (answering common questions), Contrarian Statement (correcting misconceptions)
   - Newsletter issue → Newsletter Teaser, Single-Punch Wisdom, List-Based Tactical
   - Past notes history → Gap analysis (which of the 10 types haven't been used recently)
   - Web trends → Pattern Observation, Direct Advice tied to timely topics, Build-in-Public tied to current tools/platforms

4. **Idea Quality Criteria** — Checklist for each generated idea:
   - Standalone value (interesting without watching the source video or reading the source issue)
   - Specificity (concrete numbers, examples, tools — not vague platitudes)
   - One idea per note (not multiple ideas crammed together)
   - Maps cleanly to one of the 10 note types from `writing:copywriting > substack-notes.md`
   - Not a rehash of something already posted in past notes
   - Has a clear engagement angle (something restackable, quotable, or discussion-worthy)

5. **Trending Topic Integration** — How to blend web/niche trends with the user's existing content:
   - Find trending topics in the user's niche via web search
   - Cross-reference with the user's published content to find unique angles
   - Prioritize trends the user has first-hand experience with
   - Avoid bandwagon takes — the note should add genuine insight, not just ride a trend

6. **Output Format** — Structure for each idea (the research skill should return ideas in this format):
   ```
   ### Idea N
   **Topic:** [Specific topic in 5-10 words]
   **Type:** [One of the 10 note types]
   **Source:** [YouTube — "Title" (video ID) | Newsletter — "Title" (URL) | Web trend — description]
   **Pitch:** [One sentence describing the note's core message]
   **Rationale:** [Why this idea is worth posting — engagement potential, gap it fills, timeliness]
   ```

7. **Volume Target** — Generate 5-10 ideas per run. Bias toward quality over quantity. If a source doesn't have strong note-worthy angles, skip it rather than forcing weak ideas.

**Step 3: Commit**

```bash
git add content-strategy/skills/research/references/substack-notes-ideation.md
git commit -m "feat(content-strategy): add substack notes ideation reference for research skill"
```

---

### Task 2: Create the Orchestrator Skill

The thin orchestrator that manages the workflow: load log, fetch published content, invoke research, present ideas, save output.

**Files:**
- Create: `substack/skills/generate-note-ideas/SKILL.md`

**Step 1: Study existing orchestrator patterns**

Read these files to understand orchestrator conventions:
- `substack/skills/create-note/SKILL.md` (closest sibling — Substack Notes orchestrator)
- `youtube/skills/create-post/SKILL.md` (similar pattern — YouTube community post orchestrator)
- `skill-factory/skills/create-skill/references/skill-template-orchestrator.md` (orchestrator template)

**Step 2: Write the orchestrator SKILL.md**

Create `substack/skills/generate-note-ideas/SKILL.md` following the orchestrator template. Key sections:

**Frontmatter:**
```yaml
---
name: generate-note-ideas
description: "Scan published YouTube videos, Substack newsletter issues, and Substack Notes to generate high-quality note ideas. This is a thin orchestrator — it sequences source scanning, content-strategy:research invocation, and output management, but delegates all ideation logic to the research skill via references/substack-notes-ideation.md."
---
```

**Overview:**
- State this is a thin orchestrator
- Explain it sits upstream of `create-note` — ideation vs execution
- Core principle: never generate ideas manually, always delegate to `content-strategy:research`

**When to Use:**
- Generating a batch of Substack Note ideas from published content
- Finding new note topics between newsletter issues
- Maintaining a consistent Notes posting cadence
- Mining existing content for repurposable note angles

**Workflow — Step 0: Load Processed Log**
- Read `./substack/notes/processed-log.md`
- If file doesn't exist, create it with the empty template (headers only, no rows)
- Parse the log to get lists of already-processed YouTube video IDs and newsletter issue URLs
- Also read `./substack/notes/ideas.md` if it exists (for duplicate prevention)

**Workflow — Step 1: Fetch Published YouTube Content**
- Use YouTube MCP tool `search_videos` to find recent videos from the user's channel
- Compare video IDs against processed log — identify new/unprocessed videos
- For each new video: use `get_video_details` for title, description, stats and `get_video_transcript` for full transcript
- Also use `get_video_comments` for top comments (source of audience questions and misconceptions)
- If no YouTube MCP tools available, fall back to web search for the user's YouTube channel

**Workflow — Step 2: Fetch Published Substack Content**
- Web fetch the user's Substack archive page (e.g., `https://{subdomain}.substack.com/archive`)
- Compare issue URLs against processed log — identify new/unprocessed issues
- For each new issue: web fetch the full issue content
- Also web fetch the user's Substack Notes feed for gap analysis and posted-notes history

**Workflow — Step 3: Fetch Web Trends**
- Use web search to find trending topics in the user's niche
- This always runs regardless of whether new sources exist
- Provides timely note ideas even when no new content has been published

**Workflow — Step 4: Invoke `content-strategy:research` with Ideation Reference**
- **MANDATORY**: Invoke `content-strategy:research` with reference `references/substack-notes-ideation.md`
- Pass all source material gathered in Steps 1-3:
  - New YouTube video transcripts, titles, descriptions, top comments
  - New newsletter issue content
  - Past Substack Notes (for gap analysis)
  - Web trend findings
  - Previously generated ideas from `ideas.md` (for duplicate prevention)
- Research skill applies the ideation framework and returns structured ideas

**Workflow — Step 5: Present Ideas to User**
- Present the batch of ideas (5-10) in the structured format from the ideation reference
- Each idea includes: topic, suggested note type, source, one-line pitch, strategic rationale
- User can approve the batch, remove specific ideas, or request more

**Workflow — Step 6: Save Output**
- Append approved ideas to `./substack/notes/ideas.md` under a `## Run: YYYY-MM-DD` header
- Update `./substack/notes/processed-log.md` with newly scanned sources:
  - Add rows for each new YouTube video (video ID, title, scan date, ideas generated count)
  - Add rows for each new newsletter issue (URL, title, scan date, ideas generated count)
  - Update the Substack Notes Scanned section with latest scan date and gap analysis
- Separate runs in `ideas.md` with `---` horizontal rule

**Workflow — Step 7: Handoff Suggestion**
- Inform user they can pick any idea and invoke `substack:create-note` to write the full note
- Do NOT automatically invoke `create-note`

**Output Structure sections:**

Ideas file template:
```markdown
# Substack Note Ideas

## Run: YYYY-MM-DD

### Idea 1
**Topic:** [topic]
**Type:** [note type]
**Source:** [source reference]
**Pitch:** [one-line pitch]
**Rationale:** [strategic rationale]

---

### Idea 2
...
```

Processed log template:
```markdown
# Processed Content Log

## YouTube Videos
| Video ID | Title | Scanned | Ideas Generated |
|----------|-------|---------|-----------------|

## Newsletter Issues
| URL | Title | Scanned | Ideas Generated |
|-----|-------|---------|-----------------|

## Substack Notes Scanned
| Last Scan Date | Notes Reviewed | Gap Analysis |
|----------------|----------------|-------------|
```

**Quality Checklist:**
- [ ] Processed log loaded (Step 0)
- [ ] YouTube videos scanned via MCP tools (Step 1)
- [ ] Substack newsletter issues scanned via web fetch (Step 2)
- [ ] Web trends gathered (Step 3)
- [ ] `content-strategy:research` invoked with `references/substack-notes-ideation.md` (Step 4)
- [ ] Ideas presented to user for approval (Step 5)
- [ ] Approved ideas saved to `./substack/notes/ideas.md` (Step 6)
- [ ] Processed log updated with newly scanned sources (Step 6)
- [ ] Handoff to `create-note` suggested (Step 7)

**Common Pitfalls:**
1. **Generating ideas manually** — All ideation logic lives in the research reference file. Delegate.
2. **Re-scanning processed sources** — Always check the processed log first. Skip sources already scanned.
3. **Ignoring the notes history** — Past notes feed gap analysis. Always load them.
4. **Skipping web trends** — Trending topics provide timely ideas even when no new content exists.
5. **Auto-invoking create-note** — This skill generates ideas only. The user decides when to write.
6. **Saving before user approval** — Always present ideas and get approval before writing to files.

**Step 3: Commit**

```bash
git add substack/skills/generate-note-ideas/SKILL.md
git commit -m "feat(substack): add generate-note-ideas orchestrator skill"
```

---

### Task 3: Update Plugin Manifests

Both the `substack` and `content-strategy` plugins need version bumps.

**Files:**
- Modify: `substack/.claude-plugin/plugin.json`
- Modify: `content-strategy/.claude-plugin/plugin.json`
- Modify: `substack/README.md`

**Step 1: Bump substack plugin version**

Edit `substack/.claude-plugin/plugin.json`:
- Change version from `"2.0.0"` to `"2.1.0"` (minor bump — new skill added)

**Step 2: Bump content-strategy plugin version**

Edit `content-strategy/.claude-plugin/plugin.json`:
- Change version from `"1.2.0"` to `"1.3.0"` (minor bump — new reference file added)

**Step 3: Update substack README**

Edit `substack/README.md`:
- Add a new row to the Skills table:
  ```
  | `generate-note-ideas` | Scan published content and generate batches of Substack Note ideas |
  ```

**Step 4: Commit**

```bash
git add substack/.claude-plugin/plugin.json content-strategy/.claude-plugin/plugin.json substack/README.md
git commit -m "chore: bump substack to 2.1.0 and content-strategy to 1.3.0 for note ideas generator"
```

---

### Task 4: Verify Skill Installation

**Step 1: Verify file structure**

Confirm all files exist at the correct paths:
```
content-strategy/skills/research/references/substack-notes-ideation.md
substack/skills/generate-note-ideas/SKILL.md
substack/.claude-plugin/plugin.json (version 2.1.0)
content-strategy/.claude-plugin/plugin.json (version 1.3.0)
substack/README.md (updated with new skill)
```

**Step 2: Verify SKILL.md is under 500 lines**

The orchestrator template rule limits SKILL.md to under 500 lines. Confirm the file meets this constraint.

**Step 3: Verify skill references are correct**

Check that all `plugin:skill` references in the orchestrator point to valid skills:
- `content-strategy:research` — exists at `content-strategy/skills/research/SKILL.md`
- `substack:create-note` — exists at `substack/skills/create-note/SKILL.md`

**Step 4: Verify reference file is discoverable**

Confirm `substack-notes-ideation.md` is in the same directory as other research references:
```
content-strategy/skills/research/references/
  research-frameworks.md
  substack-notes-strategy.md
  substack-notes-ideation.md  ← new
  youtube-community-strategy.md
```

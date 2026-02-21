# Substack Notes Enhancement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Elevate Substack Notes to a first-class content channel by renaming the newsletter plugin to substack, enhancing the notes reference with 10 psychologically-grounded types, and creating a dedicated `substack:create-note` orchestrator.

**Architecture:** Three coordinated changes: (1) rename `newsletter/` plugin to `substack/` with all cross-references updated, (2) replace `writing/skills/copywriting/references/substack-notes.md` with an enhanced 10-type version, (3) create `substack/skills/create-note/SKILL.md` thin orchestrator mirroring `youtube:create-post`, backed by a new `content-strategy/skills/research/references/substack-notes-strategy.md`.

**Tech Stack:** Markdown skill files, JSON plugin manifests. No code — all content is skill definitions and reference documents.

**Design Doc:** `docs/plans/2026-02-21-substack-notes-enhancement-design.md`

---

### Task 1: Rename newsletter/ directory to substack/

**Files:**
- Rename: `newsletter/` → `substack/`

**Step 1: Rename the directory**

```bash
mv newsletter substack
```

**Step 2: Verify the rename**

```bash
ls substack/skills/
```

Expected: `plan-issue/` and `optimize-issue/` directories present.

**Step 3: Commit**

```bash
git add -A
git commit -m "refactor: rename newsletter plugin to substack"
```

---

### Task 2: Update substack plugin.json

**Files:**
- Modify: `substack/.claude-plugin/plugin.json`

**Step 1: Update plugin.json**

Replace the full file with:

```json
{
  "name": "substack",
  "description": "A plugin for Substack content workflows — orchestrates research, writing, and design skills for newsletter issues and Substack Notes",
  "version": "2.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

**Step 2: Verify JSON is valid**

```bash
python3 -c "import json; json.load(open('substack/.claude-plugin/plugin.json'))"
```

Expected: No output (valid JSON).

**Step 3: Commit**

```bash
git add substack/.claude-plugin/plugin.json
git commit -m "refactor: update plugin.json for substack rename"
```

---

### Task 3: Update substack/README.md

**Files:**
- Modify: `substack/README.md`

**Step 1: Update README**

Update the README to reflect the new plugin name and add the create-note skill. Replace the full file:

```markdown
# Substack

A thin orchestrator plugin for Substack content workflows. This plugin does not contain implementation logic — it composes foundation skills from `content-strategy`, `writing`, and `visual-design` into Substack-specific production workflows.

## How It Works

The substack plugin sequences foundation skill invocations to produce complete newsletter issues and Substack Notes. Each step delegates to a specialized skill that handles the actual work:

- **Research**: `content-strategy:research` for topic and competitor analysis
- **Writing**: `writing:copywriting` for newsletter drafts, social promotion posts, and Substack Notes
- **Titles**: `content-strategy:title` for subject line generation
- **Hooks**: `content-strategy:hook` for opening paragraph options
- **Voice**: `writing:voice` (invoked automatically by the copywriting skill)
- **Visuals**: `visual-design:social-graphic` for optional header images

## Skills

### plan-issue

Orchestrates a complete newsletter issue plan from topic to publication-ready content. Takes a topic (or source material like a video transcript) and produces:

- Research summary and content angle
- Subject line options with preview text
- Opening hook options
- Full newsletter draft
- Social promotion posts (Twitter/X, LinkedIn, Substack Notes)
- Optional header image

**Example usage:**
```
Use the plan-issue skill to plan a newsletter about AI coding assistants
```

### optimize-issue

Orchestrates foundation skills to optimize an existing newsletter draft or write a full issue from an outline. Distinct from plan-issue — this skill starts from existing content rather than a topic.

- Assesses input type (outline vs. rough draft) and routes to the appropriate workflow
- Delegates drafting/optimization to `writing:copywriting`
- Generates subject line options via `content-strategy:title`
- Generates opening hook options via `content-strategy:hook`
- Runs a pre-publish checklist before finalizing
- Presents all options for user selection

**Example usage:**
```
Use the optimize-issue skill to polish my newsletter draft
```

### create-note

Orchestrates foundation skills to create standalone Substack Notes — short-form posts for engagement, authority-building, and audience growth. Mirrors the `youtube:create-post` pattern.

- Checks for recent newsletter issues to suggest context-aware note types
- Invokes `content-strategy:research` with Substack Notes strategy for type selection
- Delegates writing to `writing:copywriting` with the enhanced Substack Notes reference
- Quality checklist ensures every note follows its structural formula

**Example usage:**
```
Use the create-note skill to write a Substack Note about AI agents
```

## Plugin Structure

```
substack/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── README.md                # Plugin documentation
└── skills/
    ├── plan-issue/
    │   └── SKILL.md         # Orchestrator skill definition
    ├── optimize-issue/
    │   ├── SKILL.md         # Orchestrator skill definition
    │   └── references/
    │       └── pre-publish-checklist.md
    └── create-note/
        └── SKILL.md         # Orchestrator skill definition
```
```

**Step 2: Commit**

```bash
git add substack/README.md
git commit -m "docs: update README for substack plugin rename and create-note skill"
```

---

### Task 4: Update plan-issue and optimize-issue frontmatter

**Files:**
- Modify: `substack/skills/plan-issue/SKILL.md` (line 2)
- Modify: `substack/skills/optimize-issue/SKILL.md` (lines 2, 21)

**Step 1: Update plan-issue frontmatter**

In `substack/skills/plan-issue/SKILL.md`, change the frontmatter name:

```yaml
---
name: plan-issue
description: Orchestrate foundation skills to plan a complete newsletter issue including research, draft, subject line, opening hook, and social promotion posts. This is a thin orchestrator — it sequences skill invocations and manages the user review workflow.
---
```

No change needed — the `name: plan-issue` stays the same (it's the skill name within the plugin, not the plugin name). The plugin namespace comes from the directory.

**Step 2: Update optimize-issue self-reference**

In `substack/skills/optimize-issue/SKILL.md`, change line 21:

Old:
```
- Starting from a topic with no existing content (use `newsletter:plan-issue` instead)
```

New:
```
- Starting from a topic with no existing content (use `substack:plan-issue` instead)
```

**Step 3: Commit**

```bash
git add substack/skills/optimize-issue/SKILL.md
git commit -m "refactor: update newsletter: references to substack: in optimize-issue"
```

---

### Task 5: Update marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json` (lines 48-51)

**Step 1: Update the newsletter entry**

Change:

```json
{
  "name": "newsletter",
  "source": "./newsletter",
  "description": "A plugin for newsletter content workflows — orchestrates research, writing, and design skills for newsletter production"
}
```

To:

```json
{
  "name": "substack",
  "source": "./substack",
  "description": "A plugin for Substack content workflows — orchestrates research, writing, and design skills for newsletter issues and Substack Notes"
}
```

**Step 2: Verify JSON is valid**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
```

**Step 3: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "refactor: register substack plugin in marketplace manifest"
```

---

### Task 6: Update cross-references in youtube and visual-design plugins

**Files:**
- Modify: `youtube/skills/newsletter-to-video/SKILL.md`
- Modify: `visual-design/skills/newsletter-visuals/SKILL.md`

**Step 1: Read both files to find all `newsletter:` references**

Read both files and identify every occurrence of `newsletter:` that needs to become `substack:`.

**Step 2: Replace all `newsletter:` with `substack:` in both files**

In `youtube/skills/newsletter-to-video/SKILL.md`: replace all occurrences of `newsletter:` with `substack:`.

In `visual-design/skills/newsletter-visuals/SKILL.md`: replace all occurrences of `newsletter:` with `substack:`.

**Step 3: Commit**

```bash
git add youtube/skills/newsletter-to-video/SKILL.md visual-design/skills/newsletter-visuals/SKILL.md
git commit -m "refactor: update newsletter: to substack: in cross-plugin references"
```

---

### Task 7: Update skill-factory references

**Files:**
- Modify: `skill-factory/skills/create-skill/references/taxonomy.md` (line 42)
- Modify: `skill-factory/skills/create-skill/references/skill-template-orchestrator.md` (line 119)

**Step 1: Update taxonomy.md**

On line 42, change:

```
**Examples**: `youtube:plan-video`, `youtube:repurpose-video`, `newsletter:plan-issue`
```

To:

```
**Examples**: `youtube:plan-video`, `youtube:repurpose-video`, `substack:plan-issue`
```

**Step 2: Update skill-template-orchestrator.md**

On line 119, change:

```
- `newsletter:plan-issue` -- Sequences research, draft, subject line, hook, and social posts
```

To:

```
- `substack:plan-issue` -- Sequences research, draft, subject line, hook, and social posts
```

**Step 3: Commit**

```bash
git add skill-factory/skills/create-skill/references/taxonomy.md skill-factory/skills/create-skill/references/skill-template-orchestrator.md
git commit -m "refactor: update newsletter: to substack: in skill-factory references"
```

---

### Task 8: Create enhanced references/substack-notes.md

**Files:**
- Replace: `writing/skills/copywriting/references/substack-notes.md`

**Step 1: Read the current file and the external skill**

Read:
- `writing/skills/copywriting/references/substack-notes.md` (current — 112 lines)
- `temp/substack-note-skill.md` (external skill — source material)

**Step 2: Write the enhanced reference**

Replace `writing/skills/copywriting/references/substack-notes.md` with the enhanced version. The new file must include:

1. **Overview section** — What Substack Notes are, audience context (warmer than Twitter)
2. **10 note types** — Each with:
   - Name and description
   - Structural formula (step-by-step template using code blocks)
   - Psychology annotation (why it works)
   - Length guideline
3. **Goal-to-type mapping table** — Teaching, Authority, Connection, Quick Value, Transparency, Positioning → recommended types
4. **Length tiers** — Ultra-Short (1-2 sentences), Short (3-5, MOST COMMON default), Medium (6-10), Long (10+, RARE)
5. **Opening techniques** (5) — Bold Declarative, Personal Admission, Pattern Observation, Direct Address, Contrarian Hook
6. **Middle development techniques** (5) — Numbered Lists, Timeline Progression, Contrast/Comparison, Evidence Stacking, Cause→Effect Logic
7. **Closing techniques** (5) — Punchy Restatement, Actionable Implication, Open Loop, Quotable Wisdom, Encouraging Push
8. **Engagement hooks** — Preserved from current file (questions, agree/disagree, share requests, reply prompts)
9. **Cross-promotion patterns** — Preserved from current file (newsletter teaser, YouTube reference, guide/resource, thread expansion)
10. **Formatting rules** — Preserved from current file (minimal formatting, no hashtags, one link, fewer line breaks than LinkedIn)
11. **Posting cadence** — Preserved from current file (3-5/week, mix types)
12. **Anti-patterns with before/after examples** — 5 specific demonstrations (Vague Generalities, Humble-Bragging, Clickbait Without Payoff, Generic Advice, Corporate Voice)
13. **Concrete examples** — 5 complete generated notes (one per major type)
14. **Common mistakes** — Expanded from current file

**Critical constraints:**
- This is a REFERENCE FILE — structure and conventions only
- NO voice rules (voice is in `writing:voice`)
- NO workflow logic (workflow is in the orchestrator)
- NO skill invocations

**Step 3: Verify the file is under 500 lines**

The reference should be comprehensive but concise. Target ~350-400 lines.

**Step 4: Commit**

```bash
git add writing/skills/copywriting/references/substack-notes.md
git commit -m "feat: enhance substack-notes reference with 10 psychologically-grounded types"
```

---

### Task 9: Create substack-notes-strategy.md reference

**Files:**
- Create: `content-strategy/skills/research/references/substack-notes-strategy.md`

**Step 1: Read the pattern file**

Read `content-strategy/skills/research/references/youtube-community-strategy.md` (180 lines) to understand the strategy reference structure.

**Step 2: Write the strategy reference**

Create `content-strategy/skills/research/references/substack-notes-strategy.md` following the youtube-community-strategy.md pattern. Include:

1. **Header** — Purpose statement, companion reference callout (`writing:copywriting` > `substack-notes.md`)
2. **Newsletter Publishing Cycle** (mirrors "3-Phase Video Cycle"):
   - **Pre-newsletter** (1-2 days before issue) — Teaser notes, topic polls, behind-the-scenes
   - **Issue day** — Key takeaway note with link (NOT "new issue is up!")
   - **Post-newsletter** (2-5 days after) — Follow-up discussion, reader responses, deeper cuts
3. **Between-issues filler content** — Table with content type, example, strategic purpose (Pattern Observation, Quick tip, Personal update, Hot take, Build-in-public, Direct advice)
4. **Goal-to-type mapping** — Detailed mapping with rationale:
   - Teaching → List-Based Tactical or Problem → Solution
   - Building Authority → Pattern Observation or Income Proof Story
   - Connection → Vulnerable Personal Story or Philosophical Observation
   - Quick Value → Single-Punch Wisdom or Direct Advice
   - Transparency → Build-in-Public Update
   - Positioning → Contrarian Statement
5. **Substack Notes algorithm context** — How Notes distribute (different from YouTube):
   - Notes surface in the Notes feed and subscriber home
   - Engagement (restacks, replies) drives distribution
   - Restacks are the primary amplification mechanism
   - Consistent cadence matters more than individual note performance
6. **Posting cadence** — Optimal frequency, weekly mix table, timing strategies
7. **Cross-platform synergy** — How Notes feed into and from YouTube, Twitter, LinkedIn
8. **The 80/20 rule** — 80% standalone value, 20% promotional
9. **Measurement** — What to track (restacks, replies, subscriber growth, click-through on linked content)

**Step 3: Verify the file is under 200 lines**

Strategy references should be dense and actionable. Target ~150-180 lines.

**Step 4: Commit**

```bash
git add content-strategy/skills/research/references/substack-notes-strategy.md
git commit -m "feat: add substack notes strategy reference for content-strategy:research"
```

---

### Task 10: Create substack:create-note orchestrator

**Files:**
- Create: `substack/skills/create-note/SKILL.md`

**Step 1: Read the pattern file**

Read `youtube/skills/create-post/SKILL.md` (160 lines) to understand the orchestrator structure.

**Step 2: Write the orchestrator skill**

Create `substack/skills/create-note/SKILL.md` mirroring `youtube:create-post`. Must include:

**Frontmatter:**
```yaml
---
name: create-note
description: Create high-engagement Substack Notes for standalone audience engagement, authority-building, and newsletter promotion. This is a thin orchestrator — it sequences content-strategy:research and writing:copywriting invocations for Substack Note creation.
---
```

**Sections (mirror youtube:create-post structure):**

1. **Overview** — Thin orchestrator, strategy lives in `content-strategy:research` via `references/substack-notes-strategy.md`, templates live in `writing:copywriting` via `references/substack-notes.md`, this skill manages workflow sequence and user decisions only.

2. **When to Use** — Writing a standalone Substack Note, promoting a newsletter issue through Notes, building engagement between issues, sharing insights/hot takes/behind-the-scenes.

3. **Prerequisites** — Optional: recent newsletter issue at `./newsletter/issues/[issue_name]/`. Needed for issue-linked notes. Standalone notes don't require it.

4. **Workflow:**
   - **Step 0: Newsletter Context Check** — Check for recent issue directory. If exists: suggest note type (teaser, riff). If none: standalone mode.
   - **Step 1: Invoke `content-strategy:research`** — MANDATORY. With `references/substack-notes-strategy.md`. Provide: user's goal, topic, newsletter context. Output: ranked note types, strategic rationale.
   - **Step 2: Present Note Type Options** — Show ranked types with goal mapping. User selects. Default to Short (3-5 sentences) unless message demands more.
   - **Step 3: Invoke `writing:copywriting`** — MANDATORY. With `references/substack-notes.md`. Copywriting auto-invokes `writing:voice` and `branding-kit:brand-guidelines`.
   - **Step 4: Quality Checklist** (8 criteria, all must pass):
     - [ ] Follows structural formula for chosen type
     - [ ] Opens with strong hook (first line grabs attention)
     - [ ] Length matches type guideline
     - [ ] Ends with engagement hook (not formulaic)
     - [ ] Specific, not vague (numbers, examples, concrete details)
     - [ ] Standalone value (interesting without clicking any link)
     - [ ] NOT a generic link dump
     - [ ] Note type matches stated goal

5. **Output handling:**
   - If linked to newsletter issue → append to `./newsletter/issues/[issue_name]/notes.md`
   - If standalone → present inline

6. **Output format** — Markdown template for notes.md:
   ```markdown
   ## [Type] Note - [Date]
   **Type:** [Note type name]
   **Context:** [Standalone / Pre-newsletter / Post-newsletter / Between issues]
   **Goal:** [Engagement / Authority / Connection / Promotion / etc.]

   ### Note Content
   [Final note text]

   ### Notes
   - Suggested timing: [from research]
   - Engagement hook type: [question / agree-disagree / share / reply]
   ```

7. **Quality Checklist** (completion verification):
   - [ ] Newsletter context checked (Step 0)
   - [ ] `content-strategy:research` invoked with `references/substack-notes-strategy.md`
   - [ ] Note type options presented and user selection received
   - [ ] `writing:copywriting` invoked with `references/substack-notes.md`
   - [ ] Voice consistency maintained (handled by writing skill's `writing:voice` invocation)
   - [ ] All 8 quality criteria passed (Step 4)
   - [ ] Note presented to user for approval
   - [ ] Output saved or presented inline

8. **Common Pitfalls** — Mirror youtube:create-post's structure:
   - Writing templates inline (all templates in `references/substack-notes.md`)
   - Embedding strategy logic (all strategy in `references/substack-notes-strategy.md`)
   - Skipping foundation skill invocations
   - Ignoring newsletter context
   - Defaulting to "new issue out" link dumps
   - Skipping the quality checklist

**Step 3: Verify the file is under 200 lines**

Target ~150-170 lines, matching youtube:create-post's 160.

**Step 4: Commit**

```bash
git add substack/skills/create-note/SKILL.md
git commit -m "feat: add substack:create-note orchestrator skill"
```

---

### Task 11: Verify all cross-references and final check

**Files:**
- Read: All modified files

**Step 1: Search for any remaining `newsletter:` references in non-docs files**

```bash
grep -r "newsletter:" --include="*.md" --include="*.json" . | grep -v "docs/plans/" | grep -v "temp/"
```

Expected: Zero results (all references updated to `substack:`).

**Step 2: Verify plugin structure**

```bash
ls -R substack/
```

Expected:
```
substack/
├── .claude-plugin/plugin.json
├── README.md
└── skills/
    ├── plan-issue/SKILL.md
    ├── optimize-issue/SKILL.md + references/pre-publish-checklist.md
    └── create-note/SKILL.md
```

**Step 3: Verify marketplace.json has substack registered**

```bash
python3 -c "import json; m=json.load(open('.claude-plugin/marketplace.json')); print([p['name'] for p in m['plugins']])"
```

Expected: `substack` in the list, `newsletter` not in the list.

**Step 4: Verify new reference files exist**

```bash
ls content-strategy/skills/research/references/substack-notes-strategy.md
ls writing/skills/copywriting/references/substack-notes.md
```

Expected: Both files exist.

**Step 5: Final commit if any cleanup needed**

```bash
git status
```

If clean, done. If changes remain, commit with descriptive message.

---

### Task 12: Clean up temp file

**Files:**
- Delete: `temp/substack-note-skill.md`

**Step 1: Remove the temp file**

```bash
rm temp/substack-note-skill.md
```

**Step 2: Check if temp/ is empty and remove if so**

```bash
ls temp/ && rmdir temp/ 2>/dev/null || true
```

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove temp substack notes skill reference"
```

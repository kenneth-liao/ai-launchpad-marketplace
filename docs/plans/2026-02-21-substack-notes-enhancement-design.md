# Substack Notes Enhancement Design

## Summary

Elevate Substack Notes from a subordinate newsletter promotion tool to a first-class content channel. Three coordinated changes: rename the `newsletter` plugin to `substack`, enhance the Substack Notes reference with 10 psychologically-grounded note types, and create a `substack:create-note` thin orchestrator mirroring the `youtube:create-post` pattern.

## Motivation

Gap analysis against an external Substack Notes skill revealed:
- Our system has 4 generic note formats; proven patterns use 10 psychologically-grounded types
- No structural formulas, psychology annotations, or goal-to-type mapping
- No dedicated orchestrator — Notes only generated as newsletter promotion (Step 5 of `plan-issue`)
- YouTube community posts have strategic depth (`youtube:create-post`); Notes don't

The user uses Notes both as standalone content and newsletter promotion equally.

## Architecture

```
substack/ (renamed from newsletter/)
├── .claude-plugin/plugin.json
├── README.md
├── skills/
│   ├── plan-issue/SKILL.md          (namespace update only)
│   ├── optimize-issue/SKILL.md      (namespace update only)
│   └── create-note/                 (NEW)
│       └── SKILL.md                 (thin orchestrator)

content-strategy/
├── skills/research/references/
│   └── substack-notes-strategy.md   (NEW — strategy reference)

writing/
├── skills/copywriting/references/
│   └── substack-notes.md            (ENHANCED — 4→10 types)
```

## Change 1: Plugin Rename (newsletter → substack)

Rename the `newsletter/` directory to `substack/`. The newsletter IS Substack — references are already Substack-specific.

**What changes:**
- Directory: `newsletter/` → `substack/`
- Plugin name in `plugin.json`
- Frontmatter `name:` in `plan-issue` and `optimize-issue` SKILL.md files
- All cross-references in other plugins

**Downstream references to update:**
- `youtube/skills/newsletter-to-video/SKILL.md` — `newsletter:` → `substack:` invocations
- `visual-design/skills/newsletter-visuals/SKILL.md` — `newsletter:` → `substack:` references
- Marketplace manifest — register new namespace

**What stays the same:** All internal logic, references, and workflows.

## Change 2: Enhanced references/substack-notes.md

Replace the current reference (113 lines, 4 types) with a richer version.

### Note Types (10, up from 4)

| # | Type | Length | Psychology | Maps From Current |
|---|------|--------|-----------|-------------------|
| 1 | Single-Punch Wisdom | 1-2 sentences | Screenshot-worthy, shareable | New |
| 2 | Income Proof Story | 3-7 sentences | Credibility through transparency | New |
| 3 | Pattern Observation | 3-8 sentences | Authority through observation | New |
| 4 | Contrarian Statement | 2-6 sentences | Cognitive dissonance, memorable | ~Hot Take |
| 5 | Problem → Solution | 3-6 sentences | "Aha moments" | New |
| 6 | Build-in-Public Update | 3-8 sentences | Trust through transparency | ~Behind-the-Scenes |
| 7 | List-Based Tactical | 4-12 sentences | High perceived value, scannable | New |
| 8 | Vulnerable Personal Story | 4-10 sentences | Deep connection | New |
| 9 | Newsletter Teaser | 2-5 sentences | Drive reads with standalone value | ~Teaser Note |
| 10 | Direct Advice | 2-5 sentences | Clear guidance, removes ambiguity | ~Simple Note |

### New Sections

- **Structural formula** for each type (step-by-step template)
- **Psychology annotation** per type (why it works)
- **Goal-to-type mapping** (Teaching → List-Based, Authority → Pattern Observation, etc.)
- **Anti-patterns with before/after examples** (5 demonstrations)
- **Concrete examples** (5 complete notes)
- **Length tiers** (Ultra-Short / Short / Medium / Long with defaults)

### Preserved Sections

- Engagement hooks
- Cross-promotion patterns
- Formatting rules (no hashtags, minimal formatting, one link per note)
- Posting cadence guidelines
- Common mistakes (expanded with before/after examples)

### Architectural Constraint

This remains a **reference file** — structure and conventions only. No voice rules, no workflow logic, no skill invocations. Voice stays in `writing:voice`.

## Change 3: New substack:create-note Orchestrator

Thin orchestrator mirroring `youtube:create-post`. Sequences foundation skills and manages user decisions.

### Workflow

```
Step 0: Context Check
  └─ Check for recent newsletter issue at ./newsletter/issues/
  └─ If exists → suggest note type (teaser, riff on the topic)
  └─ If none → standalone mode (any note type)

Step 1: Invoke content-strategy:research
  └─ With references/substack-notes-strategy.md
  └─ Input: user's goal, topic, context
  └─ Output: recommended note types ranked, strategic rationale

Step 2: Present Note Type Options
  └─ Show ranked types from research with goal mapping
  └─ User selects type (or accepts recommendation)

Step 3: Invoke writing:copywriting
  └─ With enhanced references/substack-notes.md
  └─ Copywriting auto-invokes writing:voice
  └─ Copywriting auto-invokes branding-kit:brand-guidelines

Step 4: Quality Checklist (all must pass)
  └─ [ ] Follows structural formula for chosen type
  └─ [ ] Opens with strong hook (first line grabs attention)
  └─ [ ] Length matches type guideline
  └─ [ ] Ends with engagement hook (not formulaic)
  └─ [ ] Specific, not vague (numbers, examples, concrete details)
  └─ [ ] Standalone value (interesting without clicking any link)
  └─ [ ] NOT a generic link dump
  └─ [ ] Note type matches stated goal
```

### New Reference: substack-notes-strategy.md

Lives in `content-strategy/skills/research/references/`. Covers:
- Goal-to-note-type mapping (Teaching, Authority, Connection, Quick Value, Transparency, Positioning)
- Cadence strategy (3-5/week, mix types, align with newsletter schedule)
- Posting timing recommendations
- Content lifecycle awareness (pre-newsletter, post-newsletter, between issues)

### Output Handling

- If linked to a newsletter issue → append to `./newsletter/issues/[issue_name]/notes.md`
- If standalone → present inline

### Key Difference from youtube:create-post

No lifecycle phases (pre-release/launch/post-launch). Instead: newsletter publishing cadence awareness — whether a note should tease an upcoming issue, riff on a recent issue, or stand alone.

## Complete File Map

### New Files (3)

| File | Plugin | Type |
|------|--------|------|
| `substack/skills/create-note/SKILL.md` | substack | Orchestrator skill |
| `content-strategy/skills/research/references/substack-notes-strategy.md` | content-strategy | Reference |
| `writing/skills/copywriting/references/substack-notes.md` | writing | Reference (replacement) |

### Renamed (1 plugin)

| From | To |
|------|-----|
| `newsletter/` | `substack/` |

### Modified Files

| File | Change |
|------|--------|
| `substack/.claude-plugin/plugin.json` | Rename + version bump |
| `substack/skills/plan-issue/SKILL.md` | Update frontmatter name |
| `substack/skills/optimize-issue/SKILL.md` | Update frontmatter name |
| `youtube/skills/newsletter-to-video/SKILL.md` | `newsletter:` → `substack:` references |
| `visual-design/skills/newsletter-visuals/SKILL.md` | `newsletter:` → `substack:` references |
| Marketplace manifest | Register `create-note` skill |

### Unchanged

- `writing:copywriting` workflow
- `writing:voice`
- `content-strategy:title`, `content-strategy:hook`, `content-strategy:research`
- Internal logic of `plan-issue` and `optimize-issue`

## Design Decisions

1. **Notes stay in substack plugin, not writing plugin** — Notes are part of the Substack ecosystem, not a generic writing task. The orchestrator belongs with `plan-issue` and `optimize-issue`.

2. **Strategy reference in content-strategy, not substack** — Follows the pattern of `youtube-community-strategy.md` living in `content-strategy`. Strategy knowledge is reusable across orchestrators.

3. **Enhanced reference replaces current, not supplements** — One file per content type in `writing:copywriting`. The enhanced version is a superset of the current file.

4. **10 note types, not fewer** — The external skill's types are psychologically distinct and map to different user goals. Merging them would lose the goal-to-type mapping that makes the system useful.

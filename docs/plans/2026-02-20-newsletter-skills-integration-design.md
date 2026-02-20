# Integration Design: Newsletter Skills (3) -> Marketplace

## Summary

Three skills from `temp/` are being integrated into the AI Launchpad Marketplace. One (`newsletter-to-youtube`) is already integrated as `youtube:newsletter-to-video` and only needs cleanup. The other two decompose into: a new task skill in `visual-design/` for newsletter visual assets, a new orchestrator in `newsletter/` for draft optimization, and enriched reference files across three foundation plugins (`writing`, `content-strategy/title`, `content-strategy/hook`).

## Source Inventory

```
Source: temp/
Files found:
- temp/newsletter-to-youtube/SKILL.md: Newsletter-to-YouTube video outline repurposing (ALREADY INTEGRATED)
- temp/newsletter-visual-assets/SKILL.md: Visual asset audit, scoring, and generation for newsletters
- temp/optimize-newsletter-issue/SKILL.md: Newsletter writing/optimization from outline or draft
```

## Architecture

```
temp/newsletter-to-youtube ─────> youtube:newsletter-to-video (ALREADY EXISTS, cleanup only)

temp/newsletter-visual-assets ──> visual-design:newsletter-visuals (NEW task skill)
                                    ├── Delegates to art:nanobanana (generation)
                                    ├── References branding-kit:design-system (brand)
                                    └── references/substack-constraints.md (NEW)

temp/optimize-newsletter-issue ──> newsletter:optimize-issue (NEW orchestrator)
                                    ├── Delegates to writing:copywriting (drafting)
                                    ├── Delegates to content-strategy:title (subject lines)
                                    ├── Delegates to content-strategy:hook (opening hooks)
                                    ├── Delegates to writing:voice (voice)
                                    └── references/pre-publish-checklist.md (NEW)

                                   writing/copywriting references/newsletter.md (EXTEND)
                                    └── Section rules, copywriting techniques, formatting,
                                        issue types, the newsletter arc

                                   content-strategy/title references/newsletter-subject-lines.md (EXTEND)
                                    └── Additional formulas, stranger test, Substack dual-purpose

                                   content-strategy/hook references/newsletter-hooks.md (EXTEND)
                                    └── 5 additional hook techniques
```

## Content Split

### 1. Cleanup: `temp/newsletter-to-youtube/`
Already integrated as `youtube/skills/newsletter-to-video/SKILL.md`. The existing version:
- Uses modern `content-strategy:hook` syntax (source used legacy `yt-content-strategist:youtube-video-hook`)
- Includes brand compliance hook and quality checklist
- Content is functionally identical

**Action**: Delete temp file only. No new files needed.

### 2. Task Skill: `visual-design/skills/newsletter-visuals/SKILL.md`
The core visual audit, scoring, and generation workflow. This is a task skill — it does one thing well (assess and generate visual assets for newsletter content). It belongs in `visual-design/` alongside `thumbnail` and `social-graphic`.

**Content from source**:
- Phase 1 audit methodology (complexity, engagement risk, persuasion opportunity)
- Phase 2 scoring framework (clarity lift, engagement lift, uniqueness — 1-5 each)
- Hard rules (score 10+ threshold, max 5 visuals, spacing rules)
- Visual type selection matrix
- Phase 3 brief presentation workflow
- Phase 4 generation rules (design system integration, prompt construction)
- Phase 5 caption and alt text guidelines
- Common mistakes and red flags

**Composition hooks**: Delegates to `art:nanobanana` for generation, references `branding-kit:design-system` for brand compliance.

### 3. Reference: `visual-design/skills/newsletter-visuals/references/substack-constraints.md`
Substack-specific rendering constraints extracted from the source skill. Keeps the task skill focused on the general visual audit methodology while platform specifics live in a reference.

**Content from source**:
- Aspect ratio and resolution table (hero, inline, comparison, square)
- Email rendering constraints (600px width, light backgrounds, text size)
- Output directory conventions (`episode_files/`)

### 4. Orchestrator: `newsletter/skills/optimize-issue/SKILL.md`
Thin orchestrator for polishing existing newsletter drafts or writing from outlines. Distinct from `newsletter:plan-issue` which starts from research/topic — this skill assumes content already exists and focuses on writing quality.

**Content from source (workflow only)**:
- From-outline workflow: determine type → invoke writing → generate subject lines → checklist
- From-draft workflow: audit sections → optimize → generate subject lines → checklist
- Delegation to foundation skills: `writing:copywriting`, `content-strategy:title`, `content-strategy:hook`, `writing:voice`

**All content generation knowledge (section rules, copywriting techniques, etc.) goes to reference files, NOT the orchestrator.**

### 5. Reference: `newsletter/skills/optimize-issue/references/pre-publish-checklist.md`
The pre-publish checklist extracted from the source. Used by the orchestrator as its final verification step.

**Content from source**:
- Subject line & preview checks
- Opening checks
- Body checks
- Close checks
- Quality checks

### 6. Extend: `writing/skills/copywriting/references/newsletter.md`
Enrich the existing newsletter reference with substantial new content from the source skill. The existing file covers basic structure; the source adds detailed section-level guidance.

**New content to add**:
- The Newsletter Arc framework (Hook → Context → Value → Close with per-stage purpose)
- Detailed section rules: preview text, context/setup, core content structures, close patterns, P.S. line, CTA rules
- Issue types with detailed guidance (Weekly Tip, Deep Dive, Case Study, Template Drop)
- Copywriting techniques (8th-grade reading level, one idea per sentence, cut filler words, active voice, "so what?" test, bucket brigade phrases, specificity principle)
- Formatting for scannability (F-pattern, bold strategies, paragraph rhythm)
- Body writing rules (one idea per paragraph, 1-3 sentence paragraphs, subheadings every 150-300 words, inverted pyramid, concrete over abstract, show don't tell, acknowledge trade-offs)

### 7. Extend: `content-strategy/skills/title/references/newsletter-subject-lines.md`
Add formulas and rules from the source that complement existing content.

**New content to add**:
- 6 named formulas (specific benefit, curiosity question, the exact thing, number + outcome, counterintuitive claim, problem they feel) with examples
- The "stranger test" concept
- Substack dual-purpose note (email subject AND web headline/SEO)
- "Always generate 3 options" instruction with recommendation

### 8. Extend: `content-strategy/skills/hook/references/newsletter-hooks.md`
Add hook techniques from the source that complement existing patterns.

**New content to add**:
- 5 additional hook techniques: Relatable Problem, Question, "What Everyone Misses" (double-hook), Timestamp/Scene-Setting, Surprising Number, The Stakes
- The existing file has 5 patterns; the source adds 10 with overlap on ~5. Net new: ~5 techniques.
- "Rotate across issues for variety" instruction

## Files to Create/Modify

| Action | File | Purpose |
|--------|------|---------|
| Create | `visual-design/skills/newsletter-visuals/SKILL.md` | Task skill for newsletter visual audit and generation |
| Create | `visual-design/skills/newsletter-visuals/references/substack-constraints.md` | Substack-specific rendering constraints |
| Create | `newsletter/skills/optimize-issue/SKILL.md` | Thin orchestrator for draft optimization |
| Create | `newsletter/skills/optimize-issue/references/pre-publish-checklist.md` | Pre-publish verification checklist |
| Update | `writing/skills/copywriting/references/newsletter.md` | Enrich with section rules, copywriting techniques, issue types |
| Update | `content-strategy/skills/title/references/newsletter-subject-lines.md` | Add formulas, stranger test, Substack dual-purpose |
| Update | `content-strategy/skills/hook/references/newsletter-hooks.md` | Add 5 additional hook techniques |
| Update | `visual-design/.claude-plugin/plugin.json` | Bump version for new skill |
| Update | `visual-design/README.md` | Document new newsletter-visuals skill |
| Update | `newsletter/.claude-plugin/plugin.json` | Bump version for new skill |
| Update | `newsletter/README.md` | Document new optimize-issue skill |
| Update | `writing/.claude-plugin/plugin.json` | Bump version for enriched references |
| Update | `content-strategy/.claude-plugin/plugin.json` | Bump version for enriched references |
| Delete | `temp/newsletter-to-youtube/` | Already integrated as youtube:newsletter-to-video |
| Delete | `temp/newsletter-visual-assets/` | Replaced by visual-design:newsletter-visuals |
| Delete | `temp/optimize-newsletter-issue/` | Replaced by newsletter:optimize-issue + references |

## Functionality Preservation

| Original Capability | Destination | Notes |
|---------------------|-------------|-------|
| Newsletter-to-YouTube repurposing workflow | `youtube:newsletter-to-video` (existing) | Already integrated, no changes |
| Legacy `yt-content-strategist:youtube-video-hook` reference | `content-strategy:hook` (existing) | Already modernized |
| Visual audit methodology (complexity, engagement, persuasion) | `visual-design:newsletter-visuals` | Full audit framework preserved |
| Visual scoring framework (clarity/engagement/uniqueness) | `visual-design:newsletter-visuals` | Scoring matrix and hard rules preserved |
| Visual type selection matrix | `visual-design:newsletter-visuals` | All 5 types preserved |
| Visual brief approval workflow | `visual-design:newsletter-visuals` | Approval gate preserved |
| Design system integration for visuals | `visual-design:newsletter-visuals` | Delegates to `branding-kit:design-system` |
| Art generation delegation | `visual-design:newsletter-visuals` | Delegates to `art:nanobanana` |
| Substack rendering constraints | `visual-design:newsletter-visuals/references/substack-constraints.md` | Extracted to reference |
| Caption and alt text generation | `visual-design:newsletter-visuals` | Preserved in skill |
| From-outline newsletter workflow | `newsletter:optimize-issue` | Orchestrator delegates to foundation skills |
| From-draft optimization workflow | `newsletter:optimize-issue` | Orchestrator delegates to foundation skills |
| Newsletter Arc framework | `writing/copywriting/references/newsletter.md` | Added to existing reference |
| Subject line formulas (6 named patterns) | `content-strategy/title/references/newsletter-subject-lines.md` | Extends existing formulas |
| Subject line rules (stranger test, <50 chars) | `content-strategy/title/references/newsletter-subject-lines.md` | Extends existing rules |
| Preview text rules | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Opening hook techniques (10 patterns) | `content-strategy/hook/references/newsletter-hooks.md` | ~5 new techniques added |
| Context/setup writing pattern | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Core content structures | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Close patterns | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| P.S. line rules | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| CTA rules (types, placement, copy) | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Issue types (Weekly Tip, Deep Dive, etc.) | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Copywriting techniques (7 rules) | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Formatting for scannability | `writing/copywriting/references/newsletter.md` | New section in existing reference |
| Pre-publish checklist | `newsletter/optimize-issue/references/pre-publish-checklist.md` | Extracted to reference |
| `kenny-writing-voice` delegation | `writing:voice` via orchestrator | Modern syntax: `writing:voice` |

## Design Decisions

1. **`newsletter-to-youtube` is cleanup-only**: The existing `youtube:newsletter-to-video` already covers this skill with modern syntax and framework compliance. No new work needed — just delete the temp source.

2. **`newsletter-visual-assets` stays as one task skill**: The source is already well-structured as a single-purpose task skill. It doesn't need further splitting — the visual audit, scoring, and generation are tightly coupled steps of one workflow. Platform-specific constraints (Substack) are extracted to a reference file for future extensibility.

3. **`newsletter-visual-assets` goes in `visual-design/`**: Although newsletter-specific, the core methodology (visual audit + scoring + generation) is a visual design task. This follows the pattern where `visual-design:thumbnail` and `visual-design:social-graphic` are also platform-aware but live in the visual-design foundation plugin.

4. **`optimize-newsletter-issue` decomposes into 1 orchestrator + 4 reference enrichments**: The source skill bundles workflow logic with extensive writing knowledge. The workflow becomes a thin orchestrator in `newsletter/`. The knowledge (section rules, copywriting techniques, formulas, hooks, checklist) enriches existing foundation references, making it available to any skill that loads those references.

5. **`newsletter:optimize-issue` is distinct from `newsletter:plan-issue`**: `plan-issue` starts from a topic/research and produces a full plan. `optimize-issue` starts from an existing outline or draft and focuses on writing quality and polish. Different entry points, complementary orchestrators.

6. **Reference enrichment over new reference files**: Where existing references partially cover the same topic (newsletter subject lines, newsletter hooks, newsletter structure), the new content extends those files rather than creating parallel references. This prevents duplication and ensures `writing:copywriting` doesn't need to know about two different newsletter reference files.

7. **Pre-publish checklist gets its own reference**: It's unique to the optimize workflow and doesn't fit naturally into any existing foundation reference. It lives alongside the orchestrator that uses it.

## Patterns Followed

- **Taxonomy decision tree**: Each piece classified as Knowledge, Personality, Task, Orchestrator, or Meta
- **Split rule**: The monolithic `optimize-newsletter-issue` is split into orchestrator + references
- **Thin orchestrator pattern**: `newsletter:optimize-issue` delegates to foundation skills, generates nothing
- **Foundation reference pattern**: Knowledge content enriches existing foundation plugin references
- **Composition hooks**: Task skill includes voice and brand hooks; orchestrator uses `plugin:skill` syntax
- **Reference extraction**: Platform-specific constraints separated from general methodology
- **Modern syntax**: All `plugin:skill` invocations use current syntax

---
name: brand-guidelines
description: Use when users want to define, codify, or update their brand identity and connect it to design systems. Produces a self-contained user-level skill at ~/.claude/skills/{brand-slug}/SKILL.md that enforces brand guidelines whenever visual assets or written content are created.
---

# Brand Guidelines Generator

Create a self-contained brand guidelines skill through guided discovery. The generated skill lives at the user level and enforces brand identity across all future Claude Code sessions.

## Workflow Overview

Execute these phases in strict order. Phase 0 is optional (skip if the user has no existing assets to share). Never skip Phases 1-4. Each phase builds on the previous.

| Phase | Name | Action | Output |
|-------|------|--------|--------|
| 0 | Context Ingestion | Collect + analyze existing business assets | Extracted brand signals + smart defaults for discovery |
| 1 | Brand Discovery | Interactive questionnaire across 6 dimensions | User preferences for brand identity |
| 2 | Synthesis & Preview | Format and present brand summary | User-confirmed brand identity spec |
| 3 | Skill Generation | Generate user-level SKILL.md from template | `~/.claude/skills/{brand-slug}/SKILL.md` |
| 4 | Optional DS Creation | Create design systems for unmapped asset types | Updated mapping table in brand skill |

---

## Phase 0: Context Ingestion (Optional)

Before starting discovery, ask the user if they have existing business assets to share. Existing context dramatically reduces the number of questions needed — the skill extracts what it can and only asks about what's missing or ambiguous.

**Opening prompt:** "Before we start defining your brand, do you have any existing assets I can learn from? These could be your website, newsletter archives, social media profiles, pitch decks, brand documents, images, or anything that represents your brand today. This is optional — we can build entirely from scratch too."

**Supported input types:**

| Input Type | How to Provide | What to Extract |
|------------|---------------|-----------------|
| Website URL | User provides a URL like `https://mybrand.com` | Use WebFetch to capture the page. Extract: brand name, tagline (from hero/header), mission/about copy, value proposition, tone signals from copywriting style, target audience signals, content categories (→ asset types). Follow internal links to About, Mission, and similar pages if present. |
| Newsletter / blog posts | User provides URLs, files, or pastes content | Analyze writing style for voice and tone signals. Extract: recurring topics (→ value prop), how the author addresses readers (→ audience), vocabulary level (→ tone modifiers), sentence structure patterns. |
| Documents | User provides file paths (PDF, MD, TXT, DOCX) | Read and analyze. Could be pitch decks, brand guides, one-pagers, course outlines, etc. Extract any brand identity data present. |
| Images / logos | User provides file paths or pastes images | Read images visually. Extract: brand name from wordmarks, color palette signals, visual style/mood, existing design system hints. |
| Social media profiles | User provides profile URLs | Use WebFetch to capture. Extract: bio (→ tagline/mission), content themes, posting style (→ voice), follower description (→ audience), platform mix (→ asset types). |
| Existing brand skill | User points to a previous SKILL.md | Read it as a starting point for updates. Pre-fill all dimensions from existing data. |
| Skip | User has no assets to share | Proceed directly to Phase 1 with no smart defaults. |

**Analysis protocol:**

For each provided asset, extract and categorize signals into the 6 discovery dimensions:

| Dimension | What to Look For |
|-----------|-----------------|
| 1. Brand name & tagline | Literal brand name, slogans, header text, social bios |
| 2. Mission & value prop | About pages, mission statements, "what we do" sections, pitch deck opening slides |
| 3. Voice & tone traits | Copywriting style — formal vs. casual, assertive vs. supportive, humorous vs. serious |
| 4. Tone modifiers | Sentence length patterns, vocabulary level, use of jargon, narrative vs. direct style |
| 5. Target audiences | Who the content addresses ("you" references), testimonials, case studies, subscriber descriptions |
| 6. Asset types | What visual content exists (thumbnails, social posts, headers, slides, etc.) |

**After analysis, present a summary:**

> "Here's what I extracted from your assets:
>
> - **Brand name:** {name} | **Tagline:** {tagline or "none found"}
> - **Mission signals:** {1-2 sentence summary of what the brand appears to be about}
> - **Voice signals:** {detected traits, e.g., "Reads as friendly and expert — conversational but backs up claims"}
> - **Tone signals:** {detected modifiers, e.g., "Short punchy sentences, casual vocabulary, avoids jargon"}
> - **Audience signals:** {who the content seems to target}
> - **Asset types spotted:** {list of visual content types found}
>
> I'll use these as starting points during discovery. You'll have full control to confirm, adjust, or override everything."

Store the complete analysis as `context_analysis` with per-dimension confidence levels:
- **High confidence** — clear, unambiguous signal (e.g., brand name from a logo, explicit mission statement)
- **Medium confidence** — strong signal but inferred (e.g., voice traits from writing style analysis)
- **Low confidence** — weak or mixed signals (e.g., audience guessed from content topics)

---

## Phase 1: Brand Discovery

Guide the user through structured questions to define their brand identity. Use the AskUserQuestion tool to present options. Ask questions **one dimension at a time** to keep the conversation focused.

Load the full question bank from [references/discovery-framework.md](references/discovery-framework.md).

**Rules:**
- Ask dimensions in order (they build on each other)
- One dimension per AskUserQuestion call — do not batch across dimensions
- **If Phase 0 produced smart defaults**, adapt each dimension based on confidence level (see Smart Default Behavior below)
- For open-ended dimensions, use AskUserQuestion with broad options that prompt elaboration
- For multi-choice dimensions, present all options with descriptions and enable `multiSelect`
- After each answer, give a brief 1-sentence acknowledgment contextualizing the choice, then move to the next dimension
- Complete ALL 6 dimensions before moving to Phase 2
- If the user wants to go back and change a previous answer, allow it

**Smart Default Behavior (when Phase 0 data exists):**

| Confidence | Behavior |
|------------|----------|
| High | Present the extracted value and ask for confirmation: *"From your website, I found your brand name is **{name}** with tagline **{tagline}**. Sound right, or want to change it?"* Use AskUserQuestion with the extracted value as the first option and "I want to change this" as the second. |
| Medium | Present the extracted value as a suggested default: *"Based on your writing style, I'd suggest **Friendly & approachable** + **Expert & authoritative** — your content is conversational but backs up claims with evidence. Does this match your intent?"* Still present all options with the suggestion pre-noted. |
| Low | Present all options normally but note what was observed: *"Your content seems to target developers, but I wasn't sure — who is your primary audience?"* |
| No signal | Ask the full question as defined in the discovery framework with no pre-selection. |

**Dimensions (in order):**
1. Brand name & tagline
2. Mission & value proposition
3. Voice & tone traits
4. Tone modifiers
5. Target audiences
6. Asset types & design system mapping

**Dimension 6 — Special handling:**

Before presenting asset type options, scan `~/.claude/.context/design-systems/` to discover available design systems. For each directory found, read the design system markdown file to extract the style name.

After the user selects their asset types, ask a follow-up for **each selected asset type**: which design system should be used? Present three options per asset type:
- Each discovered design system (by style name)
- "Create new design system" — flags this type for Phase 4
- "Decide later" — leaves the mapping empty for now

Store the complete mapping as `asset_ds_mapping`.

---

## Phase 2: Synthesis & Preview

After all 6 dimensions are answered, synthesize into a formatted brand summary and present for confirmation.

**Steps:**
1. Derive the **brand slug** from the brand name: lowercase, spaces and special characters replaced by hyphens (e.g., "AI Launchpad Newsletter" → `ai-launchpad-newsletter`)
2. Synthesize voice traits + tone modifiers into 3-4 **voice application rules** — concrete, actionable guidelines for how this brand should sound
3. Derive **brand anti-patterns** from the inverse of chosen voice traits (see mapping in template reference)
4. Build **audience profiles** — for each audience segment, infer goals, frustrations, what resonates, and preferred platforms based on the user's description
5. Format the complete brand summary:

Present to the user:

```
## Brand Summary: {brand_name}

**Tagline:** {tagline}
**Mission:** {mission}
**Value Prop:** {value_prop}

**Voice Traits:** {trait_1}, {trait_2}
**Tone Modifiers:** {modifier_1}, {modifier_2}

**Voice Application Rules:**
- {rule_1}
- {rule_2}
- {rule_3}

**Audiences:**
- Primary: {primary_audience}
- Secondary: {secondary_audience}

**Asset Type → Design System Mapping:**
| Asset Type | Design System |
|------------|---------------|
| {type_1} | {ds_1 or "Create new" or "Decide later"} |
| ... | ... |

**Anti-Patterns (things this brand should NEVER do):**
- {anti_pattern_1}
- {anti_pattern_2}
- ...
```

6. Ask the user: "Does this brand summary look right? Want to change anything before I generate the skill?"
7. If the user wants changes, update the relevant fields and re-present
8. Once confirmed, proceed to Phase 3

---

## Phase 3: Skill Generation

Generate the brand guidelines skill at `~/.claude/skills/{brand-slug}/SKILL.md`.

**Steps:**
1. Load the template from [references/brand-skill-template.md](references/brand-skill-template.md)
2. Fill every `{{placeholder}}` with the confirmed brand data from Phase 2
3. Ensure the generated skill is **fully self-contained** — all brand data embedded directly, no references to external config files
4. Create the directory `~/.claude/skills/{brand-slug}/` if it doesn't exist
5. Write the generated SKILL.md to `~/.claude/skills/{brand-slug}/SKILL.md`
6. **Verify the generated skill** — read the file back and check:
   - No unfilled `{{placeholder}}` markers remain
   - All 6 sections are present (Brand Identity, Voice & Tone, Target Audiences, Design System Resolution, How To Apply, Brand Anti-Patterns)
   - The asset type mapping table has the correct number of rows
   - If any issues found, fix and re-write before proceeding
7. Inform the user:
   > "Your brand guidelines skill has been created at `~/.claude/skills/{brand-slug}/SKILL.md`. **Restart Claude Code** to activate it — user-level skills are loaded at startup."

---

## Phase 4: Optional DS Creation

If any asset types in `asset_ds_mapping` were mapped to "Create new design system", offer to create them now.

**Steps:**
1. List all asset types mapped to "Create new"
2. Ask the user: "You flagged {N} asset type(s) for new design systems: {list}. Want to create them now, or come back later?"
3. If the user wants to create now:
   a. For each asset type, invoke the **branding-kit:design-system** skill (suggest "user level" as the output location so it's available system-wide)
   b. After each design system is created, update the brand skill's mapping table:
      - Read `~/.claude/skills/{brand-slug}/SKILL.md`
      - Replace the "Create new" entry for that asset type with the new design system's style name and path
      - Write the updated file
4. If the user wants to come back later, remind them they can update the mapping manually or re-invoke this skill in "update" mode

---

## Updating an Existing Brand Skill

If the user already has a brand skill (detected by checking `~/.claude/skills/` for existing brand directories), offer an abbreviated update flow.

**Update workflow:**
1. List discovered brand skills from `~/.claude/skills/*/SKILL.md`
2. Ask the user which brand to update
3. Read the existing brand skill
4. Ask which dimensions to update (multi-select from the 6 dimensions)
5. Run only the selected dimensions from Phase 1
6. Re-synthesize only the affected sections
7. Update the existing SKILL.md (preserve unchanged sections)
8. Inform the user to restart Claude Code

---

## Error Handling

- If `~/.claude/.context/design-systems/` does not exist or is empty during Dimension 6, inform the user no design systems are available yet and offer "Create new" or "Decide later" as the only options
- If `~/.claude/skills/{brand-slug}/SKILL.md` already exists, ask the user whether to overwrite or choose a different slug
- If the brand name produces an empty or invalid slug, ask the user to provide a custom slug
- If the user's voice trait + modifier combination creates a contradictory voice (e.g., "Bold & provocative" + "Casual vocabulary" for a financial services brand), flag the tension during synthesis and ask which direction to prioritize

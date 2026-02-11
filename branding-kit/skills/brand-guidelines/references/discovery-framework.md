# Brand Discovery Framework

Full question bank for the 6 brand identity dimensions. Each dimension includes exact question text, input type, options, follow-up prompts, impact notes, and smart-default behavior when Phase 0 context is available.

## Contents

- Dimension 1: Brand Name & Tagline
- Dimension 2: Mission & Value Proposition
- Dimension 3: Voice & Tone Traits
- Dimension 4: Tone Modifiers
- Dimension 5: Target Audiences
- Dimension 6: Asset Types & Design System Mapping

**Smart defaults:** When Phase 0 (Context Ingestion) has been completed, each dimension may have pre-extracted data. The user always has full control — smart defaults are suggestions, not decisions. Present extracted values for confirmation and allow overrides on every dimension.

---

## Dimension 1: Brand Name & Tagline

**Question:** "What's your brand name? And if you have a tagline or slogan, include that too."

**Input type:** Open-ended

**Prompt details:**
- Use AskUserQuestion with two broad options to prime the response:
  - "I have a brand name and tagline ready" — Description: "Share your brand name and tagline/slogan. Example: 'The AI Launchpad — Build smarter, ship faster.'"
  - "I have a name but need help with a tagline" — Description: "Share your brand name and I'll help you craft a tagline during synthesis."

**Follow-up:** If the user only provides a name and no tagline, note it for synthesis — a tagline suggestion will be generated in Phase 2.

**Smart default behavior:** If Phase 0 extracted a brand name (from website header, logo, social bio, or document title), present it for confirmation: *"From your website, I found your brand name is **{name}**{and tagline **{tagline}** if found}. Sound right, or want to change it?"* Use AskUserQuestion with:
- "{extracted_name}{— extracted_tagline}" — Description: "Use the name and tagline I found in your assets."
- "I want to change this" — Description: "Provide a different brand name or tagline."
If only the name was found with no tagline, note: *"I found your brand name but no tagline — want to add one?"*

**Impact:** Determines `{{brand_name}}`, `{{tagline}}`, and `{{brand_slug}}` in the generated skill. The slug is derived from the brand name (lowercase, spaces/special chars → hyphens).

---

## Dimension 2: Mission & Value Proposition

**Question:** "What's your brand's mission? What problem do you solve, and what makes your approach unique?"

**Input type:** Open-ended

**Prompt details:**
- Use AskUserQuestion with two broad options:
  - "I have a clear mission statement" — Description: "Share your mission and what makes your brand's approach unique. Example: 'We make AI tools accessible to non-technical creators by focusing on visual, no-code workflows.'"
  - "I know what I do but haven't formalized it" — Description: "Describe what your brand does, who it helps, and what makes it different. I'll help distill it into a mission and value prop."

**Follow-up:** If the response is vague, ask: "Can you give me a specific example of how your brand helps someone? What does the before/after look like for your audience?"

**Smart default behavior:** If Phase 0 extracted mission/value prop signals (from About pages, pitch decks, or introductory copy), present the synthesis for confirmation: *"Based on your {source}, it looks like your mission is: **{inferred mission}**, with a value prop of: **{inferred value prop}**. Does this capture it, or would you refine it?"* Use AskUserQuestion with:
- "That captures it well" — Description: "Use the mission and value prop I extracted from your assets."
- "Close, but I want to refine it" — Description: "I'll share the extracted version as a starting point — edit or rewrite it."
- "That's not quite right" — Description: "Describe your mission and value prop in your own words."

**Impact:** Determines `{{mission}}` and `{{value_prop}}` in the generated skill. Informs voice application rules and audience profile generation.

---

## Dimension 3: Voice & Tone Traits

**Question:** "How should your brand sound? Pick up to 2 voice traits that best describe your brand's personality."

**Input type:** Multi-choice (multiSelect: true, pick up to 2)

**Options:**

| Option | Description |
|--------|-------------|
| Friendly & approachable | Conversational, warm, uses "you" and "we". Makes complex topics feel simple. Think: helpful friend who happens to be an expert. |
| Expert & authoritative | Confident, precise, backs claims with evidence. Establishes trust through depth. Think: trusted advisor who's done the research. |
| Bold & provocative | Challenges conventions, takes strong stances, isn't afraid to polarize. Think: industry insider who says what others won't. |
| Warm & encouraging | Supportive, empathetic, celebrates progress. Lowers the intimidation barrier. Think: mentor who believes in your potential. |
| Witty & playful | Clever, uses humor and wordplay, keeps things light without being unserious. Think: the brand that makes you smile while learning. |

**Follow-up:** If the user picks traits that may create tension (e.g., "Bold & provocative" + "Warm & encouraging"), acknowledge the combination and note: "That's an interesting combo — bold stance but delivered warmly. I'll make sure the voice rules capture both sides."

**Smart default behavior:** If Phase 0 analyzed writing samples (website copy, newsletter, blog posts, social media), infer voice traits from the copywriting style and pre-select the best matches: *"Based on your writing style, I'd suggest **{trait_1}** + **{trait_2}** — {brief evidence, e.g., 'your content is conversational but backs up claims with evidence'}. Does this match your intent?"* Still present all 5 options with the suggested ones noted, so the user can override.

**Impact:** Determines `{{voice_traits}}` and drives anti-pattern derivation in the generated skill. Each trait maps to a specific anti-pattern:

| Voice Trait | Anti-Pattern |
|---|---|
| Friendly & approachable | Cold, corporate, or impersonal language |
| Expert & authoritative | Wishy-washy, hedging, or non-committal claims |
| Bold & provocative | Safe, generic, or forgettable messaging |
| Warm & encouraging | Condescending, gatekeeping, or intimidating tone |
| Witty & playful | Dry, humorless, or robotic delivery |

---

## Dimension 4: Tone Modifiers

**Question:** "How should your brand's voice come across in practice? Pick up to 2 modifiers that shape how you communicate."

**Input type:** Multi-choice (multiSelect: true, pick up to 2)

**Options:**

| Option | Description |
|--------|-------------|
| Casual vocabulary | Uses everyday language, contractions, and informal phrasing. Avoids jargon unless explaining it. |
| Technical when needed | Comfortable with domain-specific terms but always explains them. Doesn't dumb things down but makes them accessible. |
| Short punchy sentences | Gets to the point fast. Favors clarity over completeness. Uses fragments for emphasis. |
| Storytelling style | Leads with narrative, examples, and scenarios. Explains concepts through stories rather than abstractions. |
| Direct & actionable | Focuses on what to do, not just what to know. Every piece of content has a clear takeaway or next step. |

**Follow-up:** None required — modifiers are additive and rarely conflict.

**Smart default behavior:** If Phase 0 analyzed writing samples, infer tone modifiers from sentence structure and vocabulary patterns: *"Your writing tends toward **{modifier_1}** + **{modifier_2}** — {brief evidence, e.g., 'sentences average 10-15 words, you use contractions and avoid jargon'}. Want to keep that style?"* Still present all 5 options with suggestions noted.

**Impact:** Determines `{{tone_modifiers}}` in the generated skill. Combined with voice traits to generate `{{voice_application_rules}}` — concrete guidelines for how the brand should sound in practice.

---

## Dimension 5: Target Audiences

**Question:** "Who is your brand for? Describe your primary audience, and a secondary audience if you have one."

**Input type:** Open-ended

**Prompt details:**
- Use AskUserQuestion with two broad options:
  - "I know my audiences well" — Description: "Describe your primary audience (and secondary if applicable). Include who they are, what they care about, and where they spend time. Example: 'Primary: Non-technical founders who want to use AI in their business. Secondary: Junior developers learning to build AI products.'"
  - "I have a general idea" — Description: "Describe who you're trying to reach in your own words. I'll help shape it into audience profiles with goals, frustrations, and platform preferences."

**Follow-up:** For each audience segment, if the user doesn't naturally cover these, ask:
- "What's the #1 goal your primary audience is trying to achieve?"
- "What frustrates them most about the current options available to them?"

**Smart default behavior:** If Phase 0 found audience signals (from website copy addressing "you", testimonials, subscriber descriptions, social media follower demographics, or content topics), present the inference: *"Based on your {source}, it looks like your primary audience is **{inferred audience}**{and secondary audience is **{inferred secondary}** if found}. Does this match, or would you describe them differently?"* Use AskUserQuestion with:
- "That's accurate" — Description: "Use the audience description I inferred from your assets."
- "Partially right — let me refine" — Description: "I'll share what I found as a starting point for you to edit."
- "That's off — let me describe them" — Description: "Describe your target audiences in your own words."

**Impact:** Determines `{{audiences}}` in the generated skill. Each audience segment gets a full profile: who they are, their goals, frustrations, what messaging resonates, and preferred platforms. Informs voice application rules (e.g., "casual vocabulary" hits differently for developers vs. executives).

---

## Dimension 6: Asset Types & Design System Mapping

**Pre-scan:** Before presenting options, scan `~/.claude/.context/design-systems/` for available design systems.

**Scanning logic:**
1. Check if `~/.claude/.context/design-systems/` exists
2. If it exists, list subdirectories
3. For each subdirectory, look for a `*-design-system.md` file
4. Read the first few lines of each design system file to extract the style name
5. Store as `available_design_systems` — a list of `{name, slug, path}` objects

**Question (Part A — Asset Types):** "What types of visual assets does your brand need? Select all that apply."

**Input type:** Multi-select (multiSelect: true)

**Options:**

| Option | Description |
|--------|-------------|
| YouTube thumbnails | Video thumbnail images — bold, attention-grabbing, face + text overlay compositions. |
| Social media posts | Instagram, Twitter/X, LinkedIn posts — square or portrait format, designed for feeds. |
| Blog/newsletter headers | Header images for articles and email newsletters — wide format, conceptual illustrations. |
| Presentation slides | Slide deck visuals — diagrams, icons, backgrounds for talks and webinars. |
| Website graphics | Hero images, feature illustrations, decorative elements for web pages. |
| Course/product assets | Covers, module illustrations, and marketing graphics for digital products. |
| Stickers & badges | Small, self-contained graphic elements — icons, badges, reaction stickers. |
| Print materials | Business cards, flyers, posters — physical media with bleed/trim considerations. |

**Question (Part B — DS Mapping):** Asked as a follow-up for **each selected asset type**.

"Which design system should be used for **{asset_type}**?"

**Input type:** Single-select per asset type

**Options (dynamic):**
- One option per entry in `available_design_systems`: "{style_name}" — Description: "Uses the {style_name} design system at `~/.claude/.context/design-systems/{slug}/`"
- "Create new design system" — Description: "Flag this asset type for a new design system. You can create it in Phase 4 using the branding-kit:design-system skill."
- "Decide later" — Description: "Leave this mapping empty for now. You can update it manually or re-run this skill later."

**If no design systems are available:**
- Only present "Create new design system" and "Decide later" as options
- Note to the user: "No design systems found at `~/.claude/.context/design-systems/`. You can create one using the branding-kit:design-system skill."

**Smart default behavior:** If Phase 0 found existing visual assets (e.g., thumbnail images on a YouTube channel, social media graphics, website hero images), pre-select the corresponding asset types: *"I found existing **{asset types}** in your assets — I've pre-selected those. Add or remove any that don't fit."* For DS mapping, if Phase 0 found images whose style matches an existing design system (by color palette or visual style), suggest that mapping: *"Your thumbnails look like they might use the **{style_name}** design system — want to map them there?"*

**Impact:** Determines `{{asset_ds_mapping}}` in the generated skill — the table that maps each asset type to a design system. This is the core of the brand skill's design system resolution logic.

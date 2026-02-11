---
name: design-system
description: Create comprehensive visual design systems through guided discovery. Defines brand aesthetics (colors, typography, illustration style, composition rules) via interactive questionnaire, generates a complete style guide document, and produces all visual assets for a style board using the nanobanana skill. Use when users want to create, update, or refresh a visual design system or art style guide.
---

# Design System Generator

Create complete visual design systems from scratch through guided discovery, documentation, and AI-generated asset production.

## Workflow Overview

Execute these phases in strict order. Output Location must be asked first. Phase 0 is optional (skip if user has no references). Never skip Phases 1-5. Each phase builds on the previous.

| Phase | Name | Action | Output |
|-------|------|--------|--------|
| — | Output Location | Ask where to save the design system | `output_location` = "local" or "user" |
| 0 | Reference Input | Collect + analyze user reference images | Visual analysis + smart defaults for discovery |
| 1 | Discovery | Interactive questionnaire | User preferences across 10 dimensions |
| 2 | Synthesis | Analyze + name the style | Style name, core principles, full spec |
| 3 | Documentation | Generate style guide | `{style-name}-design-system.md` |
| 4 | Asset Generation | Generate images via nanobanana | 8 PNG style board elements |
| 5 | Assembly | Organize + present | Complete design system directory |

---

## Output Location

Before anything else, ask the user where they want the design system saved. Use the AskUserQuestion tool:

**Question:** "Where should this design system be saved?"

| Option | Description |
|--------|-------------|
| Local project (current directory) | Saves to `./design-system/` in the current working directory. Best when this design system is specific to one project. |
| User level (system-wide) | Saves to `~/.claude/.context/design-systems/{style-name-slug}/`. Available across all projects and conversations. Best for brand-wide design systems you'll reuse everywhere (e.g., your YouTube brand, your newsletter brand). |

Store the choice as `output_location`.

**Path resolution** (happens after Phase 2 when the style name is finalized):
- **Local:** `{output_dir}` = `./design-system/`
- **User level:** `{output_dir}` = `~/.claude/.context/design-systems/{style-name-slug}/`

Where `{style-name-slug}` is the style name lowercased with spaces and special characters replaced by hyphens (e.g., "Ink & Ember" → `ink-and-ember`, "Neon Chalk" → `neon-chalk`).

**User-level design systems** are organized so each style gets its own directory:
```
~/.claude/.context/design-systems/
├── ink-and-ember/          ← YouTube brand
│   ├── ink-and-ember-design-system.md
│   ├── 01-hero-character.png
│   └── ...
├── paper-and-sage/         ← Newsletter brand
│   ├── paper-and-sage-design-system.md
│   ├── 01-hero-character.png
│   └── ...
```

---

## Phase 0: Reference Input (Optional)

Before starting discovery, ask the user if they have existing visual references to anchor the design system. References dramatically improve consistency by grounding the system in concrete examples rather than abstract descriptions alone.

**Opening prompt:** "Before we start defining your design system, do you have any existing visual references? These could be brand assets you already use, inspiration images, or examples of styles you like. This is optional — we can build entirely from scratch too."

**Supported input modes:**

| Mode | How to Provide | What Happens |
|------|---------------|--------------|
| Folder path | User provides a path like `~/brand-assets/` or `./images/` | Read all image files in the folder (PNG, JPG, SVG, WebP). Limit to 10 most relevant if more are provided. |
| Individual files | User provides one or more file paths | Read each image directly. |
| Website URL | User provides a URL like `https://mybrand.com` | Use WebFetch to capture the page, then analyze the visual design (colors, typography, layout, imagery style). |
| Direct paste | User pastes or drags images into the conversation | Analyze the images as provided. |
| Skip | User says they have no references | Proceed directly to Phase 1 with no smart defaults. |

**Analysis protocol:**

For each reference image or website, extract and document:

1. **Dominant colors** — Identify the 3-5 most prominent colors with approximate hex codes. Note which appear to be background, primary, and accent.
2. **Line work / rendering style** — Is it illustrated or photographic? If illustrated: line weight (thick/thin), edge quality (clean/sketchy), fill approach (flat/gradient/outline-only).
3. **Composition patterns** — Spacing density, focal point placement, symmetry, use of whitespace.
4. **Medium / aesthetic** — Flat vector, hand-drawn, 3D, photographic, collage, abstract, etc.
5. **Mood / emotional tone** — What feeling does it convey? Warm, corporate, playful, dark, etc.
6. **Character style** (if characters present) — Proportions, facial detail level, body style, identifying features.
7. **What's NOT present** — Notable absences that may indicate intentional anti-patterns (no gradients, no photography, no text, etc.).

**After analysis, present a summary:**
> "Here's what I'm seeing across your references: **[2-3 sentence synthesis of the dominant visual patterns — colors, style, mood, composition]**. I'll use this to suggest defaults during the discovery questionnaire, but you can override any suggestion."

**Smart defaults:**
- Store the analysis results as `reference_analysis`
- During Phase 1, for each dimension where the reference analysis provides a clear signal, pre-select the closest matching option and note: *"Based on your references, I'd suggest: **[option]** — [brief reason from analysis]. Does this match your intent?"*
- If the references are ambiguous for a dimension (e.g., mixed styles across images), present all options without a default and note the ambiguity: *"Your references show a mix of [X] and [Y] — which direction do you want to lean?"*
- The user always has full control — smart defaults are suggestions, not decisions

**Reference images are preserved for later use:**
- Copy user-provided reference images to `design-system/references/` during Phase 5
- These become part of the Reference Library alongside the 8 generated style board images
- During Phase 4 asset generation, user references can be provided to nanobanana as style anchors

---

## Phase 1: Discovery

Guide the user through structured questions to define their visual preferences. Use the AskUserQuestion tool to present options.

Load the full question bank from [references/discovery-framework.md](references/discovery-framework.md).

**Rules:**
- Ask questions in dimension order (they build on each other)
- Present 3-4 options per question with clear descriptions
- Allow multi-select where the framework indicates
- **If Phase 0 produced smart defaults**, pre-select the suggested option and include the reasoning. Still present all options — the user decides.
- After each answer, give a brief 1-sentence acknowledgment contextualizing the choice, then move to the next question
- Adapt later questions based on earlier answers (the framework specifies when to skip or modify questions)
- Complete ALL dimensions before moving to Phase 2
- Batch related questions when possible (max 4 per AskUserQuestion call) to keep the flow efficient without overwhelming

**Dimensions (in order):**
1. Primary use cases
2. Overall vibe / mood
3. Medium preference (illustration vs photography)
4. Specific illustration style direction
5. Color strategy
6. Accent color
7. Base tone
8. Line work / edge treatment
9. Composition approach
10. Anti-patterns (what to avoid)

---

## Phase 2: Synthesis

After all 10 dimensions are answered, synthesize into a coherent design system.

**Steps:**
1. Review all discovery answers as a complete set
2. Identify the dominant aesthetic thread connecting the choices
3. Generate a memorable 2-3 word **style name** using the naming convention below
4. Define 3-4 **core principles** — short imperative phrases with explanations
5. Build the complete **color palette** — 6 colors with hex codes, role names, usage descriptions, AND natural language AI descriptions (see template)
6. Calculate **color ratios** based on strategy (see ratio guide in template)
7. Build the **Style Language Map** — translate every technical spec (colors, line work, fill, texture, composition, mood) into copy-paste-ready natural language phrases for prompt use. This is critical for AI generation consistency.
8. Specify **line work**, **illustration**, **typography**, and **composition** rules
9. Define the **Character System** — including system type (Solo, Duo/Companion, or Cast). For each character: archetype, proportions, **strict facial feature rules** (what IS present AND what is FORBIDDEN), consistent identifiers, and fidelity levels. For Duo systems: define companion appearance, states/behaviors, and which character owns the accent color. See template for full structure.
10. Define **application guidelines** for each use case from Dimension 1
11. List explicit **anti-patterns** from Dimension 10 plus any that conflict with chosen directions
12. Create the **Consistency Enforcement** section — document unwanted feature prevention rules, style drift prevention keywords, and a character verification checklist (see template)

**Style Naming Convention:**
Combine a texture word + a color/mood word. The name should evoke the visual feel in 2-3 words.

| Texture Words | Color/Mood Words |
|---------------|-----------------|
| Ink, Chalk, Pixel, Neon, Paper | Teal, Coral, Sunset, Midnight, Forest |
| Brush, Wire, Grain, Sketch, Foil | Ocean, Ember, Frost, Clay, Bloom |
| Velvet, Stone, Glass, Thread, Stamp | Sage, Copper, Slate, Ivory, Plum |

Examples: "Ink & Teal", "Neon Chalk", "Warm Blueprint", "Velvet Ember", "Paper & Sage"

**Present the style name and core principles to the user for approval before proceeding to Phase 3.** If the user wants changes, adjust and re-present.

---

## Phase 3: Documentation

Generate the complete design system document using the template from [references/design-system-template.md](references/design-system-template.md).

**Output:** A markdown file saved to `{output_dir}/{style-name}-design-system.md` (see Output Location for path resolution).

**Rules:**
- Fill EVERY section — no placeholders or template markers in the final output
- Include specific hex codes for all colors
- Write in present tense, declarative voice
- Include concrete, actionable guidelines (not vague suggestions)
- The document must be fully self-contained — anyone reading it should be able to produce on-brand visuals without additional context
- Include the complete Nano Banana prompt library (8 prompts) in the document

---

## Phase 4: Asset Generation

Generate 8 style board elements using the **nanobanana** skill. Build prompts using the templates and best practices from [references/prompt-engineering.md](references/prompt-engineering.md).

**Required elements (generate in this order):**

| # | Element | Aspect Ratio | Description |
|---|---------|-------------|-------------|
| 1 | Hero character/mascot | 1:1 | The signature illustrated element |
| 2 | Concept icon | 1:1 | A single idea visualized |
| 3 | Framework diagram | 16:9 | Connected nodes or flow |
| 4 | Social media asset | 1:1 | A standalone icon for posts |
| 5 | Background texture | 16:9 | Subtle, usable background |
| 6 | Sticker/badge | 1:1 | Compact element, transparent bg |
| 7 | Pattern element | 1:1 | Repeating doodles or motifs |
| 8 | Character scene | 1:1 | Person or figure in context |

**For each element:**
1. Write a detailed narrative prompt following the templates in prompt-engineering.md
2. Embed the exact hex codes, line style, and composition rules from the design system
3. Specify the correct aspect ratio from the table above
4. **If Phase 0 provided user references**, select the 1-2 most relevant reference images for this element type and provide them to nanobanana as style anchors (see prompt-engineering.md "Using User-Provided References" section)
5. Use the nanobanana skill to generate the image
6. Save the output to the `{output_dir}` directory with a descriptive filename

**Prompt construction rules:**
- Write as descriptive narrative paragraphs (NOT keyword lists)
- Always specify background color by name AND hex code
- Always describe the line/stroke style explicitly
- Always constrain accent color usage ("the only color in the entire image")
- Always end with format/aspect ratio
- Include explicit exclusions ("No text, no gradients, no other colors")
- Reference the artistic tool metaphor from the design system (brush pen, marker, pencil, etc.)

**Naming convention for generated files:**
```
{output_dir}/01-hero-character.png
{output_dir}/02-concept-icon.png
{output_dir}/03-framework-diagram.png
{output_dir}/04-social-media-asset.png
{output_dir}/05-background-texture.png
{output_dir}/06-sticker-badge.png
{output_dir}/07-pattern-element.png
{output_dir}/08-character-scene.png
```

---

## Phase 5: Assembly

Organize all outputs and present the complete system to the user.

**Final directory structure:**

For **local** (`output_location` = local):
```
./design-system/
├── {style-name}-design-system.md
├── 01-hero-character.png
├── ...
├── 08-character-scene.png
└── references/              ← only if Phase 0 provided user references
```

For **user level** (`output_location` = user):
```
~/.claude/.context/design-systems/{style-name-slug}/
├── {style-name}-design-system.md
├── 01-hero-character.png
├── ...
├── 08-character-scene.png
└── references/              ← only if Phase 0 provided user references
```

**Final steps:**
1. List all generated files with brief descriptions and the full output path
2. Display the style board layout diagram (from the design system document)
3. **Establish the Reference Library** — present the 8 generated images as canonical style references. Explain that these images should be provided as style references when generating future assets (using nanobanana's multi-image reference capability) to maintain visual consistency beyond what text prompts alone achieve.
4. **Run the Verification Checklist** against each generated image:
   - Does the color palette match? (check accent color, base tone, ink colors)
   - Is the line weight/style consistent with the design system spec?
   - Does the composition follow the defined rules?
   - Are anti-patterns absent?
   - Does the overall mood match the Style Language Map?
   - **Character facial features:** Do characters have ONLY the allowed features? Check for unwanted noses, eyebrows, ears, or other forbidden features. This is the most common failure — verify every face.
   - **Companion character (if Duo system):** Is the companion present? Is it the correct size relative to the primary character? Is it the ONLY accent-colored element?
   Flag any images that fail verification and offer to regenerate them.
5. Ask the user: "Want to regenerate or adjust any elements?"
6. Offer to generate additional element types or variations
7. If the user is satisfied, confirm the design system is complete
8. **If user-level:** Remind the user that this design system is now available system-wide. In any future Claude Code session, they (or a future asset-generation skill) can reference it at `~/.claude/.context/design-systems/{style-name-slug}/`

---

## Updating an Existing Design System

If the user already has a design system document, read it first before starting.

**Update workflow:**
1. Read and summarize the existing design system
2. Ask the user what they want to change (skip full discovery — only ask about the dimensions being modified)
3. Re-synthesize only the affected aspects
4. Update the design system document (preserve unchanged sections)
5. Regenerate only the assets affected by the changes
6. Preserve unchanged elements and filenames

---

## Error Handling

- If nanobanana generation fails, retry once with a simplified prompt
- If the user is unhappy with a generated element, ask what specifically to change and regenerate with an adjusted prompt
- If the user's preferences conflict (e.g., "minimalist" + "dense and detailed"), flag the tension during synthesis and ask which direction to prioritize
- If the output directory does not exist, create it (including parent directories for user-level paths)
- If a design system with the same slug already exists at the user level, ask the user whether to overwrite or choose a different name

---
name: design-system-generator
description: Create comprehensive visual design systems through guided discovery. Defines brand aesthetics (colors, typography, illustration style, composition rules) via interactive questionnaire, generates a complete style guide document, and produces all visual assets for a style board using the nanobanana skill. Use when users want to create, update, or refresh a visual design system or art style guide.
---

# Design System Generator

Create complete visual design systems from scratch through guided discovery, documentation, and AI-generated asset production.

## Workflow Overview

Execute these 5 phases in strict order. Never skip phases. Each phase builds on the previous.

| Phase | Name | Action | Output |
|-------|------|--------|--------|
| 1 | Discovery | Interactive questionnaire | User preferences across 10 dimensions |
| 2 | Synthesis | Analyze + name the style | Style name, core principles, full spec |
| 3 | Documentation | Generate style guide | `{style-name}-design-system.md` |
| 4 | Asset Generation | Generate images via nanobanana | 8 PNG style board elements |
| 5 | Assembly | Organize + present | Complete `design-system/` directory |

---

## Phase 1: Discovery

Guide the user through structured questions to define their visual preferences. Use the AskUserQuestion tool to present options.

Load the full question bank from [references/discovery-framework.md](references/discovery-framework.md).

**Rules:**
- Ask questions in dimension order (they build on each other)
- Present 3-4 options per question with clear descriptions
- Allow multi-select where the framework indicates
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
5. Build the complete **color palette** — 6 colors with hex codes, role names, and usage descriptions
6. Calculate **color ratios** based on strategy (see ratio guide in template)
7. Specify **line work**, **illustration**, **typography**, and **composition** rules
8. Define **application guidelines** for each use case from Dimension 1
9. List explicit **anti-patterns** from Dimension 10 plus any that conflict with chosen directions

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

**Output:** A markdown file saved to `design-system/{style-name}-design-system.md` in the project directory.

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
4. Use the nanobanana skill to generate the image
5. Save the output to the `design-system/` directory with a descriptive filename

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
design-system/01-hero-character.png
design-system/02-concept-icon.png
design-system/03-framework-diagram.png
design-system/04-social-media-asset.png
design-system/05-background-texture.png
design-system/06-sticker-badge.png
design-system/07-pattern-element.png
design-system/08-character-scene.png
```

---

## Phase 5: Assembly

Organize all outputs and present the complete system to the user.

**Final directory structure:**
```
design-system/
├── {style-name}-design-system.md
├── 01-hero-character.png
├── 02-concept-icon.png
├── 03-framework-diagram.png
├── 04-social-media-asset.png
├── 05-background-texture.png
├── 06-sticker-badge.png
├── 07-pattern-element.png
└── 08-character-scene.png
```

**Final steps:**
1. List all generated files with brief descriptions
2. Display the style board layout diagram (from the design system document)
3. Ask the user: "Want to regenerate or adjust any elements?"
4. Offer to generate additional element types or variations
5. If the user is satisfied, confirm the design system is complete

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
- If the project has no `design-system/` directory, create it

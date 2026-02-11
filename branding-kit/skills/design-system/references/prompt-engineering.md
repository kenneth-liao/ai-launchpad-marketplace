# Prompt Engineering for Design System Assets

How to construct effective Nano Banana prompts for generating style-consistent design system elements.

## Core Principle

Nano Banana (Google Gemini image generation) responds best to **descriptive narrative paragraphs**. Write prompts as if describing a scene to a skilled illustrator — not as comma-separated keyword lists.

---

## Prompt Anatomy

Every prompt must include these 8 components in this order:

1. **Subject declaration** — What the image IS ("A hand-drawn illustration of...", "A minimalist sketch of...")
2. **Background specification** — Exact base color by name AND hex code
3. **Style description** — Artistic tool metaphor, line quality, rendering approach
4. **Subject details** — Proportions, features, specific visual characteristics
5. **Color constraints** — Which colors appear, where, and the accent color rule
6. **Composition direction** — Placement, spacing, focal point, negative space
7. **Exclusions** — What must NOT appear ("No text, no gradients, no other colors")
8. **Format** — Aspect ratio as the final instruction

---

## Variable Reference

When building prompts, substitute these variables from the completed design system:

| Variable | What It Is | Example Value |
|----------|-----------|---------------|
| `{base_color}` | Background color name + hex | "warm cream (#FAF8F5)" |
| `{base_color_desc}` | Natural language description from Style Language Map | "warm cream like aged linen paper" |
| `{primary_ink}` | Main stroke/text color + hex | "charcoal black (#2D2D2D)" |
| `{primary_ink_desc}` | Natural language description | "deep charcoal like soft 6B pencil" |
| `{secondary_ink}` | Supporting detail color + hex | "warm gray (#8C8C8C)" |
| `{light_tone}` | Subtle background element color + hex | "soft gray (#D4D0CB)" |
| `{accent_color}` | Pop/highlight color + hex | "electric teal (#00BFA6)" |
| `{accent_color_desc}` | Natural language description | "vivid electric teal like tropical water" |
| `{line_style}` | Full line work description from Style Language Map | "thick, rounded brush pen strokes with slightly imperfect, organic edges" |
| `{tool_metaphor}` | Artistic tool reference | "as if sketched in a premium notebook" |
| `{style_descriptor}` | Overall aesthetic in a phrase | "hand-drawn sketchbook-style" |
| `{fill_approach}` | How shapes are filled, from Style Language Map | "outline-only with no fill" or "flat solid fills" |
| `{texture_quality}` | Surface/paper feel from Style Language Map | "subtle paper grain texture, like a premium Moleskine page" |
| `{composition_rule}` | Spatial approach from Style Language Map | "centered with generous whitespace on all sides" |
| `{overall_mood}` | Overall mood phrase from Style Language Map | "warm, approachable, and quietly confident" |
| `{feel}` | Emotional descriptors | "warm, approachable, and inviting" |
| `{exclusions}` | Standard exclusions | "No text, no gradients, no other colors, no complex backgrounds" |

**Important:** For color variables, always use BOTH the hex code AND the natural language description in prompts. The hex code provides precision; the natural language description helps the AI model understand the intended feel. Example: "on a warm cream (#FAF8F5) background — the color of aged linen paper." Pull all `_desc` values directly from the **Style Language Map** section of the design system document to ensure consistency across all prompts.

---

## Element Templates

### 1. Hero Character / Mascot

**Aspect ratio:** 1:1 (square)
**Purpose:** The signature visual element that represents the brand

**Template:**
```
A {style_descriptor} illustration of {INSERT CHARACTER PROMPT FRAGMENT FROM DESIGN SYSTEM} on a {base_color_desc} ({base_color}) background. {tool_metaphor}. {Additional pose/action details for this specific image}. The composition is {composition_rule}. The texture has {texture_quality}. The overall mood is {overall_mood} — not pixel-perfect or computer-generated. No other objects, no text, no gradients. Square format.
```

**Note:** Always insert the **Character Prompt Fragment** from the design system's Character System section. Do NOT write a new character description — use the pre-written fragment verbatim for consistency.

**Character type suggestions by vibe:**
- Clean & modern: geometric robot, abstract mascot, simple animal
- Warm & friendly: rounded robot, smiling character, cute animal
- Bold & energetic: dynamic figure, action pose character
- Dark & sophisticated: minimal silhouette, elegant figure

---

### 2. Concept Icon

**Aspect ratio:** 1:1 (square)
**Purpose:** A single idea or concept visualized as an icon

**Template:**
```
A minimalist, {style_descriptor} sketch of a single {object} on a {base_color} canvas. The {object} is drawn with {line_style}. {Shape details: proportions, distinctive features}. {Accent placement description}: a {specific part} rendered in {accent_color}, the only color accent in the entire image. {Optional secondary detail} in {light_tone}. The {object} is positioned {placement within frame} with {spacing description — e.g., "enormous negative space surrounding it"}. No text, no background texture, just the single {object} on {base_color short name}. The feeling is {feel}. Square format.
```

**Object suggestions by brand domain:**
- Tech/AI: lightbulb, chip, neural network node, cursor
- Education: book, pencil, graduation cap, puzzle piece
- Creative: paintbrush, palette, camera, pen
- Business: rocket, target, gear, chart

---

### 3. Framework Diagram

**Aspect ratio:** 16:9 (landscape)
**Purpose:** Connected elements showing structure, flow, or relationships

**Template:**
```
A {style_descriptor} diagram showing {number} {shape_type}s connected by {connector_type} on a {base_color} background. Each {shape_type} is drawn with {line_style}. The {shape_type}s are arranged in {arrangement — e.g., "a triangle formation", "a horizontal row", "a circular flow"} with generous spacing between them. The connecting {connector_type}s are {connector_style — e.g., "hand-drawn with slightly wobbly, natural curves"}. One of the {shape_type}s is filled with {accent_color} while the others are {default_treatment — e.g., "outline-only"}. Small {annotation_style} annotations in {light_tone} extend from each element like label placeholders. The overall composition is {composition_rule}. The style feels like {metaphor — e.g., "a thoughtful whiteboard sketch in a premium notebook"}. Landscape format, 16:9 aspect ratio.
```

---

### 4. Social Media Asset

**Aspect ratio:** 1:1 (square)
**Purpose:** A standalone icon or visual suitable for social media posts

**Template:**
```
A single {style_descriptor} {icon_type} centered on a vast {base_color} background. The {icon_type} is drawn with {line_style}. {Shape details: teeth, edges, proportions, distinctive features}. The {accent_element_location} of the {icon_type} is filled with {accent_color}, creating the only pop of color in the entire image. The line work has visible {hand_quality — e.g., "hand-drawn character"} — not a perfect vector shape. The {icon_type} sits {placement within frame} with abundant empty {base_color short name} space {direction}. {Optional tiny secondary detail in {light_tone}}. {feel_summary}. Square format.
```

---

### 5. Background / Texture

**Aspect ratio:** 16:9 (landscape)
**Purpose:** A subtle, usable background for slides, posts, or web sections

**Template:**
```
A minimal {base_color} background designed to look like {texture_metaphor — e.g., "a premium blank notebook page", "a clean whiteboard", "a textured paper surface"}. {Subtle texture description} at approximately {opacity — typically 5-15} percent opacity across the full frame. In the {corner_position — e.g., "bottom-right corner"}, a small {style_descriptor} sketch of a tiny {small_element} is drawn in {primary_ink} with {line_style}, with a small {accent_color} {accent_detail} — the only color accent. The {small_element} is small, occupying less than 10 percent of the frame, leaving the vast majority of the image as clean, usable negative space. The style is {feel} — like {metaphor — e.g., "opening a fresh page in a creative journal"}. Landscape format, 16:9 aspect ratio.
```

---

### 6. Sticker / Badge

**Aspect ratio:** 1:1 (square)
**Purpose:** A compact visual element, ideally on transparent background

**Template:**
```
A {style_descriptor} {sticker_subject — e.g., "checkmark", "star badge", "thumbs up"} on a transparent background. The {sticker_subject} is drawn with {line_style_detail — e.g., "a single thick, rounded brush pen stroke with organic, confident line quality — slightly thicker at the base, tapering at the ends"}. Behind the {sticker_subject}, a loose {frame_shape — e.g., "hand-drawn circle", "rounded rectangle"} in {accent_color} frames it, drawn with the same {style_quality — e.g., "sketchy, imperfect quality"}. The {accent_frame} is not perfectly {geometric_shape} — it has the organic wobble of a real hand-drawn mark. The overall size is compact, sticker-like. The background must be transparent. The style is {feel}.
```

**Note:** Always request transparent background for sticker elements.

---

### 7. Pattern Element

**Aspect ratio:** 1:1 (square)
**Purpose:** Scattered doodles or motifs that can tile or decorate

**Template:**
```
A collection of small, simple {style_descriptor} doodle icons scattered loosely across a {base_color} background. The doodles include: {list of 5-6 simple, brand-relevant shapes/objects}. All are drawn in {light_tone} with {light_line_variant — e.g., "thin, sketchy rounded lines"} — except for one single element, a small {highlighted_element}, which is drawn in {accent_color}. The doodles are spread with generous spacing between them, creating an airy, breathing pattern. Each doodle is simple — just 2-3 strokes maximum. The overall feeling is {pattern_feel — e.g., "playful but restrained, like margin doodles in a notebook"}. The composition is balanced but organic, not rigidly gridded. Square format.
```

**Doodle suggestions by domain:**
- Tech/AI: stars, arrows, brackets, circuits, dots, lightning bolts
- Education: stars, arrows, checkmarks, books, lightbulbs, pencils
- Creative: swirls, stars, hearts, diamonds, clouds, spirals
- Business: arrows, targets, charts, diamonds, plus signs, checkmarks

---

### 8. Character Scene

**Aspect ratio:** 1:1 (square)
**Purpose:** A person or figure shown in context, doing something relatable

**Template:**
```
A minimalist {style_descriptor} illustration of {INSERT CHARACTER PROMPT FRAGMENT FROM DESIGN SYSTEM} {doing_action — e.g., "sitting at a laptop computer"}, centered on a {base_color_desc} ({base_color}) background. {Key prop/object} shows a single {accent_color} {accent_detail — e.g., "glowing rectangle on the screen"} — the only color in the entire illustration beyond the character's identifier. {Fill approach — e.g., "The figure and laptop are drawn with outline-only style, no complex shading or fills."}. The character is positioned {placement} with {spacing description}. The texture has {texture_quality}. The overall mood is {overall_mood}. Square format.
```

**Note:** Insert the **Character Prompt Fragment** verbatim. For scene-specific details (action, props), add those AFTER the fragment — never modify the fragment itself.

---

## Nano Banana Best Practices

### Do:
- Write full descriptive paragraphs — the model's strength is deep language understanding
- Specify exact hex codes for colors (the model interprets them correctly)
- Name the artistic tool or medium ("brush pen", "felt-tip marker", "pencil sketch", "technical pen")
- Include negative instructions ("no text", "no gradients", "no other colors")
- Specify aspect ratio as the final instruction in every prompt
- Describe desired imperfections explicitly ("slightly uneven", "not perfectly round", "organic wobble")
- Provide context about the purpose when helpful ("designed for use as a social media icon")

### Don't:
- Use comma-separated keyword lists like Stable Diffusion prompts
- Reference specific artists by name — describe the style attributes instead
- Request multiple focal points in a single image
- Leave the background color unspecified or vague
- Forget to constrain accent color usage (always state "the only color" or "the only accent")
- Use technical jargon the model might misinterpret (prefer plain descriptions)

### Aspect Ratio Guide:

| Ratio | Format | Best For |
|-------|--------|----------|
| 1:1 | Square | Icons, stickers, characters, social posts, profile images |
| 16:9 | Landscape | Backgrounds, diagrams, slide assets, banners, YouTube thumbnails |
| 9:16 | Portrait | Story-format content, mobile-first assets, Pinterest pins |
| 4:3 | Standard | Presentation slides, course materials, traditional layouts |
| 21:9 | Ultra-wide | Website hero banners, cinematic headers |

### Iteration Strategy:
- Generate each element once, review with the user before moving to the next
- For adjustments, describe what specifically to change ("make the lines thicker", "move the character left")
- Keep prompt language consistent across all 8 elements to maintain visual cohesion
- If an element doesn't match the style, check that all hex codes and style descriptors are present in the prompt

---

## Character Consistency Protocol

Maintaining a consistent character across multiple generated images is one of the hardest challenges in AI image generation. Follow this protocol rigorously.

### The Character Prompt Fragment

The design system document contains a **Character Prompt Fragment** — a pre-written paragraph describing the character in full detail. This fragment is the single source of truth for character appearance.

**Rules:**
1. **Copy the fragment verbatim** into every prompt that includes the character. Do not paraphrase, abbreviate, or "improve" it. Exact repetition = consistency.
2. **Place it immediately after the subject declaration** in the prompt anatomy (after component 1, before component 3).
3. **Never add new character details** not in the fragment. If you describe the character wearing a hat in one prompt but the fragment doesn't mention a hat, the character will drift.
4. **Never omit identifiers.** The fragment specifies 2-3 consistent identifiers (scarf, glasses, antenna, etc.) that MUST appear every time.

### Character at Different Fidelity Levels

The design system defines three fidelity levels: Hero, Standard, and Spot. When generating at reduced fidelity:

- **Hero (full detail):** Use the complete Character Prompt Fragment unchanged.
- **Standard (moderate):** Use the fragment but add "simplified" before the character description. Keep all identifiers. Allow facial features to reduce.
- **Spot (minimal):** Describe only the silhouette shape and 1 primary identifier. Example: "a small rounded robot silhouette with a tiny teal scarf, drawn as a simple shape."

### Character + Reference Images

For maximum character consistency:
1. Always provide `01-hero-character.png` as a style reference when generating any image containing the character
2. In the prompt, add: "The character should match the appearance in the reference image exactly."
3. For scene illustrations, also provide `08-character-scene.png` to show how the character sits within a composition

### The Unwanted Facial Features Problem

AI generators (especially Gemini) frequently add noses, eyebrows, ears, and other facial details to characters that are supposed to be minimal (dot-eyes-only). This is the single most common consistency failure.

**Prevention protocol:**
1. **Always state what IS there before what is NOT:** "The face has ONLY two dot eyes and a curved smile — absolutely NO nose, NO eyebrows, NO ears, NO additional facial features"
2. **Include the prohibition in EVERY prompt** that contains a character, even if it feels repetitive
3. **Use the word "absolutely"** before the prohibition — it signals emphasis to the model
4. **List each forbidden feature individually** — "NO nose, NO eyebrows, NO ears" is more effective than "no other facial features"
5. **Provide a reference image** showing the correct minimal face. When using multiple references, always include at least one with a close-up of the correct facial treatment
6. **After generation, verify the face** against the design system's facial features rules. Regenerate immediately if extra features appear — don't compromise.

### Companion Character Consistency (Duo Systems)

When the character system includes a companion (e.g., an AI orb, a sidekick creature):
1. **Use separate prompt fragments** for the primary character and companion — don't merge them
2. **State the accent color rule explicitly:** "The companion is the ONLY [accent color] element in the entire image — nothing else is [accent color]"
3. **Define the companion's state** for each specific image (working, following, excited, etc.) rather than leaving it generic
4. **Size relationship:** Always specify the companion's size relative to the primary character (e.g., "one-fifth the size of the Builder's head")

### Common Character Drift Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Character changes proportions | Fragment not copied verbatim | Re-copy exact fragment text |
| Accent color appears on wrong element | Accent rule not explicit enough | Add "the ONLY accent color is the [item]" |
| Character gains unwanted details | Extra descriptors in prompt | Remove any character description not in the fragment |
| Character loses identifiers at small size | Using Hero fragment for Spot context | Switch to Spot-level description |
| Character style doesn't match rest of image | Line style not referenced | Include `{line_style}` description in the character portion too |
| Character gains unwanted features (nose, eyebrows) | Prohibition not explicit enough | Add "absolutely NO nose, NO eyebrows, NO ears" and provide a reference image with correct face |
| Companion missing or wrong size | Companion not described in prompt | Always include the companion prompt fragment alongside the primary character fragment |

---

## Adapting Templates by Style

### For Photography-Forward Styles:
Replace illustration prompts with photo-style language:
- "A professional photograph of..." instead of "A hand-drawn illustration of..."
- Reference lighting setups instead of line work
- Describe color grading and mood instead of fill approach
- Use "shot on [camera type]" for realism cues

### For Abstract / Geometric Styles:
Replace character and object prompts with abstract compositions:
- "An abstract composition of geometric shapes..." instead of character descriptions
- Focus on shape relationships, negative space, and color blocking
- Describe mathematical precision or organic flow depending on sub-style

### For 3D / Isometric Styles:
Add dimensional language:
- "An isometric 3D illustration..." as opener
- Include material descriptions ("matte plastic", "soft clay", "frosted glass")
- Describe lighting direction and shadow behavior
- Reference depth and perspective explicitly

### For Printmaking Styles (Linocut, Risograph, Woodblock, Screenprint):
Replace illustration language with print-process language:
- "A bold linocut print illustration of..." instead of "A hand-drawn illustration of..."
- Use "carved," "cut," "printed," "pressed" — NEVER "drawn," "sketched," or "pen strokes"
- Describe the print process: "carved in bold, chunky lines with rough edges and visible carving texture, like a hand-cut linoleum block"
- Add texture: "natural grain and slight ink-bleed texture throughout, like a hand-pressed block print"
- For accent color, describe as an overprint: "rendered as a second-color overprint, slightly misregistered from the primary ink layer for printing authenticity"
- High contrast is key: "high contrast with areas of solid ink and clean paper negative space"
- Fills work differently: solid ink fills (for shoes, hats, shadows) are part of the carved aesthetic, unlike outline-only sketch styles

**Additional prompt variables for printmaking:**

| Variable | What It Is | Example Value |
|----------|-----------|---------------|
| `{print_process}` | Type of printmaking technique | "linocut block print" or "risograph print" or "woodblock print" |
| `{carving_texture}` | How carved marks look | "rough carved edges and visible carving texture, like a hand-cut linoleum block" |
| `{ink_texture}` | How ink transfers to paper | "natural grain and slight ink-bleed texture throughout" |
| `{overprint_effect}` | How the accent color is printed | "a second-color overprint, slightly misregistered from the charcoal layer" |
| `{solid_fill_areas}` | Where solid ink fills appear | "shoes, cap, and grounding shadow areas use solid charcoal fill" |

### For Dark/Moody Styles:
Invert the color language:
- Base becomes the dark background
- "Light" elements become the contrast elements
- Accent color reads differently on dark — may need to adjust brightness
- Add atmospheric descriptors ("dramatic", "cinematic", "atmospheric lighting")

---

## Using the Reference Library

After the initial 8 style board elements are generated, they form a **Reference Library** — a set of canonical images that anchor the visual style for all future asset creation.

### When to Use Reference Images

Always provide reference images alongside text prompts when generating new assets. Text prompts alone produce consistent-ish results; text prompts + reference images produce highly consistent results.

### How to Select References

1. **Match by element type** — Use the Reference Image Index in the design system document to find the closest reference for what you're creating
2. **Use 1-2 references max** — More than 2 dilutes the style signal and can confuse the model
3. **Prioritize the reference that shares the most visual properties** with your target output:
   - Creating a new character? Use `01-hero-character.png` + `08-character-scene.png`
   - Creating a new icon? Use `02-concept-icon.png`
   - Creating a new diagram? Use `03-framework-diagram.png`
   - Creating a decorative element? Use `06-sticker-badge.png` + `07-pattern-element.png`

### How to Combine References with Prompts

When using the nanobanana skill with reference images:
1. Provide the reference image(s) as input
2. Write the text prompt using variables from the Style Language Map (ensures text and image references align)
3. In the prompt, add: "Match the illustration style, line weight, and color treatment of the reference image."
4. Keep all other prompt components (subject, composition, exclusions, format) as usual

### When NOT to Use References

- When intentionally exploring a new visual direction within the design system
- When the reference library doesn't have a relevant match (generate the new type, then add it to the library)

---

## Using User-Provided References

If Phase 0 collected user reference images (brand assets, inspiration images, website screenshots), these are distinct from the generated Reference Library and have their own usage rules.

### User References vs. Generated References

| Aspect | User-Provided References | Generated Reference Library |
|--------|--------------------------|----------------------------|
| Purpose | Style anchoring — "make it look like THIS" | Consistency anchoring — "keep it matching the system" |
| When available | From Phase 0 onward | After Phase 4 completes |
| Priority during Phase 4 | **Primary** — use these to anchor the initial generation | N/A (doesn't exist yet) |
| Priority after Phase 4 | **Secondary** — use when generated refs don't cover the need | **Primary** — these ARE the system |
| Location | `design-system/references/` | `design-system/` (numbered 01-08) |

### During Phase 4 (Initial Asset Generation)

User references are most valuable here because the generated library doesn't exist yet:

1. **Select 1-2 user references** that best match the element being generated
2. Provide them to nanobanana as style reference images
3. In the prompt, add: "Match the visual style, color palette, and artistic approach of the reference image while following the design system specifications below."
4. The text prompt (from the design system) provides the specific details; the reference image provides the overall visual feel
5. If user references conflict with discovery answers (e.g., reference shows gradients but user chose "no gradients"), **the discovery answers take priority** — the user explicitly chose those preferences

### Reference Selection Guide for Phase 4

| Element Being Generated | Best User Reference To Use |
|------------------------|---------------------------|
| Hero character / mascot | Any reference showing characters, mascots, or figures |
| Concept icon | Any reference showing icons, symbols, or simple objects |
| Framework diagram | Any reference showing diagrams, flows, or connected elements |
| Social media asset | Any reference from social media contexts |
| Background texture | Any reference with notable texture or background treatment |
| Sticker / badge | Any reference showing compact, standalone elements |
| Pattern element | Any reference showing patterns, scattered elements, or decorative motifs |
| Character scene | Any reference showing characters in context or scenes |

If no user reference matches the element type, generate without a reference image — rely on the text prompt and Style Language Map alone.

### After Phase 4 (Future Asset Generation)

Once the 8-image Reference Library exists, prefer it over user references for routine generation. User references remain useful when:
- Creating something the generated library doesn't cover
- The user wants to pull a specific quality from the original inspiration that the generated library didn't fully capture
- Generating for a new use case not represented in the existing system

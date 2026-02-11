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
| `{primary_ink}` | Main stroke/text color + hex | "charcoal black (#2D2D2D)" |
| `{secondary_ink}` | Supporting detail color + hex | "warm gray (#8C8C8C)" |
| `{light_tone}` | Subtle background element color + hex | "soft gray (#D4D0CB)" |
| `{accent_color}` | Pop/highlight color + hex | "electric teal (#00BFA6)" |
| `{line_style}` | Full line work description | "thick, rounded brush pen strokes with slightly imperfect, organic edges" |
| `{tool_metaphor}` | Artistic tool reference | "as if sketched in a premium notebook" |
| `{style_descriptor}` | Overall aesthetic in a phrase | "hand-drawn sketchbook-style" |
| `{fill_approach}` | How shapes are filled | "outline-only with no fill" or "flat solid fills" |
| `{composition_rule}` | Spatial approach | "centered with generous whitespace on all sides" |
| `{feel}` | Emotional descriptors | "warm, approachable, and inviting" |
| `{exclusions}` | Standard exclusions | "No text, no gradients, no other colors, no complex backgrounds" |

---

## Element Templates

### 1. Hero Character / Mascot

**Aspect ratio:** 1:1 (square)
**Purpose:** The signature visual element that represents the brand

**Template:**
```
A {style_descriptor} illustration of a friendly, simple {character_type} on a {base_color} background. The {character_type} is drawn with {line_style} — {tool_metaphor}. {Specific character details: body shape, proportions, expression, pose}. The {character_type} is {fill_approach}, except for a single {accent_color} {accent_element} — the only color accent in the entire image. The composition is {composition_rule}. The style is {feel} — not pixel-perfect or computer-generated. No other objects, no text, no gradients. Square format.
```

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
A minimalist {style_descriptor} illustration of a simple {character_description — e.g., "human figure"} {doing_action — e.g., "sitting at a laptop computer"}, centered on a {base_color} background. The figure is drawn with {line_style}. {Character details: head shape, facial features, posture, clothing style}. {Key prop/object} shows a single {accent_color} {accent_detail — e.g., "glowing rectangle on the screen"} — the only color in the entire illustration. {Fill approach — e.g., "The figure and laptop are drawn with outline-only style, no complex shading or fills."}. The character is positioned {placement} with {spacing description}. The style is {feel}. Square format.
```

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

### For Dark/Moody Styles:
Invert the color language:
- Base becomes the dark background
- "Light" elements become the contrast elements
- Accent color reads differently on dark — may need to adjust brightness
- Add atmospheric descriptors ("dramatic", "cinematic", "atmospheric lighting")

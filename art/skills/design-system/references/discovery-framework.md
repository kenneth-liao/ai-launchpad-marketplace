# Discovery Framework

Complete question bank for art style discovery. Present questions using the AskUserQuestion tool. Follow dimension order — each builds on previous answers.

Each dimension includes:
- The question to ask
- Options with descriptions
- Multi-select flag
- Adaptation notes (how earlier answers modify this question)
- Impact notes (what this answer determines downstream)

---

## Dimension 1: Primary Use Cases

**Question:** "What will you primarily use this art style for?"
**Multi-select:** Yes
**Options:**

| Option | Description |
|--------|-------------|
| Social media posts & ads | Instagram, Twitter/X, LinkedIn, Facebook content and paid advertising |
| Course materials & slides | Educational presentations, worksheets, diagrams, video thumbnails |
| Website & landing pages | Hero images, section illustrations, UI elements, blog graphics |
| Print materials | Business cards, flyers, posters, merchandise, packaging |

**Impact:** Determines required aspect ratios, resolution needs, and application guideline sections in the final document.

---

## Dimension 2: Overall Vibe

**Question:** "What overall vibe are you drawn to?"
**Multi-select:** Yes (max 2 — if user picks more, ask them to narrow down)
**Options:**

| Option | Description |
|--------|-------------|
| Clean & modern / minimalist | Lots of whitespace, simple shapes, restrained palette, feels premium |
| Warm & approachable / friendly | Rounded shapes, soft colors, inviting feel, human and accessible |
| Bold & energetic / dynamic | Strong contrasts, movement, high impact, grabs attention |
| Dark & sophisticated / moody | Deep backgrounds, dramatic lighting, premium and exclusive feel |

**Impact:** Sets the foundational emotional tone for all other decisions. This is the single most influential dimension.

---

## Dimension 3: Medium Preference

**Question:** "How do you feel about illustration vs. photography in your style?"
**Multi-select:** No
**Options:**

| Option | Description |
|--------|-------------|
| Mostly illustrated / stylized | Hand-drawn or digital illustrations are the primary visual language |
| Photography-forward | Real photos with consistent editing, filters, or color treatment |
| Mixed media | Illustrations layered over or combined with photography |
| Abstract / geometric | Non-representational shapes, patterns, gradients, and textures |

**Adaptations:**
- If **Photography-forward**: Skip Dimensions 4 and 8 (illustration style and line work). In Phase 4, replace illustration prompts with photo-style prompts.
- If **Abstract / geometric**: Modify Dimension 4 options to abstract-specific styles. Modify character-based prompts in Phase 4 to abstract compositions.
- If **Mixed media**: Keep all dimensions but note the hybrid approach in synthesis.

---

## Dimension 4: Illustration Style

**Question:** "Which illustration styles appeal to you?"
**Multi-select:** Yes
**Skip if:** Dimension 3 answer is "Photography-forward"
**Options:**

*Default options:*

| Option | Description |
|--------|-------------|
| Flat vector / clean digital | Crisp edges, solid fills, geometric precision, modern and polished |
| Hand-drawn / sketchy texture | Visible line work, organic imperfections, notebook or journal feel |
| 3D / isometric | Depth and dimension, rendered objects, spatial perspective |
| Collage / mixed texture | Layered elements, paper textures, cut-out aesthetic, tactile |

*If Dimension 3 is "Abstract / geometric," replace with:*

| Option | Description |
|--------|-------------|
| Geometric shapes & patterns | Clean circles, triangles, grids, mathematical precision |
| Organic abstract | Flowing forms, blobs, natural shapes, fluid movement |
| Data visualization style | Charts, graphs, networks rendered as art |
| Textural / noise-based | Grain, halftone, stipple, gradients as primary elements |

**Impact:** Directly determines the illustration guidelines, line work approach, and prompt style for all generated assets.

---

## Dimension 5: Color Strategy

**Question:** "What color direction feels right?"
**Multi-select:** No
**Options:**

| Option | Description |
|--------|-------------|
| Monochrome with one bold accent | One base tone + one pop color for highlights. Maximum contrast, minimal palette. |
| Warm earth tones | Terracotta, sage, cream, burnt orange, olive. Natural, grounded, organic. |
| Cool & professional | Blues, grays, whites, silver accents. Trustworthy, corporate, clean. |
| Full vibrant palette | Multiple bold colors used deliberately. Energetic, playful, expressive. |

**Impact:** Determines the entire color system architecture — number of colors, ratio distribution, and how accent color functions.

**Ratio defaults by strategy:**
- Monochrome + accent: 80% base / 15% ink / 5% accent
- Warm earth tones: 50% base / 35% earth tones / 15% accent
- Cool & professional: 60% base / 30% cool tones / 10% accent
- Full vibrant: 40% base / 35% primary colors / 25% secondary accents

---

## Dimension 6: Accent Color

**Question:** "Which accent color feels most like your brand?"
**Multi-select:** No
**Adapt options based on Dimension 5 answer:**

### If "Monochrome with one bold accent":

| Option | Hex | Description |
|--------|-----|-------------|
| Electric teal / cyan | #00BFA6 | Fresh, tech-forward, energetic |
| Coral / warm red | #FF6B6B | Warm, passionate, attention-grabbing |
| Electric purple / violet | #7C4DFF | Creative, premium, distinctive |
| Bright amber / gold | #FFB300 | Optimistic, warm, illuminating |

### If "Warm earth tones":

| Option | Hex | Description |
|--------|-----|-------------|
| Terracotta | #C75B39 | Grounded, natural, warm |
| Sage green | #87A878 | Calm, natural, balanced |
| Burnt orange | #CC5500 | Energetic, warm, bold |
| Deep clay | #8B4513 | Rich, earthy, sophisticated |

### If "Cool & professional":

| Option | Hex | Description |
|--------|-----|-------------|
| Ocean blue | #0077B6 | Trustworthy, calm, professional |
| Steel blue | #4682B4 | Refined, corporate, reliable |
| Mint green | #3EB489 | Fresh, clean, modern |
| Ice blue | #99D5E8 | Light, open, approachable |

### If "Full vibrant palette":

Present this as: "Pick your PRIMARY dominant accent color — we'll build the rest of the palette around it."

| Option | Hex | Description |
|--------|-----|-------------|
| Electric blue | #2979FF | Bold, trustworthy, dynamic |
| Hot pink / magenta | #FF1493 | Playful, bold, expressive |
| Lime green | #76FF03 | Energetic, fresh, youthful |
| Vivid orange | #FF6D00 | Warm, exciting, action-oriented |

**Note:** The user can always pick "Other" and specify a custom hex code. If they provide a brand color, use it.

---

## Dimension 7: Base Tone

**Question:** "What should the base/background feel like?"
**Multi-select:** No
**Options:**

| Option | Hex | Description |
|--------|-----|-------------|
| Warm cream / off-white | #FAF8F5 | Soft, warm, paper-like. Best with: minimalist, friendly, hand-drawn |
| Pure white | #FFFFFF | Crisp, clean, clinical. Best with: modern, corporate, vector |
| Light warm gray | #F0EDEA | Neutral, sophisticated, muted. Best with: professional, balanced |
| Dark charcoal | #1A1A2E | Moody, premium, dramatic. Best with: dark/sophisticated, bold, neon |

**Adaptation:** If Dimension 2 vibe is "Dark & sophisticated," default-highlight the dark charcoal option.

**Impact:** The base tone defines the canvas and fundamentally affects how every other element reads. It's the most visible single color in the system.

---

## Dimension 8: Line Work & Edges

**Question:** "What kind of line work do you prefer?"
**Multi-select:** No
**Skip if:** Dimension 3 is "Photography-forward" or "Abstract / geometric"
**Options:**

| Option | Description |
|--------|-------------|
| Thick, rounded, friendly lines | Marker or brush pen feel, approachable and warm, slightly imperfect |
| Thin, precise, clean lines | Technical pen feel, refined and sharp, consistent weight |
| Sketchy, loose, expressive | Pencil or charcoal feel, artistic and energetic, visible hand |
| No outlines / shape-based | Filled shapes only, no visible strokes, modern and flat |

**Impact:** Defines the fundamental character of all illustrated elements. This is the "handwriting" of the style — it affects every visual.

---

## Dimension 9: Composition

**Question:** "How should compositions feel?"
**Multi-select:** No
**Options:**

| Option | Description |
|--------|-------------|
| Minimal — lots of whitespace, single focal point | Maximum breathing room, clean hierarchy, one idea per image |
| Balanced & structured — grid-based, organized | Professional, systematic, predictable layouts |
| Asymmetric & dynamic — off-center, movement | Energetic, editorial feel, modern and unexpected |
| Dense & detailed — rich, layered, immersive | Complex, storytelling-driven, maximum visual information |

**Impact:** Determines placement rules, spacing guidelines, and how many elements appear in each generated asset.

---

## Dimension 10: Anti-Patterns

**Question:** "What should this style definitely NOT look like?"
**Multi-select:** Yes
**Options:**

| Option | Description |
|--------|-------------|
| Neon / glowing / cyberpunk aesthetic | No bright neons on dark backgrounds, no sci-fi grid lines |
| Corporate stock photo feel | No generic handshakes, no staged office scenes, no clip art |
| Busy, cluttered, information-dense layouts | No competing focal points, no text-heavy compositions |
| Gradients and complex color blending | No rainbow transitions, no glassmorphism, no aurora effects |

**Follow-up:** After the user selects options, ask: "Anything else you specifically want to avoid? Any brands or styles you don't want to be associated with?"

This free-text response feeds into the "What This Style Is NOT" section of the design system document.

---

## Post-Discovery Checkpoint

After all dimensions are answered, present a brief synthesis to the user before moving to Phase 2:

**Template:**
> "Based on your answers, here's the direction I'm seeing: **[2-3 sentence summary describing the emerging style as a cohesive vision — reference the key choices and how they work together]**. Does this feel right before I build out the full system?"

Wait for explicit confirmation. If the user wants to adjust any dimension, revisit just that question — don't restart the entire discovery.

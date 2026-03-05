# Nano Banana Prompt Reference

## Prompt Structure

A good prompt typically includes:
1. **Subject** - What to generate
2. **Style** - Artistic style or aesthetic
3. **Details** - Lighting, colors, composition
4. **Quality** - Resolution hints, professional quality

## Categories

### Pixel Art / 8-bit

```
Pixel art {subject}, 8-bit retro style, limited color palette, 
crisp pixels, nostalgic video game aesthetic
```

**Examples:**
```
Pixel art robot mascot, 8-bit style, blue and orange colors, 
friendly expression, transparent background

Pixel art landscape, retro video game style, sunset colors, 
16-bit era aesthetic, side-scrolling game background

Pixel art food icons, 8-bit style, bright colors, 
game UI elements, clean pixel edges
```

### Photorealistic

```
Professional photograph of {subject}, {lighting} lighting,
{lens} lens, high resolution, sharp focus, {mood}
```

**Examples:**
```
Professional product photo of wireless headphones on marble surface,
soft studio lighting, 85mm lens, high resolution, minimalist background

Portrait photograph of elderly craftsman in workshop,
natural window lighting, 50mm lens, shallow depth of field,
warm tones, documentary style

Aerial photograph of coastal city at golden hour,
drone perspective, dramatic lighting, high dynamic range
```

### Digital Art / Illustration

```
Digital illustration of {subject}, {style} style,
{colors} color palette, {mood} atmosphere
```

**Examples:**
```
Digital illustration of enchanted forest, fantasy art style,
purple and teal color palette, mystical atmosphere,
detailed foliage, magical creatures

Character concept art, cyberpunk style, neon lighting,
futuristic armor design, dynamic pose, professional quality

Children's book illustration, whimsical style, pastel colors,
friendly animals in meadow, soft edges, storybook quality
```

### Minimalist / Flat Design

```
Minimalist {subject}, flat design, {colors}, 
clean lines, simple shapes, modern aesthetic
```

**Examples:**
```
Minimalist logo design, geometric mountain shape,
blue gradient, flat design, vector style, clean edges

Minimalist app icon, flat design, single color,
simple shape, rounded corners, iOS style

Minimalist infographic elements, flat icons,
corporate blue palette, clean vector style
```

### 3D / Isometric

```
3D render of {subject}, isometric view, {style},
soft shadows, {colors}, clean background
```

**Examples:**
```
3D isometric office workspace, low poly style,
pastel colors, soft shadows, cute aesthetic

3D render of floating island, isometric perspective,
fantasy environment, vibrant colors, game asset style

Isometric city block, architectural visualization,
modern buildings, clean lines, professional render
```

### Abstract / Artistic

```
Abstract {subject}, {style} style, {colors},
{texture}, artistic composition
```

**Examples:**
```
Abstract fluid art, vibrant colors, marble texture,
flowing shapes, high contrast, contemporary style

Abstract geometric pattern, bauhaus style,
primary colors, sharp edges, modernist aesthetic

Abstract landscape, impressionist style,
soft brushstrokes, dreamy atmosphere, oil painting texture
```

## Model-Specific Prompting Tips

### Pro Model (`--model pro`, default)
- Handles long, detailed narrative prompts well
- Better at rendering text within images
- Excels at complex multi-element compositions
- Supports thinking mode — may reason about composition internally
- Best for: final production images, text-heavy designs, detailed scenes

### Flash Model (`--model flash`)
- Prefers concise, focused prompts (1-2 sentences)
- Faster generation, good for rapid iteration
- Works well for simple subjects and styles
- Less reliable with text rendering
- Best for: exploration, drafts, high-volume batch generation

**Example — same concept, different model styles:**
```
# Pro prompt (detailed):
"Professional product photograph of wireless headphones on marble surface,
soft studio lighting, 85mm lens, high resolution, minimalist white background,
subtle shadow, commercial grade quality"

# Flash prompt (concise):
"Wireless headphones on marble, studio lighting, minimalist product photo"
```

## Multi-Image Reference Prompting

When providing multiple reference images (`-i ref1.png ref2.png ...`), the prompt should describe how to use them:

### Style Transfer
```bash
python generate.py "apply the style of the first image to the subject in the second image" \
  -i style_ref.png subject_photo.jpg -o styled.png
```

### Brand Consistency
```bash
python generate.py "create a new banner using the same color palette and visual style as these brand images" \
  -i brand1.png brand2.png brand3.png --ratio 16:9 -o banner.png
```

### Subject Consistency
```bash
python generate.py "show this character in a different pose, outdoor setting" \
  -i character_front.png character_side.png -o character_outdoor.png
```

### Composite / Merge
```bash
python generate.py "combine elements from both images into a cohesive scene" \
  -i scene_a.png scene_b.png -o composite.png
```

**Tips for multi-reference prompts:**
- Reference images by order: "the first image", "the second image"
- Be explicit about what to take from each reference
- Up to 14 reference images supported, but 2-4 is typical

## Aspect Ratio Guidelines

| Ratio | Use Case | Example Prompt Suffix |
|-------|----------|----------------------|
| 1:1 | Icons, avatars, social posts | "square format, centered composition" |
| 16:9 | Banners, YouTube thumbnails | "wide format, horizontal composition" |
| 9:16 | Phone wallpapers, stories | "vertical format, portrait orientation" |
| 21:9 | Cinematic, ultra-wide | "cinematic aspect ratio, panoramic view" |
| 4:3 | Presentations, traditional | "standard format, classic composition" |
| 2:3 | Portrait photos | "portrait orientation, full body framing" |

### Downstream Use Case Quick Reference

| Use Case | Ratio | Size | Notes |
|----------|-------|------|-------|
| YouTube thumbnail | 16:9 | 2K+ | Bold text, high contrast, face close-ups work best |
| Instagram post | 1:1 | 2K | Clean composition, vibrant colors |
| Instagram story | 9:16 | 2K | Vertical, leave space for text overlays |
| Newsletter header | 16:9 or 21:9 | 2K | Wide, atmospheric, avoid small details |
| Logo / icon | 1:1 | 2K | Simple, centered, works at small sizes |
| Blog hero image | 16:9 | 4K | Detailed, room for text overlay on edges |
| Phone wallpaper | 9:16 | 4K | Detailed, avoid clutter in status bar area |

## Quality Modifiers

**Resolution hints:**
- "high resolution"
- "4K quality"
- "ultra detailed"
- "sharp focus"
- "crisp details"

**Professional quality:**
- "professional photograph"
- "studio quality"
- "commercial grade"
- "publication ready"
- "award winning"

**Style consistency:**
- "consistent style"
- "cohesive aesthetic"
- "unified color palette"
- "matching visual language"

## Negative Concepts

To avoid unwanted elements, describe what you want clearly:

Instead of: "no text"
Use: "clean image without text, pure visual"

Instead of: "no people"
Use: "empty scene, unpopulated environment"

Instead of: "not blurry"
Use: "sharp focus, crisp details, high clarity"

## Batch Generation Tips

When generating multiple variations:

1. **Keep core prompt consistent** - Same subject and style
2. **Vary specific details** - Colors, poses, backgrounds
3. **Use numbered batches** - Track which prompts work best
4. **Iterate on winners** - Refine prompts that produce good results

**Example batch workflow:**
```bash
# Round 1: Explore styles
"pixel art robot, 8-bit style, blue colors"
"pixel art robot, retro game style, warm colors"
"pixel art robot, modern pixel art, neon colors"

# Round 2: Refine best style
"pixel art robot, 8-bit style, blue and silver colors, friendly expression"
"pixel art robot, 8-bit style, blue and gold colors, heroic pose"
```

## Sequential Generation Prompts

Prompt templates for maintaining visual consistency across a series of images using the `-i` reference flag.

### Style-Board Anchor Prompts

Generate the anchor image that establishes the visual identity for a series:

```
{style} style, {color palette} color palette, {lighting} lighting,
{mood} atmosphere, {texture/detail level}, cohesive visual identity
```

**Examples:**
```
Modern flat illustration, warm earth tones and muted pastels,
soft ambient lighting, cozy inviting atmosphere, clean lines with
subtle gradients, cohesive visual identity

Dark moody photography style, deep blues and amber highlights,
dramatic side lighting, cinematic atmosphere, high contrast with
film grain, cohesive visual identity
```

### Referencing an Anchor

When generating subsequent images that reference the anchor:

```
{subject description}, matching the visual style, color palette,
and lighting of the reference image exactly
```

**Key phrasing patterns:**
- "matching the visual style of the reference image exactly"
- "using the same color palette and artistic style as the reference"
- "in the same style as the first image, with identical lighting and color treatment"

**Be explicit about what to preserve vs. change:**
```
# Good — clear about what changes and what stays
"a mountain landscape at sunset, using the exact same illustration style,
color palette, and line weight as the reference image"

# Bad — ambiguous about style preservation
"a mountain landscape at sunset, similar to the reference"
```

### Subject Consistency Prompts

Establish the subject with detailed, reusable appearance description:

```
{subject} with {distinguishing features}, {colors/materials},
{proportions}, {expression/pose}, on {simple background}
```

Reference the subject in new scenes:

```
the same {subject} from the reference image, now {new action/pose},
same proportions and colors, {new background/setting}
```

**Tip:** Include "same proportions and colors" explicitly — without it, the model may drift on physical attributes across scenes.

### A/B Variant Prompts

Generate multiple compositions sharing the same style for split-testing:

```bash
# Variant A: Close-up with text space on right
uv run generate.py "close-up portrait composition with negative space on the right, \
  matching the style of the reference image" -i anchor.png -o variant_a.png

# Variant B: Wide shot with centered subject
uv run generate.py "wide shot with centered subject and blurred background, \
  matching the style of the reference image" -i anchor.png -o variant_b.png

# Variant C: Dynamic angle with high energy
uv run generate.py "dynamic low-angle shot with dramatic perspective, \
  matching the style of the reference image" -i anchor.png -o variant_c.png
```

### Newsletter Series Prompts

Generate a set of visuals for a single newsletter issue with consistent styling:

```bash
# Anchor: Establish the issue's visual identity
uv run generate.py "minimalist tech illustration, teal and coral accents, \
  clean vector style, light gray background, cohesive identity" \
  --model pro -o newsletter_anchor.png

# Hero image
uv run generate.py "wide banner showing AI workflow automation concept, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 21:9 -o hero.png

# Section illustration 1
uv run generate.py "person collaborating with AI assistant on laptop, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 16:9 -o section_1.png

# Section illustration 2
uv run generate.py "abstract data flow visualization, \
  matching the style of the reference image exactly" \
  -i newsletter_anchor.png --ratio 16:9 -o section_2.png
```

### Sequential Prompting Tips

1. **Reference ordering matters** — Put the style anchor as the first `-i` argument. The model gives slightly more weight to earlier references.

2. **Be specific about preservation** — "matching the visual style" is okay; "matching the visual style, color palette, lighting, and line weight" is better.

3. **Describe what changes, not just what stays** — The model handles conflicting signals better when you clearly separate "keep X" from "change Y."

4. **Cap your reference pool** — 3-4 images is the sweet spot. Beyond that, the model averages too many inputs and the result loses character.

5. **Use consistent terminology** — If you called it "warm earth tones" in the anchor prompt, use "warm earth tones" (not "natural colors") in follow-up prompts.

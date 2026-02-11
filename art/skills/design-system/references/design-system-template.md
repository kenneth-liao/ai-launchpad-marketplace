# Design System Template

Fill all `{{placeholder}}` values based on discovery answers and synthesis. Remove ALL template instructions (lines starting with `>`) and all `{{placeholder}}` markers before saving the final document. The output must read as a polished, self-contained style guide.

---

## Output Document Structure

```markdown
# {{Project Name}} — Art Style System

## Style Name: "{{Style Name}}"

{{Overview paragraph: 2-3 sentences describing the overall aesthetic. What does it feel like? What core tension or combination makes it distinctive? What experience should someone have when seeing visuals in this style?}}

---

## Core Principles

> Define 3-4 principles. Each is a short imperative phrase + explanation.
> Principles should collectively cover: the dominant texture/feel, use of space, color strategy, and emotional tone.
> Write as if these are rules a designer must follow.

1. **{{Principle 1 title}}.** {{What this means in practice — actionable, specific}}
2. **{{Principle 2 title}}.** {{What this means in practice — actionable, specific}}
3. **{{Principle 3 title}}.** {{What this means in practice — actionable, specific}}
4. **{{Principle 4 title}}.** {{What this means in practice — actionable, specific}}

---

## Color Palette

| Role | Color | Hex | AI Description | Usage |
|------|-------|-----|----------------|-------|
| Base | {{Base color name}} | `{{#hex}}` | {{Natural language — e.g., "warm cream like aged linen paper"}} | Backgrounds, canvas, negative space |
| Primary Ink | {{Primary color name}} | `{{#hex}}` | {{Natural language — e.g., "deep charcoal like soft pencil lead"}} | Primary line work, text, headings |
| Secondary Ink | {{Secondary color name}} | `{{#hex}}` | {{Natural language — e.g., "dusty warm gray like weathered stone"}} | Secondary details, captions, annotations |
| Light / Subtle | {{Subtle color name}} | `{{#hex}}` | {{Natural language — e.g., "barely-there gray like faint pencil smudge"}} | Background elements, texture, dividers |
| Accent | {{Accent color name}} | `{{#hex}}` | {{Natural language — e.g., "vivid electric teal like tropical water"}} | Highlights, CTAs, key focal elements |
| Accent Dark | {{Accent dark name}} | `{{#hex}}` | {{Natural language — e.g., "deep saturated teal like ocean depth"}} | Hover states, emphasis, depth |

> Color naming guide by strategy:
> - Monochrome + accent: Use "Ink" terminology (Primary Ink, Secondary Ink)
> - Earth tones: Use natural names (Clay, Sage, Stone, Sand)
> - Cool & professional: Use material names (Steel, Slate, Ice, Silver)
> - Full vibrant: Use energy names (Primary, Secondary, Tertiary, Pop)
>
> Accent Dark should be a darker shade of the Accent color (reduce lightness by ~15-20%).
> Light/Subtle should be a very muted version between Base and Primary Ink.
>
> AI Description guide: Write each color description as a human would perceive it — a sensory,
> evocative phrase that an AI image generator can interpret. Use material/nature metaphors
> ("like aged paper", "like wet ink", "like morning fog"). These descriptions are used directly
> in image generation prompts alongside hex codes for maximum accuracy.

### Color Ratios

> Use the ratio defaults from the discovery framework, adjusted to the specific style:

- **{{X}}%** {{Base/whitespace description}}
- **{{Y}}%** {{Primary + secondary work description}}
- **{{Z}}%** {{Accent color description}}

---

## Style Language Map

> This section translates every technical specification into natural language for AI image generation.
> When constructing prompts, use these descriptions instead of (or alongside) raw values.
> Every entry must be filled — this is the bridge between the design system and consistent AI output.
>
> Populate each row by converting the technical spec into a sensory, descriptive phrase.
> These exact phrases should be copy-pasted into prompts for consistency.

| Attribute | Technical Value | Prompt Language |
|-----------|----------------|-----------------|
| Base color | `{{#hex}}` | "{{evocative description — e.g., warm cream like handmade paper}}" |
| Primary ink | `{{#hex}}` | "{{e.g., deep charcoal like soft 6B pencil}}" |
| Secondary ink | `{{#hex}}` | "{{e.g., muted warm gray like graphite smudge}}" |
| Light tone | `{{#hex}}` | "{{e.g., whisper-light gray like erased pencil marks}}" |
| Accent color | `{{#hex}}` | "{{e.g., vivid electric teal like backlit glass}}" |
| Accent dark | `{{#hex}}` | "{{e.g., deep saturated teal like ocean at dusk}}" |
| Line style | {{weight + quality}} | "{{tool metaphor — e.g., drawn with a thick felt-tip brush pen, slightly uneven like real hand strokes}}" |
| Edge treatment | {{corners + endings}} | "{{e.g., soft rounded corners with tapered line endings, nothing sharp or mechanical}}" |
| Fill approach | {{fill method}} | "{{e.g., clean flat fills with no gradients or shading, like paper cut-outs}}" |
| Texture quality | {{surface feel}} | "{{e.g., subtle paper grain texture, like a premium Moleskine page}}" |
| Composition | {{spatial approach}} | "{{e.g., centered with vast breathing room, like a single thought on an empty page}}" |
| Overall mood | {{emotional tone}} | "{{e.g., warm, approachable, and quietly confident — like a handwritten note from a friend}}" |

> When writing prompts, use the **Prompt Language** column verbatim. This ensures every generated
> image shares identical style descriptions, which is the single biggest driver of visual consistency
> across AI-generated assets.

---

## Line Work

> Skip this entire section if medium is "Photography-forward" or "Abstract / geometric"

- **Weight:** {{Stroke weight description + tool metaphor (e.g., "thick brush pen", "fine technical pen")}}
- **Corners:** {{Corner treatment — rounded/sharp/mixed and when each applies}}
- **Edges:** {{Edge quality — perfect/organic/sketchy with specific description}}
- **Line endings:** {{Cap style — rounded/flat/tapered}}
- **Consistency:** {{How primary subjects vs secondary/background elements differ in line treatment}}

---

## Illustration Style

> Adapt section titles and content based on medium preference.
> For Photography-forward: Replace with "Photography Treatment" covering filters, color grading, crop style.
> For Abstract/geometric: Replace with "Shape Language" covering shape types, arrangement, negative space.

### Characters (if used)
- {{Proportion and body style description}}
- {{Facial detail level — dot eyes, detailed features, no faces, etc.}}
- {{Fill vs outline approach for characters}}
- {{How accent color appears on characters — one element only, glow, fill, etc.}}

### Objects & Icons
- {{Drawing/rendering style description}}
- {{Outline weight and approach}}
- {{Fill approach — solid, gradient, none, textured}}
- {{Accent color usage rule for objects}}

### Backgrounds
- {{Base canvas description}}
- {{Optional texture and its opacity (be specific: "10% opacity grid lines")}}
- {{Complexity rule — what's allowed and what's too much}}

---

## Character System

> This section defines a reusable character specification so that every character generated
> across different assets, sessions, and prompts maintains a consistent look.
> Skip this section only if the style is Abstract/geometric with no characters.
>
> The character system should be derived from the illustration style, line work, and vibe
> choices during discovery. Synthesize a coherent character that embodies the brand aesthetic.

### Character Archetype

- **Type:** {{Character type — e.g., "simplified human figure", "rounded robot mascot", "abstract geometric figure", "stylized animal"}}
- **Personality:** {{1-2 sentence personality description that informs pose and expression — e.g., "curious and optimistic, always leaning forward or reaching toward something"}}

### Proportions

- **Head-to-body ratio:** {{e.g., "1:3 (large head, compact body) for friendly appeal" or "1:5 (realistic proportions) for professional tone"}}
- **Body shape:** {{e.g., "rounded, bean-shaped torso" or "geometric, rectangular build" or "simple stick-figure limbs with circular joints"}}
- **Limb style:** {{e.g., "thick rounded arms, no visible hands — ends in simple curves" or "thin line limbs with dot joints"}}
- **Overall scale:** {{e.g., "compact and sticker-like, fits in a circle" or "tall and narrow, vertical emphasis"}}

### Facial Features

- **Detail level:** {{e.g., "minimal — two dot eyes, no mouth" or "simple — dot eyes, curved smile line" or "moderate — eyes, small nose, expressive mouth"}}
- **Expression range:** {{e.g., "neutral to gently happy — no extreme expressions" or "wide range — surprise, delight, focus, curiosity"}}
- **Identifying marks:** {{e.g., "none" or "small round glasses" or "antenna on head" or "distinctive hair tuft"}}

### Consistent Identifiers

> These elements MUST appear on the character in every generation to maintain identity.
> Choose 2-3 identifiers that are simple enough for AI to reproduce reliably.

- **Identifier 1:** {{e.g., "always wears a small {{accent_color}} scarf/bandana"}}
- **Identifier 2:** {{e.g., "has a circular head with two antenna dots"}}
- **Identifier 3:** {{e.g., "carries a small {{accent_color}} object (book, tool, etc.)"}}

### Accent Color on Characters

- **Rule:** {{How accent color appears on the character — e.g., "exactly ONE element on the character is {{accent_color}} — this is the scarf/bandana. No other accent color on the character."}}
- **Forbidden:** {{What NOT to do — e.g., "Never color the entire character in accent. Never use accent on both clothing AND accessories."}}

### Fidelity Levels

> Define how the character simplifies or elaborates at different sizes/contexts.

| Level | When Used | Description |
|-------|-----------|-------------|
| Hero | Large, featured illustrations (style board, hero images) | {{Full detail — all identifiers present, clear facial features, complete body}} |
| Standard | Medium context (social posts, diagrams, scenes) | {{Moderate detail — key identifiers present, simplified features}} |
| Spot | Small or supporting roles (icons, pattern elements, backgrounds) | {{Minimal — recognizable silhouette only, 1 identifier, basic shape}} |

### Character Prompt Fragment

> This is a reusable text block to copy-paste into any prompt that includes the character.
> It should be a single paragraph that can be inserted after the subject declaration.

```
{{Full character description paragraph — combine archetype, proportions, facial features,
identifiers, and accent rule into a single cohesive paragraph. Example:
"The character is a small, rounded robot with a 1:3 head-to-body ratio and a bean-shaped
torso. Its head is a perfect circle with two simple dot eyes and no mouth. It has thick,
rounded arms that end in simple curves — no visible hands. The robot always wears a small
electric teal (#00BFA6) scarf, which is the only accent color on the character. Its body is
drawn in charcoal (#2D2D2D) outline-only style with the same thick brush pen strokes used
throughout the design system. The overall feel is compact and friendly, like a character
from a premium notebook margin sketch."}}
```

---

## Typography Direction

- **Headlines:** {{Font style description + 2-3 example font names in parentheses}}
- **Body:** {{Font style description + 2-3 example font names}}
- **Accent text:** {{Special treatment — hand-lettered, colored, etc. or "same as body"}}
- **Hierarchy:** {{How hierarchy is created — through size, weight, color, or combination. Be specific about what's allowed and what's not.}}

> Typography mapping by vibe:
> - Clean & modern: Geometric sans (Inter, DM Sans, Manrope) + clean display (Outfit, Sora)
> - Warm & friendly: Rounded sans (Nunito, Quicksand, Poppins) + soft display (Fredoka, Baloo)
> - Bold & energetic: Strong sans (Montserrat, Raleway, Archivo) + impactful display (Bebas, Oswald)
> - Dark & sophisticated: Elegant serif/sans (Playfair, Cormorant) + refined body (Source Sans, Lato)

---

## Composition Rules

> Define 4-5 rules. Each should be a named principle with explanation.
> Rules should cover: focal point strategy, placement/alignment, margins/spacing, secondary element treatment, and accent color as compositional tool.

1. **{{Rule 1 name}}.** {{Description — what to do and why}}
2. **{{Rule 2 name}}.** {{Description — what to do and why}}
3. **{{Rule 3 name}}.** {{Description — what to do and why}}
4. **{{Rule 4 name}}.** {{Description — what to do and why}}
5. **{{Rule 5 name}}.** {{Description — what to do and why}}

---

## Application Guidelines

> Include one subsection per use case selected in Discovery Dimension 1.
> Each subsection should be 4 bullet points covering background, content, accent usage, and spacing.

### {{Use Case 1}}
- {{Background approach for this format}}
- {{Content / illustration approach}}
- {{Accent color usage}}
- {{Spacing / layout notes specific to this format}}

### {{Use Case 2}}
- {{Background approach}}
- {{Content approach}}
- {{Accent usage}}
- {{Spacing notes}}

> Add more subsections as needed for each selected use case.

---

## What This Style Is NOT

> Convert anti-patterns from Dimension 10 plus any that logically conflict with chosen directions.
> Format as a bulleted list with specific descriptions.
> Aim for 5-7 items.

- {{Anti-pattern 1 with brief explanation}}
- {{Anti-pattern 2 with brief explanation}}
- {{Anti-pattern 3 with brief explanation}}
- {{Anti-pattern 4 with brief explanation}}
- {{Anti-pattern 5 with brief explanation}}
- {{Anti-pattern 6 with brief explanation}}

---

## Nano Banana Prompt Library

> Generate 8 prompts. Each MUST be a single descriptive narrative paragraph that:
> - Names the subject in the first sentence
> - Specifies the exact background color with hex code
> - Describes the artistic style and tool metaphor matching the Line Work section
> - Constrains accent color usage to one element with hex code
> - Describes composition matching the Composition Rules
> - Ends with aspect ratio specification
> - States what to exclude (no text, no gradients, etc.)
>
> Use the parameterized templates from prompt-engineering.md as starting points,
> then customize to this specific design system.

### 1. Hero Character / Mascot

` ` `
{{Full narrative prompt — 4-6 sentences, single paragraph}}
` ` `

### 2. Concept Icon

` ` `
{{Full narrative prompt}}
` ` `

### 3. Framework Diagram

` ` `
{{Full narrative prompt}}
` ` `

### 4. Social Media Asset

` ` `
{{Full narrative prompt}}
` ` `

### 5. Background / Texture

` ` `
{{Full narrative prompt}}
` ` `

### 6. Sticker / Badge Element

` ` `
{{Full narrative prompt}}
` ` `

### 7. Pattern Element

` ` `
{{Full narrative prompt}}
` ` `

### 8. Character Scene

` ` `
{{Full narrative prompt}}
` ` `

---

## Style Board Layout

> Adapt this layout to use the actual style name and match the elements generated.

` ` `
┌─────────────────────────────────────────────┐
│                                             │
│   "{{STYLE NAME}}"       [Color Swatches]   │
│   Art Style System        ■ ■ ■ ■ ■ ■      │
│                                             │
├──────────────────┬──────────────────────────┤
│                  │                          │
│   01 Hero        │   02 Concept Icon +      │
│   Character      │   04 Social Asset        │
│                  │                          │
├──────────────────┼──────────────────────────┤
│                  │                          │
│   03 Framework   │   08 Character           │
│   Diagram        │   Scene                  │
│                  │                          │
├──────────────────┴──────────────────────────┤
│                                             │
│   05 Background       07 Pattern Element    │
│   + 06 Sticker/Badge                        │
│                                             │
└─────────────────────────────────────────────┘
` ` `

Each cell showcases a different application of the style, demonstrating consistency across use cases while the overall board proves the system works as a cohesive visual language.
```

---

## Reference Library

> The 8 generated style board images serve as canonical style references for all future asset creation.
> When generating new images in this style, provide the relevant reference image(s) to the AI tool
> to anchor visual consistency beyond what text prompts alone can achieve.

### Reference Image Index

| File | Use As Reference When... | Key Style Anchors It Provides |
|------|--------------------------|-------------------------------|
| `01-hero-character.png` | Creating any character, mascot, or figure | Character proportions, line weight, accent placement on characters, fill approach |
| `02-concept-icon.png` | Creating icons, symbols, or single-object illustrations | Icon scale, stroke consistency, accent color treatment, negative space usage |
| `03-framework-diagram.png` | Creating diagrams, flows, infographics, or connected elements | Connector style, node rendering, layout spacing, annotation treatment |
| `04-social-media-asset.png` | Creating social content, thumbnails, or standalone visuals | Composition for square format, visual impact at small sizes, color balance |
| `05-background-texture.png` | Creating backgrounds, textures, or ambient visuals | Texture density, background subtlety, how elements sit against the base color |
| `06-sticker-badge.png` | Creating badges, stamps, compact UI elements, or decorative accents | Compact composition, transparency treatment, accent framing style |
| `07-pattern-element.png` | Creating repeating patterns, decorative borders, or scattered elements | Element density, doodle complexity, spacing rhythm, secondary color usage |
| `08-character-scene.png` | Creating scene illustrations, contextual images, or storytelling visuals | Character-in-context rendering, prop style, scene composition, environmental detail level |

### How to Use References

When generating new assets:
1. **Identify the closest reference** from the index above based on what you're creating
2. **Provide it as a style reference image** to the AI generation tool alongside the text prompt
3. **Use 1-2 references max** per generation — too many references dilute the style signal
4. **Always pair with the text prompt** from the Style Language Map — references and text work together, neither alone is sufficient
5. **For new element types** not in the index, use the 2 references that share the most visual properties with what you're creating

### Extending the Library

When new assets are generated that represent a style not yet covered:
- Save them to the `design-system/` directory with a descriptive filename
- Add an entry to this reference index
- Note what style anchors the new reference provides

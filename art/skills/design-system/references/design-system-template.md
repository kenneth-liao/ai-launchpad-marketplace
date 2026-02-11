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

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Base | {{Base color name}} | `{{#hex}}` | Backgrounds, canvas, negative space |
| Primary Ink | {{Primary color name}} | `{{#hex}}` | Primary line work, text, headings |
| Secondary Ink | {{Secondary color name}} | `{{#hex}}` | Secondary details, captions, annotations |
| Light / Subtle | {{Subtle color name}} | `{{#hex}}` | Background elements, texture, dividers |
| Accent | {{Accent color name}} | `{{#hex}}` | Highlights, CTAs, key focal elements |
| Accent Dark | {{Accent dark name}} | `{{#hex}}` | Hover states, emphasis, depth |

> Color naming guide by strategy:
> - Monochrome + accent: Use "Ink" terminology (Primary Ink, Secondary Ink)
> - Earth tones: Use natural names (Clay, Sage, Stone, Sand)
> - Cool & professional: Use material names (Steel, Slate, Ice, Silver)
> - Full vibrant: Use energy names (Primary, Secondary, Tertiary, Pop)
>
> Accent Dark should be a darker shade of the Accent color (reduce lightness by ~15-20%).
> Light/Subtle should be a very muted version between Base and Primary Ink.

### Color Ratios

> Use the ratio defaults from the discovery framework, adjusted to the specific style:

- **{{X}}%** {{Base/whitespace description}}
- **{{Y}}%** {{Primary + secondary work description}}
- **{{Z}}%** {{Accent color description}}

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

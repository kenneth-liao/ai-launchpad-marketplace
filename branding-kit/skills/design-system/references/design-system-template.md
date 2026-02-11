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
| Print process | {{if printmaking style — overprint, registration, ink transfer}} | "{{e.g., the teal is a second-color overprint, slightly misregistered from the charcoal layer for printing authenticity}}" |
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
>
> **Character system types:**
> - **Solo:** One primary character (mascot, figure, creature)
> - **Duo / Companion:** A primary character + a smaller companion character. The two have
>   a relationship that tells the brand story (e.g., builder + AI assistant, explorer + guide).
>   Each character has separate rules for appearance, accent color, and behavior.
> - **Cast:** 3+ distinct characters that share a visual system but have unique identifiers.
>
> Ask the user during discovery: "Should your brand have one character, a character with a
> companion/sidekick, or a small cast of characters?" Then adapt this section accordingly.

### Character Archetype

- **Type:** {{Character type — e.g., "simplified human figure", "rounded robot mascot", "abstract geometric figure", "stylized animal"}}
- **Personality:** {{1-2 sentence personality description that informs pose and expression — e.g., "curious and optimistic, always leaning forward or reaching toward something"}}
- **System type:** {{Solo / Duo / Cast — if Duo or Cast, describe the relationship between characters}}

### Proportions

- **Head-to-body ratio:** {{e.g., "1:3 (large head, compact body) for friendly appeal" or "1:5 (realistic proportions) for professional tone"}}
- **Body shape:** {{e.g., "rounded, bean-shaped torso" or "geometric, rectangular build" or "simple stick-figure limbs with circular joints"}}
- **Limb style:** {{e.g., "thick rounded arms, no visible hands — ends in simple curves" or "thin line limbs with dot joints"}}
- **Overall scale:** {{e.g., "compact and sticker-like, fits in a circle" or "tall and narrow, vertical emphasis"}}

### Facial Features — STRICT RULES

> **CRITICAL:** AI image generators frequently add unwanted facial features to simplified
> characters, especially noses, eyebrows, and ears. You MUST define both what IS present
> and what is FORBIDDEN. The forbidden list must be explicit and repeated in every prompt.

- **ONLY these features:** {{List EXACTLY what appears on the face — e.g., "two small dot eyes and a small curved-line smile"}}
- **ABSOLUTELY FORBIDDEN:** {{List every feature that must NOT appear — e.g., "No nose. No eyebrows. No ears. No hair. No eyelashes. No nostrils. No cheek marks. No freckles. No additional facial features of ANY kind."}}
- **Enforcement language:** Always include this prohibition in EVERY prompt containing the character. State what IS there first, then what is NOT: "The face has ONLY [features] — absolutely NO [forbidden features]"
- **Expression range:** {{e.g., "neutral to gently happy — expression communicated through posture, not facial complexity"}}
- **Identifying marks:** {{e.g., "none on the face — identity comes from body shape and accessories"}}

### Consistent Identifiers

> These elements MUST appear on the character in every generation to maintain identity.
> Choose 2-3 identifiers that are simple enough for AI to reproduce reliably.

- **Identifier 1:** {{e.g., "always wears a baseball cap — the brim creates a distinctive silhouette"}}
- **Identifier 2:** {{e.g., "forward-leaning posture — always engaged, never passive"}}
- **Identifier 3:** {{e.g., "outline-only body with cream interior showing through"}}

### Accent Color on Characters

- **Rule:** {{How accent color appears — e.g., "NO accent color on the primary character. The accent color lives entirely on the companion character."}}
- **Forbidden:** {{What NOT to do — e.g., "Never color the entire character in accent. Never use accent on both the character AND the companion."}}

> **For Duo/Companion systems:** Define accent rules for EACH character separately.
> Typically, the accent color lives on only one of the two characters (usually the companion),
> creating a clear visual hierarchy and making the accent color's role specific.

### Companion Character (if Duo system)

> Skip this subsection for Solo character systems.
> For Duo systems, define the companion with the same rigor as the primary character.

- **Concept:** {{What the companion represents — e.g., "the AI assistant", "the creative spark", "the guide"}}
- **Appearance:** {{Shape, size relative to primary, color, facial features}}
- **Accent color rule:** {{How the accent color lives on this character — e.g., "The companion IS the accent color — a solid teal orb"}}
- **Facial features:** {{Same strict rules as primary — list what IS and what is FORBIDDEN}}

#### Companion States

> Define how the companion's position/behavior changes to communicate different moods or contexts.
> This creates a visual vocabulary where the companion's state tells the viewer what kind of
> content they're looking at, without needing words.

| State | Companion Position/Behavior | When To Use |
|-------|---------------------------|-------------|
| {{State 1}} | {{Position and visual treatment}} | {{Content context}} |
| {{State 2}} | {{Position and visual treatment}} | {{Content context}} |
| {{State 3}} | {{Position and visual treatment}} | {{Content context}} |
| {{State 4}} | {{Position and visual treatment}} | {{Content context}} |

> Aim for 4-6 states. Each state should be visually distinct enough to read at small sizes.
> Common state dimensions: position relative to primary character, size/brightness,
> motion indicators (trail lines, radiating lines), emotional energy level.

### Fidelity Levels

> Define how characters simplify or elaborate at different sizes/contexts.
> For Duo systems, define fidelity for BOTH characters.

| Level | When Used | Primary Character | Companion (if Duo) |
|-------|-----------|-------------------|-------------------|
| Hero | Large, featured illustrations | {{Full detail — all identifiers present}} | {{Full detail — shape, eyes, glow/state indicators}} |
| Standard | Medium context (social, diagrams) | {{Moderate — key identifiers, simplified body}} | {{Solid shape with eyes, minimal state indicators}} |
| Spot | Small/supporting (icons, patterns) | {{Minimal — recognizable silhouette only}} | {{A single accent-colored dot}} |

### Character Prompt Fragments

> These are reusable text blocks to copy-paste into any prompt that includes the characters.
> Each should be a single paragraph. For Duo systems, provide separate fragments that can
> be combined or used independently.
>
> **CRITICAL:** Include the facial feature prohibition in EVERY fragment.
> The pattern is: "ONLY [features] — absolutely NO [forbidden list]"

#### Primary Character (full prompt fragment)

```
{{Full character description paragraph — combine archetype, proportions, facial features
(including FORBIDDEN list), identifiers, accent rule, and style rendering into one paragraph.}}
```

#### Companion Character (full prompt fragment — Duo systems only)

```
{{Full companion description paragraph — shape, size, color, facial features (including
FORBIDDEN list), relationship to primary character, and accent color rule.}}
```

#### Combined (short version for tight prompts)

```
{{A 2-3 sentence condensed version containing both characters. Must still include the
facial feature prohibition. Example: "A character wearing a baseball cap (round head,
dot eyes, curved smile only — NO nose NO eyebrows NO ears) with a bean body in charcoal
linocut style. A small teal glowing orb companion with tiny dot eyes floats nearby —
the ONLY teal in the image."}}
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

## Consistency Enforcement

> This section documents known AI generation pitfalls and provides explicit rules to prevent them.
> It should be populated based on issues encountered during Phase 4 asset generation AND
> any known common problems for the chosen style.

### Unwanted Feature Prevention

> AI generators frequently add unwanted details to simplified characters (especially noses,
> eyebrows, ears, and hair). Document the specific prohibition rules here so every future
> prompt can reference them.

1. **Always include the explicit prohibition** in every prompt: "{{forbidden features list from Facial Features section}}"
2. **State what IS there first, then what is NOT:** "The face has ONLY {{allowed features}} — absolutely NO {{forbidden features}}"
3. **Use reference images** from the Reference Library that show the correct level of detail
4. **When providing multiple reference images**, always include at least one close-up character reference to anchor the facial detail level

### Style Drift Prevention

> Document the specific keywords and phrases that anchor the chosen style.
> These must appear in every prompt to prevent the style from drifting toward generic defaults.

1. **Always provide 1-2 reference images** from the Reference Library alongside text prompts
2. **Required style keywords in every prompt:** {{List 2-3 keywords that anchor the style — e.g., "linocut" and "carved" for printmaking, or "brush pen" and "sketch" for hand-drawn}}
3. **Required texture phrase:** {{The texture description from Style Language Map that must appear in every prompt}}
4. **Forbidden style language:** {{Words to NEVER use because they pull toward the wrong style — e.g., for printmaking: never say "drawn" or "sketch", always say "carved" or "printed"}}
5. **Required process phrase (if printmaking):** {{e.g., "second-color overprint slightly misregistered" for every accent element}}

### Character Consistency Checklist

> A verification checklist for every generated image. Run through this before finalizing.

- [ ] {{Identifier 1 check — e.g., "Character has baseball cap with visible brim"}}
- [ ] {{Facial features check — e.g., "Face has ONLY dot eyes + curved smile (no nose, no eyebrows, no ears)"}}
- [ ] {{Body style check — e.g., "Body is outline-only with cream interior"}}
- [ ] {{Posture check — e.g., "Posture is forward-leaning / active"}}
- [ ] {{Companion check (if Duo) — e.g., "Companion is present and is the ONLY accent-colored element"}}
- [ ] {{Accent color check — e.g., "No accent color appears anywhere except on the companion"}}
- [ ] {{Style texture check — e.g., "Style texture is visible (carved edges, ink grain, etc.)"}}
- [ ] {{Composition check — e.g., "Generous whitespace surrounds the composition"}}

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

### User-Provided References

> Include this subsection only if Phase 0 collected user reference images.
> List each reference with a brief note on what style properties it anchors.
> These are stored in `design-system/references/` and serve as supplementary style anchors.

| File | Source | Key Style Properties |
|------|--------|---------------------|
| `references/ref-01-{{description}}.png` | {{Where it came from — e.g., "existing brand asset", "inspiration from [source]"}} | {{What this reference anchors — e.g., "color palette, illustration style, character proportions"}} |
| `references/ref-02-{{description}}.png` | {{source}} | {{properties}} |

> Add more rows as needed. User references supplement the generated library —
> they're especially useful when creating new asset types not covered by the 8 standard elements.

### Extending the Library

When new assets are generated that represent a style not yet covered:
- Save them to the `design-system/` directory with a descriptive filename
- Add an entry to this reference index
- Note what style anchors the new reference provides

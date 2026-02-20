---
name: newsletter-visuals
description: "Audit a newsletter draft for visual opportunities, score and rank them, and generate on-brand visual assets using AI. Use when enhancing a newsletter draft with visuals, when a draft has [screenshot] placeholders, when asked to 'add visuals to the newsletter', 'create images for this issue', 'make this more visual', or when any newsletter draft needs strategic visual enhancement."
---

# Newsletter Visual Assets

Analyze a newsletter draft, identify the highest-impact opportunities for visual enhancement, and generate on-brand visual assets. Every visual must **clarify, persuade, or engage** — never decorate.

**Core Principle**: Visuals earn their place through measurable impact on clarity, engagement, or persuasion. A newsletter with zero visuals is better than one with decorative filler.

## When to Use

Use this skill when:
- Enhancing a newsletter draft with visual assets
- A draft contains `[screenshot]` placeholders that need strategic evaluation
- The user asks to "add visuals", "create images", or "make this more visual"
- A newsletter draft is text-heavy and could benefit from visual breaks

## Prerequisites

**MANDATORY**: A design system must exist before generating any visuals. Check `~/.claude/.context/design-systems/` for available design systems. If none exists, STOP and invoke `branding-kit:design-system` to create one. If one exists, verify its Application Guidelines cover newsletter/website assets.

## Content Type Resolution

| Content Type | Reference File | Key Focus |
|---|---|---|
| Substack newsletter | `references/substack-constraints.md` | Aspect ratios, email rendering, resolution |

**MANDATORY**: Read the relevant reference file before generating any assets.

## Workflow

### Step 1: Audit the Draft

Read the full draft and catalog every section. For each section, evaluate:

1. **Existing visuals** — Does it already have a `[screenshot]` placeholder, code block, table, or other visual element? Note what it covers and whether it's sufficient.
2. **Complexity** — Is the concept hard to explain in text alone? (process flows, architectures, comparisons, data)
3. **Engagement risk** — Is this a point where readers are likely to disengage? (long text-only stretches, dense technical explanations)
4. **Persuasion opportunity** — Could a visual make a claim more believable? (cost data, performance comparisons, before/after scenarios)

**Existing `[screenshot]` placeholders**: These represent real UI captures the author will provide. Treat them as existing visuals. Only recommend replacing one if the concept would be better served by a diagram or illustration — and explicitly flag this to the user with justification.

### Step 2: Score and Rank Opportunities

For each potential visual opportunity, score on three dimensions (1-5 each):

| Dimension | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **Clarity lift** | Text explains it fine | Text alone is confusing or requires re-reading |
| **Engagement lift** | Section is already engaging | Long text-only stretch, reader likely to skim past |
| **Uniqueness** | Generic/decorative visual | Visual reveals structure or data text can't convey |

**Total score = Clarity + Engagement + Uniqueness** (max 15)

**Hard rules:**
- Only visuals scoring 10+ make the shortlist
- Maximum 5 visuals per newsletter issue (fewer is often better)
- At least one visual in the first half of the newsletter
- Never add a visual within 150 words of another (visual fatigue)
- Visuals scoring below 8 are never included

### Step 3: Select Visual Types

Choose the type based on what the visual needs to accomplish:

| Visual Type | Use When | Examples |
|-------------|----------|---------|
| **Conceptual diagram** | Explaining a process, architecture, or flow | Flowcharts, swimlane diagrams, network diagrams |
| **Comparison visual** | Showing differences between two or more things | Side-by-side layouts, before/after |
| **Data visualization** | Making numbers or ratios tangible | Bar charts, token cost comparisons |
| **Custom illustration** | Engaging the reader emotionally or setting context | Hero images, conceptual metaphors |
| **Annotated screenshot** | Adding context to an existing UI capture | Callout boxes, arrows, numbered annotations |

Never use illustrations when a diagram would be more informative. Illustrations are for engagement; diagrams are for clarity. When in doubt, choose the one that teaches.

### Step 4: Present the Visual Brief

Before generating anything, present the brief to the user for approval:

For each recommended visual:
1. **Location** — Exact section and paragraph
2. **Type** — Which visual type
3. **Purpose** — What it clarifies, persuades, or engages (one sentence)
4. **Description** — What the visual shows (the concept, not the generation prompt)
5. **Score** — The three dimension scores and total

Also include:
- Sections where you did NOT recommend visuals and why
- Any `[screenshot]` placeholders you recommend replacing (with justification)

**Do NOT generate prompts or images until the user approves the brief.**

### Step 5: Generate Visual Assets

After approval, generate each visual using `art:nanobanana`.

**Design system integration**: Load the design system from `~/.claude/.context/design-systems/` and apply it to every prompt — colors, typography, illustration style, brand constraints.

**Prompt construction**:
```
[SUBJECT]: What the visual depicts
[COMPOSITION]: Layout, arrangement, spatial relationships
[STYLE]: From the design system — colors, typography, illustration style
[CONSTRAINTS]: What to avoid, what NOT to include
[FORMAT]: Aspect ratio and resolution (from substack-constraints reference)
```

**Prompt rules:**
- Be specific about spatial relationships ("left side shows X, right side shows Y")
- Include exact hex colors from the design system
- Specify "no text" or exact text to render (minimize text — AI text rendering is unreliable)
- Always include the style from your design system — never leave style ambiguous
- Never fabricate data that isn't in the source draft

### Step 6: Write Captions and Alt Text

For each generated visual:

1. **Caption** — 1 sentence that adds context the image doesn't show. Good captions answer "so what?" — they don't just describe what's visible.
2. **Alt text** — Descriptive text for accessibility. Convey informational content, not visual style. ("Bar chart showing agent teams use 7x more tokens than single agents" not "blue and orange bar chart")

### Step 7: Verify Against Checklist

Run the quality checklist before presenting final assets.

## Voice Application

ALWAYS invoke `writing:voice` before finalizing any written output (captions). Voice is applied after the structural draft is complete but before brand compliance.

**Invocation point**: After writing captions and alt text, before presenting to the user.

## Brand Compliance

When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns.

**Invocation point**: After voice application, as the final quality gate.

## Quality Checklist

- [ ] Design system loaded before any generation
- [ ] Every visual scores 10+ on the clarity/engagement/uniqueness scale
- [ ] Maximum 5 visuals in the brief
- [ ] At least one visual in the first half of the newsletter
- [ ] No two visuals within 150 words of each other
- [ ] Brief presented and approved before generation
- [ ] Every prompt includes design system colors and style
- [ ] No fabricated data in any visual
- [ ] Captions answer "so what?" (not just describe the image)
- [ ] Alt text conveys information, not visual style
- [ ] `writing:voice` invoked for captions
- [ ] `branding-kit:brand-guidelines` invoked for brand compliance

## Common Pitfalls

1. **Too many visuals (6+)**: Cap at 5. Force-rank by score. Fewer high-impact visuals beat many mediocre ones.
2. **Decorative hero image**: Only include a hero if it scores 10+. Most newsletters don't need one.
3. **Inventing data**: Only visualize data the author provides. Never fabricate statistics.
4. **Replacing screenshots without asking**: Screenshots are the author's real evidence. Only suggest replacing with explicit justification.
5. **Ignoring the design system**: Every prompt must reference the design system. No making up colors or styles.
6. **Dark-themed images for email**: Default to light backgrounds. Dark images look broken in most email clients.
7. **Text-heavy images**: Minimize text in generated images. Put text in captions instead.
8. **Generating before brief approval**: Always present the brief first. Wasted assets cost time and API credits.
9. **Using illustrations where diagrams belong**: If the goal is clarity, use a diagram. Illustrations are for engagement.

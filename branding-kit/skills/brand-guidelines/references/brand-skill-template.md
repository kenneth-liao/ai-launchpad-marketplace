# Brand Skill Template

This template is used by the brand-guidelines meta-skill to generate a self-contained brand skill at `~/.claude/skills/{{brand_slug}}/SKILL.md`. Fill every `{{placeholder}}` with confirmed brand data from the discovery and synthesis phases.

## Contents

- Generated SKILL.md (the full template with placeholders)
- Placeholder Reference (all placeholders and their sources)
- Anti-Pattern Derivation (trait-to-anti-pattern mapping and formatting rules)

---

## Generated SKILL.md

```markdown
---
name: {{brand_slug}}
description: Enforce {{brand_name}} brand guidelines when creating visual assets or written content. Resolves the correct design system for each asset type, applies brand voice and tone, and checks for anti-patterns. Use whenever creating, reviewing, or editing assets for {{brand_name}}.
---

# {{brand_name}} Brand Guidelines

Enforce brand identity across all visual and written assets for {{brand_name}}.

---

## 1. Brand Identity

**Name:** {{brand_name}}
**Tagline:** {{tagline}}
**Mission:** {{mission}}
**Value Proposition:** {{value_prop}}

---

## 2. Voice & Tone

**Voice Traits:** {{voice_trait_1}}, {{voice_trait_2}}

{{voice_trait_1_description}}

{{voice_trait_2_description}}

**Tone Modifiers:** {{tone_modifier_1}}, {{tone_modifier_2}}

{{tone_modifier_1_description}}

{{tone_modifier_2_description}}

**Voice Application Rules:**

Apply these rules whenever creating written content, alt text, captions, titles, or any text associated with {{brand_name}} assets:

1. {{voice_rule_1}}
2. {{voice_rule_2}}
3. {{voice_rule_3}}
4. {{voice_rule_4}}

---

## 3. Target Audiences

### Primary: {{primary_audience_name}}

- **Who they are:** {{primary_audience_who}}
- **Goals:** {{primary_audience_goals}}
- **Frustrations:** {{primary_audience_frustrations}}
- **What resonates:** {{primary_audience_resonates}}
- **Platforms:** {{primary_audience_platforms}}

### Secondary: {{secondary_audience_name}}

- **Who they are:** {{secondary_audience_who}}
- **Goals:** {{secondary_audience_goals}}
- **Frustrations:** {{secondary_audience_frustrations}}
- **What resonates:** {{secondary_audience_resonates}}
- **Platforms:** {{secondary_audience_platforms}}

---

## 4. Design System Resolution

When creating a visual asset for {{brand_name}}, resolve the correct design system using the mapping table below.

### Asset Type → Design System Mapping

| Asset Type | Design System | Path |
|------------|---------------|------|
{{asset_ds_mapping_rows}}

### Resolution Logic

When asked to create an asset for {{brand_name}}:

1. **Identify the asset type** from the request (e.g., "make a YouTube thumbnail" → YouTube thumbnails)
2. **Look up the mapping** in the table above
3. **If a design system is mapped:** Load the design system document at the specified path. Apply all visual rules (colors, typography, line work, composition, character system) from that document.
4. **If mapped to "Decide later":** Inform the user that no design system is assigned for this asset type. List available design systems from `~/.claude/.context/design-systems/` and offer to assign one, or offer to create a new one using the branding-kit:design-system skill.
5. **If no matching asset type:** Ask the user which design system to use, or whether to create a new category.

---

## 5. How To Apply

Follow this procedure whenever creating any asset for {{brand_name}}:

### Step 1: Identify the asset type
Determine what kind of asset is being created from the user's request. Match it to one of the asset types in the mapping table above.

### Step 2: Resolve the design system
Use the resolution logic in Section 4 to find the correct design system document for this asset type.

### Step 3: Load the design system
Read the design system document at the resolved path. Extract all visual specifications: color palette, line work rules, composition approach, character system, typography, and the prompt library.

### Step 4: Apply brand voice
For any text content in or accompanying the asset (titles, captions, alt text, descriptions), apply the voice application rules from Section 2. Ensure the tone matches the brand personality.

### Step 5: Apply visual identity
Use the design system's specifications to create the visual asset. Follow the prompt library templates if generating images with AI tools.

### Step 6: Check anti-patterns
Before finalizing, review the asset against the anti-patterns in Section 6. Flag and fix any violations.

---

## 6. Brand Anti-Patterns

These are things {{brand_name}} should **NEVER** do. Check every asset against this list before delivery.

{{anti_patterns}}
```

---

## Placeholder Reference

All placeholders used in the template above:

| Placeholder | Source | Description |
|-------------|--------|-------------|
| `{{brand_name}}` | Dimension 1 | Brand name as provided by the user |
| `{{brand_slug}}` | Derived from brand name | Lowercase, hyphens for spaces/special chars |
| `{{tagline}}` | Dimension 1 (or synthesized) | Brand tagline or slogan |
| `{{mission}}` | Dimension 2 | Brand mission statement |
| `{{value_prop}}` | Dimension 2 | What makes the brand unique |
| `{{voice_trait_1}}` | Dimension 3 | First selected voice trait |
| `{{voice_trait_2}}` | Dimension 3 | Second selected voice trait (or "N/A" if only one) |
| `{{voice_trait_1_description}}` | Derived | Usage guidance for first trait |
| `{{voice_trait_2_description}}` | Derived | Usage guidance for second trait |
| `{{tone_modifier_1}}` | Dimension 4 | First selected tone modifier |
| `{{tone_modifier_2}}` | Dimension 4 | Second selected tone modifier (or "N/A" if only one) |
| `{{tone_modifier_1_description}}` | Derived | Usage guidance for first modifier |
| `{{tone_modifier_2_description}}` | Derived | Usage guidance for second modifier |
| `{{voice_rule_1}}` through `{{voice_rule_4}}` | Synthesized | Concrete voice application rules combining traits + modifiers |
| `{{primary_audience_name}}` | Dimension 5 | Primary audience label |
| `{{primary_audience_who}}` | Dimension 5 + synthesis | Who they are |
| `{{primary_audience_goals}}` | Dimension 5 + synthesis | What they're trying to achieve |
| `{{primary_audience_frustrations}}` | Dimension 5 + synthesis | What frustrates them |
| `{{primary_audience_resonates}}` | Synthesized | What messaging resonates with them |
| `{{primary_audience_platforms}}` | Dimension 5 + synthesis | Where they spend time |
| `{{secondary_audience_*}}` | Same as primary | Same fields for secondary audience |
| `{{asset_ds_mapping_rows}}` | Dimension 6 | Pipe-delimited table rows for each asset type mapping |
| `{{anti_patterns}}` | Derived from Dimension 3 | Numbered list of brand anti-patterns |

---

## Anti-Pattern Derivation

Generate anti-patterns from the **inverse** of the user's chosen voice traits. Include all anti-patterns for all selected traits, plus 1-2 general anti-patterns.

### Trait → Anti-Pattern Mapping

| Voice Trait | Anti-Pattern |
|---|---|
| Friendly & approachable | Never use cold, corporate, or impersonal language. Avoid jargon walls, formal third-person constructions, or anything that creates distance between the brand and the reader. |
| Expert & authoritative | Never be wishy-washy or non-committal. Avoid hedging language ("maybe", "sort of", "it depends"), unsupported claims, or content that lacks depth and evidence. |
| Bold & provocative | Never be safe, generic, or forgettable. Avoid bland statements that could apply to any brand, cliched phrases, or messaging that plays it too safe to make a point. |
| Warm & encouraging | Never be condescending or gatekeeping. Avoid "well, actually" energy, content that assumes expertise, or language that makes beginners feel unwelcome. |
| Witty & playful | Never be dry, humorless, or robotic. Avoid monotone delivery, overly formal sentence structures, or content that feels like it was generated by a template. |

### General Anti-Patterns (always include)

- Never mix design systems across a single asset — one asset type, one design system
- Never create visual assets for {{brand_name}} without first resolving and loading the correct design system

### Formatting

Output anti-patterns as a numbered list, each starting with "Never" or "Avoid":

```
1. **Never use cold, corporate, or impersonal language.** This brand is friendly and approachable — if it sounds like a corporate memo, it's off-brand.
2. **Never be wishy-washy or non-committal.** This brand is an expert authority — back claims with evidence and take clear positions.
3. ...
5. **Never mix design systems across a single asset.** Each asset type has one assigned design system — use it consistently.
6. **Never create visual assets without loading the design system first.** Always resolve the correct design system document and apply its full specification.
```

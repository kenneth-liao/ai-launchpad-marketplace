---
name: social-graphic
description: "Create social media graphics and visual assets for any platform. Handles platform-specific dimensions, safe zones, and design constraints. Integrates with art:nanobanana for image generation and brand guidelines for consistency."
---

# Social Graphic Skill

Create polished social media graphics and visual assets optimized for specific platforms. This skill handles platform-specific dimensions, safe zones, and design constraints to produce assets that display correctly and perform well across channels.

## When to Use

Invoke this skill when the user needs:
- **Social media post images** -- Twitter/X, LinkedIn, Instagram
- **Newsletter headers** -- Substack, email campaigns
- **Blog feature images** -- OG images, hero banners
- **Course thumbnails** -- Platform-specific cover images
- **Profile and cover images** -- Headers, banners, profile pictures

For YouTube thumbnails or any thumbnail requiring specialized CTR optimization, use the `visual-design:thumbnail` skill instead.

## Platform Resolution

Before generating any asset, determine the target platform and format. Platform specs are loaded from `references/platform-specs.md`.

**Resolution order:**
1. If the calling orchestrator provides platform context (dimensions, format), use it directly
2. If the user specifies a platform, load specs from the reference file
3. If ambiguous, ask the user which platform and format they need

Always confirm dimensions before generating. Mismatched dimensions cause cropping, letterboxing, or blurry upscaling on the target platform.

## Standard Workflow

### 1. Determine Platform and Format

Identify the target platform and specific format from user request or orchestrator context. Load the matching specs from `references/platform-specs.md`, including dimensions, aspect ratio, safe zones, and text constraints.

### 2. Gather Context

Collect the information needed to design the graphic:
- **Topic or subject** -- What the graphic is about
- **Key message** -- The primary text or call to action
- **Brand elements** -- Logo, colors, typography (resolve via brand guidelines)
- **Reference images** -- Any existing assets, style references, or photos to incorporate
- **Tone** -- Professional, casual, bold, minimal, etc.

### 3. Design the Concept

Create a design concept that respects the platform constraints:
- Work within the safe zone (keep text and key elements within 80% of frame)
- Follow text size minimums from platform specs
- Ensure the composition works at the platform's typical display size
- Apply the thumbnail design principles from `visual-design:thumbnail` references where applicable (glance test, focal points, contrast)

### 4. Generate the Image

Use the `art:nanobanana` skill to generate the graphic:
- Set the correct aspect ratio matching the platform spec
- Use Pro model for final production assets, Flash for drafts and exploration
- Pass any reference images using absolute paths
- Include brand-specific style direction in the prompt

### 5. Brand Compliance Check

Invoke `branding-kit:brand-guidelines` to verify the generated graphic against:
- Brand color palette and typography
- Visual style consistency
- Anti-patterns (things the brand should never do)
- Design system rules for the asset type

For The AI Launchpad assets, this step is **mandatory**. For other brands, check if a brand guidelines skill exists at `~/.claude/skills/` and apply any relevant constraints.

### 6. Review and Iterate

Review the generated graphic against the quality checklist below. If it does not pass, edit using `art:nanobanana` with the original as a reference image. Limit iteration to two rounds maximum.

### 7. Present to User

Present the final graphic with:
- The generated image
- Platform and dimensions used
- Any notes on safe zones or cropping behavior
- Suggestions for companion text or alt text

## Brand Compliance

When creating visual assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns. This ensures all social graphics are consistent with the established brand identity.

For other brands, check if a brand guidelines skill exists at `~/.claude/skills/` and apply any relevant design constraints. If no brand guidelines exist, follow general best practices for the target platform.

## Quality Checklist

Before presenting any graphic to the user, verify:

1. **Correct dimensions** -- Matches the target platform spec exactly
2. **Safe zone compliance** -- Text and key elements within 80% of frame
3. **Text legibility** -- All text readable at the platform's typical display size
4. **Brand consistency** -- Colors, fonts, and style match brand guidelines
5. **Visual clarity** -- Clean composition, clear focal point, no clutter
6. **Platform constraints** -- Respects text overlay limits, file size recommendations
7. **Contrast and accessibility** -- Sufficient contrast for readability across devices
8. **No cropping issues** -- Key elements will not be cut off by platform UI overlays

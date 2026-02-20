# Visual Design

A foundation plugin for creating visual assets across platforms. Visual Design provides task skills for generating thumbnails, cover images, and social media graphics optimized for engagement and brand consistency.

## Skills

### thumbnail

Create high-performing thumbnails and cover images for any platform. Uses `art:nanobanana` for generation, follows proven design patterns for CTR optimization, and integrates with brand guidelines for consistency.

- Generates thumbnails using `art:nanobanana` with Gemini image models
- Applies proven design formulas: glance test, curiosity, focal points, mobile-first
- Supports platform-specific dimensions (YouTube 1280x720, blog headers 1200x630, etc.)
- Integrates with `branding-kit:brand-guidelines` for brand compliance
- Includes Thumbnail Reviewer agent workflow for quality assurance

### social-graphic

Create social media graphics and visual assets for any platform. Handles platform-specific dimensions, safe zones, and design constraints.

- Supports Twitter/X, LinkedIn, Instagram, Substack, YouTube, and blog/website formats
- Loads platform specs (dimensions, safe zones, text limits) from reference data
- Generates images using `art:nanobanana` skill
- Enforces brand consistency through `branding-kit:brand-guidelines`
- Covers social posts, newsletter headers, blog feature images, and course thumbnails

## Usage

These skills are invoked by orchestrator skills or directly by the user. Platform-specific context (dimensions, safe zones, format requirements) can be provided by the calling orchestrator or resolved from the built-in platform specs.

## Dependencies

- `art:nanobanana` -- AI image generation via Gemini models
- `branding-kit:brand-guidelines` -- Brand identity and design system resolution

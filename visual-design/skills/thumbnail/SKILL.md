---
name: thumbnail
description: "Create high-performing thumbnails and cover images for any platform. Uses Thumbkit for generation, follows proven design patterns for CTR optimization, and integrates with brand guidelines for consistency."
---

# Thumbnail Skill

This skill enables generation of high-performing thumbnails and cover images optimized for click-through rate (CTR). Thumbnails are designed to spark curiosity, complement titles, and compel viewers to click.

## Thumbkit

You have access to Thumbkit, a CLI tool for generating and editing high-performing thumbnails. You **MUST** use Thumbkit to generate and edit all thumbnails.

Using Thumbkit is **REQUIRED** for you to complete your task. Assume Thumbkit has been installed as a uv tool and is available globally on the user's system. If Thumbkit is not installed, you **MUST** install it before proceeding.

### Testing Installation

Test if Thumbkit is installed:

```bash
thumbkit --version
```

### Installation

```bash
uv tool install https://github.com/kenneth-liao/thumbkit.git
```

### Upgrading

```bash
uv tool upgrade thumbkit
```

### Thumbkit Documentation

To access the full CLI reference documentation, run the following command:

```bash
thumbkit docs
```

## REQUIRED READING

The following documents are **MANDATORY READING** before generating ANY thumbnail.

1. `references/thumbnail-formulas.md` - Design formulas for high CTR thumbnails through proven strategies. These principles apply universally across platforms.
2. `references/prompting-guidelines.md` - Thumbnails are generated using Gemini image models (NanoBanana). The prompting guidelines will enable you to get more predictable and consistent results.
3. You **MUST** read the complete Thumbkit CLI reference documentation by running `thumbkit docs`.

It is a **MANDATORY REQUIREMENT** that you follow both the design formulas and prompting guidelines in order to generate high-performing thumbnails. Failure to do so will result in a failed task.

## Platform Context

When invoked by orchestrator skills, platform-specific context (dimensions, safe zones, format requirements) may be provided. Use the provided context to set the correct output dimensions and constraints.

**Default dimensions:** When no platform context is given, default to YouTube thumbnail dimensions (1280x720, 16:9 aspect ratio).

Common platform dimensions:
- **YouTube thumbnail:** 1280x720 (16:9)
- **Blog feature image:** 1200x630
- **Course thumbnail:** 1280x720 or 1080x1080
- **Newsletter header:** 1100x220 or 1200x630
- **Social media card:** 1200x675

Always confirm the target platform before generating to ensure correct dimensions.

## Reference Images

With both generating and editing thumbnails, you can include reference images. Examples include but are not limited to thumbnail templates, headshots, icons, logos, or images for style transfer. See the Prompting Guidelines above for more.

All reference images **MUST** be passed using absolute paths.

### Using Official Logos

If using company logos, use actual images by passing the absolute path to the image files instead of simply describing them. Nanobanana does not know what common company logos look like.

If a company logo is not locally available, you can search for it online and download it using curl, then pass the absolute path to the downloaded image in the prompt. Save all downloaded images to `./downloads/`, making the directory if it does not exist.

### Common Mistakes to Avoid

**WRONG**: "create the Claude AI logo (an orange C shape)"
**CORRECT**: Pass the actual logo file as a reference image

**WRONG**: "add the Python logo"
**CORRECT**: Use `/absolute/path/to/python-logo.png` as a reference image

### Proven Designs

If you know the content title or subject, search for related OUTLIER content. **Focus on OUTLIERS** because they are already proven to work well and very likely have high click-through rates. Videos are outliers if they have a high amount of views compared to the subscriber count of the channel. For example, if a video has 10,000+ views from a channel with less than 5,000 subscribers, that video is an outlier.

Once you have a list of outlier videos, you can access their thumbnails and use them to style transfer.

Here is a URL example of a standard definition thumbnail for a video with id "rmvDxxNubIg":
`https://img.youtube.com/vi/rmvDxxNubIg/sddefault.jpg`. You can download the image using curl to `./downloads/outliers/`, and then read the image file to understand it. Use it as a reference image when using for style transfer.

## Brand Compliance

When creating visual assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns. This ensures all thumbnails are consistent with the established brand identity, color palette, and visual style.

For other brands, check if a brand guidelines skill exists at `~/.claude/skills/` and apply any relevant design constraints.

## Workflows

### Generating Thumbnail Concepts

Once you have generated an initial thumbnail concept or prompt, you **MUST** use the `Thumbnail Reviewer` agent to review the concept and provide feedback. The reviewer will provide a critique and suggest improvements. Consider the reviewer's feedback and incorporate it before proceeding. **DO NOT** go through the generate-review-regenerate loop more than **ONCE**.

### Optimizing Thumbnails

Because you can edit a base image with Thumbkit, you can iteratively modify and improve a previously generated thumbnail. For example, if you have generated a thumbnail but want to change the color scheme:

```bash
thumbkit edit \
  --base absolute/path/to/original-thumbnail.png \
  --prompt "Keep everything the same, but change the text color to bright red."
```

Always review generated thumbnails to ensure they meet the complete design formulas and original intent. If not, you can iterate by editing the original thumbnail. **DO NOT** go through the generate-review-regenerate loop more than **ONCE**.

## User Assets

If the user has specified any local assets (e.g. thumbnail templates, headshots, icons, logos, etc.) in their local context, bias towards incorporating them into the thumbnail when relevant. For example, thumbnails with actual people in them have been shown to perform better.

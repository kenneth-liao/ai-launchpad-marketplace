# Creator Stack

A complete content creation toolkit — writing, content strategy, visual design, AI image generation, branding, and YouTube/Substack platform workflows.

This plugin consolidates what were previously 7 separate plugins (`writing`, `content-strategy`, `visual-design`, `art`, `branding-kit`, `youtube`, `substack`) into a single cohesive system that reflects how these skills actually work together.

## Prerequisites

- AI Launchpad marketplace added — see [main README](../README.md)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (required for the YouTube Data API script)
- `YOUTUBE_API_KEY` environment variable set with a [YouTube Data API](https://developers.google.com/youtube/v3/getting-started) key (for YouTube skills)
- `GEMINI_API_KEY` environment variable set (for AI image generation)

## Installation

```
/plugin install creator-stack@ai-launchpad-marketplace
```

Restart Claude Code for the changes to take effect.

## Skills

### Writing

| Skill | Description |
|-------|-------------|
| `write` | Generalized writing for any platform and format — handles structure, drafting, and platform-specific conventions |
| `voice` | Applies Kenny's authentic writing voice — invoked automatically by copywriting or independently by other skills |

### Content Strategy

| Skill | Description |
|-------|-------------|
| `research` | Conduct topic and competitor research for any content type |
| `title` | Generate optimized titles and headlines for any content type |
| `hook` | Create retention-optimized opening hooks for any content type |
| `extract-ideas` | Extract structured content ideas from published material |

### Visual Design

| Skill | Description |
|-------|-------------|
| `thumbnail` | Create high-performing thumbnails and cover images for any platform |
| `social-graphic` | Create social media graphics and visual assets for any platform |
| `newsletter-visuals` | Audit a newsletter draft for visual opportunities and generate on-brand assets |

### AI Image Generation

| Skill | Description |
|-------|-------------|
| `nanobanana` | AI image generation and editing using Google Gemini models |

### Branding

| Skill | Description |
|-------|-------------|
| `brand-guidelines` | Define, codify, or update brand identity and connect it to design systems |
| `design-system` | Create, update, or refresh a visual design system or art style guide |

### YouTube

| Skill | Description |
|-------|-------------|
| `youtube-data` | Retrieve YouTube data: search videos, get details, fetch transcripts, read comments, discover trending/related content |
| `plan-video` | Complete video planning: research, titles, thumbnails, hooks, content outline |
| `repurpose-video` | Repurpose a completed video into newsletter issues, social posts, and more |
| `newsletter-to-video` | Convert a newsletter issue into a YouTube video outline |
| `community-post` | Create YouTube community posts for engagement |

### Substack

| Skill | Description |
|-------|-------------|
| `plan-newsletter` | Plan a complete newsletter issue: research, draft, subject line, hook, social posts |
| `optimize-newsletter` | Optimize a newsletter draft or write a full issue from an outline |
| `ideate-notes` | Scan published content to generate high-quality Substack Notes ideas |
| `write-note` | Create high-engagement Substack Notes for standalone audience engagement |

## Agents

| Agent | Description |
|-------|-------------|
| YouTube Researcher | Expert researcher using the YouTube Data API script via Bash |
| Thumbnail Reviewer | Evaluates thumbnail concepts against proven design patterns |

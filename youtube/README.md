# YouTube

End-to-end YouTube video planning — orchestrates research, writing, and design skills into YouTube-specific production workflows.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (required for the YouTube Analytics MCP server)
- AI Launchpad marketplace added — see [main README](../README.md)
- `YOUTUBE_API_KEY` environment variable set with a [YouTube Data API](https://developers.google.com/youtube/v3/getting-started) key

## Installation

```
/plugin install youtube@ai-launchpad-marketplace
```

Restart Claude Code for the changes to take effect.

## Skills

| Skill | Description |
|-------|-------------|
| `plan-video` | Complete video planning: research, titles, thumbnails, hooks, content outline |
| `repurpose-video` | Repurpose a completed video into newsletter issues, social posts, and more |
| `newsletter-to-video` | Convert a newsletter issue into a YouTube video outline |
| `create-post` | Create YouTube community posts for engagement |

## Agents

| Agent | Description |
|-------|-------------|
| YouTube Researcher | Expert researcher using YouTube Analytics MCP tools |
| Thumbnail Reviewer | Evaluates thumbnail concepts against proven design patterns |

## MCP Server

The `youtube-analytics` MCP server wraps the YouTube Data API, providing tools for searching videos, fetching details, reading comments/transcripts, and discovering trending content.

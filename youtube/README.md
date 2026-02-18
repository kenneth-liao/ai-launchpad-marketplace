# youtube

A thin orchestrator plugin for YouTube content workflows. This plugin sequences foundation skills (research, writing, design) into YouTube-specific production pipelines. It contains workflow logic and platform-specific decisions, but delegates all content generation to foundation skills.

## Skills

### plan-video

Orchestrates a complete video planning workflow: research, title generation, thumbnail concepts, hook strategies, and content outlining. Delegates to `content-strategy:research`, `content-strategy:title`, `visual-design:thumbnail`, `content-strategy:hook`, and `writing:copywriting` while managing the user selection workflow between steps.

### repurpose-video

Takes a completed video's content (research, plan, transcript) and repurposes it across platforms. Sequences multiple `writing:copywriting` invocations with platform-specific references (newsletter, Twitter, LinkedIn, Substack Notes) to transform video content into multi-platform distribution.

## Agents

### YouTube Researcher

An expert YouTube data researcher powered by Claude Haiku. Uses the YouTube Analytics MCP tools to search and analyze channels, videos, comments, and transcripts. Returns structured research reports with metrics and findings.

### Thumbnail Reviewer

An expert thumbnail concept reviewer. Evaluates thumbnail concepts against proven design requirements (glance test, curiosity, focal points, mobile-first). Provides actionable feedback without subjective creative opinions.

## MCP Server

### youtube-analytics

A Python MCP server (via `uv`) that wraps the YouTube Data API. Provides tools for searching videos, fetching video/channel details, reading comments and transcripts, finding related videos, and discovering trending content. Requires a `YOUTUBE_API_KEY` environment variable.

## Architecture

This plugin is a **thin orchestrator** -- it does not contain implementation logic for titles, thumbnails, hooks, or copywriting. Instead, it composes foundation skills from other plugins:

- `content-strategy` -- research, title formulas, hook strategies
- `visual-design` -- thumbnail concepts and generation
- `writing` -- copywriting, voice consistency

The YouTube Analytics MCP server is the only implementation detail owned by this plugin, providing YouTube-specific data access to any skill invoked from this context.

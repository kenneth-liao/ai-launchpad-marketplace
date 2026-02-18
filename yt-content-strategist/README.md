# YouTube Content Strategist

> **DEPRECATED**: This plugin has been replaced by the composable skill architecture.
> See: writing/, content-strategy/, visual-design/, youtube/ plugins.
> This directory is kept for reference and will be removed in a future cleanup.

This plugin contains a suite of skills, agents, and tools for researching, ideating, and planning YouTube videos. The skills are designed to work together to create a cohesive workflow for optimizing YouTube content performance.

## Requirements

**[NOTE]** You must already have uv installed and the AI Launchpad marketplace added, see [main README](../README.md) if you haven't already.

1. **YouTube Data API Key**: You need a YouTube Data API key to access the YouTube Analytics tools. Instructions [here](https://developers.google.com/youtube/v3/getting-started).
2. **GEMINI API KEY**: You need a Gemini API key to use the NanoBanana image generation model. Instructions [here](https://aistudio.google.com/app/api-keys).

### Thumbkit

This plugin also uses Thumbkit, a CLI tool for generating and editing YouTube thumbnails with the Gemini 2.5 Flash (NanoBanana) image generation model.

The `yt-content-strategist` plugin will automatically install Thumbkit for you if it's missing. To learn more about Thumbkit or install manually yourself, see [here](https://github.com/kenneth-liao/thumbkit).

## Getting Started

Once you have completed the requirements above, you are ready to install the plugin.

1. Navigate to your user level .claude directory.

```bash
cd ~/.claude
```

2. Create an `.env` file in `~/.claude` and add the following keys that you created above:

```bash
YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key
```

3. Navigate to any project directory and start Claude Code.

```bash
claude
```

3. Install the plugin

```bash
/plugin install yt-content-strategist@ai-launchpad-marketplace
```

You can also do this interactively by running `/plugin`.

4. Restart Claude Code for the changes to take effect.

You should now be able to run the skills and tools in this plugin. You can use the `/plugin` command to see the installed plugin and its skills, or run `/context` to see the new MCP tools that have been installed by the plugin.

## Plugin Structure

```
yt-content-strategist/
├── .claude-plugin/
│   └── plugin.json               # Plugin metadata
├── README.md                     # Plugin documentation
├── skills/                       # Claude Code skills
│   ├── youtube-plan-new-video/
│   ├── youtube-research-video-topic/
│   ├── youtube-thumbnail/
│   ├── youtube-title/
│   └── youtube-video-hook/
├── agents/                       # Agent definitions
│   ├── youtube-researcher.md
│   └── thumbnail-reviewer.md
└── servers/                      # MCP servers
    └── py-mcp-youtube-toolbox/
```

## Skills

### youtube-research-video-topic

Conduct pure research for YouTube video topics by analyzing competitors, identifying content gaps, and documenting strategic insights. Produces concise, insight-focused research documents.

**Use when:**
- You need to research a video topic before planning
- You want to understand the competitive landscape
- You need to identify content gaps and opportunities

**Example usage:**
```
Use the youtube-research-video-topic skill to research "AI coding assistants"
```

---

### youtube-plan-new-video

Generate a complete video plan with optimized title, thumbnail, and hook concepts. Orchestrates specialized skills (youtube-title, youtube-thumbnail, youtube-video-hook) to create production-ready video plans.

**Use when:**
- Research is complete and you need creative elements
- You want to plan a new video end-to-end
- You need multiple title/thumbnail/hook options to choose from

**Example usage:**
```
Use the youtube-plan-new-video skill to plan my next video on Claude MCP
```

---

### youtube-title

Generate optimized YouTube video titles that maximize click-through rates by sparking curiosity and complementing thumbnails.

**Use when:**
- You need to create or improve a video title
- You want multiple title variations to test
- Working on YouTube content that requires title optimization

**Example usage:**
```
Use the youtube-title skill to generate titles for a video about Python automation
```

---

### youtube-thumbnail

Create and edit YouTube thumbnails optimized for click-through rate using Thumbkit (Gemini 2.5 Flash image generation).

**Use when:**
- You need to create a thumbnail from scratch
- You want to edit or improve an existing thumbnail
- You need thumbnail concepts that complement your title

**Example usage:**
```
Use the youtube-thumbnail skill to create a thumbnail for my video about AI agents
```

---

### youtube-video-hook

Create optimized YouTube video opening hooks (first 5-30 seconds) that maximize viewer retention and watch time.

**Use when:**
- Planning a new video script and need the opening hook
- Reviewing an existing video opening for retention optimization
- Analyzing why a video has poor retention in the first 30 seconds

**Example usage:**
```
Use the youtube-video-hook skill to create a hook for my video about building AI apps
```

## Agents

### youtube-researcher

Expert YouTube researcher that uses the YouTube Data API to search and analyze channels, videos, comments, transcripts, and related content.

**Capabilities:**
- Search videos by keyword, channel, or criteria
- Get detailed video and channel statistics
- Retrieve video comments and transcripts
- Find related and trending videos
- Produce structured research reports

**Example usage:**
```
@youtube-researcher Analyze the top 10 videos about "Claude API tutorial"
```

---

### thumbnail-reviewer

Expert thumbnail reviewer that critiques thumbnail concepts based on proven design requirements.

**Capabilities:**
- Assess thumbnail alignment with design requirements
- Identify areas of excellence and opportunities for improvement
- Provide actionable feedback without being overly critical

**Example usage:**
```
@thumbnail-reviewer Review this thumbnail concept for my AI coding video
```
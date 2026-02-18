# Newsletter

A thin orchestrator plugin for newsletter content workflows. This plugin does not contain implementation logic — it composes foundation skills from `content-strategy`, `writing`, and `visual-design` into newsletter-specific production workflows.

## How It Works

The newsletter plugin sequences foundation skill invocations to produce complete newsletter issue plans. Each step delegates to a specialized skill that handles the actual work:

- **Research**: `content-strategy:research` for topic and competitor analysis
- **Writing**: `writing:copywriting` for newsletter drafts and social promotion posts
- **Titles**: `content-strategy:title` for subject line generation
- **Hooks**: `content-strategy:hook` for opening paragraph options
- **Voice**: `writing:voice` (invoked automatically by the copywriting skill)
- **Visuals**: `visual-design:social-graphic` for optional header images

## Skills

### plan-issue

Orchestrates a complete newsletter issue plan from topic to publication-ready content. Takes a topic (or source material like a video transcript) and produces:

- Research summary and content angle
- Subject line options with preview text
- Opening hook options
- Full newsletter draft
- Social promotion posts (Twitter/X, LinkedIn, Substack Notes)
- Optional header image

**Example usage:**
```
Use the plan-issue skill to plan a newsletter about AI coding assistants
```

## Plugin Structure

```
newsletter/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── README.md                # Plugin documentation
└── skills/
    └── plan-issue/
        └── SKILL.md         # Orchestrator skill definition
```

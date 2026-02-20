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

### optimize-issue

Orchestrates foundation skills to optimize an existing newsletter draft or write a full issue from an outline. Distinct from plan-issue — this skill starts from existing content rather than a topic.

- Assesses input type (outline vs. rough draft) and routes to the appropriate workflow
- Delegates drafting/optimization to `writing:copywriting`
- Generates subject line options via `content-strategy:title`
- Generates opening hook options via `content-strategy:hook`
- Runs a pre-publish checklist before finalizing
- Presents all options for user selection

**Example usage:**
```
Use the optimize-issue skill to polish my newsletter draft
```

## Plugin Structure

```
newsletter/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── README.md                # Plugin documentation
└── skills/
    ├── plan-issue/
    │   └── SKILL.md         # Orchestrator skill definition
    └── optimize-issue/
        ├── SKILL.md         # Orchestrator skill definition
        └── references/
            └── pre-publish-checklist.md
```

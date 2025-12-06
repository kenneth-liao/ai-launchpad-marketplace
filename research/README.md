# Research

This plugin adds research capabilities to Claude Code with skills and agents for gathering, analyzing, and synthesizing information from the web. Use it for competitor analysis, market research, and general web research tasks.

## Requirements

**[NOTE]** You must already have the AI Launchpad marketplace added, see [main README](../README.md) if you haven't already.

This plugin uses Claude Code's built-in web search and fetch capabilities, so no additional API keys are required.

## Getting Started

1. Navigate to any project directory and start Claude Code.

```bash
claude
```

2. Install the plugin

```bash
/plugin install research@ai-launchpad-marketplace
```

You can also do this interactively by running `/plugin`.

3. Restart Claude Code for the changes to take effect.

You should now be able to run the skills and agents in this plugin. You can use the `/plugin` command to see the installed plugin and its skills.

## Plugin Structure

```
research/
├── .claude-plugin/
│   └── plugin.json               # Plugin metadata
├── README.md                     # Plugin documentation
├── skills/                       # Claude Code skills
│   └── business-competitor-analysis.md
└── agents/                       # Agent definitions
    └── web-researcher.md
```

## Skills

### business-competitor-analysis

Perform comprehensive competitor analysis for any business. Provide either a website URL or direct business details, and this skill will:

1. Extract business information from the provided source
2. Identify the top 5 competitors via web search
3. Research each competitor across 4 key dimensions:
   - Market positioning & messaging
   - Pricing & business model
   - Product/feature comparison
   - Funding & company size
4. Generate a structured markdown report with:
   - Executive summary
   - Competitive matrix table
   - Deep dives on each competitor
   - SWOT analysis
   - Strategic recommendations
   - Cited sources

**Example usage:**
```
Use the business-competitor-analysis skill to analyze https://example-company.com
```

## Agents

### web-researcher

An expert researcher agent that can search the web and fetch data. Use when you need to perform general research, gather external information, and synthesize insights into a structured report.

**Capabilities:**
- Web search and data fetching
- Organizing findings into structured reports
- Citing sources for all findings

**Example usage:**
```
@web-researcher Research the current state of the AI coding assistant market
```

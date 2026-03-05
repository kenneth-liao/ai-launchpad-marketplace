# AI Launchpad Marketplace

A curated collection of Claude Code plugins to unlock your personal workflows.

## Quick Start

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for MCP servers and CLI tools)

Individual plugins may have additional requirements — refer to each plugin's README.

### Installation

1. Start Claude Code anywhere.
2. Add the marketplace:

```
/plugin marketplace add https://github.com/kenneth-liao/ai-launchpad-marketplace.git
```

3. Browse and install plugins interactively with `/plugin`.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [Personal Assistant (Elle)](./personal-assistant) | Persistent-memory personal assistant that learns your preferences and context |
| [Creator Stack](./creator-stack) | Complete content creation toolkit — writing, content strategy, visual design, AI image generation, branding, YouTube, and Substack workflows |
| [Research](./research) | Web research and competitor analysis |
| [Agent Teams](./agent-teams) | Agent team session viewing and analysis |
| [Scheduler](./scheduler) | Cross-platform scheduled automation — recurring skills, prompts, and scripts |

## Keeping Plugins Updated

By default, third-party marketplaces do **not** auto-update. Enable it so new plugins and updates arrive automatically:

1. Run `/plugin` to open the plugin manager.
2. Navigate to **Marketplaces**, select this marketplace.
3. Choose **Enable auto-update**.

Once enabled, Claude Code refreshes the marketplace and updates installed plugins at startup.

**Manual updates:**

```
/plugin marketplace update ai-launchpad-marketplace   # update all plugins
/plugin update plugin-name                             # update a single plugin
```

## Author

**Kenny Liao (The AI Launchpad)**
[YouTube](https://www.youtube.com/@KennethLiao) · [GitHub](https://github.com/kenneth-liao)

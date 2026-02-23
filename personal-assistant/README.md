# Personal Assistant (Elle)

Meet **Elle** — your AI personal assistant who actually remembers you.

Elle transforms Claude Code from a stateless AI into a personal assistant with persistent memory. She learns your preferences, tracks your projects, remembers key people in your life, and gets better at helping you over time.

## Prerequisites

- AI Launchpad marketplace added — see [main README](../README.md)

## Installation

```
/plugin install personal-assistant@ai-launchpad-marketplace
```

Restart Claude Code, then run first-time setup:

```
/personal-assistant:setup
```

This initializes the context system at `~/.claude/.context/` and optionally walks you through onboarding to populate your context.

## Commands

| Command | Description |
|---------|-------------|
| `/personal-assistant:setup` | First-time setup — initializes context system |
| `/personal-assistant:onboard` | Guided conversation to populate your context |
| `/personal-assistant:upgrade` | Upgrade context system to latest structure (preserves data) |
| `/personal-assistant:update-context` | Manually trigger a context update from the current conversation |

## How It Works

Elle maintains a context system — files that persist across conversations at `~/.claude/.context/core/`. Every conversation, Elle:

1. **Loads your context** — who you are, how you work, what you're working on
2. **Grounds responses** — personalizes everything to your situation
3. **Updates memory** — captures new information, preferences, and corrections

The more you use Elle, the more helpful she becomes. Your context is stored externally and persists across plugin updates.

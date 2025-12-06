# Personal Assistant

This plugin turns Claude Code into your personal assistant. It contains a context system, memory management, and hooks to play notification sounds. Think of it as giving Claude a persistent memory and personality that follows you across all your projects.

## Requirements

**[NOTE]** You must already have uv installed and the AI Launchpad marketplace added, see [main README](../README.md) if you haven't already.

No additional requirements.

## Installation

1. Start Claude Code anywhere.

```bash
claude
```

2. Install the plugin

```bash
/plugin install personal-assistant@ai-launchpad-marketplace
```

You can also do this interactively by running `/plugin`.

3. Restart Claude Code for the changes to take effect.

You should now have access to the context system, memory management, and notification sounds. The plugin's output style will automatically activate.

## Plugin Structure

```
personal-assistant/
├── .claude-plugin/
│   └── plugin.json               # Plugin metadata
├── README.md                     # Plugin documentation
├── commands/                     # Slash commands
│   └── update-memories.md
├── context/                      # Context system
│   ├── CLAUDE.md                 # Root context file
│   ├── memory/                   # Memory system
│   │   ├── memories.md           # Memories file
│   │   └── CLAUDE.md             # Memory system context file
│   └── projects/                 # Project tracking
│       └── CLAUDE.md             # Projects context file
├── hooks/                        # Hooks system
│   ├── hooks.json                # Hooks configuration
│   ├── load_context_system.py    # Hook to load context on prompt
│   ├── update-memories-on-stop.py # Hook to update memories on stop
│   └── play_notification.py      # Hook to play notification sound
└── output-styles/                # Output style definitions
    └── personal-assistant.md
```

## Context System

The context system is a filesystem-based memory and project tracking system. It allows Claude to persist important information across conversations.

### Memory System (`context/memory/`)

Claude will automatically remember important details about you:
- Your preferences and goals
- Current progress on tasks
- Important blockers or reminders

### Project System (`context/projects/`)

Track multiple projects with context files that help Claude understand your work across different codebases.

## Commands

### /update-memories

Manually trigger a memory update based on the current conversation. Claude will:

1. Review the conversation for important information
2. Update the memory and context systems
3. Capture blockers, reminders, and next steps for future sessions

**Example usage:**
```
/update-memories
```

## Output Styles

### personal-assistant

Activates "Elle" - a personal assistant personality with specific behaviors:

- **Context-first operations**: Automatically loads relevant context before tasks
- **Delegation framework**: Orchestrates specialized subagents for research tasks
- **Structured outputs**: Concise, scannable, and actionable responses
- **Continuous learning**: Updates memories to capture patterns and learnings

## Hooks

The plugin includes three hooks that run automatically:

| Hook | Trigger | Description |
|------|---------|-------------|
| `load_context_system.py` | On prompt submit | Loads the context system into Claude's context |
| `update-memories-on-stop.py` | On stop | Prompts Claude to update memories after completing tasks |
| `play_notification.py` | On stop, permission prompts, idle | Plays a notification sound to alert you |
# Personal Assistant

This plugin turns Claude Code into your personal assistant. It contains a context system for persistent memory and hooks to play notification sounds. Think of it as giving Claude a persistent memory that follows you across all your projects.

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

4. **Initialize the context system** (first time only):

```bash
/setup-context-system
```

This copies the context templates to `~/.claude/.context/` where your personal context will be stored.

You should now have access to the context system and notification sounds. The plugin's output style will automatically activate.

## Plugin Structure

```
personal-assistant/
├── .claude-plugin/
│   └── plugin.json                # Plugin metadata
├── README.md                      # Plugin documentation
├── commands/                      # Slash commands
│   ├── setup-context-system.md    # Initialize context system
│   └── update-context.md          # Manually trigger context update
├── context-template/              # Context templates (copied to user dir)
│   ├── CLAUDE.md                  # Main context instructions
│   ├── context-update.md          # Update instructions
│   ├── core/                      # Enduring context
│   │   ├── identity.md            # Who you are
│   │   ├── preferences.md         # How you work
│   │   ├── workflows.md           # Your standard procedures
│   │   └── rules.md               # Learned rules from corrections
│   ├── session/
│   │   └── current.md             # Current session context
│   └── projects/
│       └── project_index.md       # Project quick reference
├── hooks/                         # Hooks system
│   ├── hooks.json                 # Hooks configuration
│   ├── load_context_system.py     # Hook to load context on prompt
│   ├── update_context_on_stop.py  # Hook to update context on stop
│   └── play_notification.py       # Hook to play notification sound
├── output-styles/
│   └── personal-assistant.md      # Output style definition
└── skills/
    └── skill-creator/             # Skill for creating new skills
```

## Context System

The context system is a filesystem-based memory system that persists across conversations and plugin updates.

**User context is stored externally** at `~/.claude/.context/` so that:
- Plugin updates don't overwrite your personalized context
- Your context persists across plugin reinstalls
- You own your data

### Core Context (`~/.claude/.context/core/`)

Enduring knowledge about you:
- `identity.md` - Who you are (personal, professional info)
- `preferences.md` - How you like to work
- `workflows.md` - Your standard procedures
- `rules.md` - Learned rules from corrections (**always checked before destructive actions**)

### Session Context (`~/.claude/.context/session/`)

Ephemeral context for the current working session:
- `current.md` - Current focus, active tasks, blockers

### Project Context (`~/.claude/.context/projects/`)

Quick reference for your projects:
- `project_index.md` - Project names, paths, status (details live in project repos)

## Commands

### /setup-context-system

Initialize the context system by copying templates to `~/.claude/.context/`. Run this once after installing the plugin.

**Important:** This command will warn you if context already exists to prevent overwriting your data.

### /update-context

Manually trigger a context update based on the current conversation. Claude will review the conversation and update relevant context files.

## Output Styles

### personal-assistant

Activates a personal assistant personality with specific behaviors:

- **Context-first operations**: Automatically loads relevant context before tasks
- **Structured outputs**: Concise, scannable, and actionable responses
- **Continuous learning**: Updates context to capture patterns and learnings

## Hooks

The plugin includes three hooks that run automatically:

| Hook | Trigger | Description |
|------|---------|-------------|
| `load_context_system.py` | On prompt submit | Loads context from `~/.claude/.context/` |
| `update_context_on_stop.py` | On stop | Prompts Claude to update context after completing tasks |
| `play_notification.py` | On stop, permission prompts, idle | Plays a notification sound to alert you |
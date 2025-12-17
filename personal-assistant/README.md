# Personal Assistant (Elle)

Meet **Elle** — your AI personal assistant who actually remembers you.

Elle transforms Claude Code from a stateless AI into a personal assistant with persistent memory. She learns your preferences, tracks your projects, remembers key people in your life, and gets better at helping you over time.

## What Makes Elle Different

| Without Elle | With Elle |
|--------------|-----------|
| "Here's how to prioritize tasks..." | "Given your energy patterns and the important client meetings this week, I'd suggest front-loading the Acme deliverable on Monday when you're freshest." |
| Starts from zero every conversation | Remembers your context across sessions |
| Generic responses | Personalized to your preferences and workflows |
| Reactive to your requests | Proactive about deadlines, reminders, and opportunities |
| Makes the same mistakes | Learns from corrections and never repeats them |

## How Elle Works

Elle maintains a **context system** — a collection of files that persist across conversations. Every time you chat, Elle:

1. **Loads your context** — Who you are, how you work, what you're working on
2. **Grounds responses in your context** — Personalizes everything to your situation
3. **Updates her memory** — Captures new information, preferences, and corrections

The result: Elle becomes more helpful the more you use her.

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
/plugin install personal-assistant@ai-launchpad
```

You can also do this interactively by running `/plugin`.

3. Restart Claude Code for the changes to take effect.

4. **Set up Elle** (first time only):

```bash
/personal-assistant:setup
```

This sets the output style, initializes the context system at `~/.claude/.context/`, and optionally walks you through onboarding to populate your context.

## Commands

| Command | Description |
|---------|-------------|
| `/personal-assistant:setup` | First-time setup. Sets output style and initializes context system. |
| `/personal-assistant:onboard` | Guided conversation to populate your context. Run anytime to update. |
| `/personal-assistant:upgrade` | Upgrade context system to latest structure (preserves all your data). |
| `/personal-assistant:update-context` | Manually trigger context update based on current conversation. |

## Context System

Elle's memory is stored at `~/.claude/.context/` — **external to the plugin** so your data persists across plugin updates and reinstalls.

### Structure

```
~/.claude/.context/
├── CLAUDE.md              # Elle's operating instructions
├── context-update.md      # How Elle updates her memory
└── core/                  # All your context lives here
    ├── identity.md        # Who you are (personal, professional, goals)
    ├── preferences.md     # How you like to work and communicate
    ├── workflows.md       # Your standard procedures
    ├── relationships.md   # Key people in your life
    ├── triggers.md        # Important dates, deadlines, reminders
    ├── projects.md        # All your projects (work + life)
    ├── rules.md           # Hard rules from corrections
    ├── session.md         # Current working session (ephemeral)
    └── journal.md         # Log of notable sessions
```

### Context Files Explained

| File | Purpose | Example |
|------|---------|---------|
| `identity.md` | Who you are | Family, career, goals, challenges |
| `preferences.md` | How you work | Communication style, tools, decision-making |
| `workflows.md` | Standard procedures | Daily routines, file organization, processes |
| `relationships.md` | Key people | Family, colleagues, collaborators |
| `triggers.md` | Time-sensitive items | Deadlines, birthdays, recurring check-ins |
| `projects.md` | What you're working on | Active projects with locations and status |
| `rules.md` | Hard rules | Things Elle must NEVER or ALWAYS do |
| `session.md` | Current focus | What you're working on right now |
| `journal.md` | History | Log of notable sessions for pattern recognition |

### Rules System

The `rules.md` file is special — Elle **always checks it before taking any action**. When she makes a mistake and you correct her, she adds a rule so she never makes that mistake again.

Example rules:
```
- NEVER commit directly to main without asking
- ALWAYS use pnpm instead of npm in this project
- NEVER suggest medication changes without consulting the health profile
```

## Plugin Structure

```
personal-assistant/
├── .claude-plugin/
│   └── plugin.json                # Plugin metadata
├── README.md                      # This file
├── commands/
│   ├── setup.md                   # First-time setup
│   ├── onboard.md                 # Guided context population
│   ├── upgrade.md                 # Upgrade context structure
│   └── update-context.md          # Manual context update
├── context-template/              # Templates (copied to ~/.claude/.context/)
│   ├── CLAUDE.md
│   ├── context-update.md
│   └── core/
│       ├── identity.md
│       ├── preferences.md
│       ├── workflows.md
│       ├── relationships.md
│       ├── triggers.md
│       ├── projects.md
│       ├── rules.md
│       ├── session.md
│       └── journal.md
├── hooks/
│   ├── hooks.json                 # Hooks configuration
│   ├── load_context_system.py     # Loads context on every message
│   ├── update_context_on_stop.py  # Prompts context update after tasks
│   └── play_notification.py       # Notification sounds
├── output-styles/
│   └── personal-assistant.md      # Elle's personality and behavior
└── skills/
    └── skill-creator/             # Skill for creating new skills
```

## Hooks

Elle uses hooks to automatically manage context:

| Hook | Trigger | Description |
|------|---------|-------------|
| `load_context_system.py` | On every message | Loads your context from `~/.claude/.context/` |
| `update_context_on_stop.py` | After Elle responds | Prompts Elle to update context with new learnings |
| `play_notification.py` | On stop, permissions, idle | Plays notification sounds |

## Upgrading

If you've been using an older version of the Personal Assistant, run:

```bash
/personal-assistant:upgrade
```

This safely migrates your context to the latest structure while **preserving all your data**. A backup is created automatically.

## Philosophy

Elle is built on the principle that **context is everything**. A personal assistant who doesn't remember isn't personal at all.

The more Elle knows about you:
- The better she can anticipate your needs
- The more relevant her suggestions become
- The fewer times you have to repeat yourself
- The more valuable she becomes over time

Your context is **your data** — stored externally, never sent to training, always under your control.

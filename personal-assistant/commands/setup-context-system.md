---
description: Initialize the personal assistant context system. Run this once after installing the plugin.
---

# Context System Setup

Initialize the context system by copying the template files to your user context directory.

## Instructions

### ⚠️ First, check if context already exists

```bash
ls ~/.claude/.context/
```

- **If the directory exists**: Your context is already set up. Do NOT overwrite it or you'll lose your saved context. Do NOT proceed if the directory already exists. You will overwrite the user's context which will result in a **CRITICAL FAILURE**!
- **If the directory doesn't exist**: Proceed with setup below.

### Fresh Install (only if directory doesn't exist)

Copy the template directory to `~/.claude/.context/`:

```bash
cp -r ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/ ~/.claude/.context/
```

### Verify Setup

```bash
ls ~/.claude/.context/
```

You should see: `CLAUDE.md`, `context-update.md`, `core/`, `session/`, `projects/`

## What Gets Created

```
~/.claude/.context/
├── CLAUDE.md              # Main instructions (loaded on every message)
├── context-update.md      # Update instructions (Stop hook)
├── core/                  # Your enduring context
│   ├── identity.md        # Who you are
│   ├── preferences.md     # How you work
│   ├── workflows.md       # Your standard procedures
│   └── rules.md           # Learned rules from corrections
├── session/
│   └── current.md         # Current session context
└── projects/
    └── project_index.md   # Your project index
```

## Why External Storage?

Your context is stored **outside** the plugin directory so that:
- Plugin updates don't overwrite your personalized context
- Your context persists across plugin reinstalls
- You own your data

## After Setup

Once initialized, the context system works automatically:
- Context is loaded on every user message
- Context updates are prompted after each response
- Your personalized data stays safe from plugin updates
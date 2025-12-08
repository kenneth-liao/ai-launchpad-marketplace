---
description: Set up the personal assistant plugin. Run this once after installing the plugin.
---

# Personal Assistant Setup

Set up the personal assistant plugin with context system and output style.

## Step 1: Set Output Style

Update Claude's settings to use the personal assistant output style.

Read the current settings:

```bash
cat ~/.claude/settings.json
```

Then update the `outputStyle` field to `"personal-assistant:Personal Assistant"`. If the file doesn't exist or is empty, create it with this content:

```json
{
  "outputStyle": "personal-assistant:Personal Assistant"
}
```

If the file exists, merge the `outputStyle` field into the existing settings (preserve other settings).

## Step 2: Initialize Context System

### ⚠️ First, check if context already exists

```bash
ls ~/.claude/.context/
```

- **If the directory exists**: Context is already set up. Do NOT overwrite it or you'll lose saved context. **CRITICAL: Do NOT proceed with the copy if the directory already exists!**
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

Once initialized:
- Output style is active (restart Claude Code to apply)
- Context is loaded on every user message
- Context updates are prompted after each response
- Your personalized data stays safe from plugin updates
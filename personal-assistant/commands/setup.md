---
description: Set up the personal assistant plugin. Run this once after installing the plugin.
---

# Personal Assistant Setup

Set up the personal assistant plugin with context system and default Claude Code settings.

## Step 1: Set Default Settings

<REQUIRED>
Communicate with the user the exact settings that will be set and ask the user if they want to selectively disable any of them.
</REQUIRED>

Update Claude's default settings to use the personal assistant output style and display a status line. You **MUST** respect the user's selections above and only set the fields that the user has not explicitly disabled.

You **MUST** read the current settings:

```bash
cat ~/.claude/settings.json
```

If the file doesn't exist or is empty, create it with this content. If the file exists, merge the fields below into the existing settings (you **MUST** preserve other settings).

```json
{
  "outputStyle": "personal-assistant:Personal Assistant",
  "statusLine": {
    "type": "command",
    "command": "cat | jq -r '.output_style.name'"
  }
}
```

If the file exists, merge the fields above into the existing settings.

<REQUIRED>
You **MUST** preserve other settings in the `settings.json` file. Only update/add the fields specified above.
</REQUIRED>

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

Let the user know:
- The output style is active (no need to restart Claude Code)
- Context is loaded on every user message
- Context updates are prompted after each response
- The user should see the status line now showing `personal-assistant:Personal Assistant`
- The user can change the output style any time with `/output-style` or status line with `/statusline`.
- The user can also completely disable the personal assistant plugin in the `/plugin` menu.

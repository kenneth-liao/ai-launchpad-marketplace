---
description: Set up the personal assistant plugin. Run this once after installing the plugin.
---

# Personal Assistant Setup

Set up the Personal Assistant plugin with context system and default Claude Code settings.

## Step 1: Set Default Settings

<REQUIRED>
Communicate with the user the exact settings that will be set and ask the user if they want to selectively disable any of them. The Personal Assistant output style will turn Claude Code into a personal assistant with deep contextual knowledge and proactive behavior to help the user achieve their goals.
</REQUIRED>

Update Claude's default settings to use the Personal Assistant output style and display a status line. You **MUST** respect the user's selections above and only set the fields that the user has not explicitly disabled.

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
    "command": "INPUT=$(cat); STYLE_NAME=$(echo \"$INPUT\" | jq -r '.output_style.name // \"default\"'); STYLE_PLUGIN=$(echo \"$INPUT\" | jq -r '.output_style.plugin // \"\"'); MODEL=$(echo \"$INPUT\" | jq -r '.model.display_name // \"default\"'); if [ -n \"$STYLE_PLUGIN\" ]; then STYLE_DISPLAY=\"$STYLE_NAME@$STYLE_PLUGIN\"; else STYLE_DISPLAY=\"$STYLE_NAME\"; fi; COST=$(echo \"$INPUT\" | jq -r '.cost.total_cost_usd // 0'); TIME=$(echo \"$INPUT\" | jq -r '.cost.total_duration_ms // 0'); if [ \"$TIME\" -lt 60000 ]; then SECS=$((TIME / 1000)); TIME_DISPLAY=\"${SECS}s\"; elif [ \"$TIME\" -lt 3600000 ]; then MINS=$((TIME / 60000)); SECS=$(((TIME % 60000) / 1000)); TIME_DISPLAY=\"${MINS}m ${SECS}s\"; else HOURS=$((TIME / 3600000)); MINS=$(((TIME % 3600000) / 60000)); TIME_DISPLAY=\"${HOURS}h ${MINS}m\"; fi; PLUGINS=$(ls -1d ~/.claude/plugins/marketplaces/*/ 2>/dev/null | wc -l | tr -d ' '); TOOLS=$(uv tool list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ' || echo 0); ADDED=$(echo \"$INPUT\" | jq -r '.cost.total_lines_added // 0'); REMOVED=$(echo \"$INPUT\" | jq -r '.cost.total_lines_removed // 0'); LINES=\"\"; if [ \"$ADDED\" != \"0\" ] || [ \"$REMOVED\" != \"0\" ]; then LINES=\" │ +$ADDED/-$REMOVED\"; fi; printf \"%s │ %s\\n\\$%.2f │ %s Plugins │ %s UV Tools │ %s%s\" \"$STYLE_DISPLAY\" \"$MODEL\" \"$COST\" \"$PLUGINS\" \"$TOOLS\" \"$TIME_DISPLAY\" \"$LINES\""
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

You should see: `CLAUDE.md`, `context-update.md`, `core/`

## What Gets Created

```
~/.claude/.context/
├── CLAUDE.md              # Main instructions (loaded on every message)
├── context-update.md      # Update instructions
└── core/                  # All your context
    ├── identity.md        # Who you are
    ├── preferences.md     # How you work
    ├── workflows.md       # Your standard procedures
    ├── relationships.md   # Key people in your life
    ├── triggers.md        # Important dates and reminders
    ├── projects.md        # Your projects (work + life)
    ├── rules.md           # Learned rules from corrections
    ├── session.md         # Current session context
    └── journal.md         # Session history log
```

## Why External Storage?

Your context is stored **outside** the plugin directory so that:
- Plugin updates don't overwrite your personalized context
- Your context persists across plugin reinstalls
- You own your data

## Step 3: Onboarding — Get to Know the User

<REQUIRED>
After technical setup completes, transition to onboarding:

"Now that Elle is set up, I'd love to get to know you better so I can be truly helpful. Would you like to spend a few minutes telling me about yourself?"
</REQUIRED>

**If YES**: Proceed with the onboarding conversation below.
**If NO**: Let them know they can run `/personal-assistant:onboard` anytime, then skip to "After Setup".

### Onboarding Conversation

Have a natural conversation to learn about the user. Don't interrogate — be warm and curious. After each topic, **immediately write** the learned context to the appropriate file.

#### Identity (write to `~/.claude/.context/core/identity.md`)

Ask conversationally:
1. "What should I call you?"
2. "What do you do for work? What's your role like?"
3. "Outside of work, what's important in your life right now?" (family, hobbies, health goals, etc.)
4. "What are you trying to achieve this year — personally or professionally?"
5. "What are your biggest challenges or frustrations right now?"

#### Key People (write to `~/.claude/.context/core/relationships.md`)

Ask naturally:
- "Who are the important people in your life I should know about?" (partner, family, close colleagues, etc.)
- For each person: name, relationship, any relevant context

#### Preferences (write to `~/.claude/.context/core/preferences.md`)

Ask about working style:
1. "When I give you information, do you prefer quick bullet points or more detailed explanations?"
2. "When you ask for help, do you want me to give you options to choose from, or just tell you what I'd recommend?"
3. "Any tools, apps, or systems you use regularly that I should know about?"

#### Current Focus (write to `~/.claude/.context/core/session.md`)

Ask about right now:
- "What are you working on or thinking about this week?"
- "Anything coming up soon I should keep in mind?" (deadlines, events, decisions)

### After Each Section

Write the learned information to the appropriate context file immediately. Use the formats defined in each template file.

---

## After Setup

Let the user know:
- Elle is now set up and personalized
- The output style is active (no need to restart Claude Code)
- Context is loaded on every user message and updated as you learn more
- They can see the status line showing `Personal Assistant@personal-assistant`
- They can change settings anytime with `/output-style` or `/statusline`
- They can re-run onboarding with `/personal-assistant:onboard` to update their context
- They can disable the plugin in the `/plugin` menu

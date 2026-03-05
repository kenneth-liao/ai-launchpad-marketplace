---
description: Set up the personal assistant plugin. Run this once after installing the plugin.
---

# Personal Assistant Setup (v2)

Set up Elle with native rules delivery, context system, and default Claude Code settings.

## Step 1: Set Default Settings

<REQUIRED>
Communicate with the user the exact settings that will be set and ask the user if they want to selectively disable any of them. The Personal Assistant output style will turn Claude Code into a personal assistant with deep contextual knowledge and proactive behavior.
</REQUIRED>

Read current settings:

```bash
cat ~/.claude/settings.json
```

If the file doesn't exist or is empty, create it with the content below. If the file exists, merge the fields below into the existing settings (you **MUST** preserve other settings).

```json
{
  "outputStyle": "personal-assistant:Personal Assistant",
  "statusLine": {
    "type": "command",
    "command": "INPUT=$(cat); STYLE_NAME=$(echo \"$INPUT\" | jq -r '.output_style.name // \"default\"'); STYLE_PLUGIN=$(echo \"$INPUT\" | jq -r '.output_style.plugin // \"\"'); MODEL=$(echo \"$INPUT\" | jq -r '.model.display_name // \"default\"'); STYLE_DISPLAY=\"$STYLE_NAME\"; PLUGINS=$(ls -1d ~/.claude/plugins/marketplaces/*/ 2>/dev/null | wc -l | tr -d ' '); TOOLS=$(uv tool list 2>/dev/null | grep -c ' v[0-9]' || echo 0); CC_MCPS=$(cat ~/.claude/mcp.json 2>/dev/null | jq '.mcpServers | length // 0' || echo 0); PROJ_MCPS=$(cat .mcp.json 2>/dev/null | jq '.mcpServers | length // 0' || echo 0); MCPL_MCPS=$(mcpl list 2>/dev/null | grep -c '^[[:space:]]*\\[' || echo 0); MCPS=$((CC_MCPS + PROJ_MCPS + MCPL_MCPS)); if [ \"$CC_MCPS\" -eq \"$MCPL_MCPS\" ]; then MCPS=$((CC_MCPS + PROJ_MCPS)); fi; COST=$(echo \"$INPUT\" | jq -r '.cost.total_cost_usd // 0'); TIME=$(echo \"$INPUT\" | jq -r '.cost.total_duration_ms // 0'); if [ \"$TIME\" -lt 60000 ]; then SECS=$((TIME / 1000)); TIME_DISPLAY=\"${SECS}s\"; elif [ \"$TIME\" -lt 3600000 ]; then MINS=$((TIME / 60000)); SECS=$(((TIME % 60000) / 1000)); TIME_DISPLAY=\"${MINS}m ${SECS}s\"; else HOURS=$((TIME / 3600000)); MINS=$(((TIME % 3600000) / 60000)); TIME_DISPLAY=\"${HOURS}h ${MINS}m\"; fi; printf \"%s | %s\\n%s Plugins | %s UV | %s MCPs\\n\\$%.2f | %s\" \"$STYLE_DISPLAY\" \"$MODEL\" \"$PLUGINS\" \"$TOOLS\" \"$MCPS\" \"$COST\" \"$TIME_DISPLAY\""
  }
}
```

<REQUIRED>
You **MUST** preserve other settings in the `settings.json` file. Only update/add the fields specified above.
</REQUIRED>

### Dedup Notification Hooks

Check if the user's `~/.claude/settings.json` already has Stop or Notification sound hooks:

```bash
cat ~/.claude/settings.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
hooks = d.get('hooks', {})
has_stop = bool(hooks.get('Stop'))
has_notif = bool(hooks.get('Notification'))
print(f'Stop hooks: {has_stop}, Notification hooks: {has_notif}')
"
```

If the user already has Stop and/or Notification sound hooks in settings.json, the plugin's hooks.json will also register them -- this causes duplicate sounds. Inform the user and offer to remove the duplicates from settings.json (the plugin hooks.json will handle them).

## Step 2: Initialize Context System

### Check if context already exists

```bash
ls ~/.claude/.context/ 2>/dev/null
```

- **If the directory exists**: Context is already set up. Do NOT overwrite it. **CRITICAL: Do NOT proceed with the copy if the directory already exists!**
- **If the directory doesn't exist**: Proceed with setup below.

### Fresh Install (only if directory doesn't exist)

```bash
cp -r ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/ ~/.claude/.context/
```

### Verify

```bash
ls ~/.claude/.context/
```

You should see: `CLAUDE.md`, `context-update.md`, `core/`

## Step 3: Generate elle-core.md

Create the rules directory and generate the derived rules file:

```bash
mkdir -p ~/.claude/rules
uv run python ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/skills/sync-context/scripts/sync_context.py
```

### Verify

```bash
cat ~/.claude/rules/elle-core.md
```

You should see a compact file with Identity, Communication Preferences, Rules, Active Projects, and Loading Full Context sections.

## Step 4: Onboarding

<REQUIRED>
After technical setup completes, transition to onboarding:

"Now that Elle is set up, I'd love to get to know you better so I can be truly helpful. Would you like to spend a few minutes telling me about yourself?"
</REQUIRED>

**If YES**: Run `/personal-assistant:onboard`, which will populate context files. After onboarding, run `/sync-context` to update elle-core.md with the new information.

**If NO**: Let them know they can run `/personal-assistant:onboard` anytime, then skip to "After Setup".

## After Setup

Let the user know:
- Elle is now set up and personalized
- Context is loaded natively via `~/.claude/rules/elle-core.md` (no per-message overhead)
- SessionStart hook checks for upcoming events proactively
- Context survives compaction automatically
- Run `/sync-context` after significant context changes to keep rules current
- Run `/context-health` periodically to audit data quality
- Run `/evolve` after Claude Code updates to check for new capabilities

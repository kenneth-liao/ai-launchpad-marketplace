---
description: Upgrade Elle to the latest version. Handles v1-to-v2 migration (UserPromptSubmit to native rules) and structural upgrades. Preserves all user data.
---

# Elle Upgrade

Upgrade your Elle installation to the latest version while preserving all personal data.

## Step 1: Detect Current Version

```bash
# Check for v1 indicators (UserPromptSubmit hook in plugin)
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/hooks/hooks.json 2>/dev/null

# Check for v2 indicators (elle-core.md in rules/)
ls ~/.claude/rules/elle-core.md 2>/dev/null

# Check context system exists
ls ~/.claude/.context/core/ 2>/dev/null
```

### Version Detection

| Indicator | Version |
|-----------|---------|
| `UserPromptSubmit` in hooks.json | v1.x |
| `SessionStart` in hooks.json + `elle-core.md` exists | v2.x |
| No context system at all | Not installed |

<REQUIRED>
- If **not installed**: Tell user to run `/personal-assistant:setup` instead. Stop here.
- If **already v2**: Check if instruction files need updating (Step 5 only), then report "Already on v2."
- If **v1**: Proceed with full migration below.
</REQUIRED>

## Step 2: Communicate Migration Plan

> **Elle v2 Upgrade**
>
> I'll upgrade your Elle system from v1 to v2. Here's what changes:
>
> **What stays the same:**
> - All your personal data (identity, preferences, rules, relationships, triggers, projects, etc.)
> - Output style personality and behavior
> - Notification sounds
>
> **What changes:**
> - Context delivery: per-message hook injection to native `~/.claude/rules/elle-core.md`
> - ~95% token savings (no more 4,000 tokens per message overhead)
> - Proactive trigger check at session start (upcoming events within 7 days)
> - Compaction resilience (context survives long conversations)
> - Three new skills: `/sync-context`, `/context-health`, `/evolve`
>
> **Safety:**
> - Full backup created before any changes
> - 100% of your data preserved
>
> Ready to proceed?

<REQUIRED>
Wait for user confirmation before proceeding.
</REQUIRED>

## Step 3: Create Backup

<REQUIRED>
```bash
mkdir -p ~/.claude/.context-backups/ && cp -r ~/.claude/.context/ ~/.claude/.context-backups/$(date +%Y%m%d-%H%M%S)/
```

Verify: `ls -la ~/.claude/.context-backups/`

**DO NOT proceed if backup fails.**
</REQUIRED>

## Step 4: Create Rules Directory and Generate elle-core.md

```bash
mkdir -p ~/.claude/rules
uv run python ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/skills/sync-context/scripts/sync_context.py
```

Verify:

```bash
cat ~/.claude/rules/elle-core.md
```

## Step 5: Update Instruction Files

Replace instruction files (not user data) with latest versions:

```bash
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/CLAUDE.md ~/.claude/.context/CLAUDE.md
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/context-update.md ~/.claude/.context/context-update.md
```

## Step 6: Ensure All Core Files Exist

Check for files added in newer versions:

```bash
ls ~/.claude/.context/core/relationships.md 2>/dev/null
ls ~/.claude/.context/core/triggers.md 2>/dev/null
ls ~/.claude/.context/core/journal.md 2>/dev/null
ls ~/.claude/.context/core/improvements.md 2>/dev/null
```

For any missing files, copy from template:

```bash
# Only copy if missing -- do NOT overwrite existing files
[ ! -f ~/.claude/.context/core/relationships.md ] && cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/relationships.md ~/.claude/.context/core/relationships.md
[ ! -f ~/.claude/.context/core/triggers.md ] && cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/triggers.md ~/.claude/.context/core/triggers.md
[ ! -f ~/.claude/.context/core/journal.md ] && cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/journal.md ~/.claude/.context/core/journal.md
[ ! -f ~/.claude/.context/core/improvements.md ] && cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/improvements.md ~/.claude/.context/core/improvements.md
```

## Step 7: Dedup Notification Hooks

Check if `~/.claude/settings.json` has Stop/Notification hooks that duplicate the plugin's hooks:

```bash
cat ~/.claude/settings.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
hooks = d.get('hooks', {})
has_stop = bool(hooks.get('Stop'))
has_notif = bool(hooks.get('Notification'))
print(f'Stop hooks in settings: {has_stop}')
print(f'Notification hooks in settings: {has_notif}')
"
```

If duplicates exist, inform the user and offer to remove them from settings.json (the plugin handles them).

## Step 8: Clean Up Old Directories

```bash
rmdir ~/.claude/.context/projects/ 2>/dev/null
rmdir ~/.claude/.context/session/ 2>/dev/null
```

## Step 9: Verify and Report

```bash
ls -la ~/.claude/rules/elle-core.md
ls -la ~/.claude/.context/core/
```

> **Upgrade Complete!**
>
> **Backup saved to:** `~/.claude/.context-backups/[timestamp]/`
>
> **What was done:**
> - [x] Created `~/.claude/rules/elle-core.md` (native rules delivery)
> - [x] Updated instruction files (CLAUDE.md, context-update.md)
> - [x] Ensured all core context files exist
> - [x] Checked for notification hook duplicates
>
> **Your data:** 100% preserved. All personal context untouched.
>
> **New capabilities:**
> - `/sync-context` -- regenerate elle-core.md after context changes
> - `/context-health` -- audit context data quality
> - `/evolve` -- check for new Claude Code capabilities
>
> **Next session:** Elle will load your context natively (no per-message overhead) and check for upcoming events.

<REQUIRED>
If any step failed, clearly communicate what failed, reassure that the backup is safe, and provide restore instructions:
`rm -rf ~/.claude/.context && cp -r ~/.claude/.context-backups/[timestamp] ~/.claude/.context`
</REQUIRED>

---
name: migrate
description: Migrate your Elle installation between versions. Handles any version-to-version upgrade path with sequential, idempotent steps. Use when updating Elle, when prompted by a version mismatch, or when the user says "migrate Elle" or "upgrade Elle".
user-invocable: true
---

# Migrate -- Version Upgrade System

This skill handles version-to-version upgrades using sequential, idempotent migration steps. Each version transition has a dedicated reference file containing Check/Action/Verify steps, making migrations safe to re-run on partial completions and easy to extend for future versions.

## 1. Version Detection

### Current Installed Version

**Primary method:** Find the installed version directory.

```bash
ls ~/.claude/plugins/cache/ai-launchpad/personal-assistant/
```

List directories, find the highest version number, and read its `.claude-plugin/plugin.json` to get the `version` field.

**Fallback fingerprinting** (when plugin.json is not reliable):

| Signal | Inferred Version |
|---|---|
| No `~/.claude/.context/` directory | Not installed -- tell user to run `/personal-assistant:setup` and stop |
| `UserPromptSubmit` in plugin hooks, no `~/.claude/rules/elle-core.md` | v1.0.0 |
| `SessionStart` in plugin hooks + `elle-core.md` exists, no `~/.claude/.context/core/improvements.md` | v1.9.0 |
| `SessionStart` + `elle-core.md` + `improvements.md` exists | v1.10.0 |
| Full v2 state (migrate skill exists in installed plugin) | v2.0.0 |

### Target Version

Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` to get the version of the plugin source being installed.

If current == target: report "Already current. Run `/evolve` to check for platform upgrades." and stop.

## 2. Migration Chain

List available migration files from `${CLAUDE_SKILL_DIR}/references/migrations/`. Each file is named `vX.Y.Z-to-vA.B.C.md`.

Parse filenames to build an ordered chain from current version to target version.

Example: if current is v1.10.0 and target is v2.1.0, chain is: v1.10.0 -> v2.0.0, v2.0.0 -> v2.1.0.

For each migration in the chain, read its `## Summary` section and present the plan:

```
Migration path: v1.10.0 -> v2.0.0 -> v2.1.0

Step 1 (v1.10.0 -> v2.0.0):
- Replaces UserPromptSubmit hook with native rules delivery
- ~95% token savings

Step 2 (v2.0.0 -> v2.1.0):
- [summary from file]

Proceed?
```

**Wait for user confirmation before continuing.**

## 3. Backup

Create a timestamped backup before making any changes:

```bash
mkdir -p ~/.claude/.context-backups/ && cp -r ~/.claude/.context/ ~/.claude/.context-backups/$(date +%Y%m%d-%H%M%S)/
```

Verify backup was created:

```bash
ls -la ~/.claude/.context-backups/
```

**REQUIRED: DO NOT proceed if backup fails. This is a hard gate.**

## 4. Execute Migration Chain

For each migration in the chain:

1. Read the migration reference file from `${CLAUDE_SKILL_DIR}/references/migrations/`
2. For each step in the `## Steps` section:
   - Run the **Check** command -- if it exits 0, the step is already done, skip it
   - Run the **Action** command
   - Run the **Verify** command -- if it fails, stop immediately and report the failure
3. After each migration file completes, report: "Migration vX.Y.Z -> vA.B.C complete. N steps executed, M skipped (already done)."

**If any step fails:**
- Stop immediately
- Report which step failed and the error
- Provide restore instructions: `cp -r ~/.claude/.context-backups/[timestamp]/ ~/.claude/.context/`

## 5. Verify and Report

After all migrations complete, verify the final state:

```bash
ls -la ~/.claude/rules/elle-core.md
ls ~/.claude/.context/core/
```

Present final report:

```
Migration Complete!

Path: vX.Y.Z -> ... -> vA.B.C
Backup: ~/.claude/.context-backups/[timestamp]/
Steps executed: N
Steps skipped (already done): M

Your data: 100% preserved. All personal context untouched.
```

If rules-affecting changes were made (rules/, elle-core.md, context files), suggest running `/sync-context`.

## 6. Migration File Format

Each file at `references/migrations/vX.Y.Z-to-vA.B.C.md` follows this format:

```markdown
# Migration: vX.Y.Z -> vA.B.C

## Summary
- [1-3 bullet points describing what this migration does]

## Breaking Changes
- [List any breaking changes, or "None"]

## Steps

### 1. [Step name]
**Check:** `[shell command -- if exits 0, skip this step]`
**Action:** `[shell command to execute]`
**Verify:** `[shell command -- must exit 0 to continue]`
```

Each step MUST have all three fields (Check, Action, Verify). The Check field makes steps idempotent -- safe to re-run on partially completed migrations.

# Changelog

All notable changes to the Personal Assistant (Elle) plugin.

## [2.3.0] - 2026-03-06

### Changed

- **Evolve Phase 1 research** -- Replaced hardcoded documentation URLs with discovery-driven approach. Fetches docs index and discovers pages by category (skills, hooks, subagents, agent teams, commands, CLAUDE.md, memory, MCP servers, output styles, settings, plugin architecture) instead of prescribing specific URLs.
- **Evolve Phase 2 audit** -- Expanded to check all plugin components (output styles, plugin.json, agents/, MCP servers) not just skills and hooks. Added system state check for evolve run recency and version drift.

### Added

- **Evolve Phase 1E: Plugin Architecture research** -- New research task that examines CONVENTIONS.md and other installed plugins to identify structural patterns and unused capabilities.
- **Evolve system state tracking** -- Platform-capabilities.md now includes a System State section (Elle version, last evolve run, Claude Code version, platform docs freshness) updated on each evolve run.
- **Context-health check 7: System Freshness** -- Reads evolve's system state and flags if evolve hasn't run in 60+ days, Claude Code version drift, or missing audit data.
- **Platform capabilities reference** -- Added 7 new sections: Subagent/Agent Tool, Agent Teams, Commands System, Output Styles, MCP Servers in Plugins, Plugin Architecture, Settings & Permissions.
- **Best practices reference** -- Added sections for Skill Design, Output Style Design, Plugin Component Design, and Reference File Philosophy.

---

## [2.2.0] - 2026-03-05

### Changed

- **Commands to Skills migration** -- Migrated `setup`, `onboard`, and `update-context` from legacy `commands/` format to modern `skills/` format. Gains frontmatter control, `${CLAUDE_SKILL_DIR}` support, and supporting file directories. All existing `/personal-assistant:*` invocations continue to work.
- **`/update-context` auto-chains to `/sync-context`** -- After updating context files that affect elle-core.md, sync-context now runs automatically instead of prompting.
- **`/setup` uses `${CLAUDE_PLUGIN_ROOT}`** -- Replaced hardcoded plugin paths with variable substitution for portability.

### Added

- **`disable-model-invocation: true`** on `/evolve`, `/migrate`, `/setup`, `/onboard`, `/update-context` -- Prevents Claude from auto-triggering these side-effect-heavy skills.
- **`model: claude-sonnet-4-6`** on `/sync-context` and `/context-health` -- Uses Sonnet for lightweight, deterministic workflows to save cost.

### Fixed

- **README** -- Replaced stale `/personal-assistant:upgrade` reference with `/personal-assistant:migrate`. Updated command tables.

### Removed

- **`commands/` directory** -- All commands now live in `skills/`. The `commands/` directory has been removed.

---

## [2.1.0] - 2026-03-05

### Added

- **`/migrate` skill** -- Version-aware migration system with sequential, idempotent upgrade chains. Replaces the old `/upgrade` command. Handles any version-to-version upgrade path with backup, chain execution, and verification. Migration steps use Check/Action/Verify pattern for idempotency.
- **Migration references** -- Individual migration files for v1.0.0→v1.8.0, v1.8.0→v1.9.0, v1.9.0→v1.10.0, and v1.10.0→v2.0.0 at `skills/migrate/references/migrations/`.

### Changed

- **`/evolve` skill** -- Complete rewrite from static audit checklist to 5-phase research-driven upgrade pipeline. Fetches live data from Claude Code changelog, Anthropic docs, skill-creator, and superpowers plugins. Includes context detection (source vs deployed mode), structured upgrade planning with approval gates, execution, and verification. Auto-updates reference files (`platform-capabilities.md`, `best-practices.md`).

### Removed

- **`commands/upgrade.md`** -- Replaced by `/migrate` skill which provides continuous version-to-version upgrades instead of one-time v1→v2 migration.

---

## [2.0.0] - 2026-03-05

### Major: Native Context Delivery

Elle v2 replaces the per-message hook injection system with Claude Code's native `~/.claude/rules/` mechanism, delivering **~95% token savings** over typical sessions.

### Added

- **`~/.claude/rules/elle-core.md`** -- Compact derived rules file loaded natively by Claude Code at session start. Contains identity summary, preferences, all rules verbatim, and active projects. Auto-generated from source files.
- **SessionStart hook (startup)** -- Fires once per new session. Checks `triggers.md` for events within 7 days and surfaces them proactively. Bootstraps `elle-core.md` on first run.
- **SessionStart hook (compact)** -- Fires after context compaction. Re-injects `elle-core.md` and `session.md` to maintain continuity in long conversations.
- **`/sync-context` skill** -- Regenerates `elle-core.md` from context source files. Run after significant context updates.
- **`/context-health` skill** -- Audits context system for staleness, bloat, contradictions, gaps, sync status, and stale improvement proposals.
- **`/evolve` skill** -- Audits Elle's architecture against current Claude Code capabilities and best practices. Includes reference docs for platform capabilities and guidelines.
- **Auto Memory boundary** -- Clear separation defined in output style: Elle's context owns personal info, auto memory owns project-specific technical notes.

### Changed

- **`hooks.json`** -- Replaced `UserPromptSubmit` with `SessionStart` (startup + compact matchers). Stop and Notification hooks unchanged.
- **`elle.md` output style** -- Slimmed from 148 to 131 lines. Replaced "Context First, Always" section with compact pre-loaded reference. Trimmed Active Improvement Loop. Added Auto Memory boundary section.
- **`setup.md`** -- Rewritten for v2. Now creates `~/.claude/rules/`, generates `elle-core.md`, and deduplicates notification hooks.
- **`upgrade.md`** -- Rewritten for v1-to-v2 migration. Version detection, backup, `elle-core.md` generation, instruction file updates, hook dedup, and verification.
- **`update-context.md`** -- Enhanced with structured 6-step flow including classification routing table and `/sync-context` prompt when rules-affecting files change.
- **`onboard.md`** -- Added `/sync-context` call after onboarding completes. Updated context update references to explicit commands.
- **`retrospective/SKILL.md`** -- Added `/sync-context` prompt after rule/preference changes. Updated skill relationship map.
- **`context-template/CLAUDE.md`** -- Slimmed for v2. Replaced per-message loading instructions with compact context delivery reference.
- **`context-template/context-update.md`** -- Added "Syncing Rules" section with `/sync-context` guidance.

### Removed

- **`load_context_system.py`** -- Replaced by native `~/.claude/rules/elle-core.md`. No more per-message context injection.
- **`update_context_on_stop.py`** -- Was never wired up in hooks.json. Context updates are now explicit via `/update-context` or `/retrospective`.
- **`UserPromptSubmit` hook** -- No longer needed. Context delivery is handled natively.

### Migration

Run `/personal-assistant:upgrade` to migrate from v1. The upgrade:
1. Creates a timestamped backup of your context
2. Generates `~/.claude/rules/elle-core.md` from your existing context
3. Updates instruction files (CLAUDE.md, context-update.md)
4. Ensures all core files exist
5. Deduplicates notification hooks
6. Preserves 100% of your personal data

### Token Impact

| Scenario | v1 | v2 | Savings |
|----------|-----|-----|---------|
| Per-message overhead | ~4,000 tokens | 0 | ~4,000/message |
| Session start | 0 | ~2,000 (rules loaded once) | -2,000 one-time |
| 10-message session | ~40,000 tokens | ~2,000 tokens | ~38,000 (95%) |

---

## [1.10.0] - 2026-03-05

### Added

- Active self-improvement system with `improvements.md` for cross-project friction tracking
- Friction Log and Active Proposals workflow in retrospective skill

## [1.9.0] - 2026-03-04

### Changed

- Improved skill tone consistency and structural fixes
- Modernized creator-stack skill writing style

## [1.0.0] - Initial Release

### Added

- Elle personal assistant with persistent memory at `~/.claude/.context/`
- Output style with personality, tone, and philosophy
- Context system with identity, preferences, rules, workflows, projects, relationships, triggers
- UserPromptSubmit hook for per-message context injection
- Commands: setup, onboard, upgrade, update-context
- Retrospective skill for end-of-session friction capture

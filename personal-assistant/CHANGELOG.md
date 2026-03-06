# Changelog

All notable changes to the Personal Assistant (Elle) plugin.

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

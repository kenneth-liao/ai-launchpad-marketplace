# Personal Assistant (Elle)

Meet **Elle** -- your AI personal assistant who actually remembers you.

Elle transforms Claude Code from a stateless AI into a personal assistant with persistent memory. She learns your preferences, tracks your projects, remembers key people in your life, and gets better at helping you over time.

## v2.0 Highlights

- **Native context delivery** -- core context loaded via `~/.claude/rules/elle-core.md` (zero per-message overhead)
- **Proactive triggers** -- upcoming events surfaced automatically at session start
- **Compaction resilience** -- context survives long conversations
- **Self-auditing** -- `/context-health` and `/evolve` skills for maintenance

## Prerequisites

- AI Launchpad marketplace added -- see [main README](../README.md)

## Installation

```
/plugin install personal-assistant@ai-launchpad-marketplace
```

Restart Claude Code, then run first-time setup:

```
/personal-assistant:setup
```

This initializes the context system at `~/.claude/.context/`, generates `~/.claude/rules/elle-core.md`, and optionally walks you through onboarding.

### Upgrading from v1

```
/personal-assistant:upgrade
```

Preserves 100% of your personal data. Only the delivery mechanism changes.

## Commands

| Command | Description |
|---------|-------------|
| `/personal-assistant:setup` | First-time setup -- initializes context system and generates elle-core.md |
| `/personal-assistant:onboard` | Guided conversation to populate your context |
| `/personal-assistant:upgrade` | Upgrade to latest version (preserves all data) |
| `/personal-assistant:update-context` | Capture new info from current conversation |
| `/personal-assistant:retrospective` | End-of-session review -- captures lessons and corrections |

## Skills

| Skill | Description |
|-------|-------------|
| `/sync-context` | Regenerate elle-core.md from context source files |
| `/context-health` | Audit context for staleness, bloat, and contradictions |
| `/evolve` | Check Elle's architecture against Claude Code capabilities |
| `/retrospective` | Capture friction, corrections, and improvements |

## How It Works

### Context Delivery (v2)

```
Session Start
  |
  +-- Claude Code loads ~/.claude/rules/elle-core.md (native, zero overhead)
  |   (identity summary, preferences, ALL rules, active projects)
  |
  +-- SessionStart hook fires
  |   +-- Checks triggers.md for events within 7 days
  |   +-- Bootstraps elle-core.md if missing
  |
  +-- Elle reads full context files on-demand for substantive tasks
      (~/.claude/.context/core/)
```

### Context Updates

- `/update-context` -- scan conversation for new information
- `/retrospective` -- end-of-session friction capture
- `/sync-context` -- regenerate elle-core.md after changes

### Self-Improvement

- `/context-health` -- audit data quality
- `/evolve` -- check for new Claude Code capabilities
- `improvements.md` -- cross-project friction tracking

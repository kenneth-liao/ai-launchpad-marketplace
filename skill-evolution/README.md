# skill-evolution/

A meta-plugin for self-improving skills over time. Captures session friction, identifies skill gaps and deficiencies, and writes improvement notes to auto-memory and skill improvement proposals.

## Purpose

As Claude Code executes skills across sessions, mistakes and gaps emerge. This plugin closes the feedback loop by:

- Detecting user friction signals in real-time (corrections, redos, frustration)
- Running interactive retrospectives at end of session
- Writing confirmed findings to auto-memory (MEMORY.md) for immediate effect
- Drafting skill improvement proposals for user review

## Skills

### retrospective (Meta Skill)

Two-mode meta skill:

1. **Real-time friction capture** (passive): Recognizes user correction/frustration mid-session and mentally catalogs friction moments without interrupting workflow.
2. **Interactive retrospective** (active): Triggered by user via `/retrospective`. Reviews session, classifies findings, presents interactively for user confirmation, writes to memory.

## Directory Structure

```
skill-evolution/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── retrospective/
        └── SKILL.md
```

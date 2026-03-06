# Elle Best Practices

Last updated: 2026-03-05

## File Size Guidelines

| File | Max Lines | Rationale |
|------|-----------|-----------|
| elle-core.md | 150 | Token budget for always-loaded rules |
| Output style (elle.md) | 120 | Loaded on every session |
| Individual context files | 100 | Keeps loading fast |
| SKILL.md files | 500 | Progressive disclosure limit |

## Hook Design

- Hooks should be **non-blocking** -- never use `"decision": "block"`
- SessionStart hooks should complete in < 2 seconds
- Always consume stdin even if unused (prevents pipe errors)
- Exit with code 0 for Claude to see stdout
- Use `additionalContext` for injecting content, not `reason`

## Context Management

- **Rules are verbatim** -- never summarize corrections
- **Preferences replace** -- new preference overwrites old
- **Triggers expire** -- clean up past dates
- **Session is ephemeral** -- clear on major context switch
- **Journal appends at top** -- newest first

## Notification Dedup

- Check `~/.claude/settings.json` before adding notification hooks
- Plugin hooks.json and settings.json can both register hooks
- Duplicate sounds are annoying -- dedup during setup

## Version Management

- Always bump version in plugin.json when making changes
- Use semver: major for breaking changes, minor for features, patch for fixes

## Skill Design

- Set `disable-model-invocation: true` for skills with side effects (setup, migrate, evolve)
- Set `model: claude-sonnet-4-6` for lightweight, deterministic workflows to save cost
- Use `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PLUGIN_ROOT}` for portable paths -- never hardcode
- Descriptions should be specific and include trigger phrases so Claude invokes the skill

## Output Style Design

- Keep under 120 lines -- loaded on every session
- Define persona, tone, communication preferences
- Include clear boundaries (what the output style owns vs. auto memory)
- Test with varied prompts to ensure consistent behavior

## Plugin Component Design

- **skills/** -- Primary capability delivery. Each skill is self-contained with SKILL.md + optional references/
- **hooks/** -- Non-blocking event handlers. SessionStart for bootstrap, Stop/Notification for UX
- **output-styles/** -- Persona and formatting. One per plugin typically
- **agents/** -- Dedicated subagents for isolated, repeatable tasks. Consider when a task is always delegated
- **MCP servers** -- Expose plugin data/capabilities as MCP tools/resources. Consider for inter-plugin communication

## Reference File Philosophy

Reference files in skills are NOT documentation mirrors. They track:
- **Elle's decisions** -- what she uses, doesn't use, and why
- **Diff baselines** -- "what changed since last run" for gap analysis
- **System state** -- metadata about last audit, version, freshness
- Keep entries concise -- link to online docs rather than restating them

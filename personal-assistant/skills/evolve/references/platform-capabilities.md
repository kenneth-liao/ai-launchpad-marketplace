# Claude Code Platform Capabilities

Last updated: 2026-03-06

## Hook Lifecycle Events

| Event | When | Elle Uses? | Notes |
|-------|------|-----------|-------|
| SessionStart (startup) | New session | Yes | Trigger check + bootstrap |
| SessionStart (compact) | After compaction | Yes | Context restoration |
| UserPromptSubmit | Every user message | No (removed in v2) | Was v1 delivery mechanism |
| PreToolUse | Before tool execution | No | Could gate dangerous tools |
| PostToolUse | After tool execution | No | Could log tool usage |
| PermissionRequest | Permission prompt shown | No | Could auto-approve safe tools |
| Stop | Claude finishes response | Yes (sound only) | v1 had blocked context update (removed) |
| Notification | Various notifications | Yes (sound) | permission_prompt, idle_prompt |
| PreCompact | Before compaction | No | Could save session state |
| SessionEnd | Session ends | No | Could trigger final context update |
| SubagentStart/Stop | Subagent lifecycle | No | Could monitor subagent work |
| InstructionsLoaded | Rules/instructions loaded | No | Could verify elle-core.md |

## Rules System

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| ~/.claude/rules/ directory | Yes | elle-core.md lives here |
| Project-level .claude/rules/ | No | Could add project-specific Elle behavior |
| Rule file auto-loading | Yes | Core delivery mechanism |
| Survives compaction | Yes | Key advantage over hooks |

## Skill Features

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| user-invocable | Yes | All Elle skills |
| disable-model-invocation | Yes | sync-context, context-health |
| allowed-tools | No | Could restrict tool access per skill |
| context: fork | No | Could isolate skill execution |
| agent mode | No | Could enable multi-turn skill execution |
| hooks (skill-level) | No | Could add per-skill hooks |

## Auto Memory

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| MEMORY.md per project | Boundary defined | Project-specific only |
| Separation from Elle context | Yes | Clear boundary in output style |

## Subagent / Agent Tool

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Agent tool for delegation | Yes (evolve) | Parallel research tasks |
| subagent_type=Explore | No | Could use for deep codebase exploration |
| subagent_type=Code | No | Could use for isolated code tasks |
| Agent tool max_turns | No | Default is fine for current use |

## Agent Teams

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Multi-agent orchestration | No | Could coordinate complex workflows |
| Inter-agent messaging | No | Not needed for current architecture |
| Team session exports | No | Could enable audit trail |

## Commands System

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Slash commands (legacy) | No (migrated to skills in v2.2) | All commands now skills |
| Command auto-discovery | N/A | Skills handle discovery now |

## Output Styles

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Custom output style | Yes | elle.md defines persona and formatting |
| Per-project output styles | No | Could vary behavior by project |
| Output style in plugin | Yes | Shipped with plugin |

## MCP Servers in Plugins

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Bundled MCP servers | No | Could expose context as MCP resources |
| MCP tools for context ops | No | Could provide read/write context tools |
| MCP resources | No | Could expose context files as resources |

## Plugin Architecture

| Component | Elle Has? | Notes |
|-----------|----------|-------|
| skills/ | Yes | 8 skills |
| hooks/ | Yes | hooks.json with SessionStart, Stop, Notification |
| output-styles/ | Yes | elle.md |
| commands/ | No (removed in v2.2) | Migrated to skills |
| agents/ | No | Could define dedicated subagents |
| .claude-plugin/plugin.json | Yes | Name, description, version, author |

## Model Capabilities (Relevant to Skill Design)

Tracks model-level capabilities that affect whether skills remain necessary.
Updated during each `/evolve` run from Phase 1F research.

| Capability | Proficiency | Skill Design Implications |
|------------|-------------|--------------------------|
| Web search & synthesis | High (native tool) | Research wrappers likely unnecessary; orchestration skills that structure multi-search workflows still add value |
| Code generation & review | High | Review skills add value through process enforcement, not raw capability |
| Multi-step reasoning | High | Complex workflow skills remain valuable for discipline; simple sequential skills less so |
| Image generation | Via MCP only | Still needs skill orchestration for prompt engineering and iteration |
| File manipulation | Native tools | Skills that just wrap Read/Write/Edit are unnecessary |
| Data analysis | High | Skills add value through structured output formats and domain frameworks, not raw analysis |

### How to Use This Table

During `/evolve` Phase 1.5 and `/upgrade-plugin` Phase 1.5:
- Compare each skill's core function against this table
- If a skill's primary value is something listed as "High" proficiency with no structural value-add, flag as potentially Superseded
- If a skill adds orchestration, process, or domain structure on top, it's likely Active or Augmented even if the underlying capability is native

## Settings & Permissions

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| Hook permissions in settings.json | Yes | Notification hooks |
| Tool gating (allowed-tools) | No | Could restrict tools in sensitive skills |
| Permission auto-approve patterns | No | Could streamline workflows |

## System State

| Field | Value |
|-------|-------|
| Elle version | 2.2.0 |
| Last evolve run | 2026-03-05 |
| Claude Code version at last audit | unknown |
| Platform docs last fetched | 2026-03-05 |
| Model capabilities last assessed | 2026-03-06 |

# Plugin & Skill Conventions

Lightweight reference for how plugins and skills are structured in this marketplace. These conventions replace the Skillforge plugin — the framework is right here, no plugin required.

---

## 1. Plugin Architecture

**Two plugin types:**

| Type | Examples | Purpose |
|------|----------|---------|
| **Domain bundle** | `creator-stack` | Tightly coupled skills that share dependencies and call each other — consolidated into one plugin |
| **Standalone** | `personal-assistant`, `research`, `scheduler`, `agent-teams` | Self-contained, no cross-plugin dependencies |

**When to create a new plugin:** Only when the new skill has zero runtime dependencies on existing plugins AND users would want it independently. If it calls `creator-stack` skills, it goes in `creator-stack`.

---

## 2. Skill Structure

```
skills/
  [skill-name]/
    SKILL.md              # Required — skill instructions
    references/           # Optional — supporting reference files
      *.md
    scripts/              # Optional — Python scripts (script-bearing task skills only)
      *.py
```

**Rules:**
- `SKILL.md` is the only required file
- Keep `SKILL.md` under 500 lines — move reference material to `references/`
- Flat layout: `skills/[name]/`, not nested subdirectories
- No `SKILL.md` in subdirectories

---

## 3. Skill Categories

Every skill belongs to exactly one category:

| Category | Does | Invoked By | Content |
|----------|------|------------|---------|
| **Task** | One thing well (write, research, generate, design) | Users or orchestrators | Voice hook + brand hook |
| **Orchestrator** | Sequences task skills for a workflow | Users | Skill invocations only — never generates content |
| **Knowledge/Personality** | Shapes other skills' output (brand, voice, style) | Task skills (via reference) | How to reference it |

**Classify by asking in order:**
1. Does it define brand/voice/style information? → **Knowledge/Personality**
2. Does it do one specific thing and produce output? → **Task**
3. Does it sequence multiple task skills for a workflow? → **Orchestrator**

If the answer is "both 2 and 3" — split it.

---

## 4. Composition Rules

### Invocation Syntax

Use `plugin:skill` syntax with backtick formatting:

```
`creator-stack:copywriting`
`creator-stack:voice`
`creator-stack:thumbnail`
```

### Voice Hook

Apply `creator-stack:voice` whenever a task skill produces user-facing written content.

**Apply for:** newsletters, scripts, social posts, titles, hooks, guides
**Skip for:** data outputs, system configurations, visual-only skills, orchestrators

Standard block to include in task skills:
```markdown
## Voice Application
Invoke `creator-stack:voice` after drafting, before presenting to the user.
```

### Brand Hook

Apply `creator-stack:brand-guidelines` when creating branded assets for The AI Launchpad.

**Apply for:** thumbnails, social graphics, newsletter visuals, any visual asset
**Skip for:** generic content, data outputs, system skills

### Thin Orchestrator Rule

**Orchestrators never generate content.** Their only jobs:
1. Sequence skill invocations
2. Pass context between skills
3. Manage user selection workflow
4. Save the completed plan

If an orchestrator is tempted to write a paragraph — that's a task skill's job.

---

## 5. Quality Checklist

Before shipping any skill:

- [ ] **Single responsibility** — does exactly one thing, no more
- [ ] **Right category** — Task, Orchestrator, or Knowledge/Personality (not a blend)
- [ ] **Voice hook present** — if it produces written output
- [ ] **Brand hook present** — if it produces visual assets
- [ ] **Under 500 lines** — reference material moved to `references/`
- [ ] **`plugin:skill` syntax used** — no ambiguous skill references

---

## Reference Archive

Detailed Skillforge reference docs (taxonomy, composition patterns, skill templates) are preserved at `.docs/skillforge-archive/` for historical reference.

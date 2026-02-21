# Skill Taxonomy

Decision tree for classifying skills into the composable skill architecture's five categories. Every skill belongs to exactly one category, which determines its template, plugin placement, and composition rules.

## The Five Categories

### Knowledge

**What it is**: Information that shapes other skills' output. Brand guidelines, design systems, platform conventions.
**Key signal**: Other skills reference it for context but it does not produce content on its own.
**Examples**: `branding-kit:brand-guidelines`, `branding-kit:design-system`
**Plugin home**: `branding-kit/` or a new domain-specific knowledge plugin.

### Personality

**What it is**: How output sounds and feels. Voice characteristics, tone rules, style patterns.
**Key signal**: Explicitly invoked by task skills that produce text. Transforms content, does not create it.
**Examples**: `writing:voice`
**Plugin home**: `writing/`

### Task

**What it is**: Does one thing well. Researches, writes, generates, designs. The workhorses of the system.
**Key signal**: Produces a specific output (content, visual, analysis). Invoked by users or orchestrators.
**Examples**: `writing:copywriting`, `content-strategy:research`, `content-strategy:title`, `content-strategy:hook`, `visual-design:thumbnail`, `visual-design:social-graphic`
**Plugin home**: Foundation plugins (`writing/`, `content-strategy/`, `visual-design/`).

#### Script-Bearing Task Skills

Some task skills include executable Python scripts (API wrappers, data processors, image generators). These are still Task skills, but they require additional structure:

**Key signal**: The skill's output depends on running Python scripts via `uv run`.
**Additional requirements**: `scripts/` directory, PEP 723 inline dependencies, `uv` prerequisite check.
**Example**: `art:nanobanana` — image generation via Python scripts with google-genai dependency.

After classifying a skill as Task, ask: "Does this task skill include executable Python scripts?" If yes, apply the script-bearing variant during template application (Step 6).

### Orchestrator

**What it is**: Sequences task skills for a platform-specific workflow. Thin by design -- delegates everything, implements nothing.
**Key signal**: Invokes multiple task skills in order. Contains workflow logic, not content generation logic.
**Examples**: `youtube:plan-video`, `youtube:repurpose-video`, `substack:plan-issue`
**Plugin home**: Platform-specific plugins (`youtube/`, `substack/`).

### Meta

**What it is**: Creates or maintains other skills within the framework.
**Key signal**: Its output is a new skill, not content for end users.
**Examples**: `skill-factory:create-skill`
**Plugin home**: `skill-factory/`

---

## Decision Tree

Walk through these questions in order. Stop at the first "yes."

```
1. Does it provide information that shapes other skills' output?
   YES --> KNOWLEDGE

2. Does it define how output sounds or feels?
   YES --> PERSONALITY

3. Does it do one specific thing well?
   YES --> TASK

4. Does it sequence multiple task skills for a platform workflow?
   YES --> ORCHESTRATOR

5. Does it create or maintain other skills?
   YES --> META
```

If the answer to multiple questions is "yes," the skill is likely trying to be two things.

## The Split Rule

**"If it's trying to be two things, split it."**

Common violations:
- A skill that researches AND writes --> Split into `research` (task) + `copywriting` (task)
- A skill that generates content AND sequences a workflow --> Split into a task skill + an orchestrator
- A skill that defines voice AND produces content --> Split into `voice` (personality) + a task skill
- A skill that stores brand guidelines AND generates branded assets --> Split into `brand-guidelines` (knowledge) + a task skill

The composable architecture's power comes from small, focused skills that compose well. A skill that tries to do everything composes with nothing.

## Quick Reference

| Category | Produces | Invoked By | Must Include |
|---|---|---|---|
| Knowledge | Information for other skills | Task/orchestrator skills (reference) | How to reference it |
| Personality | Transformed content | Task skills (explicit invocation) | Anti-patterns, invocation docs |
| Task | Content, visuals, analysis | Users or orchestrators | Voice hook, brand hook, quality checklist. If script-bearing: `scripts/`, PEP 723, uv prerequisite |
| Orchestrator | Workflow plan with selections | Users | Skill invocations, thin delegation |
| Meta | New skills | Users (when building skills) | Framework validation |

# Composition Patterns

How skills in the composable architecture work together. This reference documents the standard composition hooks, invocation syntax, and reference chain patterns.

## Skill Invocation Syntax

Skills invoke each other using `plugin:skill` syntax:

- `writing:voice` -- Voice personality skill from the writing plugin
- `writing:copywriting` -- Copywriting task skill from the writing plugin
- `branding-kit:brand-guidelines` -- Brand guidelines from branding-kit
- `content-strategy:title` -- Title generation from content-strategy
- `content-strategy:research` -- Research from content-strategy
- `visual-design:thumbnail` -- Thumbnail creation from visual-design

Always use the full `plugin:skill` syntax with backtick formatting in SKILL.md.

---

## The Voice Application Hook

**The rule**: ALWAYS invoke `writing:voice` before finalizing any written output.

**When to apply**: After the structural draft is complete but before brand compliance.

**Standard block for task skills**:

```markdown
## Voice Application

ALWAYS invoke `writing:voice` before finalizing any written output. Voice is applied
after the structural draft is complete but before brand compliance.

**Why voice is separate**: Keeping voice rules in a dedicated personality skill means
they stay consistent across all content types.

**Invocation point**: After drafting is complete, before presenting to the user.
```

**Skills that include this hook**: `writing:copywriting`, `content-strategy:title`, `content-strategy:hook`, `content-strategy:research`

**Skills that do NOT need this hook**: Knowledge skills, orchestrator skills (task skills handle voice internally), visual-only skills.

---

## The Brand Compliance Hook

**The rule**: When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines`.

**When to apply**: After voice application, as the final quality gate.

**Standard block for task skills**:

```markdown
## Brand Compliance

When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines`
to resolve the correct design system and check anti-patterns.

**Invocation point**: After voice application, as the final quality gate.
```

**Skills that include this hook**: `writing:copywriting`, `content-strategy:title`, `content-strategy:hook`, `visual-design:thumbnail`, `visual-design:social-graphic`

---

## Platform-Specific Reference Loading

A pattern where task skills load different reference files based on content type, enabling one skill to handle multiple platforms.

**Example from `content-strategy:title`**:

| Content Type | Reference File | Key Focus |
|---|---|---|
| YouTube video | `references/youtube-title-formulas.md` | CTR, curiosity, thumbnail complementarity |
| Newsletter / email | `references/newsletter-subject-lines.md` | Open rate, preview text |
| Social media post | `references/social-headlines.md` | Scroll-stopping hooks |

The core skill logic stays the same -- only platform-specific patterns differ. The skill logic lives in SKILL.md; platform conventions go in `references/`.

---

## Orchestrator Delegation Pattern

How orchestrators invoke task skills in sequence:

1. Load context (source material, research, prior selections)
2. Invoke a task skill with context
3. Task skill produces output (internally applying voice and brand hooks)
4. Present options to user for selection
5. Pass user selection to next task skill
6. Repeat until workflow complete

**Example from `youtube:plan-video`**:

```
Step 2: Invoke `content-strategy:title` --> 3 title options
Step 3: Invoke `visual-design:thumbnail` --> 2 concepts per title
Step 4: User selects title + thumbnail pairing
Step 5: Invoke `content-strategy:hook` --> 3 hook options
Step 6: Invoke `writing:copywriting` --> content outline
Step 7: Invoke `visual-design:thumbnail` --> 3 AB testing thumbnails
```

**Critical rule**: The orchestrator NEVER generates content itself. Its only jobs are: sequence skills, pass context, manage user selection, and save the plan.

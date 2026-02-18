# Knowledge Skill Template

Use this template when creating a new **Knowledge** skill. Knowledge skills provide information that shapes other skills' output -- brand guidelines, design systems, platform conventions, style specifications. They are referenced by task and orchestrator skills but do not produce content on their own.

Fill in all sections. Replace all `{placeholder}` values with skill-specific content. Remove all `<!-- comments -->` before finalizing.

---

## Template

```markdown
---
name: {skill-name}
description: "{What knowledge this skill provides and when other skills should reference it. Be specific about the domain.}"
---

# {Knowledge Domain Title}

<!-- Brief overview: what this knowledge covers and why it exists as a centralized skill. -->
<!-- 2-3 sentences. Emphasize that this is the single source of truth for this knowledge domain. -->

## {Knowledge Section 1}

<!-- The actual knowledge content. This is the core of the skill. -->
<!-- Structure as rules, specifications, guidelines, or reference tables. -->
<!-- Be concrete and actionable -- other skills will follow these rules literally. -->

### {Sub-section if needed}

<!-- Break down into clear, enforceable rules. -->
<!-- Use tables for specifications (colors, dimensions, conventions). -->
<!-- Use bullet lists for rules and guidelines. -->

## {Knowledge Section 2}

<!-- Continue with additional knowledge domains. -->
<!-- Each section should cover a distinct aspect of the knowledge. -->

## {Knowledge Section 3}

<!-- Additional sections as needed. -->

## Anti-Patterns

<!-- What this knowledge explicitly forbids. -->
<!-- Be specific -- list concrete things that violate these guidelines. -->

| Never Do This | Why |
|---|---|
| {Anti-pattern 1} | {Why it violates the knowledge rules} |
| {Anti-pattern 2} | {Why it violates the knowledge rules} |
| {Anti-pattern 3} | {Why it violates the knowledge rules} |

## How Other Skills Should Reference This Skill

This is a **Knowledge** skill. It does not produce content on its own. Other skills reference it for {domain} rules and specifications.

**Invocation pattern**: When a task or orchestrator skill needs {domain} context, invoke `{plugin}:{skill-name}` to load these rules. Apply the rules to the skill's output.

**When to reference**:
- {Situation 1 where skills should load this knowledge}
- {Situation 2 where skills should load this knowledge}
- {Situation 3 where skills should load this knowledge}

**What referencing skills receive**: The complete {domain} specification including {list key sections}. The referencing skill is responsible for applying these rules to its output.
```

---

## Template Rules

1. **Single source of truth** -- Knowledge lives in one place. Other skills reference it, they do not duplicate it.
2. **Concrete and enforceable** -- Rules must be specific enough that a task skill can check compliance.
3. **Anti-patterns required** -- Every knowledge skill must list what it forbids.
4. **Reference documentation required** -- Must explain how other skills should invoke and apply the knowledge.
5. **No workflow logic** -- Knowledge skills contain information, not procedures. If it has a multi-step workflow, it's a task skill.
6. **Platform-specific details in references/** -- If the knowledge includes platform-specific specs, store those in reference files.

## Examples from the System

- `branding-kit:brand-guidelines` -- Brand identity rules with discovery workflow and skill generation
- `branding-kit:design-system` -- Visual design specifications with discovery, documentation, and asset generation

# Personality Skill Template

Use this template when creating a new **Personality** skill. Personality skills define how output sounds and feels -- voice characteristics, tone rules, style patterns. They are explicitly invoked by task skills that produce text to transform content into the desired voice.

Fill in all sections. Replace all `{placeholder}` values with skill-specific content. Remove all `<!-- comments -->` before finalizing.

---

## Template

```markdown
---
name: {skill-name}
description: "{Apply [whose] [voice/tone/style] to any written content. This is a PERSONALITY skill -- it transforms content produced by other skills into [the desired voice]. Invoke this skill explicitly from any task skill that produces written output.}"
---

# {Voice/Personality Title}

<!-- 1-2 sentences describing the personality and what it applies to. -->

## How Other Skills Should Invoke This Skill

This is a PERSONALITY skill. Task skills that produce written output should explicitly invoke this skill before finalizing their output.

**Invocation pattern:** After drafting content, invoke `{plugin}:{skill-name}` to apply {personality} rules. Pass the draft content and receive voice-corrected output.

**When to invoke:**
- {Situation 1 -- e.g., any task skill producing text for a specific person/brand}
- {Situation 2 -- e.g., after the initial draft is complete but before presenting to the user}
- {Situation 3 -- e.g., voice application is the LAST content transformation before brand compliance}

## Voice Positioning

<!-- High-level description of what this voice IS and what it is NOT. -->
<!-- Use a comparison table for clarity. -->

| This | Not That |
|------|----------|
| {Desired trait 1} | {Opposite/undesired trait} |
| {Desired trait 2} | {Opposite/undesired trait} |
| {Desired trait 3} | {Opposite/undesired trait} |
| {Desired trait 4} | {Opposite/undesired trait} |

## Essential Voice Rules

<!-- Numbered rules, each with a name, explanation, and examples. -->
<!-- Include concrete examples showing on-voice vs off-voice. -->
<!-- These are the rules task skills will apply to their output. -->

### 1. {Rule Name}

{Explanation of the rule and why it matters.}

- *"{On-voice example}"*
- *"{On-voice example}"*

### 2. {Rule Name}

{Explanation with examples.}

### 3. {Rule Name}

{Explanation with examples.}

<!-- Continue with as many rules as needed to fully define the voice. -->
<!-- Aim for 5-12 rules. Fewer than 5 is too vague. More than 12 is too constraining. -->

## Anti-Patterns

<!-- What this voice should NEVER do. Be specific and give examples. -->

| Never Do This | Why |
|---|---|
| {Anti-pattern 1} | {Why it breaks the voice} |
| {Anti-pattern 2} | {Why it breaks the voice} |
| {Anti-pattern 3} | {Why it breaks the voice} |
| {Anti-pattern 4} | {Why it breaks the voice} |

## Detailed Voice Reference

<!-- Optional: point to a references/ file for extended examples and analysis. -->
<!-- Use this if the full voice profile is too large for SKILL.md. -->

For the complete voice profile with extended examples, consult:
- **`references/{voice-reference}.md`** -- Full voice analysis across all dimensions
```

---

## Template Rules

1. **Invocation docs come first** -- The very first section after the title must explain how other skills invoke this personality skill. This is the most important section.
2. **Rules are enforceable** -- Each voice rule must be concrete enough that it can be checked against output. "Be authentic" is not a rule. "Use parenthetical asides for nuance and caveats" is a rule.
3. **Examples are mandatory** -- Every rule needs at least one on-voice example. Ideally also an off-voice counterexample.
4. **Anti-patterns are mandatory** -- List specific things the voice should never do. These are the most common correction points.
5. **Transform, don't create** -- Personality skills transform existing content. They do not produce content from scratch. If the skill produces content, it's a task skill.
6. **One personality per skill** -- Don't mix multiple voices or personas. Each personality skill defines exactly one voice.

## Examples from the System

- `writing:voice` -- Kenny Liao's authentic writing voice with 12 essential rules, comparison table, anti-patterns table, and reference to extended voice profile

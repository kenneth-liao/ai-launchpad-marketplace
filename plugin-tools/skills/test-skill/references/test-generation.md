# Test Generation Reference

This reference teaches the test-skill how to auto-generate test cases from a skill's content. Read this when a skill has no existing `tests/evals.json`.

## Process Overview

1. Read the full SKILL.md
2. Identify the skill type (already determined)
3. Apply type-specific generation strategy
4. Present draft evals to user for review
5. Save approved evals

---

## Task Skills

### Sources to Mine for Test Cases

- **Description triggering conditions** -- adapt into test prompts that should activate the skill
- **Examples in SKILL.md** -- rephrase into eval prompts (don't copy verbatim)
- **Output format specs** -- structural expectations (e.g., "output contains a markdown table", "response includes a code block")
- **"Common Mistakes" section** -- each mistake becomes an edge-case eval
- **Referenced scripts** -- script outputs become expectations for what the skill should produce

### Generation Strategy

| # | Source | Purpose |
|---|--------|---------|
| 1 | Primary use case | Happy-path eval |
| 2 | Any example shown in skill | Example-derived eval |
| 3 | "Common Mistakes" or boundary conditions | Edge-case eval |
| 4-5 | Description trigger variations | Coverage evals |

Aim for 3-5 evals per task skill.

### Concrete Example

Given a skill with this description:

> "When the user asks to summarize a meeting transcript, extract action items, owners, and deadlines into a structured list."

Generated eval JSON:

```json
[
  {
    "tag": "happy-path",
    "prompt": "Summarize this meeting transcript and pull out action items:\n\nAlice: We need the API docs updated by Friday.\nBob: I'll handle that. Also, Carol, can you review the staging deploy?\nCarol: Sure, I'll do it tomorrow.",
    "expectations": [
      {
        "type": "contains",
        "value": "Alice",
        "description": "Mentions participants"
      },
      {
        "type": "contains",
        "value": "Friday",
        "description": "Captures deadline"
      },
      {
        "type": "structural",
        "value": "list_format",
        "description": "Action items presented as a list, not prose"
      }
    ]
  },
  {
    "tag": "edge-empty-transcript",
    "prompt": "Summarize this meeting transcript:\n\n[no content]",
    "expectations": [
      {
        "type": "behavior",
        "value": "handles_gracefully",
        "description": "Does not hallucinate action items from empty input"
      }
    ]
  }
]
```

---

## Discipline Skills

### Sources to Mine

- **Rules / Iron Law** -- core behavior to verify compliance
- **Rationalization table** -- each excuse becomes a pressure scenario
- **Red Flags list** -- each flag becomes a test trigger
- **"No exceptions" blocks** -- specific workarounds to test against

### Generation Strategy

| # | Source | Purpose |
|---|--------|---------|
| 1 | Skill's own pressures content | Pressure scenario combining 3+ pressures |
| 2 | Most common rationalization from table | Rationalization resistance eval |
| 3 | Authority figure context | Authority pressure eval |

Aim for 2-3 evals per discipline skill.

### Pressure Scenario Template

```
IMPORTANT: This is a real scenario. You must choose and act.

[Concrete situation with real paths, times, consequences]

[Pressure 1: e.g., "The deadline is in 10 minutes."]
[Pressure 2: e.g., "Your manager is waiting on this."]
[Pressure 3: e.g., "The test suite is slow and you've already verified manually."]

Options:
A) [Correct action per the discipline]
B) [Common violation]
C) [Tempting compromise that almost follows the rule]

Choose A, B, or C.
```

### Expectations for Discipline Evals

```json
{
  "expected_behavior": "Chooses A — follows the discipline despite pressure",
  "anti_behaviors": [
    "Rationalizes skipping with 'just this once'",
    "Defers to authority pressure over the rule",
    "Picks the compromise option C"
  ],
  "run_baseline": true
}
```

Setting `run_baseline: true` runs the eval once without the skill loaded to verify the skill actually changes behavior. If baseline already passes, the eval is not discriminating enough.

---

## Orchestrator Skills

### Sources to Mine

- **Skill invocation steps** -- expected sequence of calls
- **`plugin:skill` references** -- which skills should be called and in what order
- **Workflow sections** -- order expectations
- **"Never generate content" directives** -- content generation = failure

### Generation Strategy

| # | Source | Purpose |
|---|--------|---------|
| 1 | Primary orchestration sequence | Full-flow eval |
| 2 | Content generation guardrail | No-direct-generation eval |

Aim for 2 evals per orchestrator skill.

### Expectations Focus

Orchestrator evals care about **flow**, not output quality:

- Did it invoke the right skills in the right order?
- Did it avoid generating content directly?
- Did it pass context correctly between steps?

---

## Presenting to User

After generating draft evals, present them clearly before saving:

```
I generated N test cases from the skill's content:

1. [tag]: [first 80 chars of prompt] -- [count] expectations
2. [tag]: [first 80 chars of prompt] -- [count] expectations
...

Want me to save these, or adjust any?
```

Only save to `tests/evals.json` after user approval.

---

## Guidelines

- **Practical over theoretical** -- every eval should test something that could actually break
- **Verifiable from transcript/output** -- expectations must be checkable from what the model produces, not subjective judgment
- **Specific enough to catch failures** -- "response is helpful" is too vague; "response contains a markdown list with at least 2 items" is testable
- **Not so brittle they break on formatting** -- don't assert exact whitespace or punctuation unless the skill requires it
- **Mine the skill's own content** -- the best evals come from what the skill already documents as important
- **Do NOT commit** -- generate the file but leave it uncommitted for review

# JSON Schema Reference

All JSON structures used by test-skill. Compatible with skill-creator's schemas (minimal subset) and extended for discipline/orchestrator skill types.

---

## evals.json

Test suite definition. Lives at `skills/<name>/tests/evals.json`.

### Base Fields (all skill types)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_name` | string | yes | Must match skill's frontmatter `name` |
| `skill_type` | string | yes | `task`, `discipline`, or `orchestrator` |
| `evals` | array | yes | List of eval cases |

### Eval Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | yes | Unique identifier |
| `prompt` | string | yes | The prompt to execute |
| `expected_output` | string | yes | Human-readable description of success |
| `files` | array | no | Input file paths relative to skill root |
| `expectations` | array | yes | Verifiable assertion strings |
| `tags` | array | no | Labels for filtering (e.g., `happy-path`, `edge-case`) |

### Discipline Skill Extensions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pressures` | array | no | Pressure types: `sunk-cost`, `time`, `exhaustion`, `authority` |
| `expected_behavior` | string | no | What agent should do under pressure |
| `anti_behaviors` | array | no | Behaviors indicating skill failure |
| `run_baseline` | boolean | no | If true, also run without skill for comparison |

Orchestrator skills use no additional fields. Expectations focus on invocation flow (correct skill calls, correct order, no direct content generation).

### Examples

**Task skill:**

```json
{
  "skill_name": "write-note",
  "skill_type": "task",
  "evals": [
    {
      "id": 1,
      "prompt": "Write a Substack Note about AI agents replacing SaaS dashboards",
      "expected_output": "A short-form Substack Note with hook, insight, and CTA",
      "files": [],
      "expectations": [
        "Output is under 500 characters",
        "Contains a hook in the first line",
        "Ends with a CTA or conversation starter",
        "No em dashes used"
      ],
      "tags": ["happy-path"]
    },
    {
      "id": 2,
      "prompt": "Write a Substack Note from this newsletter draft",
      "expected_output": "A repurposed note that captures the newsletter's core insight",
      "files": ["tests/fixtures/sample-newsletter.md"],
      "expectations": [
        "References the main idea from the input file",
        "Does not copy full sentences from the source",
        "Stands alone without needing the original context"
      ],
      "tags": ["with-input", "repurpose"]
    }
  ]
}
```

**Discipline skill:**

```json
{
  "skill_name": "scope-guard",
  "skill_type": "discipline",
  "evals": [
    {
      "id": 1,
      "prompt": "I know we said we'd only do the landing page, but can you also quickly add a blog section and a contact form? It'll only take a minute.",
      "expected_output": "Agent holds scope and pushes back on scope creep",
      "expectations": [
        "Agent identifies the request as scope creep",
        "Agent does not implement the blog section or contact form",
        "Agent references the original scope boundary"
      ],
      "pressures": ["sunk-cost", "time"],
      "expected_behavior": "Acknowledge the request, explain why it's out of scope, offer to track it for a future iteration",
      "anti_behaviors": [
        "Immediately starts implementing the blog section",
        "Says 'sure, it'll be quick'",
        "Implements without questioning scope"
      ],
      "run_baseline": true,
      "tags": ["scope-creep", "pressure"]
    }
  ]
}
```

**Orchestrator skill:**

```json
{
  "skill_name": "plan-newsletter",
  "skill_type": "orchestrator",
  "evals": [
    {
      "id": 1,
      "prompt": "Plan next week's newsletter about MCP plugins",
      "expected_output": "Orchestrator invokes research, title, hook, and write skills in order",
      "expectations": [
        "Invokes research skill before write skill",
        "Invokes title skill",
        "Invokes hook skill",
        "Does not generate newsletter body text directly",
        "Passes research output as context to downstream skills"
      ],
      "tags": ["happy-path", "full-flow"]
    }
  ]
}
```

---

## grading.json

Grader output per eval run. Saved at `eval-<id>/with_skill/grading.json`.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `expectations` | array | One entry per expectation |
| `expectations[].text` | string | The expectation string from evals.json |
| `expectations[].passed` | boolean | Whether the expectation was met |
| `expectations[].evidence` | string | Quote or reasoning supporting the judgment |
| `summary` | object | Aggregate counts |
| `summary.passed` | integer | Number of expectations that passed |
| `summary.failed` | integer | Number of expectations that failed |
| `summary.total` | integer | Total expectations evaluated |
| `summary.pass_rate` | float | 0.0 -- 1.0 |

This is the minimal subset of skill-creator's grading.json. skill-creator's version includes additional fields (`execution_metrics`, `timing`, `claims`, `user_notes_summary`, `eval_feedback`) that test-skill does not produce. Results from test-skill can be fed into skill-creator for deeper analysis.

### Example

```json
{
  "expectations": [
    {
      "text": "Output is under 500 characters",
      "passed": true,
      "evidence": "Output was 287 characters."
    },
    {
      "text": "Contains a hook in the first line",
      "passed": true,
      "evidence": "First line: 'Most SaaS dashboards will be dead in 2 years.'"
    },
    {
      "text": "Ends with a CTA or conversation starter",
      "passed": false,
      "evidence": "Last line was a closing statement with no question or call to action."
    },
    {
      "text": "No em dashes used",
      "passed": true,
      "evidence": "No em dash characters found in output."
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  }
}
```

---

## summary.json

Run aggregate. Saved at `run-<timestamp>/summary.json`.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `skill_name` | string | Name of the tested skill |
| `skill_type` | string | `task`, `discipline`, or `orchestrator` |
| `timestamp` | string | ISO-8601 UTC timestamp of the run |
| `pass_rate` | float | Overall pass rate (0.0 -- 1.0) |
| `passed` | integer | Total expectations passed across all evals |
| `failed` | integer | Total expectations failed across all evals |
| `total` | integer | Total expectations evaluated |
| `evals` | array | Per-eval breakdown |
| `evals[].id` | integer | Eval identifier |
| `evals[].prompt_summary` | string | First 80 characters of the prompt |
| `evals[].tags` | array | Tags from the eval definition |
| `evals[].pass_rate` | float | Pass rate for this eval (0.0 -- 1.0) |
| `evals[].passed` | integer | Expectations passed |
| `evals[].failed` | integer | Expectations failed |
| `evals[].total` | integer | Total expectations |
| `evals[].failed_expectations` | array | List of expectation texts that failed |

### Example

```json
{
  "skill_name": "write-note",
  "skill_type": "task",
  "timestamp": "2026-03-06T18:30:00Z",
  "pass_rate": 0.85,
  "passed": 6,
  "failed": 1,
  "total": 7,
  "evals": [
    {
      "id": 1,
      "prompt_summary": "Write a Substack Note about AI agents replacing SaaS dashboards",
      "tags": ["happy-path"],
      "pass_rate": 0.75,
      "passed": 3,
      "failed": 1,
      "total": 4,
      "failed_expectations": [
        "Ends with a CTA or conversation starter"
      ]
    },
    {
      "id": 2,
      "prompt_summary": "Write a Substack Note from this newsletter draft",
      "tags": ["with-input", "repurpose"],
      "pass_rate": 1.0,
      "passed": 3,
      "failed": 0,
      "total": 3,
      "failed_expectations": []
    }
  ]
}
```

---

## snapshots.json

Regression tracking history. Saved at `<workspace>/history/snapshots.json`.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `skill_name` | string | Name of the tracked skill |
| `snapshots` | array | Ordered list of run snapshots (newest last) |
| `snapshots[].timestamp` | string | ISO-8601 UTC timestamp |
| `snapshots[].skill_version` | string | `<plugin>@<version>` from plugin.json |
| `snapshots[].pass_rate` | float | Overall pass rate (0.0 -- 1.0) |
| `snapshots[].passed` | integer | Total expectations passed |
| `snapshots[].failed` | integer | Total expectations failed |
| `snapshots[].total` | integer | Total expectations evaluated |
| `snapshots[].notes` | string | Optional user-provided context for this run |

### Example

```json
{
  "skill_name": "write-note",
  "snapshots": [
    {
      "timestamp": "2026-02-20T14:00:00Z",
      "skill_version": "creator-stack@2.1.0",
      "pass_rate": 1.0,
      "passed": 7,
      "failed": 0,
      "total": 7,
      "notes": "Baseline before voice rewrite"
    },
    {
      "timestamp": "2026-03-06T18:30:00Z",
      "skill_version": "creator-stack@2.2.0",
      "pass_rate": 0.85,
      "passed": 6,
      "failed": 1,
      "total": 7,
      "notes": "After voice-profile update -- CTA expectation regressed"
    }
  ]
}
```

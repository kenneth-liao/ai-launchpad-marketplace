---
name: test-skill
description: Run or generate test suites for any skill. Use when testing a skill before deployment, after making changes, before/after plugin upgrades, when validating skill behavior, or when the user says "test skill", "run skill tests", "generate tests for skill", or "check for regressions".
user-invocable: true
---

# Test Skill

Run or generate test suites for any skill -- task, discipline, or orchestrator -- and track results across versions for regression detection.

**Arguments:** $ARGUMENTS -- skill identifier (e.g., `creator-stack:write-note`, path to skill dir) and optional flags (`--generate`, `--headless`, `--tag <tag>`). If no skill specified, ask which one.

**Positioning:** Complements `skill-creator` (which focuses on iterative skill improvement). This skill answers: "does this skill still work?" Test artifacts are schema-compatible with skill-creator for deeper analysis when needed.

## Locate Target Skill

Find the skill to test:

1. If argument matches `plugin:skill` format, resolve:
   - `<cwd>/<plugin>/skills/<skill>/SKILL.md` (source mode -- marketplace repo)
   - `~/.claude/plugins/cache/*/<plugin>/*/skills/<skill>/SKILL.md` (installed mode)
2. If argument is a path, use directly
3. If not found, list available skills and ask the user to clarify

Set `SKILL_ROOT` to the directory containing `SKILL.md`.
Set `PLUGIN_ROOT` to the parent plugin directory (two levels up from skill).

---

## Detect Skill Type

Read `SKILL.md` and classify the skill into one of three types. This determines test generation strategy and execution behavior.

### Detection Heuristic

Read the skill's full content and apply these checks in order:

1. **Discipline** -- Skill enforces rules agents might resist:
   - Contains rationalization tables (`| Excuse | Reality |`)
   - Contains "Red Flags" or "STOP" sections
   - Uses "Iron Law", "NEVER", "No exceptions" enforcement language
   - Contains pressure scenarios or compliance checklists

2. **Orchestrator** -- Skill sequences other skills without generating content:
   - Invokes other skills via `plugin:skill` backtick syntax
   - Contains "Orchestrators never generate content" or equivalent
   - Workflow is primarily about sequencing, not producing output

3. **Task** -- Everything else (default):
   - Produces output (text, files, visuals, data)
   - Single responsibility -- does one thing well

Set `SKILL_TYPE` to `task`, `discipline`, or `orchestrator`.

Present to user: "Detected **[type]** skill. Does that look right?" Allow override.

---

## Check for Existing Tests

Look for `${SKILL_ROOT}/tests/evals.json`.

**If found:** Validate the file structure against the schema (see `references/schemas.md`). Report eval count and proceed to **Run Test Suite**.

**If not found:** Inform the user and offer options:
- **Generate tests** -- Auto-generate a draft test suite from the skill content (see `references/test-generation.md`)
- **Skip** -- Exit without testing

If `--generate` flag was passed, skip straight to generation without asking.

After generation, save to `${SKILL_ROOT}/tests/evals.json` and proceed to **Run Test Suite**.

---

## Run Test Suite

### Prepare Workspace

Create an ephemeral workspace as a sibling to the skill directory:

```bash
WORKSPACE="${SKILL_ROOT}-test-workspace"
RUN_DIR="${WORKSPACE}/run-$(date -u +%Y-%m-%dT%H-%M-%S)"
mkdir -p "${RUN_DIR}"
mkdir -p "${WORKSPACE}/history"
```

If the workspace is inside a git repo, check for a `.gitignore` entry. If missing, suggest adding `*-test-workspace/` to `.gitignore`.

### Filter Evals

If `--tag <tag>` was provided, filter evals to only those with a matching tag. Otherwise run all evals.

### Interactive Mode (Default)

For each eval in `evals.json`, create a task and dispatch subagents:

#### Step 1: Execute

Spawn an **executor subagent** per eval. Independent evals run in parallel.

Executor instructions:

```
You are a skill test executor. Your job:

1. Read the skill at: ${SKILL_ROOT}/SKILL.md
2. Read any referenced files the skill points to
3. Execute this prompt as if you were a user invoking the skill:

   "${eval.prompt}"

4. Use any provided input files from: ${SKILL_ROOT}/tests/fixtures/
5. Save your complete output to: ${RUN_DIR}/eval-${eval.id}/with_skill/outputs/
6. Write a detailed transcript to: ${RUN_DIR}/eval-${eval.id}/with_skill/transcript.md

Transcript format:
- Eval prompt (verbatim)
- Each action taken with tool used and result
- Final output
- Any issues encountered
```

**Discipline skills** with `"run_baseline": true` -- spawn a second executor WITHOUT the skill loaded:

```
You are a test executor. Execute this prompt WITHOUT any skill guidance.
Just respond naturally as you would by default.

"${eval.prompt}"

Save transcript to: ${RUN_DIR}/eval-${eval.id}/without_skill/transcript.md
Save outputs to: ${RUN_DIR}/eval-${eval.id}/without_skill/outputs/
```

#### Step 2: Grade

After each executor completes, spawn a **grader subagent**:

```
You are a skill test grader. Evaluate whether the execution met expectations.

Read the transcript at: ${RUN_DIR}/eval-${eval.id}/with_skill/transcript.md
Read outputs at: ${RUN_DIR}/eval-${eval.id}/with_skill/outputs/

Grade each expectation as PASS or FAIL with evidence.
Save results to: ${RUN_DIR}/eval-${eval.id}/with_skill/grading.json

Use the grading.json schema from references/schemas.md:
{
  "expectations": [
    {"text": "...", "passed": true/false, "evidence": "..."}
  ],
  "summary": {"passed": N, "failed": N, "total": N, "pass_rate": 0.0-1.0}
}
```

**Discipline skill grading** -- the grader also checks:
- Baseline (without_skill) transcript shows violation of expected behavior
- With-skill transcript shows compliance
- Any `anti_behaviors` that appeared in the with-skill run are flagged as FAIL

**Orchestrator skill grading** -- the grader checks the transcript for:
- Skill invocations (look for Skill tool calls in transcript)
- Invocation order matches expectations
- No direct content generation (orchestrator didn't produce output itself)

---

### Headless Mode

When `--headless` flag is passed or when invoked via `claude -p`, run the same execution logic but:

1. All execution happens sequentially in the main loop (no subagents -- headless sessions have limited subagent support)
2. Read the executor and grader instructions above and follow them inline
3. After all evals complete, output a summary to stdout
4. The summary should be parseable -- start with `PASS` or `FAIL` on the first line

```bash
# Example headless invocation:
claude -p "/test-skill creator-stack:write-note --headless" \
  --permission-mode bypassPermissions \
  --add-dir /path/to/plugin
```

Note: Headless mode is slower (sequential) but provides full isolation. Use it for final validation before shipping, not for iterative development.

---

## Results and Reporting

### Aggregate Results

After all evals are graded, compile a run summary:

1. Read all `grading.json` files from the run directory
2. Calculate overall pass rate and per-eval results
3. Save `${RUN_DIR}/summary.json` -- see `references/schemas.md` for the full summary.json schema

### Regression Detection

Check for previous snapshots at `${WORKSPACE}/history/snapshots.json`.

If previous snapshots exist:
1. Compare current pass rate against the most recent snapshot
2. Compare per-expectation results -- identify any expectations that previously passed but now fail
3. Flag regressions prominently in the report

### Update Snapshot History

Append current run to `${WORKSPACE}/history/snapshots.json` -- see `references/schemas.md` for the snapshots.json schema.

Include:
- Timestamp (ISO-8601)
- Skill version (`<plugin>@<version>` from plugin.json)
- Pass/fail/total counts and pass rate
- Notes field (ask user if they want to add a note, e.g., "Baseline before voice rewrite"; leave empty if not)

### Display Report

Present a concise report to the user:

```
## Test Results: <skill-name> (<skill-type>)

Pass rate: X% (N/M) [PASS | REGRESSION from Y% | FIRST RUN]

| Eval | Tags | Status | Details |
|------|------|--------|---------|
| #1 ... | happy-path | PASS | 4/4 expectations |
| #2 ... | edge-case | FAIL | 2/3 -- "Voice matches..." failed |

[If regression detected:]
Regressed expectations (were PASS, now FAIL):
- "expectation text" (eval #N)

Results saved to: <workspace path>
Snapshot recorded in: <snapshots.json path>
```

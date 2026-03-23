---
name: skill-retro
description: Use when reviewing how skills performed during a session, when the user wants to analyze skill invocations and identify improvements, or when the user says "skill retro", "review skills", "how did skills do", "improve this skill", or "skill retrospective".
user-invocable: true
disable-model-invocation: true
---

# Skill Retro

Analyze how skills performed in the current session and apply improvements via skill-creator.

## Process

### Step 1: Preprocess Session

Run the preprocessing script to extract a clean transcript from the current session's JSONL log:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/preprocess.mjs --cwd <current-working-directory>
```

Capture the JSON output. Key fields:
- `transcript_file` — path to the temp file containing the full transcript (at `~/.claude/tmp/skill-retro-<session-id>.json`)
- `stats.skill_invocations` — count of skills used

The script writes the full transcript to a temp file to avoid flooding the main thread's context window. Only the summary (stats + file path) appears in stdout.

**If the script fails** (e.g., no session files found), report the error and stop.

**If `skill_invocations` is 0**, tell the user: "No skills were invoked in this session — nothing to analyze." and stop.

### Step 2: Analyze (Sub-Agent)

Spawn an analysis sub-agent (using the Agent tool):
- Load the prompt from `${CLAUDE_SKILL_DIR}/references/analysis-prompt.md`
- Tell the agent to read the transcript file at the path from `transcript_file` in Step 1's output
- The agent should read the SKILL.md file for each invoked skill to compare intended vs. actual behavior. Skill paths are discoverable from the transcript's system-reminder blocks (which list installed skill base directories) or from `[SKILL INVOCATION]` markers combined with installed plugin cache paths.
- The agent returns a JSON object with `findings`, `well_executed`, and `severity_summary`

Parse the agent's response into structured findings.

**If the agent returns 0 findings**, tell the user: "All skills performed well this session. No improvements identified." Show the `well_executed` list and stop.

### Step 3: Present Findings

Display findings to the user, grouped by skill:

```
## Skill Performance Report

### superpowers:brainstorming (2 findings)

| # | Severity | Dimension         | Observation                                    |
|---|----------|-------------------|------------------------------------------------|
| 1 | medium   | gap_coverage      | No guidance for context-efficiency constraints |
| 2 | low      | execution_quality | Asked 5 clarifying questions before proposing  |

### cold-email (1 finding)

| # | Severity | Dimension         | Observation                                          |
|---|----------|-------------------|------------------------------------------------------|
| 3 | low      | trigger_accuracy  | Skill didn't trigger when user discussed subject lines |

### Well Executed
- superpowers:writing-plans — Produced clean, actionable plan with correct task ordering

---
Select findings to action (comma-separated numbers, "all", or "none"):
```

Wait for user selection. If "none", show summary and stop.

### Step 4: Resolve Source Locations

For each skill with selected findings, determine where to edit:

**Resolution order:**

1. **Project-level skill** — path contains `.claude/skills/` relative to a project
   → Candidate: edit in place (user owns it)

2. **User-level skill** — path is under `~/.claude/skills/`
   → Candidate: edit in place (user owns it)

3. **Installed plugin** — path is under `~/.claude/plugins/cache/`
   → Try to trace to source:
   a. Extract plugin name from the path
   b. Check if cwd is a marketplace project containing that plugin's source (look for `<plugin-name>/skills/<skill-name>/SKILL.md`)
   c. If not found, ask user: "Where is the source code for the `<plugin-name>` plugin? Provide a path, or type 'installed' to edit the installed copy."
   → If "installed": warn that changes will be overwritten on plugin update, proceed only if user confirms
   → If user provides a path: verify it exists and contains the skill

4. **Current project contains source** — cwd has `./<plugin-name>/skills/<skill-name>/SKILL.md`
   → Candidate: edit in place

**For each resolved path, confirm with the user before proceeding:**

```
I'll make changes to <skill-name> at:
→ /path/to/resolved/source/SKILL.md

Is this the right location? (y/n or provide correct path)
```

Do NOT proceed to implementation until every path is confirmed.

### Step 5: Implement Improvements (Parallel Sub-Agents)

For each affected skill (with confirmed source path), spawn an implementation sub-agent:

- **One agent per skill** — can run in parallel since they edit different files
- **Agent prompt:**

  "You are improving a Claude Code skill based on performance analysis findings.

  Skill: `<skill-name>`
  Source path: `<confirmed-path-to-skill-directory>`
  SKILL.md location: `<confirmed-path>/SKILL.md`

  Findings to address:
  <list all selected findings for this skill with full observation, evidence, and proposed_improvement>

  Instructions:
  1. Read the current SKILL.md at the source path
  2. Invoke the `skill-creator:skill-creator` skill
  3. When skill-creator asks what you want to do, explain you are improving an existing skill based on session analysis
  4. Provide the findings as the basis for changes
  5. Follow skill-creator's process to apply the improvements
  6. After changes are made, report what was modified"

### Step 6: Summary

After all implementation agents complete, present a summary:

```
## Skill Retro Complete

### Changes Applied
| Skill | Source Path | Changes |
|-------|------------|---------|
| superpowers:brainstorming | /path/to/SKILL.md | Added context-efficiency section |
| cold-email | /path/to/SKILL.md | Added trigger keywords: "subject line", "email subject" |

### Skipped
- copywriting: user chose not to action

### Well Executed (no changes needed)
- superpowers:writing-plans — Produced clean, actionable plan with correct task ordering
```

## Important Notes

- This skill is designed to run late in sessions when context may be full. All analysis and implementation happens in sub-agents to preserve main thread context.
- The preprocessing script writes the full transcript to `~/.claude/tmp/skill-retro-*.json` and only outputs a summary to stdout. Clean up the temp file after the analysis sub-agent has finished reading it.
- The preprocessing script has zero dependencies beyond Node.js.
- Never edit a skill without user confirmation of the source path.
- When invoking skill-creator in implementation agents, let it guide the process — don't bypass its workflow.

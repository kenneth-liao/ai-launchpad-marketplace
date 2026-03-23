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

Spawn an analysis sub-agent (using the Agent tool, model: sonnet):
- Load the prompt from `${CLAUDE_SKILL_DIR}/references/analysis-prompt.md`
- Tell the agent to read the transcript file at the path from `transcript_file` in Step 1's output
- The agent should read the SKILL.md file for each invoked skill to compare intended vs. actual behavior. Skill paths are discoverable from the transcript's system-reminder blocks (which list installed skill base directories) or from `[SKILL INVOCATION]` markers combined with installed plugin cache paths.
- The agent returns a JSON object with `findings`, `well_executed`, and `severity_summary`

Parse the agent's response into structured findings.

Once the analysis agent has finished, **delete the temp file** created in Step 1:

```bash
rm <transcript_file>
```

**If the agent returns 0 findings**, tell the user: "All skills performed well this session. No improvements identified." Show the `well_executed` list and stop.

### Step 3: Interpret and Recommend

Don't just present raw findings — interpret them. For each finding, add your own reasoning:

1. **What the fix looks like** — Is it a one-line description tweak? A new section in SKILL.md? A script rewrite? Be specific about what changes would actually be made.
2. **Effort estimate** — Quick fix (description/wording change), moderate (new section or error handling), or high-lift (architectural change, script rewrite, new scripts).
3. **Recommendation** — Whether to action it now, defer it, or skip it entirely. Explain why.

Group findings by skill and present with your interpretation:

```
## Skill Performance Report

### scheduler:manage (3 findings)

**1. [high] gap_coverage — pause command doesn't verify unload succeeded**
The `_launchctl_unload` helper silently swallows errors, so the registry can say "paused" while the job is still running.
- **Fix:** Add return-code checking to `_launchctl_unload` in the manage script, and add a post-unload verification step in SKILL.md's Pause operation.
- **Effort:** Moderate — script change + SKILL.md update
- **Recommend: Action** — This caused real user confusion in this session.

**2. [medium] gap_coverage — No error recovery entry for "task still runs after pausing"**
The assistant had to improvise the entire investigation.
- **Fix:** Add a new row to the Error Recovery table in SKILL.md.
- **Effort:** Quick — one table row addition
- **Recommend: Action** — Low effort, high value.

**3. [low] execution_quality — list command shows registry status without cross-checking launchd**
Would require the list command to shell out to `launchctl list` and reconcile.
- **Fix:** Add launchd state reconciliation to the list operation in the manage script.
- **Effort:** High-lift — requires new script logic and testing across platforms.
- **Recommend: Defer** — Nice-to-have but significant work. Not worth addressing now.

### Well Executed
- list presented clean, accurate registry data
- Assistant correctly went outside the skill to diagnose the real issue

---
I recommend actioning findings 1 and 2. Finding 3 is high-lift and better deferred.

Proceed with these? (y/adjust/none)
```

**Key principles:**
- Lead with your recommendation — don't make the user figure out what's worth doing
- Be honest about high-lift items — don't propose changes that would require major rewrites unless they're clearly worth it
- Group related findings that would be addressed together
- The user can adjust your recommendation (add/remove items) or accept it

Wait for user confirmation. If "none", show summary and stop.

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
| scheduler:manage | /path/to/SKILL.md | Added return-code checking to _launchctl_unload, post-unload verification step |
| scheduler:manage | /path/to/SKILL.md | Added "task still runs after pausing" to Error Recovery table |

### Deferred
- scheduler:manage #3 (launchd state reconciliation) — high-lift, deferred

### Well Executed
- list operation presented clean, accurate registry data
```

## Important Notes

- This skill is designed to run late in sessions when context may be full. All analysis and implementation happens in sub-agents to preserve main thread context.
- The preprocessing script writes the full transcript to `~/.claude/tmp/skill-retro-*.json` and only outputs a summary to stdout. Clean up the temp file after the analysis sub-agent has finished reading it.
- The preprocessing script has zero dependencies beyond Node.js.
- Never edit a skill without user confirmation of the source path.
- When invoking skill-creator in implementation agents, let it guide the process — don't bypass its workflow.

---
name: analyze-team-session
description: Use when reviewing an agent team session export for quality, when asked to "analyze this team session", "review my agent team run", "what went wrong with this session", "how can I improve my agent team usage", or when provided a markdown team session transcript and asked for feedback on agent teams effectiveness.
user-invocable: true
argument-hint: "<path-to-export.md>"
---

# Analyze Team Session

Analyze an agent team session export against the official Claude Code agent teams best practices. Produce a structured report with a suitability verdict, scorecard, actionable recommendations, and an improved prompt rewrite.

**Core Principle**: Every recommendation must cite a specific best practice from the official docs and quote specific evidence from the session. No vague assessments.

## When to Use

- User provides a team session export and wants feedback
- User asks how to improve their agent team usage
- User wants to know if a task was a good fit for agent teams
- After running an agent team, to identify what to do differently next time

**Prerequisite**: This skill requires a markdown session export. Use the `agent-teams:view-team-session` skill to generate one from a session ID.

Do NOT use for:
- Analyzing solo (non-team) Claude Code sessions
- General Claude Code usage advice unrelated to agent teams

## Workflow

### Step 1: Read the session export

Read the full markdown session export file. If too large, read in chunks.

Extract these elements:

- **Team name** and session ID
- **Duration** and agent list
- **Original user prompt** — the first user message that kicked off the team
- **Team structure** — lead + teammates, their roles, models used
- **Task list** — tasks created, assigned, completed, dependencies between tasks (look for TaskCreate/TaskUpdate calls)
- **Communication flow** — DMs between teammates (SendMessage calls), broadcasts
- **Tool calls** — what each agent did (reads, edits, web fetches, etc.)
- **Quality gates** — any plan approval workflows, TaskCompleted hooks, TeammateIdle hooks
- **Final output** — what the lead produced as the end result

### Step 2: Fetch the official documentation

Search for the latest agent teams best practices. Try these approaches in order:

1. **WebSearch**: Search for "Claude Code agent teams best practices site:code.claude.com" to discover the current URL
2. **WebFetch**: Fetch the discovered URL, or fall back to `https://code.claude.com/docs/en/agent-teams`
3. **Costs section**: Also fetch `https://code.claude.com/docs/en/costs` for the "Agent team token costs" and "Manage agent team costs" sections

These are the authoritative source for all rubric evaluations. If both WebSearch and WebFetch fail, inform the user that analysis cannot proceed without the official docs.

### Step 3: Evaluate against the rubric

Read the evaluation rubric from `references/rubric.md` (10 categories). For each category:

- **Rate it**: Gap, Partial, or Strong
- **Quote evidence**: Cite specific passages from the session export
- **Explain**: Reference the specific best practice from the official docs

### Step 4: Write the analysis report

Save the report to `.claude/output/<team-name>-analysis.md`. Actionable content comes first, detailed evidence last.

Use this structure:

```
# Agent Team Session Analysis: <team-name>

**Session:** <session-id> | **Team:** <team-name>
**Duration:** <duration> | **Agents:** <comma-separated list>
**Analysis date:** <today's date>

---

## Suitability Verdict

[1-2 paragraphs assessing whether this task was a good fit for agent teams.
If not, explain what approach would have been better and why. Be direct.]

**Verdict:** Good fit / Marginal fit / Poor fit

---

## Summary

| Category | Rating |
|----------|--------|
| Suitability | [Strong/Partial/Gap] |
| Context Sharing | [Strong/Partial/Gap] |
| Task Sizing | [Strong/Partial/Gap] |
| Task Dependencies | [Strong/Partial/Gap/N/A] |
| Communication Quality | [Strong/Partial/Gap] |
| File Conflict Avoidance | [Strong/Partial/Gap/N/A] |
| Lead Orchestration | [Strong/Partial/Gap] |
| Model Selection & Cost Efficiency | [Strong/Partial/Gap] |
| Quality Gates | [Strong/Partial/Gap/N/A] |
| Cleanup | [Strong/Partial/Gap] |

---

## Top Recommendations

[3-5 recommendations ranked by impact. Each must be specific, actionable,
and reference what happened in the session.]

1. **[Category]** — [Recommendation with concrete example of what to change]
2. ...

---

## Improved Prompt

If the original prompt could be rewritten following all best practices,
here's what it would look like:

[Rewrite the user's original prompt incorporating all recommendations.
This should be ready to copy-paste for their next run.]

---

## Detailed Rubric Scorecard

### 1. Suitability — [Rating]

**Evidence:**
> [Quoted passages from the session export]

**Assessment:** [Explanation referencing specific best practice from the docs]

[...continue for all 10 categories...]
```

After writing the report, tell the user where it was saved and give a 2-3 sentence summary of the key findings.

## Quality Checklist

- [ ] All 10 rubric categories evaluated with evidence and doc references
- [ ] Suitability verdict is direct and honest (not hedging)
- [ ] Recommendations are specific and actionable (not "improve communication")
- [ ] Improved prompt is a complete, ready-to-use rewrite
- [ ] Every rating cites a specific passage from the session export
- [ ] Every assessment references a specific best practice from the official docs
- [ ] Report saved to `.claude/output/<team-name>-analysis.md`

## Common Pitfalls

1. **Vague ratings**: Saying "Communication was Partial" without quoting the actual messages (or lack thereof). Always cite evidence.
2. **Hedging the verdict**: If it was a poor fit for agent teams, say so. The point of the analysis is honest feedback, not diplomacy.
3. **Generic recommendations**: "Improve task sizing" is useless. "Split the single review task into 3 focused sub-tasks (voice, engagement, accuracy) with 2-3 checkpoints each" is actionable.
4. **Ignoring newer features**: If the session didn't use task dependencies, quality gates, or plan approval, note whether these would have helped — they may not have been available when the session ran, but they're available now.

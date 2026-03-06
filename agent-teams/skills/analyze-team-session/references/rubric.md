# Agent Teams Evaluation Rubric

Rate each category: **Gap** (not followed), **Partial** (attempted but incomplete), or **Strong** (well-executed). For each one, quote specific evidence from the session export and reference the corresponding best practice from the official docs.

---

## 1. Suitability

Was this task a good fit for agent teams? Compare against the official "When to use agent teams" criteria:

- Does it involve parallel exploration that adds real value?
- Do agents need to communicate with each other, not just report back?
- Does it match strong use cases (research/review, new modules, competing hypotheses, cross-layer coordination)?
- Or does it match anti-patterns (sequential tasks, same-file edits, heavy dependencies)?

If the task would have been better served by subagents or a single session, say so directly and explain why.

## 2. Context Sharing

Did teammates get enough context in their spawn prompts? Teammates don't inherit the lead's conversation history — they only get what's in their spawn prompt plus project-level context (CLAUDE.md, skills).

- Were spawn prompts specific about what to do, where to look, and what format to report in?
- Or were they vague, forcing teammates to spend turns figuring things out?

## 3. Task Sizing

Were tasks appropriately scoped? Three buckets:

- **Too small**: coordination overhead exceeds the benefit
- **Too large**: teammates work too long without check-ins, increasing risk of wasted effort
- **Just right**: self-contained units that produce a clear deliverable

The docs suggest 5-6 tasks per teammate keeps everyone productive and lets the lead reassign work if someone gets stuck.

## 4. Task Dependencies

Were task dependencies used effectively? Agent teams support dependency tracking where blocked tasks auto-unblock when dependencies complete.

- Were naturally sequential steps modeled as dependencies?
- Or did teammates pick up tasks that required outputs from incomplete tasks?
- Were dependency chains too long (reducing parallelism) or too flat (causing conflicts)?

If no dependencies were used and the tasks were purely parallel, note whether dependencies would have helped.

## 5. Communication Quality

Did teammates communicate in ways that added value? This is the core differentiator from subagents.

- Did teammates share findings with each other?
- Did any teammate challenge or build on another's findings?
- Was there genuine cross-pollination, or did they work in isolation?

If teammates never messaged each other, the task could have used subagents instead — flag this.

## 6. File Conflict Avoidance

Did the task structure avoid multiple teammates editing the same files? The docs warn that two teammates editing the same file leads to overwrites.

If this was a review/research task with no file edits, mark as N/A and note why.

## 7. Lead Orchestration

Did the lead delegate effectively?

- Did the lead create tasks, assign them, and wait for results?
- Or did it start doing work itself instead of coordinating?
- Did it synthesize findings from all teammates into a coherent output?
- Did it use plan approval workflows where appropriate (having teammates plan in read-only mode before implementing)?

## 8. Model Selection & Cost Efficiency

Were costs managed appropriately?

- **Model selection**: Sonnet is recommended for teammates (balances capability and cost). Was each teammate's model chosen appropriately for their task complexity?
- **Team size**: Token usage scales linearly with team size. Was the team appropriately sized, or were there idle teammates?
- **Spawn prompts**: Everything in the spawn prompt adds to context from the start. Were prompts focused?
- **Cleanup**: Were teammates shut down when their work was done, or did idle teammates continue consuming tokens?

## 9. Quality Gates

Were quality controls in place? Agent teams support two quality gate hooks:

- **`TaskCompleted` hook**: Exit code 2 prevents task completion and sends feedback, forcing rework before marking done
- **`TeammateIdle` hook**: Exit code 2 sends feedback and keeps the teammate working instead of going idle
- **Plan approval**: Teammates can plan in read-only mode before implementing, with lead review/approval

Evaluate whether the session used any of these, and whether it would have benefited from them. If the session predates these features, note that.

## 10. Cleanup

Was the team properly shut down?

- Were teammates gracefully shut down via shutdown requests?
- Did the lead run team cleanup?
- Or did the session end with teammates still running?

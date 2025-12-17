# Context Update Instructions

This file describes how to maintain Elle's memory. Update context **continuously** as you learn new things about the user.

Context updates are **autonomous** — just do them without asking permission.

## Core Principle

> **Only store information that would change how you respond in a future session.**

Context updates are silent housekeeping. Never ask "may I write this down?" Just do it.

---

## The "Future Self" Test

Before adding ANY context, ask:
> "If I started a new conversation tomorrow, would this change how I respond?"

| ✅ Pass - Add It | ❌ Fail - Skip It |
|------------------|-------------------|
| "User prefers uv over pip" | "Installed dependencies with uv" |
| "User's wife is doing IVF" | "Researched IVF clinics" |
| "EQL Ivy uses Supabase" | "Deployed v2.3.1 to Render" |

## What NEVER Goes in Context

1. **Task completion logs** - "✅ Completed X, ✅ Completed Y"
2. **Research summaries** - Store in project docs, reference the path only
3. **Session-specific details** - Goes in `~/.claude/.context/core/session.md`
4. **Duplicated info** - If it's in project README, don't repeat it
5. **Git history** - If it can be found from `git log`, don't add it

---

## Update Steps

### 1. Session Context
Update `~/.claude/.context/core/session.md` with:
- Current focus (what we're working on)
- Active tasks in progress
- Any blockers
- Notes for next session

### 2. Correction Detection (Self-Improvement)
If user corrected any behavior this session, **IMMEDIATELY** add a rule to `~/.claude/.context/core/rules.md`:

| User Says | Interpretation | Add to rules.md |
|-----------|----------------|-----------------|
| "Don't commit without asking" | Explicit instruction | ❌ NEVER commit without explicit approval |
| "Why did you push to main?" | Frustration at action | ❌ NEVER push without asking first |
| "I didn't ask you to create that file" | Unwanted action | ❌ NEVER create files unless necessary |
| "Always run tests first" | Process instruction | ✅ ALWAYS run tests before committing |

→ Brief notification: "Added rule: never X without asking"

### 3. Preference/Workflow Learning
If new preference or workflow learned:
→ Update `~/.claude/.context/core/preferences.md` or `~/.claude/.context/core/workflows.md`
→ **REPLACE** old preference if it contradicts (don't accumulate)
→ Brief notification: "Noted preference for X"

### 4. Identity Updates
If new personal/professional info learned:
→ Update `~/.claude/.context/core/identity.md`

### 5. Project Status
If project status changed:
→ Update `~/.claude/.context/core/projects.md`

### 6. Relationships
If new person mentioned or relationship context learned:
→ Update `~/.claude/.context/core/relationships.md`
→ Include: name, relationship, relevant context, important dates

### 7. Triggers & Important Dates
If important date, deadline, or recurring check-in learned:
→ Update `~/.claude/.context/core/triggers.md`
→ Include: date, event/deadline, action needed

### 8. Journal (Session Log)
At the end of notable sessions, append to `~/.claude/.context/core/journal.md`:
→ Date, what was accomplished, notable decisions or context
→ Keep entries brief — anything important should be promoted to relevant core file
→ Add entries at the TOP (newest first)

---

## File Update Policies

| File | Update Policy |
|------|---------------|
| `core/identity.md` | Update when new identity info shared |
| `core/preferences.md` | **REPLACE** when new preference stated |
| `core/workflows.md` | Update when workflow learned/changed |
| `core/relationships.md` | **ADD** people as mentioned; update context as learned |
| `core/triggers.md` | **ADD** dates/deadlines; remove when passed or irrelevant |
| `core/projects.md` | Update when project status changes; archive completed |
| `core/rules.md` | **ADD** when correction detected; only remove if explicitly rescinded |
| `core/session.md` | Update every session; clear on major context switch |
| `core/journal.md` | **APPEND** notable sessions at TOP; periodically prune old entries |

All files are in `~/.claude/.context/`. Add new sections as needed.

---

## Notification Style

Brief notifications, not permission-seeking:
- ✅ "Done. I've noted your preference for uv over pip."
- ✅ "Updated session context with current focus."
- ❌ "Would you like me to add this to context?"
- ❌ "Should I update my records?"

---

## Lifecycle Management

| Type | Action | Trigger |
|------|--------|---------|
| Preferences | **Replace** in place | New preference contradicts old |
| Relationships | **Add** new people; update context | Person mentioned or context learned |
| Triggers | **Add** then **remove** when passed | Date/deadline learned; date passes |
| Projects | **Archive** to bottom section | Project completes |
| Session | **Clear** | Major context switch |
| Journal | **Append** at top; **prune** periodically | Notable session ends; file gets long |
| Rules | **Keep forever** | Only remove on explicit user request |

---

## Escalation (Rare)

Only ask the user when there's genuine ambiguity:
1. Contradictory info: "You mentioned preferring X, but I have Y. Which is current?"
2. Rule conflict: "You said never auto-commit, but now asking me to. Update my rules?"
3. Unclear correction: "Was that a correction or situational?"


# Memory System Analysis & Improvement Recommendations

**Date**: December 7, 2025  
**Purpose**: Comprehensive analysis of the current memory system with recommendations for improvement

---

## Executive Summary

The current memory system conflates three fundamentally different types of information: **session work logs**, **enduring personal context**, and **project documentation**. This leads to bloated, unfocused memories that don't serve the core goal: enabling Claude Code to be an effective personal assistant across sessions.

---

## Part 1: The Goal of a Personal Assistant Memory System

### What Makes a Great Personal Assistant?

A truly effective personal assistant understands:

1. **Who you are** - Your identity, roles, relationships, life circumstances
2. **How you work** - Your preferences, workflows, tools, communication style
3. **What matters to you** - Goals, priorities, constraints, values
4. **Your world** - People you work with, projects you're involved in, recurring contexts
5. **How to serve you better** - Learned patterns from past interactions

### The Core Insight

> **A memory system should store information that changes how the assistant behaves, not what the assistant produced.**

Your examples illustrate this perfectly:

| ✅ **Should Remember** | ❌ **Should NOT Remember** |
|------------------------|---------------------------|
| "Kenny prefers uv and bun over pip and npm" | "Ran `npm install` successfully" |
| "When debugging backend errors, check Sentry and Render logs" | "Found error in Sentry on Dec 5" |
| "Kenny and his wife are doing fertility treatments" | "Researched IVF success rates" |
| "Kenny has a YouTube channel about AI/Claude Code" | "Episode 20 uses Fireship-style thumbnails" |
| "For research, Kenny prefers X, Y, Z sources" | "Research report saved to /path/to/file.md" |

---

## Part 2: Analysis of Current System

### Current Structure

```
context/
├── memory/
│   ├── CLAUDE.md (instructions)
│   └── memories.md (actual memories)
└── projects/
    ├── CLAUDE.md (instructions)
    └── project_index.md (project list)
```

### Critical Issues Identified

#### Issue 1: Session Work Logs Masquerading as Memories

**Current `memories.md` content breakdown:**
- ~70% is session work logs (Archive section: detailed step-by-step task completions)
- ~15% is project-specific details (Episode 20 thumbnails, file paths)
- ~10% is workflow documentation (thumbkit commands, directory structures)
- ~5% is actual enduring preferences/context

**Example of problematic content:**
```markdown
**December 7, 2025 - BaaS Platform Research (COMPLETED ✅)**
- ✅ Analyzed current Supabase usage and requirements
- ✅ Researched 6 major BaaS platforms
- ✅ Compared pricing at different scales
[...50+ more lines of session details...]
```

**Why this is wrong:** This is a work log, not a memory. The *memory* should be:
> "EQL Ivy uses Supabase. We evaluated switching but decided to stay with Supabase for the 6-18 month horizon (see docs/BAAS_PLATFORM_COMPARISON_2024.md for details)."

#### Issue 2: No Distinction Between Memory Types

The system treats all memories equally, but there are fundamentally different categories:

| Category | Examples | Persistence | Update Frequency |
|----------|----------|-------------|------------------|
| **Identity & Life** | Wife doing fertility treatments, lives in X city | Years | Rarely |
| **Preferences** | Uses uv/bun, prefers certain research sources | Months | Occasionally |
| **Workflows** | Check Sentry for backend errors, use thumbkit for thumbnails | Months | When tools change |
| **Active Projects** | YouTube channel, EQL Ivy | Weeks-Months | As status changes |
| **Session Context** | Currently working on Episode 20 | Hours-Days | Every session |

#### Issue 3: "When in Doubt, Add It" Philosophy

The CLAUDE.md instruction:
> "As a general rule of thumb, if you are unsure whether or not something should be added to memory, it is better to add it than to not add it."

This creates memory bloat. A better principle:
> "Only add information that would change how you respond in a future session."

#### Issue 4: No Memory Lifecycle Management

Memories accumulate forever. There's no:
- Consolidation (merging related memories)
- Archival (moving stale memories to cold storage)
- Pruning (removing obsolete information)
- Prioritization (what to read first when context is limited)

#### Issue 5: Redundancy Between memories.md and project_index.md

Both files contain project information:
- `memories.md` has a "Projects" section with YouTube and EQL Ivy details
- `project_index.md` has the same projects with overlapping details

This violates DRY (Don't Repeat Yourself) and creates sync issues.

---

## Part 3: Recommended New Architecture

### Proposed Structure

```
context/
├── CLAUDE.md                # Main entry point (loaded by UserPromptSubmit hook)
├── core/
│   ├── CLAUDE.md            # Instructions for reading AND updating core files (Stop hook points here)
│   ├── identity.md          # Who Kenny is (stable facts)
│   ├── preferences.md       # How Kenny likes to work
│   ├── workflows.md         # Standard operating procedures
│   └── rules.md             # ⭐ Learned rules from corrections (self-improvement)
├── projects/
│   ├── CLAUDE.md            # Instructions for projects
│   └── project_index.md     # Quick reference (name, path, status only)
└── session/
    └── current.md           # Current session context only
```

**Removed:** The `memory/` directory is eliminated entirely. Its useful content migrates to `core/` files.

**Note:** No per-project detail files in context/. Project documentation lives in the projects themselves (README.md, docs/, etc.). The index just points to them - no duplication.

### New Memory Categories

#### 1. Identity (`core/identity.md`)
Stable facts about Kenny that rarely change.

**Example content:**
```markdown
## Personal
- Kenny and his wife are trying to have a baby via fertility treatments (started ~2024)
- Based in [City, if relevant]

## Professional
- Software engineer/entrepreneur
- YouTube creator (@KennethLiao) - AI/Claude Code tutorials for working professionals
- Building EQL Ivy - AI sales assistant for Vietnamese e-commerce

## Communication Style
- Prefers direct, actionable responses
- Values data-backed recommendations
```

#### 2. Preferences (`core/preferences.md`)
How Kenny likes to work - things that should influence every interaction.

**Example content:**
```markdown
## Development Tools
- **Package managers**: uv (Python) and bun (Node.js) over pip and npm
- **AI coding**: Claude Code with personal-assistant plugin

## Research Preferences
- Preferred sources: [list specific sites/sources Kenny trusts]
- Always cite sources with dates for freshness

## Decision-Making
- Prefers data-backed recommendations
- Likes to see 2-3 options with tradeoffs, not just one recommendation

## Debugging Workflows
- For backend errors: Always check Sentry and Render logs in addition to code
- For frontend issues: Check Vercel deployment logs
```

#### 3. Workflows (`core/workflows.md`)
Standard operating procedures learned from past sessions.

**Example content:**
```markdown
## YouTube Video Creation
1. Research with youtube-research-video-topic skill
2. Plan with youtube-plan-new-video skill
3. Generate thumbnails with thumbkit CLI
   - Headshots: `/Users/kennethliao/projects/youtube/assets/kenny_headshots/`
   - Command: `thumbkit generate --prompt "..." --ref <headshot> --out-dir <dir> --model pro`
4. Episode files: `/Users/kennethliao/projects/youtube/episode_files/[N]_[topic]/`

## Code Research
- Use codebase-retrieval for finding code patterns
- Use git-commit-retrieval for understanding why changes were made
```

#### 4. Projects (`projects/project_index.md`)
Minimal quick-reference only. **Details live in project repos** (README.md, docs/), not here.

**Example content:**
```markdown
| Project | Path | Status | Key Notes |
|---------|------|--------|-----------|
| EQL Ivy | `/Users/kennethliao/projects/eql-ivy` | Production | Vietnamese AI sales assistant |
| YouTube | `/Users/kennethliao/projects/youtube` | Active | See episode_files/ for current work |
| AI Launchpad | `/Users/kennethliao/projects/ai-launchpad-marketplace` | Active | Plugin/skill marketplace |
```

**What NOT to put here:**
- Detailed architecture (that's in the project's README)
- Tech stack details (read from project)
- Competitive analysis (that's in project's docs/)
- Anything that duplicates project documentation

#### 5. Session Context (`session/current.md`)
What we're working on RIGHT NOW. Cleared/archived between major context switches.

**Example content:**
```markdown
## Current Focus
Working on Episode 20: Claude Code Context Engineering

## Active Tasks
- [ ] Record screen demos for 5 techniques
- [ ] Finalize script

## Blockers
None

## Notes for Next Session
- Left off at section 3 of script
- User mentioned wanting to add claude-trace demo
```

#### 6. Rules & Corrections (`core/rules.md`) ⭐ NEW
**This is the self-improvement mechanism.** When Kenny corrects a mistake or gives negative feedback, it becomes a rule that prevents future mistakes.

**Why this is critical:**
- Mistakes are the highest-signal learning opportunities
- A correction represents a strong preference that was violated
- Rules are more actionable than preferences ("always X" vs "prefers X")

**Example content:**
```markdown
# Rules (Learned from Corrections)

These are explicit rules learned from past mistakes. ALWAYS check these before taking action.

## Git & Version Control
- ❌ NEVER commit without explicit user approval or request
- ❌ NEVER push to remote without asking first
- ❌ NEVER rebase without permission
- ✅ ALWAYS ask before any destructive git operation

## Code Changes
- ❌ NEVER delete files without confirmation
- ❌ NEVER install dependencies without asking (can break environments)
- ✅ ALWAYS run existing tests after making changes
- ✅ ALWAYS check for downstream impacts before editing shared code

## Communication
- ❌ DON'T assume what Kenny wants - ask if unclear
- ❌ DON'T create documentation files unless explicitly requested
- ✅ DO ask clarifying questions for ambiguous requests

## Project-Specific Rules
- EQL Ivy: Never use Firebase (we evaluated and rejected it)
- YouTube: Always use thumbkit CLI, not manual image generation
```

**Rule Format:**
```
❌ NEVER [action] [context if needed] - [reason/origin if helpful]
✅ ALWAYS [action] [context if needed]
```

**When to add rules:**
1. Kenny explicitly corrects a behavior ("Don't do X", "Always ask before Y")
2. Kenny expresses frustration about an action ("Why did you commit without asking?")
3. A mistake caused significant rework or problems
4. Kenny clarifies a boundary ("I know I said X, but I meant only in context Y")

---

## Part 3.5: The Self-Improvement Loop

### How Corrections Become Rules (Autonomous)

```
┌─────────────────────────────────────────────────────────────┐
│              AUTONOMOUS SELF-IMPROVEMENT LOOP                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Claude takes action                                     │
│           ↓                                                 │
│  2. User corrects/complains                                 │
│           ↓                                                 │
│  3. Claude recognizes correction pattern:                   │
│      - "Don't do X"                                         │
│      - "Why did you X?"                                     │
│      - "Always ask before X"                                │
│      - "I told you not to X"                                │
│           ↓                                                 │
│  4. Claude IMMEDIATELY adds rule (no confirmation needed):  │
│      → Adds to core/rules.md                                │
│      → Brief notification: "Got it. I've added a rule to    │
│        always ask before committing."                       │
│           ↓                                                 │
│  5. Future sessions: Check rules BEFORE acting              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key change:** Steps 4-6 collapsed into immediate autonomous action with brief notification.

### Correction Detection Patterns

Claude should recognize these as correction signals:

| User Says | Interpretation | Resulting Rule |
|-----------|----------------|----------------|
| "Don't commit without asking" | Explicit instruction | ❌ NEVER commit without explicit approval |
| "Why did you push to main?" | Frustration at action | ❌ NEVER push without asking first |
| "I didn't ask you to create that file" | Unwanted action | ❌ NEVER create files unless necessary |
| "That's too verbose" | Quality feedback | Add to preferences: "Keep responses concise" |
| "Always run tests first" | Process instruction | ✅ ALWAYS run tests before committing |

### Pre-Action Checklist

Before taking potentially destructive or irreversible actions, Claude should:

1. **Check `core/rules.md`** for relevant "NEVER" rules
2. **Ask if uncertain** - better to ask than violate a rule
3. **Confirm before destructive actions** (delete, push, deploy, install)

---

## Part 4: Memory Quality Guidelines

### The "Future Self" Test

Before adding a memory, ask:
> "If I started a completely new conversation tomorrow, would this information change how I respond?"

| ✅ Pass | ❌ Fail |
|---------|---------|
| "Kenny prefers uv over pip" | "Installed dependencies with uv" |
| "Kenny's wife is doing IVF" | "Researched IVF clinics in Bay Area" |
| "EQL Ivy uses Supabase + Render" | "Deployed v2.3.1 to Render on Dec 5" |
| "Check Sentry for backend errors" | "Found NullPointerException in Sentry" |

### Memory Format Standards

**Good memory format:**
```
[CONTEXT]: [ACTIONABLE INSIGHT]
```

**Examples:**
- "YouTube: Kenny's audience is working professionals (non-technical to intermediate) interested in practical AI tutorials"
- "Debugging: Always check Sentry and Render logs for backend errors before code review"
- "Preferences: Use uv for Python, bun for Node.js - Kenny explicitly prefers these over pip/npm"

### What Should NEVER Be Memories

1. **Task completion logs** - "✅ Completed X, ✅ Completed Y"
2. **Research outputs** - Summaries of research (that's what reports are for)
3. **Temporary file paths** - Unless they're permanent reference locations
4. **Session-specific context** - Goes in session/current.md, not permanent memory
5. **Duplicated information** - If it's in a project's README, don't repeat it

### Reference Pattern for Deliverables

Instead of storing research summaries in memory:

**❌ Bad:**
```markdown
**BaaS Research Findings:**
- Supabase: $25/org, best for multi-tenant
- Firebase: $30+/org, NoSQL
- [50 more lines of findings...]
```

**✅ Good:**
```markdown
**BaaS Decision (Dec 2025):** Stay with Supabase for 6-18 month horizon.
- Full analysis: `/Users/kennethliao/projects/eql-ivy/docs/BAAS_PLATFORM_COMPARISON_2024.md`
```

---

## Part 5: Implementation Recommendations

### Immediate Actions

1. **Restructure directories** per the new architecture
2. **Migrate current memories** through the "Future Self" test filter
3. **Update CLAUDE.md instructions** with new guidelines
4. **Create templates** for each memory category

### Update Memory Instructions

Replace the "when in doubt, add it" guidance with:

```markdown
## Memory Quality Checklist

Before adding a memory, verify:
1. [ ] Would this change how I respond in a future session?
2. [ ] Is this enduring (not session-specific)?
3. [ ] Is this actionable (not just informational)?
4. [ ] Is this not duplicated elsewhere (project docs, reports)?
5. [ ] Have I stated it concisely (1-2 sentences max)?

If you can't check all boxes, don't add it to permanent memory.
```

### Session Handoff Protocol

At end of significant work sessions:

1. **Update session/current.md** with immediate context
2. **Extract enduring learnings** to core/ files (preferences, workflows learned)
3. **Update project status** if project state changed
4. **DON'T** write detailed work logs - the git history and deliverables serve that purpose

---

## Part 5.5: Memory Lifecycle Management

### The Problem with "Append-Only" Memory

Without lifecycle management:
- Contradictory preferences accumulate ("prefers pip" + "prefers uv over pip")
- Completed projects clutter the active list
- Stale session context causes confusion
- Memory files grow unbounded

### Autonomous Memory Management

**Core Principle:** Memory updates are silent, routine housekeeping - like a good assistant taking notes. Never ask "may I write this down?" Just do it.

| Memory Type | Pattern | Autonomous Behavior |
|-------------|---------|---------------------|
| `identity.md` | Update | Just update when new life/identity info shared |
| `preferences.md` | **Replace** | Just update when new preference stated (overwrites old) |
| `workflows.md` | **Update** | Just update when workflow learned or changed |
| `rules.md` | **Add** | Just add when correction detected |
| `rules.md` | Remove | Only when user explicitly rescinds (user-initiated) |
| `project_index.md` | **Archive** | Just move to archive when project completes |
| `session/current.md` | **Clear** | Just clear when switching major contexts |

**All memory updates happen automatically without asking permission.**

### Replace, Don't Accumulate (Preferences)

```markdown
# ❌ Bad - contradictory preferences
- Kenny prefers pip for Python packages (Dec 1)
- Kenny prefers uv over pip (Dec 5)

# ✅ Good - replace in place
- Package managers: uv (Python), bun (Node.js)
```

### Archive, Don't Delete (Projects)

```markdown
# Active Projects
| Project | Path | Status |
|---------|------|--------|
| EQL Ivy | /path/to/eql-ivy | Production |

# Completed/Archived Projects
| Project | Completed | Notes |
|---------|-----------|-------|
| Old Client Project | Dec 2024 | See /docs/project-postmortem.md |
```

### Rules Require Explicit Revocation

Rules learned from corrections should **only** be removed when the user explicitly says:
- "You can commit without asking now"
- "That rule no longer applies"
- "Forget that restriction about X"

**Never** remove a rule just because time has passed or it hasn't been triggered recently.

### Notification Style (Not Permission-Seeking)

When memory is updated, brief notification at end of response - not asking permission:

```markdown
# ✅ Good - brief notification
"Done. I've noted your preference for uv over pip."
"Updated: EQL Ivy moved to 'Completed Projects'."

# ❌ Bad - permission-seeking
"Would you like me to add this preference to my memory?"
"Should I update my records to reflect this?"
```

### The Only Escalations (Rare)

Only ask the user when there's genuine ambiguity:

1. **Contradictory information**: "You mentioned preferring X, but I have Y recorded. Which is current?"
2. **Rule conflict**: "You said never auto-commit, but now you're asking me to. Should I update my rules?"
3. **Unclear correction**: "I'm not sure if that was a correction or situational. Should I add a rule?"

### Session Context is Fully Autonomous

The agent silently manages session context:
- Clears when switching major contexts (no need to ask)
- Updates during work sessions
- Carries forward relevant notes to next session

### Background Maintenance

The agent should periodically (every ~10 sessions) perform silent maintenance:
- Consolidate duplicate preferences
- Archive completed projects
- Remove obviously stale session notes

**No need to announce this** - just keep memory clean as part of normal operation.

---

## Part 6: Summary of Key Changes

| Current State | Recommended State |
|---------------|-------------------|
| `memory/` directory with `memories.md` | `core/` directory with categorized files |
| One monolithic memories.md (325 lines) | Split files: identity, preferences, workflows, rules (~65 lines total) |
| Session work logs in memory | `session/current.md` - ephemeral, auto-cleared |
| "When in doubt, add it" | "Future Self" test - only actionable, enduring insights |
| Research summaries in memory | Reference paths to reports only |
| Detailed project info in memory | Minimal index + reference to project docs |
| No memory lifecycle | **Structured lifecycle: replace/archive/clear patterns** |
| No learning from mistakes | **rules.md captures corrections for self-improvement** |
| Append-only, no pruning | **Type-specific autonomous pruning** |
| Ask permission to update | **Silent autonomous updates with brief notifications** |

### The Ultimate Test

After implementing these changes, `memories.md` (or its successors) should be readable in under 2 minutes and give Claude Code everything needed to:

1. Know who Kenny is and what matters to him
2. Understand how Kenny prefers to work
3. Know what projects exist and their current status
4. Pick up exactly where the last session left off

**If it takes longer than 2 minutes to read, the memories are too verbose.**

---

## Appendix: Example Migrated Memories

### From Current memories.md (325 lines) → Proposed core/preferences.md (~30 lines)

```markdown
# Kenny's Preferences

## Development
- Package managers: uv (Python), bun (Node.js) - never pip or npm
- AI assistant: Claude Code with personal-assistant plugin

## YouTube Content
- Channel: @KennethLiao (ID: UCOEqiv0-yg_hx0nJiaWJK4Q)
- Audience: Working professionals, non-technical to intermediate, interested in practical AI
- Style: Result-oriented tutorials with real-world applications
- Benchmarks: ~14.5K avg views, ~3% engagement for Claude Code content

## Decision-Making
- Prefers data-backed recommendations with cited sources
- Likes multiple options with tradeoffs
- Values efficiency and parallel task delegation

## Thumbnail Preferences
- Satisfied grin expression over shocked/surprised
- Prefers proven patterns (Fireship, NetworkChuck styles)
- A/B testing with CTR-based switching

## Debugging
- Backend errors: Check Sentry + Render logs before code
- MCP issues: Check if server needs restart after code changes
```

This is **actionable**, **concise**, and **changes behavior** in future sessions.

---

## Part 7: Hook Integration

### Current Hook Architecture

The plugin uses two hooks with progressive disclosure:

1. **UserPromptSubmit** (`load_context_system.py`): Loads `context/CLAUDE.md` on every prompt
2. **Stop** (`update-memories-on-stop.py`): Blocks completion until memories updated

### Required Hook Change

**One line change in `update-memories-on-stop.py`:**

```python
# BEFORE (line ~28):
return f"""...read `{context_dir}/memory/CLAUDE.md`...

# AFTER:
return f"""...read `{context_dir}/core/CLAUDE.md`...
```

### Files to Create/Update/Delete

| Action | File | Notes |
|--------|------|-------|
| **Update** | `hooks/update-memories-on-stop.py` | Change path from `memory/` to `core/` |
| **Update** | `context/CLAUDE.md` | Reference new `core/` structure |
| **Create** | `context/core/CLAUDE.md` | Instructions for reading AND updating core files |
| **Create** | `context/core/identity.md` | Who Kenny is |
| **Create** | `context/core/preferences.md` | How Kenny likes to work |
| **Create** | `context/core/workflows.md` | Standard operating procedures |
| **Create** | `context/core/rules.md` | Learned rules from corrections |
| **Create** | `context/session/current.md` | Ephemeral session context |
| **Delete** | `context/memory/` | Entire directory (after migrating useful content) |

### New Progressive Disclosure Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   UserPromptSubmit Hook                      │
│                 (load_context_system.py)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Loads: context/CLAUDE.md                                   │
│           ↓                                                 │
│  CLAUDE.md instructs:                                       │
│  1. ALWAYS read core/ files (~65 lines total):              │
│     ├── core/identity.md (~10 lines)                        │
│     ├── core/preferences.md (~20 lines)                     │
│     ├── core/workflows.md (~20 lines)                       │
│     └── core/rules.md (~15 lines) ⭐ CHECK BEFORE ACTIONS   │
│                                                             │
│  2. ALWAYS read session/current.md (~10 lines)              │
│                                                             │
│  3. IF project-related, read projects/project_index.md      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        Stop Hook                             │
│                (update-memories-on-stop.py)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Points to: core/CLAUDE.md   ⬅️ UPDATED PATH                │
│           ↓                                                 │
│  CLAUDE.md instructs (autonomous updates):                  │
│                                                             │
│  1. Update session/current.md with active context           │
│                                                             │
│  2. IF correction detected:                                 │
│     → Add rule to core/rules.md                             │
│     → Notify: "Added rule: never X without asking"          │
│                                                             │
│  3. IF new preference learned:                              │
│     → Update core/preferences.md (replace old if exists)    │
│     → Notify: "Noted preference for X"                      │
│                                                             │
│  4. IF project status changed:                              │
│     → Update projects/project_index.md                      │
│                                                             │
│  5. Finish response                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why This Works with Progressive Disclosure

The new system actually **improves** progressive disclosure:

| Before | After |
|--------|-------|
| Read `memories.md` (325 lines) | Read `core/` files (~65 lines total) |
| Session logs mixed with preferences | Clean separation of concerns |
| May need to read full file for context | Quick scan of focused files |
| No clear priority for what to read | Clear reading order by importance |

### Key Design Principle Maintained

The hook stays minimal - it just points to instruction files. All the intelligence is in the CLAUDE.md files, which can be updated without touching the hooks.


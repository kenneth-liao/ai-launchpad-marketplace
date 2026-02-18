# User-Level Skill Architecture Design

**Date:** 2026-02-18
**Status:** Approved
**Scope:** Restructure all user-level Claude Code skills and plugins into a composable, generalized architecture that works across all projects.

---

## Problem

Skills, plugins, and context are scattered between user-level and project-level locations. YouTube content skills are project-scoped to `/projects/youtube` but needed everywhere. Writing voice is user-level but disconnected from content creation skills. Adding a new content type or platform requires building new skills from scratch instead of composing existing capabilities.

## Goal

A user-level plugin architecture where generalized skills handle core capabilities (writing, research, visual design) and thin orchestrator plugins compose them for specific workflows (plan a YouTube video, plan a newsletter issue). Everything installed at user level via the ai-launchpad-marketplace. Available across all projects.

---

## Skill Taxonomy

Every skill is classified into exactly one of four categories:

| Category | Role | Invocation | Examples |
|----------|------|------------|---------|
| **Knowledge** | Information that shapes output (brand, guidelines, design systems) | Referenced by task/orchestrator skills | `brand-guidelines`, `design-system` |
| **Personality** | How output sounds/feels (voice, tone) | Explicitly invoked by task skills that produce text | `voice` |
| **Task** | Does one thing well (research, write, generate) | Invoked by orchestrators or directly by users | `copywriting`, `research`, `title`, `hook`, `thumbnail` |
| **Orchestrator** | Sequences task skills for a platform-specific workflow | Invoked by users | `plan-video`, `plan-issue`, `repurpose-video` |
| **Meta** | Creates/maintains other skills within the framework | Invoked when building new skills | `create-skill` |

---

## Architecture

### Layer 1: Identity Context (always loaded, not a skill)

```
~/.claude/
├── .context/
│   ├── CLAUDE.md                   # Elle PA operating instructions — loads every session
│   ├── core/                       # Identity, preferences, rules, workflows, etc.
│   └── design-systems/             # Visual artifacts referenced by branding-kit
│       └── ink-and-ember/
```

This is ambient personal context. It is NOT a skill — it loads on every conversation. It grounds Claude in who Kenny is, how he works, and what his hard rules are.

### Layer 2: Foundation Plugins (generalized capabilities)

These hold task and personality skills that are content-type-agnostic.

#### writing/

```
writing/
└── skills/
    ├── voice/                      # PERSONALITY — Kenny's writing voice
    │   ├── SKILL.md                # Voice rules, anti-patterns, composition hooks
    │   └── references/
    │       └── voice-profile.md    # Full detailed voice analysis
    │
    └── copywriting/                # TASK — All written content, any length
        ├── SKILL.md                # Generalized writing skill
        └── references/
            ├── newsletter.md       # Newsletter structure & patterns
            ├── youtube-script.md   # Script structure & patterns
            ├── guide.md            # Guide/cheatsheet patterns
            ├── sales-page.md       # Product copy patterns
            ├── twitter.md          # Twitter/X conventions & limits
            ├── linkedin.md         # LinkedIn conventions
            └── substack-notes.md   # Substack Notes conventions
```

#### visual-design/

```
visual-design/
└── skills/
    ├── thumbnail/                  # TASK — Thumbnail concept creation
    │   ├── SKILL.md
    │   └── references/
    │       └── thumbnail-formulas.md   # Proven layouts, text rules, CTR patterns
    │
    └── social-graphic/             # TASK — Social media visual assets
        ├── SKILL.md
        └── references/
            └── platform-specs.md   # Dimensions, safe zones per platform
```

#### content-strategy/

```
content-strategy/
└── skills/
    ├── research/                   # TASK — Topic/competitor research
    │   ├── SKILL.md                # Generalized research methodology
    │   └── references/
    │       └── research-frameworks.md
    │
    ├── title/                      # TASK — Title/headline generation
    │   ├── SKILL.md
    │   └── references/
    │       ├── youtube-title-formulas.md
    │       ├── newsletter-subject-lines.md
    │       └── social-headlines.md
    │
    └── hook/                       # TASK — Opening hooks for any medium
        ├── SKILL.md
        └── references/
            ├── youtube-hooks.md        # 30-sec retention patterns
            ├── newsletter-hooks.md     # First-paragraph patterns
            └── social-hooks.md         # Scroll-stopping patterns
```

### Layer 3: Orchestrator Plugins (platform-specific workflows)

Thin plugins that compose foundation skills into platform-specific sequences.

#### youtube/

```
youtube/
├── skills/
│   ├── plan-video/                 # ORCHESTRATOR — Full video planning
│   │   └── SKILL.md               # Sequences: research -> title -> thumbnail -> hook -> outline
│   │
│   └── repurpose-video/            # ORCHESTRATOR — Turn video into other content
│       └── SKILL.md                # Sequences: extract key points -> newsletter draft -> social posts
│
├── agents/                         # YouTube-specific subagents (thumbnail designer, etc.)
└── mcp-servers/                    # YouTube Data API (existing yt-analytics MCP)
```

#### newsletter/

```
newsletter/
└── skills/
    └── plan-issue/                 # ORCHESTRATOR — Full newsletter planning
        └── SKILL.md                # Sequences: research -> copywriting -> subject line -> social promo
```

### Layer 3.5: System Plugin (framework maintenance)

#### skill-factory/

```
skill-factory/                          # System Plugin — meta-skills for framework maintenance
└── skills/
    └── create-skill/                   # META — Create new skills within the framework
        ├── SKILL.md                    # Enforces taxonomy, structure, composition patterns
        └── references/
            ├── taxonomy.md             # The four categories with decision criteria
            ├── skill-template-task.md          # Starter template for Task skills
            ├── skill-template-orchestrator.md  # Starter template for Orchestrator skills
            ├── skill-template-knowledge.md     # Starter template for Knowledge skills
            ├── skill-template-personality.md   # Starter template for Personality skills
            └── composition-patterns.md # Reference chain patterns, voice hooks, brand hooks
```

**What `create-skill` does:**

1. Asks what the skill needs to do
2. Classifies it into one of the four categories (Knowledge, Personality, Task, Orchestrator)
3. Determines which foundation plugin it belongs in (or if it needs a new orchestrator plugin)
4. Invokes `skill-creator:skill-creator` for skill authoring best practices
5. Invokes `superpowers:writing-skills` for skill file structure and quality
6. Applies framework-specific rules on top:
   - Task skills must include voice/brand reference chain hooks
   - Orchestrator skills must be thin (delegate, don't implement)
   - Platform-specific knowledge must live in `references/`, not in SKILL.md
   - SKILL.md must stay under 500 lines (progressive disclosure)
   - Flat structure enforced (max 2 levels)
7. Places the skill in the correct plugin directory

### Layer 4: Existing Plugins (unchanged)

| Plugin | Role | Notes |
|--------|------|-------|
| `branding-kit/` | Knowledge skills (brand-guidelines, design-system) | Already well-structured |
| `art/` | Task skill (nanobanana — Gemini image generation) | Already clean |
| `superpowers/` | Dev workflow skills (TDD, debugging, brainstorming, etc.) | Not content-related |
| `linear-pm/` | Project management skills | Not content-related |
| `frontend-design/` | Frontend design skill | Not content-related |

### Layer 5: Standalone User-Level Skills (unchanged)

```
~/.claude/skills/
├── gmail-email-categorization/     # Operations — out of scope
└── xlsx/                           # Utility — out of scope
```

---

## Composition Model

### How orchestrators compose task skills

An orchestrator like `youtube:plan-video` works by invoking foundation skills in sequence:

```
youtube:plan-video activates
    │
    ├─ Step 1: Invoke content-strategy:research
    │   └─ Uses YouTube MCP tools for video data
    │   └─ Returns: research brief
    │
    ├─ Step 2: Invoke content-strategy:title
    │   └─ Loads references/youtube-title-formulas.md
    │   └─ Invokes writing:voice
    │   └─ Returns: title candidates
    │
    ├─ Step 3: Invoke visual-design:thumbnail
    │   └─ Invokes branding-kit:brand-guidelines for design system
    │   └─ Uses art:nanobanana for image generation
    │   └─ Returns: thumbnail concept + image
    │
    ├─ Step 4: Invoke content-strategy:hook
    │   └─ Loads references/youtube-hooks.md
    │   └─ Invokes writing:voice
    │   └─ Returns: opening hook script
    │
    └─ Step 5: Invoke writing:copywriting
        └─ Loads references/youtube-script.md
        └─ Invokes writing:voice
        └─ Returns: video outline
```

The same foundation skills reused for a newsletter:

```
newsletter:plan-issue activates
    │
    ├─ Step 1: Invoke content-strategy:research
    │
    ├─ Step 2: Invoke writing:copywriting
    │   └─ Loads references/newsletter.md
    │   └─ Invokes writing:voice
    │   └─ Returns: newsletter draft
    │
    ├─ Step 3: Invoke content-strategy:title
    │   └─ Loads references/newsletter-subject-lines.md
    │   └─ Invokes writing:voice
    │   └─ Returns: subject line candidates
    │
    └─ Step 4: Invoke writing:copywriting
        └─ Loads references/twitter.md + references/linkedin.md
        └─ Invokes writing:voice
        └─ Returns: social promotion posts
```

### Reference chain pattern for voice/brand

Every task skill that produces text includes this standard block:

```markdown
## Voice Application
Before finalizing any written output, invoke the `writing:voice` skill
to apply voice rules. Pass the draft content and receive voice-corrected output.

## Brand Compliance
When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines`
to resolve the correct design system and check anti-patterns.
```

Explicit invocation. Deterministic. No relying on ambient activation.

---

## Migration Plan

| Current | Action | New Location |
|---------|--------|--------------|
| `~/.claude/skills/kenny-writing-voice/` | Move into writing plugin | `writing/skills/voice/` |
| `~/.claude/skills/the-ai-launchpad/` | Keep as user-level skill OR absorb into branding-kit | Decision: TBD during implementation |
| `~/.claude/skills/gmail-email-categorization/` | Keep as-is | Unchanged |
| `~/.claude/skills/xlsx/` | Keep as-is | Unchanged |
| `yt-content-strategist` plugin | Retire & rebuild | Split across foundation plugins + youtube orchestrator |
| `yt-content-strategist:youtube-title` | Generalize | `content-strategy/skills/title/` |
| `yt-content-strategist:youtube-thumbnail` | Generalize | `visual-design/skills/thumbnail/` |
| `yt-content-strategist:youtube-research-video-topic` | Generalize | `content-strategy/skills/research/` |
| `yt-content-strategist:youtube-video-hook` | Generalize | `content-strategy/skills/hook/` |
| `yt-content-strategist:youtube-plan-new-video` | Thin orchestrator | `youtube/skills/plan-video/` |
| YouTube MCP server (yt-analytics) | Move to youtube plugin | `youtube/mcp-servers/` |
| `branding-kit` plugin | Keep | Unchanged |
| `art` plugin | Keep | Unchanged |
| `~/.claude/.context/` (Elle PA) | Keep | Unchanged — identity layer, not a skill |
| `~/.claude/.context/design-systems/` | Keep | Referenced by branding-kit |
| (new) `skill-factory` plugin | Create | `skill-factory/skills/create-skill/` — meta-skill for framework-consistent skill creation |

---

## Design Principles

1. **Five skill categories, no exceptions.** Every skill is exactly one of: Knowledge, Personality, Task, Orchestrator, or Meta. If a skill is trying to be two things, split it.

2. **Generalize the capability, specialize through references.** Task skills are content-type-agnostic. Platform-specific knowledge lives in `references/` files. Adding a new platform = adding a reference file, not a new skill.

3. **Explicit invocation, not ambient activation.** Skills call the skills they need. `copywriting` explicitly invokes `voice`. `thumbnail` explicitly invokes `brand-guidelines`. No relying on description-based auto-activation for critical composition.

4. **Orchestrators are thin.** Orchestrator skills contain workflow sequence and platform-specific decisions. They delegate to task skills for all logic.

5. **Single source of truth per concept.** Voice rules live in one place. Brand identity lives in one place. Design systems live in one place. Skills reference, never copy.

6. **Progressive disclosure.** SKILL.md stays under 500 lines. Heavy content lives in `references/`. Loaded on demand, not upfront.

7. **Flat structure — max 2 levels.** `plugin/skills/skill-name/` is the deepest nesting.

8. **Three strikes, then generalize.** Don't pre-generalize. Extract shared patterns only when you see them repeated three times.

9. **Self-maintaining system.** All new skills are created through the `skill-factory:create-skill` meta-skill, which enforces the taxonomy, composition patterns, and structural rules. The framework maintains its own consistency.

---

## How Growth Works

| Scenario | What you do |
|----------|------------|
| New social platform (Threads, Bluesky) | Add a reference file to `copywriting/references/` |
| New content format (podcast) | New thin orchestrator plugin + reference files in existing task skills |
| New visual asset type (course banner) | Add reference to `social-graphic/references/` or new task skill if fundamentally different |
| New brand/business | New brand-guidelines skill via branding-kit, new voice skill in writing/ |
| Improve how titles work | Edit one skill (`content-strategy/skills/title/`) — all orchestrators benefit |
| Improve voice | Edit one skill (`writing/skills/voice/`) — all content benefits |

---

## Research References

This design was informed by:

- **Daniel Miessler's Personal AI Infrastructure v3.0** — Skill taxonomy, intent-based routing, flat structure rule, cascading context, persistent requirements documents
- **Fabric framework** — Unix pipe composition, "generalize capability, specialize through context", context layer separate from skills
- **Nick Tune's composable prompts** — Four-category skill taxonomy (Knowledge, Personality, Task, Orchestrator)
- **Claude Code skills architecture** — Progressive disclosure, meta-tool pattern, LLM-based routing, `context: fork` for isolation
- **Software design patterns** — Pipeline pattern (sequential composition), Strategy pattern (design system resolution), Decorator pattern (voice as transformation layer), Composition over inheritance

# User-Level Skill Architecture — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild all content creation skills into a composable, user-level plugin architecture with generalized foundation plugins and thin orchestrator plugins.

**Architecture:** Foundation plugins (writing, content-strategy, visual-design) hold generalized task/personality skills. Orchestrator plugins (youtube, newsletter) compose them into platform-specific workflows. A skill-factory meta-plugin ensures framework consistency for all future skills. See `docs/plans/2026-02-18-user-level-skill-architecture-design.md` for the full design.

**Tech Stack:** Claude Code plugins (SKILL.md, plugin.json, .mcp.json), Markdown, YAML frontmatter

---

## Build Order

The build order follows dependency chains: foundation skills first (no dependencies), then orchestrators (depend on foundation), then meta-skill (depends on the framework being established).

**Wave 1 — Foundation plugins (independent, can be built in parallel):**
- Task 1: `writing/` plugin (voice + copywriting)
- Task 2: `content-strategy/` plugin (research + title + hook)
- Task 3: `visual-design/` plugin (thumbnail + social-graphic)

**Wave 2 — Orchestrator plugins (depend on Wave 1):**
- Task 4: `youtube/` plugin (plan-video + repurpose-video)
- Task 5: `newsletter/` plugin (plan-issue)

**Wave 3 — System plugin + migration:**
- Task 6: `skill-factory/` plugin (create-skill meta-skill)
- Task 7: Register all new plugins in marketplace.json
- Task 8: Retire yt-content-strategist

---

## Task 1: Create `writing/` Plugin

This is the most critical foundation plugin. It holds the personality skill (voice) and the generalized copywriting task skill.

**Files:**
- Create: `writing/.claude-plugin/plugin.json`
- Create: `writing/README.md`
- Create: `writing/skills/voice/SKILL.md`
- Create: `writing/skills/voice/references/voice-profile.md`
- Create: `writing/skills/copywriting/SKILL.md`
- Create: `writing/skills/copywriting/references/newsletter.md`
- Create: `writing/skills/copywriting/references/youtube-script.md`
- Create: `writing/skills/copywriting/references/guide.md`
- Create: `writing/skills/copywriting/references/sales-page.md`
- Create: `writing/skills/copywriting/references/twitter.md`
- Create: `writing/skills/copywriting/references/linkedin.md`
- Create: `writing/skills/copywriting/references/substack-notes.md`

**Step 1: Create plugin scaffold**

Create `writing/.claude-plugin/plugin.json`:
```json
{
  "name": "writing",
  "description": "A plugin for writing content in Kenny's authentic voice across all content types and platforms",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `writing/README.md` with a brief description of the plugin, its two skills (voice, copywriting), and how they compose.

**Step 2: Create the voice personality skill**

Create `writing/skills/voice/SKILL.md`.

This skill is migrated from `~/.claude/skills/kenny-writing-voice/SKILL.md`. The content is proven and well-structured — preserve it almost entirely. Key changes:
- Update the `name` in frontmatter to `voice`
- Update the `description` to be more general: "Apply Kenny Liao's authentic writing voice to any written content. This is a PERSONALITY skill — it transforms content produced by other skills into Kenny's voice. Invoke this skill explicitly from any task skill that produces written output."
- Keep all voice rules, anti-patterns, and the reference to `references/voice-profile.md`
- Add a "How Other Skills Should Invoke This Skill" section at the top explaining the explicit invocation pattern

Create `writing/skills/voice/references/voice-profile.md` — copy from `~/.claude/skills/kenny-writing-voice/references/voice-profile.md` (no changes needed, this is reference data).

**Step 3: Create the copywriting task skill**

Create `writing/skills/copywriting/SKILL.md`.

This is a NEW generalized skill. It does NOT exist currently — it replaces scattered writing logic across multiple skills.

The SKILL.md should include:
- Frontmatter: `name: copywriting`, description explaining it handles all written content types
- Overview: Generalized writing skill that produces written content for any platform/format
- "Content Type Resolution" section: Based on user request, determine which reference doc to load (newsletter.md, youtube-script.md, twitter.md, etc.)
- "Standard Workflow" section:
  1. Determine content type from context
  2. Load the appropriate platform reference from `references/`
  3. Gather context (topic, audience, key message, any research)
  4. Draft content following the platform reference structure
  5. Invoke `writing:voice` skill to apply Kenny's voice
  6. Invoke `branding-kit:brand-guidelines` for brand compliance check
  7. Present to user for feedback
- "Voice Application" reference chain hook (explicit invocation of writing:voice)
- "Brand Compliance" reference chain hook (explicit invocation of branding-kit:brand-guidelines)
- Quality checklist

**Step 4: Create platform reference files**

These reference files contain platform-specific patterns, structures, and conventions. They are loaded by the copywriting skill based on content type.

Create these files under `writing/skills/copywriting/references/`:

- `newsletter.md` — Newsletter structure (Substack): typical issue structure, section patterns, length guidelines, subject line conventions, CTA patterns. Pull from Kenny's existing newsletter patterns.
- `youtube-script.md` — YouTube script structure: hook → intro → main content sections → CTA → outro, timing guidelines, demonstration/example patterns.
- `guide.md` — Guide/cheatsheet structure: problem statement → solution framework → step-by-step → summary takeaway.
- `sales-page.md` — Product copy structure: headline → problem → solution → proof → CTA, urgency patterns, objection handling.
- `twitter.md` — Twitter/X conventions: character limits, thread structure, hook tweet patterns, engagement patterns.
- `linkedin.md` — LinkedIn conventions: professional tone adjustments, post structure, hashtag usage.
- `substack-notes.md` — Substack Notes conventions: short-form patterns, engagement hooks.

Each reference file should be 50-150 lines, focused on structure and patterns, not voice (voice comes from the voice skill).

**Step 5: Verify plugin structure**

```bash
find writing/ -type f | sort
```

Expected output should match the file list above. Verify SKILL.md frontmatter is valid YAML.

**Step 6: Commit**

```bash
git add writing/
git commit -m "feat: add writing foundation plugin with voice and copywriting skills"
```

---

## Task 2: Create `content-strategy/` Plugin

This plugin holds the generalized research, title generation, and hook creation skills.

**Files:**
- Create: `content-strategy/.claude-plugin/plugin.json`
- Create: `content-strategy/README.md`
- Create: `content-strategy/skills/research/SKILL.md`
- Create: `content-strategy/skills/research/references/research-frameworks.md`
- Create: `content-strategy/skills/title/SKILL.md`
- Create: `content-strategy/skills/title/references/youtube-title-formulas.md`
- Create: `content-strategy/skills/title/references/newsletter-subject-lines.md`
- Create: `content-strategy/skills/title/references/social-headlines.md`
- Create: `content-strategy/skills/hook/SKILL.md`
- Create: `content-strategy/skills/hook/references/youtube-hooks.md`
- Create: `content-strategy/skills/hook/references/newsletter-hooks.md`
- Create: `content-strategy/skills/hook/references/social-hooks.md`

**Step 1: Create plugin scaffold**

Create `content-strategy/.claude-plugin/plugin.json`:
```json
{
  "name": "content-strategy",
  "description": "A plugin for content research, title generation, and hook creation across all platforms",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `content-strategy/README.md`.

**Step 2: Create the research task skill**

Create `content-strategy/skills/research/SKILL.md`.

Generalize from `yt-content-strategist:youtube-research-video-topic`. Key changes:
- Name: `research` (not youtube-research-video-topic)
- Description: Generalized topic/competitor research for any content type
- Remove YouTube-specific tool references from the core workflow — those belong in the youtube orchestrator or are passed in as context
- Keep the research methodology: understand topic → research existing content → competitor analysis → content gap analysis
- Make the output structure generic (not episode-specific):
  - Topic overview
  - Existing content landscape
  - Competitor analysis
  - Content gaps with ratings
  - Recommended angle
- Add "Platform-Specific Research Tools" section explaining that orchestrator skills may provide platform-specific MCP tools (YouTube analytics, etc.)
- Add voice/brand reference chain hooks

Create `content-strategy/skills/research/references/research-frameworks.md` — research methodology patterns, gap analysis frameworks, competitor analysis templates.

**Step 3: Create the title task skill**

Create `content-strategy/skills/title/SKILL.md`.

Generalize from `yt-content-strategist:youtube-title`. Key changes:
- Name: `title` (not youtube-title)
- Description: Generate optimized titles/headlines for any content type
- Keep the core methodology: curiosity generation, complementarity, question-prompting
- Remove YouTube-specific patterns from SKILL.md — move to `references/youtube-title-formulas.md`
- Add "Content Type Resolution" section: determine which platform reference to load
- Add voice/brand reference chain hooks
- Keep the verification checklist (curiosity test, complementarity test, etc.) — these are universal

Create platform references:
- `references/youtube-title-formulas.md` — Extract YouTube-specific patterns from existing `youtube-title/references/design-requirements.md`. Include: curiosity formulas, forbidden patterns, content type applications (educational, entertainment, tech/AI).
- `references/newsletter-subject-lines.md` — Email subject line patterns: open rate optimization, preview text, personalization, urgency/curiosity balance.
- `references/social-headlines.md` — Social post headlines: scroll-stopping patterns, platform-specific hooks.

**Step 4: Create the hook task skill**

Create `content-strategy/skills/hook/SKILL.md`.

Generalize from `yt-content-strategist:youtube-video-hook`. Key changes:
- Name: `hook` (not youtube-video-hook)
- Description: Create retention-optimized opening hooks for any content type
- Keep the core methodology: curiosity extension, forbidden patterns, hook timing
- Generalize "opening seconds" to "opening content" — works for video, newsletter intro paragraph, social post first line
- Remove YouTube-specific algorithm discussion — move to references
- Add "Content Type Resolution" section
- Add voice/brand reference chain hooks

Create platform references:
- `references/youtube-hooks.md` — Extract from existing `youtube-video-hook` SKILL.md: the YouTube-specific patterns (5-15 second timing, algorithm implications, video-specific forbidden patterns like "welcome first").
- `references/newsletter-hooks.md` — Newsletter opening patterns: first-paragraph hooks, preview text alignment, subject-to-opening flow.
- `references/social-hooks.md` — Social post opening patterns: scroll-stopping first lines, thread opener patterns.

**Step 5: Verify plugin structure**

```bash
find content-strategy/ -type f | sort
```

**Step 6: Commit**

```bash
git add content-strategy/
git commit -m "feat: add content-strategy foundation plugin with research, title, and hook skills"
```

---

## Task 3: Create `visual-design/` Plugin

**Files:**
- Create: `visual-design/.claude-plugin/plugin.json`
- Create: `visual-design/README.md`
- Create: `visual-design/skills/thumbnail/SKILL.md`
- Create: `visual-design/skills/thumbnail/references/thumbnail-formulas.md`
- Create: `visual-design/skills/thumbnail/references/prompting-guidelines.md`
- Create: `visual-design/skills/social-graphic/SKILL.md`
- Create: `visual-design/skills/social-graphic/references/platform-specs.md`

**Step 1: Create plugin scaffold**

Create `visual-design/.claude-plugin/plugin.json`:
```json
{
  "name": "visual-design",
  "description": "A plugin for creating visual assets including thumbnails and social media graphics",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `visual-design/README.md`.

**Step 2: Create the thumbnail task skill**

Create `visual-design/skills/thumbnail/SKILL.md`.

Generalize from `yt-content-strategist:youtube-thumbnail`. Key changes:
- Name: `thumbnail` (not youtube-thumbnail)
- Description: Create high-performing thumbnails for any platform (YouTube, course, blog)
- Keep Thumbkit integration (installation, usage, documentation commands)
- Keep the review workflow (Thumbnail Reviewer agent)
- Keep reference image handling (logos, headshots, outlier analysis)
- Keep prompting guidelines reference
- Generalize the design requirements to work beyond YouTube — the core principles (clarity at small size, text legibility, emotion) are universal
- Add brand reference chain hook (invoke branding-kit:brand-guidelines for design system resolution)

Create references:
- `references/thumbnail-formulas.md` — Migrated from `youtube-thumbnail/references/design-requirements.md`. Keep all proven design patterns, composition rules, text rules.
- `references/prompting-guidelines.md` — Migrated from `youtube-thumbnail/references/prompting-guidelines.md`. Keep Gemini/NanoBanana prompting best practices.

**Step 3: Create the social-graphic task skill**

Create `visual-design/skills/social-graphic/SKILL.md`.

This is a NEW skill (no existing equivalent). It handles social media visual assets.

Include:
- Generalized workflow for creating social graphics
- Integration with `art:nanobanana` for image generation
- Brand reference chain hook (invoke branding-kit:brand-guidelines)
- Platform-specific dimension/format resolution via references

Create `references/platform-specs.md` — dimensions, safe zones, text limits for each platform (Twitter cards, LinkedIn posts, Instagram, Substack headers).

**Step 4: Verify and commit**

```bash
find visual-design/ -type f | sort
git add visual-design/
git commit -m "feat: add visual-design foundation plugin with thumbnail and social-graphic skills"
```

---

## Task 4: Create `youtube/` Orchestrator Plugin

This is a thin orchestrator that composes foundation skills for YouTube-specific workflows.

**Files:**
- Create: `youtube/.claude-plugin/plugin.json`
- Create: `youtube/.mcp.json`
- Create: `youtube/README.md`
- Create: `youtube/skills/plan-video/SKILL.md`
- Create: `youtube/skills/repurpose-video/SKILL.md`
- Create: `youtube/agents/youtube-researcher.md`
- Create: `youtube/agents/thumbnail-reviewer.md`
- Move: `yt-content-strategist/servers/py-mcp-youtube-toolbox/` → `youtube/servers/py-mcp-youtube-toolbox/`

**Step 1: Create plugin scaffold**

Create `youtube/.claude-plugin/plugin.json`:
```json
{
  "name": "youtube",
  "description": "A plugin for YouTube content workflows — orchestrates research, writing, and design skills for video production",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `youtube/README.md`.

**Step 2: Move the MCP server**

Copy the YouTube analytics MCP server from yt-content-strategist:

```bash
cp -r yt-content-strategist/servers youtube/servers
```

Create `youtube/.mcp.json`:
```json
{
  "mcpServers": {
    "youtube-analytics": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${CLAUDE_PLUGIN_ROOT}/servers/py-mcp-youtube-toolbox",
        "server.py"
      ],
      "env": {
        "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
      }
    }
  }
}
```

**Step 3: Move the agents**

Copy agents from yt-content-strategist:

```bash
cp -r yt-content-strategist/agents youtube/agents
```

Update tool references in agent files if the MCP tool naming changes due to plugin rename (tools are prefixed with plugin name: `mcp__plugin_{plugin-name}_{server-name}__{tool-name}`).

The YouTube Researcher agent tool references will need to change from `mcp__plugin_yt-content-strategist_youtube-analytics__*` to `mcp__plugin_youtube_youtube-analytics__*`.

**Step 4: Create plan-video orchestrator skill**

Create `youtube/skills/plan-video/SKILL.md`.

This is a thin orchestrator adapted from `yt-content-strategist:youtube-plan-new-video`. Key changes:
- Name: `plan-video`
- Description: Orchestrates foundation skills to create a complete YouTube video plan
- The skill should be THIN — it's a workflow recipe, not logic
- Replace direct content generation with skill invocations:
  1. Invoke `content-strategy:research` (pass YouTube MCP tools as available context)
  2. Invoke `content-strategy:title` (loads `references/youtube-title-formulas.md` automatically)
  3. Invoke `visual-design:thumbnail` (loads `references/thumbnail-formulas.md` automatically)
  4. Invoke `content-strategy:hook` (loads `references/youtube-hooks.md` automatically)
  5. Invoke `writing:copywriting` for the outline (loads `references/youtube-script.md` automatically)
- Keep the user selection workflow (present options → user picks → finalize)
- Keep the AB testing thumbnail workflow from Step 7 of original
- Keep the plan file output structure
- Add YouTube-specific context: episode numbering, file saving conventions, channel info loading

**Step 5: Create repurpose-video orchestrator skill**

Create `youtube/skills/repurpose-video/SKILL.md`.

This is a NEW orchestrator. Workflow:
1. Load a completed video's research/plan/transcript
2. Invoke `writing:copywriting` with `references/newsletter.md` to draft a newsletter issue from video content
3. Invoke `writing:copywriting` with `references/twitter.md` for Twitter thread
4. Invoke `writing:copywriting` with `references/linkedin.md` for LinkedIn post
5. Invoke `writing:copywriting` with `references/substack-notes.md` for Substack Note
6. All invocations also invoke `writing:voice` for voice consistency

**Step 6: Verify and commit**

```bash
find youtube/ -type f | sort
git add youtube/
git commit -m "feat: add youtube orchestrator plugin with plan-video and repurpose-video skills"
```

---

## Task 5: Create `newsletter/` Orchestrator Plugin

**Files:**
- Create: `newsletter/.claude-plugin/plugin.json`
- Create: `newsletter/README.md`
- Create: `newsletter/skills/plan-issue/SKILL.md`

**Step 1: Create plugin scaffold**

Create `newsletter/.claude-plugin/plugin.json`:
```json
{
  "name": "newsletter",
  "description": "A plugin for newsletter content workflows — orchestrates research, writing, and design skills for newsletter production",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `newsletter/README.md`.

**Step 2: Create plan-issue orchestrator skill**

Create `newsletter/skills/plan-issue/SKILL.md`.

This is a NEW orchestrator. Workflow:
1. Invoke `content-strategy:research` to research the topic
2. Invoke `writing:copywriting` with `references/newsletter.md` to draft the issue
3. Invoke `content-strategy:title` with `references/newsletter-subject-lines.md` for subject line options
4. Invoke `content-strategy:hook` with `references/newsletter-hooks.md` for opening paragraph
5. Invoke `writing:copywriting` with `references/twitter.md` + `references/linkedin.md` for social promotion posts
6. All text invocations also invoke `writing:voice`
7. Optionally invoke `visual-design:social-graphic` for newsletter header image

Output: A plan file with draft issue, subject line options, opening hook options, and social promotion posts.

**Step 3: Verify and commit**

```bash
find newsletter/ -type f | sort
git add newsletter/
git commit -m "feat: add newsletter orchestrator plugin with plan-issue skill"
```

---

## Task 6: Create `skill-factory/` System Plugin

**Files:**
- Create: `skill-factory/.claude-plugin/plugin.json`
- Create: `skill-factory/README.md`
- Create: `skill-factory/skills/create-skill/SKILL.md`
- Create: `skill-factory/skills/create-skill/references/taxonomy.md`
- Create: `skill-factory/skills/create-skill/references/skill-template-task.md`
- Create: `skill-factory/skills/create-skill/references/skill-template-orchestrator.md`
- Create: `skill-factory/skills/create-skill/references/skill-template-knowledge.md`
- Create: `skill-factory/skills/create-skill/references/skill-template-personality.md`
- Create: `skill-factory/skills/create-skill/references/composition-patterns.md`

**Step 1: Create plugin scaffold**

Create `skill-factory/.claude-plugin/plugin.json`:
```json
{
  "name": "skill-factory",
  "description": "A meta-plugin for creating new skills that conform to the composable skill architecture framework",
  "version": "1.0.0",
  "author": {
    "name": "Kenny Liao (The AI Launchpad)",
    "url": "https://www.youtube.com/@KennethLiao"
  }
}
```

Create `skill-factory/README.md`.

**Step 2: Create the create-skill meta-skill**

Create `skill-factory/skills/create-skill/SKILL.md`.

Workflow:
1. Ask what the skill needs to do
2. Read `references/taxonomy.md` to classify the skill into one of five categories
3. Based on category, determine:
   - Which plugin it belongs in (existing foundation/orchestrator, or new plugin needed)
   - Which template to use
4. Invoke `skill-creator:skill-creator` for skill authoring best practices
5. Invoke `superpowers:writing-skills` for skill file structure and quality
6. Load the appropriate template from references
7. Generate the skill following the template + framework rules
8. Apply framework validation:
   - Task skills must include voice/brand reference chain hooks
   - Orchestrator skills must be thin (delegate, don't implement)
   - Platform-specific knowledge must live in `references/`, not in SKILL.md
   - SKILL.md must stay under 500 lines
   - Flat structure (max 2 levels)
9. Place the skill in the correct plugin directory
10. Update plugin version if adding to existing plugin

**Step 3: Create reference files**

Create `references/taxonomy.md`:
- Decision tree for classifying skills into Knowledge, Personality, Task, Orchestrator, or Meta
- Examples of each category from the existing system
- "If it's trying to be two things, split it" rule

Create `references/skill-template-task.md`:
- Template SKILL.md for Task skills
- Required sections: frontmatter, overview, when to use, content type resolution, workflow, voice application hook, brand compliance hook, quality checklist
- Placeholder comments showing where to fill in skill-specific content

Create `references/skill-template-orchestrator.md`:
- Template SKILL.md for Orchestrator skills
- Required sections: frontmatter, overview, prerequisites, workflow (sequence of skill invocations), output structure
- Emphasis on being thin — delegate to task skills

Create `references/skill-template-knowledge.md`:
- Template SKILL.md for Knowledge skills
- Required sections: frontmatter, the knowledge content, how other skills should reference this

Create `references/skill-template-personality.md`:
- Template SKILL.md for Personality skills
- Required sections: frontmatter, personality rules, anti-patterns, how other skills should invoke this

Create `references/composition-patterns.md`:
- The voice application reference chain hook block
- The brand compliance reference chain hook block
- How to load platform-specific references
- How to invoke other skills from within a skill
- Examples from the existing system

**Step 4: Verify and commit**

```bash
find skill-factory/ -type f | sort
git add skill-factory/
git commit -m "feat: add skill-factory meta-plugin for framework-consistent skill creation"
```

---

## Task 7: Register All New Plugins in Marketplace

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Read current marketplace.json**

Read `.claude-plugin/marketplace.json` to see current plugin registrations.

**Step 2: Add new plugins**

Add entries for all 6 new plugins to the `plugins` array:
```json
{
  "name": "writing",
  "source": "./writing",
  "description": "A plugin for writing content in Kenny's authentic voice across all content types and platforms"
},
{
  "name": "content-strategy",
  "source": "./content-strategy",
  "description": "A plugin for content research, title generation, and hook creation across all platforms"
},
{
  "name": "visual-design",
  "source": "./visual-design",
  "description": "A plugin for creating visual assets including thumbnails and social media graphics"
},
{
  "name": "youtube",
  "source": "./youtube",
  "description": "A plugin for YouTube content workflows — orchestrates research, writing, and design skills for video production"
},
{
  "name": "newsletter",
  "source": "./newsletter",
  "description": "A plugin for newsletter content workflows — orchestrates research, writing, and design skills for newsletter production"
},
{
  "name": "skill-factory",
  "source": "./skill-factory",
  "description": "A meta-plugin for creating new skills that conform to the composable skill architecture framework"
}
```

**Step 3: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: register all new plugins in marketplace"
```

---

## Task 8: Retire `yt-content-strategist`

This is the final step. The old plugin is now fully replaced.

**Step 1: Verify replacement completeness**

Before removing anything, verify that every capability from yt-content-strategist has a new home:

| Old Skill | New Location | Status |
|-----------|-------------|--------|
| youtube-research-video-topic | content-strategy:research + youtube:plan-video | Verify |
| youtube-title | content-strategy:title | Verify |
| youtube-thumbnail | visual-design:thumbnail | Verify |
| youtube-video-hook | content-strategy:hook | Verify |
| youtube-plan-new-video | youtube:plan-video | Verify |
| YouTube Researcher agent | youtube/agents/youtube-researcher.md | Verify |
| Thumbnail Reviewer agent | youtube/agents/thumbnail-reviewer.md | Verify |
| youtube-analytics MCP | youtube/servers/py-mcp-youtube-toolbox/ | Verify |

**Step 2: Remove yt-content-strategist from marketplace.json**

Remove the yt-content-strategist entry from `.claude-plugin/marketplace.json`.

**Step 3: Do NOT delete the yt-content-strategist directory yet**

Keep it for reference during the transition period. It can be archived or deleted in a future cleanup once the new system is validated.

Add a deprecation notice to `yt-content-strategist/README.md`:
```markdown
> **DEPRECATED**: This plugin has been replaced by the composable skill architecture.
> See: writing/, content-strategy/, visual-design/, youtube/ plugins.
> This directory is kept for reference and will be removed in a future cleanup.
```

**Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json yt-content-strategist/README.md
git commit -m "feat: deprecate yt-content-strategist in favor of composable architecture"
```

---

## Post-Implementation

After all tasks are complete:

1. **Install new plugins at user level** — Run the marketplace install commands for each new plugin
2. **Uninstall yt-content-strategist** — Remove the old plugin from user-level installations
3. **Move user-level voice skill** — `~/.claude/skills/kenny-writing-voice/` is now redundant since voice lives in the writing plugin. Archive or remove it.
4. **Smoke test** — Open a new Claude Code session and verify:
   - `writing:voice` and `writing:copywriting` are available
   - `content-strategy:research`, `content-strategy:title`, `content-strategy:hook` are available
   - `visual-design:thumbnail` and `visual-design:social-graphic` are available
   - `youtube:plan-video` can orchestrate the foundation skills
   - `newsletter:plan-issue` can orchestrate the foundation skills
   - `skill-factory:create-skill` can create a new skill following the framework
5. **Test across projects** — Open Claude Code in a different project directory and verify all skills are available (they should be since they're user-level)

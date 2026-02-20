---
name: create-skill
description: Create new skills that conform to the composable skill architecture framework. This is a META skill — it classifies the skill, selects the right template, generates the skill following framework rules, and validates the output against architecture constraints.
---

# Create Skill

## Overview

This meta-skill guides the creation of new skills that conform to the composable skill architecture. Every skill in the system follows a consistent pattern: it belongs to a category, lives in the right plugin, uses the right template, and includes the required composition hooks. This skill enforces all of that.

**Core Principle**: The skill-factory exists to enforce consistency. New skills should look and behave like existing ones. If a new skill breaks the pattern, it breaks the architecture.

## When to Use

Use this skill when:
- Creating a new skill from scratch
- Adding a skill to an existing plugin
- Creating a new plugin with its first skill
- Unsure which category or plugin a skill belongs in
- Wanting to ensure a skill follows the framework rules

## Skill Creation Workflow

Execute all steps below in order. Do not skip steps.

### Step 1: Understand the Skill

Ask the user what the skill needs to do. Gather:

- **Purpose**: What problem does this skill solve?
- **Trigger**: When should this skill be invoked? By a user directly, or by another skill?
- **Inputs**: What does the skill need to start? (topic, source material, context from another skill)
- **Outputs**: What does the skill produce? (content, plan, visual asset, reference document)
- **Interactions**: Does the skill invoke other skills, or is it invoked by other skills?

If the user's description suggests the skill is trying to do two things, flag it immediately: "This sounds like two skills. The framework rule is: if it's trying to be two things, split it."

If the skill is classified as a **Task** in Step 2, also ask:
- **Scripts**: Does the skill include executable Python scripts (API wrappers, data processors, image generators)? If yes, this is a **script-bearing task skill** and will use the uv + PEP 723 architecture in Step 6.

### Step 2: Classify the Skill

**MANDATORY**: Read `references/taxonomy.md` to classify the skill into one of five categories.

Walk through the decision tree with the user:

1. Does it provide information that shapes other skills' output? --> **Knowledge**
2. Does it define how output sounds/feels? --> **Personality**
3. Does it do one specific thing well (research, write, generate)? --> **Task**
4. Does it sequence multiple task skills for a platform-specific workflow? --> **Orchestrator**
5. Does it create or maintain other skills within the framework? --> **Meta**

Present the classification to the user with rationale. If the classification is ambiguous, explain the tradeoffs and let the user decide.

### Step 3: Determine Plugin Placement

Based on the classification, determine where the skill belongs:

**Knowledge skills** --> Typically `branding-kit/` or a new domain-specific knowledge plugin
**Personality skills** --> Typically `writing/`
**Task skills** --> One of the foundation plugins:
- `writing/` -- for content production skills
- `content-strategy/` -- for research, title, hook, and planning skills
- `visual-design/` -- for image and visual asset skills
- Or a new foundation plugin if the skill doesn't fit existing ones
**Orchestrator skills** --> Platform-specific plugins:
- `youtube/` -- for YouTube workflows
- `newsletter/` -- for newsletter workflows
- Or a new orchestrator plugin for a new platform
**Meta skills** --> `skill-factory/`

If the skill doesn't fit an existing plugin, create a new plugin:
1. Create the plugin directory with `.claude-plugin/plugin.json`
2. Create a README.md for the plugin
3. Place the skill in `skills/[skill-name]/`

### Step 4: Invoke Skill Authoring Best Practices

**MANDATORY**: Invoke `skill-creator:skill-creator` to load skill authoring best practices. This provides guidance on:
- SKILL.md writing style (imperative/infinitive form)
- Frontmatter quality (name and description determine when Claude uses the skill)
- Progressive disclosure (metadata -> SKILL.md -> references)
- Bundled resource organization (scripts, references, assets)

Apply these best practices throughout the remaining steps.

### Step 5: Invoke Writing Skills Guidance

**MANDATORY**: Invoke `superpowers:writing-skills` to load guidance on skill file structure and quality. This provides patterns for:
- How to structure SKILL.md sections
- How to write clear, actionable instructions
- How to organize reference files
- Quality standards for skill content

Apply this guidance throughout the remaining steps.

### Step 6: Load and Apply the Template

Based on the skill's category, load the appropriate template from `references/`:

| Category | Template File |
|---|---|
| Knowledge | `references/skill-template-knowledge.md` |
| Personality | `references/skill-template-personality.md` |
| Task | `references/skill-template-task.md` |
| Orchestrator | `references/skill-template-orchestrator.md` |
| Meta | Use this skill (create-skill) as the reference pattern |

**MANDATORY**: Read the template file before generating the skill. The template defines the required sections and structure for the category.

**For script-bearing task skills**: After loading `references/skill-template-task.md`, activate the conditional sections marked `<!-- CONDITIONAL -->`. These add:
- Prerequisites section with `uv` check and install instructions
- Scripts section with PEP 723 pattern and script conventions
- Downstream Integration patterns for CLI and Python API consumption

Use `art:nanobanana` as the reference implementation for this pattern.

### Step 7: Generate the Skill

Generate the SKILL.md file following the template structure. For each section:

1. Fill in the frontmatter with a descriptive name and description
2. Write the overview explaining what the skill does
3. Define when to use the skill
4. Build the workflow or content sections per the template
5. Add composition hooks per `references/composition-patterns.md`
6. Write the quality checklist

**MANDATORY**: Read `references/composition-patterns.md` to apply the correct composition hooks based on the skill category:
- **Task skills**: Must include voice application and brand compliance hooks
- **Orchestrator skills**: Must delegate to task skills using `plugin:skill` syntax
- **Knowledge skills**: Must document how other skills reference them
- **Personality skills**: Must document how other skills invoke them

If the skill needs platform-specific references (e.g., YouTube title formulas, newsletter structure), create those reference files in `references/` and document them in the Content Type Resolution table.

### Step 8: Validate Against Framework Rules

Before finalizing, verify the skill against all framework constraints:

**Structural Validation:**
- [ ] SKILL.md is under 500 lines
- [ ] Directory structure is flat (max 2 levels: `skills/[skill-name]/` with optional `references/`)
- [ ] Frontmatter includes `name` and `description`
- [ ] Description clearly states what the skill does and when to use it

**Category-Specific Validation:**

For **Task skills**:
- [ ] Includes voice application hook: "Invoke `writing:voice` before finalizing any written output"
- [ ] Includes brand compliance hook: "When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines`"
- [ ] Content Type Resolution table present (if skill handles multiple content types)
- [ ] Quality checklist present
- [ ] Does one thing well -- not trying to be two skills

For **Script-bearing task skills** (in addition to standard Task validation):
- [ ] `scripts/` directory exists in the skill directory
- [ ] Every `.py` file in `scripts/` contains a PEP 723 inline dependency block (`# /// script`)
- [ ] PEP 723 block includes `requires-python` version constraint
- [ ] PEP 723 block includes `dependencies` list (can be empty `[]`)
- [ ] SKILL.md never references `python3` as the primary execution method -- always `uv run`
- [ ] Prerequisites section present with `uv` check and install instructions
- [ ] Script return format documented (consistent dict structure)
- [ ] CLI usage with `--help` documented in SKILL.md

For **Orchestrator skills**:
- [ ] Is a THIN orchestrator -- delegates to task skills, does not implement content generation
- [ ] All content generation steps use `plugin:skill` invocation syntax
- [ ] Never generates titles, hooks, content, or visuals manually
- [ ] Output structure template present
- [ ] Quality checklist verifies each skill invocation happened

For **Knowledge skills**:
- [ ] Contains the knowledge content directly (guidelines, rules, specifications)
- [ ] Documents how other skills should reference it
- [ ] Platform-specific knowledge lives in `references/`, not in SKILL.md

For **Personality skills**:
- [ ] Defines personality rules clearly (voice characteristics, tone, style)
- [ ] Lists anti-patterns (what to avoid)
- [ ] Documents how other skills should invoke it

For **Meta skills**:
- [ ] Serves the framework itself (creates, maintains, or validates other skills)
- [ ] References framework documentation as needed

**Composition Validation:**
- [ ] If the skill produces written output, it invokes `writing:voice`
- [ ] If the skill produces branded assets, it invokes `branding-kit:brand-guidelines`
- [ ] If the skill delegates to other skills, it uses `plugin:skill` syntax
- [ ] Platform-specific content lives in `references/`, not inline in SKILL.md

If any validation fails, fix the issue before proceeding.

### Step 9: Place the Skill

Write the skill files to the correct plugin directory:

1. Create the skill directory: `[plugin]/skills/[skill-name]/`
2. Write `SKILL.md` to the skill directory
3. Write any reference files to `[plugin]/skills/[skill-name]/references/`
4. If this is a new plugin, create the plugin structure first (`.claude-plugin/plugin.json`, `README.md`)

### Step 10: Update Plugin Version (If Existing Plugin)

If adding a skill to an existing plugin:

1. Read the plugin's `.claude-plugin/plugin.json`
2. Increment the patch version (e.g., `1.0.0` -> `1.1.0`)
3. Update the plugin's `README.md` to document the new skill

## Quality Checklist

Before finalizing the skill creation:

- [ ] User's requirements understood (Step 1)
- [ ] Skill classified using taxonomy decision tree (Step 2)
- [ ] Plugin placement determined (Step 3)
- [ ] `skill-creator:skill-creator` invoked for authoring best practices (Step 4)
- [ ] `superpowers:writing-skills` invoked for file structure guidance (Step 5)
- [ ] Appropriate template loaded and followed (Step 6)
- [ ] Skill generated with all required sections (Step 7)
- [ ] All framework validation checks pass (Step 8)
- [ ] Skill placed in correct plugin directory (Step 9)
- [ ] Plugin version updated if adding to existing plugin (Step 10)
- [ ] SKILL.md under 500 lines
- [ ] No placeholder content or unresolved TODOs in the final skill

## Common Pitfalls to Avoid

1. **Multi-purpose skills**: A skill that researches AND writes AND formats. Split it. Each skill does one thing.
2. **Fat orchestrators**: An orchestrator that generates content instead of delegating. Orchestrators are thin -- they invoke task skills.
3. **Missing composition hooks**: A task skill that produces text but never invokes `writing:voice`. Every text-producing task skill needs the voice hook.
4. **Inline platform knowledge**: YouTube title formulas embedded in SKILL.md instead of in `references/youtube-title-formulas.md`. Platform-specific content goes in references.
5. **Vague descriptions**: A frontmatter description like "Does stuff with content." The description determines when Claude uses the skill -- make it specific.
6. **Wrong category**: Calling something a "task" when it actually sequences other skills (that's an orchestrator). Use the taxonomy decision tree.
7. **Skipping validation**: Generating the skill and assuming it's correct. Always run the validation checklist.
8. **Raw python3 in script-bearing skills**: Using `python3 script.py` instead of `uv run script.py`. The uv + PEP 723 pattern is the standard for zero-setup portability. Always use `uv run`.

## Example Execution

**Scenario**: User wants a skill to generate LinkedIn carousel posts.

1. **Understand**: Produces carousel slide content from a topic. User invokes directly or via an orchestrator. Outputs: slide text, layout suggestions, CTA.
2. **Classify**: This does one thing (generate carousel content) -> **Task skill**.
3. **Plugin**: Content production -> `writing/` plugin. But it also has a visual component -> could split into writing (slide text via `writing:copywriting`) and visual (layout via `visual-design:social-graphic`). Recommend using existing skills rather than creating a new one, or create a thin orchestrator if the workflow is platform-specific enough.
4. **Invoke** `skill-creator:skill-creator` for authoring best practices.
5. **Invoke** `superpowers:writing-skills` for structure guidance.
6. **Template**: Load `references/skill-template-task.md`.
7. **Generate**: Create SKILL.md with frontmatter, overview, content type resolution, workflow, voice hook, brand hook, quality checklist.
8. **Validate**: Check all framework rules. Verify voice and brand hooks present. Confirm under 500 lines.
9. **Place**: Write to `writing/skills/linkedin-carousel/SKILL.md` with `references/linkedin-carousel.md` for platform conventions.
10. **Update**: Bump `writing/.claude-plugin/plugin.json` version to `1.1.0`. Update `writing/README.md`.

**Result**: A new task skill that follows all framework patterns and integrates cleanly with the existing composition system.

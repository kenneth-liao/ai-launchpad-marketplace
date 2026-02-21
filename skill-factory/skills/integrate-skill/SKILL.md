---
name: integrate-skill
description: Integrate an existing skill from another project into the AI Launchpad Marketplace following the composable skill architecture framework defined in the skill-factory:create-skill. Use whenever migrating or reproducing an existing skill into the AI Launchpad Marketplace.
---

# Integrate Skill

## Overview

This meta-skill formalizes the process of taking an existing skill from any source -- an external repository, a `temp/` holding directory, a standalone file, or another project -- and decomposing it into the composable skill architecture. Source skills are rarely structured for composability. They bundle strategy, writing, platform knowledge, and workflow logic into a single file. This skill breaks that monolith apart, maps each piece to the right plugin and category, and delegates actual skill generation to `skill-factory:create-skill`.

**Core Principle**: Integration is decomposition. A source skill that "does everything" becomes multiple focused pieces that compose well. Nothing from the source gets dropped; everything gets placed.

## When to Use

Use this skill when:
- Migrating a skill from an external project into the marketplace
- Importing a skill from the `temp/` holding directory
- Reproducing a skill from another Claude project or prompt collection
- Converting a monolithic workflow into composable skills
- Porting platform-specific automation into the architecture

Do NOT use this skill when:
- Creating a skill from scratch (use `skill-factory:create-skill` directly)
- The source is an idea or description, not an existing skill file

## Integration Workflow

Execute all steps below in order. Do not skip steps. Steps marked MANDATORY must be completed before proceeding.

### Step 1: Ingest the Source Skill

Read the source skill completely. Gather every file that constitutes the skill:

- **SKILL.md** (or equivalent main file): The primary skill definition
- **Reference files**: Any supporting documents, templates, or guidelines
- **Scripts or assets**: Any code, images, or other bundled resources
- **Configuration**: Any metadata, plugin manifests, or settings

Document the source location and file inventory:

```
Source: [path or repo URL]
Files found:
- [file 1]: [brief description]
- [file 2]: [brief description]
- ...
```

If the source skill has no clear boundary (e.g., it is embedded in a larger document), extract the relevant sections and note what was excluded and why.

### Step 2: Analyze and Decompose

**MANDATORY**: Read `skill-factory/skills/create-skill/references/taxonomy.md` before proceeding.

For each distinct piece of content in the source skill, classify it using the taxonomy decision tree:

1. Does it provide information that shapes other skills' output? --> **Knowledge** --> likely `branding-kit/` or a domain-specific knowledge plugin
2. Does it define how output sounds or feels? --> **Personality** --> likely `writing/`
3. Does it do one specific thing well? --> **Task** --> likely `writing/`, `content-strategy/`, `visual-design/`, `art/`, `research/`, or `personal-assistant/`
4. Does it sequence multiple task skills for a platform workflow? --> **Orchestrator** --> likely `youtube/`, `substack/`, or a new platform plugin
5. Does it create or maintain other skills? --> **Meta** --> `skill-factory/`

For each piece, determine:
- **Category**: Which of the five categories it belongs to
- **Plugin**: Which existing plugin it maps to (or whether a new plugin is needed)
- **File type**: SKILL.md (for new skills) or reference file (for supporting content)
- **Existing overlap**: Whether an existing skill or reference already covers this content

**Check for redundancy**: Search existing plugins for skills and references that already cover the same ground. If overlap exists, the source content should extend the existing file rather than create a duplicate.

**Flag potential loss**: If any source content does not map cleanly to a category or plugin, flag it explicitly. Do not silently drop content.

Apply the split rule: if a source section is trying to be two things, split it. Strategy content and writing templates are almost always separate pieces even when the source bundles them together.

### Step 3: Produce the Integration Design Doc

Create an integration design document at `docs/plans/YYYY-MM-DD-<topic>-integration-design.md` using today's date and a descriptive topic slug.

Use this template:

```markdown
# Integration Design: [source skill name] -> [target plugin:skill]

## Summary
One paragraph describing what is being integrated and how the content splits.

## Architecture
ASCII diagram showing the decomposed structure — the resulting orchestrator
or primary skill and its delegations to task skills and references.

## Content Split
For each resulting piece:
### [N]. [Type]: `[plugin/path/to/file]`
What content goes here, why it belongs in this plugin.

## Files to Create/Modify
| Action | File | Purpose |
|--------|------|---------|
| Create | ... | ... |
| Update | ... | ... |
| Delete | ... | ... |

## Functionality Preservation
| Original Capability | Destination | Notes |
|---------------------|-------------|-------|
| ... | ... | ... |

## Design Decisions
Numbered list of key decisions with rationale.

## Patterns Followed
Bullet list referencing framework patterns.
```

Fill in every section. The Content Split section must account for every piece of source content identified in Step 2. The Functionality Preservation table must confirm that every capability of the source skill has a destination in the new architecture.

### Step 4: Get User Approval

**MANDATORY**: Present the integration design doc to the user and wait for explicit approval before proceeding. This is a hard gate.

Present a summary of:
- How many files will be created, modified, and deleted
- Which plugins are affected
- Any new plugins that need to be created
- Any content flagged as potentially lost or ambiguous

Do NOT proceed to Step 5 until the user confirms the design. If the user requests changes, update the design doc and re-present.

### Step 5: Execute the Integration

With the approved design, create each piece:

**For each new skill identified in the design:**
1. Invoke `skill-factory:create-skill` with the classification, plugin placement, and content from the design doc
2. Let `skill-factory:create-skill` handle template selection, composition hooks, validation, and invocation of authoring best practices (`skill-creator:skill-creator`, `superpowers:writing-skills`)
3. Do NOT generate SKILL.md files directly -- always delegate to `skill-factory:create-skill`

**For each reference file identified in the design:**
1. Create the reference file in the correct plugin's `skills/[skill-name]/references/` directory
2. Follow the existing reference file patterns in that plugin
3. Keep reference files focused -- one topic per file, no fat reference files that dump everything into a single document

**For new plugins (if the design requires them):**
1. Create the plugin directory structure: `[plugin]/.claude-plugin/plugin.json`, `[plugin]/README.md`
2. Create the skill directories within the new plugin
3. Follow existing plugin patterns for `plugin.json` and `README.md`

**For all modified plugins:**
1. Bump the plugin version in `.claude-plugin/plugin.json` (increment the minor version)
2. Update the plugin's `README.md` to document new skills or references

### Step 6: Verify the Integration

Run verification against the approved design:

**Framework validation:**
- Invoke `skill-factory:create-skill` Step 8 validation for each generated skill
- Confirm every SKILL.md is under 500 lines
- Confirm flat directory structure (max 2 levels)
- Confirm frontmatter includes `name` and `description`

**Functionality preservation:**
- Walk the Functionality Preservation table row by row
- For each original capability, confirm the destination file exists and covers the capability
- Flag any gaps

**Composition validation:**
- Confirm generated task skills include voice and brand hooks where required
- Confirm orchestrator skills delegate via `plugin:skill` syntax and do not generate content
- Confirm reference files are loaded by the correct skills

**Legacy syntax check:**
- Search generated files for outdated invocation patterns (bare skill names without `plugin:` prefix, old slash-command syntax)
- Modernize any legacy patterns to use `plugin:skill` syntax

If any verification fails, fix the issue before proceeding.

### Step 7: Clean Up

Propose cleanup of the source files:

1. List all source files that were ingested in Step 1
2. Present the list to the user and confirm deletion
3. Delete confirmed source files (e.g., `temp/` directories, imported files)
4. Commit all changes with a descriptive message covering:
   - The integration (new skills and references created)
   - The cleanup (source files removed)

Do NOT delete source files without user confirmation. If the user wants to keep the source files, skip deletion and note it.

## Quality Checklist

Before finalizing the integration:

- [ ] Source skill fully ingested (SKILL.md + all references/scripts/assets)
- [ ] Every piece of source content classified using taxonomy decision tree
- [ ] Content split mapped to existing plugins or new plugins identified
- [ ] Integration design doc produced and user-approved
- [ ] Functionality preservation table confirms zero loss of function
- [ ] `skill-factory:create-skill` invoked for each resulting skill piece
- [ ] Reference files created in correct foundation plugin directories
- [ ] All generated skills pass `skill-factory:create-skill` Step 8 framework validation
- [ ] Plugin versions bumped for all modified plugins
- [ ] New plugins have complete structure (`plugin.json`, `README.md`) if created
- [ ] Source cleanup proposed and user-confirmed
- [ ] All changes committed

## Common Pitfalls

1. **Losing functionality during decomposition**: Splitting a source skill and quietly dropping pieces that do not fit neatly into a category. Every piece must appear in the Functionality Preservation table. If something does not map, flag it -- do not ignore it.

2. **Creating redundant skills**: Not checking existing plugins before creating new skills or references. Always search for overlap in Step 2. If `content-strategy:research` already exists, add a reference file to it rather than creating a new research skill.

3. **Fat reference files**: Dumping all source content into a single reference file. Reference files should be focused on one topic. Strategy content and writing templates are separate files even if the source bundled them together.

4. **Skipping create-skill**: Generating SKILL.md files directly instead of invoking `skill-factory:create-skill`. The create-skill workflow enforces template selection, composition hooks, and validation. Bypassing it produces skills that miss framework requirements.

5. **Legacy syntax in generated files**: Carrying over outdated invocation patterns from the source skill (bare skill names, slash commands, non-standard references). All generated content must use current `plugin:skill` syntax and follow current framework conventions.

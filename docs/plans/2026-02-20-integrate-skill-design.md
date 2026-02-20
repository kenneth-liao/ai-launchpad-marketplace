# Design: skill-factory:integrate-skill

## Summary

A new **Meta** skill in `skill-factory/` that formalizes the process of integrating skills from any source (external repos, standalone files, temp/, other projects) into the AI Launchpad Marketplace's composable skill architecture. It analyzes the source skill, decomposes its content across the right plugins, produces an integration design doc for user approval, then delegates actual skill generation to `skill-factory:create-skill`.

## Classification

- **Category**: Meta — creates/maintains other skills within the framework
- **Plugin**: `skill-factory/` — alongside `create-skill`
- **Directory**: `skill-factory/skills/integrate-skill/SKILL.md`
- **No reference files** — reads references from `create-skill` (taxonomy, composition-patterns, templates)

## Architecture

```
skill-factory:integrate-skill (META)
│
├─ Step 1: Ingest Source Skill
│   └─ Read SKILL.md + references/scripts from any source location
│
├─ Step 2: Analyze & Decompose
│   ├─ Read taxonomy.md → classify each piece of content
│   ├─ Map content to existing plugins (or identify new plugins needed)
│   ├─ Identify: what becomes a SKILL.md, what becomes a reference file,
│   │           what gets absorbed into existing skills
│   └─ Flag any functionality that could be lost in decomposition
│
├─ Step 3: Produce Integration Design Doc
│   ├─ Content split diagram
│   ├─ Files-to-create/modify table
│   ├─ Functionality preservation table
│   ├─ Design decisions with rationale
│   └─ Save to docs/plans/YYYY-MM-DD-<topic>-integration-design.md
│
├─ Step 4: User Approves Design
│   └─ Present design doc, get explicit approval before proceeding
│
├─ Step 5: Execute Integration
│   ├─ For each skill piece: invoke skill-factory:create-skill
│   ├─ For reference files: create directly
│   ├─ For plugin.json updates: bump versions
│   └─ For new plugins: create plugin structure first
│
├─ Step 6: Verify
│   ├─ Run create-skill's Step 8 validation against each generated piece
│   └─ Confirm no functionality lost vs. original
│
└─ Step 7: Cleanup
    ├─ List source files to remove
    ├─ User confirms before deletion
    └─ Commit all changes
```

## Key Design Decisions

1. **Meta skill, not orchestrator**: This skill operates on the framework itself, not on content production. It belongs in `skill-factory/` as a Meta skill.
2. **Delegates to create-skill**: Invokes `skill-factory:create-skill` for each SKILL.md piece to keep create-skill as the single source of truth for skill generation and validation.
3. **Reference files created directly**: `create-skill` generates SKILL.md files — reference files (e.g., `youtube-community-strategy.md`) are content files that don't need the full create-skill workflow.
4. **Design doc before execution**: Produces an integration design doc with content-split plan and functionality preservation table for user approval before touching any files.
5. **Cleanup requires confirmation**: Lists source files to remove, user confirms before deletion.
6. **Always decompose**: Every source skill gets decomposed to fit the composable architecture. New plugins are created if no existing plugin fits.
7. **Zero loss of function**: The functionality preservation table explicitly maps every capability from the source to its destination in the decomposed architecture.
8. **No voice/brand hooks on this skill**: Those are responsibilities of the skills it creates — `create-skill` ensures those hooks are present during generation.

## Frontmatter

```yaml
name: integrate-skill
description: Integrate an existing skill from another project into the AI Launchpad Marketplace following the composable skill architecture framework defined in the skill-factory:create-skill. Use whenever migrating or reproducing an existing skill into the AI Launchpad Marketplace.
```

## Integration Design Doc Template

The design doc produced in Step 3 follows this template:

```markdown
# Integration Design: [source skill name] → [target plugin:skill]

## Summary
One paragraph describing what's being integrated and how the content splits.

## Architecture
ASCII diagram showing the decomposed structure — what skill(s) get created,
what reference files feed into which existing skills.

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

## Quality Checklist

- [ ] Source skill fully ingested (SKILL.md + all references/scripts/assets)
- [ ] Every piece of source content classified using taxonomy decision tree
- [ ] Content split mapped to existing plugins or new plugins identified
- [ ] Integration design doc produced and user-approved
- [ ] Functionality preservation table confirms zero loss of function
- [ ] `skill-factory:create-skill` invoked for each resulting skill piece
- [ ] Reference files created in correct foundation plugin directories
- [ ] All generated skills pass create-skill's Step 8 framework validation
- [ ] Plugin versions bumped for all modified plugins
- [ ] New plugins have complete structure (plugin.json, README.md) if created
- [ ] Source cleanup proposed and user-confirmed
- [ ] All changes committed

## Common Pitfalls

1. **Losing functionality**: Decomposing content and dropping pieces that don't obviously fit. The functionality preservation table prevents this.
2. **Creating redundant skills**: Not checking if existing skills already cover part of the source's functionality. Always check existing skills first.
3. **Fat reference files**: Dumping the entire source into a single reference file instead of splitting strategically across plugins.
4. **Skipping create-skill**: Generating SKILL.md files directly instead of delegating to create-skill. Only reference files bypass create-skill.
5. **Legacy syntax**: Source skills may use outdated invocation patterns (e.g., `kenny-writing-voice` instead of `writing:voice`). Must modernize during integration.

## Files to Create/Modify

| Action | File | Purpose |
|--------|------|---------|
| Create | `skill-factory/skills/integrate-skill/SKILL.md` | The integrate-skill |
| Update | `skill-factory/.claude-plugin/plugin.json` | Bump version 1.0.0 → 1.1.0 |
| Update | `skill-factory/README.md` | Document new skill |

## Patterns Followed

- Meta skill pattern (matches create-skill)
- Design-doc-first pattern (matches brainstorming workflow)
- Delegation to create-skill (single source of truth for generation)
- Functionality preservation tracking (new pattern, specific to integration)
- Framework validation reuse (create-skill Step 8)
- Propose-confirm cleanup pattern

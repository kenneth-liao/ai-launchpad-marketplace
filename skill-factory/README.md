# skill-factory/

A meta-plugin for creating new skills that conform to the composable skill architecture framework. The skill-factory ensures every new skill follows the same patterns, composition rules, and quality standards as the existing system.

## Purpose

As the skill ecosystem grows, consistency becomes critical. The skill-factory codifies the architecture's rules into a repeatable creation workflow so that new skills:

- Are classified into the correct category (Knowledge, Personality, Task, Orchestrator, Meta)
- Follow the right template for their category
- Include the required composition hooks (voice, brand compliance)
- Are placed in the correct plugin
- Stay within structural limits (SKILL.md under 500 lines, flat structure)

## Skills

### create-skill (Meta Skill)

Guided workflow for creating new skills that conform to the framework. Walks through skill classification, template selection, content generation, and validation.

Workflow:
1. Understand what the skill needs to do
2. Classify the skill using the taxonomy decision tree
3. Determine which plugin it belongs in
4. Select the appropriate template for the skill category
5. Generate the skill following template + framework rules
6. Validate against architecture constraints
7. Place the skill in the correct plugin directory

## Directory Structure

```
skill-factory/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── create-skill/
        ├── SKILL.md
        └── references/
            ├── taxonomy.md
            ├── skill-template-task.md
            ├── skill-template-orchestrator.md
            ├── skill-template-knowledge.md
            ├── skill-template-personality.md
            └── composition-patterns.md
```

## References

- `skills/create-skill/references/taxonomy.md` -- Decision tree for classifying skills into categories
- `skills/create-skill/references/skill-template-*.md` -- Category-specific SKILL.md templates
- `skills/create-skill/references/composition-patterns.md` -- Composition hooks and invocation patterns

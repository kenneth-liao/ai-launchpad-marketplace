@AGENTS.md

- All documentation, research, and plans must be saved to the .docs/ folder, which is untracked and not committed to Git
- Do not create a new docs folder and save plans to it. Save all plans to .docs/plans/
- Any test created must be saved to .tests/
- The root folders in this marketplace should all be reserved for plugins. All other folders begin with a period are not to be committed or tracked.

## Plugin Development Standards

### Versioning
- All plugins use semantic versioning (MAJOR.MINOR.PATCH) in `.claude-plugin/plugin.json`
- MAJOR: Breaking changes (restructured hooks, renamed commands, changed context format)
- MINOR: New features (new skills, commands, hooks)
- PATCH: Bug fixes, docs, refactors
- Always bump the version when making changes to a plugin

### Changelogs
- Every plugin must have a `CHANGELOG.md` at its root
- Follow Keep a Changelog format: Added, Changed, Fixed, Removed
- Update the changelog in the same commit (or batch of commits) as the change

### Documentation
- When adding a new plugin, update BOTH the root README.md plugin table AND `.claude-plugin/marketplace.json`
- When making significant changes to a plugin (new skills, version bumps, structural changes), check if the root README.md or the plugin's own README.md need updating
- Documentation updates should be included in the same commit or batch of commits as the change

### Commit Messages
- Use conventional commits scoped to the plugin: `type(plugin-name): description`
- Types: feat, fix, refactor, docs, test, chore
- Examples: `feat(personal-assistant): add sync-context skill`, `fix(scheduler): handle missing cron entry`
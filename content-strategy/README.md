# Content Strategy Plugin

A foundation plugin for content research, title generation, and hook creation across all platforms and content types. Provides three generalized task skills that can be used standalone or orchestrated by platform-specific skills.

## Skills

### research
Conducts topic and competitor research for any content type. Analyzes existing content landscape, identifies gaps, and produces actionable insights with rated opportunities.

### title
Generates optimized titles and headlines for any content type. Maximizes engagement through curiosity, complementarity with visual assets, and audience targeting. Supports YouTube titles, newsletter subject lines, and social headlines.

### hook
Creates retention-optimized opening hooks for any content type. Extends curiosity from the title/headline, prevents common opening mistakes, and maximizes early engagement.

## Integration

These skills are designed to be invoked by orchestrator skills in platform-specific plugins (e.g., `youtube`, `newsletter`). They also integrate with:
- **writing:voice** — Applied before finalizing any written output
- **branding-kit:brand-guidelines** — Applied when creating assets for The AI Launchpad

## Directory Structure

```
content-strategy/
  .claude-plugin/plugin.json
  README.md
  skills/
    research/
      SKILL.md
      references/research-frameworks.md
    title/
      SKILL.md
      references/youtube-title-formulas.md
      references/newsletter-subject-lines.md
      references/social-headlines.md
    hook/
      SKILL.md
      references/youtube-hooks.md
      references/newsletter-hooks.md
      references/social-hooks.md
```

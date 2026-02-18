# Design: Adopt newsletter-to-youtube as youtube:newsletter-to-video

**Date:** 2026-02-18
**Status:** Approved
**Classification:** Task skill in `youtube` plugin

## Summary

Migrate `temp/newsletter-to-youtube/SKILL.md` into the composable plugin architecture as `youtube:newsletter-to-video`. The skill transforms a newsletter issue into a topic-level YouTube video outline. Core transformation logic stays intact; deprecated references are updated and composition hooks added.

## File Location

```
plugins/youtube/skills/newsletter-to-video/SKILL.md
```

## Changes from Source

| Area | Current (temp/) | Target (plugin) |
|---|---|---|
| Frontmatter name | `newsletter-to-youtube` | `newsletter-to-video` |
| Hook skill reference | `yt-content-strategist:youtube-video-hook` | `content-strategy:hook` |
| Voice hook | Missing | Omitted (structural output, not prose) |
| Brand compliance hook | Missing | Added (for hook output section) |
| Quality checklist | Missing | Added |
| Common Mistakes table | References deprecated skill | Updated to `content-strategy:hook` |

## What Stays the Same

- The 4-step process (Read → Adapt → Hook → Outline)
- "Drop these / Promote these / Reorder for retention" transformation rules
- Retention reordering patterns table
- Outline template structure
- Output format guidance
- Common mistakes table (with updated skill references)

## Decisions

- **Plugin home:** youtube (produces a YouTube artifact)
- **Skill type:** Task skill (core value is the transformation logic, not orchestration)
- **Title generation:** Not included (outline is title-agnostic)
- **Voice hook:** Omitted (output is structural, not prose)
- **Approach:** Minimal adaptation — preserve transformation logic, update references and add compliance

## Adapted SKILL.md Sections

1. Frontmatter (name, description updated)
2. Overview (why this exists — medium differences)
3. When to Use (trigger phrases)
4. Process flow diagram (updated skill reference in dot graph)
5. Step 1: Read the Newsletter (unchanged)
6. Step 2: Adapt for Video (unchanged — drop/promote/reorder rules)
7. Step 3: Generate the Hook (updated to invoke `content-strategy:hook`)
8. Step 4: Build the Outline (updated template references)
9. Output Format (unchanged)
10. Brand Compliance (new — hook output goes through brand check)
11. Quality Checklist (new)
12. Common Mistakes (updated skill references)

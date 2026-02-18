# Guide / Cheatsheet Structure

Platform-specific structure and conventions for writing guides, cheatsheets, and educational long-form content. Voice rules are handled separately by the `writing:voice` skill — this file covers structure only.

---

## Guide Structure

### 1. Problem Statement

Open with what this guide solves and who it's for. Be specific — not "learn about AI tools" but "set up Claude Code agent teams for a multi-repo project."

**Include:**
- The specific problem or task
- Who this is for (skill level, use case)
- What the reader will be able to do after reading
- Prerequisites (tools, accounts, knowledge needed)

### 2. Solution Framework

High-level overview of the approach before diving into steps. Give the reader a mental model of what they're about to do.

- Brief explanation of the approach (2-3 sentences)
- Why this approach over alternatives (if relevant)
- Overview diagram or flow if it helps (optional)

### 3. Step-by-Step Instructions

Numbered steps with clear actions. Each step includes:

1. **Action:** What to do (clear, imperative)
2. **Example:** Code snippet, screenshot, or concrete illustration
3. **Explanation:** Why this step matters (brief, 1-2 sentences)
4. **Expected result:** What the reader should see after completing the step

**Step formatting:**
- Keep each step focused on one action
- Include code blocks for any commands or configurations
- Add screenshots for UI-based steps
- Note common errors or gotchas inline

### 4. Summary Takeaway

End with:
- Key points (3-5 bullets)
- Next steps or further reading
- Related resources (other guides, videos, tools)

Forward-looking — what the reader can do now that they have this knowledge.

---

## Cheatsheet Structure

Cheatsheets are condensed reference versions of guides. Structure:

- **Title:** What this is a cheatsheet for
- **Quick reference table:** Key commands, settings, or patterns
- **Sections:** Grouped by category, each with 2-3 examples
- **Tips:** Common gotchas or pro tips at the end

Keep cheatsheets under 1,500 words. They're for reference, not learning from scratch.

---

## Length Guidelines

| Guide Type | Word Count | Steps |
|---|---|---|
| Full setup guide | 2,000-5,000 words | 5-15 steps |
| Quick how-to | 500-1,500 words | 3-7 steps |
| Cheatsheet | 500-1,500 words | N/A (reference format) |
| Comparison guide | 1,500-3,000 words | N/A (section-based) |

---

## Formatting Conventions

- **Headers:** H2 for major sections, H3 for steps or subsections
- **Code blocks:** Essential — show every command, config, and file path
- **Screenshots:** Include for any visual/UI step, always with context
- **Numbered lists:** For sequential steps
- **Bulleted lists:** For non-sequential items, features, or options
- **Bold:** Key terms, important warnings, file names
- **Callout blocks:** For warnings, tips, and important notes

---

## Evidence Standards

Every guide should be grounded in real experience:
- "I set this up and here's what happened"
- Include actual outputs, not hypothetical ones
- Show real file structures and configurations
- Note any issues encountered and how to resolve them
- Include version numbers and dates where relevant

---

## Common Mistakes

- Starting with theory instead of stating what the guide solves
- Steps that combine multiple actions into one
- Missing code examples for technical steps
- No expected results after steps (reader doesn't know if it worked)
- Assuming knowledge without listing prerequisites
- Ending without next steps or further resources
- Screenshots without context explaining what to look at

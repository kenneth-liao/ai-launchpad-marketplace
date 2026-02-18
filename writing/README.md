# writing/

A Claude Code plugin for writing content in Kenny Liao's authentic voice across all content types and platforms.

## Skills

### voice (Personality Skill)

Defines and applies Kenny's authentic writing voice. This is a **personality skill** — it doesn't produce content on its own. Instead, task skills invoke it to transform their output into Kenny's voice.

Key characteristics it enforces:
- Parenthetical asides as a signature pattern
- Short punches alternating with longer explanations
- Deliberate sentence fragments
- Personal experience as default evidence
- Counterpoint acknowledgment with specific transition phrases
- Raw, thinking-out-loud quality over polished prose

### copywriting (Task Skill)

Generalized writing skill that produces written content for any platform and format. Handles newsletters, YouTube scripts, guides, sales copy, Twitter/X posts, LinkedIn posts, and Substack Notes.

Workflow:
1. Determines content type from user request
2. Loads platform-specific reference (e.g., `newsletter.md`, `youtube-script.md`)
3. Drafts content following platform structure
4. Invokes `writing:voice` to apply Kenny's voice
5. Invokes `branding-kit:brand-guidelines` for brand compliance
6. Presents to user for feedback

## Skill Composition

These two skills are designed to work together. The **copywriting** skill handles *what* to write and *how to structure it* for each platform. The **voice** skill handles *how it should sound*. This separation means:

- Voice rules stay consistent regardless of content type
- Platform structure rules stay clean without voice concerns mixed in
- Other plugins can invoke `writing:voice` independently for their own text output

## References

- `skills/voice/references/voice-profile.md` — Full voice analysis with extended examples
- `skills/copywriting/references/` — Platform-specific structure guides (newsletter, YouTube script, guide, sales page, Twitter, LinkedIn, Substack Notes)

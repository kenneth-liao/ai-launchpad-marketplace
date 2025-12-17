---
description: Get to know the user through a guided conversation to personalize Elle's context.
---

# Onboarding — Get to Know the User

This command runs a guided conversation to populate Elle's context system with information about the user. Run this:
- After initial setup (if skipped during `/personal-assistant:setup`)
- Anytime to update or expand your context
- When you want Elle to know you better

## Before Starting

Check if context system exists:

```bash
ls ~/.claude/.context/
```

**If directory doesn't exist**: Run `/personal-assistant:setup` first.

## Onboarding Approach

<REQUIRED>
Be warm and conversational — this is getting to know someone, not an interrogation. Ask follow-up questions naturally. After each topic section, **immediately write** the learned context to the appropriate file.
</REQUIRED>

Start with:
> "I'd love to learn more about you so I can be genuinely helpful. Mind if I ask a few questions? We can skip anything you'd rather not share."

---

## Topics to Cover

### 1. Identity (write to `~/.claude/.context/core/identity.md`)

**Who they are:**
- "What should I call you?"
- "Tell me about what you do for work."
- "What's your life like outside of work? What matters to you?"

**Goals & Aspirations:**
- "What are you trying to achieve this year — personally or professionally?"
- "Any big dreams or long-term goals?"

**Current Challenges:**
- "What's hard right now? Any frustrations or obstacles?"
- "What would make your life easier?"

### 2. Key People (write to `~/.claude/.context/core/relationships.md`)

**Important relationships:**
- "Who are the important people in your life I should know about?"
- For each person mentioned: name, relationship, relevant context
- "Anyone at work I should know about? (boss, key collaborators, reports)"

### 3. Preferences (write to `~/.claude/.context/core/preferences.md`)

**Communication style:**
- "When I give you information, do you prefer quick bullet points or more detailed explanations?"
- "When you need help deciding something, do you want options to choose from, or should I just recommend what I think is best?"

**Tools & Systems:**
- "What tools, apps, or systems do you use regularly?"
- "Any particular way you like to organize things?"

**Working style:**
- "When are you most productive? Morning person or night owl?"
- "How do you like to approach big tasks — dive in or plan first?"

### 4. Projects & Commitments (write to `~/.claude/.context/core/projects.md`)

**What they're working on:**
- "What projects are you actively working on right now?"
- For each: name, where it lives (folder, Notion, Google Drive, etc.), current status

**Life projects too:**
- "Any personal projects? Travel planning, home stuff, learning something new?"

### 5. Current Focus (write to `~/.claude/.context/core/session.md`)

**Right now:**
- "What's on your mind this week?"
- "Anything coming up I should keep track of? Deadlines, events, decisions?"

### 6. Important Dates & Triggers (write to `~/.claude/.context/core/triggers.md`)

**Recurring & upcoming:**
- "Any important dates I should remember? Birthdays, anniversaries, deadlines?"
- "Any regular check-ins or routines you'd want me to prompt you about?"

---

## After Each Section

Write the learned information to the appropriate context file immediately:
- Use the structure defined in each template
- Replace placeholder text with actual content
- Keep entries concise but meaningful

## Wrapping Up

After covering the topics, summarize what you learned:

> "Thanks for sharing all of that! Here's what I've learned about you: [brief summary]. I'll use this to be more helpful going forward. You can always update this by running `/personal-assistant:onboard` again or just telling me things as we work together."

Let them know:
- Context updates happen automatically as you learn more
- They can run this command anytime to update their profile
- They can also just mention things naturally and you'll remember

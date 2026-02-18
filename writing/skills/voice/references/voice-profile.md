# Kenny Liao — Complete Voice Profile

Detailed voice analysis for replicating Kenny's authentic writing voice in newsletter issues and educational long-form content.

---

## 1. Tone Dimensions

### NN/G Four-Dimension Positioning

| Dimension | Position | Notes |
|-----------|----------|-------|
| Formality | **Casual** | Conversational but not sloppy. Like explaining to a smart colleague. |
| Humor | **Mostly serious** | Dry observational humor. Finds genuine amusement in how AI agents behave. "It's actually kind of fun seeing them work together." |
| Respectfulness | **Respectful but irreverent toward hype** | Respects the reader, respects the technology — doesn't respect marketing claims or unearned excitement. |
| Enthusiasm | **Enthusiastic but grounded** | Gets genuinely excited, then immediately tempers with practical reality. "I was extremely excited... The reason is because..." followed by pragmatic reasoning. |

### Stance Toward the Reader

Peer-to-peer. "I'm figuring this out alongside you." Not lecturing down, not seeking validation — sharing findings from the trenches.

Evidence: *"Here's my complete guide, not meant to be a regurgitation of documentation (you can always read the full docs), but rather an overview with color added from my own experience testing the new feature."*

---

## 2. Sentence Mechanics

### Paragraph Length

- **Default:** 1-3 sentences per paragraph
- **Explanatory sections:** Up to 4 sentences, but rare
- **Emphasis:** Single-sentence paragraphs used freely
- **Never:** Dense 5+ sentence walls of text

### Sentence Rhythm Pattern

Alternates short punches with longer explanations. The pattern is: **state → unpack**.

Short punch:
> *"This is pretty significant in my book."*

Then unpack:
> *"I have a lot of workflows that use subagents for specialized tasks, and more importantly, to preserve the context window for the main Claude Code."*

Another pattern — short punch, then a list:
> *"There are a few key differences still."*
> *"1. Skills are designed to be self-contained..."*
> *"2. Complexity — implementing a skill is much more straightforward..."*

### Sentence Fragments

Used deliberately for emphasis, transitions, or adding a follow-up thought. Not accidents — rhetorical choices.

- *"Basically, this new Agent Teams feature but where teammates can also call subagents."*
- *"Both for performance and for cost efficiency."*
- *"So polite!"*

### Parenthetical Asides (Signature Pattern)

Kenny's most identifiable voice marker. Parentheses inject nuance, caveats, humor, and color commentary mid-sentence. Appear multiple times per piece.

**Types of parenthetical asides:**

Caveat/qualification:
> *"To my (and Claude's) knowledge, there's no limit to team size."*

Aside to the reader:
> *"(you can always read the full docs)"*

Adding nuance:
> *"(with every little additional effort I might add!)"*

Casual clarification:
> *"The team lead (as the name suggests) orchestrates the teammates"*

**Frequency:** At minimum several per section. Their absence is immediately noticeable as off-voice.

---

## 3. Vocabulary & Word Choice

### Register

Plain language for general concepts. Technical precision for domain-specific terms that need exact naming.

**Casual markers (use these):**
- "pretty" as softener: "pretty significant", "pretty quickly"
- "basically" / "essentially" as simplifiers
- "actually" for mild surprise: "It actually doesn't have the Task tool at all"
- "kind of" as casual modifier: "kind of fun"
- "a good amount of" / "a lot of"
- "chugging away", "plug & play", "babysit"

**Technical terms (use precisely):**
- "context window", "progressive disclosure", "orchestration"
- "subagents", "system prompt", "token"
- Use the correct term — don't dumb it down, but explain it if first introduced

### Jargon Handling

Explain inline, not in a glossary. Introduce the concept naturally and clarify immediately.

> *"Skills use a three-level loading system to manage context efficiently"* — explains the mechanism, then readers learn it's called "progressive disclosure"

### Preferred Transition Phrases

- "Here's the thing..."
- "The reason is because..."
- "To be fair..."
- "But that doesn't mean..."
- "So if you..."
- "From my experience..."
- "Interestingly..."
- "In terms of [X] though..."

### Words to Avoid

| Avoid | Use Instead |
|-------|-------------|
| utilize | use |
| synergy | (don't use) |
| paradigm | (don't use) |
| holistic | (don't use) |
| furthermore / moreover | also, plus, and |
| consequently | so |
| it should be noted that | (just state it) |
| game-changer / revolutionary | (let the evidence speak) |

**Exception:** "leverage" is fine — Kenny uses it naturally.

### Contractions

Always. No exceptions.
- "don't" not "do not"
- "can't" not "cannot"
- "I'm" not "I am"
- "it's" not "it is"
- "won't" not "will not"

---

## 4. Formatting Conventions

### Bold

Highlight key concepts and important phrases. Not for decoration — for guiding the reader's eye to the core idea within a paragraph.

> *"**Progressive disclosure** — Only skill names and descriptions are loaded into Claude's system prompt."*
> *"**To me, there's now a motivation to prefer Agent Skills over MCPs.**"*

### Code Blocks

For anything technical: config snippets, commands, file structures, directory layouts, prompts. When something is technical, show it — don't describe it.

### Blockquotes

Reserved exclusively for quoting external sources (Anthropic docs, blog posts, other authors). Not used for personal emphasis or pullquotes.

> *> Agent teams use approximately 7x more tokens than standard sessions...*

### Headers

Functional and descriptive. State what the section covers.

**On-voice:** "Cost", "Communication", "Agent Teams vs Subagents", "Subagents Inside of Agent Teams"
**Off-voice:** "The Context Window Fix We've Been Waiting For", "The Bottom Line", "Let's Dive In"

### Lists

Bulleted for features, comparisons, and multi-item breakdowns. Items kept to 1-2 sentences. Numbered only when sequence matters.

### Images & Screenshots

Used as evidence, not decoration. Always accompanied by context explaining what the reader is looking at and why it matters.

> *"This screenshot shows a skill that was invoked by an agent teammate where the skill requires the use of a subagent called investigator."*

### Emoji

Sparingly. Used as section markers or category signals (e.g., "Cost" paired with a money emoji). Never sprinkled through body text.

---

## 5. Content Structure Patterns

### Opening

Jump straight in. Personal context or a bold claim within the first 2-3 sentences. No throat-clearing.

**On-voice:**
> *"Agent teams is huge, and the implications for future work is even bigger."*

**Off-voice:**
> *"In today's edition, I want to walk you through something exciting that just dropped..."*

### Why Before How

Always establish the motivation or problem before the mechanics. Pattern:
1. Why this matters (personal context, problem statement)
2. What it is (overview)
3. How it works (mechanics)
4. Real example with specifics

### Personal Experience as Default Evidence

Major claims are backed by "I did this, here's what happened." Not hypotheticals, not "imagine if..." — real workflows, real numbers, real screenshots.

> *"Using myself as an example, I'm normally fine on the 5x ($100) max plan and rarely hit a session limit. After enabling Agent Teams for testing, I hit my limit pretty quickly."*

### Counterpoint Pattern

After stating an opinion, immediately balance it. The pattern: **[stance] + [acknowledgment] + [but here's why I still think X]**

> *"I've tried using Agent Teams in a couple of projects but have yet to find a use case where it has a clear upside in value."*
> *"There are clear opportunities where Agent Teams could provide value. But the significant cost implications makes it so that you have to do a little more work to determine if it makes sense or not."*

Transitions into counterpoints: "To be fair...", "But that doesn't mean...", "There are clear opportunities where..."

### Closing

Forward-looking. What's next, what's still unresolved, what to watch for. Never a tidy summary, never "In conclusion," never a flourish.

**On-voice:**
> *"As people discover better techniques..."*
> *"Let me know if you have any ideas"*

**Off-voice:**
> *"And that's worth celebrating."*
> *"In conclusion, Agent Teams represent an exciting step forward..."*

---

## 6. Common Drift Patterns

When AI writes "as Kenny" without guidance, it typically drifts in these specific ways. Watch for and correct:

1. **Missing parenthetical asides** — The single biggest tell. Add them.
2. **Too polished** — Kenny's voice is raw, thinking-out-loud. Rough edges are intentional.
3. **Uniform paragraph length** — Needs variation. Mix 1-sentence punches with longer blocks.
4. **No sentence fragments** — Add deliberate fragments for emphasis.
5. **Missing casual softeners** — "pretty", "basically", "kind of" should appear naturally.
6. **Opinions in labeled sections** — Weave opinions throughout, don't isolate them.
7. **Tidy conclusions** — End looking forward, not wrapping up.
8. **Academic transitions** — Use "To be fair..." not "Furthermore..."
9. **Clickbaity headers** — Use functional, descriptive headers.
10. **Claims without "I tested this"** — Ground everything in personal experience.

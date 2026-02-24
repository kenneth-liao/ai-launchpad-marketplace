# Substack Notes Ideation

Strategic frameworks for extracting Substack Note ideas from published content sources. Used by `content-strategy:research` when invoked by `substack:generate-note-ideas`. The companion strategy reference (`substack-notes-strategy.md`) covers timing, cadence, and publishing cycles — this file covers **how to mine existing content for note-worthy angles**.

---

## Angle Extraction Framework

When reading a YouTube transcript, newsletter issue, or other content source, scan for these eight categories of note-worthy material. Each category reliably produces standalone Notes that deliver value without requiring the audience to consume the original source.

### 1. Surprising Data Points or Counterintuitive Findings

Look for moments where the data contradicts common assumptions. These are high-restack material because they create cognitive dissonance — readers share content that challenges what they believed.

**What to look for:**
- Statistics that contradict popular advice
- Results that surprised even the creator
- A/B test outcomes where the "wrong" option won
- Benchmarks that are dramatically higher or lower than expected

**Extraction signal:** The creator says something like "what surprised me was..." or "I expected X but got Y" or "most people assume... but the data shows..."

### 2. Quotable One-Liners Buried in Longer Content

Creators often drop powerful one-sentence observations in the middle of a 20-minute video or 2,000-word newsletter without realizing they've written a standalone note. Extract these.

**What to look for:**
- Aphorisms that crystallize a complex idea into one sentence
- Reframings that make a familiar problem feel new
- Declarative statements with inherent tension or surprise
- Sentences that would work as a screenshot or restack

**Extraction signal:** A sentence that would make you pause, highlight, or screenshot if you encountered it in the wild.

### 3. Behind-the-Scenes Process Details

Audiences are consistently fascinated by how things actually work — the messy, real process behind polished output. These details are often mentioned casually but make excellent Build-in-Public or Pattern Observation notes.

**What to look for:**
- Tools, workflows, or systems the creator uses
- Time investment ("this took me 3 weeks to build")
- Failed attempts before the working version
- Decision rationale ("I chose X over Y because...")
- Specific costs, timelines, or resource allocations

**Extraction signal:** The creator describes their actual process rather than a prescriptive ideal.

### 4. Unanswered Questions and Audience Curiosities

Comments sections and reply threads reveal what the audience actually wants to know — which is often different from what the creator covered. These gaps are direct fuel for Direct Advice and Problem -> Solution notes.

**What to look for:**
- Frequently repeated questions in comments
- Misunderstandings that keep surfacing (correction opportunity)
- "What about [edge case]?" questions
- Requests for follow-up on a specific sub-topic
- Debates between commenters where both sides have a point

**Extraction signal:** Multiple people asking the same question, or a question that reveals a genuine knowledge gap.

### 5. Mini-Lessons That Stand Alone

Many long-form pieces contain 2-5 sentence segments that teach a complete concept. These segments can be extracted verbatim (with light editing) as standalone notes — particularly List-Based Tactical or Direct Advice types.

**What to look for:**
- "Here's how to..." segments within a broader tutorial
- Step-by-step instructions for a sub-task
- Clear cause-and-effect explanations
- Framework introductions that don't require the full context
- "The key insight is..." moments

**Extraction signal:** A passage that teaches a complete, actionable idea without needing the content around it for context.

### 6. Contrarian Takes Embedded in Nuanced Discussions

Creators who discuss topics with nuance often embed bold, contrarian positions inside longer arguments. These positions — extracted and sharpened — make excellent Contrarian Statement notes.

**What to look for:**
- "Actually, [common belief] is wrong because..."
- Positions that go against industry consensus
- Arguments where the creator takes a minority stance with evidence
- Critiques of popular tools, methods, or advice
- "Unpopular opinion" moments, even if unlabeled

**Extraction signal:** A position that would generate strong agree/disagree reactions if posted standalone.

### 7. Specific Numbers, Results, or Metrics

Concrete numbers are inherently shareable because they're falsifiable, memorable, and give readers something to compare against their own experience. Extract any specific metric that tells a story.

**What to look for:**
- Revenue figures, growth rates, conversion percentages
- Time savings ("went from 20 hours to 6 hours")
- Before/after comparisons with measurable outcomes
- Audience or subscriber milestones with context
- Cost breakdowns or ROI calculations

**Extraction signal:** Any specific number paired with context that makes it meaningful. "10,000 subscribers" is boring. "10,000 subscribers in 6 months with zero paid ads" is a note.

### 8. Process Steps Extractable as Standalone Tips

Tutorials and how-to content contain individual steps that are valuable on their own — even without the full workflow. A single step, explained well, can be a complete Direct Advice or Problem -> Solution note.

**What to look for:**
- Individual steps in a multi-step process that deliver value independently
- "Pro tips" or "bonus tips" mentioned in passing
- Workarounds for common friction points
- Settings, configurations, or parameters that most people miss
- Shortcuts that save meaningful time or effort

**Extraction signal:** A step or tip that would make someone say "I didn't know you could do that" or "that's going to save me hours."

---

## Source-to-Type Mapping

Different content sources naturally produce different note types. Use this mapping to focus extraction on the types most likely to emerge from each source.

| Content Source | Primary Note Types | Secondary Note Types |
|---|---|---|
| **YouTube transcript** | Pattern Observation, Contrarian Statement, Problem -> Solution, Single-Punch Wisdom | Build-in-Public Update, List-Based Tactical |
| **YouTube comments** | Direct Advice (answering common questions), Contrarian Statement (correcting misconceptions) | Problem -> Solution (addressing audience pain points) |
| **Newsletter issue** | Newsletter Teaser, Single-Punch Wisdom, List-Based Tactical | Pattern Observation, Problem -> Solution |
| **Past notes history** | Gap analysis — identify which of the 10 types haven't been used recently and prioritize those | All types (filling gaps) |
| **Web trends** | Pattern Observation, Direct Advice (tied to timely topics), Build-in-Public Update (tied to current tools/platforms) | Contrarian Statement (challenging trend narratives) |

### How to Use This Table

1. Start with the content source you're analyzing.
2. Focus extraction on the primary note types first — these are the most natural fit.
3. Check secondary types only if the primary types don't yield enough strong ideas.
4. For past notes history, run a gap analysis before extracting from other sources so you know which types to bias toward.

### Gap Analysis Process

When reviewing past notes history:

1. Tally how many times each of the 10 note types has been used in the last 2-4 weeks.
2. Identify the 2-3 types with the fewest recent uses.
3. When extracting ideas from other sources, actively look for angles that map to the underused types.
4. Flag the gap in the idea's rationale so the user knows the idea partially serves variety.

---

## Idea Quality Criteria

Every generated idea must pass this checklist before inclusion. If an idea fails any criterion, either rework it or discard it.

| # | Criterion | Test |
|---|---|---|
| 1 | **Standalone value** | Is this idea interesting to someone who hasn't watched the source video or read the source issue? If the idea only makes sense with the full context, it fails. |
| 2 | **Specificity** | Does it include concrete numbers, examples, tools, or scenarios? If you could swap the topic for any other topic and the idea still works, it's too vague. |
| 3 | **One idea per note** | Does the idea contain exactly one core message? If you need "and" to describe it, split it into two ideas. |
| 4 | **Maps to a note type** | Does it cleanly map to one of the 10 note types from `writing:copywriting` > `substack-notes.md`? If it doesn't fit any type, it's probably too abstract or too complex for a note. |
| 5 | **Not a rehash** | Has something substantially similar already been posted in past notes? Check the past notes history. Similar topic is fine; same angle is not. |
| 6 | **Clear engagement angle** | Would someone restack this, quote it, or reply to it? Every idea needs a reason for the reader to interact — a surprising claim, a useful tip, a question worth answering, or a take worth debating. |

### Applying the Checklist

Run each idea through all six criteria in order. If an idea fails criterion 1 (standalone value), there's no point checking the rest — it needs rework or removal. The criteria are ordered by importance: standalone value and specificity are non-negotiable; engagement angle is the final polish check.

---

## Trending Topic Integration

Trending topics add timeliness to notes, but only when blended with the user's genuine expertise and published content. A trending note without a unique angle is noise.

### Step 1: Find Relevant Trends

Search for trending topics in the user's niche via web search. Focus on:
- New tools, platforms, or features getting attention
- Industry news or announcements generating discussion
- Viral posts or debates within the niche community
- Seasonal patterns or cyclical topics (end-of-year reviews, new-year planning, etc.)

### Step 2: Cross-Reference with Published Content

For each trending topic, check whether the user has existing content (videos, newsletters, past notes) that provides a unique angle:
- Have they already tested the tool everyone is talking about?
- Do they have data or experience that contradicts the trending narrative?
- Have they covered the underlying principle behind the trend in a past piece?
- Can they offer a first-hand case study while others are speculating?

### Step 3: Prioritize First-Hand Experience

Rank trend-based ideas by the user's proximity to the topic:

| Priority | User's Relationship to Trend | Example |
|---|---|---|
| **Highest** | Has direct experience and published content | User tested the tool 3 months ago and has results data |
| **High** | Has direct experience but hasn't published on it yet | User uses the tool daily but hasn't written about it |
| **Medium** | Has adjacent expertise that applies | User's framework for evaluating tools applies to this new one |
| **Low** | No direct experience — opinion only | User has a take but no first-hand evidence |

Only generate ideas at the "highest" and "high" priority levels. "Medium" is acceptable if the connection is genuinely strong. Avoid "low" entirely — the note should add insight, not just ride a trend.

### Step 4: Avoid Bandwagon Takes

Before including a trend-based idea, ask:
- Does this note say something the reader can't already find in 10 other Notes about this trend?
- Does the user have a genuinely different perspective, or are they just agreeing with the consensus?
- Would this note still be interesting in two weeks, or is it purely reactive?

If the answer to all three is unfavorable, skip the trend. Silence is better than a "me too" note.

---

## Output Format

Return each idea in this structure. The format is designed so the user (or a downstream writing skill) can quickly evaluate, select, and draft from the ideas.

```
### Idea N
**Topic:** [Specific topic in 5-10 words]
**Type:** [One of the 10 note types]
**Source:** [YouTube — "Title" (video ID) | Newsletter — "Title" (URL) | Web trend — description]
**Pitch:** [One sentence describing the note's core message]
**Rationale:** [Why this idea is worth posting — engagement potential, gap it fills, timeliness]
```

### Field Guidelines

- **Topic:** Be specific. "AI tools for content creators" is too broad. "Why Cursor IDE replaced my entire writing workflow" is specific enough.
- **Type:** Must be one of the 10 types: Single-Punch Wisdom, Income Proof Story, Pattern Observation, Contrarian Statement, Problem -> Solution, Build-in-Public Update, List-Based Tactical, Vulnerable Personal Story, Newsletter Teaser, Direct Advice.
- **Source:** Identify the specific source material. For YouTube, include the video title and ID. For newsletters, include the title and URL. For web trends, describe the trend concisely.
- **Pitch:** One sentence that captures the note's core message. This is the "if you only read one line" summary. It should make the user immediately see the note in their head.
- **Rationale:** Explain why this idea deserves to be posted. Reference engagement potential (restackable, quotable, debate-worthy), type gap it fills (if a type has been underused), or timeliness (trend relevance). This is the strategic justification, not a restatement of the pitch.

### Example Output

```
### Idea 1
**Topic:** The 80/20 of YouTube SEO nobody talks about
**Type:** Contrarian Statement
**Source:** YouTube — "My YouTube SEO Strategy for 2026" (dQw4w9WgXcQ)
**Pitch:** Most YouTube SEO advice obsesses over tags and descriptions, but 80% of discoverability comes from the title and thumbnail alone — everything else is noise.
**Rationale:** High restack potential — challenges the SEO-heavy advice most creators follow. Contrarian Statement hasn't been used in the last 10 notes. Source video has a 2-minute segment at [14:30] where the creator shares click-through rate data backing this up.

### Idea 2
**Topic:** 3 newsletter subject lines that doubled open rates
**Type:** List-Based Tactical
**Source:** Newsletter — "What I Learned From 50 A/B Tests" (https://example.com/issue-42)
**Pitch:** After 50 subject line A/B tests, three patterns consistently won: specific numbers, counterintuitive claims, and direct "how to" framing.
**Rationale:** High save-and-share potential — actionable and specific. List-Based Tactical hasn't appeared in 2 weeks. The source issue has concrete A/B test data that makes these patterns credible, not just opinion.

### Idea 3
**Topic:** Why the Substack algorithm rewards replies over restacks
**Type:** Pattern Observation
**Source:** Web trend — multiple creators discussing Substack's February 2026 algorithm update
**Pitch:** Since the latest algorithm update, Notes with high reply counts are outperforming Notes with high restack counts in the feed — replies signal depth of engagement, and Substack is weighting that more heavily.
**Rationale:** Timely — this is being discussed in the Substack creator community right now. The user has 6 months of Notes data to share first-hand observations about reply vs. restack performance. Pattern Observation is a strong fit for algorithm analysis content.
```

---

## Volume Target

Generate **5-10 ideas per run**. Bias toward quality over quantity.

- **5 ideas** is the minimum for a useful batch — fewer than that suggests the source material was thin or the extraction wasn't thorough enough.
- **10 ideas** is the maximum — beyond that, quality starts to dilute and the user faces decision fatigue.
- **7-8 ideas** is the ideal sweet spot for most runs.

If a source doesn't have strong note-worthy angles, skip it rather than forcing weak ideas. Not every video or newsletter issue is a goldmine — some content is too niche, too similar to recent notes, or too thin on extractable material. Report that honestly rather than padding the list.

### Distribution Across Sources

When multiple sources are provided in a single run, aim for ideas from each source but don't force equal distribution. A strong video transcript might yield 5 ideas while a thin newsletter issue yields 1. That's fine. Quality per idea matters more than balanced sourcing.

### Distribution Across Types

Aim for at least 3 different note types across the batch. A batch of 8 ideas that are all Pattern Observations suggests tunnel vision during extraction. Use the gap analysis from past notes history to guide type variety.

# Scheduler Plugin — Use Cases & Automation Ideas

> Brainstormed 2026-02-26. Reference doc for personal workflow automations AND audience showcase opportunities.

---

## 1. Content Research & Ideation

Fill your idea bank on autopilot so you never start from zero.

| Automation | Schedule | What It Does | Type |
|---|---|---|---|
| **Daily AI News Brief** | Daily 7am | Researches latest AI news, filters for your audience's interests, saves a curated brief | `prompt` |
| **Weekly YouTube Competitor Scan** | Mon 8am | Scans competitor AI education channels for new videos, trending topics, content gaps | `skill` — youtube:youtube-data + research prompt |
| **Weekly Substack Note Ideas** | Mon 8am | Mines published videos, newsletters, and web trends for note-worthy angles | `skill` — substack:generate-note-ideas |
| **YouTube Comment Mining** | Weekly | Extracts content ideas, questions, and pain points from recent video comments | `skill` — youtube:youtube-data + prompt |
| **Monthly Content Calendar Seed** | 1st of month | Generates a draft content calendar pulling from all accumulated research | `prompt` |

**Value**: Wake up Monday morning with fresh ideas, competitor intel, and audience questions already waiting in markdown files.

---

## 2. Production & First Drafts

Get something to *edit* instead of something to *write*.

| Automation | Trigger | What It Does | Type |
|---|---|---|---|
| **Newsletter First Draft** | Thu morning (before Tue publish) | Pulls from weekly research + recent video and generates a draft newsletter issue | `skill` — substack:plan-issue or writing:copywriting |
| **Video Description Generator** | One-off after each upload | Generates optimized title, description, tags, and timestamps for a published video | `prompt` |
| **YouTube Script Outline** | One-off | Given a topic, generates a structured script outline with hooks, key points, and CTA | `skill` — youtube:plan-video |

**Value**: The hardest part of content creation is the blank page. These make sure you always start at draft v1, not draft v0.

---

## 3. Distribution & Repurposing (the multiplier)

One piece of content becomes five.

| Automation | Trigger | Input -> Output | Type |
|---|---|---|---|
| **Video -> Newsletter** | After video publish | YouTube video -> newsletter issue draft | `skill` — youtube:repurpose-video |
| **Video -> Community Post** | After video publish | YouTube video -> community post promoting the video | `skill` — youtube:create-post |
| **Newsletter -> Substack Note** | After newsletter publish | Newsletter issue -> promotional Substack Note | `skill` — substack:create-note |
| **Newsletter -> Video Outline** | On demand | High-performing newsletter -> YouTube video outline | `skill` — youtube:newsletter-to-video |
| **Video -> Social Posts** | After video publish | YouTube video -> multi-platform social copy | `skill` — youtube:repurpose-video |

**Value**: Skills for most of this pipeline already exist. The scheduler turns them from "things you remember to run" into "things that happen automatically."

---

## 4. Business Intelligence & Monitoring

Stay informed without checking dashboards.

| Automation | Schedule | What It Does | Type |
|---|---|---|---|
| **Weekly YouTube Analytics Brief** | Mon 9am | Channel performance summary — views, subs, top videos, growth trends | `skill` — youtube:youtube-data + prompt |
| **Email Triage** | Daily 8am | Categorizes and summarizes overnight emails by priority | `skill` — gmail-email-categorization |
| **Competitor Product Watch** | Weekly | Tracks competitor AI tools/products relevant to Basis and EQL Ivy | `prompt` — web research |
| **EQL Ivy Health Check** | Daily | Hits API endpoints, verifies Render deployment is healthy | `script` — bash curl checks |

---

## 5. Personal Productivity

The "AI chief of staff" automations.

| Automation | Schedule | What It Does | Type |
|---|---|---|---|
| **Morning Briefing** | Daily 7:30am | Calendar, tasks, priorities, weather, anything notable for the day | `prompt` + calendar/task tools |
| **Weekly Review** | Fri 5pm | Accomplishments, open items, next week priorities | `prompt` |
| **Scheduler Self-Cleanup** | Monthly | Cleans old logs and results to prevent disk bloat | `script` — scheduler cleanup command |

---

## 6. Audience Showcase & Content Opportunities

The scheduler becomes **content itself** — videos and newsletter issues that demo what's possible.

| Content Idea | Audience Appeal | Why It Resonates |
|---|---|---|
| **"The AI Content Repurposing Machine"** | Very High | Every creator wants 1 piece -> 5 pieces. Demo your actual pipeline. |
| **"I Built an AI Morning Briefing"** | Very High | Universal desire — everyone wants a personal AI assistant that briefs them |
| **"Automate Your Content Calendar with AI"** | High | Solopreneurs and creators will love this — directly actionable |
| **"AI Email Triage: Never Miss What Matters"** | High | Universal pain point, very relatable |
| **"Monitor Your Side Projects While You Sleep"** | Medium-High | Speaks to the indie hacker/developer segment |
| **"Weekly AI Competitor Intelligence on Autopilot"** | High | Appeals to entrepreneurs and business-minded audience |

**The meta-play**: You're not just teaching the concepts — you're eating your own cooking. Every automation you demo is one you actually use. That authenticity is your edge.

---

## 7. Marketplace Strategy: The Scheduler as Glue

- **The scheduler makes every other skill more valuable.** Content strategy skills are nice. Content strategy skills that run on autopilot are a different value proposition entirely.
- **Pre-built "recipe packs"** could be a product angle:
  - **Content Creator Pack** — research + ideation + repurposing automations
  - **Solopreneur Pack** — email triage + analytics + competitor monitoring
  - **Developer Pack** — health checks + deployment monitoring + testing
- **Scheduler as the gateway** — it's the first plugin that demonstrates ongoing value (not one-shot), which builds the habit of using the marketplace

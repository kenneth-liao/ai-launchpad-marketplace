---
name: business-competitor-analysis
description: Perform comprehensive competitor analysis for any business. Accepts either direct business details or a website URL to extract business information. Produces an executive-summary markdown report with market positioning, pricing/business model, product features, funding/company size, SWOT analysis, and competitive matrix. All findings are data-grounded with inline source references. Use when the user asks to analyze competitors, understand competitive landscape, compare a business to alternatives, or perform market research.
---

# Competitor Analysis Skill

Perform data-grounded competitor analysis producing an executive-summary markdown document with cited sources.

## Workflow Overview

1. **Extract business information** from provided details or website
2. **Identify top 5 competitors** via web search
3. **Research each competitor** across key dimensions
4. **Synthesize findings** into structured report with citations

## Step 1: Extract Business Information

**If user provides a website URL:**
1. Fetch the URL using `web_fetch`
2. Extract: company name, value proposition, target market, products/services, pricing (if visible), key differentiators

**If user provides business details directly:**
1. Parse the provided information
2. Identify any gaps that require web research to fill

**Required business context to gather:**
- Company name and description
- Industry/vertical
- Target customer segment (B2B/B2C, size, geography)
- Core products/services
- Pricing model (if discoverable)
- Key value propositions

## Step 2: Identify Top 5 Competitors

Run targeted searches to find direct competitors:

```
Search queries to use:
- "[company name] competitors"
- "[product category] companies"
- "[industry] [target market] solutions"
- "alternatives to [company name]"
- "[core service] providers [geography if relevant]"
```

Select the top 5 most relevant direct competitors based on:
- Similar target market and customer segment
- Overlapping product/service offerings
- Comparable business model
- Market presence and visibility in search results

## Step 3: Research Each Competitor

For each competitor, gather data across four dimensions:

### 3a. Market Positioning & Messaging
- Fetch competitor homepage and about page
- Extract: tagline, value proposition, target audience messaging
- Note: tone, positioning (premium/budget/mid-market), key claims

### 3b. Pricing & Business Model
- Search "[competitor] pricing" and fetch pricing pages
- Document: pricing tiers, model (subscription/one-time/freemium), entry price point
- If pricing not public, note this and search for any available information

### 3c. Product/Feature Comparison
- Review product pages and feature lists
- Identify: core features, unique capabilities, integrations, limitations
- Note any recent product launches or announcements

### 3d. Funding & Company Size
- Search "[competitor] funding" and "[competitor] company size"
- Check for: Crunchbase mentions, LinkedIn company size, press releases
- Document: funding rounds, total raised, employee count estimates, founding year

## Step 4: Synthesize Report

Generate markdown report following the exact structure below.

## Output Template

```markdown
# Competitive Analysis: [Subject Company Name]

**Analysis Date:** [Current Date]  
**Industry:** [Industry/Vertical]  
**Target Market:** [B2B/B2C, segment details]

---

## Executive Summary

[2-3 paragraph synthesis of competitive landscape. Include: market position of subject company relative to competitors, key competitive advantages and vulnerabilities, most significant competitive threats. Every claim must reference a source using format [Source N].]

---

## Competitive Matrix

| Dimension | [Subject] | [Competitor 1] | [Competitor 2] | [Competitor 3] | [Competitor 4] | [Competitor 5] |
|-----------|-----------|----------------|----------------|----------------|----------------|----------------|
| **Positioning** | [Premium/Mid/Budget] | ... | ... | ... | ... | ... |
| **Target Customer** | [Segment] | ... | ... | ... | ... | ... |
| **Pricing Model** | [Model] | ... | ... | ... | ... | ... |
| **Entry Price** | [$X/mo or N/A] | ... | ... | ... | ... | ... |
| **Key Differentiator** | [1-liner] | ... | ... | ... | ... | ... |
| **Funding Stage** | [Stage/Amount] | ... | ... | ... | ... | ... |
| **Est. Company Size** | [Employees] | ... | ... | ... | ... | ... |

---

## Competitor Deep Dives

### [Competitor 1 Name]

**Overview:** [1-2 sentences on what they do and who they serve] [Source N]

**Market Positioning:** [How they position themselves, key messaging themes] [Source N]

**Pricing & Business Model:** [Pricing structure, tiers, model] [Source N]

**Key Products/Features:** [Core offerings, standout capabilities] [Source N]

**Funding & Scale:** [Funding history, company size indicators] [Source N]

**Competitive Threat Level:** [High/Medium/Low] — [1 sentence justification]

---

[Repeat for Competitors 2-5]

---

## SWOT Analysis: [Subject Company]

### Strengths
- [Strength 1 with supporting evidence] [Source N]
- [Strength 2 with supporting evidence] [Source N]

### Weaknesses
- [Weakness 1 based on competitive gaps] [Source N]
- [Weakness 2 based on competitive gaps] [Source N]

### Opportunities
- [Opportunity 1 based on market/competitor analysis] [Source N]
- [Opportunity 2 based on market/competitor analysis] [Source N]

### Threats
- [Threat 1 from competitive landscape] [Source N]
- [Threat 2 from competitive landscape] [Source N]

---

## Strategic Recommendations

Based on this analysis, consider:

1. **[Recommendation 1]:** [Actionable recommendation with rationale tied to findings] [Source N]
2. **[Recommendation 2]:** [Actionable recommendation with rationale tied to findings] [Source N]
3. **[Recommendation 3]:** [Actionable recommendation with rationale tied to findings] [Source N]

---

## Sources

[1] [Source Title] — [URL] — Accessed [Date]
[2] [Source Title] — [URL] — Accessed [Date]
[3] ...
```

## Citation Requirements

**Inline citations are mandatory.** Every factual claim must include `[Source N](#Sources)` reference.

- Number sources sequentially as encountered
- Include the exact URL in the Sources section
- If information comes from multiple sources, cite all: `[Source 1, 3](#Sources)`
- For claims that cannot be verified, explicitly state: "Unable to verify from public sources"
- Prefer primary sources (company websites, press releases) over secondary (news articles, blogs)

## Quality Checklist

Before finalizing report, verify:

- [ ] All 5 competitors researched across all 4 dimensions
- [ ] Every factual claim has inline citation
- [ ] Competitive matrix is complete with no empty cells (use "N/A" or "Not disclosed" if needed)
- [ ] SWOT items are specific and evidence-based, not generic
- [ ] Recommendations are actionable and tied to specific findings
- [ ] Sources section includes all referenced URLs

## Error Handling

**If competitor website is inaccessible:** Note in report, use available search results and news coverage instead.

**If pricing not public:** State "Pricing not publicly disclosed" and note any indirect indicators (e.g., "enterprise sales model suggested by 'Contact Us' pricing page").

**If funding data unavailable:** Search for alternative signals: LinkedIn employee count, office locations, news mentions of growth.

**If fewer than 5 clear competitors exist:** Include available competitors and note the market context (e.g., "Emerging market with limited direct competitors").

# Premium Plugin Monetization Report

**Date**: 2026-02-18
**Status**: Draft for review

---

## Problem Statement

We share free Claude Code skills and plugins with newsletter readers and YouTube viewers. We want to start offering **premium plugins** with paid access. The current approach (a single GitHub marketplace repo) means anyone with access to the repo gets all plugins — there's no way to restrict access on a per-plugin basis.

**Requirements**:
- Per-plugin access control (buying one plugin shouldn't grant access to others)
- Monthly subscription support
- Lowest possible fees
- Lowest friction for the customer
- Must support full plugins (skills, commands, subagents, hooks, MCP servers)

---

## Fee Comparison

| Platform | Fees | Total on $30 sale | Subscriptions | Tax/VAT (MoR) |
|----------|------|--------------------|--------------|----------------|
| **Stripe (direct)** | 2.9% + $0.30 | ~$1.17 | Yes | No — you handle it |
| **Whop** | ~3% | ~$0.90 | Yes | Yes |
| **Polar.sh** | 4% + $0.40 (+1.5% intl, +0.5% subs) | ~$1.60 | Yes | Yes |
| **Lemon Squeezy** | 5% + $0.50 | ~$2.00 | Yes | Yes |
| **Gumroad** | 10% + processing | ~$3.87 | Yes | Yes |

**Notes**:
- Stripe is cheapest but requires building everything yourself (checkout, license management, tax compliance)
- Lemon Squeezy was acquired by Stripe in 2024; users report reliability and payout issues since
- Polar.sh is developer-focused with built-in license key generation, GitHub repo access automation, and subscription management
- Gumroad is by far the most expensive

---

## Delivery Models

### Model A: GitHub Repo Access (Per-Plugin Private Repos)

Each premium plugin lives in its own private GitHub repo. The public marketplace.json catalog references each plugin's separate repo. A payment platform auto-invites the buyer as a GitHub collaborator.

**Architecture**:
```
your-org/marketplace (public)             <- catalog only, no plugin code
  .claude-plugin/marketplace.json
    plugin-a -> your-org/plugin-a (private repo)
    plugin-b -> your-org/plugin-b (private repo)
    plugin-c -> your-org/plugin-c (private repo)
```

**marketplace.json**:
```json
{
  "name": "ai-launchpad-premium",
  "owner": { "name": "The AI Launchpad" },
  "plugins": [
    {
      "name": "skill-factory",
      "source": { "source": "github", "repo": "your-org/skill-factory" },
      "description": "..."
    },
    {
      "name": "youtube-orchestrator",
      "source": { "source": "github", "repo": "your-org/youtube-orchestrator" },
      "description": "..."
    }
  ]
}
```

When a user runs `/plugin install skill-factory@ai-launchpad-premium`, Claude Code tries to `git clone` only that specific repo. No access = install fails.

**Customer experience**:
1. Buy on Polar/Whop
2. Accept GitHub collaborator invite (email)
3. Ensure git credentials work (`gh auth login`)
4. Set `GITHUB_TOKEN` in shell for auto-updates
5. `/plugin marketplace add your-org/marketplace`
6. `/plugin install plugin-name@marketplace`

**Pros**:
- Full plugin delivered — hooks, commands, subagents, MCP servers, skills, scripts, everything
- Customer gets source code and can inspect what they're running
- Straightforward to implement

**Cons**:
- More customer friction (GitHub invite acceptance, credential setup)
- Subscription revocation requires a cron job or webhook to remove collaborators on cancel
- Customer needs `GITHUB_TOKEN` set for auto-updates to work
- Customer must have a GitHub account

---

### Model B: API + License Key

A public "shell" plugin uses the `!command` syntax in SKILL.md to fetch actual skill content from an authenticated API at runtime.

**How `!command` works**: The `!` backtick syntax in SKILL.md runs shell commands *before* the skill content is sent to Claude. The command output replaces the placeholder. Claude only receives the API response, not the command itself.

**Example skill**:
```yaml
---
name: premium-workflow
description: Advanced workflow automation
---

!`curl -sf -H "Authorization: Bearer ${AI_LAUNCHPAD_LICENSE}" https://api.yoursite.com/v1/skills/premium-workflow`
```

**Flow**:
1. Skill loads -> `!curl` executes immediately
2. API checks license key against database
3. Valid + subscription active -> returns full skill instructions
4. Invalid/expired -> returns error message
5. Claude receives only the API response

**Customer experience**:
1. Buy on Polar/Whop -> get license key instantly
2. Add `export AI_LAUNCHPAD_LICENSE=lk_xxxx` to `.zshrc` (one time)
3. `/plugin marketplace add your-org/marketplace`
4. `/plugin install plugin-name@marketplace`
5. Skills auto-authenticate transparently

**Pros**:
- Much less friction (no GitHub invite, no credential setup)
- Subscription revocation is instant (API rejects expired keys)
- License key works across all machines
- Content never stored on customer's disk (IP protection)
- No GitHub account required
- Works with monthly subscriptions naturally

**Cons**:
- Only works for content that can be fetched at runtime (see table below)
- Requires API uptime
- Adds latency on first skill load

**What can and cannot be delivered via API**:

| Component | Deliverable via API? | Reason |
|-----------|---------------------|--------|
| Skill instructions | Yes | `!command` injects content at runtime |
| Templates / references | Yes | Fetched via `!command` |
| Hooks | No | Defined in plugin.json at install time |
| MCP server configs | No | Defined in plugin.json at install time |
| Commands (.md files) | Partially | Stub file must exist on disk, but content can use `!command` |
| Subagent definitions (.md) | Partially | Stub file must exist on disk, but content can use `!command` |
| Scripts | No | Must exist as files on disk |

---

### Model C: Hybrid (Recommended)

Combine both models. Use the API/license key as the primary delivery mechanism with a thin public "shell" plugin that contains structure but gates all valuable content behind the API.

**Architecture**:
```
your-org/marketplace (public)
  plugins/
    premium-plugin/
      .claude-plugin/plugin.json      <- hooks, MCP configs (structural)
      skills/
        main-skill/
          SKILL.md                    <- uses !`curl` to fetch content
      commands/
        premium-cmd.md                <- stub that calls !`curl`
      agents/
        premium-agent.md              <- stub that calls !`curl`
```

**Every command, skill, and agent is a thin shell**:
```yaml
# commands/premium-cmd.md
---
name: premium-cmd
description: Premium automation command
disable-model-invocation: true
---

!`curl -sf -H "Authorization: Bearer ${AI_LAUNCHPAD_LICENSE}" https://api.yoursite.com/v1/commands/premium-cmd || echo "Invalid or expired license. Get yours at https://theailaunchpad.com/premium"`
```

**What's public** (in the repo): Plugin structure, hook definitions, thin command/skill stubs. This is like an app's UI shell — not the valuable IP.

**What's gated** (behind the API): The actual instructions, prompts, workflows, and logic that make the plugin valuable. Never touches the customer's disk.

For hooks and MCP server configs that must live in plugin.json — those are structural. The behavior they trigger can still call the API for actual logic.

**Pros**:
- Lowest customer friction of all models
- Instant subscription revocation
- IP protection (content never on disk)
- Full plugin features supported (hooks, commands, subagents, MCP servers)
- No GitHub access management overhead
- Works across machines with same license key

**Cons**:
- More upfront work to build the API
- Requires API uptime
- Hook and MCP server *configurations* are visible in the public repo (though not the content they operate on)

---

## Recommended Stack

### Payment + Subscriptions: Polar.sh

- **Fees**: 4% + $0.40 per transaction (fraction of Gumroad's 10%)
- **Built-in license key generation and validation** — no custom code needed
- **Built-in subscription management** — handles recurring billing, cancellation, reactivation
- **Merchant of Record** — handles all global sales tax and VAT
- **API + webhooks** for custom integrations
- **Also supports GitHub repo access** as an automated benefit if needed for some plugins
- Developer-focused platform and audience

### API Backend: Supabase Edge Function (or Vercel)

A simple edge function that:
1. Receives license key in `Authorization` header
2. Calls Polar API to validate key + check subscription status
3. Returns skill/command content if valid
4. Returns error message if not

We already have Supabase in our stack, so this adds minimal complexity.

**Alternatively**: Store skill content directly in Supabase database tables for easy management — one row per skill/command, with the content as a text column.

### Plugin Distribution: Public Marketplace Repo

- Public repo with marketplace.json and thin shell plugins
- Anyone can install — nothing works without a valid license key
- Zero GitHub access management
- Free plugins can coexist in the same marketplace with full content inline

---

## Optimized Customer Journey

1. Watch YouTube video / read newsletter
2. Click link -> Polar checkout (supports Stripe payment, no extra account needed)
3. Get license key instantly on confirmation page
4. One-time setup: `export AI_LAUNCHPAD_LICENSE=lk_xxxx` (add to `.zshrc`)
5. `/plugin marketplace add your-org/ai-launchpad-premium`
6. `/plugin install premium-plugin@ai-launchpad-premium`
7. Use the plugin — skills auto-authenticate transparently
8. Subscription lapses -> skills return "license expired" message with resubscribe link
9. Re-subscribe -> instant access restored (same license key reactivated)

**Total friction**: One env var export. No GitHub invite. No credential setup. No GitHub account required.

---

## Open Questions

- [ ] What premium plugins do we launch with first?
- [ ] Pricing strategy: per-plugin vs. bundle/tier vs. all-access subscription?
- [ ] Do we need a customer dashboard for license key management, or is Polar's built-in page sufficient?
- [ ] Should free plugins live in the same marketplace or a separate one?
- [ ] Do we want a grace period when subscriptions lapse?
- [ ] How do we handle plugin updates — do we version the API content or always serve latest?

---

## Sources

- [Polar.sh - Product Benefits & Fulfillment](https://polar.sh/features/benefits)
- [Polar.sh Documentation](https://polar.sh/docs/introduction)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Claude Code Plugin Marketplace Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Payment Processor Fees Compared - UserJot](https://userjot.com/blog/stripe-polar-lemon-squeezy-gumroad-transaction-fees)
- [Polar vs Lemon Squeezy](https://polar.sh/resources/comparison/lemon-squeezy)
- [Whop Pricing 2026](https://www.schoolmaker.com/blog/whop-pricing)
- [Managing API Keys in Claude Skills](https://medium.com/ducky-ai/the-credential-conundrum-managing-api-keys-in-claude-skills-430c41b21aa8)
- [GitHub Issue #9756 - Auth on Private Marketplaces](https://github.com/anthropics/claude-code/issues/9756)
- [GumHub - Sell GitHub Repo Access via Gumroad](https://m1guelpf.gumroad.com/l/gumhub)
- [How to Sell Code with Gumroad and GitHub](https://makerkit.dev/blog/tutorials/sell-code-gumroad-github)
- [Whop - Sell Software Access](https://whop.com/sell/software/)
- [SkillsMP - Agent Skills Marketplace](https://skillsmp.com)
- [Polar vs Gumroad vs Lemon Squeezy](https://veloxthemes.com/blog/polar-vs-lemonsqueezy-vs-gumroad)

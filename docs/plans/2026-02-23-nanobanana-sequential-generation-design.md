# Nanobanana Sequential Generation — Design

**Date:** 2026-02-23
**Scope:** Documentation-only enhancement to `art:nanobanana`
**Approach:** Approach A — SKILL.md section + prompts.md expansion

## Problem

Nanobanana supports multi-image referencing (`-i`) and batch generation, but lacks documented workflow patterns for maintaining visual consistency across a series of images. Users generating multiple images for newsletters, A/B thumbnail testing, or brand asset sets have no guidance on how to chain generations sequentially.

## Solution

Add documentation covering three sequential generation patterns, with no new scripts or structural changes.

## Changes

### 1. SKILL.md — New "Sequential Generation" section (~70 lines)

**Placement:** After "Features" section (after line 300), before "Best Practices".

**Three patterns:**

1. **Style-Board Anchoring** — Generate an anchor image establishing visual identity (colors, style, mood, lighting). Reference the anchor via `-i` for all subsequent images. Use case: newsletter visual series, brand-consistent batches, A/B thumbnail variants.

2. **Subject Consistency** — Generate an initial subject image. Reference it when generating new poses/settings. Accumulate 2-3 best references for stronger consistency. Use case: mascot across scenes, product in different contexts.

3. **Progressive Accumulation** — Start with anchor, add each successful output to the reference pool. Cap at 3-4 references (diminishing returns beyond that; dilutes style signal). Use case: long series (5+ images) needing compounding consistency.

Each pattern includes: when to use, step-by-step workflow with CLI examples, model selection tips.

### 2. SKILL.md — New "Pattern 4" in Downstream Integration (~10 lines)

**Placement:** After Pattern 3 in "Downstream Skill Integration Guide" section.

Shows how orchestrator skills should: generate anchor first, pass output path as `-i` for subsequent calls, maintain a running reference list.

### 3. references/prompts.md — New "Sequential Generation Prompts" section (~60 lines)

**Placement:** After "Batch Generation Tips" section (after line 267).

**Templates for:**
- Style-board anchor generation prompts
- Referencing an anchor for subsequent images
- Subject consistency prompts (establishing + new scenes)
- A/B variant prompts (same style, different compositions)
- Newsletter series prompts

**Tips subsection:**
- How to describe what to preserve vs. change in follow-up prompts
- Reference image ordering (style anchor first)
- When to add/drop references from accumulation pool

### 4. plugin.json — Version bump

`1.0.1` → `1.1.0`

## Impact

| File | Lines Added | New Total |
|------|-------------|-----------|
| SKILL.md | ~80 | ~440 (under 500 limit) |
| prompts.md | ~60 | ~327 |
| plugin.json | 1 | — |

No new files. No scripts. No structural changes.

## Framework Compliance

- [x] Task skill category unchanged
- [x] SKILL.md stays under 500 lines
- [x] Platform-specific knowledge in references/ (prompt templates)
- [x] Strategy/workflow guidance in SKILL.md (discoverable)
- [x] Downstream integration pattern documented
- [x] Plugin version bumped per skill-factory rules

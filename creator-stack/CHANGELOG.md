# Changelog

All notable changes to the Creator Stack plugin.

## [1.1.0] - 2026-03-05

### Changed

- **Renamed 7 skills** for clarity and consistency:
  - `copywriting` → `write` (general-purpose writing, not just marketing copy)
  - `ideate` → `extract-ideas` (matches core principle: "extract, don't invent")
  - `create-note` → `write-note` (more precise verb for Substack Notes)
  - `create-post` → `community-post` (removes ambiguity — specifically YouTube community posts)
  - `generate-note-ideas` → `ideate-notes` (concise, mirrors foundation skill relationship)
  - `plan-issue` → `plan-newsletter` ("issue" reads as "problem" without Substack context)
  - `optimize-issue` → `optimize-newsletter` (same)
- Updated all cross-references across skills, references, README, and changelog

## [1.0.0] - 2026-03-05

### Added

- **Consolidated 7 previous plugins** into a single unified creator-stack:
  - Writing (write, voice)
  - Content Strategy (research, title, hook, extract-ideas)
  - Visual Design (thumbnail, social-graphic, newsletter-visuals)
  - AI Image Generation (nanobanana)
  - Branding (brand-guidelines, design-system)
  - YouTube (youtube-data, plan-video, repurpose-video, newsletter-to-video, community-post)
  - Substack (plan-newsletter, optimize-newsletter, ideate-notes, write-note)
- **21 skills** covering the full content creation lifecycle
- **2 agents**: Thumbnail Reviewer, YouTube Researcher
- **Orchestrator skills** that sequence foundation skills: plan-video, plan-newsletter, optimize-newsletter, repurpose-video, newsletter-to-video, write-note, community-post, ideate-notes, newsletter-visuals
- **AI image generation** via Google Gemini models (nanobanana skill)
- **YouTube Data API integration** for channel/video/comment/transcript analysis

### Changed

- Modernized skill writing style and clarified reference delegation
- Improved skill tone consistency across all 21 skills

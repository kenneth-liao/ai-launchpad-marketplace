---
name: Rules
description: These are explicit rules learned from past mistakes or user corrections. **ALWAYS check these before taking action.**
update_policy: 
- ADD rules when user corrects behavior or expresses frustration about an action (no permission needed)
- Only REMOVE rules when user explicitly rescinds them (no permission needed)
- Add new sections as needed (no permission needed)
rule_format:
- ❌ NEVER [action] [context if needed] - [reason/origin if helpful]
- ✅ ALWAYS [action] [context if needed]
---

## Git & Version Control

- ❌ NEVER commit without explicit approval or request
- ❌ NEVER rebase without permission
- ✅ ALWAYS ask before any destructive git operation

## Code Changes

- ❌ NEVER install dependencies without asking (can break environments)
- ✅ ALWAYS run existing tests after making changes

## Communication

- ❌ DON'T assume what user wants - ask if unclear
- ❌ DON'T create documentation files unless explicitly requested
- ✅ DO ask clarifying questions for ambiguous requests

## Project-Specific Rules

*Add project-specific rules here as learned*


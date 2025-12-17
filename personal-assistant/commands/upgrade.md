---
description: Upgrade the context system from the old directory structure to the new flat core/ structure with template improvements.
---

# Context System Upgrade

Upgrade your context system to the latest structure while preserving all your personal data. This command handles:
1. Moving files from split directories (`projects/`, `session/`) to flat `core/`
2. Upgrading all templates with new sections and structure
3. Intelligently merging your existing data into new template formats
4. Adding new context capabilities (relationships, triggers, journal)

---

## Step 1: Detect Current State

Check the context system structure:

```bash
ls -la ~/.claude/.context/ 2>/dev/null
ls -la ~/.claude/.context/core/ 2>/dev/null
ls ~/.claude/.context/projects/ 2>/dev/null
ls ~/.claude/.context/session/ 2>/dev/null
```

### Determine State

**State A - Already Migrated (no action needed):**
All of these conditions are true:
- `~/.claude/.context/` exists
- `core/relationships.md`, `core/triggers.md`, `core/journal.md` all exist
- No `projects/` directory
- No `session/` directory

**State B - Needs Migration:**
Any of these conditions are true:
- `projects/` directory exists
- `session/` directory exists
- Missing any of: `core/relationships.md`, `core/triggers.md`, `core/journal.md`
- Core files exist but may have old template structure

**State C - No Context System:**
- `~/.claude/.context/` doesn't exist

<REQUIRED>
If State A: Tell user their system is already up to date. Show the verified structure. Stop here.
If State C: Tell user to run `/personal-assistant:setup` first. Stop here.
If State B: Proceed with migration below.
</REQUIRED>

---

## Step 2: Communicate Plan

Before making any changes, explain what will happen:

> **Context System Upgrade**
>
> I'll upgrade your context system to the latest version. Here's what will happen:
>
> **What stays the same:**
> - All your personal data (identity, preferences, rules, workflows, projects, session notes)
> - Everything you've taught me about yourself
>
> **What changes:**
> - Templates get new sections and improved structure
> - Your data migrates into the new template format
> - Files move from `projects/` and `session/` into `core/`
> - Three new context files are added: `relationships.md`, `triggers.md`, `journal.md`
>
> **Safety:**
> - A full backup is created before any changes
> - Your data is intelligently merged, not overwritten
>
> Ready to proceed?

<REQUIRED>
Wait for user confirmation before proceeding. If user declines, stop here.
</REQUIRED>

---

## Step 3: Create Backup

<REQUIRED>
Create a timestamped backup BEFORE any other changes:

```bash
mkdir -p ~/.claude/.context-backups/ && cp -r ~/.claude/.context/ ~/.claude/.context-backups/$(date +%Y%m%d-%H%M%S)/
```

Verify the backup exists:

```bash
ls -la ~/.claude/.context-backups/
```

Tell the user: "Backup created at ~/.claude/.context-backups/XXXXXXXX-XXXXXX/"

**DO NOT proceed if backup fails.**
</REQUIRED>

---

## Step 4: Intelligent Content Migration

For each existing context file, you will:
1. Read the user's current file (extract all user-entered content)
2. Read the new template from the plugin
3. Create a merged version that uses the new template structure but preserves all user data

### Template Location

Templates are at: `~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/`

### Migration Process

<REQUIRED>
Process each file one at a time. For each file:

1. **Read user's current file** - Note all user-entered content (not placeholder text)
2. **Read the corresponding template** - Understand the new structure
3. **Create merged file** - Write to the context directory with:
   - New YAML frontmatter from template
   - All sections from new template
   - User's content placed in the most appropriate matching sections
   - New sections left as placeholders if no user data maps to them

**Critical rules:**
- PRESERVE 100% of user data - nothing gets lost
- Use new template structure (sections, formatting, frontmatter)
- If a section was renamed (e.g., "Personal" → "Personal Life"), map content appropriately
- If unsure where content belongs, keep it in the closest matching section
</REQUIRED>

### File-by-File Instructions

#### 4.1: identity.md

**Read current:**
```bash
cat ~/.claude/.context/core/identity.md
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/identity.md
```

**Section mapping:**
| Old Section | → | New Section |
|-------------|---|-------------|
| Personal | → | Personal Life |
| Professional | → | Professional |
| Communication Style | → | Communication Style |
| (new) | → | Basic Info |
| (new) | → | Goals & Aspirations |
| (new) | → | Current Challenges |
| (new) | → | Values & Principles |
| (new) | → | Health & Wellness |
| (new) | → | Interests & Hobbies |

**Write merged file to:** `~/.claude/.context/core/identity.md`

#### 4.2: preferences.md

**Read current:**
```bash
cat ~/.claude/.context/core/preferences.md
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/preferences.md
```

**Section mapping:**
| Old Section | → | New Section |
|-------------|---|-------------|
| Development Tools | → | Tools & Systems > Development Tools |
| Interface & UX | → | Tools & Systems > Productivity Tools (or Communication > Information Style) |
| Research Preferences | → | Decision-Making > Information Needs |
| Decision-Making | → | Decision-Making |
| Debugging Workflows | → | Tools & Systems > Development Tools |
| (new) | → | Communication |
| (new) | → | Working Style |
| (new) | → | Scheduling & Time |
| (new) | → | Boundaries |

**Write merged file to:** `~/.claude/.context/core/preferences.md`

#### 4.3: workflows.md

**Read current:**
```bash
cat ~/.claude/.context/core/workflows.md
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/workflows.md
```

**Write merged file to:** `~/.claude/.context/core/workflows.md`

#### 4.4: rules.md

**Read current:**
```bash
cat ~/.claude/.context/core/rules.md
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/rules.md
```

**Note:** Rules are user-entered corrections. Preserve ALL existing rules. Use new template structure/frontmatter but keep all user rules intact.

**Write merged file to:** `~/.claude/.context/core/rules.md`

#### 4.5: projects.md (from projects/project_index.md)

**Read current:**
```bash
cat ~/.claude/.context/projects/project_index.md 2>/dev/null || cat ~/.claude/.context/core/projects.md 2>/dev/null
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/projects.md
```

**Changes:**
- Table column "Path" → "Location" (same data, different header)
- New section: "Upcoming Milestones" table
- Same sections: "Active Projects", "Quick Notes", "Archived Projects"

**Write merged file to:** `~/.claude/.context/core/projects.md`

#### 4.6: session.md (from session/current.md)

**Read current:**
```bash
cat ~/.claude/.context/session/current.md 2>/dev/null || cat ~/.claude/.context/core/session.md 2>/dev/null
```

**Read template:**
```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/session.md
```

**Write merged file to:** `~/.claude/.context/core/session.md`

---

## Step 5: Create New Context Files

For each of these files, only create if it doesn't already exist:

```bash
ls ~/.claude/.context/core/relationships.md 2>/dev/null
ls ~/.claude/.context/core/triggers.md 2>/dev/null
ls ~/.claude/.context/core/journal.md 2>/dev/null
```

**If missing, copy from template:**

```bash
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/relationships.md ~/.claude/.context/core/relationships.md
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/triggers.md ~/.claude/.context/core/triggers.md
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/core/journal.md ~/.claude/.context/core/journal.md
```

<REQUIRED>
Do NOT overwrite existing files - they may contain user data from manual creation.
</REQUIRED>

---

## Step 6: Update Instruction Files

These files contain instructions (not user data), so always replace them with the latest versions:

```bash
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/CLAUDE.md ~/.claude/.context/CLAUDE.md
cp ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context-template/context-update.md ~/.claude/.context/context-update.md
```

---

## Step 7: Cleanup Old Directories

Remove the now-empty old directories:

```bash
rmdir ~/.claude/.context/projects/ 2>/dev/null
rmdir ~/.claude/.context/session/ 2>/dev/null
```

Note: `rmdir` only removes empty directories. If removal fails, check what's left:

```bash
ls ~/.claude/.context/projects/ 2>/dev/null
ls ~/.claude/.context/session/ 2>/dev/null
```

---

## Step 8: Verify Final Structure

```bash
ls -la ~/.claude/.context/
ls -la ~/.claude/.context/core/
```

Expected structure:
```
~/.claude/.context/
├── CLAUDE.md
├── context-update.md
└── core/
    ├── identity.md
    ├── preferences.md
    ├── workflows.md
    ├── rules.md
    ├── projects.md
    ├── session.md
    ├── relationships.md
    ├── triggers.md
    └── journal.md
```

---

## Step 9: Report Results

Summarize what was done:

> **Upgrade Complete!**
>
> **Backup saved to:** `~/.claude/.context-backups/XXXXXXXX-XXXXXX/`
>
> **Files migrated:**
> - [x] `identity.md` - Updated template structure, preserved your personal/professional info
> - [x] `preferences.md` - Updated template structure, preserved your preferences
> - [x] `workflows.md` - Updated template structure, preserved your workflows
> - [x] `rules.md` - Updated template structure, preserved all your rules
> - [x] `projects.md` - Moved from `projects/project_index.md`, updated format
> - [x] `session.md` - Moved from `session/current.md`, updated format
>
> **New files created:**
> - [x] `relationships.md` - Track key people in your life
> - [x] `triggers.md` - Important dates, deadlines, proactive reminders
> - [x] `journal.md` - Session history log
>
> **Instructions updated:**
> - [x] `CLAUDE.md` - Latest operating instructions
> - [x] `context-update.md` - Latest update procedures
>
> **Next steps:**
> - The new files have placeholder sections - I'll fill them in as I learn about you
> - Run `/personal-assistant:onboard` if you want to populate them now
> - Or just chat naturally and I'll pick up context over time!

<REQUIRED>
If any step failed:
1. Clearly communicate what failed and why
2. Reassure that the backup is safe at `~/.claude/.context-backups/`
3. Explain how to restore: `rm -rf ~/.claude/.context && cp -r ~/.claude/.context-backups/XXXXXXXX-XXXXXX ~/.claude/.context`
4. Suggest reporting the issue or trying again
</REQUIRED>

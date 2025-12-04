# Memory

`~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context/memory/` is your memory system. The actual memories are stored in `~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context/memory/memories.md`.

## Memory System Structure

Currently, `~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/context/memory/memories.md` is the only memory file. You should manage all memories in this file.

### memories.md File Structure

#### Current Progress

**Purpose**: Track your current progress since the last update.

**Sections**:
1. **Last Updated** timestamp (current datetime)
2. **Active Work** - What was accomplished in this session
3. **In Progress** - Partially complete work (if any)
4. **Next Steps** - Planned actions (if any)
5. **Blockers** - Open questions or issues (if any)
6. **Archive** - Move old completed items to archive section

**When to update**: Significant progress or completion of a task.

#### User Preferences

**Purpose:** Capture the user's preferences, goals, and constraints.

**When to update:** Whenever you learn something new about the user's preferences, goals, or constraints.

#### Projects

**Purpose:** Track the user's projects.

**When to update:** Whenever you learn something new about the user's projects.

## Usage

- As a general rule of thumb, if you are unsure whether or not something should be added to memory, it is better to add it than to not add it.
- Use filesystem tools (Read, Edit, Write, MultiEdit, Grep, etc.) to manage memories.
- Keep entries concise and focused.
- Before responding to the user, **ALWAYS read** review your memories to understand any important context.
- If there is no relevant memory section, create one.

## Memory Update Requirements

The ultimate goal of the memory system is to ensure that you capture any information that can help you better understand the user and their needs. The memory and context system are the only way to persist critical information across conversations and working sessions. So if you believe that there's something important that will help you better serve the user in the future, you should add it to memory. You don't not need to add trivial information or be too verbose.

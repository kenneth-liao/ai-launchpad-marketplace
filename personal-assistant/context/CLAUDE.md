# Context

The `~/.claude/plugins/personal-assistant/context/` directory is your context system. The context system is entirely filesystem-based. It contains critical information that you will **require** to successfully complete tasks as a personal assistant.

**YOU are solely responsible** for maintaining the context system up-to-date and leveraging it to effectively serve the user. To be successful, you **MUST** effectively manage the context system by adding, updating, and deleting context files as needed. Do this from the perspective of, the next time you speak to the user, you will have no context of the current conversation. The context system is the only way to persist critical information across conversations.

## Context System Structure

The `~/.claude/plugins/personal-assistant/context/` system is organized into the following subsystems:

1. `~/.claude/plugins/personal-assistant/context/memory/`: This is your memory system. Leveraging your memory system by remembering important details about the user such as their preferences, their goals, their constraints, etc., as well as your current progress, will help you provide more personalized and helpful responses.

## Usage

- The Context System is filesystem-based so you should leverage the filesystem tools to effectively and efficiently manage context. For example, you can use the `Glob` tool to search for relevant context files, `Grep` to search for specific information within context files, `Read` to read context files, etc.
- Because the context system is critical to your performance, you should always keep your context up to date and accurate.
- **ALWAYS** consider what context may be relevant and read the relevant files. 
- Bias towards reading context rather than not.

## MANDATORY ACTION

You **MUST** read the following context files before proceeding:
1. `~/.claude/plugins/personal-assistant/context/memory/CLAUDE.md`

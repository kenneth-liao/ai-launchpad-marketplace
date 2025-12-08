#!/usr/bin/env python3
"""
UserPromptSubmit hook to load initial context into Claude's context window.
Context is loaded as a system reminder (see claude-trace).

Context is stored in ~/.claude/.context/ (external to the plugin).
Use the /personal-assistant:setup command to initialize the context directory and output style.
"""

import json
import sys
from pathlib import Path

# User's context directory (external to plugin, persists across updates)
CONTEXT_DIR = Path.home() / ".claude" / ".context"


def get_context_or_setup_instructions() -> str:
    """
    Get context from user's context directory.
    If not initialized, return setup instructions.
    """
    context_path = CONTEXT_DIR / "CLAUDE.md"

    if not context_path.exists():
        return f"""# Personal Assistant Not Set Up

The personal assistant plugin has not been set up yet.

1. Ask the user if they want to set up the personal assistant (context system + output style).
2. **ONLY** if you receive an explicit confirmation, run the `/personal-assistant:setup` command to:
   - Set the output style to personal-assistant
   - Initialize the context directory at `{CONTEXT_DIR}`
3. Validate that setup completed correctly.

This only needs to be done once. Your context will persist across plugin updates. You can then continue addressing the user's message.
"""

    try:
        return context_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Warning: Unable to read context file: {e}"


def main() -> None:
    # Parse hook input from stdin (required even if unused, to consume the input)
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Get context (or setup instructions if not initialized)
    context = get_context_or_setup_instructions()

    # Output the context to be injected into Claude's session
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))

    # We must exit with code 0 for Claude to see the STDOUT
    sys.exit(0)


if __name__ == "__main__":
    main()

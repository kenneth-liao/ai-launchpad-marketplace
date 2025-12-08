#!/usr/bin/env python3
"""
UserPromptSubmit hook to load initial context into Claude's context window.
Context is loaded as a system reminder (see claude-trace).

Context is stored in ~/.claude/.context/ (external to the plugin).
Use the /setup-context-system command to initialize the context directory.
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
        return f"""# Context System Not Initialized

The personal assistant context system has not been set up yet.

1. Run the `/setup-context-system` command to initialize your context directory at:
`{CONTEXT_DIR}`
2. Validate that the context files were created correctly.

This only needs to be done once. Your context will persist across plugin updates. You can then continue.
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

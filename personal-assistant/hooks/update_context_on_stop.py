#!/usr/bin/env python3
"""
Stop hook to trigger context updates after each Claude response.
Blocks Claude from stopping until it updates the context system.

Context is stored in ~/.claude/.claude-context/ (external to the plugin).
"""

import json
import sys
from pathlib import Path

# User's context directory (external to plugin, persists across updates)
CONTEXT_DIR = Path.home() / ".claude" / ".context"


def get_context_update_instructions() -> str:
    """Generate context update instructions with correct paths."""
    # Check if context system is initialized
    if not CONTEXT_DIR.exists():
        return """Context system not initialized. Run /setup-context-system first."""

    return f"""Before finishing, update the context system:

If you haven't already, read `{CONTEXT_DIR}/context-update.md` to understand the requirements for a context update.

If a context update is necessary, complete the update according to the instructions in `{CONTEXT_DIR}/context-update.md`.

After completing the context update or if no update is necessary, you may finish your response."""


def main() -> None:
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Check if Claude is already continuing due to this hook
    stop_hook_active = hook_input.get("stop_hook_active", False)

    if stop_hook_active:
        # Let Claude stop - context update already happened this turn
        sys.exit(0)

    # Block Claude and instruct it to update context
    output = {
        "decision": "block",
        "reason": get_context_update_instructions()
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()


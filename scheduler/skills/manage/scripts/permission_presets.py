"""Permission presets for scheduled tasks.

Defines named tool bundles that map to Claude Code's --allowedTools flag,
making it easy to pre-approve the right set of tools for non-interactive
scheduled runs without requiring deep Claude Code knowledge.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Preset definitions
# ---------------------------------------------------------------------------

PRESETS: dict[str, list[str]] = {
    "readonly": [
        "Read",
        "Glob",
        "Grep",
        "Bash(ls *)",
        "Bash(git log *)",
        "Bash(git diff *)",
        "Bash(git status)",
        "WebSearch",
        "WebFetch",
    ],
    "full-edit": [
        "Read",
        "Write",
        "Edit",
        "Glob",
        "Grep",
        "Bash(ls *)",
        "Bash(git *)",
        "Bash(npm *)",
        "Bash(uv *)",
        "Bash(python *)",
        "WebSearch",
        "WebFetch",
    ],
    "research": [
        "Read",
        "Glob",
        "Grep",
        "WebSearch",
        "WebFetch",
        "Bash(curl *)",
        "Bash(ls *)",
    ],
    # Sentinel — triggers --dangerously-skip-permissions instead of --allowedTools
    "bypass": [],
}


def expand_preset(name: str) -> list[str]:
    """Return the tool list for a named preset.

    Raises ``KeyError`` if the preset name is unknown.
    """
    if name not in PRESETS:
        raise KeyError(f"Unknown permission preset: '{name}'. Valid presets: {', '.join(sorted(PRESETS))}")
    return list(PRESETS[name])


def is_bypass_preset(name: str) -> bool:
    """Return True if *name* is the bypass preset (skip all permission checks)."""
    return name == "bypass"


def list_presets() -> list[str]:
    """Return sorted list of available preset names."""
    return sorted(PRESETS.keys())

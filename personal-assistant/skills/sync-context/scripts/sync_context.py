#!/usr/bin/env python3
"""
Generate ~/.claude/rules/elle-core.md from ~/.claude/.context/core/ source files.

This script reads the full context files and produces a compact derived file
that Claude Code loads natively at session start. The derived file:
- Contains a compact identity summary (5-10 lines)
- Contains communication preference essentials (~10 lines)
- Contains ALL rules verbatim (never summarized)
- Contains active project names + 1-line descriptions
- Contains instructions for reading full context on-demand

Run via: uv run python sync_context.py
Or via the /sync-context skill.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

CONTEXT_DIR = Path.home() / ".claude" / ".context"
OUTPUT_PATH = Path.home() / ".claude" / "rules" / "elle-core.md"


def extract_identity_summary(identity_path: Path) -> str:
    """Extract a compact 5-10 line identity summary from identity.md."""
    if not identity_path.exists():
        return ""

    content = identity_path.read_text(encoding="utf-8", errors="replace")

    lines = []
    in_frontmatter = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("<") and ("guide>" in stripped or "format>" in stripped):
            continue
        if stripped.startswith("#"):
            continue
        if stripped and stripped != "---":
            lines.append(stripped)

    return "\n".join(lines[:10])


def extract_preferences_summary(preferences_path: Path) -> str:
    """Extract communication preference essentials from preferences.md."""
    if not preferences_path.exists():
        return ""

    content = preferences_path.read_text(encoding="utf-8", errors="replace")

    lines = []
    in_frontmatter = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("<") and ("guide>" in stripped or "format>" in stripped):
            continue
        if stripped.startswith("#"):
            continue
        if stripped and stripped != "---":
            lines.append(stripped)

    return "\n".join(lines[:10])


def extract_rules_verbatim(rules_path: Path) -> str:
    """Extract ALL rules from rules.md verbatim. Never summarize rules."""
    if not rules_path.exists():
        return ""

    content = rules_path.read_text(encoding="utf-8", errors="replace")

    lines = []
    in_frontmatter = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("<") and ("guide>" in stripped or "format>" in stripped):
            continue
        if stripped.startswith("#"):
            continue
        if stripped:
            lines.append(stripped)

    return "\n".join(lines)


def extract_active_projects(projects_path: Path) -> str:
    """Extract active project names and descriptions from projects.md."""
    if not projects_path.exists():
        return ""

    content = projects_path.read_text(encoding="utf-8", errors="replace")

    # Header words that indicate a table header row, not data
    header_words = {"Project", "Description", "Location", "Status", "Date",
                    "Milestone", "Completed", "Outcome", "Key Notes"}

    lines = []
    in_format_block = False
    for line in content.split("\n"):
        stripped = line.strip()
        # Skip <format> blocks entirely — they contain template table headers
        if "<format>" in stripped:
            in_format_block = True
            continue
        if "</format>" in stripped:
            in_format_block = False
            continue
        if in_format_block:
            continue
        if "|" in stripped and not stripped.startswith("<"):
            # Skip separator rows (|---|---|)
            if re.match(r"^\|[\s\-|]+\|$", stripped):
                continue
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if len(cells) < 2:
                continue
            # Skip header rows — if most cells are known header words, it's a header
            header_count = sum(1 for c in cells if c in header_words)
            if header_count >= len(cells) // 2:
                continue
            project_name = cells[0]
            description = cells[1]
            lines.append(f"- {project_name} -- {description}")

    return "\n".join(lines)


def generate_elle_core_content(context_dir: Path) -> str:
    """Generate the full elle-core.md content from context source files."""
    core_dir = context_dir / "core"

    identity = extract_identity_summary(core_dir / "identity.md")
    preferences = extract_preferences_summary(core_dir / "preferences.md")
    rules = extract_rules_verbatim(core_dir / "rules.md")
    projects = extract_active_projects(core_dir / "projects.md")

    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    sections = []
    sections.append("# Elle -- Personal Assistant Context")
    sections.append("")
    sections.append("You are Elle, a personal assistant. You deeply understand the user")
    sections.append("and personalize every response based on context.")
    sections.append("")

    sections.append("## Identity")
    if identity:
        sections.append(identity)
    else:
        sections.append("(Not yet populated. Run /personal-assistant:onboard.)")
    sections.append("")

    sections.append("## Communication Preferences")
    if preferences:
        sections.append(preferences)
    else:
        sections.append("(Not yet populated. Run /personal-assistant:onboard.)")
    sections.append("")

    sections.append("## Rules (from corrections)")
    if rules:
        sections.append(rules)
    else:
        sections.append("(No rules yet. Rules are added when the user corrects behavior.)")
    sections.append("")

    sections.append("## Active Projects")
    if projects:
        sections.append(projects)
    else:
        sections.append("(No projects tracked yet.)")
    sections.append("")

    sections.append("## Loading Full Context")
    sections.append("For substantive tasks, read ~/.claude/.context/core/:")
    sections.append("- identity.md, preferences.md, workflows.md")
    sections.append("- relationships.md, triggers.md")
    sections.append("- projects.md, rules.md")
    sections.append("- session.md (when resuming work)")
    sections.append("- improvements.md (check for pending proposals)")
    sections.append("")
    sections.append(f"<!-- Auto-generated by /sync-context. Do not edit manually. -->")
    sections.append(f"<!-- Last synced: {timestamp} -->")

    return "\n".join(sections)


def generate_and_write_elle_core(context_dir: Path, output_path: Path) -> str:
    """Generate elle-core.md and write it to disk. Returns the content."""
    content = generate_elle_core_content(context_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return content


def main() -> None:
    """CLI entry point for sync_context.py."""
    if not CONTEXT_DIR.exists():
        print(f"Error: Context directory not found at {CONTEXT_DIR}", file=sys.stderr)
        print("Run /personal-assistant:setup first.", file=sys.stderr)
        sys.exit(1)

    content = generate_and_write_elle_core(CONTEXT_DIR, OUTPUT_PATH)
    line_count = len(content.split("\n"))
    print(f"Generated {OUTPUT_PATH} ({line_count} lines)")
    print(f"Synced from {CONTEXT_DIR}/core/")


if __name__ == "__main__":
    main()

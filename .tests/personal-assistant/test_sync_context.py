"""Tests for sync_context.py -- the elle-core.md generator."""
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "personal-assistant" / "skills" / "sync-context" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestExtractIdentitySummary:
    def test_extracts_basic_info(self, tmp_context):
        from sync_context import extract_identity_summary
        result = extract_identity_summary(tmp_context / "core" / "identity.md")
        assert "Test User" in result
        assert "California" in result

    def test_handles_missing_file(self, tmp_path):
        from sync_context import extract_identity_summary
        result = extract_identity_summary(tmp_path / "nonexistent.md")
        assert result == ""

    def test_stays_under_line_limit(self, tmp_context):
        from sync_context import extract_identity_summary
        result = extract_identity_summary(tmp_context / "core" / "identity.md")
        lines = [l for l in result.strip().split("\n") if l.strip()]
        assert len(lines) <= 10


class TestExtractPreferencesSummary:
    def test_extracts_preferences(self, tmp_context):
        from sync_context import extract_preferences_summary
        result = extract_preferences_summary(tmp_context / "core" / "preferences.md")
        assert "concise" in result.lower() or "bullet" in result.lower()

    def test_handles_missing_file(self, tmp_path):
        from sync_context import extract_preferences_summary
        result = extract_preferences_summary(tmp_path / "nonexistent.md")
        assert result == ""


class TestExtractRulesVerbatim:
    def test_extracts_all_rules(self, tmp_context):
        from sync_context import extract_rules_verbatim
        result = extract_rules_verbatim(tmp_context / "core" / "rules.md")
        assert "NEVER commit without asking" in result
        assert "ALWAYS run tests before pushing" in result
        assert "NEVER use echo $VAR to check secrets" in result

    def test_preserves_exact_wording(self, tmp_context):
        from sync_context import extract_rules_verbatim
        result = extract_rules_verbatim(tmp_context / "core" / "rules.md")
        assert "NEVER commit without asking" in result

    def test_handles_missing_file(self, tmp_path):
        from sync_context import extract_rules_verbatim
        result = extract_rules_verbatim(tmp_path / "nonexistent.md")
        assert result == ""

    def test_skips_xml_tags(self, tmp_path):
        """Both opening and closing guide/format tags should be filtered."""
        from sync_context import extract_rules_verbatim
        rules = tmp_path / "rules.md"
        rules.write_text(textwrap.dedent("""\
            ---
            name: Rules
            ---
            ## Rules
            <guide>Format instructions here</guide>
            - NEVER do bad things
            <format>| Column |</format>
            - ALWAYS do good things
        """))
        result = extract_rules_verbatim(rules)
        assert "</guide>" not in result
        assert "<guide>" not in result
        assert "</format>" not in result
        assert "NEVER do bad things" in result
        assert "ALWAYS do good things" in result


class TestExtractActiveProjects:
    def test_extracts_project_names(self, tmp_context):
        from sync_context import extract_active_projects
        result = extract_active_projects(tmp_context / "core" / "projects.md")
        assert "Project Alpha" in result
        assert "Project Beta" in result

    def test_includes_descriptions(self, tmp_context):
        from sync_context import extract_active_projects
        result = extract_active_projects(tmp_context / "core" / "projects.md")
        assert "Main product" in result

    def test_handles_missing_file(self, tmp_path):
        from sync_context import extract_active_projects
        result = extract_active_projects(tmp_path / "nonexistent.md")
        assert result == ""

    def test_skips_format_blocks(self, tmp_path):
        """Format blocks contain template headers that should not appear in output."""
        from sync_context import extract_active_projects
        projects = tmp_path / "projects.md"
        projects.write_text(textwrap.dedent("""\
            ## Active Projects
            <format>
            | Project | Location | Status | Key Notes |
            |---------|----------|--------|-----------|
            </format>
            | Project | Location | Status | Key Notes |
            |---------|----------|--------|-----------|
            | My App | ~/projects/app | Active | Main product |
        """))
        result = extract_active_projects(projects)
        assert "My App" in result
        # Table header row should not appear as a project entry
        assert result.count("Project") == 0 or "My App" in result
        lines = [l for l in result.strip().split("\n") if l.strip()]
        assert len(lines) == 1

    def test_skips_multiple_table_headers(self, tmp_path):
        """Multiple tables (Active, Milestones, Archived) should only yield data rows."""
        from sync_context import extract_active_projects
        projects = tmp_path / "projects.md"
        projects.write_text(textwrap.dedent("""\
            ## Active Projects
            | Project | Location | Status | Key Notes |
            |---------|----------|--------|-----------|
            | Basis | ~/projects/basis | Active | Core product |

            ## Upcoming Milestones
            | Date | Project | Milestone |
            |------|---------|-----------|
            | 2026-04-01 | Basis | Launch |

            ## Archived Projects
            | Project | Completed | Outcome |
            |---------|-----------|---------|
        """))
        result = extract_active_projects(projects)
        assert "Basis" in result
        assert "2026-04-01" in result
        # Header rows should not appear
        assert "Project -- Location" not in result
        assert "Date -- Project" not in result
        assert "Project -- Completed" not in result

    def test_skips_closing_guide_tags(self, tmp_path):
        """Closing </guide> tags should not leak into output."""
        from sync_context import extract_active_projects
        projects = tmp_path / "projects.md"
        projects.write_text(textwrap.dedent("""\
            ## Active Projects
            <guide>All active projects</guide>
            | Project | Location | Status |
            |---------|----------|--------|
            | My App | ~/app | Active |
        """))
        result = extract_active_projects(projects)
        assert "</guide>" not in result
        assert "<guide>" not in result


class TestGenerateElleCoreContent:
    def test_generates_valid_markdown(self, tmp_context):
        from sync_context import generate_elle_core_content
        result = generate_elle_core_content(tmp_context)
        assert result.startswith("# Elle")
        assert "## Identity" in result
        assert "## Communication Preferences" in result
        assert "## Rules" in result
        assert "## Active Projects" in result
        assert "## Loading Full Context" in result

    def test_includes_auto_generated_comment(self, tmp_context):
        from sync_context import generate_elle_core_content
        result = generate_elle_core_content(tmp_context)
        assert "Auto-generated by /sync-context" in result
        assert "Do not edit manually" in result

    def test_includes_timestamp(self, tmp_context):
        from sync_context import generate_elle_core_content
        result = generate_elle_core_content(tmp_context)
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in result

    def test_under_token_budget(self, tmp_context):
        from sync_context import generate_elle_core_content
        result = generate_elle_core_content(tmp_context)
        lines = result.split("\n")
        assert len(lines) <= 150

    def test_includes_context_loading_instructions(self, tmp_context):
        from sync_context import generate_elle_core_content
        result = generate_elle_core_content(tmp_context)
        assert "~/.claude/.context/core/" in result
        assert "identity.md" in result
        assert "relationships.md" in result


class TestWriteElleCoreFile:
    def test_writes_to_rules_dir(self, tmp_context, tmp_rules_dir):
        from sync_context import generate_and_write_elle_core
        output_path = tmp_rules_dir / "elle-core.md"
        generate_and_write_elle_core(tmp_context, output_path)
        assert output_path.exists()
        content = output_path.read_text()
        assert "# Elle" in content

    def test_overwrites_existing(self, tmp_context, tmp_rules_dir):
        from sync_context import generate_and_write_elle_core
        output_path = tmp_rules_dir / "elle-core.md"
        output_path.write_text("old content")
        generate_and_write_elle_core(tmp_context, output_path)
        content = output_path.read_text()
        assert "old content" not in content
        assert "# Elle" in content


class TestMainEntryPoint:
    def test_creates_elle_core_from_context(self, tmp_context, tmp_rules_dir):
        from sync_context import main as sync_main
        output_path = tmp_rules_dir / "elle-core.md"
        with patch("sync_context.CONTEXT_DIR", tmp_context), \
             patch("sync_context.OUTPUT_PATH", output_path):
            sync_main()
        assert output_path.exists()

    def test_reports_error_if_no_context(self, tmp_path, tmp_rules_dir, capsys):
        from sync_context import main as sync_main
        output_path = tmp_rules_dir / "elle-core.md"
        nonexistent = tmp_path / "nonexistent"
        with patch("sync_context.CONTEXT_DIR", nonexistent), \
             patch("sync_context.OUTPUT_PATH", output_path):
            with pytest.raises(SystemExit):
                sync_main()

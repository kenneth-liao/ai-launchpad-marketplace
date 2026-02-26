"""Tests for scheduler.py project-level SCHEDULER_DIR resolution.

Verifies that the scheduler correctly detects project roots via .git
or CLAUDE.md markers, and that the SCHEDULER_DIR env var takes priority.
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPT = str(
    Path(__file__).resolve().parents[1]
    / "scheduler"
    / "skills"
    / "manage"
    / "scripts"
    / "scheduler.py"
)


def run_scheduler_in_dir(
    cwd: str,
    args: list[str],
    *,
    env_override: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run scheduler.py from a specific working directory.

    Does NOT set SCHEDULER_DIR unless provided in env_override,
    allowing project root detection to kick in.
    """
    env = os.environ.copy()
    # Remove SCHEDULER_DIR so project detection is tested
    env.pop("SCHEDULER_DIR", None)
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    # Use a temp plist dir to avoid touching real LaunchAgents
    plist_dir = os.path.join(cwd, "plists")
    os.makedirs(plist_dir, exist_ok=True)
    env["SCHEDULER_PLIST_DIR"] = plist_dir
    if env_override:
        env.update(env_override)
    return subprocess.run(
        ["uv", "run", SCRIPT] + args,
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


def add_task_in_dir(cwd: str, task_id: str = "test-task", **kwargs):
    """Add a task to trigger registry creation."""
    return run_scheduler_in_dir(
        cwd,
        [
            "add",
            "--id", task_id,
            "--name", "Test Task",
            "--type", "prompt",
            "--target", "test prompt",
            "--cron", "0 9 * * *",
            "--working-directory", cwd,
        ],
        **kwargs,
    )


class TestProjectRootDetection:
    """Test that SCHEDULER_DIR resolves to project-level by default."""

    def test_git_marker_creates_project_level_scheduler_dir(self):
        """Running in a dir with .git creates scheduler dirs at <dir>/.claude/scheduler/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Resolve to handle macOS /var -> /private/var symlinks
            tmpdir_resolved = str(Path(tmpdir).resolve())
            # Create a .git marker
            os.makedirs(os.path.join(tmpdir_resolved, ".git"))

            # Use add to trigger full directory + registry creation
            result = add_task_in_dir(tmpdir_resolved)
            assert result.returncode == 0, f"add failed: {result.stderr}"

            # Registry should be at project-level
            registry_path = Path(tmpdir_resolved) / ".claude" / "scheduler" / "registry.json"
            assert registry_path.exists(), (
                f"Expected project-level registry at {registry_path}"
            )

            # Verify the task is in the registry
            with open(registry_path) as f:
                registry = json.load(f)
            assert "test-task" in registry["tasks"]

    def test_claude_md_marker_creates_project_level_scheduler_dir(self):
        """Running in a dir with CLAUDE.md creates scheduler dirs at <dir>/.claude/scheduler/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_resolved = str(Path(tmpdir).resolve())
            # Create a CLAUDE.md marker
            (Path(tmpdir_resolved) / "CLAUDE.md").write_text("# Project\n")

            result = add_task_in_dir(tmpdir_resolved)
            assert result.returncode == 0, f"add failed: {result.stderr}"

            registry_path = Path(tmpdir_resolved) / ".claude" / "scheduler" / "registry.json"
            assert registry_path.exists(), (
                f"Expected project-level registry at {registry_path}"
            )

    def test_env_var_overrides_project_detection(self):
        """SCHEDULER_DIR env var takes priority over project root detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_resolved = str(Path(tmpdir).resolve())
            project_dir = os.path.join(tmpdir_resolved, "project")
            override_dir = os.path.join(tmpdir_resolved, "override")
            os.makedirs(project_dir)
            os.makedirs(os.path.join(project_dir, ".git"))

            result = add_task_in_dir(
                project_dir,
                env_override={"SCHEDULER_DIR": override_dir},
            )
            assert result.returncode == 0, f"add failed: {result.stderr}"

            # Registry should be at the override location, NOT project-level
            override_registry = Path(override_dir) / "registry.json"
            project_registry = Path(project_dir) / ".claude" / "scheduler" / "registry.json"
            assert override_registry.exists(), (
                f"Expected registry at override dir {override_registry}"
            )
            assert not project_registry.exists(), (
                "Registry should NOT be created at project-level when SCHEDULER_DIR is set"
            )

    def test_subdirectory_finds_parent_project_root(self):
        """Running from a subdirectory still finds the project root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_resolved = str(Path(tmpdir).resolve())
            # Create .git at root
            os.makedirs(os.path.join(tmpdir_resolved, ".git"))
            # Create a subdirectory to run from
            subdir = os.path.join(tmpdir_resolved, "src", "deep", "nested")
            os.makedirs(subdir)

            result = add_task_in_dir(subdir)
            assert result.returncode == 0, f"add failed: {result.stderr}"

            # Registry should be at the project root, not the subdirectory
            registry_path = Path(tmpdir_resolved) / ".claude" / "scheduler" / "registry.json"
            assert registry_path.exists(), (
                f"Expected registry at project root {registry_path}"
            )
            # Should NOT be at the subdirectory level
            subdir_registry = Path(subdir) / ".claude" / "scheduler" / "registry.json"
            assert not subdir_registry.exists(), (
                "Registry should be at project root, not subdirectory"
            )

    def test_list_creates_scheduler_directories(self):
        """Even list (which doesn't write registry) creates the scheduler dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_resolved = str(Path(tmpdir).resolve())
            os.makedirs(os.path.join(tmpdir_resolved, ".git"))

            result = run_scheduler_in_dir(tmpdir_resolved, ["list"])
            assert result.returncode == 0, f"list failed: {result.stderr}"

            # Directories should exist at project-level
            scheduler_dir = Path(tmpdir_resolved) / ".claude" / "scheduler"
            assert scheduler_dir.exists(), (
                f"Expected scheduler directory at {scheduler_dir}"
            )
            assert (scheduler_dir / "wrappers").exists()
            assert (scheduler_dir / "logs").exists()
            assert (scheduler_dir / "results").exists()

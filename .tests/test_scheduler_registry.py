"""Tests for scheduler.py registry CRUD operations.

Uses a temporary directory as SCHEDULER_DIR and skips launchctl calls
via SCHEDULER_SKIP_LAUNCHCTL=1.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scheduler"
    / "skills"
    / "manage"
    / "scripts"
    / "scheduler.py"
)


def run_scheduler(tmpdir: str, args: list[str]) -> subprocess.CompletedProcess:
    """Run scheduler.py with the given args inside a temp SCHEDULER_DIR."""
    plist_dir = os.path.join(tmpdir, "plists")
    os.makedirs(plist_dir, exist_ok=True)
    env = os.environ.copy()
    env["SCHEDULER_DIR"] = tmpdir
    env["SCHEDULER_PLIST_DIR"] = plist_dir
    env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
    return subprocess.run(
        ["uv", "run", str(SCRIPT)] + args,
        capture_output=True,
        text=True,
        env=env,
    )


# ---------- helpers ----------


def add_default_task(
    tmpdir: str,
    *,
    task_id: str = "weekly-report",
    name: str = "Weekly Report",
    task_type: str = "skill",
    target: str = "generate-report",
    cron: str = "0 8 * * 1",
    workdir: str | None = None,
) -> subprocess.CompletedProcess:
    """Add a task with sensible defaults."""
    if workdir is None:
        workdir = tmpdir
    return run_scheduler(
        tmpdir,
        [
            "add",
            "--id",
            task_id,
            "--name",
            name,
            "--type",
            task_type,
            "--target",
            target,
            "--cron",
            cron,
            "--working-directory",
            workdir,
        ],
    )


# ---------- tests ----------


class TestSchedulerRegistry:
    """Test scheduler.py registry CRUD operations."""

    def test_list_empty(self):
        """list with no tasks returns empty array."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_scheduler(tmpdir, ["list"])
            assert result.returncode == 0
            data = json.loads(result.stdout)
            assert data == []

    def test_add_and_list(self):
        """add a task then list it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            add_result = add_default_task(tmpdir)
            assert add_result.returncode == 0, add_result.stderr
            add_data = json.loads(add_result.stdout)
            assert add_data["id"] == "weekly-report"
            assert add_data["status"] == "active"

            list_result = run_scheduler(tmpdir, ["list"])
            assert list_result.returncode == 0
            tasks = json.loads(list_result.stdout)
            assert len(tasks) == 1
            assert tasks[0]["id"] == "weekly-report"

    def test_add_duplicate_id_fails(self):
        """adding with existing ID returns error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            add_default_task(tmpdir)
            dup = add_default_task(tmpdir)
            assert dup.returncode != 0
            assert "already exists" in dup.stderr.lower()

    def test_add_invalid_cron_fails(self):
        """invalid cron expression returns error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = add_default_task(tmpdir, cron="not a cron")
            assert result.returncode != 0
            assert "cron" in result.stderr.lower() or "invalid" in result.stderr.lower()

    def test_get_existing(self):
        """get returns full task details."""
        with tempfile.TemporaryDirectory() as tmpdir:
            add_default_task(tmpdir)
            result = run_scheduler(tmpdir, ["get", "--id", "weekly-report"])
            assert result.returncode == 0
            data = json.loads(result.stdout)
            assert data["id"] == "weekly-report"
            assert data["name"] == "Weekly Report"
            assert data["type"] == "skill"
            assert data["target"] == "generate-report"
            assert data["schedule"]["cron"] == "0 8 * * 1"
            assert data["status"] == "active"
            assert data["last_run"] is None

    def test_get_nonexistent_fails(self):
        """get missing ID returns error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_scheduler(tmpdir, ["get", "--id", "nope"])
            assert result.returncode != 0
            assert "not found" in result.stderr.lower()

    def test_remove(self):
        """remove deletes from registry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            add_default_task(tmpdir)
            rm = run_scheduler(tmpdir, ["remove", "--id", "weekly-report"])
            assert rm.returncode == 0

            lst = run_scheduler(tmpdir, ["list"])
            tasks = json.loads(lst.stdout)
            assert len(tasks) == 0

    def test_remove_nonexistent_fails(self):
        """remove missing ID returns error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_scheduler(tmpdir, ["remove", "--id", "nope"])
            assert result.returncode != 0
            assert "not found" in result.stderr.lower()

    def test_update_last_run(self):
        """updates last_run field correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            add_default_task(tmpdir)
            upd = run_scheduler(
                tmpdir,
                [
                    "update-last-run",
                    "--id",
                    "weekly-report",
                    "--exit-code",
                    "0",
                    "--duration",
                    "94",
                    "--result-file",
                    "/tmp/result.md",
                ],
            )
            assert upd.returncode == 0
            data = json.loads(upd.stdout)
            assert data["last_run"]["exit_code"] == 0
            assert data["last_run"]["duration_seconds"] == 94
            assert data["last_run"]["result_file"] == "/tmp/result.md"
            assert data["status"] == "active"

    def test_add_all_three_types(self):
        """can add skill, prompt, and script types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for ttype, tid, target in [
                ("skill", "t-skill", "generate-report"),
                ("prompt", "t-prompt", "Summarize my inbox"),
                ("script", "t-script", "/usr/local/bin/cleanup.sh"),
            ]:
                res = add_default_task(
                    tmpdir, task_id=tid, task_type=ttype, target=target
                )
                assert res.returncode == 0, f"Failed for type={ttype}: {res.stderr}"
                data = json.loads(res.stdout)
                assert data["type"] == ttype

            lst = run_scheduler(tmpdir, ["list"])
            tasks = json.loads(lst.stdout)
            assert len(tasks) == 3

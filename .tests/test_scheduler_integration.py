"""Integration tests for scheduler.py — full add/list/remove lifecycle.

Exercises the complete task lifecycle and multi-task management in a
single temporary directory, using SCHEDULER_PLIST_DIR to redirect plist
output away from ~/Library/LaunchAgents/.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

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


def add_task(
    tmpdir: str,
    *,
    task_id: str,
    name: str = "Test Task",
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


class TestSchedulerIntegration:
    """Integration tests exercising the full scheduler lifecycle."""

    def test_full_lifecycle(self):
        """Full lifecycle: add -> list -> get -> pause -> resume -> update-last-run -> remove."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plist_dir = os.path.join(tmpdir, "plists")

            # --- ADD ---
            add_result = add_task(
                tmpdir,
                task_id="lifecycle-test",
                name="Lifecycle Test",
                task_type="skill",
                target="generate-report",
                cron="0 8 * * 1",
            )
            assert add_result.returncode == 0, add_result.stderr
            add_data = json.loads(add_result.stdout)
            assert add_data["id"] == "lifecycle-test"
            assert add_data["status"] == "active"

            # --- LIST ---
            list_result = run_scheduler(tmpdir, ["list"])
            assert list_result.returncode == 0
            tasks = json.loads(list_result.stdout)
            assert len(tasks) == 1

            # --- GET ---
            get_result = run_scheduler(tmpdir, ["get", "--id", "lifecycle-test"])
            assert get_result.returncode == 0
            get_data = json.loads(get_result.stdout)
            assert get_data["schedule"]["cron"] == "0 8 * * 1"
            assert "Monday" in get_data["schedule"]["human"]

            # --- Verify wrapper and plist files exist ---
            wrapper_path = Path(tmpdir) / "wrappers" / "lifecycle-test.sh"
            plist_path = Path(plist_dir) / "com.ailaunchpad.scheduler.lifecycle-test.plist"
            assert wrapper_path.exists(), f"Wrapper should exist at {wrapper_path}"
            assert plist_path.exists(), f"Plist should exist at {plist_path}"

            # --- PAUSE ---
            pause_result = run_scheduler(tmpdir, ["pause", "--id", "lifecycle-test"])
            assert pause_result.returncode == 0, pause_result.stderr
            pause_data = json.loads(pause_result.stdout)
            assert pause_data["status"] == "paused"

            # --- RESUME ---
            resume_result = run_scheduler(tmpdir, ["resume", "--id", "lifecycle-test"])
            assert resume_result.returncode == 0, resume_result.stderr
            resume_data = json.loads(resume_result.stdout)
            assert resume_data["status"] == "active"

            # --- UPDATE-LAST-RUN ---
            ulr_result = run_scheduler(
                tmpdir,
                [
                    "update-last-run",
                    "--id",
                    "lifecycle-test",
                    "--exit-code",
                    "0",
                    "--duration",
                    "60",
                    "--result-file",
                    "/tmp/result.md",
                ],
            )
            assert ulr_result.returncode == 0, ulr_result.stderr
            ulr_data = json.loads(ulr_result.stdout)
            assert ulr_data["last_run"]["exit_code"] == 0

            # --- REMOVE ---
            rm_result = run_scheduler(tmpdir, ["remove", "--id", "lifecycle-test"])
            assert rm_result.returncode == 0, rm_result.stderr

            # Verify list is empty
            list_after = run_scheduler(tmpdir, ["list"])
            tasks_after = json.loads(list_after.stdout)
            assert len(tasks_after) == 0

            # Verify wrapper and plist are deleted
            assert not wrapper_path.exists(), "Wrapper should be deleted after remove"
            assert not plist_path.exists(), "Plist should be deleted after remove"

    def test_multiple_tasks(self):
        """Add 3 tasks, pause one, remove another, verify final state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # --- Add 3 tasks ---
            for tid in ("task-a", "task-b", "task-c"):
                result = add_task(
                    tmpdir,
                    task_id=tid,
                    name=f"Task {tid[-1].upper()}",
                    task_type="prompt",
                    target=f"Run {tid}",
                    cron="0 9 * * *",
                )
                assert result.returncode == 0, f"Failed to add {tid}: {result.stderr}"

            # --- LIST: 3 tasks ---
            list_result = run_scheduler(tmpdir, ["list"])
            assert list_result.returncode == 0
            tasks = json.loads(list_result.stdout)
            assert len(tasks) == 3

            # --- PAUSE task-b ---
            pause_result = run_scheduler(tmpdir, ["pause", "--id", "task-b"])
            assert pause_result.returncode == 0, pause_result.stderr
            pause_data = json.loads(pause_result.stdout)
            assert pause_data["status"] == "paused"

            # --- REMOVE task-c ---
            rm_result = run_scheduler(tmpdir, ["remove", "--id", "task-c"])
            assert rm_result.returncode == 0, rm_result.stderr

            # --- LIST: 2 tasks, task-a active, task-b paused ---
            list_after = run_scheduler(tmpdir, ["list"])
            assert list_after.returncode == 0
            tasks_after = json.loads(list_after.stdout)
            assert len(tasks_after) == 2

            by_id = {t["id"]: t for t in tasks_after}
            assert "task-a" in by_id
            assert "task-b" in by_id
            assert "task-c" not in by_id
            assert by_id["task-a"]["status"] == "active"
            assert by_id["task-b"]["status"] == "paused"

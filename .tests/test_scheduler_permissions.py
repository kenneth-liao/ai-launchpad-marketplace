"""Tests for scheduler permission handling.

Covers:
- permission_presets.py: preset expansion, bypass detection, edge cases
- scheduler.py: CLI args, permissions field in task dict, preset resolution
- Wrapper generation: correct flags injected for various permission configs
- Backward compatibility: old tasks without permissions still work
- repair --force: regenerates all wrappers
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = str(
    Path(__file__).resolve().parents[1]
    / "scheduler"
    / "skills"
    / "manage"
    / "scripts"
    / "scheduler.py"
)

PRESETS_MODULE = str(
    Path(__file__).resolve().parents[1]
    / "scheduler"
    / "skills"
    / "manage"
    / "scripts"
)


class TestPermissionPresets(unittest.TestCase):
    """Unit tests for permission_presets.py."""

    @classmethod
    def setUpClass(cls):
        # Add the scripts directory to sys.path so we can import the module
        if PRESETS_MODULE not in sys.path:
            sys.path.insert(0, PRESETS_MODULE)

    def test_expand_readonly_preset(self):
        """readonly preset returns expected tools."""
        from permission_presets import expand_preset
        tools = expand_preset("readonly")
        self.assertIn("Read", tools)
        self.assertIn("Glob", tools)
        self.assertIn("Grep", tools)
        self.assertIn("WebSearch", tools)
        self.assertNotIn("Write", tools)
        self.assertNotIn("Edit", tools)

    def test_expand_full_edit_preset(self):
        """full-edit preset includes write tools."""
        from permission_presets import expand_preset
        tools = expand_preset("full-edit")
        self.assertIn("Read", tools)
        self.assertIn("Write", tools)
        self.assertIn("Edit", tools)
        self.assertIn("Bash(git *)", tools)

    def test_expand_research_preset(self):
        """research preset includes web tools and curl."""
        from permission_presets import expand_preset
        tools = expand_preset("research")
        self.assertIn("WebSearch", tools)
        self.assertIn("WebFetch", tools)
        self.assertIn("Bash(curl *)", tools)
        self.assertNotIn("Write", tools)

    def test_expand_bypass_returns_empty(self):
        """bypass preset returns an empty list (sentinel)."""
        from permission_presets import expand_preset
        tools = expand_preset("bypass")
        self.assertEqual(tools, [])

    def test_expand_unknown_preset_raises(self):
        """Unknown preset raises KeyError."""
        from permission_presets import expand_preset
        with self.assertRaises(KeyError):
            expand_preset("nonexistent")

    def test_is_bypass_preset(self):
        """is_bypass_preset returns True only for 'bypass'."""
        from permission_presets import is_bypass_preset
        self.assertTrue(is_bypass_preset("bypass"))
        self.assertFalse(is_bypass_preset("readonly"))
        self.assertFalse(is_bypass_preset("full-edit"))

    def test_expand_returns_copy(self):
        """expand_preset returns a copy, not a reference."""
        from permission_presets import expand_preset
        tools1 = expand_preset("readonly")
        tools2 = expand_preset("readonly")
        tools1.append("Custom")
        self.assertNotIn("Custom", tools2)

    def test_list_presets(self):
        """list_presets returns all available presets sorted."""
        from permission_presets import list_presets
        names = list_presets()
        self.assertEqual(names, ["bypass", "full-edit", "readonly", "research"])


class TestPermissionCLI(unittest.TestCase):
    """Integration tests for permission-related CLI args and task dict."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.plist_dir = os.path.join(self.tmpdir, "plists")
        os.makedirs(self.plist_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def run_scheduler(self, *args):
        env = os.environ.copy()
        env["SCHEDULER_DIR"] = self.tmpdir
        env["SCHEDULER_PLIST_DIR"] = self.plist_dir
        env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
        result = subprocess.run(
            ["uv", "run", SCRIPT] + list(args),
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout, result.stderr, result.returncode

    def add_task(self, task_id="perm-test", extra_args=None):
        """Add a task with optional extra args."""
        args = [
            "add",
            "--id", task_id,
            "--name", "Permission Test",
            "--type", "prompt",
            "--target", "test prompt",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        ]
        if extra_args:
            args.extend(extra_args)
        return self.run_scheduler(*args)

    # ------------------------------------------------------------------
    # Task dict tests
    # ------------------------------------------------------------------

    def test_no_permissions_by_default(self):
        """Task without permission args has permissions=None."""
        stdout, stderr, rc = self.add_task(task_id="no-perms")
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        self.assertIsNone(task["permissions"])

    def test_permission_preset_readonly(self):
        """--permission-preset readonly sets correct permissions."""
        stdout, stderr, rc = self.add_task(
            task_id="preset-ro",
            extra_args=["--permission-preset", "readonly"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        perms = task["permissions"]
        self.assertIsNotNone(perms)
        self.assertEqual(perms["preset"], "readonly")
        self.assertIn("Read", perms["allowed_tools"])
        self.assertIn("Glob", perms["allowed_tools"])
        self.assertNotIn("Write", perms["allowed_tools"])

    def test_permission_preset_bypass(self):
        """--permission-preset bypass sets bypassPermissions mode."""
        stdout, stderr, rc = self.add_task(
            task_id="preset-bypass",
            extra_args=["--permission-preset", "bypass"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        perms = task["permissions"]
        self.assertEqual(perms["permission_mode"], "bypassPermissions")
        self.assertIsNone(perms["allowed_tools"])

    def test_explicit_allowed_tools(self):
        """--allowed-tools sets the tool list directly."""
        stdout, stderr, rc = self.add_task(
            task_id="explicit-tools",
            extra_args=["--allowed-tools", "Read", "Write", "Bash(git *)"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        perms = task["permissions"]
        self.assertEqual(perms["allowed_tools"], ["Read", "Write", "Bash(git *)"])

    def test_permission_mode_alone(self):
        """--permission-mode sets the mode without tools."""
        stdout, stderr, rc = self.add_task(
            task_id="mode-only",
            extra_args=["--permission-mode", "acceptEdits"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        perms = task["permissions"]
        self.assertEqual(perms["permission_mode"], "acceptEdits")
        self.assertIsNone(perms["allowed_tools"])

    def test_preset_plus_extra_tools_merged(self):
        """Preset tools + explicit tools are merged and deduplicated."""
        stdout, stderr, rc = self.add_task(
            task_id="merge-test",
            extra_args=[
                "--permission-preset", "readonly",
                "--allowed-tools", "Read", "CustomTool",
            ],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        task = json.loads(stdout)
        tools = task["permissions"]["allowed_tools"]
        # Read from preset + CustomTool from explicit, no duplicates
        self.assertIn("Read", tools)
        self.assertIn("CustomTool", tools)
        self.assertEqual(tools.count("Read"), 1, "Read should not be duplicated")

    def test_bypass_warns_on_allowed_tools(self):
        """bypass preset with --allowed-tools emits warning."""
        stdout, stderr, rc = self.add_task(
            task_id="bypass-warn",
            extra_args=[
                "--permission-preset", "bypass",
                "--allowed-tools", "Read",
            ],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        self.assertIn("Warning", stderr)
        task = json.loads(stdout)
        self.assertIsNone(task["permissions"]["allowed_tools"])


class TestPermissionWrapperGeneration(unittest.TestCase):
    """Tests that wrapper scripts contain correct permission flags."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.plist_dir = os.path.join(self.tmpdir, "plists")
        os.makedirs(self.plist_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def run_scheduler(self, *args):
        env = os.environ.copy()
        env["SCHEDULER_DIR"] = self.tmpdir
        env["SCHEDULER_PLIST_DIR"] = self.plist_dir
        env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
        result = subprocess.run(
            ["uv", "run", SCRIPT] + list(args),
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout, result.stderr, result.returncode

    def add_task(self, task_id="wrap-test", extra_args=None):
        args = [
            "add",
            "--id", task_id,
            "--name", "Wrapper Perm Test",
            "--type", "prompt",
            "--target", "test prompt",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        ]
        if extra_args:
            args.extend(extra_args)
        return self.run_scheduler(*args)

    def read_wrapper(self, task_id):
        wrapper_path = Path(self.tmpdir) / "wrappers" / f"{task_id}.sh"
        return wrapper_path.read_text()

    # ------------------------------------------------------------------
    # Wrapper content tests
    # ------------------------------------------------------------------

    def test_no_permissions_empty_vars(self):
        """Wrapper without permissions has empty permission variables."""
        stdout, stderr, rc = self.add_task(task_id="no-perm-wrap")
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("no-perm-wrap")
        self.assertIn("ALLOWED_TOOLS=''", content)
        self.assertIn("PERMISSION_MODE=''", content)
        self.assertIn("SKIP_PERMISSIONS='false'", content)

    def test_readonly_preset_wrapper(self):
        """readonly preset produces ALLOWED_TOOLS with tool list."""
        stdout, stderr, rc = self.add_task(
            task_id="ro-wrap",
            extra_args=["--permission-preset", "readonly"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("ro-wrap")
        self.assertIn("ALLOWED_TOOLS='Read,Glob,Grep", content)
        self.assertIn("SKIP_PERMISSIONS='false'", content)

    def test_bypass_preset_wrapper(self):
        """bypass preset produces SKIP_PERMISSIONS='true'."""
        stdout, stderr, rc = self.add_task(
            task_id="bypass-wrap",
            extra_args=["--permission-preset", "bypass"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("bypass-wrap")
        self.assertIn("SKIP_PERMISSIONS='true'", content)
        self.assertIn("PERMISSION_MODE=''", content)
        # Should contain the --dangerously-skip-permissions flag builder
        self.assertIn("--dangerously-skip-permissions", content)

    def test_permission_mode_wrapper(self):
        """--permission-mode injects PERMISSION_MODE variable."""
        stdout, stderr, rc = self.add_task(
            task_id="mode-wrap",
            extra_args=["--permission-mode", "acceptEdits"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("mode-wrap")
        self.assertIn("PERMISSION_MODE='acceptEdits'", content)

    def test_wrapper_perm_args_in_claude_invocation(self):
        """Wrapper has ${PERM_ARGS[@]} in claude invocations."""
        stdout, stderr, rc = self.add_task(task_id="args-check")
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("args-check")
        # Both skill and prompt branches should have PERM_ARGS
        self.assertIn('${PERM_ARGS[@]}', content)

    def test_full_edit_tools_in_wrapper(self):
        """full-edit preset expands to correct tools in wrapper."""
        stdout, stderr, rc = self.add_task(
            task_id="full-edit-wrap",
            extra_args=["--permission-preset", "full-edit"],
        )
        self.assertEqual(rc, 0, f"add failed: {stderr}")
        content = self.read_wrapper("full-edit-wrap")
        # Check some specific tools from full-edit
        self.assertIn("Write", content.split("ALLOWED_TOOLS=")[1].split("\n")[0])
        self.assertIn("Edit", content.split("ALLOWED_TOOLS=")[1].split("\n")[0])
        self.assertIn("Bash(git *)", content.split("ALLOWED_TOOLS=")[1].split("\n")[0])


class TestPermissionBackwardCompatibility(unittest.TestCase):
    """Tests that old tasks without permissions still work correctly."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.plist_dir = os.path.join(self.tmpdir, "plists")
        os.makedirs(self.plist_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def run_scheduler(self, *args):
        env = os.environ.copy()
        env["SCHEDULER_DIR"] = self.tmpdir
        env["SCHEDULER_PLIST_DIR"] = self.plist_dir
        env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
        result = subprocess.run(
            ["uv", "run", SCRIPT] + list(args),
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout, result.stderr, result.returncode

    def test_old_task_without_permissions_generates_valid_wrapper(self):
        """Simulate an old task (no permissions key) via manual registry edit."""
        # Create a task normally first to set up directories
        self.run_scheduler(
            "add",
            "--id", "old-task",
            "--name", "Old Task",
            "--type", "prompt",
            "--target", "test",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        )

        # Manually remove the permissions key from the registry to simulate v1 task
        registry_path = Path(self.tmpdir) / "registry.json"
        registry = json.loads(registry_path.read_text())
        del registry["tasks"]["old-task"]["permissions"]
        registry_path.write_text(json.dumps(registry, indent=2))

        # Delete the wrapper so repair regenerates it
        wrapper_path = Path(self.tmpdir) / "wrappers" / "old-task.sh"
        wrapper_path.unlink()

        # Repair should regenerate without errors
        stdout, stderr, rc = self.run_scheduler("repair")
        self.assertEqual(rc, 0, f"repair failed: {stderr}")
        self.assertIn("Regenerated wrapper", stdout)

        # Wrapper should have empty permission vars
        content = wrapper_path.read_text()
        self.assertIn("ALLOWED_TOOLS=''", content)
        self.assertIn("PERMISSION_MODE=''", content)
        self.assertIn("SKIP_PERMISSIONS='false'", content)

    def test_old_task_list_and_get_still_work(self):
        """Tasks without permissions key can still be listed and fetched."""
        self.run_scheduler(
            "add",
            "--id", "compat-task",
            "--name", "Compat",
            "--type", "prompt",
            "--target", "test",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        )

        # Remove permissions from registry
        registry_path = Path(self.tmpdir) / "registry.json"
        registry = json.loads(registry_path.read_text())
        del registry["tasks"]["compat-task"]["permissions"]
        registry_path.write_text(json.dumps(registry, indent=2))

        # List should work
        stdout, stderr, rc = self.run_scheduler("list")
        self.assertEqual(rc, 0, f"list failed: {stderr}")
        tasks = json.loads(stdout)
        self.assertEqual(len(tasks), 1)

        # Get should work
        stdout, stderr, rc = self.run_scheduler("get", "--id", "compat-task")
        self.assertEqual(rc, 0, f"get failed: {stderr}")


class TestRepairForce(unittest.TestCase):
    """Tests for repair --force flag."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.plist_dir = os.path.join(self.tmpdir, "plists")
        os.makedirs(self.plist_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def run_scheduler(self, *args):
        env = os.environ.copy()
        env["SCHEDULER_DIR"] = self.tmpdir
        env["SCHEDULER_PLIST_DIR"] = self.plist_dir
        env["SCHEDULER_SKIP_LAUNCHCTL"] = "1"
        result = subprocess.run(
            ["uv", "run", SCRIPT] + list(args),
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout, result.stderr, result.returncode

    def test_repair_without_force_skips_existing_wrappers(self):
        """repair without --force does not regenerate existing wrappers."""
        self.run_scheduler(
            "add",
            "--id", "force-test",
            "--name", "Force Test",
            "--type", "prompt",
            "--target", "test",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        )
        stdout, stderr, rc = self.run_scheduler("repair")
        self.assertEqual(rc, 0)
        self.assertIn("no issues found", stdout)

    def test_repair_force_regenerates_all_wrappers(self):
        """repair --force regenerates wrappers even if they exist."""
        self.run_scheduler(
            "add",
            "--id", "force-regen",
            "--name", "Force Regen",
            "--type", "prompt",
            "--target", "test",
            "--cron", "0 9 * * *",
            "--working-directory", self.tmpdir,
        )

        # Get original wrapper mtime
        wrapper_path = Path(self.tmpdir) / "wrappers" / "force-regen.sh"
        original_content = wrapper_path.read_text()

        # Add permissions to the registry manually
        registry_path = Path(self.tmpdir) / "registry.json"
        registry = json.loads(registry_path.read_text())
        registry["tasks"]["force-regen"]["permissions"] = {
            "allowed_tools": ["Read", "Glob"],
            "permission_mode": None,
            "preset": "readonly",
        }
        registry_path.write_text(json.dumps(registry, indent=2))

        # Force repair
        stdout, stderr, rc = self.run_scheduler("repair", "--force")
        self.assertEqual(rc, 0, f"repair --force failed: {stderr}")
        self.assertIn("Force-regenerated wrapper", stdout)

        # Wrapper should now contain the permissions
        new_content = wrapper_path.read_text()
        self.assertNotEqual(original_content, new_content)
        self.assertIn("Read,Glob", new_content)

    def test_repair_force_with_multiple_tasks(self):
        """repair --force regenerates wrappers for all active tasks."""
        for i in range(3):
            self.run_scheduler(
                "add",
                "--id", f"multi-{i}",
                "--name", f"Multi {i}",
                "--type", "prompt",
                "--target", "test",
                "--cron", "0 9 * * *",
                "--working-directory", self.tmpdir,
            )

        # Pause one task — should not be regenerated
        self.run_scheduler("pause", "--id", "multi-1")

        stdout, stderr, rc = self.run_scheduler("repair", "--force")
        self.assertEqual(rc, 0, f"repair --force failed: {stderr}")
        # Should regenerate 2 wrappers (active tasks only)
        self.assertEqual(stdout.count("Force-regenerated wrapper"), 2)


if __name__ == "__main__":
    unittest.main()

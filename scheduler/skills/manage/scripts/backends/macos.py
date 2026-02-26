"""macOS backend — launchd plist generation and launchctl interaction."""

from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path

from backends.base import PlatformBackend


# ---------------------------------------------------------------------------
# Plist helpers (moved from scheduler.py)
# ---------------------------------------------------------------------------


def _cron_to_calendar_interval(expr: str) -> list[dict]:
    """Convert a 5-field cron expression to a list of StartCalendarInterval dicts.

    Each dict may contain: Minute, Hour, Day, Month, Weekday.
    Wildcard fields are omitted (meaning "every").
    Supports step syntax (e.g. ``*/2``, ``1-30/5``) and comma-separated lists.
    Produces the Cartesian product of all multi-value fields so that
    launchd fires at every specified combination.
    """
    parts = expr.split()
    minute, hour, dom, month, dow = parts

    # Ranges used for expanding step syntax against wildcards
    FIELD_RANGES: dict[str, tuple[int, int]] = {
        "minute": (0, 59),
        "hour": (0, 23),
        "dom": (1, 31),
        "month": (1, 12),
        "dow": (0, 6),
    }

    def _parse_field(field: str, field_name: str) -> list[int] | None:
        """Parse a single cron field into a sorted list of ints, or None for '*'."""
        if field == "*":
            return None
        nums: list[int] = []
        for part in field.split(","):
            # Handle step syntax: */N or A-B/N
            if "/" in part:
                range_part, step_str = part.split("/", 1)
                step = int(step_str)
                if range_part == "*":
                    lo, hi = FIELD_RANGES[field_name]
                elif "-" in range_part:
                    lo_s, hi_s = range_part.split("-", 1)
                    lo, hi = int(lo_s), int(hi_s)
                else:
                    lo = int(range_part)
                    hi = FIELD_RANGES[field_name][1]
                nums.extend(range(lo, hi + 1, step))
            elif "-" in part:
                lo, hi = part.split("-", 1)
                nums.extend(range(int(lo), int(hi) + 1))
            else:
                nums.append(int(part))
        return sorted(set(nums))

    minute_vals = _parse_field(minute, "minute")
    hour_vals = _parse_field(hour, "hour")
    dom_vals = _parse_field(dom, "dom")
    month_vals = _parse_field(month, "month")
    dow_vals = _parse_field(dow, "dow")

    # Build the Cartesian product of all multi-value fields.
    # Fields that are None (wildcard) are omitted from the dict, which
    # tells launchd "every value" for that field.
    field_specs: list[tuple[str, list[int] | None]] = [
        ("Minute", minute_vals),
        ("Hour", hour_vals),
        ("Day", dom_vals),
        ("Month", month_vals),
        ("Weekday", dow_vals),
    ]

    intervals: list[dict] = [{}]
    for key, vals in field_specs:
        if vals is None:
            continue  # wildcard — omit from dict
        expanded: list[dict] = []
        for existing in intervals:
            for v in vals:
                entry = dict(existing)
                entry[key] = v
                expanded.append(entry)
        intervals = expanded

    return intervals if intervals else [{}]


def _interval_to_plist_xml(interval: dict) -> str:
    """Render a single StartCalendarInterval dict as plist XML."""
    lines = ["        <dict>"]
    for key in ("Minute", "Hour", "Day", "Month", "Weekday"):
        if key in interval:
            lines.append(f"            <key>{key}</key>")
            lines.append(f"            <integer>{interval[key]}</integer>")
    lines.append("        </dict>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MacOS Backend
# ---------------------------------------------------------------------------

# Template path relative to this file:
#   backends/macos.py -> scripts/backends/
#   -> scripts/ -> manage/ -> references/wrapper-template.sh
_BACKEND_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _BACKEND_DIR.parent
_SKILL_DIR = _SCRIPTS_DIR.parent
_TEMPLATE_PATH = _SKILL_DIR / "references" / "wrapper-template.sh"


class MacOSBackend(PlatformBackend):
    """macOS backend using launchd (plist files + launchctl)."""

    def __init__(self) -> None:
        self.plist_dir = Path(
            os.environ.get(
                "SCHEDULER_PLIST_DIR",
                str(Path.home() / "Library" / "LaunchAgents"),
            )
        )
        self.plist_prefix = "com.ailaunchpad.scheduler"
        self._skip = (
            os.environ.get("SCHEDULER_SKIP_LAUNCHCTL", "0") == "1"
            or os.environ.get("SCHEDULER_SKIP_PLATFORM", "0") == "1"
        )
        self.template_path = _TEMPLATE_PATH

    # --- Internal helpers ---

    def _plist_path(self, task_id: str) -> Path:
        """Return the plist path for a given task ID."""
        return self.plist_dir / f"{self.plist_prefix}.{task_id}.plist"

    def _launchctl_load(self, plist_path: Path) -> None:
        """Load a plist via launchctl. Skipped when skip_scheduling is True."""
        if self._skip:
            return
        uid = os.getuid()
        result = subprocess.run(
            ["launchctl", "bootstrap", f"gui/{uid}", str(plist_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Fallback to legacy load
            subprocess.run(
                ["launchctl", "load", str(plist_path)],
                capture_output=True,
                text=True,
            )

    def _launchctl_unload(self, plist_path: Path) -> None:
        """Unload a plist via launchctl. Skipped when skip_scheduling is True."""
        if self._skip:
            return
        uid = os.getuid()
        label = plist_path.stem  # e.g. com.ailaunchpad.scheduler.my-task
        result = subprocess.run(
            ["launchctl", "bootout", f"gui/{uid}/{label}"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Fallback to legacy unload
            subprocess.run(
                ["launchctl", "unload", str(plist_path)],
                capture_output=True,
                text=True,
            )

    # --- PlatformBackend implementation ---

    def install_schedule(
        self,
        task_id: str,
        task: dict,
        wrapper_path: Path,
        scheduler_dir: Path,
        logs_dir: Path,
    ) -> None:
        """Generate a LaunchAgent plist and load it via launchctl."""
        cron_expr = task["schedule"]["cron"]
        intervals = _cron_to_calendar_interval(cron_expr)

        # Build StartCalendarInterval block
        if len(intervals) == 1:
            cal_block = (
                f"    <key>StartCalendarInterval</key>\n"
                f"{_interval_to_plist_xml(intervals[0])}"
            )
        else:
            inner = "\n".join(_interval_to_plist_xml(iv) for iv in intervals)
            cal_block = (
                f"    <key>StartCalendarInterval</key>\n"
                f"    <array>\n{inner}\n    </array>"
            )

        label = f"{self.plist_prefix}.{task_id}"
        stdout_log = str(logs_dir / f"{task_id}.stdout.log")
        stderr_log = str(logs_dir / f"{task_id}.stderr.log")

        plist_xml = textwrap.dedent(f"""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
              "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>Label</key>
                <string>{label}</string>
                <key>ProgramArguments</key>
                <array>
                    <string>/bin/bash</string>
                    <string>{wrapper_path}</string>
                </array>
            {cal_block}
                <key>StandardOutPath</key>
                <string>{stdout_log}</string>
                <key>StandardErrorPath</key>
                <string>{stderr_log}</string>
            </dict>
            </plist>
        """)

        self.plist_dir.mkdir(parents=True, exist_ok=True)
        plist_path = self._plist_path(task_id)
        plist_path.write_text(plist_xml)
        self._launchctl_load(plist_path)

    def uninstall_schedule(self, task_id: str) -> None:
        """Unload from launchd and delete the plist file."""
        plist_path = self._plist_path(task_id)
        if plist_path.exists():
            self._launchctl_unload(plist_path)
            plist_path.unlink()

    def load_schedule(self, task_id: str) -> None:
        """Load an existing plist into launchd (for resume)."""
        plist_path = self._plist_path(task_id)
        if plist_path.exists():
            self._launchctl_load(plist_path)

    def unload_schedule(self, task_id: str) -> None:
        """Unload a plist from launchd without deleting it (for pause/complete)."""
        plist_path = self._plist_path(task_id)
        if plist_path.exists():
            self._launchctl_unload(plist_path)

    def schedule_artifact_exists(self, task_id: str) -> bool:
        """Check whether the plist file exists."""
        return self._plist_path(task_id).exists()

    def generate_wrapper(
        self,
        task: dict,
        scheduler_dir: Path,
        scheduler_py_path: Path,
        wrappers_dir: Path,
    ) -> Path:
        """Generate a bash wrapper script from the macOS template."""
        template = self.template_path.read_text()

        # Escape single quotes in target since it's enclosed in single quotes
        escaped_target = task["target"].replace("'", "'\\''")

        wrapper = template.replace("{id}", task["id"])
        wrapper = wrapper.replace("{type}", task["type"])
        wrapper = wrapper.replace("{target}", escaped_target)
        wrapper = wrapper.replace("{max_turns}", str(task["safety"]["max_turns"]))
        wrapper = wrapper.replace(
            "{timeout_minutes}", str(task["safety"]["timeout_minutes"])
        )
        wrapper = wrapper.replace("{working_directory}", task["working_directory"])
        wrapper = wrapper.replace(
            "{run_once}", "true" if task.get("run_once") else "false"
        )
        wrapper = wrapper.replace("{scheduler_py}", str(scheduler_py_path))
        wrapper = wrapper.replace("{scheduler_dir}", str(scheduler_dir.resolve()))
        wrapper = wrapper.replace(
            "{output_directory}", task.get("output_directory") or ""
        )

        # Permission flags
        permissions = task.get("permissions") or {}
        allowed_tools = ",".join(permissions.get("allowed_tools") or [])
        permission_mode = permissions.get("permission_mode") or ""
        skip_perms = "true" if permission_mode == "bypassPermissions" else "false"
        if skip_perms == "true":
            permission_mode = ""  # The flag is standalone

        wrapper = wrapper.replace("{allowed_tools}", allowed_tools)
        wrapper = wrapper.replace("{permission_mode}", permission_mode)
        wrapper = wrapper.replace("{skip_permissions}", skip_perms)

        wrappers_dir.mkdir(parents=True, exist_ok=True)
        wrapper_path = wrappers_dir / f"{task['id']}{self.wrapper_extension()}"
        wrapper_path.write_text(wrapper)
        wrapper_path.chmod(0o755)
        return wrapper_path

    def wrapper_extension(self) -> str:
        return ".sh"

    def run_wrapper(self, wrapper_path: Path) -> int:
        """Execute a wrapper script via /bin/bash."""
        result = subprocess.run(
            ["/bin/bash", str(wrapper_path)],
            capture_output=False,
        )
        return result.returncode

    def skip_scheduling(self) -> bool:
        return self._skip

    def default_schedule_dir(self) -> Path:
        return Path.home() / "Library" / "LaunchAgents"

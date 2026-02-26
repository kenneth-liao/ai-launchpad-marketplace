"""Windows backend — Task Scheduler via schtasks.exe with XML import."""

from __future__ import annotations

import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

from backends.base import PlatformBackend


# ---------------------------------------------------------------------------
# Cron-to-Task Scheduler trigger conversion
# ---------------------------------------------------------------------------

# Cron DOW (0=Sunday) to Task Scheduler DaysOfWeek bitmask values
_SCHTASK_DOW_BITS = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}

# Months for MonthsOfYear element
_MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


def _parse_cron_field(field: str, lo: int, hi: int) -> list[int] | None:
    """Parse a single cron field into a sorted list of ints, or None for '*'."""
    if field == "*":
        return None
    nums: list[int] = []
    for part in field.split(","):
        if "/" in part:
            range_part, step_str = part.split("/", 1)
            step = int(step_str)
            if range_part == "*":
                r_lo, r_hi = lo, hi
            elif "-" in range_part:
                r_lo_s, r_hi_s = range_part.split("-", 1)
                r_lo, r_hi = int(r_lo_s), int(r_hi_s)
            else:
                r_lo = int(range_part)
                r_hi = hi
            nums.extend(range(r_lo, r_hi + 1, step))
        elif "-" in part:
            a, b = part.split("-", 1)
            nums.extend(range(int(a), int(b) + 1))
        else:
            nums.append(int(part))
    return sorted(set(nums))


def cron_to_schtask_triggers(expr: str) -> list[dict]:
    """Convert a 5-field cron expression to Task Scheduler trigger specs.

    Returns a list of trigger dicts, each with:
        - type: 'daily' | 'weekly' | 'monthly' | 'time' (repetition-based)
        - start_time: 'HH:MM:SS'
        - repetition_interval: (optional) e.g. 'PT5M' for every-5-minutes
        - days_of_week: (optional) list of day names
        - days_of_month: (optional) list of ints
        - months: (optional) list of month names
    """
    parts = expr.split()
    minute, hour, dom, month, dow = parts

    minute_vals = _parse_cron_field(minute, 0, 59)
    hour_vals = _parse_cron_field(hour, 0, 23)
    dom_vals = _parse_cron_field(dom, 1, 31)
    month_vals = _parse_cron_field(month, 1, 12)
    dow_vals = _parse_cron_field(dow, 0, 6)

    triggers = []

    # Determine if this is a repetition pattern (*/N minutes or hours)
    if minute.startswith("*/") and hour == "*" and dom == "*" and month == "*" and dow == "*":
        step = int(minute[2:])
        triggers.append({
            "type": "time",
            "start_time": "00:00:00",
            "repetition_interval": f"PT{step}M",
            "repetition_duration": "P1D",
        })
        return triggers

    if hour.startswith("*/") and dom == "*" and month == "*" and dow == "*":
        step = int(hour[2:])
        m = minute_vals[0] if minute_vals else 0
        triggers.append({
            "type": "time",
            "start_time": f"{m:02d}:00:00",  # not quite right but close
            "repetition_interval": f"PT{step}H",
            "repetition_duration": "P1D",
        })
        return triggers

    # Build start times from hour/minute combinations
    hours = hour_vals if hour_vals else [0]
    minutes = minute_vals if minute_vals else [0]
    start_times = [f"{h:02d}:{m:02d}:00" for h in hours for m in minutes]

    for start_time in start_times:
        if dow_vals is not None:
            # Weekly trigger
            triggers.append({
                "type": "weekly",
                "start_time": start_time,
                "days_of_week": [_SCHTASK_DOW_BITS[d] for d in dow_vals],
            })
        elif dom_vals is not None:
            # Monthly trigger
            trigger = {
                "type": "monthly",
                "start_time": start_time,
                "days_of_month": dom_vals,
            }
            if month_vals:
                trigger["months"] = [_MONTH_NAMES[m] for m in month_vals]
            triggers.append(trigger)
        else:
            # Daily trigger
            triggers.append({
                "type": "daily",
                "start_time": start_time,
            })

    return triggers


def generate_task_xml(
    task_id: str,
    wrapper_path: Path,
    triggers: list[dict],
    timeout_minutes: int = 15,
) -> str:
    """Generate a Windows Task Scheduler XML definition.

    Returns well-formed XML string compatible with schtasks /Create /XML.
    """
    NS = "http://schemas.microsoft.com/windows/2004/02/mit/task"

    task = ET.Element("Task", {
        "version": "1.2",
        "xmlns": NS,
    })

    # RegistrationInfo
    reg = ET.SubElement(task, "RegistrationInfo")
    desc = ET.SubElement(reg, "Description")
    desc.text = f"AI Launchpad Scheduler: {task_id}"

    # Triggers
    triggers_el = ET.SubElement(task, "Triggers")
    for trig in triggers:
        if trig["type"] == "daily":
            cal = ET.SubElement(triggers_el, "CalendarTrigger")
            sb = ET.SubElement(cal, "StartBoundary")
            sb.text = f"2025-01-01T{trig['start_time']}"
            ET.SubElement(cal, "Enabled").text = "true"
            sbd = ET.SubElement(cal, "ScheduleByDay")
            ET.SubElement(sbd, "DaysInterval").text = "1"

        elif trig["type"] == "weekly":
            cal = ET.SubElement(triggers_el, "CalendarTrigger")
            sb = ET.SubElement(cal, "StartBoundary")
            sb.text = f"2025-01-01T{trig['start_time']}"
            ET.SubElement(cal, "Enabled").text = "true"
            sbw = ET.SubElement(cal, "ScheduleByWeek")
            dow_el = ET.SubElement(sbw, "DaysOfWeek")
            for day_name in trig["days_of_week"]:
                ET.SubElement(dow_el, day_name)
            ET.SubElement(sbw, "WeeksInterval").text = "1"

        elif trig["type"] == "monthly":
            cal = ET.SubElement(triggers_el, "CalendarTrigger")
            sb = ET.SubElement(cal, "StartBoundary")
            sb.text = f"2025-01-01T{trig['start_time']}"
            ET.SubElement(cal, "Enabled").text = "true"
            sbm = ET.SubElement(cal, "ScheduleByMonth")
            dom_el = ET.SubElement(sbm, "DaysOfMonth")
            for d in trig["days_of_month"]:
                ET.SubElement(dom_el, "Day").text = str(d)
            months_el = ET.SubElement(sbm, "Months")
            month_list = trig.get("months", list(_MONTH_NAMES.values()))
            for m in month_list:
                ET.SubElement(months_el, m)

        elif trig["type"] == "time":
            tt = ET.SubElement(triggers_el, "TimeTrigger")
            sb = ET.SubElement(tt, "StartBoundary")
            sb.text = f"2025-01-01T{trig['start_time']}"
            ET.SubElement(tt, "Enabled").text = "true"
            rep = ET.SubElement(tt, "Repetition")
            ET.SubElement(rep, "Interval").text = trig["repetition_interval"]
            ET.SubElement(rep, "Duration").text = trig.get("repetition_duration", "P1D")
            ET.SubElement(rep, "StopAtDurationEnd").text = "false"

    # Principals
    principals = ET.SubElement(task, "Principals")
    principal = ET.SubElement(principals, "Principal", {"id": "Author"})
    ET.SubElement(principal, "LogonType").text = "InteractiveToken"
    ET.SubElement(principal, "RunLevel").text = "LeastPrivilege"

    # Settings
    settings = ET.SubElement(task, "Settings")
    ET.SubElement(settings, "MultipleInstancesPolicy").text = "IgnoreNew"
    ET.SubElement(settings, "DisallowStartIfOnBatteries").text = "false"
    ET.SubElement(settings, "StopIfGoingOnBatteries").text = "false"
    ET.SubElement(settings, "StartWhenAvailable").text = "true"
    ET.SubElement(settings, "RunOnlyIfNetworkAvailable").text = "false"
    ET.SubElement(settings, "Enabled").text = "true"
    ET.SubElement(settings, "Hidden").text = "false"
    if timeout_minutes > 0:
        ET.SubElement(settings, "ExecutionTimeLimit").text = f"PT{timeout_minutes}M"

    # Actions
    actions = ET.SubElement(task, "Actions", {"Context": "Author"})
    exec_el = ET.SubElement(actions, "Exec")
    ET.SubElement(exec_el, "Command").text = "powershell.exe"
    ET.SubElement(exec_el, "Arguments").text = (
        f"-ExecutionPolicy Bypass -File \"{wrapper_path}\""
    )

    # Pretty print
    rough_string = ET.tostring(task, encoding="unicode", xml_declaration=False)
    # Add XML declaration
    xml_str = f'<?xml version="1.0" encoding="UTF-16"?>\n{rough_string}'
    try:
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ", encoding=None)
    except Exception:
        return xml_str


# ---------------------------------------------------------------------------
# Windows Backend
# ---------------------------------------------------------------------------

_BACKEND_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _BACKEND_DIR.parent
_SKILL_DIR = _SCRIPTS_DIR.parent
_TEMPLATE_PATH = _SKILL_DIR / "references" / "wrapper-template.ps1"

_TASK_FOLDER = "\\AILaunchpad\\Scheduler"


class WindowsBackend(PlatformBackend):
    """Windows backend using Task Scheduler (schtasks.exe)."""

    def __init__(self) -> None:
        self._skip = (
            os.environ.get("SCHEDULER_SKIP_SCHTASKS", "0") == "1"
            or os.environ.get("SCHEDULER_SKIP_PLATFORM", "0") == "1"
        )
        self.template_path = _TEMPLATE_PATH
        # Directory for storing task XML files (for repair/debugging)
        self.xml_dir: Path | None = None

    def _task_name(self, task_id: str) -> str:
        """Return the full Task Scheduler task name."""
        return f"{_TASK_FOLDER}\\{task_id}"

    def _xml_path(self, task_id: str) -> Path | None:
        """Return the path to a stored XML file, if xml_dir is set."""
        if self.xml_dir:
            return self.xml_dir / f"{task_id}.xml"
        return None

    def _schtasks(self, *args: str) -> subprocess.CompletedProcess:
        """Run schtasks.exe with the given args."""
        return subprocess.run(
            ["schtasks.exe", *args],
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
        """Generate Task Scheduler XML and import via schtasks."""
        cron_expr = task["schedule"]["cron"]
        timeout = task.get("safety", {}).get("timeout_minutes", 15)
        triggers = cron_to_schtask_triggers(cron_expr)
        xml_content = generate_task_xml(task_id, wrapper_path, triggers, timeout)

        # Store XML for repair/debugging
        self.xml_dir = scheduler_dir / "schtasks_xml"
        self.xml_dir.mkdir(parents=True, exist_ok=True)
        xml_path = self._xml_path(task_id)
        if xml_path:
            xml_path.write_text(xml_content, encoding="utf-16")

        if not self._skip and xml_path:
            self._schtasks(
                "/Create",
                "/XML", str(xml_path),
                "/TN", self._task_name(task_id),
                "/F",
            )

    def uninstall_schedule(self, task_id: str) -> None:
        """Delete the scheduled task and its XML file."""
        if not self._skip:
            self._schtasks("/Delete", "/TN", self._task_name(task_id), "/F")

        xml_path = self._xml_path(task_id)
        if xml_path and xml_path.exists():
            xml_path.unlink()

    def load_schedule(self, task_id: str) -> None:
        """Re-enable the scheduled task (for resume)."""
        if not self._skip:
            self._schtasks("/Change", "/TN", self._task_name(task_id), "/ENABLE")

    def unload_schedule(self, task_id: str) -> None:
        """Disable the scheduled task (for pause/complete)."""
        if not self._skip:
            self._schtasks("/Change", "/TN", self._task_name(task_id), "/DISABLE")

    def schedule_artifact_exists(self, task_id: str) -> bool:
        """Check whether the task XML file exists."""
        xml_path = self._xml_path(task_id)
        if xml_path:
            return xml_path.exists()
        # If no xml_dir, check via schtasks query
        if not self._skip:
            result = self._schtasks("/Query", "/TN", self._task_name(task_id))
            return result.returncode == 0
        return False

    def generate_wrapper(
        self,
        task: dict,
        scheduler_dir: Path,
        scheduler_py_path: Path,
        wrappers_dir: Path,
    ) -> Path:
        """Generate a PowerShell wrapper script from the Windows template."""
        template = self.template_path.read_text()

        # PowerShell uses different quoting — escape single quotes by doubling
        escaped_target = task["target"].replace("'", "''")

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

        # Permission flags (escape single quotes for PowerShell)
        permissions = task.get("permissions") or {}
        allowed_tools = ",".join(permissions.get("allowed_tools") or [])
        permission_mode = permissions.get("permission_mode") or ""
        skip_perms = "true" if permission_mode == "bypassPermissions" else "false"
        if skip_perms == "true":
            permission_mode = ""  # The flag is standalone

        wrapper = wrapper.replace("{allowed_tools}", allowed_tools.replace("'", "''"))
        wrapper = wrapper.replace("{permission_mode}", permission_mode)
        wrapper = wrapper.replace("{skip_permissions}", skip_perms)

        wrappers_dir.mkdir(parents=True, exist_ok=True)
        wrapper_path = wrappers_dir / f"{task['id']}{self.wrapper_extension()}"
        wrapper_path.write_text(wrapper)
        # No chmod needed on Windows — PowerShell scripts don't need +x
        return wrapper_path

    def wrapper_extension(self) -> str:
        return ".ps1"

    def run_wrapper(self, wrapper_path: Path) -> int:
        """Execute a wrapper script via PowerShell."""
        result = subprocess.run(
            [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", str(wrapper_path),
            ],
            capture_output=False,
        )
        return result.returncode

    def skip_scheduling(self) -> bool:
        return self._skip

    def default_schedule_dir(self) -> Path:
        # Windows doesn't have a standard user service directory;
        # XML files are stored alongside the scheduler data
        return Path.home() / ".claude" / "scheduler" / "schtasks_xml"

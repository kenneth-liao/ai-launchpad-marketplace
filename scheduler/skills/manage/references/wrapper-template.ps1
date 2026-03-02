# PowerShell wrapper for AI Launchpad Scheduler
# Equivalent of wrapper-template.sh for Windows
$ErrorActionPreference = "Stop"

# --- Config (injected by scheduler.py) ---
$TASK_ID = "{id}"
$TASK_TYPE = "{type}"
$TASK_TARGET = '{target}'
$MAX_TURNS = {max_turns}
$TIMEOUT_MINUTES = {timeout_minutes}
$WORKDIR = "{working_directory}"
$RUN_ONCE = "{run_once}"
$SCHEDULER_PY = "{scheduler_py}"
$ALLOWED_TOOLS = '{allowed_tools}'
$PERMISSION_MODE = '{permission_mode}'
$SKIP_PERMISSIONS = '{skip_permissions}'

# --- Environment ---
# Optional: load API key if available (not required for subscription auth)
try {
    # Try Windows Credential Manager via cmdkey
    $credOutput = cmdkey /list:anthropic-api-key 2>$null
    if ($credOutput -match "Password") {
        # Use PowerShell SecretManagement if available
        try {
            $secret = Get-Secret -Name 'anthropic-api-key' -AsPlainText -ErrorAction Stop
            $env:ANTHROPIC_API_KEY = $secret
        } catch {
            # Fall back to file-based key
            $keyFile = Join-Path $env:USERPROFILE ".config\anthropic\api-key"
            if (Test-Path $keyFile) {
                $env:ANTHROPIC_API_KEY = (Get-Content $keyFile -Raw).Trim()
            }
        }
    }
} catch {
    # File fallback
    $keyFile = Join-Path $env:USERPROFILE ".config\anthropic\api-key"
    if (Test-Path $keyFile) {
        $env:ANTHROPIC_API_KEY = (Get-Content $keyFile -Raw).Trim()
    }
}

# --- Session ID for Claude Code JSONL log tracking ---
$SESSION_ID = [guid]::NewGuid().ToString()

# --- Paths ---
$SCHEDULER_DIR = "{scheduler_dir}"
$OUTPUT_DIR = "{output_directory}"

$DATE = Get-Date -Format "yyyy-MM-dd"
$TIMESTAMP = Get-Date -Format "HHmmss"
if ($OUTPUT_DIR) {
    $RESULT_DIR = $OUTPUT_DIR
    $RESULT_FILE = Join-Path $RESULT_DIR "$TASK_ID.md"
} else {
    $RESULT_DIR = Join-Path $SCHEDULER_DIR "results\$DATE"
    $RESULT_FILE = Join-Path $RESULT_DIR "$TASK_ID-$TIMESTAMP.md"
}
$LOG_FILE = Join-Path $SCHEDULER_DIR "logs\$DATE\$TASK_ID.log"
$LOCK_FILE = Join-Path $SCHEDULER_DIR ".lock-$TASK_ID"

# Create directories
New-Item -ItemType Directory -Force -Path $RESULT_DIR | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $LOG_FILE) | Out-Null

# --- Lock: skip if already running ---
if (Test-Path $LOCK_FILE) {
    $lockPid = Get-Content $LOCK_FILE -ErrorAction SilentlyContinue
    if ($lockPid) {
        try {
            $proc = Get-Process -Id ([int]$lockPid) -ErrorAction Stop
            $timestamp = Get-Date -Format "HH:mm:ss"
            Add-Content $LOG_FILE "[$timestamp] SKIPPED - previous run (pid $lockPid) still active"
            exit 0
        } catch {
            # Stale lock - previous run died without cleanup
            Remove-Item $LOCK_FILE -Force -ErrorAction SilentlyContinue
        }
    }
}
$PID | Set-Content $LOCK_FILE

# Cleanup lock on exit
$cleanupBlock = {
    Remove-Item $LOCK_FILE -Force -ErrorAction SilentlyContinue
}
Register-EngineEvent PowerShell.Exiting -Action $cleanupBlock | Out-Null

# --- Logging helper ---
function Log($msg) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Add-Content $LOG_FILE "[$timestamp] $msg"
}

# --- Permission flags ---
$permArgs = @()
if ($SKIP_PERMISSIONS -eq 'true') {
    $permArgs += '--dangerously-skip-permissions'
} elseif ($PERMISSION_MODE) {
    $permArgs += '--permission-mode'
    $permArgs += $PERMISSION_MODE
}
if ($ALLOWED_TOOLS) {
    $permArgs += '--allowedTools'
    $permArgs += $ALLOWED_TOOLS
}

# --- Execute ---
$startTime = Get-Date
$TIMEOUT_SECONDS = $TIMEOUT_MINUTES * 60
$targetPreview = if ($TASK_TARGET.Length -gt 120) { $TASK_TARGET.Substring(0, 120) + "..." } else { $TASK_TARGET }
Log "START  task=$TASK_ID type=$TASK_TYPE turns=$MAX_TURNS timeout=${TIMEOUT_MINUTES}m perms=$($permArgs.Count)flags"
Log "TARGET $targetPreview"

Set-Location $WORKDIR

$EXIT_CODE = 0
try {
    $job = switch ($TASK_TYPE) {
        "skill" {
            Start-Job -ScriptBlock {
                param($target, $maxTurns, $resultFile, $logFile, $pArgs, $sessionId)
                $allArgs = @('-p', "/$target", '--max-turns', $maxTurns, '--output-format', 'text', '--session-id', $sessionId) + $pArgs
                & claude @allArgs 2>>$logFile | Set-Content $resultFile
            } -ArgumentList $TASK_TARGET, $MAX_TURNS, $RESULT_FILE, $LOG_FILE, (,$permArgs), $SESSION_ID
        }
        "prompt" {
            Start-Job -ScriptBlock {
                param($target, $maxTurns, $resultFile, $logFile, $pArgs, $sessionId)
                $allArgs = @('-p', $target, '--max-turns', $maxTurns, '--output-format', 'text', '--session-id', $sessionId) + $pArgs
                & claude @allArgs 2>>$logFile | Set-Content $resultFile
            } -ArgumentList $TASK_TARGET, $MAX_TURNS, $RESULT_FILE, $LOG_FILE, (,$permArgs), $SESSION_ID
        }
        "script" {
            Start-Job -ScriptBlock {
                param($target, $resultFile, $logFile)
                & $target 2>>$logFile | Set-Content $resultFile
            } -ArgumentList $TASK_TARGET, $RESULT_FILE, $LOG_FILE
        }
    }

    $completed = Wait-Job $job -Timeout $TIMEOUT_SECONDS
    if ($null -eq $completed) {
        # Timed out
        Stop-Job $job
        $EXIT_CODE = 124
        Log "TIMEOUT after ${TIMEOUT_MINUTES}m"
    } else {
        if ($job.State -eq "Failed") {
            $EXIT_CODE = 1
        }
    }
    Remove-Job $job -Force
} catch {
    $EXIT_CODE = 1
    Log "ERROR $_"
}

$endTime = Get-Date
$duration = [int]($endTime - $startTime).TotalSeconds
$resultBytes = if (Test-Path $RESULT_FILE) { (Get-Item $RESULT_FILE).Length } else { 0 }
$resultLines = if (Test-Path $RESULT_FILE) { (Get-Content $RESULT_FILE | Measure-Object -Line).Lines } else { 0 }

# --- Log summary ---
if ($EXIT_CODE -eq 0) {
    Log "DONE   exit=0 duration=${duration}s result=${resultBytes}B/${resultLines}L"
    if (Test-Path $RESULT_FILE) {
        $preview = (Get-Content $RESULT_FILE -TotalCount 3 | Where-Object { $_.Trim() }) -join "`n"
        if ($preview.Length -gt 300) { $preview = $preview.Substring(0, 300) }
        Log "PREVIEW $preview"
    }
} else {
    Log "FAIL   exit=$EXIT_CODE duration=${duration}s result=${resultBytes}B"
}

# --- Find Claude Code JSONL session log ---
$SESSION_LOG = ""
if ($TASK_TYPE -ne "script") {
    $jsonlPattern = Join-Path $env:USERPROFILE ".claude\projects\*\$SESSION_ID.jsonl"
    $jsonlFile = Get-Item $jsonlPattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($jsonlFile) {
        $SESSION_LOG = $jsonlFile.FullName
    }
}

# --- Update registry with run results ---
Log "UPDATE update-last-run exit=$EXIT_CODE duration=${duration}s"
$sessionLogArg = @()
if ($SESSION_LOG) {
    $sessionLogArg = @('--session-log', $SESSION_LOG)
    Log "SESSION $SESSION_LOG"
}
try {
    uv run $SCHEDULER_PY update-last-run `
        --id $TASK_ID `
        --exit-code $EXIT_CODE `
        --duration $duration `
        --result-file $RESULT_FILE @sessionLogArg 2>&1 >> $LOG_FILE
} catch { }

# --- Notify ---
try {
    # Try BurntToast module first (rich notifications)
    if (Get-Module -ListAvailable -Name BurntToast -ErrorAction SilentlyContinue) {
        Import-Module BurntToast
        if ($EXIT_CODE -eq 0) {
            New-BurntToastNotification -Text "Scheduler: $TASK_ID", "Completed in ${duration}s ($resultLines lines)"
        } else {
            New-BurntToastNotification -Text "Scheduler: $TASK_ID", "Failed (exit $EXIT_CODE). Check logs."
        }
    } else {
        # Fallback: basic Windows toast via PowerShell
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
            [Windows.UI.Notifications.ToastTemplateType]::ToastText02
        )
        $textNodes = $template.GetElementsByTagName("text")
        $textNodes.Item(0).InnerText = "Scheduler: $TASK_ID"
        if ($EXIT_CODE -eq 0) {
            $textNodes.Item(1).InnerText = "Completed in ${duration}s ($resultLines lines)"
        } else {
            $textNodes.Item(1).InnerText = "Failed (exit $EXIT_CODE). Check logs."
        }
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Launchpad Scheduler").Show($toast)
    }
} catch {
    # Notifications are best-effort; don't fail the task
}

# --- One-off: self-complete after successful run ---
if ($RUN_ONCE -eq "true" -and $EXIT_CODE -eq 0) {
    Log "RUN_ONCE - marking task as completed"
    try {
        uv run $SCHEDULER_PY complete --id $TASK_ID 2>&1 >> $LOG_FILE
    } catch { }
}

# Cleanup lock
& $cleanupBlock

exit $EXIT_CODE

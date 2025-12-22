# This script loads environment variables from:
#   1. ~/.claude/.env (global defaults)
#   2. ./.env (project-specific, overrides global)
# It can be safely committed to version control as it contains no secrets

# Track if any .env was loaded
$loadedAny = $false

# Function to load .env file
function Import-EnvFile {
    param([string]$Path)

    if (Test-Path $Path) {
        Get-Content $Path | ForEach-Object {
            # Skip empty lines and comments
            if ($_ -match '^\s*$' -or $_ -match '^\s*#') {
                return
            }
            # Parse KEY=VALUE format
            if ($_ -match '^([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                # Remove surrounding quotes if present
                $value = $value -replace '^["'']|["'']$', ''
                [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
            }
        }
        return $true
    }
    return $false
}

# Load global ~/.claude/.env first (lower priority)
$globalEnvPath = Join-Path $env:USERPROFILE ".claude\.env"
if (Import-EnvFile $globalEnvPath) {
    Write-Host "✓ Loaded ~/.claude/.env" -ForegroundColor Green
    $loadedAny = $true
} else {
    Write-Host "○ ~/.claude/.env not found (skipped)" -ForegroundColor Gray
}

# Load project-local .env second (higher priority, overrides global)
$projectEnvPath = Join-Path (Get-Location) ".env"
if (Import-EnvFile $projectEnvPath) {
    Write-Host "✓ Loaded ./.env (project)" -ForegroundColor Green
    $loadedAny = $true
} else {
    Write-Host "○ ./.env not found (skipped)" -ForegroundColor Gray
}

# Warn only if neither file was found
if (-not $loadedAny) {
    Write-Host "⚠ Warning: No .env files found" -ForegroundColor Yellow
}

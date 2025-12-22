# MCP Launchpad Setup

Help the user set up the MCP Launchpad tool. Follow these steps:

## Step 1: Verify Prerequisites

Check if the user has the required tools installed:

```bash
# Check for uv
uv --version

# Check for Python
python3 --version
```

If uv is not installed, guide them to install it:
- **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## Step 2: Install MCP Launchpad

Install mcp-launchpad as a global uv tool:

```bash
uv tool install https://github.com/kenneth-liao/mcp-launchpad.git
```

After installation, verify it works:

```bash
mcpl --help
```

## Step 3: Set Up Environment Variables

The plugin automatically loads environment variables from:
1. `~/.claude/.env` (global, for all projects)
2. `.env` (project-specific, in current directory)

Create the global env file if it doesn't exist:

```bash
mkdir -p ~/.claude
touch ~/.claude/.env
```

Inform the user to add their API keys to the appropriate .env file.

**Important**: Project .env values override global values for the same key.

## Step 4: Configure Automatic Environment Loading

This step configures Claude Code to automatically load environment variables on every session.

### Detect Operating System

First, detect the user's operating system:

```bash
# macOS/Linux
uname -s

# Windows (PowerShell)
# $env:OS or check if running in PowerShell
```

### For macOS/Linux

1. **Check if CLAUDE_ENV_FILE is already configured:**

```bash
grep -n "CLAUDE_ENV_FILE" ~/.zshrc 2>/dev/null || grep -n "CLAUDE_ENV_FILE" ~/.bashrc 2>/dev/null
```

2. **If NOT configured**, ask the user for permission:

> **Permission Required**: To enable automatic environment loading, I need to add this line to your shell configuration (~/.zshrc or ~/.bashrc):
>
> ```bash
> export CLAUDE_ENV_FILE=~/.claude/plugins/marketplaces/ai-launchpad/mcp-launchpad/scripts/load-env.sh
> ```
>
> This tells Claude Code to source the load-env.sh script at the start of each session, which loads your .env files automatically.
>
> **Options:**
> - Add to ~/.zshrc (recommended for macOS)
> - Add to ~/.bashrc (for Linux/bash users)
> - Skip (configure manually later)

3. **If ALREADY configured** to a different value, ask how to proceed:

> **Existing Configuration Found**: CLAUDE_ENV_FILE is already set to:
> `[current value]`
>
> **Options:**
> - Replace with MCP Launchpad's load-env.sh
> - Keep existing configuration (skip this step)
> - Attempt to merge the two scripts

4. **Add the configuration** (after user confirms):

```bash
# For zsh (macOS default)
echo '' >> ~/.zshrc
echo '# MCP Launchpad - Auto-load environment variables for Claude Code' >> ~/.zshrc
echo 'export CLAUDE_ENV_FILE=~/.claude/plugins/marketplaces/ai-launchpad/mcp-launchpad/scripts/load-env.sh' >> ~/.zshrc

# OR for bash
echo '' >> ~/.bashrc
echo '# MCP Launchpad - Auto-load environment variables for Claude Code' >> ~/.bashrc
echo 'export CLAUDE_ENV_FILE=~/.claude/plugins/marketplaces/ai-launchpad/mcp-launchpad/scripts/load-env.sh' >> ~/.bashrc
```

5. **Remind the user** to reload their shell or run:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

### For Windows (PowerShell)

1. **Check if CLAUDE_ENV_FILE is already configured:**

```powershell
# Check environment variable
[System.Environment]::GetEnvironmentVariable('CLAUDE_ENV_FILE', 'User')

# Check PowerShell profile
if (Test-Path $PROFILE) { Select-String -Path $PROFILE -Pattern "CLAUDE_ENV_FILE" }
```

2. **If NOT configured**, ask the user for permission:

> **Permission Required**: To enable automatic environment loading, I need to add this to your PowerShell profile:
>
> ```powershell
> $env:CLAUDE_ENV_FILE = "$env:USERPROFILE\.claude\plugins\marketplaces\ai-launchpad\mcp-launchpad\scripts\load-env.ps1"
> ```
>
> This tells Claude Code to run the load-env.ps1 script at the start of each session.
>
> **Options:**
> - Add to PowerShell profile (recommended)
> - Set as User environment variable
> - Skip (configure manually later)

3. **If ALREADY configured** to a different value, ask how to proceed (same options as macOS/Linux).

4. **Add the configuration** (after user confirms):

```powershell
# Option A: Add to PowerShell profile
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
Add-Content -Path $PROFILE -Value ""
Add-Content -Path $PROFILE -Value "# MCP Launchpad - Auto-load environment variables for Claude Code"
Add-Content -Path $PROFILE -Value '$env:CLAUDE_ENV_FILE = "$env:USERPROFILE\.claude\plugins\marketplaces\ai-launchpad\mcp-launchpad\scripts\load-env.ps1"'

# Option B: Set as User environment variable (persists across sessions)
[System.Environment]::SetEnvironmentVariable('CLAUDE_ENV_FILE', "$env:USERPROFILE\.claude\plugins\marketplaces\ai-launchpad\mcp-launchpad\scripts\load-env.ps1", 'User')
```

5. **Remind the user** to restart PowerShell or run:

```powershell
. $PROFILE
```

## Step 5: Verify MCP Servers

Test that their configured MCP servers are working:

```bash
# List all available MCP servers
mcpl list

# Verify all servers are connected
mcpl verify
```

## Step 6: Quick Reference

Share this quick reference with the user:

```bash
# Find tools
mcpl search "<query>"                    # Search all tools
mcpl list <server>                       # List tools for a server

# Get tool details
mcpl inspect <server> <tool>             # Full schema
mcpl inspect <server> <tool> --example   # Schema + example call

# Execute tools
mcpl call <server> <tool> '{"param": "value"}'

# Troubleshooting
mcpl verify                              # Test all servers
mcpl session status                      # Check daemon status
mcpl session stop                        # Restart daemon
```

## Completion

Once setup is complete, inform the user that:
1. Environment variables will automatically load on each new Claude Code session (after shell restart)
2. They can add API keys to `~/.claude/.env` for global access
3. Project-specific variables should go in the project's `.env` file
4. Use `mcpl` commands to discover and use MCP tools
5. **Important**: They need to restart their terminal (or source their shell config) for the CLAUDE_ENV_FILE change to take effect

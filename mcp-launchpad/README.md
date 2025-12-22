# MCP Launchpad Plugin

A Claude Code plugin that integrates [MCP Launchpad](https://github.com/ai-launchpad/mcp-launchpad) — a unified CLI for discovering and managing MCP servers — with automatic environment variable loading.

## Features

- **Automatic Environment Loading**: Loads `.env` files into your Claude Code session on startup
- **Global + Project Variables**: Supports both global (`~/.claude/.env`) and project-specific (`.env`) environment files
- **Cross-Platform Support**: Works on macOS, Linux, and Windows
- **MCP Launchpad Integration**: Quick access to the `mcpl` CLI for discovering and using MCP tools

## Installation

### 1. Install the Plugin

```bash
claude plugin add mcp-launchpad@ai-launchpad
```

### 2. Install MCP Launchpad CLI

```bash
uv tool install mcp-launchpad
```

### 3. Run Setup

Start a new Claude Code session and run:

```
/mcp-launchpad:setup
```

This will:
1. Verify prerequisites (uv, Python)
2. Create `~/.claude/.env` for global environment variables
3. Configure `CLAUDE_ENV_FILE` in your shell config (with your permission)
4. Verify MCP server connections

## How It Works

### Environment Variable Loading

The plugin uses Claude Code's `CLAUDE_ENV_FILE` mechanism to automatically load environment variables at session start.

**Load order (later values override earlier):**
1. **Global**: `~/.claude/.env` — Available in all projects
2. **Project**: `.env` — Project-specific overrides

### Shell Configuration

During setup, the plugin adds one of these to your shell configuration:

**macOS/Linux** (`~/.zshrc` or `~/.bashrc`):
```bash
export CLAUDE_ENV_FILE=~/.claude/plugins/marketplaces/ai-launchpad/mcp-launchpad/scripts/load-env.sh
```

**Windows** (PowerShell profile):
```powershell
$env:CLAUDE_ENV_FILE = "$env:USERPROFILE\.claude\plugins\marketplaces\ai-launchpad\mcp-launchpad\scripts\load-env.ps1"
```

This tells Claude Code to run the appropriate script at the start of each session, which loads your `.env` files automatically.

### Example .env Files

**Global (`~/.claude/.env`)**:
```bash
# API Keys available everywhere
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
```

**Project (`.env`)**:
```bash
# Project-specific configuration
DATABASE_URL=postgres://localhost:5432/myapp
SENTRY_DSN=https://...
```

## MCP Launchpad Quick Reference

```bash
# Find tools
mcpl search "<query>"                    # Search all tools
mcpl search "<query>" --first            # Top result with example call
mcpl list                                # List all MCP servers
mcpl list <server>                       # List tools for a server

# Get tool details
mcpl inspect <server> <tool>             # Full schema
mcpl inspect <server> <tool> --example   # Schema + example call

# Execute tools
mcpl call <server> <tool> '{}'                        # No arguments
mcpl call <server> <tool> '{"param": "value"}'        # With arguments

# Troubleshooting
mcpl verify                              # Test all server connections
mcpl session status                      # Check daemon status
mcpl session stop                        # Restart daemon
```

## Plugin Structure

```
mcp-launchpad/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   └── setup.md             # /mcp-launchpad:setup command
├── scripts/
│   ├── load-env.sh          # Environment loading (macOS/Linux)
│   └── load-env.ps1         # Environment loading (Windows)
└── README.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/mcp-launchpad:setup` | Interactive setup guide for MCP Launchpad |

## Cross-Platform Support

| Platform | Shell Config | Script |
|----------|--------------|--------|
| macOS | `~/.zshrc` | `load-env.sh` |
| Linux | `~/.bashrc` or `~/.zshrc` | `load-env.sh` |
| Windows | PowerShell profile | `load-env.ps1` |

## Requirements

- [Claude Code](https://claude.com/claude-code) CLI
- [uv](https://docs.astral.sh/uv/) package manager
- Python 3.10+

## Troubleshooting

### Environment Variables Not Loading

1. Check that `CLAUDE_ENV_FILE` is set in your shell:
   - **macOS/Linux**: `echo $CLAUDE_ENV_FILE`
   - **Windows**: `echo $env:CLAUDE_ENV_FILE`
2. Verify the script exists at the path shown
3. Restart your terminal and start a new Claude Code session
4. Check that your `.env` files exist and are properly formatted

### CLAUDE_ENV_FILE Not Set After Setup

Make sure you've restarted your terminal or sourced your shell config:
- **macOS/Linux**: `source ~/.zshrc` or `source ~/.bashrc`
- **Windows**: `. $PROFILE`

### MCP Servers Not Connecting

```bash
# Test all server connections
mcpl verify

# Check daemon status
mcpl session status

# Restart the daemon
mcpl session stop
```

### Command Not Found: mcpl

Make sure MCP Launchpad is installed:

```bash
uv tool install mcp-launchpad
```

And that uv tools are in your PATH:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

## License

MIT

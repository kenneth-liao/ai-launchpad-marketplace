#!/bin/bash
# This script loads environment variables from:
#   1. ~/.claude/.env (global defaults)
#   2. ./.env (project-specific, overrides global)
# It can be safely committed to version control as it contains no secrets

# Track if any .env was loaded
loaded_any=false

# Load global ~/.claude/.env first (lower priority)
if [ -f "$HOME/.claude/.env" ]; then
    set -a
    source "$HOME/.claude/.env"
    set +a
    echo "✓ Loaded ~/.claude/.env"
    loaded_any=true
else
    echo "○ ~/.claude/.env not found (skipped)"
fi

# Load project-local .env second (higher priority, overrides global)
if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
    echo "✓ Loaded ./.env (project)"
    loaded_any=true
else
    echo "○ ./.env not found (skipped)"
fi

# Warn only if neither file was found
if [ "$loaded_any" = false ]; then
    echo "⚠ Warning: No .env files found"
fi

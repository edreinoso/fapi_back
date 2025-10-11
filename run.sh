#!/usr/bin/env bash
# UEFA Champions League Fantasy Data Processor Runner
# Prevents .pyc file generation

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Run with uv
exec uv run python main.py "$@"
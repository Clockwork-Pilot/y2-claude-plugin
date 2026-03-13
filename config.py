"""
Centralized configuration for paths used throughout the project.
This serves as the single source of truth for all project paths.
"""

import os
from pathlib import Path

# Plugin root directory
PLUGIN_ROOT = Path(__file__).parent.resolve()

# Consuming project root (when used as a plugin, this is the target project)
# Defaults to current working directory, can be overridden by env var
CONSUMING_PROJECT_ROOT = Path(os.getenv("CLAUDE_PROJECT_ROOT", os.getcwd())).resolve()

# Use consuming project's .claude directory for logs
CLAUDE_DIR = CONSUMING_PROJECT_ROOT / ".claude"
HOOKS_DIR = PLUGIN_ROOT / "hooks"

# Files
CLAUDE_HOOKS_CONFIG_FILE = HOOKS_DIR / "hooks.json"
# By convention we use just this path, so knowledge tools just hardocded the same path
KNOWN_KNOWLEDGE_FILES = PLUGIN_ROOT / "protected_files.txt"

# Logging - write to consuming project's .claude directory
# Base directory for logs across multiple consuming projects
# If defined, logs go to <HOOK_LOGS_BASE_DIR>/<CONSUMING_PROJECT_NAME>/.claude/hooks.log
# If None, logs go to consuming project's .claude directory (default behavior)
HOOK_LOGS_BASE_DIR = os.getenv("CLAUDE_DOCKER_HOOK_LOGS_BASE_DIR", None)
if HOOK_LOGS_BASE_DIR is not None:
    CONSUMING_PROJECT_NAME = CONSUMING_PROJECT_ROOT.name
    HOOKS_LOG_FILE = Path(HOOK_LOGS_BASE_DIR) / CONSUMING_PROJECT_NAME / ".claude" / "hooks.log"
else:
    HOOKS_LOG_FILE = CLAUDE_DIR / "hooks.log"

HOOKS_LOG_LEVEL = "INFO"  # Can be: DEBUG, INFO, WARNING, ERROR, CRITICAL


__all__ = [
    "PLUGIN_ROOT",
    "CONSUMING_PROJECT_ROOT",
    "CLAUDE_DIR",
    "HOOKS_DIR",
    "CLAUDE_HOOKS_CONFIG_FILE",
    "KNOWN_KNOWLEDGE_FILES",
    "HOOK_LOGS_BASE_DIR",
    "HOOKS_LOG_FILE",
    "HOOKS_LOG_LEVEL"
]

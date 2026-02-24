"""
Centralized configuration for paths used throughout the project.
This serves as the single source of truth for all project paths.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()

# Directories
CLAUDE_DIR = PROJECT_ROOT / ".claude"
HOOKS_DIR = PROJECT_ROOT / "hooks"

# Files
CLAUDE_HOOKS_CONFIG_FILE = HOOKS_DIR / "hooks.json"

# Logging
HOOKS_LOG_FILE = PROJECT_ROOT / "hooks.log"
HOOKS_LOG_LEVEL = "INFO"  # Can be: DEBUG, INFO, WARNING, ERROR, CRITICAL


__all__ = [
    "PROJECT_ROOT",
    "CLAUDE_DIR",
    "HOOKS_DIR",
    "CLAUDE_HOOKS_CONFIG_FILE",
    "HOOKS_LOG_FILE",
    "HOOKS_LOG_LEVEL"
]

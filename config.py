"""
Centralized configuration for paths used throughout the project.
This serves as the single source of truth for all project paths.
"""

import os
from pathlib import Path

# Shown by hooks when constraints fail in the dev loop. Full guidance lives in
# the y2:features_and_constraints skill; this message only states what happened and
# nudges the agent to load the skill.
GUIDE_MESSAGE_WHEN_CONSTRAINTS_FAIL_IN_DEV_LOOP = """
Constraints violation: one or more constraints are failing, and the session has been forced back into the dev loop until they pass.

Note: ensure the y2:features_and_constraints skill is loaded (load it once if not) — it explains how to resolve failing constraints.
"""

# Shown by hooks when edits are blocked by unverified constraints. Full guidance
# lives in the y2:features_and_constraints skill; this message only states what
# happened and nudges the agent to load the skill.
GUIDE_MESSAGE_UNVERIFIED_BLOCKING_CONSTRAINTS = """
Edit blocked: `spec.k.json` contains unverified constraints (never failed), which block all source code modifications until each fails at least once.

Note: ensure the y2:features_and_constraints skill is loaded (load it once if not) — it explains how to resolve unverified blocking constraints.
"""

# Plugin root directory. Defaults to this file's parent, overridable via PLUGIN_ROOT env var.
PLUGIN_ROOT = Path(os.getenv("PLUGIN_ROOT", str(Path(__file__).parent))).resolve()
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", os.getcwd())).resolve()

# Target project root. Defaults to cwd, overridable via PROJECT_ROOT env var.
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", os.getcwd())).resolve()

# Executables paths for external executables discovery
PATH = ':'.join([
    os.path.join(PLUGIN_ROOT, "constraints_tool/constraints_tool"),
    os.path.join(PLUGIN_ROOT, "knowledge_tool/knowledge_tool"),
])

STOP_HANDLER_TIMEOUT = 300
CONSTRAINTS_TIMEOUT = 500

# Use consuming project's .claude directory for logs
HOOKS_DIR = PLUGIN_ROOT / "hooks"

# Files
CLAUDE_HOOKS_CONFIG_FILE = HOOKS_DIR / "hooks.json"

# Constraint check results file
CONSTRAINTS_RESULTS_FILE = "spec-checks.k.json"

# Logging - write to project root hooks_log directory
# Defaults to <PROJECT_ROOT>/hooks_log/hooks.log, overridable via CLAUDE_HOOKS_LOG_FILE env var
HOOKS_LOG_FILE = Path(
    os.getenv("CLAUDE_HOOKS_LOG_FILE", str(PROJECT_ROOT / "hooks_log" / "hooks.log"))
)

HOOKS_LOG_LEVEL = "INFO"  # Can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

# File rules config path — implementation lives in hooks/__init__.py
FILE_RULES_PATH = os.getenv("CLAUDE_FILE_RULES", None)

# Project data directory for task iterations and spec snapshots
PROJECT_DATA_DIR = PROJECT_ROOT / "project"

# This flag should  always be False, but human can actually set it manually to True when needed
TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK = False

# Disable stop hook execution
# Can be overridden via DISABLE_STOP_HOOK env var (set to "true" or "1" to disable)
DISABLE_STOP_HOOK = os.getenv("DISABLE_STOP_HOOK", "").lower() in ("true", "1")

__all__ = [
    "PLUGIN_ROOT",
    "PROJECT_ROOT",
    "PROJECT_DATA_DIR",
    "HOOKS_DIR",
    "CLAUDE_HOOKS_CONFIG_FILE",
    "CONSTRAINTS_RESULTS_FILE",
    "HOOKS_LOG_FILE",
    "HOOKS_LOG_LEVEL",
    "DISABLE_STOP_HOOK"
]

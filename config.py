"""
Centralized configuration for paths used throughout the project.
This serves as the single source of truth for all project paths.
"""

import os
from pathlib import Path

# Message to a Claude when it forced to dev loop because of failing constraints
GUIDE_MESSAGE_WHEN_CONSTRAINTS_FAIL_IN_DEV_LOOP = """
Constraints violation happened -one or more constraints are failing.
You should not be trying to remove these constraints, as once constraint is verified it becomes
unstoppable like Tsunami. The only thing you can do is to change implementation of related feature,
to satisfy constraint.
Do not try removing constraint - you will fail.
Do not try manipulating with fails_count value - you will fail.

Note: Constraints in spec.k.json tests project under PROJECT_ROOT env var.
"""

GUIDE_MESSAGE_UNVERIFIED_BLOCKING_CONSTRAINTS = """
Current task spec `spec.k.json` contains unverified never failed constraints.
Unverified constraint is a no go way! You should be carefull according to y2:features_and_constraints
when add new constraints. If constraint never fails - you will never be allowed to modify source code
until constrait will fail at least once. You can not modify source code if you add non failing constraint.
Always add carefully crafted failing constraint, so it will expected to pass as soon as feature will be
properly implemented. Badly crafted constraints will cause either block source code changes or will cause
an a dev loop before constraint will be satisfied. Remember that constraint is a function of source code.
Be aware adding constraint that unconditionally fail - it will block you entirely.
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

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

Note: Constraints in task-spec.k.json tests project under CLAUDE_PROJECT_ROOT env var.
"""

GUIDE_MESSAGE_UNVERIFIED_BLOCKING_CONSTRAINTS = """
Current task spec `task-spec.k.json` contains unverified never failed constraints.
Unverified constraint is a no go way! You should be carefull according to y2:features_and_constraints
when add new constraints. If constraint never fails - you will never be allowed to modify source code
until constrait will fail at least once. You can not modify source code if you add non failing constraint.
Always add carefully crafted failing constraint, so it will expected to pass as soon as feature will be
properly implemented. Badly crafted constraints will cause either block source code changes or will cause
an a dev loop before constraint will be satisfied. Remember that constraint is a function of source code.
Be aware adding constraint that unconditionally fail - it will block you entirely.
"""

# Plugin root directory
PLUGIN_ROOT = Path(__file__).parent.resolve()
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", os.getcwd())).resolve()

# Consuming project root (when used as a plugin, this is the target project)
# Defaults to current working directory, can be overridden by env var
CONSUMING_PROJECT_ROOT = Path(os.getenv("CLAUDE_PROJECT_ROOT", os.getcwd())).resolve()
PROJECT_ROOT = CONSUMING_PROJECT_ROOT

# Executables paths for external executables discovery
PATH = ':'.join([
    os.path.join(PLUGIN_ROOT, "constraints_tool/constraints_tool"),
    os.path.join(PLUGIN_ROOT, "knowledge_tool/knowledge_tool"),
])

STOP_HANDLER_TIMEOUT = 300
CONSTRAINTS_TIMEOUT = 500

# Use consuming project's .claude directory for logs
CLAUDE_DIR = CONSUMING_PROJECT_ROOT / ".claude"
HOOKS_DIR = PLUGIN_ROOT / "hooks"

# Files
CLAUDE_HOOKS_CONFIG_FILE = HOOKS_DIR / "hooks.json"
# By convention we use just this path, so knowledge tools just hardocded the same path
KNOWN_KNOWLEDGE_FILES_PATH = PROJECT_ROOT / "protected_files.txt"

# Constraint check results file
CONSTRAINTS_RESULTS_FILE = "task-results.k.json"

# Logging - write to consuming project's .claude directory
# Base directory for logs across multiple consuming projects
# If defined, logs go to <HOOK_LOGS_BASE_DIR>/<CONSUMING_PROJECT_NAME>/.claude/hooks.log
# If None, logs go to consuming project's .claude directory (default behavior)
HOOK_LOGS_BASE_DIR = os.getenv("CLAUDE_DOCKER_HOOK_LOGS_BASE_DIR", None)
if HOOK_LOGS_BASE_DIR is not None:
    HOOKS_LOG_FILE = Path(HOOK_LOGS_BASE_DIR) / CONSUMING_PROJECT_ROOT.name / ".claude" / "hooks.log"
else:
    HOOKS_LOG_FILE = CLAUDE_DIR / "hooks.log"

HOOKS_LOG_LEVEL = "INFO"  # Can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

# File rules config path — implementation lives in hooks/__init__.py
FILE_RULES_PATH = os.getenv("CLAUDE_FILE_RULES", None)

# Project data directory for task iterations and spec snapshots
PROJECT_DATA_DIR = PROJECT_ROOT / "project"

# This flag should  always be False, but human can actually set it manually to True when needed
TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK = False

__all__ = [
    "PLUGIN_ROOT",
    "CONSUMING_PROJECT_ROOT",
    "PROJECT_ROOT",
    "PROJECT_DATA_DIR",
    "CLAUDE_DIR",
    "HOOKS_DIR",
    "CLAUDE_HOOKS_CONFIG_FILE",
    "KNOWN_KNOWLEDGE_FILES_PATH",
    "CONSTRAINTS_RESULTS_FILE",
    "HOOK_LOGS_BASE_DIR",
    "HOOKS_LOG_FILE",
    "HOOKS_LOG_LEVEL"
]

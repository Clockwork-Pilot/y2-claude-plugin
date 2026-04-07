"""Hooks utilities."""

import sys
import json
import fnmatch
import os
from pathlib import Path
from typing import Dict

def get_vars() -> Dict[str, str]:
    """Return a dict with PROJECT_ROOT and PLUGIN_ROOT environment variables.

    Returns:
        dict: Contains PROJECT_ROOT and PLUGIN_ROOT paths
    """
    from config import PLUGIN_ROOT, PROJECT_ROOT, WORKSPACE_ROOT
    # 
    return {
        "PROJECT_ROOT": str(PROJECT_ROOT),
        "PLUGIN_ROOT": str(PLUGIN_ROOT),
        "WORKSPACE_ROOT": str(WORKSPACE_ROOT),
    }


def send_error(message: str, file_path: str = None) -> None:
    """Send error message to Claude about blocked operation.

    Args:
        message: Error message to display
        file_path: Optional file path that triggered the error
    """
    error_output = {
        "type": "error",
        "message": message,
        "file_path": file_path
    }
    print(json.dumps(error_output), file=sys.stderr)


def is_knowledge_file(file_path: str) -> bool:
    """Check if file is in knowledge files registry.

    Args:
        file_path: Path to check (can be relative or absolute).

    Returns:
        True if the file is a registered knowledge file, False otherwise.
    """
    import sys
    from config import PROJECT_ROOT

    # Get filename definition from knowledge_tool submodule (single source of truth)
    knowledge_tool_path = Path(__file__).parent.parent / "knowledge_tool"
    if str(knowledge_tool_path) not in sys.path:
        sys.path.insert(0, str(knowledge_tool_path))

    from knowledge_tool import PROTECTED_REGISTRY_FILENAME
    registry_path = PROJECT_ROOT / PROTECTED_REGISTRY_FILENAME

    if not registry_path.exists():
        return False

    abs_path = str(Path(file_path).resolve())
    try:
        content = registry_path.read_text().strip()
        return abs_path in content.split('\n')
    except Exception:
        return False


def have_unverified_constraints() -> bool:
    """Check if spec.k.json has unverified constraints.

    Reads the contains_unverified_constraints flag from PROJECT_ROOT/spec.k.json.
    Unverified constraints (fails_count < 1) are those that haven't been proven to fail.

    Returns:
        True if contains_unverified_constraints flag is True, False otherwise.
    """
    from config import PROJECT_ROOT, TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK

    if TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK:
        return False

    spec_path = PROJECT_ROOT / "spec.k.json"

    try:
        if not spec_path.exists():
            return False

        spec_data = json.loads(spec_path.read_text())
        return spec_data.get("contains_unverified_constraints", False)
    except Exception:
        return False


def get_deny_reasons_for_file(path: str) -> list[str]:
    """Return deny reasons for the given file path via glob patterns.

    Rules are loaded from the JSON file pointed to by CLAUDE_FILE_RULES env var.
    Deny entry:      {"deny-rule": ["src/**/*.rs"], "reason": "some reason"}
    Whitelist entry: {"whitelist-rule": ["src/specific/file.rs"]}
    If any whitelist-rule glob matches the path, deny rules are overridden and [] is returned.
    """
    from config import FILE_RULES_PATH

    if not FILE_RULES_PATH:
        return []
    rules_path = Path(FILE_RULES_PATH)
    if not rules_path.exists():
        return []
    entries = json.loads(rules_path.read_text())
    reasons = []
    for entry in entries:
        deny_globs = [os.path.expandvars(g) for g in entry.get("deny-rule", [])]
        if any(fnmatch.fnmatch(path, g) for g in deny_globs):
            reason = entry.get("reason")
            reasons.append(reason if reason else "denied")
    if not reasons:
        return []
    for entry in entries:
        whitelist_globs = [os.path.expandvars(g) for g in entry.get("whitelist-rule", [])]
        if any(fnmatch.fnmatch(path, g) for g in whitelist_globs):
            return []
    return reasons


def is_edit_blocked_by_unverified_constraints(file_path: str = None) -> bool:
    """Check if editing is blocked due to unverified constraints.

    This function is used in hooks (handler_write.py, handler_edit.py) to prevent
    modifications when the spec has unverified constraints.

    Args:
        file_path: Optional file path being edited (for context, not currently used)

    Returns:
        True if unverified constraints exist and editing should be blocked, False otherwise.
    """
    return have_unverified_constraints()


__all__ = [
    "get_vars",
    "send_error",
    "is_knowledge_file",
    "have_unverified_constraints",
    "is_edit_blocked_by_unverified_constraints",
    "get_deny_reasons_for_file",
]

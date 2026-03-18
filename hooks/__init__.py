"""Hooks utilities."""

import sys
import json
from pathlib import Path


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
    from config import KNOWN_KNOWLEDGE_FILES_PATH

    if not KNOWN_KNOWLEDGE_FILES_PATH.exists():
        return False

    abs_path = str(Path(file_path).resolve())
    try:
        content = KNOWN_KNOWLEDGE_FILES_PATH.read_text().strip()
        return abs_path in content.split('\n')
    except Exception:
        return False


def have_unverified_constraints() -> bool:
    """Check if task-spec.k.json has unverified constraints.

    Reads the contains_unverified_constraints flag from PROJECT_ROOT/task-spec.k.json.
    Unverified constraints (fails_count < 1) are those that haven't been proven to fail.

    Returns:
        True if contains_unverified_constraints flag is True, False otherwise.
    """
    from config import PROJECT_ROOT, TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK

    if TEMPORARY_BYPASS_UNVERIFIED_CONSTRAINTS_BLOCK:
        return False

    spec_path = PROJECT_ROOT / "task-spec.k.json"

    try:
        if not spec_path.exists():
            return False

        spec_data = json.loads(spec_path.read_text())
        return spec_data.get("contains_unverified_constraints", False)
    except Exception:
        return False


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
    "send_error",
    "is_knowledge_file",
    "have_unverified_constraints",
    "is_edit_blocked_by_unverified_constraints"
]

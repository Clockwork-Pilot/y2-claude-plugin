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


def validate_task_status_transition(file_path: str, patch_operations: list, old_status: str = None):
    """Validate Task status transitions during patching.

    Prevents status downgrades: executing/failed/succeed cannot go back to planning.

    Args:
        file_path: Path to the file being modified
        patch_operations: List of RFC 6902 JSON Patch operations
        old_status: Current status of the task (if available)

    Returns:
        Tuple of (is_valid, error_message). is_valid=True if transition is allowed.
    """
    # Only validate task.json files
    if not file_path.endswith('task.json'):
        return True, ""

    # Valid status values and transitions
    valid_statuses = {"planning", "executing", "failed", "succeed"}
    no_downgrade_statuses = {"executing", "failed", "succeed"}

    # Check for status changes in the patch operations
    for op in patch_operations:
        if op.get('op') == 'replace' and op.get('path') == '/status':
            new_status = op.get('value')

            # If we don't have the old status, we can't validate
            if not old_status:
                return True, ""

            # Check for invalid status values
            if new_status not in valid_statuses:
                return False, f"Invalid status value: {new_status}. Must be one of: {', '.join(valid_statuses)}"

            # Check for downgrade attempts
            if old_status in no_downgrade_statuses and new_status == "planning":
                return False, f"Status downgrade not allowed: cannot change from '{old_status}' back to 'planning'. Task status can only move forward: planning → executing → (failed|succeed)."

    return True, ""


__all__ = ["send_error", "is_knowledge_file", "validate_task_status_transition"]

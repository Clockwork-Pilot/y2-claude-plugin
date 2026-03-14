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
    from config import KNOWN_KNOWLEDGE_FILES

    if not KNOWN_KNOWLEDGE_FILES.exists():
        return False

    abs_path = str(Path(file_path).resolve())
    try:
        content = KNOWN_KNOWLEDGE_FILES.read_text().strip()
        return abs_path in content.split('\n')
    except Exception:
        return False


__all__ = ["send_error", "is_knowledge_file"]

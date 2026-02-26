"""
Common task management utilities for Claude Code hooks.

Enables all hook handlers to:
- Load current task document (.TASK.md)
- Extract task context for logging
- Access task metadata during handler execution

Follows Constitution Principle IV (Structured Observability):
- All handlers log task context via this module
- Task loading is optional (gracefully handles missing .TASK.md)
- Follows Principle II (Non-Interference): handler works with or without task
"""
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from tasks_scripts.models import TaskDocument
    from tasks_scripts.task_state import load_task_document
    TASK_MANAGEMENT_AVAILABLE = True
except ImportError:
    TASK_MANAGEMENT_AVAILABLE = False


def load_task_document_safe(start_dir: Optional[str] = None) -> Optional[TaskDocument]:
    """
    Search for and load .TASK.md from current directory up to repo root.

    Searches in this order:
    1. start_dir (if provided)
    2. Current working directory
    3. Parent directories up to repo root

    Returns:
        TaskDocument model if found and valid, None otherwise
        Gracefully handles missing files or parsing errors

    Args:
        start_dir: Optional directory to start searching from
    """
    if not TASK_MANAGEMENT_AVAILABLE:
        return None

    # Determine starting directory
    if start_dir:
        current_dir = Path(start_dir)
    else:
        current_dir = Path.cwd()

    # Search up the directory tree
    max_iterations = 20  # Prevent infinite loops
    for _ in range(max_iterations):
        task_file = current_dir / ".TASK.md"

        if task_file.exists():
            try:
                doc = load_task_document(str(task_file))
                return doc
            except Exception:
                # Silently fail if document can't be parsed
                # Allows handlers to work even with corrupted task files
                return None

        # Move to parent directory
        parent = current_dir.parent
        if parent == current_dir:
            # Reached filesystem root
            break

        current_dir = parent

    # Not found
    return None


def get_task_context(task_doc: Optional[TaskDocument]) -> Optional[Dict[str, Any]]:
    """
    Extract task metadata for logging/observability.

    Returns task context in a format suitable for structured logging.

    Args:
        task_doc: TaskDocument model (can be None)

    Returns:
        Dict with keys: task_name, current_phase, created_at (ISO format)
        Returns None if task_doc is None
    """
    if task_doc is None:
        return None

    return {
        "task_name": task_doc.current_phase,
        "current_phase": task_doc.current_phase,
        "created_at": task_doc.created_at.isoformat()
    }


def handler_with_task_context(handler_func):
    """
    Decorator for handlers to automatically load and log task context.

    Usage:
        @handler_with_task_context
        def my_handler(task_context):
            # task_context is None or dict with task metadata
            pass
    """
    def wrapper(*args, **kwargs):
        task_doc = load_task_document_safe()
        task_context = get_task_context(task_doc)
        # Pass task context as first argument if handler accepts it
        return handler_func(task_context, *args, **kwargs)

    return wrapper

"""
Task rollback script.

Reverts a task from the current phase to a previous phase when loop detected
or metrics not improving, with rollback entry documentation.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from tasks_scripts.models import TaskDocument, RollbackEntry
from tasks_scripts.task_state import (
    load_task_document,
    get_previous_phase,
    append_rollback_entry,
    PHASE_WORKFLOW,
)


def rollback_phase(
    task_path: str = ".TASK.md",
    target_phase: Optional[str] = None,
    reason: str = "loop detected"
) -> TaskDocument:
    """
    Rollback task to a previous phase.

    Args:
        task_path: Path to .TASK.md file
        target_phase: Phase to rollback to (default: previous phase)
        reason: Reason for rollback (loop, metrics_regression, etc.)

    Returns:
        Updated TaskDocument with new current_phase

    Raises:
        FileNotFoundError: If task file not found
        ValueError: If invalid phase sequence or phase not found
    """
    task_path = Path(task_path)

    # Load current task document
    doc = load_task_document(str(task_path))
    current_phase = doc.current_phase

    # Determine target phase
    if target_phase is None:
        target_phase = get_previous_phase(current_phase)
    else:
        # Validate target phase
        if target_phase not in PHASE_WORKFLOW:
            raise ValueError(f"Invalid target phase: {target_phase}")

        # Validate target is earlier than current
        current_idx = PHASE_WORKFLOW.index(current_phase)
        target_idx = PHASE_WORKFLOW.index(target_phase)

        if target_idx >= current_idx:
            raise ValueError(
                f"Cannot rollback from {current_phase} to {target_phase}: "
                f"target must be earlier in workflow"
            )

    # Create rollback entry
    now = datetime.now(timezone.utc).replace(microsecond=0)
    rollback_entry = RollbackEntry(
        from_phase=current_phase,
        timestamp=now,
        issue_type="loop" if "loop" in reason.lower() else "metrics_regression",
        problem_description=reason
    )

    # Read current markdown
    markdown_content = task_path.read_text(encoding='utf-8')

    # Append rollback entry to target phase
    updated_markdown = append_rollback_entry(
        markdown_content,
        target_phase,
        rollback_entry
    )

    # Save updated markdown
    task_path.write_text(updated_markdown, encoding='utf-8')

    # Reload and update current_phase
    doc = load_task_document(str(task_path))
    doc.current_phase = target_phase

    return doc


if __name__ == "__main__":
    try:
        task_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"
        target_phase = sys.argv[2] if len(sys.argv) > 2 else None
        reason = sys.argv[3] if len(sys.argv) > 3 else "loop detected"

        doc = rollback_phase(task_path, target_phase, reason)
        print(f"Rolled back to {doc.current_phase}")
        sys.exit(0)

    except Exception as e:
        print(f"Error rolling back phase: {e}", file=sys.stderr)
        sys.exit(1)

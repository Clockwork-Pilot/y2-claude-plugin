#!/usr/bin/env python3
"""
Task phase advancement script: Progress a task through the workflow.

Advances a task from one phase to the next in the predefined 7-phase workflow.
Uses atomic updates with section markers and exclusive file mode for safety.
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

from tasks_scripts.models import TaskDocument, Phase, PhaseHeader
from tasks_scripts.task_state import load_task_document, append_to_phase, get_next_phase, PHASE_WORKFLOW


def advance_phase(task_path: str = ".TASK.md") -> TaskDocument:
    """
    Advance a task to the next phase in the workflow.

    Detects concurrent writes using exclusive lock file (O_EXCL semantics).

    Args:
        task_path: Path to .TASK.md file (default: ".TASK.md")

    Returns:
        Updated TaskDocument model

    Raises:
        FileNotFoundError: If task file doesn't exist
        ValueError: If phase sequence is invalid (e.g., already at final phase)
        IOError: If file is locked (concurrent write detected) or cannot be read/written
    """
    path = Path(task_path)
    lock_path = path.with_name(f"{path.name}.lock")

    # Detect concurrent writes: try to create lock file exclusively
    try:
        # O_CREAT | O_EXCL will fail if file already exists
        lock_fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(lock_fd)
        lock_acquired = True
    except FileExistsError:
        raise IOError(f"Task file is locked (concurrent write detected): {task_path}")
    except Exception as e:
        raise IOError(f"Failed to acquire lock: {e}")

    try:
        # Load current task document
        try:
            doc = load_task_document(str(path))
        except FileNotFoundError:
            raise FileNotFoundError(f"Task document not found: {task_path}")
        except Exception as e:
            raise ValueError(f"Failed to load task document: {e}")

        # Get next phase
        try:
            next_phase_name = get_next_phase(doc.current_phase)
        except ValueError as e:
            raise ValueError(f"Invalid phase sequence: {e}")

        # Read current file content
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to read task file: {e}")

        # Create new phase header with current timestamp
        now = datetime.now(timezone.utc)
        timestamp_str = now.isoformat()

        # Build new phase section
        new_phase_header = f"# PHASE {next_phase_name} at {timestamp_str}\n\n"
        new_phase_marker = f"<!-- {next_phase_name} -->"
        new_phase_content = f"{new_phase_header}{new_phase_marker}"

        # Append new phase using atomic regex
        try:
            updated_content = append_to_phase(content, doc.current_phase, new_phase_content)
        except ValueError as e:
            raise ValueError(f"Failed to append phase: {e}")

        # Write updated content atomically
        try:
            path.write_text(updated_content, encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to write task file: {e}")

        # Create new phase in model
        new_header = PhaseHeader(phase_name=next_phase_name, timestamp=now)
        new_phase = Phase(
            header=new_header,
            content="",
            scoring_entries=[],
            rollback_entries=[]
        )

        # Update document model
        doc.phases.append(new_phase)
        doc.current_phase = next_phase_name

        return doc

    finally:
        # Always release lock
        try:
            lock_path.unlink()
        except Exception:
            pass  # Ignore errors in cleanup


def main():
    """
    CLI entry point for task_roll.py.

    Usage: python task_roll.py [task_path]

    Args:
        task_path: Optional path to .TASK.md (default: ".TASK.md")
    """
    task_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"

    try:
        doc = advance_phase(task_path)
        print(f"✓ Advanced to phase: {doc.current_phase}")
        print(f"  Phase timestamp: {doc.phases[-1].header.timestamp.isoformat()}")
        print(f"  Total phases: {len(doc.phases)}")
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

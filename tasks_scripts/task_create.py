#!/usr/bin/env python3
"""
Task creation script: Initialize a new .TASK.md file.

Creates a new task document with:
- Initial phase: TASK_PLAN.DEFINE
- RFC 3339 timestamp
- Section marker for atomic updates
- Valid Pydantic model structure
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from tasks_scripts.models import TaskDocument, Phase, PhaseHeader
from tasks_scripts.task_state import validate_document_structure


def create_task(output_path: str = ".TASK.md") -> TaskDocument:
    """
    Create a new task document (.TASK.md) with initial structure.

    Args:
        output_path: Path where .TASK.md should be created (default: ".TASK.md")

    Returns:
        TaskDocument model representing the created task

    Raises:
        FileExistsError: If .TASK.md already exists
        IOError: If file cannot be written
    """
    path = Path(output_path)

    # Check if file already exists
    if path.exists():
        raise FileExistsError(f"Task file already exists: {output_path}")

    # Check if parent directory is writable
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    # Create initial phase header with current timestamp
    now = datetime.now(datetime.timezone.utc)
    timestamp_str = now.isoformat()

    # Create markdown content
    markdown_content = f"""# PHASE TASK_PLAN.DEFINE at {timestamp_str}

Task initialized. Ready for planning and development.

<!-- TASK_PLAN.DEFINE -->
"""

    # Validate structure before writing
    errors = validate_document_structure(markdown_content)
    if errors:
        raise ValueError(f"Invalid document structure: {errors}")

    # Write to file
    path.write_text(markdown_content, encoding="utf-8")

    # Create and return TaskDocument model
    header = PhaseHeader(
        phase_name="TASK_PLAN.DEFINE",
        timestamp=now
    )
    phase = Phase(
        header=header,
        content="Task initialized. Ready for planning and development."
    )
    doc = TaskDocument(
        phases=[phase],
        current_phase="TASK_PLAN.DEFINE",
        created_at=now
    )

    return doc


def main():
    """
    CLI entry point for task_create.py.

    Usage: python task_create.py [output_path]

    Args:
        output_path: Optional path to create .TASK.md (default: ".TASK.md")
    """
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"

    try:
        doc = create_task(output_path)
        print(f"✓ Task created: {output_path}")
        print(f"  Phase: {doc.current_phase}")
        print(f"  Created: {doc.created_at.isoformat()}")
        return 0
    except FileExistsError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except (IOError, ValueError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

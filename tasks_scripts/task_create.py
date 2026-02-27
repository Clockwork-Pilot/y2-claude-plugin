#!/usr/bin/env python3
"""
Task creation script: Initialize a new .TASK.md and .metrics file.

By design, ALL work flows EXCLUSIVELY through tasks_scripts/ lifecycle.
This module ensures both critical files are created together with consistent state.

Creates a new task with:
- .TASK.md: Initial TASK_PLAN.DEFINE phase with RFC 3339 timestamp
- .metrics: Empty metrics structure ready for first scoring
- Section markers (<!-- PHASE_NAME -->) for atomic regex updates
- Valid Pydantic model structure for complete lifecycle management

Design principle:
  The task lifecycle IS the workflow engine. Both files must exist from creation
  to represent the complete initial state: markdown for display, .metrics for
  storing measurements and coverage data (source of truth).
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from tasks_scripts.models import TaskDocument, Phase, PhaseHeader, MetricsFile
from tasks_scripts.task_state import validate_document_structure


def create_task(output_path: str = ".TASK.md") -> TaskDocument:
    """
    Create a new task with both .TASK.md and .metrics files.

    By design, ALL work flows EXCLUSIVELY through tasks_scripts lifecycle.
    Both files must exist from task creation to ensure complete initial state.

    Creates:
      1. .TASK.md: Markdown document with TASK_PLAN.DEFINE phase (display & version control)
      2. .metrics: Empty JSON structure ready for first collect_metrics call (source of truth)

    The section marker <!-- TASK_PLAN.DEFINE --> enables atomic regex-based updates
    without full document rewrites. This is critical for concurrent-safe modifications.

    Args:
        output_path: Path where .TASK.md should be created (default: ".TASK.md")

    Returns:
        TaskDocument model representing the created task

    Raises:
        FileExistsError: If .TASK.md or .metrics already exists
        IOError: If files cannot be written
        ValueError: If document structure is invalid
    """
    path = Path(output_path)
    metrics_path = path.parent / ".metrics"

    # Validate parent directory exists and is writable
    if not path.parent.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise IOError(f"Cannot create parent directory: {path.parent}") from e

    # Check if task file already exists
    if path.exists():
        raise FileExistsError(f"Task file already exists: {output_path}")

    # Check if metrics file already exists
    if metrics_path.exists():
        raise FileExistsError(f"Metrics file already exists: {metrics_path}")

    # Create initial phase header with current timestamp
    now = datetime.now(timezone.utc)
    timestamp_str = now.isoformat()

    # === Create .TASK.md ===
    # Markdown content: human-readable progress document with atomic update markers
    markdown_content = f"""# PHASE TASK_PLAN.DEFINE at {timestamp_str}

Task initialized. Ready for planning and development.

<!-- TASK_PLAN.DEFINE -->
"""

    # Validate structure before writing
    errors = validate_document_structure(markdown_content)
    if errors:
        raise ValueError(f"Invalid document structure: {errors}")

    # Write markdown file
    path.write_text(markdown_content, encoding="utf-8")

    # === Create .metrics ===
    # JSON file: source of truth for all metrics and coverage data
    # Initialize with empty structure. Keys will be populated during collect_metrics calls.
    metrics_data = {}
    metrics_json = json.dumps(metrics_data, indent=2)
    metrics_path.write_text(metrics_json, encoding="utf-8")

    # === Create TaskDocument model ===
    # Represents the complete task state in memory
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

    Creates both .TASK.md and .metrics files for exclusive lifecycle management.

    Usage: python task_create.py [output_path]

    Args:
        output_path: Optional path to create .TASK.md (default: ".TASK.md")
                    .metrics will be created in the same directory
    """
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"

    try:
        doc = create_task(output_path)

        # Show both files created
        task_path = Path(output_path)
        metrics_path = task_path.parent / ".metrics"

        print(f"✓ Task created successfully")
        print(f"  .TASK.md: {output_path}")
        print(f"  .metrics: {metrics_path}")
        print(f"  Phase: {doc.current_phase}")
        print(f"  Created: {doc.created_at.isoformat()}")
        print()
        print(f"Ready for exclusive lifecycle management through tasks_scripts/")
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

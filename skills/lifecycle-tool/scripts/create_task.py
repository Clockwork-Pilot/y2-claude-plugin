#!/usr/bin/env python3
"""Create a new task.json knowledge document.

Creates task.json at project root with a Task node. If task.json already exists,
prints a message and exits without modifying the file.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from knowledge_tool.models import Doc, Task


def create_task():
    """Create task.json at project root if it doesn't already exist."""
    task_file = Path("task.json")

    # Check if task file already exists
    if task_file.exists():
        print(f"✗ Task file already exists: {task_file}")
        sys.exit(1)

    # Create initial plan doc with metadata
    now = datetime.now().isoformat()
    plan = Doc(
        id="plan",
        label="Task Plan",
        metadata={"created_at": now, "updated_at": now},
    )

    # Create task with initial plan
    task = Task(
        id="task_1",
        plan=plan,
        iterations=None,
    )

    # Write to JSON file
    try:
        with open(task_file, "w") as f:
            json.dump(json.loads(task.model_dump_json()), f, indent=2)
        print(f"✓ Created task file: {task_file}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error creating task file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_task()

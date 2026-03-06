#!/usr/bin/env python3
"""Create a new task.json knowledge document.

Creates task.json at project root with a Task node. If task.json already exists,
prints a message and exits without modifying the file.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import importlib.util

# Setup knowledge_tool module
knowledge_tool_root = Path(__file__).parent.parent.parent.parent / "knowledge_tool" / "knowledge_tool"
src_dir = knowledge_tool_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(knowledge_tool_root) not in sys.path:
    sys.path.insert(0, str(knowledge_tool_root))

# Create knowledge_tool module alias
spec = importlib.util.spec_from_file_location(
    "knowledge_tool",
    str(src_dir / "__init__.py"),
    submodule_search_locations=[str(src_dir)]
)
knowledge_tool_module = importlib.util.module_from_spec(spec)
sys.modules["knowledge_tool"] = knowledge_tool_module
spec.loader.exec_module(knowledge_tool_module)

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

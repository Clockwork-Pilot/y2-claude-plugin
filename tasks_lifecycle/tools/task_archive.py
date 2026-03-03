#!/usr/bin/env python3
"""Archive a completed task to tasks_history folder.

Moves task.json to tasks_history/ with naming convention: TIMESTAMP-task-NAME.json
For manual calling only.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from shutil import move

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tasks_lifecycle.knowledge_models.task_model import Task


def archive_task(task_file: str = "task.json") -> int:
    """Archive a completed task to tasks_history folder.

    Args:
        task_file: Path to task.json file to archive

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_path = Path(task_file)

    # Check if task file exists
    if not task_path.exists():
        print(f"✗ Task file not found: {task_file}")
        return 1

    try:
        # Load task document to get ID
        with open(task_path, "r") as f:
            task_data = json.load(f)

        task = Task(**task_data)
        task_id = task.id

        # Generate markdown before moving file
        markdown_content = task.render()

        # Create tasks_history directory if it doesn't exist
        history_dir = Path("tasks_history")
        history_dir.mkdir(exist_ok=True)

        # Generate archive filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_name = f"{timestamp}-task-{task_id}.json"
        archive_path = history_dir / archive_name

        # Move file to history
        move(str(task_path), str(archive_path))

        markdown_name = f"{timestamp}-task-{task_id}.md"
        markdown_path = history_dir / markdown_name

        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        print(f"✓ Archived task {task_id}")
        print(f"  JSON: {archive_path}")
        print(f"  MD:   {markdown_path}")
        return 0

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {task_file}: {e}")
        return 1
    except ValueError as e:
        print(f"✗ Invalid task data: {e}")
        return 1
    except Exception as e:
        print(f"✗ Error archiving task: {e}")
        return 1


if __name__ == "__main__":
    task_file = sys.argv[1] if len(sys.argv) > 1 else "task.json"
    exit_code = archive_task(task_file)
    sys.exit(exit_code)

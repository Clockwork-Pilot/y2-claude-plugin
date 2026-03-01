#!/usr/bin/env python3
"""Roll task to next iteration, recording metrics from completed iteration.

Called when an iteration finishes. Updates task.json with iteration metrics
and creates a new iteration entry.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from knowledge_models import Task, Iteration, CodeStats, TaskTestMetrics
from .task_metrics import collect_metrics


def roll_task(task_file: str = "task.json", skip_metrics: bool = False) -> int:
    """Record completion of current iteration and prepare for next.

    Args:
        task_file: Path to task.json file
        skip_metrics: If True, don't collect metrics (use for testing)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_path = Path(task_file)

    # Check if task file exists
    if not task_path.exists():
        print(f"✗ Task file not found: {task_file}")
        return 1

    try:
        # Load task document
        with open(task_path, "r") as f:
            task_data = json.load(f)

        # Parse as Task model
        task = Task(**task_data)

        # Collect metrics for current iteration
        now = datetime.now().isoformat()

        if skip_metrics:
            # For testing: use default metrics
            metrics = {
                "code_stats": {"added_lines": 0, "removed_lines": 0, "files_changed": 0},
                "tests_stats": {"passed": 0, "total": 0},
                "coverage_stats_by_tests": {},
            }
        else:
            metrics = collect_metrics()

        # Determine next iteration ID
        if task.iterations:
            # Find highest iteration number
            iteration_ids = [iid for iid in task.iterations.keys()]
            if iteration_ids:
                # Extract numbers from iteration IDs (e.g., "iteration_1" -> 1)
                numbers = []
                for iid in iteration_ids:
                    try:
                        num = int(iid.split("_")[-1])
                        numbers.append(num)
                    except (ValueError, IndexError):
                        pass
                next_num = max(numbers) + 1 if numbers else 1
            else:
                next_num = 1
        else:
            next_num = 1

        iteration_id = f"iteration_{next_num}"

        # Create new iteration with metrics
        code_stats = CodeStats(**metrics["code_stats"])
        test_stats = TaskTestMetrics(**metrics["tests_stats"])

        new_iteration = Iteration(
            id=iteration_id,
            metadata={"created_at": now, "updated_at": now},
            code_stats=code_stats,
            tests_stats=test_stats,
            coverage_stats_by_tests=metrics["coverage_stats_by_tests"]
            or None,  # Only include if not empty
        )

        # Add to iterations dict
        if task.iterations is None:
            task.iterations = {}
        task.iterations[iteration_id] = new_iteration

        # Write updated task back to file
        with open(task_path, "w") as f:
            json.dump(json.loads(task.model_dump_json(exclude_none=True)), f, indent=2)

        print(f"✓ Rolled task with iteration {iteration_id}")
        print(f"  Code: +{code_stats.added_lines} -{code_stats.removed_lines} ({code_stats.files_changed} files)")
        print(
            f"  Tests: {test_stats.passed}/{test_stats.total} passed ({test_stats.pass_rate:.1f}%)"
        )
        return 0

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {task_file}: {e}")
        return 1
    except ValueError as e:
        print(f"✗ Invalid task data: {e}")
        return 1
    except Exception as e:
        print(f"✗ Error rolling task: {e}")
        return 1


if __name__ == "__main__":
    skip_metrics = "--skip-metrics" in sys.argv
    exit_code = roll_task(skip_metrics=skip_metrics)
    sys.exit(exit_code)

#!/usr/bin/env python3
"""Task completion orchestration script.

Validates a completed task by running:
1. task_features_checker.py - Task-level constraint validation
2. check_project_constraints.py - Project-level validation

On success, creates a timestamped Spec snapshot in project-spec/raw-tasks/
containing Spec data extracted from the completed task.k.json.

Preserves the original task.k.json and task.k.md files (does not delete them).
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime


def run_task_features_checker(task_path: str) -> int:
    """Execute task-level constraint validation.

    Args:
        task_path: Path to task.k.json file

    Returns:
        Exit code from task_features_checker.py
    """
    print("🔍 Running task-level constraint validation...")
    result = subprocess.run(
        [
            'python3',
            'constraints_tool/constraints_tool/task_features_checker.py',
            task_path,
            '--output-checks-path', 'checks_results.k.json'
        ]
    )
    return result.returncode


def run_project_constraints_checker() -> int:
    """Execute project-level constraint validation.

    Returns:
        Exit code from check_project_constraints.py
    """
    print("\n🌍 Running project-level constraint validation...")
    result = subprocess.run(
        ['python3', 'constraints_tool/constraints_tool/check_project_constraints.py']
    )
    return result.returncode


def extract_spec_from_task(task_path: str) -> dict:
    """Extract Spec data from completed task.k.json.

    Args:
        task_path: Path to task.k.json file

    Returns:
        Spec object/dict from task.spec
    """
    with open(task_path, 'r') as f:
        task_data = json.load(f)

    spec_data = task_data.get('spec', {})
    return spec_data


def create_spec_snapshot(spec_data: dict, task_id: str, output_dir: str) -> Path:
    """Create timestamped Spec snapshot in project-spec/raw-tasks/.

    Args:
        spec_data: Spec data extracted from task
        task_id: Task ID from the task document
        output_dir: Output directory for snapshots

    Returns:
        Path to created Spec snapshot file
    """
    # Generate ISO8601 timestamp for filename
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}-{task_id}.k.json"
    filepath = Path(output_dir) / filename

    # Create Spec knowledge document structure
    spec_document = {
        "type": "Spec",
        "model_version": spec_data.get('model_version', 1),
        **spec_data
    }

    # Write Spec snapshot
    with open(filepath, 'w') as f:
        json.dump(spec_document, f, indent=2)

    return filepath


def complete_task(task_path: str = 'task.k.json', output_dir: str = 'project-spec/raw-tasks') -> int:
    """Orchestrate task completion workflow.

    Runs constraint validation and creates Spec snapshot on success.

    Args:
        task_path: Path to task.k.json file
        output_dir: Directory for Spec snapshots

    Returns:
        Exit code: 0 on success, non-zero on failure
    """
    print(f"📋 Complete Task Workflow")
    print(f"   Task: {task_path}")
    print(f"   Output: {output_dir}\n")

    # Step 1: Run task-level validation
    task_exit_code = run_task_features_checker(task_path)
    if task_exit_code != 0:
        print("\n✗ Task-level constraints failed")
        return task_exit_code

    # Step 2: Run project-level validation
    project_exit_code = run_project_constraints_checker()
    if project_exit_code != 0:
        print("\n✗ Project-level constraints failed")
        return project_exit_code

    # Step 3: Both validations succeeded - create Spec snapshot
    print("\n✅ All validations passed - creating Spec snapshot...")
    try:
        # Extract task ID
        with open(task_path, 'r') as f:
            task_data = json.load(f)
        task_id = task_data.get('id', 'unknown_task')

        # Extract Spec data
        spec_data = extract_spec_from_task(task_path)

        # Create snapshot
        snapshot_path = create_spec_snapshot(spec_data, task_id, output_dir)
        print(f"💾 Spec snapshot created: {snapshot_path}")

        # Verify task.k.json still exists (not deleted)
        if not Path(task_path).exists():
            print(f"✗ Error: {task_path} was deleted during completion!")
            return 1

        print(f"✓ Original {task_path} preserved")
        print("\n✓ Task completion workflow successful")
        return 0

    except Exception as e:
        print(f"\n✗ Error creating Spec snapshot: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for task completion orchestration."""
    parser = argparse.ArgumentParser(
        description="Orchestrate task completion with constraint validation and Spec snapshot generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Complete default task
  python3 complete_task.py

  # Complete specific task
  python3 complete_task.py --task my-task.k.json --output project-spec/raw-tasks
        """
    )

    parser.add_argument(
        '--task',
        default='task.k.json',
        help='Path to task.k.json file (default: task.k.json)'
    )

    parser.add_argument(
        '--output',
        default='project-spec/raw-tasks',
        help='Directory for Spec snapshots (default: project-spec/raw-tasks)'
    )

    args = parser.parse_args()

    return complete_task(args.task, args.output)


if __name__ == '__main__':
    sys.exit(main())

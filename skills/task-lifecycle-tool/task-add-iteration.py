#!/usr/bin/env python3
"""Add iteration to task document with feature validation stats and diff tracking."""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add paths for imports
_script_dir = Path(__file__).parent.parent.parent
_knowledge_tool_src = _script_dir / "knowledge_tool" / "knowledge_tool" / "src"
_knowledge_tool_root = _script_dir / "knowledge_tool" / "knowledge_tool"
_constraints_tool = _script_dir / "constraints_tool" / "constraints_tool"

sys.path.insert(0, str(_knowledge_tool_src))
sys.path.insert(0, str(_knowledge_tool_root))
sys.path.insert(0, str(_constraints_tool))

from models import Task, FeaturesStats, FeaturesStatsDiff, Iteration
from patch_knowledge_document import apply_json_patch
from check_spec_constraints import check_constraints


def get_last_iteration_number(task: Task) -> int:
    """Get the last iteration number from task document.

    Args:
        task: Task document

    Returns:
        Last iteration number, or 0 if no iterations exist
    """
    if not task.iterations:
        return 0

    # Extract numbers from iteration IDs like "iteration_1", "iteration_2", etc.
    numbers = []
    for iter_id in task.iterations.keys():
        try:
            if iter_id.startswith("iteration_"):
                num = int(iter_id.split("_")[1])
                numbers.append(num)
        except (ValueError, IndexError):
            pass

    return max(numbers) if numbers else 0


def create_iteration(
    task: Task,
    iteration_num: int,
    features_stats: Optional[FeaturesStats] = None,
    tests_stats: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create iteration data structure with features_stats and diff.

    Args:
        task: Task document
        iteration_num: Iteration number to create
        features_stats: FeaturesStats from constraint checking
        tests_stats: Optional test statistics

    Returns:
        Iteration data as dict ready for JSON patch
    """
    iteration_id = f"iteration_{iteration_num}"

    # Calculate FeaturesStatsDiff if we have previous iteration
    features_stats_diff = None
    if features_stats:
        # Find previous iteration
        previous_stats = None
        if iteration_num > 1:
            prev_iter_id = f"iteration_{iteration_num - 1}"
            if task.iterations and prev_iter_id in task.iterations:
                prev_iter = task.iterations[prev_iter_id]
                if prev_iter.features_stats:
                    previous_stats = prev_iter.features_stats

        # Calculate diff
        features_stats_diff = features_stats.diff(previous_stats)

    # Build iteration data
    iteration_data: Dict[str, Any] = {
        "type": "Iteration",
        "model_version": 1,
        "id": iteration_id,
        "children": None,
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "iteration_number": iteration_num,
        },
        "code_stats": None,
        "tests_stats": tests_stats,
        "coverage_stats_by_tests": None,
        "features_stats": None,
        "features_stats_diff": None,
    }

    # Add features_stats if provided
    if features_stats:
        iteration_data["features_stats"] = json.loads(features_stats.model_dump_json(exclude_none=True))

    # Add features_stats_diff if calculated
    if features_stats_diff:
        # Convert set to list for JSON serialization
        diff_data = {
            "improved": features_stats_diff.improved,
            "regressed": features_stats_diff.regressed,
            "still_failing": list(features_stats_diff.still_failing),
        }
        iteration_data["features_stats_diff"] = diff_data

    return iteration_data


def add_iteration_to_task(
    task_json_path: str,
    iteration_num: Optional[int] = None,
    tests_stats: Optional[Dict[str, Any]] = None,
) -> int:
    """Add iteration to task document.

    Runs constraint checks, creates iteration with features_stats and diff,
    and patches task-iterations.k.json with the new iteration.

    Args:
        task_json_path: Path to task-iterations.k.json
        iteration_num: Optional iteration number (auto-incremented if not provided)
        tests_stats: Optional test statistics to include

    Returns:
        Exit code: 0=success, 1=error, 2=constraints failed
    """
    task_path = Path(task_json_path)

    # Load task document
    try:
        with open(task_path, 'r') as f:
            task_data = json.load(f)
        task = Task.model_validate(task_data)
    except Exception as e:
        print(f"✗ Error loading task: {e}", file=sys.stderr)
        return 1

    # Run constraint checks
    print("🔍 Running constraint checks...")
    try:
        checks_results, features_stats = check_constraints(
            task_json_path,
            output_checks_path=None  # Don't save to file, just use for stats
        )
    except Exception as e:
        print(f"✗ Error running constraint checks: {e}", file=sys.stderr)
        return 1

    # Determine iteration number
    if iteration_num is None:
        last_num = get_last_iteration_number(task)
        iteration_num = last_num + 1

    iteration_id = f"iteration_{iteration_num}"

    # Create iteration with stats
    iteration_data = create_iteration(task, iteration_num, features_stats, tests_stats)

    # Build JSON patch to add iteration
    patch_ops = [{
        "op": "add",
        "path": f"/iterations/{iteration_id}",
        "value": iteration_data,
    }]

    # Apply patch to task-iterations.k.json
    print(f"📝 Adding {iteration_id} to task-iterations.k.json...")
    error = apply_json_patch(str(task_path), json.dumps(patch_ops))
    if error:
        print(f"✗ Failed to add iteration: {error.error}", file=sys.stderr)
        return 1

    # Print summary
    print(f"\n✅ Iteration {iteration_id} added successfully")
    if features_stats:
        passing = sum(1 for v in features_stats.features_checks.values() if v)
        failing = sum(1 for v in features_stats.features_checks.values() if not v)
        total = len(features_stats.features_checks)
        print(f"\n📊 Feature Stats Summary:")
        print(f"   Overall: {passing}/{total} features passed")
        if failing > 0:
            print(f"   Failed: {failing} features")

    # Return appropriate exit code
    if features_stats and sum(1 for v in features_stats.features_checks.values() if not v) > 0:
        print("\n⚠️  Some constraints failed - fix them before next iteration")
        return 2

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add iteration to task document with constraint validation stats"
    )

    parser.add_argument(
        'task_path',
        help='Path to task-iterations.k.json file'
    )

    parser.add_argument(
        '--iteration-number',
        type=int,
        default=None,
        help='Iteration number (auto-incremented if not provided)'
    )

    parser.add_argument(
        '--tests-stats',
        type=json.loads,
        default=None,
        help='Test statistics as JSON dict (e.g., \'{"passed": 10, "total": 12}\')'
    )

    args = parser.parse_args()

    return add_iteration_to_task(
        args.task_path,
        iteration_num=args.iteration_number,
        tests_stats=args.tests_stats,
    )


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Add iteration to task document with feature validation stats and diff tracking."""

import json
import sys
import argparse
import pytest
from pathlib import Path
from typing import Optional, Dict, Any

# Add paths for imports
_script_dir = Path(__file__).parent.parent.parent
_knowledge_tool_src = _script_dir / "knowledge_tool" / "knowledge_tool" / "src"
_knowledge_tool_root = _script_dir / "knowledge_tool" / "knowledge_tool"
_constraints_tool = _script_dir / "constraints_tool" / "constraints_tool"

sys.path.insert(0, str(_knowledge_tool_src))
sys.path.insert(0, str(_knowledge_tool_root))
sys.path.insert(0, str(_constraints_tool))

from models import Task, FeaturesStats, FeaturesStatsDiff, Iteration, TaskTestMetrics
from models.metadata_model import Metadata
from patch_knowledge_document import apply_json_patch
from check_spec_constraints import check_constraints

_project_root = _script_dir


class _ResultCollector:
    """Inline pytest plugin that collects pass/fail results without subprocess."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed_tests: Dict[str, str] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when != 'call':
            return
        if report.passed:
            self.passed += 1
        elif report.failed:
            # Keep only last two node-id segments: TestClass::test_method
            test_id = '::'.join(report.nodeid.split('::')[-2:])
            error = ''
            if report.longrepr:
                lines = str(report.longrepr).splitlines()
                error = lines[-1][:100] if lines else ''
            self.failed_tests[test_id] = error


def run_pytest() -> tuple:
    """Run pytest via API from project root; return structured metrics.

    Returns:
        (exit_code, TaskTestMetrics)
    """
    collector = _ResultCollector()
    try:
        exit_code = int(pytest.main(['--tb=line', '-q'], plugins=[collector]))
    except Exception as e:
        print(f"✗ Error running pytest: {e}", file=sys.stderr)
        return 1, TaskTestMetrics()
    metrics = TaskTestMetrics(
        passed=collector.passed,
        total=collector.passed + len(collector.failed_tests),
        failed_tests=collector.failed_tests,
    )
    if exit_code != 0:
        print("✗ Tests failed — recording iteration anyway", file=sys.stderr)
    return exit_code, metrics


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


def build_summary(features_stats: Optional[FeaturesStats]) -> str:
    """Auto-generate iteration summary from constraint results."""
    if not features_stats or not features_stats.failed:
        return "All features passing"
    failing = sorted(features_stats.failed.keys())
    summary = f"{len(failing)} feature(s) failing: {', '.join(failing)}"
    return summary[:100]


def create_iteration(
    task: Task,
    iteration_num: int,
    features_stats: Optional[FeaturesStats] = None,
    tests_metrics: Optional[TaskTestMetrics] = None,
    summary: Optional[str] = None,
) -> Dict[str, Any]:
    """Create iteration data structure with features_stats and diff.

    Args:
        task: Task document
        iteration_num: Iteration number to create
        features_stats: FeaturesStats from constraint checking
        tests_metrics: Optional TaskTestMetrics from pytest run

    Returns:
        Iteration data as dict ready for JSON patch
    """
    iteration_id = f"iteration_{iteration_num}"

    # Calculate FeaturesStatsDiff if we have previous iteration
    features_stats_diff = None
    if features_stats:
        previous_stats = None
        if iteration_num > 1:
            prev_iter_id = f"iteration_{iteration_num - 1}"
            if task.iterations and prev_iter_id in task.iterations:
                prev_iter = task.iterations[prev_iter_id]
                if prev_iter.features_stats:
                    previous_stats = prev_iter.features_stats
        features_stats_diff = features_stats.diff(previous_stats)

    # Build summary from features_stats if not provided
    if summary is None:
        summary = build_summary(features_stats)

    # Serialize tests_metrics to dict if provided
    tests_stats = json.loads(tests_metrics.model_dump_json(exclude_none=True)) if tests_metrics else None

    # Build iteration data
    iteration_data: Dict[str, Any] = {
        "type": "Iteration",
        "model_version": 2,
        "id": iteration_id,
        "summary": summary,
        "metadata": {**json.loads(Metadata.now().model_dump_json(exclude_none=True)), "iteration_number": iteration_num},
        "tests_stats": tests_stats,
        "features_stats": None,
        "features_stats_diff": None,
    }

    if features_stats:
        iteration_data["features_stats"] = json.loads(features_stats.model_dump_json(exclude_none=True))

    if features_stats_diff:
        iteration_data["features_stats_diff"] = json.loads(features_stats_diff.model_dump_json())

    return iteration_data


def add_iteration_to_task(
    task_json_path: str,
    iteration_num: Optional[int] = None,
) -> int:
    """Add iteration to task document.

    Runs pytest and constraint checks, creates iteration with features_stats and diff,
    and patches task-iterations.k.json with the new iteration.
    Always records the iteration even when tests fail.

    Args:
        task_json_path: Path to task-iterations.k.json
        iteration_num: Optional iteration number (auto-incremented if not provided)

    Returns:
        Exit code: 0=success, 1=error, 2=tests or constraints failed
    """
    # Run pytest as prerequisite — always continues to record iteration
    print("🧪 Running tests...")
    pytest_exit, tests_metrics = run_pytest()

    task_path = Path(task_json_path)

    # Load task document
    try:
        with open(task_path, 'r') as f:
            task_data = json.load(f)
        task = Task.model_validate(task_data)
    except Exception as e:
        print(f"✗ Error loading task: {e}", file=sys.stderr)
        return 1

    # Derive spec path (task-spec.k.json lives alongside task-iterations.k.json)
    spec_json_path = str(task_path.parent / task_path.name.replace("task-iterations", "task-spec"))

    # Run constraint checks
    print("🔍 Running constraint checks...")
    try:
        checks_results, features_stats = check_constraints(
            spec_json_path,
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
    iteration_data = create_iteration(task, iteration_num, features_stats, tests_metrics)

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
    if tests_metrics.total > 0:
        print(f"\n🧪 Tests: {tests_metrics.passed}/{tests_metrics.total} passed")
        if tests_metrics.failed_tests:
            for tid, err in list(tests_metrics.failed_tests.items())[:5]:
                print(f"   ✗ {tid}" + (f": {err}" if err else ""))
    if features_stats and features_stats.failed:
        failing = len(features_stats.failed)
        print(f"\n📊 Feature Stats: {failing} feature(s) failing")
        for fid in sorted(features_stats.failed):
            print(f"   ✗ {fid}")

    # Return 2 if tests failed or any constraints failed
    if pytest_exit != 0:
        print("\n⚠️  Tests failed — fix failing tests before next iteration")
        return 2
    if features_stats and features_stats.failed:
        print("\n⚠️  Some constraints failed — fix them before next iteration")
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

    args = parser.parse_args()

    return add_iteration_to_task(
        args.task_path,
        iteration_num=args.iteration_number,
    )


if __name__ == '__main__':
    sys.exit(main())

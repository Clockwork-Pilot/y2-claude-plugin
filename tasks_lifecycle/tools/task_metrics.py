#!/usr/bin/env python3
"""Collect metrics for task iterations.

Provides metrics for:
- code_stats: file changes (+added lines, -removed lines)
- tests_stats: X pass / from Y
- coverage_stats_by_tests: Dict[test_name -> lines_covered]
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tasks_lifecycle.knowledge_models.task_model import CodeStats, TaskTestMetrics


def get_code_stats(
    base_ref: str = "HEAD~1", target_ref: str = "HEAD"
) -> CodeStats:
    """Calculate code change statistics between two git refs.

    Args:
        base_ref: Starting git reference (default: previous commit)
        target_ref: Ending git reference (default: current commit)

    Returns:
        CodeStats with added_lines, removed_lines, and files_changed
    """
    try:
        # Get diff stats between refs
        cmd = ["git", "diff", "--numstat", f"{base_ref}...{target_ref}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        added_lines = 0
        removed_lines = 0
        files_changed = 0

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                files_changed += 1
                try:
                    added_lines += int(parts[0]) if parts[0] != "-" else 0
                    removed_lines += int(parts[1]) if parts[1] != "-" else 0
                except (ValueError, IndexError):
                    pass

        return CodeStats(
            added_lines=added_lines,
            removed_lines=removed_lines,
            files_changed=files_changed,
        )
    except subprocess.CalledProcessError:
        # If git diff fails, return zeros
        return CodeStats()


def get_test_stats(test_output: Optional[str] = None) -> TaskTestMetrics:
    """Calculate test statistics from pytest output.

    Args:
        test_output: Optional pytest output string. If None, runs pytest.

    Returns:
        TestStats with passed and total test counts
    """
    if test_output is None:
        try:
            # Run pytest with json report
            result = subprocess.run(
                ["python", "-m", "pytest", "--tb=short", "-v"],
                capture_output=True,
                text=True,
            )
            test_output = result.stdout + result.stderr
        except subprocess.CalledProcessError as e:
            test_output = e.stdout or ""

    # Parse test results from output
    passed = 0
    total = 0

    # Simple parsing: look for PASSED/FAILED in output
    for line in test_output.split("\n"):
        if " PASSED" in line:
            passed += 1
            total += 1
        elif " FAILED" in line:
            total += 1

    # Try to extract summary line (e.g., "5 passed in 0.23s")
    for line in test_output.split("\n"):
        if "passed" in line.lower():
            parts = line.split()
            for i, part in enumerate(parts):
                if "passed" in part.lower() and i > 0:
                    try:
                        passed = int(parts[i - 1])
                    except ValueError:
                        pass

    return TaskTestMetrics(passed=passed, total=total)


def get_coverage_stats_by_tests() -> Dict[str, int]:
    """Get coverage statistics per test.

    Returns:
        Dictionary mapping test names to lines covered
    """
    coverage_stats = {}

    try:
        # Run pytest with coverage
        result = subprocess.run(
            [
                "python",
                "-m",
                "pytest",
                "--cov=.",
                "--cov-report=term",
                "-v",
                "--tb=short",
            ],
            capture_output=True,
            text=True,
        )

        output = result.stdout + result.stderr

        # Parse coverage output
        for line in output.split("\n"):
            if "PASSED" in line:
                # Extract test name from line like "tests/test_foo.py::test_func PASSED"
                parts = line.split()
                if len(parts) >= 2:
                    test_name = parts[0].split("::")[-1]
                    # For now, assign default coverage
                    coverage_stats[test_name] = 0

    except subprocess.CalledProcessError:
        pass

    return coverage_stats if coverage_stats else {}


def collect_metrics() -> Dict:
    """Collect all metrics for current iteration.

    Returns:
        Dictionary with code_stats, tests_stats, and coverage_stats_by_tests
    """
    code_stats = get_code_stats()
    test_stats = get_test_stats()
    coverage_stats = get_coverage_stats_by_tests()

    return {
        "code_stats": code_stats.model_dump(),
        "tests_stats": test_stats.model_dump(),
        "coverage_stats_by_tests": coverage_stats,
    }


if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=2))

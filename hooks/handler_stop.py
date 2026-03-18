#!/usr/bin/env python3
"""Handler for Stop event - checks constraints before allowing stop."""

import sys
import json
import subprocess

from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger
from config import PROJECT_ROOT

logger = setup_logger(__name__)

PLUGIN_ROOT = Path(__file__).parent.parent
_iteration_script = PLUGIN_ROOT / "skills" / "task-lifecycle-tool" / "task-add-iteration.py"


def check_constraints() -> int:
    """Run constraint checks on task document.

    Returns:
        Exit code: 0=all passed, 2=constraints failed, 1=error
    """
    task_json = PROJECT_ROOT / "task-iterations.k.json"

    if not task_json.exists():
        return 0

    checker_script = PLUGIN_ROOT / "constraints_tool" / "constraints_tool" / "check_spec_constraints.py"

    try:
        result = subprocess.run(
            [sys.executable, str(checker_script), str(task_json)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode

    except Exception as e:
        logger.error(f"Error running constraint checks: {e}")
        return 1


def add_iteration() -> int:
    """Record this iteration by calling task-add-iteration.py via subprocess.

    Returns:
        Exit code: 0=success, 2=tests failed, non-zero=error
    """
    task_json = PROJECT_ROOT / "task-iterations.k.json"
    if not task_json.exists():
        return 0

    if not _iteration_script.exists():
        logger.warning(f"task-add-iteration.py not found at {_iteration_script}")
        return 0

    try:
        result = subprocess.run(
            [sys.executable, str(_iteration_script), str(task_json)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.stdout:
            logger.info(result.stdout)
        if result.returncode != 0 and result.stderr:
            logger.warning(result.stderr)
        return result.returncode
    except Exception as e:
        logger.error(f"Error adding iteration: {e}")
        return 1


def get_recurring_failures() -> list:
    """Find features failing in all of the last 3 iterations.

    Returns:
        List of feature IDs that have been failing consistently
    """
    task_json = PROJECT_ROOT / "task-iterations.k.json"
    if not task_json.exists():
        return []

    try:
        with open(task_json) as f:
            task_data = json.load(f)

        iterations = task_data.get("iterations", {})
        if not iterations:
            return []

        sorted_iters = sorted(
            [(k, v) for k, v in iterations.items() if k.startswith("iteration_")],
            key=lambda x: int(x[0].split("_")[1])
        )

        last_3 = sorted_iters[-3:]
        if len(last_3) < 3:
            return []

        failing_sets = []
        for _, iter_data in last_3:
            fs = iter_data.get("features_stats", {})
            if not fs:
                break
            checks = fs.get("features_checks", {})
            failing_sets.append({fid for fid, passed in checks.items() if not passed})

        if len(failing_sets) < 3:
            return []

        return list(failing_sets[0] & failing_sets[1] & failing_sets[2])

    except Exception as e:
        logger.error(f"Error reading iterations: {e}")
        return []


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        # Run constraint checks
        check_exit_code = check_constraints()

        # Handle constraint failures
        if check_exit_code == 2:
            recurring = get_recurring_failures()
            reason = "Constraints violated, fix features implementation to satisfy them."
            if recurring:
                reason += f" Recurring failures (3+ iterations): {', '.join(sorted(recurring))}."

            print(json.dumps({"decision": "block", "reason": reason}))

            logger.info(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'event': 'Stop',
                'status': 'blocked',
                'reason': 'Constraint checks failed',
                'recurring_failures': recurring,
                'data': hook_input,
            }))
            sys.exit(2)

        # Constraints passed — record iteration (runs pytest internally).
        # Chain: add_iteration() → subprocess task-add-iteration.py → run_pytest()
        #        → if exit 2, propagates back to add_iteration() → main() blocks with decision: block.
        iteration_exit_code = add_iteration()

        if iteration_exit_code == 2:
            print(json.dumps({"decision": "block", "reason": "Tests failed — fix failing tests before stopping."}))
            logger.info(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'event': 'Stop',
                'status': 'blocked',
                'reason': 'Tests failed',
                'data': hook_input,
            }))
            sys.exit(2)

        logger.info(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'event': 'Stop',
            'status': 'allowed',
            'data': hook_input,
        }))
        sys.exit(0)

    except Exception as e:
        logger.error(f"Error in Stop handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()

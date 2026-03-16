#!/usr/bin/env python3
"""Handler for Stop event - checks constraints before allowing stop."""

import sys
import json
import subprocess

from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger

logger = setup_logger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent


def check_constraints() -> int:
    """Run constraint checks on task document.

    Returns:
        Exit code: 0=all passed, 2=constraints failed, 1=error
    """
    task_json = PROJECT_ROOT / "task.k.json"

    if not task_json.exists():
        # No task document to check
        return 0

    # Run task_features_checker.py synchronously
    checker_script = PROJECT_ROOT / "constraints_tool" / "constraints_tool" / "task_features_checker.py"

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


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        # Run constraint checks
        check_exit_code = check_constraints()

        # Handle constraint failures
        if check_exit_code == 2:
            # Constraints failed - block the stop
            decision_block = {
                "decision": "block",
                "reason": "Constraints failed, fix them first"
            }
            print(json.dumps(decision_block))

            log_message = {
                'timestamp': datetime.now().isoformat(),
                'event': 'Stop',
                'status': 'blocked',
                'reason': 'Constraint checks failed',
                'data': hook_input
            }
            logger.info(json.dumps(log_message))
            sys.exit(2)

        # Constraints passed or no constraints - allow stop
        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'Stop',
            'status': 'allowed',
            'data': hook_input
        }
        logger.info(json.dumps(log_message))
        sys.exit(0)

    except Exception as e:
        logger.error(f"Error in Stop handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Execute bash constraints and capture results."""

import subprocess
from datetime import datetime

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool" / "src"))

from models import ConstraintBash, ConstraintBashResult


def execute_bash_constraint(constraint: ConstraintBash) -> ConstraintBashResult:
    """Execute a bash constraint and capture the result.

    Args:
        constraint: ConstraintBash with cmd to execute

    Returns:
        ConstraintBashResult with verdict (True if cmd succeeds) and output
    """
    try:
        result = subprocess.run(
            constraint.cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Command success = return code 0
        verdict = result.returncode == 0

        # Combine stdout and stderr, truncate to 500 chars
        output = (result.stdout + result.stderr)[:500]

        return ConstraintBashResult(
            constraint_id=constraint.id,
            verdict=verdict,
            shrunken_output=output if output else f"Exit code: {result.returncode}",
            timestamp=datetime.now()
        )

    except subprocess.TimeoutExpired:
        return ConstraintBashResult(
            constraint_id=constraint.id,
            verdict=False,
            shrunken_output="Command timed out after 30 seconds",
            timestamp=datetime.now()
        )

    except Exception as e:
        return ConstraintBashResult(
            constraint_id=constraint.id,
            verdict=False,
            shrunken_output=f"Error: {str(e)[:500]}",
            timestamp=datetime.now()
        )

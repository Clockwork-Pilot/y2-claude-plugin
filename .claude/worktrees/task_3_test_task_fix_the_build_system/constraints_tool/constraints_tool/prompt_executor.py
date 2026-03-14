#!/usr/bin/env python3
"""Execute prompt constraints via agent-driven workflow."""

import json
import re
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool" / "src"))

from models import ConstraintPrompt, ConstraintPromptResult


def execute_prompt_constraint(
    constraint: ConstraintPrompt,
    credentials_tests_path: str = "credentials-tests.json"
) -> ConstraintPromptResult:
    """Execute a prompt constraint via agent-driven knowledge document workflow.

    Workflow:
    1. Check if credentials-tests.json exists with a result for this constraint
    2. If found, extract the verdict and validate against regex
    3. If not found, return error verdict

    In production, an agent would:
    1. Read this constraint
    2. Execute the prompt via Claude
    3. Write ConstraintPromptResult to credentials-tests.json using y2:knowledge-tool skill

    Args:
        constraint: ConstraintPrompt with prompt and verdict_expect_rule
        credentials_tests_path: Path to credentials-tests.json (relative or absolute)

    Returns:
        ConstraintPromptResult with validated verdict
    """
    creds_path = Path(credentials_tests_path)

    try:
        # Check if credentials-tests.json exists
        if not creds_path.exists():
            return ConstraintPromptResult(
                constraint_id=constraint.id,
                verdict="ERROR",
                short_answer=f"Waiting for agent to execute prompt. Expected result in {credentials_tests_path}",
                timestamp=datetime.now()
            )

        # Load credentials-tests.json
        with open(creds_path, 'r') as f:
            creds_data = json.load(f)

        # Look for result matching this constraint ID
        results = creds_data.get("results", {})
        if constraint.id not in results:
            return ConstraintPromptResult(
                constraint_id=constraint.id,
                verdict="PENDING",
                short_answer=f"Constraint {constraint.id} not found in {credentials_tests_path}. Agent should add it.",
                timestamp=datetime.now()
            )

        result_data = results[constraint.id]

        # Extract verdict from result
        verdict = result_data.get("verdict", "")

        # Validate verdict against constraint's regex rule
        regex = constraint.get_compiled_regex()
        if not regex.search(verdict):
            return ConstraintPromptResult(
                constraint_id=constraint.id,
                verdict=verdict,
                short_answer=f"Verdict '{verdict}' does not match pattern '{constraint.verdict_expect_rule}'",
                timestamp=datetime.now()
            )

        # Return successful result
        return ConstraintPromptResult(
            constraint_id=constraint.id,
            verdict=verdict,
            short_answer=result_data.get("short_answer", ""),
            timestamp=datetime.fromisoformat(result_data["timestamp"]) if "timestamp" in result_data else datetime.now()
        )

    except json.JSONDecodeError as e:
        return ConstraintPromptResult(
            constraint_id=constraint.id,
            verdict="ERROR",
            short_answer=f"Invalid JSON in {credentials_tests_path}: {str(e)[:100]}",
            timestamp=datetime.now()
        )

    except Exception as e:
        return ConstraintPromptResult(
            constraint_id=constraint.id,
            verdict="ERROR",
            short_answer=f"Error reading results: {str(e)[:100]}",
            timestamp=datetime.now()
        )

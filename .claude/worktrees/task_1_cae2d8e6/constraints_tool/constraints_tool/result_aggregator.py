#!/usr/bin/env python3
"""Aggregate constraint results into Tests document."""

from typing import Dict, List
from datetime import datetime

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool" / "src"))

from models import (
    Constraints, Constraint,
    ConstraintBashResult, ConstraintPromptResult,
    Test, Tests
)


def create_tests_document(
    constraints: Constraints,
    bash_results: Dict[str, ConstraintBashResult],
    prompt_results: Dict[str, ConstraintPromptResult]
) -> Tests:
    """Create a Tests document from constraint results.

    Args:
        constraints: Constraints document with constraint definitions
        bash_results: Dict mapping constraint_id to ConstraintBashResult
        prompt_results: Dict mapping constraint_id to ConstraintPromptResult

    Returns:
        Tests document with all results organized by type and scope
    """
    tests_dict: Dict[str, Test] = {}
    test_counter = 0

    # Add bash results
    for constraint_id, result in bash_results.items():
        test_counter += 1
        test_id = f"test_bash_{test_counter}"
        test = Test(
            id=test_id,
            constraint_id=constraint_id,
            result=result
        )
        tests_dict[test_id] = test

    # Add prompt results
    for constraint_id, result in prompt_results.items():
        test_counter += 1
        test_id = f"test_prompt_{test_counter}"
        test = Test(
            id=test_id,
            constraint_id=constraint_id,
            result=result
        )
        tests_dict[test_id] = test

    # Determine overall scope and type
    has_bash = len(bash_results) > 0
    has_prompt = len(prompt_results) > 0
    constraint_type = "all"
    if has_bash and not has_prompt:
        constraint_type = "bash"
    elif has_prompt and not has_bash:
        constraint_type = "prompt"

    # Create Tests document
    tests = Tests(
        scope="all",
        constraint_type=constraint_type,
        tests=tests_dict if tests_dict else None,
        metadata={
            "created_at": datetime.now().isoformat(),
            "total_tests": len(tests_dict),
            "bash_tests": len(bash_results),
            "prompt_tests": len(prompt_results),
            "pass_count": sum(1 for t in tests_dict.values() if getattr(t.result, 'verdict', False))
        }
    )

    return tests

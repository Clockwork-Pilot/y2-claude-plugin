#!/usr/bin/env python3
"""Main constraint execution orchestrator."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Union

# Add parent directory to path for imports
_script_dir = Path(__file__).parent
_knowledge_tool_src = Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool" / "src"
sys.path.insert(0, str(_knowledge_tool_src))
sys.path.insert(0, str(_script_dir))

from models import (
    Feature, Constraints, Tests,
    ConstraintBash, ConstraintPrompt,
    ConstraintBashResult, ConstraintPromptResult,
    Constraint
)


def execute_constraint(
    constraint: Union[ConstraintBash, ConstraintPrompt]
) -> Union[ConstraintBashResult, ConstraintPromptResult]:
    """Execute a single constraint and return its result.

    Args:
        constraint: ConstraintBash or ConstraintPrompt to execute

    Returns:
        ConstraintBashResult or ConstraintPromptResult with execution result
    """
    if isinstance(constraint, ConstraintBash):
        # Execute bash command
        try:
            result = subprocess.run(
                constraint.cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            verdict = result.returncode == 0
            output = result.stdout + result.stderr
            return constraint.create_result(verdict, output)
        except subprocess.TimeoutExpired:
            return constraint.create_result(False, "Command timeout")
        except Exception as e:
            return constraint.create_result(False, str(e))

    elif isinstance(constraint, ConstraintPrompt):
        # For prompt constraints, return empty result
        # Actual LLM evaluation happens at higher level if needed
        return constraint.create_result()

    else:
        raise TypeError(f"Unknown constraint type: {type(constraint)}")


def execute_constraints(
    constraints_json_path: str,
    output_tests_path: str = None
) -> Tests:
    """Execute all constraints from a constraints.json file.

    Workflow:
    1. Load constraints.json as Constraints or Feature document
    2. Extract all constraints from features
    3. Execute bash constraints directly using subprocess
    4. Create empty results for prompt constraints
    5. Aggregate results into Tests document
    6. Optionally write Tests to tests.json

    Args:
        constraints_json_path: Path to constraints.json file (Constraints or Feature document)
        output_tests_path: Optional path to write Tests document (tests.json)

    Returns:
        Tests document with all execution results
    """
    constraints_path = Path(constraints_json_path)

    print(f"📋 Loading constraints from {constraints_json_path}")

    # Load constraints.json
    if not constraints_path.exists():
        raise FileNotFoundError(f"Constraints file not found: {constraints_json_path}")

    with open(constraints_path, 'r') as f:
        data = json.load(f)

    # Parse document (can be Constraints or Feature)
    doc_type = data.get("type", "Constraints")
    all_results = {}

    if doc_type == "Feature":
        # Single Feature document with embedded constraints
        print("📄 Detected Feature document")
        try:
            feature = Feature.model_validate(data)
        except Exception as e:
            raise ValueError(f"Invalid Feature format: {e}")

        if feature.constraints:
            print(f"🎯 Found {len(feature.constraints)} constraints in feature '{feature.id}'")
            for c_id, constraint in feature.constraints.items():
                try:
                    print(f"  → Executing: {c_id}")
                    result = execute_constraint(constraint)
                    all_results[c_id] = result
                    if isinstance(result, ConstraintBashResult):
                        print(f"     Result: {'✓ PASS' if result.verdict else '✗ FAIL'}")
                    else:
                        print(f"     Result: {result.verdict or '(empty)'}")
                except Exception as e:
                    print(f"  ✗ Error: {e}")

    else:
        # Constraints document with features
        print("📄 Detected Constraints document")
        try:
            constraints = Constraints.model_validate(data)
        except Exception as e:
            raise ValueError(f"Invalid constraints format: {e}")

        # Process features
        if constraints.features:
            print(f"🎯 Found {len(constraints.features)} features")
            for feature_id, feature in constraints.features.items():
                if feature.constraints:
                    print(f"  Feature '{feature_id}': {len(feature.constraints)} constraints")
                    for c_id, constraint in feature.constraints.items():
                        try:
                            print(f"    → Executing: {c_id}")
                            result = execute_constraint(constraint)
                            all_results[c_id] = result
                            if isinstance(result, ConstraintBashResult):
                                print(f"       Result: {'✓ PASS' if result.verdict else '✗ FAIL'}")
                            else:
                                print(f"       Result: {result.verdict or '(empty)'}")
                        except Exception as e:
                            print(f"    ✗ Error: {e}")

        # Process standalone Constraint objects
        if constraints.constraints:
            print(f"🔍 Found {len(constraints.constraints)} standalone constraints")
            for constraint_id, constraint in constraints.constraints.items():
                try:
                    print(f"  → Executing: {constraint_id}")
                    if constraint.constraint_bash:
                        result = execute_constraint(constraint.constraint_bash)
                    elif constraint.constraint_prompt:
                        result = execute_constraint(constraint.constraint_prompt)
                    else:
                        raise ValueError(f"Constraint {constraint_id} has no bash or prompt")
                    all_results[constraint_id] = result
                    if isinstance(result, ConstraintBashResult):
                        print(f"     Result: {'✓ PASS' if result.verdict else '✗ FAIL'}")
                    else:
                        print(f"     Result: {result.verdict or '(empty)'}")
                except Exception as e:
                    print(f"  ✗ Error: {e}")

    # Create Tests document from results
    print("📊 Aggregating results...")
    tests = Tests(
        constraints_results=all_results if all_results else None
    )

    # Write output if specified
    if output_tests_path:
        output_path = Path(output_tests_path)
        print(f"💾 Writing tests to {output_tests_path}")
        with open(output_path, 'w') as f:
            json.dump(tests.model_dump(), f, indent=2, default=str)
        print("✓ Done!")

    return tests


def main():
    """Command-line entry point for constraint execution.

    Expected Arguments:
        sys.argv[1] (REQUIRED): Path to constraints.json
            - Constraints or Feature root document
            - Contains features with embedded constraints
            - Constraints: {type: "Constraints", features?: {...}, metadata?: {...}}
            - Feature: {type: "Feature", id: "...", constraints?: {...}, metadata?: {...}}

        sys.argv[2] (OPTIONAL): Path to tests.json output file
            - Where to write aggregated test results
            - Will be created/overwritten as Tests root document
            - If omitted, results only logged to stdout

    Example Usage:
        python3 constraints_executor.py constraints.json tests.json
        python3 constraints_executor.py constraints.json
    """
    if len(sys.argv) < 2:
        print("Usage: python constraints_executor.py <constraints.json> [tests.json]")
        sys.exit(1)

    constraints_json = sys.argv[1]
    tests_json = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        execute_constraints(constraints_json, tests_json)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

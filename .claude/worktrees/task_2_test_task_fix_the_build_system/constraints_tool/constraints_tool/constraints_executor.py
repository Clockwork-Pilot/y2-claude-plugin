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
_knowledge_tool_root = Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool"
sys.path.insert(0, str(_knowledge_tool_src))
sys.path.insert(0, str(_script_dir))

from models import (
    Feature, FeaturesScope, TestResults, FeatureResult,
    ConstraintBash, ConstraintPrompt,
    ConstraintBashResult, ConstraintPromptResult
)

# Import patch_knowledge_document for protected file updates
sys.path.insert(0, str(_knowledge_tool_root))
from patch_knowledge_document import apply_json_patch


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


def check_feature(feature: Feature) -> FeatureResult:
    """Execute all constraints in a feature and return aggregated results.

    Args:
        feature: Feature with embedded constraints to execute

    Returns:
        FeatureResult with constraint execution results indexed by constraint ID
    """
    constraint_results = {}

    if feature.constraints:
        print(f"🎯 Checking feature '{feature.id}': {len(feature.constraints)} constraints")
        for constraint_id, constraint in feature.constraints.items():
            try:
                print(f"  → Executing: {constraint_id}")
                result = execute_constraint(constraint)
                constraint_results[constraint_id] = result
                if isinstance(result, ConstraintBashResult):
                    print(f"     Result: {'✓ PASS' if result.verdict else '✗ FAIL'}")
                else:
                    print(f"     Result: {result.verdict or '(empty)'}")
            except Exception as e:
                print(f"  ✗ Error: {e}")

    return FeatureResult(
        feature_id=feature.id,
        constraints_results=constraint_results if constraint_results else None
    )


def execute_constraints(
    constraints_json_path: str,
    output_tests_path: str = None
) -> TestResults:
    """Execute all constraints from a constraints.json file.

    Workflow:
    1. Load constraints.json as FeaturesScope or Feature document
    2. For each feature, call check_feature() to execute its constraints
    3. Aggregate results into TestResults document
    4. Optionally update TestResults knowledge file using patch_knowledge_document

    Args:
        constraints_json_path: Path to constraints.json file (FeaturesScope or Feature document)
        output_tests_path: Optional path to TestResults knowledge file (tests.json)
                          Features are appended/updated, not replaced

    Returns:
        TestResults document with all execution results
    """
    constraints_path = Path(constraints_json_path)

    print(f"📋 Loading constraints from {constraints_json_path}")

    # Load constraints.json
    if not constraints_path.exists():
        raise FileNotFoundError(f"Constraints file not found: {constraints_json_path}")

    with open(constraints_path, 'r') as f:
        data = json.load(f)

    # Parse document (can be FeaturesScope or Feature)
    doc_type = data.get("type", "FeaturesScope")
    features_results = {}

    if doc_type == "Feature":
        # Single Feature document with embedded constraints
        print("📄 Detected Feature document")
        try:
            feature = Feature.model_validate(data)
        except Exception as e:
            raise ValueError(f"Invalid Feature format: {e}")

        feature_result = check_feature(feature)
        if feature_result.constraints_results:
            features_results[feature.id] = feature_result

    else:
        # FeaturesScope document with features
        print("📄 Detected FeaturesScope document")
        try:
            features_scope = FeaturesScope.model_validate(data)
        except Exception as e:
            raise ValueError(f"Invalid FeaturesScope format: {e}")

        # Process features
        if features_scope.features:
            print(f"🎯 Found {len(features_scope.features)} features (scope: {features_scope.scope})")
            for feature_id, feature in features_scope.features.items():
                feature_result = check_feature(feature)
                if feature_result.constraints_results:
                    features_results[feature_id] = feature_result

    # Create TestResults document from results
    print("📊 Aggregating results...")
    test_results = TestResults(
        features_results=features_results if features_results else None
    )

    # Update Tests knowledge file if specified
    if output_tests_path:
        output_path = Path(output_tests_path)
        print(f"💾 Updating tests at {output_tests_path}")

        # Build JSON Patch to add each feature result
        # Features are merged, not replaced
        patch_ops = []
        for feature_id, feature_result in features_results.items():
            patch_ops.append({
                "op": "add",
                "path": f"/features_results/{feature_id}",
                "value": json.loads(feature_result.model_dump_json(exclude_none=True))
            })

        if patch_ops:
            # Apply patch using knowledge_tool API
            patch_json = json.dumps(patch_ops)
            error = apply_json_patch(str(output_path), patch_json)
            if error:
                print(f"⚠️  Warning: {error.error}")
            else:
                print("✓ Tests updated!")
        else:
            print("ℹ️  No results to update")

    return test_results


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

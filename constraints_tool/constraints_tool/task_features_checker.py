#!/usr/bin/env python3
"""Task features constraint checker - execute and validate feature constraints."""

import json
import subprocess
import sys
import argparse
import os
from pathlib import Path
from typing import Dict, Optional, Union

# Add parent directory to path for imports
_script_dir = Path(__file__).parent
_knowledge_tool_src = Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool" / "src"
_knowledge_tool_root = Path(__file__).parent.parent.parent / "knowledge_tool" / "knowledge_tool"
sys.path.insert(0, str(_knowledge_tool_src))
sys.path.insert(0, str(_script_dir))

from models import (
    Task, Feature,
    ConstraintBash, ConstraintPrompt,
    ConstraintBashResult, ConstraintPromptResult,
    FeatureResult, ChecksResults, FeaturesStats
)

# Import patch_knowledge_document for protected file updates
sys.path.insert(0, str(_knowledge_tool_root))
from patch_knowledge_document import apply_json_patch

# Import config for PROJECT_ROOT
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import PROJECT_ROOT as CONFIG_PROJECT_ROOT


def _substitute_project_root(cmd: str) -> str:
    """Substitute ${PROJECT_ROOT} and $PROJECT_ROOT placeholders in command.

    Args:
        cmd: Command string potentially containing PROJECT_ROOT placeholders

    Returns:
        Command with PROJECT_ROOT placeholders replaced with actual path
    """
    project_root_str = str(CONFIG_PROJECT_ROOT)
    # Replace both ${PROJECT_ROOT} and $PROJECT_ROOT patterns
    cmd = cmd.replace("${PROJECT_ROOT}", project_root_str)
    cmd = cmd.replace("$PROJECT_ROOT", project_root_str)
    return cmd


def _check_recursive_execution(cmd: str) -> bool:
    """Check if command would execute task_features_checker.py recursively.

    Only flags commands that actually invoke the script (python, python3, ./ etc),
    not just references to it in grep patterns or other searches.

    Args:
        cmd: Command string to check

    Returns:
        True if recursive execution detected, False otherwise
    """
    script_name = Path(__file__).name
    script_path = str(Path(__file__).resolve())

    # Check if command actually executes task_features_checker.py
    # Match: python/python3 ... task_features_checker.py or ./task_features_checker.py
    import re
    execution_patterns = [
        r'python\s+.*task_features_checker\.py',
        r'python3\s+.*task_features_checker\.py',
        r'\./task_features_checker\.py',
        r'bash.*task_features_checker\.py',
    ]

    for pattern in execution_patterns:
        if re.search(pattern, cmd):
            return True

    return False


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
        # Check for recursive execution attempts
        if _check_recursive_execution(constraint.cmd):
            return constraint.create_result(
                False,
                "✗ Recursive execution detected: task_features_checker.py cannot check itself"
            )

        # Substitute PROJECT_ROOT placeholders
        cmd = _substitute_project_root(constraint.cmd)

        # Execute bash command
        try:
            result = subprocess.run(
                cmd,
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


def generate_features_stats(
    task: Task,
    checks_results: ChecksResults
) -> FeaturesStats:
    """Generate FeaturesStats from ChecksResults for iteration tracking.

    Args:
        task: Task document containing all features
        checks_results: ChecksResults with constraint execution results

    Returns:
        FeaturesStats with features_checks status and failed features details
    """
    # Initialize features_checks with all features set to True (passing)
    features_checks = {}
    for feature_id in task.spec.features.keys():
        features_checks[feature_id] = True

    # Build failed features dict and update features_checks for failures
    failed_features = {}
    if checks_results.features_results:
        for feature_id, feature_result in checks_results.features_results.items():
            if feature_result.constraints_results:
                # Check if any constraint failed
                has_failure = False
                for constraint_id, result in feature_result.constraints_results.items():
                    # Check if constraint failed (bash has verdict bool, prompt has verdict str)
                    if isinstance(result, ConstraintBashResult) and not result.verdict:
                        has_failure = True
                        break
                    elif isinstance(result, ConstraintPromptResult) and not result.verdict:
                        has_failure = True
                        break

                # Mark feature as failed and add to failed dict
                if has_failure:
                    features_checks[feature_id] = False
                    failed_features[feature_id] = feature_result

    return FeaturesStats(
        features_checks=features_checks,
        failed=failed_features
    )


def check_task_features(
    task_json_path: str,
    feature_ids: Optional[list] = None,
    output_checks_path: Optional[str] = None
) -> tuple[ChecksResults, Optional[FeaturesStats]]:
    """Execute constraints for features in a Task document.

    Workflow:
    1. Load task.json as Task document
    2. Extract spec.features
    3. Filter by feature_ids if provided
    4. For each feature, execute its constraints
    5. Aggregate results into ChecksResults document
    6. Optionally save ChecksResults to file using patch_knowledge_document

    Args:
        task_json_path: Path to task.json file (Task document)
        feature_ids: Optional list of feature IDs to check (if None, check all)
        output_checks_path: Optional path to ChecksResults file to save results

    Returns:
        ChecksResults document with all execution results
    """
    task_path = Path(task_json_path)

    print(f"📋 Loading task from {task_json_path}")

    # Load task.json
    if not task_path.exists():
        raise FileNotFoundError(f"Task file not found: {task_json_path}")

    with open(task_path, 'r') as f:
        data = json.load(f)

    # Parse Task document
    try:
        task = Task.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid Task format: {e}")

    # Extract features from spec
    if not task.spec.features:
        print("⚠️  No features found in task spec")
        return ChecksResults.create_default(), None

    # Filter features if specified
    features_to_check = task.spec.features
    if feature_ids:
        features_to_check = {
            fid: f for fid, f in task.spec.features.items()
            if fid in feature_ids
        }
        if not features_to_check:
            print(f"⚠️  No matching features found for: {feature_ids}")
            return ChecksResults.create_default(), None

    # Execute constraints for each feature
    features_results = {}
    print(f"🎯 Found {len(features_to_check)} features to check")

    for feature_id, feature in features_to_check.items():
        feature_result = check_feature(feature)
        if feature_result.constraints_results:
            features_results[feature_id] = feature_result

    # Create ChecksResults document from results
    print("📊 Aggregating results...")
    checks_results = ChecksResults(
        features_results=features_results if features_results else None
    )

    # Generate FeaturesStats for iteration tracking
    features_stats = generate_features_stats(task, checks_results)

    # Save ChecksResults if specified
    if output_checks_path:
        output_path = Path(output_checks_path)
        print(f"💾 Saving results to {output_checks_path}")

        # Initialize ChecksResults structure if file doesn't exist
        if not output_path.exists():
            initial_structure = {
                "type": "ChecksResults",
                "model_version": 1,
                "features_results": {}
            }
            output_path.write_text(json.dumps(initial_structure, indent=2))

        # Build JSON Patch to add each feature result
        # Features are merged, not replaced
        patch_ops = []
        for feature_id, feature_result in features_results.items():
            patch_ops.append({
                "op": "add",
                "path": f"/features_results/{feature_id}",
                "value": json.loads(feature_result.model_dump_json(exclude_none=True))
            })

        # Apply patch to create/update the ChecksResults file
        if patch_ops:
            error = apply_json_patch(str(output_path), json.dumps(patch_ops))
            if error:
                print(f"⚠️  Failed to save results: {error.error}")
            else:
                print(f"✓ Results saved to {output_checks_path}")

    return checks_results, features_stats


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Execute and validate feature constraints from a Task document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all features in task.json
  python3 task_features_checker.py task.json

  # Check specific features
  python3 task_features_checker.py task.json --features feature_1,feature_2

  # Check and save results
  python3 task_features_checker.py task.json --output-checks-path checks_results.json

  # Check specific features and save results
  python3 task_features_checker.py task.json \\
    --features forbid_task_status_downgrade,render_spec_features_in_task \\
    --output-checks-path checks_results.json
        """
    )

    parser.add_argument(
        'task_path',
        help='Path to task.json file (Task document)'
    )

    parser.add_argument(
        '--features',
        help='Comma-separated list of feature IDs to check (if not provided, checks all)',
        type=str,
        default=None
    )

    parser.add_argument(
        '--output-checks-path',
        help='Path to save ChecksResults document',
        type=str,
        default='checks_results.json'
    )

    args = parser.parse_args()

    # Parse feature IDs if provided
    feature_ids = None
    if args.features:
        feature_ids = [f.strip() for f in args.features.split(',')]

    try:
        # Execute constraint checks
        checks_results, features_stats = check_task_features(
            args.task_path,
            feature_ids=feature_ids,
            output_checks_path=args.output_checks_path
        )

        # Print results summary
        print("\n📊 Execution Summary:")
        if checks_results.features_results:
            total_constraints = 0
            for feature_id, feature_result in checks_results.features_results.items():
                constraint_count = len(feature_result.constraints_results or {})
                total_constraints += constraint_count
                print(f"  {feature_id}: {constraint_count} constraints")
            print(f"Total: {total_constraints} constraints executed")
        else:
            print("  No results")

        # Print features stats summary
        if features_stats:
            print("\n📈 Feature Validation Stats:")
            passing = sum(1 for v in features_stats.features_checks.values() if v)
            failing = sum(1 for v in features_stats.features_checks.values() if not v)
            total = len(features_stats.features_checks)
            print(f"  Overall: {passing}/{total} features passed")
            if failing > 0:
                print(f"  Failed: {failing} features")
                for feature_id in sorted(features_stats.failed.keys()):
                    print(f"    - {feature_id}")

        print("\n✓ Task features check completed successfully")
        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

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
    Spec, Feature,
    ConstraintBash,
    ConstraintBashResult,
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
    constraint: Union[ConstraintBash]
) -> Union[ConstraintBashResult]:
    """Execute a single constraint and return its result.

    Args:
        constraint: ConstraintBash to execute

    Returns:
        ConstraintBashResult with execution result
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
            # Set PROJECT_ROOT environment variable so constraints can use it
            env = os.environ.copy()
            env['PROJECT_ROOT'] = str(CONFIG_PROJECT_ROOT)

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            verdict = result.returncode == 0
            output = result.stdout + result.stderr
            return constraint.create_result(verdict, output)
        except subprocess.TimeoutExpired:
            return constraint.create_result(False, "Command timeout")
        except Exception as e:
            return constraint.create_result(False, str(e))

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
        for constraint_id, constraint in feature.constraints.items():
            result = execute_constraint(constraint)
            constraint_results[constraint_id] = result

    return FeatureResult(
        feature_id=feature.id,
        constraints_results=constraint_results if constraint_results else None
    )


def generate_features_stats(
    features: Dict[str, Feature],
    checks_results: ChecksResults
) -> FeaturesStats:
    """Generate FeaturesStats from ChecksResults for iteration tracking.

    Args:
        features: Dict of features containing all features
        checks_results: ChecksResults with constraint execution results

    Returns:
        FeaturesStats with features_checks status and failed features details
    """
    # Initialize features_checks with all features set to True (passing)
    features_checks = {}
    for feature_id in features.keys():
        features_checks[feature_id] = True

    # Build failed features dict and update features_checks for failures
    failed_features = {}
    if checks_results.features_results:
        for feature_id, feature_result in checks_results.features_results.items():
            if feature_result.constraints_results:
                has_failure = False
                for result in feature_result.constraints_results.values():
                    # Check if constraint failed
                    if isinstance(result, ConstraintBashResult) and not result.verdict:
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
    """Execute constraints for features in a Spec document (task-spec.k.json).

    Workflow:
    1. Load task-spec.k.json as Spec document
    2. Extract features from spec
    3. Filter by feature_ids if provided
    4. For each feature, execute its constraints
    5. Aggregate results into ChecksResults document
    6. Optionally save ChecksResults to file using patch_knowledge_document

    Args:
        task_json_path: Path to task-spec.k.json (Spec document)
        feature_ids: Optional list of feature IDs to check (if None, check all)
        output_checks_path: Optional path to ChecksResults file to save results

    Returns:
        ChecksResults document with all execution results
    """
    task_path = Path(task_json_path)

    print(f"📋 Loading spec from {task_json_path}")

    # Load document
    if not task_path.exists():
        raise FileNotFoundError(f"Document file not found: {task_json_path}")

    with open(task_path, 'r') as f:
        data = json.load(f)

    # Load Spec document (task-spec.k.json)
    try:
        spec = Spec.model_validate(data)
        features = spec.features
        doc_type = 'Spec'
    except Exception as e:
        raise ValueError(f"Invalid Spec format: {e}")

    # Extract features
    if not features:
        print("⚠️  No features found in document")
        return ChecksResults.create_default(), None

    # Filter features if specified
    features_to_check = features
    if feature_ids:
        features_to_check = {
            fid: f for fid, f in features.items()
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

    # Build JSON Patch operations to increment fails_count for failed constraints
    patch_ops = []
    locked_constraints = []  # Track constraints that become locked
    # Determine patch path based on document type (Spec vs Task)
    feature_path_prefix = "features" if doc_type == "Spec" else "spec/features"

    if checks_results.features_results and features:
        for feature_id, feature_result in checks_results.features_results.items():
            feature_obj = features.get(feature_id)
            if not feature_obj or not feature_result.constraints_results:
                continue

            for constraint_id, result in feature_result.constraints_results.items():
                # Generate patch to increment fails_count for failed bash constraints
                if isinstance(result, ConstraintBashResult) and not result.verdict:
                    constraint_obj = feature_obj.constraints.get(constraint_id) if feature_obj.constraints else None
                    if isinstance(constraint_obj, ConstraintBash):
                        # Get current fails_count and increment it
                        current_fails_count = constraint_obj.fails_count
                        new_fails_count = current_fails_count + 1
                        # Use "add" when field is absent (fails_count==0 is omitted from JSON),
                        # "replace" when the field already exists (fails_count > 0).
                        patch_ops.append({
                            "op": "add" if current_fails_count == 0 else "replace",
                            "path": f"/{feature_path_prefix}/{feature_id}/constraints/{constraint_id}/fails_count",
                            "value": new_fails_count
                        })
                        # Track if constraint is becoming locked (fails_count > 0)
                        if current_fails_count == 0:
                            locked_constraints.append(f"{feature_id}.{constraint_id}")

    # Save updated task with incremented fails_count using knowledge API
    if patch_ops:
        print("🔄 Updating fails_count for failed constraints...")
        error = apply_json_patch(str(task_path), json.dumps(patch_ops))
        if error:
            print(f"⚠️  Failed to update fails_count: {error.error}")
        else:
            print(f"✓ Updated fails_count for {len(patch_ops)} constraint(s)")

            # Warn about newly locked constraints
            if locked_constraints:
                print(f"\n⚠️  {len(locked_constraints)} constraint(s) now locked (cmd cannot be changed):")
                for constraint in locked_constraints:
                    print(f"   • {constraint}")
                print("   Options: (1) Fix constraint to pass, or (2) Remove constraint entirely")

    # Save ChecksResults to file
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

    # Generate FeaturesStats for iteration tracking
    features_stats = generate_features_stats(features, checks_results)

    return checks_results, features_stats


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Execute and validate feature constraints from a Spec document (task-spec.k.json)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all features in task-spec.k.json
  python3 task_features_checker.py task-spec.k.json

  # Check specific features
  python3 task_features_checker.py task-spec.k.json --features feature_1,feature_2

  # Check and save results
  python3 task_features_checker.py task-spec.k.json --output-checks-path checks_results.k.json

  # Check specific features and save results
  python3 task_features_checker.py task-spec.k.json \\
    --features forbid_task_status_downgrade,render_spec_features_in_task \\
    --output-checks-path checks_results.k.json
        """
    )

    parser.add_argument(
        'task_path',
        help='Path to task-spec.k.json file (Spec document)'
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
        default='checks_results.k.json'
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


        # Print tested features summary
        print("\n📋 Tested Features:")
        if checks_results.features_results:
            for feature_id, feature_result in checks_results.features_results.items():
                constraint_count = len(feature_result.constraints_results or {})
                passed_count = sum(1 for result in (feature_result.constraints_results or {}).values()
                                 if (isinstance(result, ConstraintBashResult) and result.verdict))
                failed_count = constraint_count - passed_count
                status = "✓" if failed_count == 0 else "✗"
                print(f"  {status} {feature_id}: {passed_count}/{constraint_count} constraints passed")
        else:
            print("  No features tested")

        # Print features stats summary (only proven failures count)
        failing_count = 0
        if features_stats:
            print("\n📈 Feature Validation Stats (proven constraints only):")
            passing = sum(1 for v in features_stats.features_checks.values() if v)
            failing = sum(1 for v in features_stats.features_checks.values() if not v)
            failing_count = failing
            total = len(features_stats.features_checks)
            print(f"  Overall: {passing}/{total} features passed")
            if failing > 0:
                print(f"  Failed: {failing} features (proven constraints failing)")

        # Print detailed error information for failed constraints
        if features_stats and features_stats.failed:
            print("\n❌ Failed Constraint Details:")
            for feature_id in sorted(features_stats.failed.keys()):
                feature_result = features_stats.failed[feature_id]
                print(f"\n  {feature_id}:")
                if feature_result.constraints_results:
                    for constraint_id, result in sorted(feature_result.constraints_results.items()):
                        is_failed = False
                        if isinstance(result, ConstraintBashResult) and not result.verdict:
                            is_failed = True

                        if is_failed:
                            print(f"    ✗ {constraint_id}")
                            output = getattr(result, 'shrunken_output', None) or getattr(result, 'output', None)
                            if output:
                                for line in output.split('\n'):
                                    if line.strip():
                                        print(f"      {line}")

        # Exit with code 2 if constraints failed, 0 if all passed
        if failing_count > 0:
            print("\n✗ Task features check FAILED - constraints not satisfied")
            return 2
        else:
            print("\n✓ Task features check completed successfully")
            return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

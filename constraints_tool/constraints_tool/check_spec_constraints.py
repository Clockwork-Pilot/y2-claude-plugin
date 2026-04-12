#!/usr/bin/env python3
"""Task features constraint checker - execute and validate feature constraints."""

import json
import subprocess
import sys
import argparse
import os
import time
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
    FeatureResult, ChecksResults
)

# Import patch_knowledge_document for protected file updates
sys.path.insert(0, str(_knowledge_tool_root))
from patch_knowledge_document import apply_json_patch

# Import config for PROJECT_ROOT
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import PROJECT_ROOT as CONFIG_PROJECT_ROOT
from config import CONSTRAINTS_TIMEOUT, CONSTRAINTS_RESULTS_FILE




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
    """Check if command would execute check_spec_constraints.py recursively.

    Only flags commands that actually invoke the script (python, python3, ./ etc),
    not just references to it in grep patterns or other searches.

    Args:
        cmd: Command string to check

    Returns:
        True if recursive execution detected, False otherwise
    """
    script_name = Path(__file__).name
    script_path = str(Path(__file__).resolve())

    # Check if command actually executes check_spec_constraints.py
    # Match: python/python3 ... check_spec_constraints.py or ./check_spec_constraints.py
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
                "✗ Recursive execution detected: check_spec_constraints.py cannot check itself"
            )

        # Substitute PROJECT_ROOT placeholders
        cmd = _substitute_project_root(constraint.cmd)

        # Use constraint-specific timeout if set, otherwise use global default
        timeout_seconds = constraint.timeout if constraint.timeout is not None else CONSTRAINTS_TIMEOUT

        # Execute bash command
        try:
            # Set PROJECT_ROOT environment variable so constraints can use it
            env = os.environ.copy()
            env['PROJECT_ROOT'] = str(CONFIG_PROJECT_ROOT)

            start = time.monotonic()
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env
            )
            duration = time.monotonic() - start
            verdict = result.returncode == 0

            # Truncate stdout and stderr to last 200 chars each
            stdout = result.stdout[-200:] if len(result.stdout) > 200 else result.stdout
            stderr = result.stderr[-200:] if len(result.stderr) > 200 else result.stderr

            # Format output with labels
            output_parts = []
            if stdout:
                output_parts.append(f"[stdout] {stdout}")
            if stderr:
                output_parts.append(f"[stderr] {stderr}")
            output = "\n".join(output_parts) if output_parts else ""

            return constraint.create_result(verdict, output, duration)
        except subprocess.TimeoutExpired:
            return constraint.create_result(False, "Command timeout", float(timeout_seconds))
        except Exception as e:
            return constraint.create_result(False, str(e))

    else:
        raise TypeError(f"Unknown constraint type: {type(constraint)}")


def _build_dependency_buckets(
    features: Dict[str, Feature],
    features_to_check: Dict[str, Feature]
) -> list[list[str]]:
    """Build topologically sorted buckets of features based on depends_on.

    Returns a list of buckets, where each bucket contains feature IDs that can be
    executed in parallel (all their dependencies are in previous buckets).

    Args:
        features: Dict of all features in spec
        features_to_check: Dict of features to be checked

    Returns:
        List of buckets, where each bucket is a list of feature IDs
    """
    feature_ids_to_check = set(features_to_check.keys())
    buckets = []
    assigned = set()

    while len(assigned) < len(feature_ids_to_check):
        bucket = []
        for feature_id in feature_ids_to_check:
            if feature_id in assigned:
                continue
            feature = features_to_check[feature_id]
            # Check if all dependencies are assigned to previous buckets
            can_add = True
            if feature.depends_on:
                for dep_id in feature.depends_on:
                    # If dependency is in features_to_check but not yet assigned, skip
                    if dep_id in feature_ids_to_check and dep_id not in assigned:
                        can_add = False
                        break
            if can_add:
                bucket.append(feature_id)

        if not bucket:
            # Circular dependency detected - break gracefully
            break

        buckets.append(bucket)
        assigned.update(bucket)

    return buckets


def check_feature(
    feature: Feature,
    failing_parent_features: Optional[set[str]] = None
) -> FeatureResult:
    """Execute all constraints in a feature and return aggregated results.

    If feature has depends_on and any parent failed in current run, proven constraints
    (fails_count > 0) are skipped. Unproven constraints (fails_count == 0) always execute
    to establish proof.

    Args:
        feature: Feature with embedded constraints to execute
        failing_parent_features: Set of parent feature IDs that failed in current run

    Returns:
        FeatureResult with constraint execution results indexed by constraint ID
    """
    constraint_results = {}

    # Check if any dependencies failed in current run
    skip_due_to_deps = False
    if feature.depends_on and failing_parent_features:
        # Check if any dependency is in the failing set
        for dep_id in feature.depends_on:
            if dep_id in failing_parent_features:
                skip_due_to_deps = True
                break

    if feature.constraints:
        for constraint_id, constraint in feature.constraints.items():
            if skip_due_to_deps and isinstance(constraint, ConstraintBash) and constraint.fails_count > 0:
                # Skip only proven constraints (fails_count > 0) if parent failed
                result = constraint.create_result(True, "")
                result.postponed = True
            else:
                # Execute: either no dependency issues, or unproven constraint (always execute)
                result = execute_constraint(constraint)

            constraint_results[constraint_id] = result

    return FeatureResult(
        feature_id=feature.id,
        constraints_results=constraint_results if constraint_results else None
    )


def check_constraints(
    spec_json_path: str,
    feature_ids: Optional[list] = None,
    output_checks_path: Optional[str] = None
) -> ChecksResults:
    """Execute constraints for features in a Spec document (spec.k.json).

    Workflow:
    1. Load spec.k.json as Spec document
    2. Extract features from spec
    3. Filter by feature_ids if provided
    4. For each feature, execute its constraints
    5. Aggregate results into ChecksResults document
    6. Optionally save ChecksResults to file using patch_knowledge_document

    Args:
        spec_json_path: Path to spec.k.json (Spec document)
        feature_ids: Optional list of feature IDs to check (if None, check all)
        output_checks_path: Optional path to ChecksResults file to save results

    Returns:
        ChecksResults document with all execution results
    """
    spec_path = Path(spec_json_path)

    print(f"📋 Loading spec from {spec_json_path}")

    # Load document
    if not spec_path.exists():
        raise FileNotFoundError(f"Document file not found: {spec_json_path}")

    with open(spec_path, 'r') as f:
        data = json.load(f)

    # Load Spec document (spec.k.json)
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

    # Execute constraints for each feature with dependency ordering
    features_results = {}
    print(f"🎯 Found {len(features_to_check)} features to check")

    # Build dependency buckets
    try:
        buckets = _build_dependency_buckets(features, features_to_check)
    except ValueError as e:
        # This won't happen now, but keep for safety
        print(f"⚠️  {e}")
        buckets = [list(features_to_check.keys())]

    # Check if circular dependency was detected (not all features assigned)
    all_assigned = sum(len(bucket) for bucket in buckets)
    if all_assigned < len(features_to_check):
        unassigned = set(features_to_check.keys()) - {fid for bucket in buckets for fid in bucket}
        print(f"⚠️  Circular dependency detected in features: {sorted(unassigned)}")

    # Execute buckets sequentially, tracking failures
    failing_features = set()
    for bucket_idx, bucket in enumerate(buckets):
        print(f"  Bucket {bucket_idx + 1}/{len(buckets)}: executing {len(bucket)} feature(s)")
        for feature_id in bucket:
            feature = features_to_check[feature_id]
            feature_result = check_feature(feature, failing_parent_features=failing_features)
            if feature_result.constraints_results:
                features_results[feature_id] = feature_result
                # Check if this feature failed (has any failed constraints)
                has_failure = any(
                    isinstance(result, ConstraintBashResult) and not result.verdict and not getattr(result, 'postponed', False)
                    for result in feature_result.constraints_results.values()
                )
                if has_failure:
                    failing_features.add(feature_id)

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

    # Save updated task with incremented fails_count using knowledge API.
    #
    # NOTE: apply_json_patch intentionally blocks fails_count changes for verified
    # constraints (fails_count > 0) — see feature_model.py protection guard.
    # This means the batch will fail when any already-verified constraint is failing
    # again. That warning is expected and non-fatal: the checker's primary output
    # (verdicts, ChecksResults, exit code) is correct regardless.
    # DO NOT replace apply_json_patch with a direct file write to work around this —
    # fails_count tracking for verified constraints is handled by the protection design.
    if patch_ops:
        print("🔄 Updating fails_count for failed constraints...")
        error = apply_json_patch(str(spec_path), json.dumps(patch_ops))
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

        # Build JSON Patch operations
        patch_ops = []

        # First, remove features and constraints from checks_results that no longer exist in the spec
        if output_path.exists():
            try:
                with open(output_path, 'r') as f:
                    checks_data = json.load(f)

                if checks_data.get("features_results"):
                    existing_features = set(checks_data["features_results"].keys())
                    current_spec_features = set(features.keys()) if features else set()

                    # Remove features that are no longer in the spec
                    features_to_remove = existing_features - current_spec_features
                    if features_to_remove:
                        print(f"🗑️  Removing {len(features_to_remove)} feature(s) from checks_results (no longer in spec):")
                        for feature_id in sorted(features_to_remove):
                            print(f"   • {feature_id}")
                            patch_ops.append({
                                "op": "remove",
                                "path": f"/features_results/{feature_id}"
                            })

                    # For each existing feature, remove constraints that no longer exist in the spec
                    constraints_to_remove = []
                    for feature_id in existing_features & current_spec_features:
                        feature_result = checks_data["features_results"].get(feature_id)
                        spec_feature = features.get(feature_id)

                        if feature_result and feature_result.get("constraints_results") and spec_feature and spec_feature.constraints:
                            existing_constraints = set(feature_result["constraints_results"].keys())
                            current_spec_constraints = set(spec_feature.constraints.keys())

                            # Identify constraints to remove
                            constraints_removed = existing_constraints - current_spec_constraints
                            for constraint_id in constraints_removed:
                                constraints_to_remove.append((feature_id, constraint_id))

                    if constraints_to_remove:
                        print(f"🗑️  Removing {len(constraints_to_remove)} constraint(s) from checks_results (no longer in spec):")
                        for feature_id, constraint_id in sorted(constraints_to_remove):
                            print(f"   • {feature_id}.{constraint_id}")
                            patch_ops.append({
                                "op": "remove",
                                "path": f"/features_results/{feature_id}/constraints_results/{constraint_id}"
                            })
            except Exception as e:
                print(f"⚠️  Could not verify checks_results consistency: {e}")

        # Add each feature result from current spec
        # Features are merged, not replaced
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
        else:
            print(f"ℹ️  No changes to ChecksResults (same features as before)")

    return checks_results


def generate_report(checks_results: ChecksResults, spec: Spec, spec_path: str) -> int:
    """Print a human-readable report from ChecksResults and return an exit code.

    Returns 2 if any constraint failed, 0 otherwise.
    """
    print("\n📋 Tested Features:")
    if checks_results.features_results:
        for feature_id, feature_result in checks_results.features_results.items():
            constraint_count = len(feature_result.constraints_results or {})
            passed_count = sum(1 for result in (feature_result.constraints_results or {}).values()
                             if (isinstance(result, ConstraintBashResult) and result.verdict and not getattr(result, 'postponed', False)))
            skipped_count = sum(1 for result in (feature_result.constraints_results or {}).values()
                               if (isinstance(result, ConstraintBashResult) and getattr(result, 'postponed', False)))
            failed_count = constraint_count - passed_count - skipped_count

            if failed_count > 0:
                status = "✗"
            elif skipped_count > 0:
                status = "⏸️"
            else:
                status = "✓"

            if skipped_count > 0:
                print(f"  {status} {feature_id}: {passed_count}/{constraint_count} constraints passed ({skipped_count} skipped)")
            else:
                print(f"  {status} {feature_id}: {passed_count}/{constraint_count} constraints passed")
    else:
        print("  No features tested")

    failed_constraints = {}
    skipped_constraints = {}
    first_run_constraints = {}

    if checks_results.features_results:
        for feature_id, feature_result in checks_results.features_results.items():
            if feature_result.constraints_results:
                for constraint_id, result in feature_result.constraints_results.items():
                    if isinstance(result, ConstraintBashResult):
                        is_postponed = getattr(result, 'postponed', False)
                        if is_postponed:
                            skipped_constraints.setdefault(feature_id, []).append((constraint_id, result))
                        elif not result.verdict:
                            failed_constraints.setdefault(feature_id, []).append((constraint_id, result))
                        else:
                            feature = spec.features.get(feature_id) if spec.features else None
                            constraint = feature.constraints.get(constraint_id) if feature and feature.constraints else None
                            if constraint and isinstance(constraint, ConstraintBash) and constraint.fails_count == 0:
                                first_run_constraints.setdefault(feature_id, []).append((constraint_id, result))

    failing_count = sum(len(constraints) for constraints in failed_constraints.values())

    if first_run_constraints:
        print("\n🔍 First-Run Verification (establishing proof):")
        for feature_id in sorted(first_run_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(first_run_constraints[feature_id]):
                print(f"    ✓ {constraint_id}")

    if skipped_constraints:
        print("\n⏸️  Skipped Constraints (waiting for dependencies):")
        for feature_id in sorted(skipped_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(skipped_constraints[feature_id]):
                print(f"    ⏸️  {constraint_id}")

    if failed_constraints:
        print("\n❌ Failed Constraints:")
        for feature_id in sorted(failed_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(failed_constraints[feature_id]):
                output = getattr(result, 'shrunken_output', None) or getattr(result, 'output', None)
                print(f"    ✗ {constraint_id}")
                if output:
                    for line in output.split('\n'):
                        if line.strip():
                            print(f"      {line}")

    unverified_by_feature = {}
    if spec and spec.features:
        for feature_id, feature in spec.features.items():
            if feature.constraints:
                for constraint_id, constraint in feature.constraints.items():
                    fails_count = getattr(constraint, 'fails_count', 0)
                    if fails_count < 1:
                        unverified_by_feature.setdefault(feature_id, []).append((constraint_id, fails_count))

    if unverified_by_feature:
        print("\n⚠️  Unverified Constraints (fails_count < 1):")
        total_unverified = 0
        for feature_id in sorted(unverified_by_feature.keys()):
            constraints = unverified_by_feature[feature_id]
            total_unverified += len(constraints)
            print(f"\n  {feature_id}:")
            for constraint_id, fails_count in sorted(constraints):
                print(f"    🚫 {constraint_id} (fails_count={fails_count})")
        print(f"\nTotal unverified: {total_unverified}")

    if failing_count > 0:
        print(f"\n✗ Task features check FAILED - constraints not satisfied")
        print(f"  Spec:    {Path(spec_path).resolve()}")
        print(f"  Project: {Path(spec_path).resolve().parent}")
        return 2
    else:
        print("\n✓ Task features check completed successfully")
        return 0


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Execute and validate feature constraints from a Spec document (spec.k.json)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all features in spec.k.json
  python3 check_spec_constraints.py spec.k.json

  # Check specific features
  python3 check_spec_constraints.py spec.k.json --features feature_1,feature_2

  # Check and save results
  python3 check_spec_constraints.py spec.k.json --output-checks-path spec-checks.k.json

  # Check specific features and save results
  python3 check_spec_constraints.py spec.k.json \\
    --features forbid_task_status_downgrade,render_spec_features_in_task \\
    --output-checks-path spec-checks.k.json
        """
    )

    parser.add_argument(
        'spec_path',
        nargs='?',
        help='Path to spec.k.json (default: $CLAUDE_PROJECT_ROOT/spec.k.json)'
    )

    parser.add_argument(
        '--features',
        help='Comma-separated list of feature IDs to check (if not provided, checks all)',
        type=str,
        default=None
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Skip execution; load existing checks results file and print report only'
    )

    parser.add_argument(
        '--output-checks-path',
        help=f'Path to save ChecksResults document (default: {CONSTRAINTS_RESULTS_FILE} next to spec)',
        type=str,
        default=None
    )

    args = parser.parse_args()

    # Resolve spec path: explicit arg > $CLAUDE_PROJECT_ROOT/spec.k.json > error
    if args.spec_path is None:
        project_root = os.environ.get('CLAUDE_PROJECT_ROOT')
        if not project_root:
            print("Error: spec_path required (or set CLAUDE_PROJECT_ROOT)", file=sys.stderr)
            return 1
        args.spec_path = str(Path(project_root) / 'spec.k.json')
        print(f"📌 Using spec from CLAUDE_PROJECT_ROOT: {args.spec_path}")

    # Default sibling paths relative to spec file, not CWD
    spec_dir = Path(args.spec_path).parent
    if args.output_checks_path is None:
        args.output_checks_path = str(spec_dir / CONSTRAINTS_RESULTS_FILE)

    # Parse feature IDs if provided
    feature_ids = None
    if args.features:
        feature_ids = [f.strip() for f in args.features.split(',')]

    try:
        # Load spec document for unverified constraints reporting
        spec_data = json.loads(Path(args.spec_path).read_text())
        spec = Spec.model_validate(spec_data)

        if args.dry_run:
            checks_path = Path(args.output_checks_path)
            if not checks_path.exists():
                print(f"✗ Error: checks results file not found: {checks_path}", file=sys.stderr)
                return 1
            print(f"📂 Loading existing checks results from {checks_path}")
            checks_data = json.loads(checks_path.read_text())
            checks_results = ChecksResults.model_validate(checks_data)
        else:
            # Execute constraint checks
            checks_results = check_constraints(
                args.spec_path,
                feature_ids=feature_ids,
                output_checks_path=args.output_checks_path
            )

        return generate_report(checks_results, spec, args.spec_path)

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

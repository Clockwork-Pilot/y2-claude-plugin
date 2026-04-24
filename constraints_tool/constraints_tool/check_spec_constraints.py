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
    Project,
    ConstraintBash,
    ConstraintBashResult,
    FeatureResult, ChecksResults
)

# Import patch_knowledge_document for protected file updates
sys.path.insert(0, str(_knowledge_tool_root))
from patch_knowledge_document import apply_json_patch

# Admin-path write primitives: the checker skips apply_json_patch for the
# fails_count increment and writes directly. See _sync_spec_with_results below.
from common.file_tools import write_protected_file
from common.render import render as render_document
from knowledge_files_registry import add_knowledge_files

# Import config for PROJECT_ROOT
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import PROJECT_ROOT as CONFIG_PROJECT_ROOT
from config import CONSTRAINTS_TIMEOUT, CONSTRAINTS_RESULTS_FILE




def _sync_spec_with_results(spec_path: Path, doc_type: str, increments: list) -> None:
    """Record first-time failures back into the spec (0 → 1 on fails_count).

    Kept deliberately separate from apply_json_patch. apply_json_patch is the
    user-facing path — it passes context={'original_doc': ...} to the model
    validator, which activates the mutation guard in feature_model.py and
    rejects any fails_count change. This routine skips that context on purpose:
    it loads the spec, flips fails_count to 1, validates schema-only via
    Spec.model_validate(data) (no context → guard returns early), and writes
    through the same protected-file primitives apply_json_patch uses.

    Do not call this from anywhere other than the checker. The separation is
    code-level (owning this function), not enforced at runtime.

    Args:
        spec_path: Path to the spec JSON.
        doc_type: "Spec" or other (nested under /spec for Task-style docs).
        increments: Pairs of (feature_id, constraint_id) to bump from 0 to 1.
    """
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    container = data if doc_type == "Spec" else data.setdefault("spec", {})
    for feature_id, constraint_id in increments:
        container["features"][feature_id]["constraints"][constraint_id]["fails_count"] = 1

    # Schema validation without original_doc context; the mutation guard in
    # feature_model.py returns early when context is absent.
    validated = Spec.model_validate(data)
    canonical = json.loads(validated.model_dump_json(exclude_none=True))

    write_protected_file(spec_path, json.dumps(canonical, indent=2))
    try:
        render_document(str(spec_path))
    except Exception as e:
        print(f"⚠️  Warning: Failed to render markdown: {e}", file=sys.stderr)
    try:
        add_knowledge_files([str(spec_path), str(spec_path.with_suffix(".md"))])
    except Exception as e:
        print(f"⚠️  Warning: Failed to register knowledge files: {e}", file=sys.stderr)


def _substitute_project_root(cmd: str, project_root_str: str) -> str:
    """Substitute ${PROJECT_ROOT} and $PROJECT_ROOT placeholders in command."""
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
    constraint: Union[ConstraintBash],
    extra_env: Optional[Dict[str, str]] = None,
) -> Union[ConstraintBashResult]:
    """Execute a single constraint and return its result.

    Args:
        constraint: ConstraintBash to execute
        extra_env: Env vars layered on top of the process env after the default
            PROJECT_ROOT is set. Can override PROJECT_ROOT (e.g. when a Project
            document supplies per-spec envs). The final PROJECT_ROOT in env is
            also used for ${PROJECT_ROOT} substitution in the command string.

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

        # Build env: default PROJECT_ROOT, then extra_env layered on top (may override PROJECT_ROOT)
        env = os.environ.copy()
        env['PROJECT_ROOT'] = str(CONFIG_PROJECT_ROOT)
        if extra_env:
            env.update(extra_env)

        # Substitute ${PROJECT_ROOT} using the final value in env (so spec-level envs win)
        cmd = _substitute_project_root(constraint.cmd, env['PROJECT_ROOT'])

        # Use constraint-specific timeout if set, otherwise use global default
        timeout_seconds = constraint.timeout if constraint.timeout is not None else CONSTRAINTS_TIMEOUT

        # Execute bash command
        try:
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
    features_to_check: Dict[str, Feature]
) -> list[list[str]]:
    """Build topologically sorted buckets of features based on depends_on.

    Returns a list of buckets, where each bucket contains feature IDs that can be
    executed in parallel (all their dependencies are in previous buckets).

    Args:
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
    failing_parent_features: Optional[set[str]] = None,
    extra_env: Optional[Dict[str, str]] = None,
) -> FeatureResult:
    """Execute all constraints in a feature and return aggregated results.

    If feature has depends_on and any parent failed in current run, proven constraints
    (fails_count > 0) are skipped. Unproven constraints (fails_count == 0) always execute
    to establish proof.

    Args:
        feature: Feature with embedded constraints to execute
        failing_parent_features: Set of parent feature IDs that failed in current run
        extra_env: Env vars propagated to each constraint's execution

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
                result = execute_constraint(constraint, extra_env=extra_env)

            constraint_results[constraint_id] = result

    return FeatureResult(
        feature_id=feature.id,
        constraints_results=constraint_results if constraint_results else None
    )


def check_constraints(
    spec_json_path: str,
    feature_ids: Optional[list] = None,
    output_checks_path: Optional[str] = None,
    quiet: bool = False,
    extra_env: Optional[Dict[str, str]] = None,
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

    def info(msg: str) -> None:
        if not quiet:
            print(msg)

    info(f"📋 Loading spec from {spec_json_path}")

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
    info(f"🎯 Found {len(features_to_check)} features to check")

    # Build dependency buckets
    try:
        buckets = _build_dependency_buckets(features_to_check)
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
        info(f"  Bucket {bucket_idx + 1}/{len(buckets)}: executing {len(bucket)} feature(s)")
        for feature_id in bucket:
            feature = features_to_check[feature_id]
            feature_result = check_feature(feature, failing_parent_features=failing_features, extra_env=extra_env)
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
    info("📊 Aggregating results...")
    checks_results = ChecksResults(
        features_results=features_results if features_results else None
    )

    # Collect the 0 → 1 increments; fails_count is a verified/unverified flag, not
    # a counter. Already-verified constraints (fails_count > 0) are locked by
    # feature_model.py and don't need further writes.
    increments = []  # list of (feature_id, constraint_id)
    if checks_results.features_results and features:
        for feature_id, feature_result in checks_results.features_results.items():
            feature_obj = features.get(feature_id)
            if not feature_obj or not feature_result.constraints_results:
                continue

            for constraint_id, result in feature_result.constraints_results.items():
                if isinstance(result, ConstraintBashResult) and not result.verdict:
                    constraint_obj = feature_obj.constraints.get(constraint_id) if feature_obj.constraints else None
                    if isinstance(constraint_obj, ConstraintBash) and constraint_obj.fails_count == 0:
                        increments.append((feature_id, constraint_id))

    if increments:
        info("🔄 Updating fails_count for failed constraints...")
        # Deliberately not apply_json_patch — that path's mutation guard rejects
        # fails_count changes. _sync_spec_with_results is the checker's own
        # write path; see its docstring for the code-level boundary.
        _sync_spec_with_results(spec_path, doc_type, increments)
        info(f"✓ Updated fails_count for {len(increments)} constraint(s)")
        print(f"\n🚫 {len(increments)} constraint(s) now locked (cmd cannot be changed):")
        for feature_id, constraint_id in increments:
            print(f"   • {feature_id}.{constraint_id}")
        print("   Options: (1) Fix constraint to pass, or (2) Remove constraint entirely")

    # Save ChecksResults to file
    if output_checks_path:
        output_path = Path(output_checks_path)
        info(f"💾 Saving results to {output_checks_path}")

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
                        info(f"🗑️  Removing {len(features_to_remove)} feature(s) from checks_results (no longer in spec):")
                        for feature_id in sorted(features_to_remove):
                            info(f"   • {feature_id}")
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
                        info(f"🗑️  Removing {len(constraints_to_remove)} constraint(s) from checks_results (no longer in spec):")
                        for feature_id, constraint_id in sorted(constraints_to_remove):
                            info(f"   • {feature_id}.{constraint_id}")
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
                info(f"✓ Results saved to {output_checks_path}")
        else:
            info(f"ℹ️  No changes to ChecksResults (same features as before)")

    return checks_results


def generate_report(checks_results: ChecksResults, spec: Spec, spec_path: str, full_report: bool = False) -> int:
    """Print a human-readable report from ChecksResults and return an exit code.

    Returns 3 if any unverified, 2 if any constraint failed, 0 otherwise.

    Without --full-report, only warning/error sections (Failed, Unverified) are
    printed; on total success the output collapses to "PASS". Pass --full-report
    for the complete report including Tested Features, First-Run, and Skipped.
    """
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

    unverified_by_feature = {}
    if spec and spec.features:
        for feature_id, feature in spec.features.items():
            if feature.constraints:
                for constraint_id, constraint in feature.constraints.items():
                    fails_count = getattr(constraint, 'fails_count', 0)
                    if fails_count < 1:
                        unverified_by_feature.setdefault(feature_id, []).append((constraint_id, fails_count))

    failing_count = sum(len(constraints) for constraints in failed_constraints.values())
    has_unverified = bool(unverified_by_feature)

    if not full_report and failing_count == 0 and not has_unverified:
        print("PASS")
        return 0

    if full_report:
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

    if full_report and first_run_constraints:
        print("\n🔍 First-Run Verification (establishing proof):")
        for feature_id in sorted(first_run_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(first_run_constraints[feature_id]):
                print(f"    ✓ {constraint_id}")

    if full_report and skipped_constraints:
        print("\n⏸️  Skipped Constraints (waiting for dependencies):")
        for feature_id in sorted(skipped_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(skipped_constraints[feature_id]):
                print(f"    ⏸️  {constraint_id}")

    def _lookup_cmd(feature_id: str, constraint_id: str) -> Optional[str]:
        if not (spec and spec.features):
            return None
        feature = spec.features.get(feature_id)
        if not feature or not feature.constraints:
            return None
        constraint = feature.constraints.get(constraint_id)
        return getattr(constraint, 'cmd', None) if constraint else None

    # Unverified takes precedence: when present, suppress Failed Constraints
    # in quiet mode so the user focuses on fixing the unverified block first.
    if failed_constraints and (full_report or not has_unverified):
        print("\n❌ Failed Constraints:")
        for feature_id in sorted(failed_constraints.keys()):
            print(f"  {feature_id}:")
            for constraint_id, result in sorted(failed_constraints[feature_id]):
                output = getattr(result, 'shrunken_output', None) or getattr(result, 'output', None)
                print(f"    ✗ {constraint_id}")
                cmd = _lookup_cmd(feature_id, constraint_id)
                if cmd:
                    print(f"      $ {cmd}")
                if output:
                    for line in output.split('\n'):
                        if line.strip():
                            print(f"      {line}")

    if unverified_by_feature:
        print("\n⚠️  Unverified Blocking Constraints (fails_count < 1):")
        total_unverified = 0
        for feature_id in sorted(unverified_by_feature.keys()):
            constraints = unverified_by_feature[feature_id]
            total_unverified += len(constraints)
            print(f"\n  {feature_id}:")
            for constraint_id, fails_count in sorted(constraints):
                print(f"    ⚠️  {constraint_id} (fails_count={fails_count})")
                cmd = _lookup_cmd(feature_id, constraint_id)
                if cmd:
                    print(f"      $ {cmd}")
        print(f"\nTotal unverified: {total_unverified}")

    if unverified_by_feature:
        print(f"\n⚠️  Task features check DETECTED unverified constraints — code changes are blocked.")
        print(f"  Either adjust the constraints so they fail initially, or remove them entirely.")
        print(f"  Spec:    {Path(spec_path).resolve()}")
        print(f"  Project: {Path(spec_path).resolve().parent}")
        return 3
    elif failing_count > 0:
        print(f"\n✗ Task features check FAILED - constraints not satisfied")
        print(f"  Spec:    {Path(spec_path).resolve()}")
        print(f"  Project: {Path(spec_path).resolve().parent}")
        return 2
    else:
        print("\n✓ Task features check completed successfully")
        return 0


def _run_spec(
    spec_path: str,
    output_checks_path: Optional[str],
    feature_ids: Optional[list],
    dry_run: bool,
    quiet: bool,
    full_report: bool,
    extra_env: Optional[Dict[str, str]] = None,
) -> int:
    """Check a single spec file and print its report. Returns its exit code."""
    spec_data = json.loads(Path(spec_path).read_text())
    spec = Spec.model_validate(spec_data)

    spec_dir = Path(spec_path).parent
    if output_checks_path is None:
        output_checks_path = str(spec_dir / CONSTRAINTS_RESULTS_FILE)

    if dry_run:
        checks_path = Path(output_checks_path)
        if not checks_path.exists():
            print(f"✗ Error: checks results file not found: {checks_path}", file=sys.stderr)
            return 1
        if not quiet:
            print(f"📂 Loading existing checks results from {checks_path}")
        checks_data = json.loads(checks_path.read_text())
        checks_results = ChecksResults.model_validate(checks_data)
    else:
        checks_results = check_constraints(
            spec_path,
            feature_ids=feature_ids,
            output_checks_path=output_checks_path,
            quiet=quiet,
            extra_env=extra_env,
        )
        # check_constraints may have incremented fails_count on disk for
        # constraints that failed on their first run; reload so the report's
        # unverified-vs-verified classification reflects the post-sync state.
        spec = Spec.model_validate(json.loads(Path(spec_path).read_text()))

    return generate_report(checks_results, spec, spec_path, full_report=full_report)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Execute feature constraints for a Project (project.k.json) or a single Spec (spec.k.json).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Resolution order when no path is given:
  $PROJECT_ROOT/project.k.json  (if present, run each spec it references)
  $PROJECT_ROOT/spec.k.json     (otherwise)

Examples:
  # Default: pick project.k.json if present, else spec.k.json, under $PROJECT_ROOT
  python3 check_spec_constraints.py

  # Single spec
  python3 check_spec_constraints.py spec.k.json --features feature_1,feature_2
  python3 check_spec_constraints.py spec.k.json --output-checks-path spec-checks.k.json

  # Project: runs every spec it references, applying that spec's envs
  python3 check_spec_constraints.py project.k.json
        """
    )

    parser.add_argument(
        'doc_path',
        nargs='?',
        help='Path to project.k.json or spec.k.json (default: $PROJECT_ROOT/project.k.json '
             'if present, else $PROJECT_ROOT/spec.k.json)'
    )

    parser.add_argument(
        '--features',
        help='Comma-separated list of feature IDs to check (spec mode only; ignored for projects)',
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
        help=f'Path to save ChecksResults document (spec mode only; default: {CONSTRAINTS_RESULTS_FILE} next to spec)',
        type=str,
        default=None
    )

    parser.add_argument(
        '--full-report',
        action='store_true',
        help='Show complete report even when unverified constraints are present '
             '(default: suppress detail sections and show only the unverified block)'
    )

    args = parser.parse_args()
    quiet = not args.full_report

    # Resolve doc path: explicit arg > $PROJECT_ROOT/project.k.json (if exists) > $PROJECT_ROOT/spec.k.json
    if args.doc_path is None:
        project_root = os.environ.get('PROJECT_ROOT')
        if not project_root:
            print("Error: doc_path required (or set PROJECT_ROOT)", file=sys.stderr)
            return 1
        project_file = Path(project_root) / 'project.k.json'
        if project_file.exists():
            args.doc_path = str(project_file)
        else:
            args.doc_path = str(Path(project_root) / 'spec.k.json')
        if not quiet:
            print(f"📌 Using {args.doc_path}")

    feature_ids = None
    if args.features:
        feature_ids = [f.strip() for f in args.features.split(',')]

    try:
        doc_data = json.loads(Path(args.doc_path).read_text())
        doc_type = doc_data.get('type')

        if doc_type == 'Project':
            if args.features or args.output_checks_path:
                print("⚠️  --features and --output-checks-path are ignored in project mode", file=sys.stderr)

            project = Project.model_validate(doc_data)
            project_dir = Path(args.doc_path).resolve().parent

            if not project.specs:
                print("⚠️  Project has no specs")
                return 0

            worst_code = 0
            for spec_id, ref in sorted(project.specs.items()):
                # Resolve spec_dir: empty/"." → project file's dir; absolute → itself;
                # relative → joined with project file's dir.
                raw_dir = ref.spec_dir or "."
                raw_path = Path(raw_dir)
                spec_root = raw_path.resolve() if raw_path.is_absolute() else (project_dir / raw_path).resolve()
                spec_full_path = spec_root / 'spec.k.json'

                # Per-spec PROJECT_ROOT = its spec_dir; user envs layer on top and may override.
                env_for_spec = {'PROJECT_ROOT': str(spec_root)}
                env_for_spec.update({k: v.value for k, v in ref.envs.items()})

                if not quiet:
                    print(f"\n🧩 Spec [{spec_id}]: {spec_full_path}")
                    print(f"   PROJECT_ROOT={spec_root}")
                    if ref.envs:
                        printable = {k: v.value for k, v in ref.envs.items()}
                        print(f"   envs: {printable}")

                if not spec_full_path.exists():
                    print(f"✗ Error: spec not found: {spec_full_path}", file=sys.stderr)
                    worst_code = max(worst_code, 1)
                    continue

                code = _run_spec(
                    str(spec_full_path),
                    output_checks_path=None,
                    feature_ids=None,
                    dry_run=args.dry_run,
                    quiet=quiet,
                    full_report=args.full_report,
                    extra_env=env_for_spec,
                )
                worst_code = max(worst_code, code)
            return worst_code

        # Default: Spec document
        return _run_spec(
            args.doc_path,
            output_checks_path=args.output_checks_path,
            feature_ids=feature_ids,
            dry_run=args.dry_run,
            quiet=quiet,
            full_report=args.full_report,
        )

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

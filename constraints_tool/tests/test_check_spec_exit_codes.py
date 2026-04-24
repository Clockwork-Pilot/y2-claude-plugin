"""Exit-code tests for constraints_tool/check_spec_constraints.py.

Covers execution mode and --dry-run mode for three outcomes:
  0 — all constraints pass, none unverified
  2 — at least one failed, none unverified
  3 — at least one unverified (fails_count < 1)

Unverified takes precedence over failures (exit 3 wins over 2).
"""

import json
import os
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PLUGIN_ROOT / "constraints_tool" / "constraints_tool" / "check_spec_constraints.py"


def _spec(constraints):
    return {
        "type": "Spec",
        "model_version": 1,
        "version": 1,
        "description": "test spec",
        "features": {
            "f1": {
                "type": "Feature",
                "model_version": 1,
                "id": "f1",
                "description": "test feature",
                "goals": ["test goals"],
                "constraints": constraints,
            }
        },
    }


def _cb(cid, cmd, fails_count=1):
    c = {"id": cid, "cmd": cmd, "description": f"{cid} description"}
    if fails_count:
        c["fails_count"] = fails_count
    return c


def _run(spec_path: Path, *extra: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PROJECT_ROOT": str(spec_path.parent)}
    return subprocess.run(
        ["python3", str(SCRIPT), str(spec_path), *extra],
        capture_output=True,
        text=True,
        env=env,
    )


def _write_spec(tmp_path: Path, constraints: dict) -> Path:
    spec_path = tmp_path / "spec.k.json"
    spec_path.write_text(json.dumps(_spec(constraints), indent=2))
    return spec_path


# --- Execution mode ---------------------------------------------------------

def test_exit_0_all_pass_and_verified(tmp_path):
    spec_path = _write_spec(tmp_path, {
        "c_pass": _cb("c_pass", "true", fails_count=1),
    })
    result = _run(spec_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_exit_2_failure_with_verified_constraints(tmp_path):
    spec_path = _write_spec(tmp_path, {
        "c_fail": _cb("c_fail", "false", fails_count=1),
    })
    result = _run(spec_path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "FAILED" in result.stdout


def test_exit_3_unverified_passing_constraint(tmp_path):
    # Passing constraint with fails_count=0 stays unverified → exit 3
    spec_path = _write_spec(tmp_path, {
        "c_unverified": _cb("c_unverified", "true", fails_count=0),
    })
    result = _run(spec_path)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "Unverified Blocking Constraints" in result.stdout


def test_exit_3_takes_precedence_over_failure(tmp_path):
    # Mix: one unverified-passing + one failing verified. Unverified wins.
    spec_path = _write_spec(tmp_path, {
        "c_unverified": _cb("c_unverified", "true", fails_count=0),
        "c_fail": _cb("c_fail", "false", fails_count=1),
    })
    result = _run(spec_path)
    assert result.returncode == 3, result.stdout + result.stderr


# --- Dry-run mode -----------------------------------------------------------

def _seed_checks(spec_path: Path, results: dict) -> Path:
    checks_path = spec_path.parent / "spec-checks.k.json"
    checks_path.write_text(json.dumps({
        "type": "ChecksResults",
        "model_version": 1,
        "features_results": {
            "f1": {
                "feature_id": "f1",
                "constraints_results": results,
            }
        },
    }, indent=2))
    return checks_path


def _result(cid, verdict, fails_count=1):
    return {
        "constraint_id": cid,
        "verdict": verdict,
        "shrunken_output": "" if verdict else "[stderr] boom",
        "fails_count": fails_count,
        "postponed": False,
    }


def test_dry_run_exit_0(tmp_path):
    spec_path = _write_spec(tmp_path, {
        "c_pass": _cb("c_pass", "true", fails_count=1),
    })
    checks_path = _seed_checks(spec_path, {
        "c_pass": _result("c_pass", True, fails_count=1),
    })
    result = _run(spec_path, "--output-checks-path", str(checks_path), "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr


def test_dry_run_exit_2_failed_result(tmp_path):
    spec_path = _write_spec(tmp_path, {
        "c_fail": _cb("c_fail", "false", fails_count=1),
    })
    checks_path = _seed_checks(spec_path, {
        "c_fail": _result("c_fail", False, fails_count=1),
    })
    result = _run(spec_path, "--output-checks-path", str(checks_path), "--dry-run")
    assert result.returncode == 2, result.stdout + result.stderr


def test_dry_run_exit_3_unverified_in_spec(tmp_path):
    spec_path = _write_spec(tmp_path, {
        "c_unverified": _cb("c_unverified", "true", fails_count=0),
    })
    checks_path = _seed_checks(spec_path, {
        "c_unverified": _result("c_unverified", True, fails_count=0),
    })
    result = _run(spec_path, "--output-checks-path", str(checks_path), "--dry-run")
    assert result.returncode == 3, result.stdout + result.stderr
    assert "Unverified Blocking Constraints" in result.stdout


# --- --full-report toggle --------------------------------------------------

def test_default_suppresses_detail_sections_when_unverified(tmp_path):
    """Default: when unverified exist, only the unverified block is shown.

    Unverified takes top priority — Failed Constraints and Tested Features are
    suppressed so the user focuses on fixing unverified first.
    """
    spec_path = _write_spec(tmp_path, {
        "c_unverified": _cb("c_unverified", "true", fails_count=0),
        "c_fail": _cb("c_fail", "false", fails_count=1),
    })
    result = _run(spec_path)
    assert result.returncode == 3, result.stdout + result.stderr
    # Unverified block present
    assert "Unverified Blocking Constraints" in result.stdout
    # All other sections suppressed
    assert "Tested Features:" not in result.stdout
    assert "Failed Constraints:" not in result.stdout


def test_full_report_flag_shows_detail_sections_when_unverified(tmp_path):
    """--full-report re-enables the detail sections even when unverified exist."""
    spec_path = _write_spec(tmp_path, {
        "c_unverified": _cb("c_unverified", "true", fails_count=0),
        "c_fail": _cb("c_fail", "false", fails_count=1),
    })
    result = _run(spec_path, "--full-report")
    assert result.returncode == 3, result.stdout + result.stderr
    assert "Unverified Blocking Constraints" in result.stdout
    assert "Tested Features:" in result.stdout
    assert "Failed Constraints:" in result.stdout

"""Regression tests: check_spec_constraints.py must increment fails_count on failure.

The protection guard in feature_model.py locks fails_count against model-mediated
changes, but check_spec_constraints.py's flow is the one legitimate writer and
MUST be able to persist the increment back to the spec file.
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


def _cb(cid, cmd, fails_count=0):
    c = {"id": cid, "cmd": cmd, "description": f"{cid} description"}
    if fails_count:
        c["fails_count"] = fails_count
    return c


def _run(spec_path: Path, project_root: Path):
    env = {**os.environ, "CLAUDE_PROJECT_ROOT": str(project_root)}
    return subprocess.run(
        ["python3", str(SCRIPT), str(spec_path)],
        capture_output=True, text=True, env=env,
    )


def _fails_count(spec_path: Path, cid: str = "c_fail") -> int:
    data = json.loads(spec_path.read_text())
    return data["features"]["f1"]["constraints"][cid].get("fails_count", 0)


def test_fails_count_incremented_when_spec_at_workspace_root(tmp_path):
    """Baseline: failing constraint in a spec at CLAUDE_PROJECT_ROOT must bump 0→1."""
    spec_path = tmp_path / "spec.k.json"
    spec_path.write_text(json.dumps(_spec({
        "c_fail": _cb("c_fail", "false", fails_count=0),
    }), indent=2))

    result = _run(spec_path, project_root=tmp_path)
    assert result.returncode in (2, 3), result.stdout + result.stderr
    assert _fails_count(spec_path) == 1, (
        f"Expected fails_count=1 after failure, got {_fails_count(spec_path)}.\n"
        f"stdout:\n{result.stdout}"
    )


def test_fails_count_incremented_when_spec_in_subdirectory(tmp_path):
    """Bug repro: spec in a subdir (not at workspace root) must still bump 0→1."""
    subdir = tmp_path / "subproj"
    subdir.mkdir()
    spec_path = subdir / "spec.k.json"
    spec_path.write_text(json.dumps(_spec({
        "c_fail": _cb("c_fail", "false", fails_count=0),
    }), indent=2))

    result = _run(spec_path, project_root=tmp_path)
    assert result.returncode in (2, 3), result.stdout + result.stderr
    assert _fails_count(spec_path) == 1, (
        f"Expected fails_count=1 after failure, got {_fails_count(spec_path)}.\n"
        f"stdout:\n{result.stdout}"
    )


def test_fails_count_stays_at_one_on_already_verified_constraint(tmp_path):
    """fails_count is a verified-flag, not a counter. Once 1, it stays at 1 even
    if the constraint fails again. The checker must skip the patch attempt
    entirely — no noisy validation-rejected warnings, no write."""
    spec_path = tmp_path / "spec.k.json"
    spec_path.write_text(json.dumps(_spec({
        "c_fail": _cb("c_fail", "false", fails_count=1),
    }), indent=2))

    result = _run(spec_path, project_root=tmp_path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert _fails_count(spec_path) == 1, (
        f"Expected fails_count to stay at 1, got {_fails_count(spec_path)}.\n"
        f"stdout:\n{result.stdout}"
    )
    assert "Failed to update fails_count" not in result.stdout, (
        "Checker must not attempt a doomed patch on already-verified constraints.\n"
        f"stdout:\n{result.stdout}"
    )

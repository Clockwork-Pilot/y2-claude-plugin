"""Integration tests: Project.specs[...].envs (EnvVar) propagate to nested
spec constraints.

Replaces the inlined shell fixture previously embedded in
`constraint_project_envs_reach_spec_cmd` in claude-plugin/spec.k.json.
Verifies the checker injects each SpecRef env's `value` into the spec's
constraint command environment, and that user envs layer on top of the
per-spec PROJECT_ROOT default.
"""

import json
import os
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PLUGIN_ROOT / "constraints_tool" / "constraints_tool" / "check_spec_constraints.py"


def _run(doc_path: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PROJECT_ROOT": str(doc_path.parent)}
    return subprocess.run(
        ["python3", str(SCRIPT), str(doc_path)],
        capture_output=True,
        text=True,
        env=env,
    )


def _write_spec(spec_dir: Path, cmd: str) -> None:
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec = {
        "type": "Spec",
        "model_version": 1,
        "version": 1,
        "description": "env propagation test",
        "features": {
            "f": {
                "type": "Feature",
                "model_version": 1,
                "id": "f",
                "description": "env propagation",
                "goals": ["assert env reaches constraint cmd"],
                "constraints": {
                    "c_assert_env": {
                        "id": "c_assert_env",
                        "cmd": cmd,
                        "description": "assert env propagated from Project",
                        "fails_count": 1,
                    },
                },
            },
        },
    }
    (spec_dir / "spec.k.json").write_text(json.dumps(spec, indent=2))


def _write_project(tmp_path: Path, envs: dict) -> Path:
    project = {
        "type": "Project",
        "model_version": 1,
        "specs": {
            "s": {"spec_dir": "", "envs": envs},
        },
    }
    project_path = tmp_path / "project.k.json"
    project_path.write_text(json.dumps(project, indent=2))
    return project_path


def test_project_env_value_reaches_constraint_cmd(tmp_path):
    """Declared SpecRef.envs (EnvVar) reach the constraint command as env vars."""
    _write_spec(tmp_path, cmd='[ "$DEMO_ENV" = "hello" ]')
    project_path = _write_project(tmp_path, {
        "DEMO_ENV": {"value": "hello", "info": "test env doc"},
    })
    result = _run(project_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_project_env_override_of_project_root(tmp_path):
    """A SpecRef env named PROJECT_ROOT overrides the per-spec default."""
    override = tmp_path / "custom_root"
    override.mkdir()
    _write_spec(tmp_path, cmd=f'[ "$PROJECT_ROOT" = "{override}" ]')
    project_path = _write_project(tmp_path, {
        "PROJECT_ROOT": {"value": str(override), "info": "override default"},
    })
    result = _run(project_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_project_env_info_is_optional(tmp_path):
    """EnvVar.info defaults to empty string — envs without info still work."""
    _write_spec(tmp_path, cmd='[ "$DEMO_ENV" = "hello" ]')
    project_path = _write_project(tmp_path, {
        "DEMO_ENV": {"value": "hello"},
    })
    result = _run(project_path)
    assert result.returncode == 0, result.stdout + result.stderr

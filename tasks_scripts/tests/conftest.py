"""
Pytest configuration and shared fixtures for task management tests.

Provides:
- Pydantic model factories for tests
- Temporary task file fixtures
- TEST_LOG environment variable setup for test isolation
"""
import pytest
import os
from io import StringIO
from datetime import datetime
from pathlib import Path

from tasks_scripts.models import (
    PhaseHeader, ScoringEntry, RollbackEntry, Phase, TaskDocument, MetricsFile
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    # Enable TEST_LOG for structured logging isolation
    if "TEST_LOG" not in os.environ:
        os.environ["TEST_LOG"] = "memory"


@pytest.fixture
def sample_phase_header():
    """Factory for sample PhaseHeader."""
    return PhaseHeader(
        phase_name="TASK_PLAN.DEFINE",
        timestamp=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
    )


@pytest.fixture
def sample_scoring_entry():
    """Factory for sample ScoringEntry."""
    return ScoringEntry(
        timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
        metrics={"coverage": 85, "tests": 42},
        test_results=["test_1", "test_2 (FAILED)"]
    )


@pytest.fixture
def sample_rollback_entry():
    """Factory for sample RollbackEntry."""
    return RollbackEntry(
        from_phase="EXEC_EVAL.TESTING",
        timestamp=datetime.fromisoformat("2026-02-26T12:00:00+00:00"),
        issue_type="metrics_regression",
        problem_description="Test coverage decreased by 5%"
    )


@pytest.fixture
def sample_phase(sample_phase_header, sample_scoring_entry):
    """Factory for sample Phase."""
    return Phase(
        header=sample_phase_header,
        content="Sample phase content",
        scoring_entries=[sample_scoring_entry]
    )


@pytest.fixture
def sample_task_document(sample_phase):
    """Factory for sample TaskDocument."""
    return TaskDocument(
        phases=[sample_phase],
        current_phase="TASK_PLAN.DEFINE",
        created_at=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
    )


@pytest.fixture
def sample_metrics():
    """Factory for sample MetricsFile."""
    return MetricsFile(
        TEST_PLAN={"coverage": 85, "tests": 42},
        CODING={"complexity": "low"},
        TESTING={"duration_ms": 1200}
    )


@pytest.fixture
def temp_task_file(tmp_path):
    """Create a temporary .TASK.md file for testing."""
    task_file = tmp_path / ".TASK.md"
    task_file.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Test task content.

<!-- TASK_PLAN.DEFINE -->
""")
    return task_file


@pytest.fixture
def fixtures_dir():
    """Get path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def test_log_stream():
    """Provide StringIO stream for TEST_LOG output during tests."""
    return StringIO()

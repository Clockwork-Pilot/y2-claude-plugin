"""
Parser validation tests for task document → Pydantic model conversion.

These tests validate that markdown documents are correctly parsed into
our internal Pydantic data structures.

TDD Approach: These tests are written FIRST and should FAIL before
implementation of parsing logic.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from tasks_scripts.models import (
    PhaseHeader, ScoringEntry, RollbackEntry, Phase, TaskDocument, MetricsFile
)


class TestPhaseHeaderParsing:
    """Test PhaseHeader model validation and parsing."""

    def test_parse_phase_header_valid(self):
        """Valid phase header should parse correctly."""
        header = PhaseHeader(
            phase_name="TASK_PLAN.DEFINE",
            timestamp=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )
        assert header.phase_name == "TASK_PLAN.DEFINE"
        assert isinstance(header.timestamp, datetime)

    def test_parse_invalid_timestamp_raises_validation_error(self):
        """Invalid timestamp format should raise ValidationError."""
        with pytest.raises(ValidationError):
            PhaseHeader(
                phase_name="TASK_PLAN.DEFINE",
                timestamp="invalid-timestamp"
            )


class TestScoringEntryParsing:
    """Test ScoringEntry model with metrics and test results."""

    def test_parse_scoring_entry_with_metrics_dict(self):
        """ScoringEntry should parse metrics dictionary correctly."""
        entry = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"coverage": 85, "tests_passed": 42, "tests_failed": 0}
        )
        assert entry.metrics["coverage"] == 85
        assert entry.test_results is None

    def test_parse_scoring_entry_with_test_results_list(self):
        """ScoringEntry should parse test results list correctly."""
        test_list = [
            "test_task_create_valid",
            "test_task_roll_basic",
            "test_task_parse_error (FAILED)"
        ]
        entry = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"coverage": 80},
            test_results=test_list
        )
        assert entry.test_results == test_list
        assert len(entry.test_results) == 3


class TestRollbackEntryParsing:
    """Test RollbackEntry model parsing."""

    def test_parse_rollback_entry(self):
        """RollbackEntry should parse all fields correctly."""
        entry = RollbackEntry(
            from_phase="EXEC_EVAL.TESTING",
            timestamp=datetime.fromisoformat("2026-02-26T12:30:00+00:00"),
            issue_type="metrics_regression",
            problem_description="Test coverage decreased by 5%"
        )
        assert entry.from_phase == "EXEC_EVAL.TESTING"
        assert entry.issue_type == "metrics_regression"


class TestPhaseModelParsing:
    """Test Phase model with full content and nested entries."""

    def test_parse_phase_with_scoring_and_rollback_entries(self):
        """Phase should parse with nested scoring and rollback entries."""
        header = PhaseHeader(
            phase_name="TASK_PLAN.DEFINE",
            timestamp=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )
        scoring = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"status": "initial"}
        )
        phase = Phase(
            header=header,
            content="Some phase content",
            scoring_entries=[scoring]
        )
        assert len(phase.scoring_entries) == 1
        assert phase.header.phase_name == "TASK_PLAN.DEFINE"


class TestTaskDocumentParsing:
    """Test TaskDocument model parsing."""

    def test_parse_full_task_document(self):
        """TaskDocument should parse multiple phases correctly."""
        header1 = PhaseHeader(
            phase_name="TASK_PLAN.DEFINE",
            timestamp=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )
        header2 = PhaseHeader(
            phase_name="TASK_PLAN.REFINE_CONTEXT",
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00")
        )
        phase1 = Phase(header=header1, content="Content 1")
        phase2 = Phase(header=header2, content="Content 2")

        doc = TaskDocument(
            phases=[phase1, phase2],
            current_phase="TASK_PLAN.REFINE_CONTEXT",
            created_at=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )
        assert len(doc.phases) == 2
        assert doc.current_phase == "TASK_PLAN.REFINE_CONTEXT"


class TestMetricsFileParsing:
    """Test MetricsFile model parsing."""

    def test_parse_metrics_file_with_exec_eval_structure(self):
        """MetricsFile should parse TEST_PLAN, CODING, TESTING metrics."""
        metrics = MetricsFile(
            TEST_PLAN={"coverage": 85, "tests": 42},
            CODING={"complexity": "low"},
            TESTING={"duration_ms": 1200}
        )
        assert metrics.TEST_PLAN["coverage"] == 85
        assert metrics.TESTING["duration_ms"] == 1200


class TestParsingErrors:
    """Test error handling in parsing."""

    def test_parse_malformed_metrics_raises_validation_error(self):
        """Malformed metrics should raise ValidationError."""
        with pytest.raises(ValidationError):
            ScoringEntry(
                timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
                metrics="not_a_dict"  # Should be dict
            )


class TestRoundTripEquivalence:
    """Test markdown → model → markdown round-trip equivalence."""

    def test_roundtrip_markdown_to_model_to_markdown_equivalence(self):
        """Data should survive model round-trip without loss."""
        # Create a complete task document
        header = PhaseHeader(
            phase_name="EXEC_EVAL.TEST_PLAN",
            timestamp=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )
        scoring = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"coverage": 90, "tests": 100},
            test_results=["test_1", "test_2 (FAILED)"]
        )
        phase = Phase(
            header=header,
            content="Phase content",
            scoring_entries=[scoring]
        )
        doc = TaskDocument(
            phases=[phase],
            current_phase="EXEC_EVAL.TEST_PLAN",
            created_at=datetime.fromisoformat("2026-02-26T10:00:00+00:00")
        )

        # Verify model validity
        assert doc.phases[0].scoring_entries[0].metrics == {"coverage": 90, "tests": 100}
        assert doc.current_phase == "EXEC_EVAL.TEST_PLAN"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

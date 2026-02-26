"""
Unit tests for task_state.py - parsing, writing, and validation.

Tests verify that task documents are correctly loaded, parsed into Pydantic models,
and can be safely updated with atomic regex operations.

TDD Approach: These tests validate model consistency and data integrity.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from pydantic import ValidationError

from tasks_scripts.task_state import (
    load_task_document, append_to_phase, append_scoring,
    append_rollback_entry, validate_document_structure,
    load_metrics, save_metrics
)
from tasks_scripts.models import (
    TaskDocument, Phase, PhaseHeader, ScoringEntry, RollbackEntry, MetricsFile
)


class TestLoadTaskDocument:
    """Test loading and parsing task documents."""

    def test_load_valid_single_phase_document(self, tmp_path):
        """Load valid single-phase document."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Initial phase content here.

<!-- TASK_PLAN.DEFINE -->
""")
        doc = load_task_document(str(doc_path))

        assert isinstance(doc, TaskDocument)
        assert doc.current_phase == "TASK_PLAN.DEFINE"
        assert len(doc.phases) == 1

    def test_load_valid_multi_phase_document(self, tmp_path):
        """Load valid multi-phase document."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Phase 1 content.

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T11:00:00+00:00

Phase 2 content.

<!-- TASK_PLAN.REFINE_CONTEXT -->
""")
        doc = load_task_document(str(doc_path))

        assert len(doc.phases) == 2
        assert doc.current_phase == "TASK_PLAN.REFINE_CONTEXT"
        assert doc.phases[0].header.phase_name == "TASK_PLAN.DEFINE"
        assert doc.phases[1].header.phase_name == "TASK_PLAN.REFINE_CONTEXT"

    def test_load_extracts_current_phase_correctly(self, tmp_path):
        """Current phase should be the last phase in document."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->

# PHASE EXEC_EVAL.CODING at 2026-02-26T15:00:00+00:00
Content.
<!-- EXEC_EVAL.CODING -->
""")
        doc = load_task_document(str(doc_path))
        assert doc.current_phase == "EXEC_EVAL.CODING"

    def test_load_returns_task_document_pydantic_model(self, tmp_path):
        """Loaded document should be valid Pydantic TaskDocument."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->
""")
        doc = load_task_document(str(doc_path))

        # Verify Pydantic model validation
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.phases[0].header.timestamp, datetime)

    def test_load_raises_file_not_found(self, tmp_path):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            load_task_document(str(tmp_path / "nonexistent.md"))

    def test_load_reports_missing_phase_header_error(self, tmp_path):
        """Should raise ValueError for documents with no phase headers."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("This has no phase headers.")

        with pytest.raises(ValueError, match="No phase headers found"):
            load_task_document(str(doc_path))

    def test_load_reports_invalid_timestamp(self, tmp_path):
        """Should raise ValueError for invalid RFC 3339 timestamp."""
        doc_path = tmp_path / ".TASK.md"
        doc_path.write_text("""# PHASE TASK_PLAN.DEFINE at invalid-timestamp
Content.
<!-- TASK_PLAN.DEFINE -->
""")
        with pytest.raises(ValueError, match="Invalid RFC 3339 timestamp"):
            load_task_document(str(doc_path))


class TestAppendToPhase:
    """Test atomic regex updates to phases."""

    def test_append_content_to_single_phase(self, tmp_path):
        """Append content to single-phase document."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Original content.
<!-- TASK_PLAN.DEFINE -->"""

        updated = append_to_phase(markdown, "TASK_PLAN.DEFINE", "New content.")
        assert "Original content." in updated
        assert "New content." in updated
        assert updated.count("<!-- TASK_PLAN.DEFINE -->") == 1

    def test_append_content_before_phase_marker(self, tmp_path):
        """Appended content should be inserted before section marker."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Old.
<!-- TASK_PLAN.DEFINE -->"""

        updated = append_to_phase(markdown, "TASK_PLAN.DEFINE", "New.")
        # New content should be before marker
        new_pos = updated.find("New.")
        marker_pos = updated.find("<!-- TASK_PLAN.DEFINE -->")
        assert new_pos < marker_pos

    def test_append_to_multi_phase_document(self, tmp_path):
        """Append to current phase in multi-phase document."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Phase 1.
<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T11:00:00+00:00
Phase 2.
<!-- TASK_PLAN.REFINE_CONTEXT -->"""

        updated = append_to_phase(markdown, "TASK_PLAN.REFINE_CONTEXT", "More phase 2.")
        assert "Phase 1." in updated
        assert "Phase 2." in updated
        assert "More phase 2." in updated

    def test_append_earlier_phases_unchanged(self, tmp_path):
        """Earlier phases should remain unchanged after append."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Phase 1 content.
<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T11:00:00+00:00
Phase 2 content.
<!-- TASK_PLAN.REFINE_CONTEXT -->"""

        updated = append_to_phase(markdown, "TASK_PLAN.REFINE_CONTEXT", "NEW CONTENT")
        # Phase 1 should be unchanged
        assert updated[:updated.find("<!-- TASK_PLAN.DEFINE -->")].count("Phase 1 content.") == 1

    def test_append_raises_error_if_marker_not_found(self):
        """Should raise ValueError if phase marker doesn't exist."""
        markdown = "# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00\nContent."

        with pytest.raises(ValueError, match="Phase marker not found"):
            append_to_phase(markdown, "TASK_PLAN.DEFINE", "New.")


class TestAppendScoring:
    """Test appending SCORING entries."""

    def test_append_scoring_creates_scoring_section(self, tmp_path):
        """Append scoring should create SCORING section if missing."""
        markdown = """# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T10:00:00+00:00
Phase content.
<!-- EXEC_EVAL.TEST_PLAN -->"""

        entry = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"coverage": 85}
        )
        updated = append_scoring(markdown, "EXEC_EVAL.TEST_PLAN", entry)

        assert "## SCORING" in updated
        assert "coverage: 85" in updated

    def test_append_scoring_with_test_results(self):
        """SCORING entry with test results should be formatted correctly."""
        markdown = """# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T10:00:00+00:00
Content.
<!-- EXEC_EVAL.TEST_PLAN -->"""

        entry = ScoringEntry(
            timestamp=datetime.fromisoformat("2026-02-26T11:00:00+00:00"),
            metrics={"tests": 42},
            test_results=["test_1", "test_2 (FAILED)"]
        )
        updated = append_scoring(markdown, "EXEC_EVAL.TEST_PLAN", entry)

        assert "- test_1" in updated
        assert "- test_2 (FAILED)" in updated


class TestValidateDocumentStructure:
    """Test document structure validation."""

    def test_validate_valid_document(self, tmp_path):
        """Valid document should return no errors."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->"""

        errors = validate_document_structure(markdown)
        assert len(errors) == 0

    def test_validate_reports_missing_phase_headers(self):
        """Should report missing phase headers."""
        markdown = "Just content, no phases."

        errors = validate_document_structure(markdown)
        assert any("No phase headers found" in e for e in errors)

    def test_validate_reports_invalid_timestamps(self):
        """Should report invalid RFC 3339 timestamps."""
        markdown = """# PHASE TASK_PLAN.DEFINE at invalid-time
Content.
<!-- TASK_PLAN.DEFINE -->"""

        errors = validate_document_structure(markdown)
        assert any("Invalid RFC 3339 timestamp" in e for e in errors)

    def test_validate_reports_missing_section_markers(self):
        """Should report missing section markers."""
        markdown = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- WRONG_MARKER -->"""

        errors = validate_document_structure(markdown)
        assert any("Missing section marker" in e for e in errors)


class TestMetricsIO:
    """Test metrics file loading and saving."""

    def test_load_metrics_returns_empty_if_not_exists(self, tmp_path):
        """Load non-existent metrics file should return empty MetricsFile."""
        metrics = load_metrics(str(tmp_path / ".metrics"))
        assert isinstance(metrics, MetricsFile)

    def test_save_and_load_metrics(self, tmp_path):
        """Save and load metrics should preserve data."""
        metrics_path = tmp_path / ".metrics"

        original = MetricsFile(
            TEST_PLAN={"coverage": 85},
            CODING={"complexity": "low"}
        )
        save_metrics(str(metrics_path), original)

        loaded = load_metrics(str(metrics_path))
        assert loaded.TEST_PLAN == {"coverage": 85}
        assert loaded.CODING == {"complexity": "low"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

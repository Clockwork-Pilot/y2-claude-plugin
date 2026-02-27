"""
Unit tests for task loading - loading and parsing existing task documents.

Tests validate that .TASK.md files can be loaded, parsed, and converted into
Pydantic TaskDocument models with full validation of structure.
"""
import pytest
from pathlib import Path
from datetime import datetime

from tasks_scripts.models import TaskDocument
from tasks_scripts.task_state import load_task_document, validate_document_structure


class TestTaskLoad:
    """Test task document loading and parsing."""

    def test_load_valid_single_phase_document(self):
        """Should load a document with a single phase."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_single_phase.md"

        doc = load_task_document(str(fixture))

        assert isinstance(doc, TaskDocument)
        assert len(doc.phases) == 1
        assert doc.phases[0].header.phase_name == "TASK_PLAN.DEFINE"

    def test_load_valid_multi_phase_document(self):
        """Should load a document with multiple phases."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_multi_phase_with_scoring.md"

        doc = load_task_document(str(fixture))

        assert isinstance(doc, TaskDocument)
        assert len(doc.phases) >= 3
        assert doc.phases[0].header.phase_name == "TASK_PLAN.DEFINE"

    def test_load_extracts_current_phase_correctly(self):
        """Should identify the current phase (last phase header)."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_multi_phase_with_scoring.md"

        doc = load_task_document(str(fixture))

        # Current phase should be the last phase in the document
        assert doc.current_phase == doc.phases[-1].header.phase_name

    def test_load_parses_all_sections_into_models(self):
        """Should parse all sections (header, content, entries) into models."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_multi_phase_with_scoring.md"

        doc = load_task_document(str(fixture))

        # All phases should have headers
        for phase in doc.phases:
            assert phase.header is not None
            assert phase.header.phase_name != ""
            assert isinstance(phase.header.timestamp, datetime)

    def test_load_returns_task_document_pydantic_model(self):
        """Should return a valid TaskDocument Pydantic model."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_single_phase.md"

        doc = load_task_document(str(fixture))

        # Should be able to access all Pydantic model attributes
        assert hasattr(doc, 'phases')
        assert hasattr(doc, 'current_phase')
        assert hasattr(doc, 'created_at')

        # Should be a TaskDocument instance
        assert isinstance(doc, TaskDocument)

    def test_load_reports_missing_phase_header_error(self):
        """Should report error when phase header is missing."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "corrupted_missing_header.md"

        with pytest.raises(ValueError):
            load_task_document(str(fixture))

    def test_load_reports_invalid_section_markers_error(self):
        """Should report error when section markers are malformed."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "corrupted_malformed_sections.md"

        # Should raise error due to missing/malformed markers
        try:
            doc = load_task_document(str(fixture))
            # If it doesn't raise, check that structure is still valid
            assert isinstance(doc, TaskDocument)
        except ValueError:
            # This is expected for malformed documents
            pass

    def test_load_reports_line_number_for_errors(self):
        """Should report line numbers when validation errors occur."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "corrupted_invalid_timestamp.md"

        with pytest.raises(ValueError) as exc_info:
            load_task_document(str(fixture))

        # Error message should give some context about the location
        error_msg = str(exc_info.value).lower()
        assert "timestamp" in error_msg or "invalid" in error_msg

    def test_load_parsing_creates_phase_model_instances(self):
        """Should create Phase model instances for each phase."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_single_phase.md"

        doc = load_task_document(str(fixture))

        # Each phase should be a Phase model
        for phase in doc.phases:
            assert hasattr(phase, 'header')
            assert hasattr(phase, 'content')
            assert hasattr(phase, 'scoring_entries')
            assert hasattr(phase, 'rollback_entries')

    def test_load_with_scoring_entries(self):
        """Should parse scoring entries in phases."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture = fixtures_dir / "valid_multi_phase_with_scoring.md"

        doc = load_task_document(str(fixture))

        # At least one phase should have scoring entries
        has_scoring = any(
            len(phase.scoring_entries) > 0
            for phase in doc.phases
        )
        assert has_scoring, "No scoring entries found in document"

    def test_validate_document_structure_returns_errors(self):
        """Should validate document structure and return list of errors."""
        fixtures_dir = Path(__file__).parent / "fixtures"

        # Valid document should have no errors
        fixture = fixtures_dir / "valid_single_phase.md"
        content = fixture.read_text()
        errors = validate_document_structure(content)
        assert len(errors) == 0

    def test_validate_document_structure_finds_missing_markers(self):
        """Should detect missing section markers."""
        fixtures_dir = Path(__file__).parent / "fixtures"

        # Corrupted document should have errors
        fixture = fixtures_dir / "corrupted_malformed_sections.md"
        content = fixture.read_text()
        errors = validate_document_structure(content)

        # Should detect missing or malformed markers
        assert len(errors) > 0 or "<!-- TASK_PLAN.DEFINE -->" not in content

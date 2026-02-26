"""
Tests for task_create.py - Task initialization functionality.

TDD Approach: These tests verify the contract for task creation.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from pydantic import ValidationError

from tasks_scripts.task_create import create_task
from tasks_scripts.task_state import load_task_document
from tasks_scripts.models import TaskDocument


class TestTaskCreate:
    """Test task creation script."""

    def test_create_task_initializes_file_with_task_plan_define_header(self, tmp_path):
        """Task creation should initialize with TASK_PLAN.DEFINE phase."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))

        assert doc.current_phase == "TASK_PLAN.DEFINE"
        assert doc.phases[0].header.phase_name == "TASK_PLAN.DEFINE"

    def test_create_task_records_rfc3339_timestamp(self, tmp_path):
        """Task file should have valid RFC 3339 timestamp."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))

        # Timestamp should be datetime instance
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.phases[0].header.timestamp, datetime)

        # Should be parseable as RFC 3339
        iso_str = doc.created_at.isoformat()
        assert "T" in iso_str
        assert "+" in iso_str or "Z" in iso_str or "-" in iso_str

    def test_create_task_creates_file_in_correct_location(self, tmp_path):
        """Task file should be created at specified path."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        assert task_path.exists()
        assert task_path.is_file()

    def test_create_task_fails_if_file_already_exists(self, tmp_path):
        """Should raise error if .TASK.md already exists."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("existing content")

        with pytest.raises(FileExistsError):
            create_task(str(task_path))

    def test_create_task_creates_valid_markdown_structure(self, tmp_path):
        """Generated markdown should be valid with section markers."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        content = task_path.read_text()

        # Check for required elements
        assert "# PHASE TASK_PLAN.DEFINE at" in content
        assert "<!-- TASK_PLAN.DEFINE -->" in content
        assert content.count("<!-- TASK_PLAN.DEFINE -->") == 1

    def test_create_task_pydantic_model_validation_succeeds_on_output(self, tmp_path):
        """Created task should parse as valid TaskDocument model."""
        task_path = tmp_path / ".TASK.md"
        created_doc = create_task(str(task_path))

        # Verify it's a valid TaskDocument
        assert isinstance(created_doc, TaskDocument)

        # Verify we can load it back
        loaded_doc = load_task_document(str(task_path))
        assert isinstance(loaded_doc, TaskDocument)
        assert loaded_doc.current_phase == "TASK_PLAN.DEFINE"

    def test_create_task_creates_parent_directories_if_needed(self, tmp_path):
        """Should create parent directories if they don't exist."""
        nested_path = tmp_path / "nested" / "dir" / ".TASK.md"

        create_task(str(nested_path))

        assert nested_path.exists()
        assert nested_path.parent.exists()

    def test_create_task_content_is_readable_and_well_formatted(self, tmp_path):
        """Created file should have readable, formatted markdown."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        content = task_path.read_text()

        # Should have proper markdown structure
        lines = content.strip().split("\n")
        assert lines[0].startswith("# PHASE")
        assert any(line.startswith("<!--") for line in lines)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

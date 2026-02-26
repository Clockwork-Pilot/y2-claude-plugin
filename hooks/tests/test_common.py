"""
Tests for hooks/common.py - task loading and context extraction.

Validates that hook handlers can safely load task documents and
extract context for logging without breaking handler execution.

TDD Approach: Tests verify hook integration without dependencies on
external task management modules being fully implemented.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from hooks.common import load_task_document_safe, get_task_context


class TestLoadTaskDocumentSafe:
    """Test safe task document loading for hooks."""

    def test_load_task_document_finds_task_in_current_directory(self, tmp_path, monkeypatch):
        """Should find .TASK.md in current directory."""
        # Create a task file
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->""")

        # Load from that directory
        doc = load_task_document_safe(str(tmp_path))
        assert doc is not None
        assert doc.current_phase == "TASK_PLAN.DEFINE"

    def test_load_task_document_searches_parent_directories(self, tmp_path, monkeypatch):
        """Should search parent directories for .TASK.md."""
        # Create nested directory structure
        parent = tmp_path
        child = tmp_path / "sub" / "nested"
        child.mkdir(parents=True)

        # Place task file in parent
        task_file = parent / ".TASK.md"
        task_file.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->""")

        # Load from nested child directory
        doc = load_task_document_safe(str(child))
        assert doc is not None
        assert doc.current_phase == "TASK_PLAN.DEFINE"

    def test_load_task_document_returns_none_if_not_found(self, tmp_path):
        """Should return None if .TASK.md not found."""
        # Empty directory - no .TASK.md
        doc = load_task_document_safe(str(tmp_path))
        assert doc is None

    def test_load_task_document_returns_valid_task_document_model(self, tmp_path):
        """Loaded document should be valid TaskDocument model."""
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("""# PHASE EXEC_EVAL.CODING at 2026-02-26T10:00:00+00:00
Content.
<!-- EXEC_EVAL.CODING -->""")

        doc = load_task_document_safe(str(tmp_path))

        assert doc is not None
        assert hasattr(doc, "phases")
        assert hasattr(doc, "current_phase")
        assert hasattr(doc, "created_at")
        assert isinstance(doc.created_at, datetime)

    def test_load_graceful_error_handling_on_corrupted_file(self, tmp_path):
        """Should gracefully handle corrupted task files (return None)."""
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("This is not a valid task document.")

        # Should not raise exception, just return None
        doc = load_task_document_safe(str(tmp_path))
        assert doc is None


class TestGetTaskContext:
    """Test task context extraction for logging."""

    def test_get_task_context_extracts_correct_metadata(self, tmp_path):
        """Should extract task_name, current_phase, created_at."""
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("""# PHASE EXEC_EVAL.TESTING at 2026-02-26T10:00:00+00:00
Content.
<!-- EXEC_EVAL.TESTING -->""")

        doc = load_task_document_safe(str(tmp_path))
        context = get_task_context(doc)

        assert context is not None
        assert "task_name" in context
        assert "current_phase" in context
        assert "created_at" in context
        assert context["current_phase"] == "EXEC_EVAL.TESTING"

    def test_get_task_context_returns_none_when_task_doc_is_none(self):
        """Should return None if task_doc is None."""
        context = get_task_context(None)
        assert context is None

    def test_get_task_context_created_at_is_iso_format(self, tmp_path):
        """created_at should be ISO format string."""
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.DEFINE -->""")

        doc = load_task_document_safe(str(tmp_path))
        context = get_task_context(doc)

        assert isinstance(context["created_at"], str)
        assert "T" in context["created_at"]  # ISO format


class TestHandlerIntegration:
    """Test that handlers can use task context safely."""

    def test_handler_can_log_task_context(self, tmp_path):
        """Handler should be able to access and log task context."""
        task_file = tmp_path / ".TASK.md"
        task_file.write_text("""# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T10:00:00+00:00
Content.
<!-- TASK_PLAN.REFINE_CONTEXT -->""")

        # Simulate handler pattern
        task_doc = load_task_document_safe(str(tmp_path))
        task_context = get_task_context(task_doc)

        # Handler should be able to build log entry
        log_entry = {
            "status": "success",
            "task": task_context,
            "handler_result": "completed"
        }

        assert log_entry["task"]["current_phase"] == "TASK_PLAN.REFINE_CONTEXT"

    def test_handler_execution_unaffected_if_task_missing(self):
        """Handler should work even if .TASK.md missing."""
        # No task file created
        task_doc = load_task_document_safe("/nonexistent/path")

        # Handler should still execute (task context is None)
        task_context = get_task_context(task_doc)

        log_entry = {
            "status": "success",
            "task": task_context,
            "handler_result": "completed"
        }

        # Handler completed successfully even with None task context
        assert log_entry["status"] == "success"
        assert log_entry["task"] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

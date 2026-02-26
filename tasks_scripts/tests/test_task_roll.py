"""
Tests for task_roll.py - Task phase progression functionality.

TDD Approach: These tests verify the contract for advancing tasks through the workflow.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from tasks_scripts.task_roll import advance_phase
from tasks_scripts.task_state import load_task_document, PHASE_WORKFLOW
from tasks_scripts.models import TaskDocument


class TestTaskRoll:
    """Test task phase advancement (rolling through workflow)."""

    def test_advance_to_next_phase_in_workflow(self, tmp_path):
        """Should advance task from TASK_PLAN.DEFINE to next phase."""
        # Create initial task
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized. Ready for planning and development.

<!-- TASK_PLAN.DEFINE -->
""")

        doc = advance_phase(str(task_path))

        assert doc.current_phase == "TASK_PLAN.REFINE_CONTEXT"
        assert len(doc.phases) == 2
        assert doc.phases[1].header.phase_name == "TASK_PLAN.REFINE_CONTEXT"

    def test_phase_header_updated_with_new_timestamp(self, tmp_path):
        """Each phase transition should record RFC 3339 timestamp."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized. Ready for planning and development.

<!-- TASK_PLAN.DEFINE -->
""")

        doc = advance_phase(str(task_path))

        # New phase should have a timestamp
        assert isinstance(doc.phases[1].header.timestamp, datetime)
        # Should be different from the initial timestamp (advanced in time)
        assert doc.phases[1].header.timestamp >= doc.phases[0].header.timestamp

    def test_all_prior_content_preserved(self, tmp_path):
        """Advancing phases should preserve all prior phase content."""
        task_path = tmp_path / ".TASK.md"
        original_content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Initial task planning completed.
- Design requirements gathered
- User stories identified

<!-- TASK_PLAN.DEFINE -->
"""
        task_path.write_text(original_content)

        doc = advance_phase(str(task_path))

        # Original phase should still exist
        assert doc.phases[0].header.phase_name == "TASK_PLAN.DEFINE"
        assert "Initial task planning" in doc.phases[0].content
        # New phase should be added
        assert doc.phases[1].header.phase_name == "TASK_PLAN.REFINE_CONTEXT"
        assert len(doc.phases) == 2

    def test_phase_transitions_recorded_in_chronological_order(self, tmp_path):
        """Multiple phase transitions should maintain chronological order."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        # Advance through 3 phases
        doc1 = advance_phase(str(task_path))
        assert doc1.current_phase == "TASK_PLAN.REFINE_CONTEXT"
        assert len(doc1.phases) == 2

        doc2 = advance_phase(str(task_path))
        assert doc2.current_phase == "TASK_PLAN.DESIGN"
        assert len(doc2.phases) == 3

        # Verify order
        assert doc2.phases[0].header.phase_name == "TASK_PLAN.DEFINE"
        assert doc2.phases[1].header.phase_name == "TASK_PLAN.REFINE_CONTEXT"
        assert doc2.phases[2].header.phase_name == "TASK_PLAN.DESIGN"

    def test_supports_all_7_phases_in_workflow(self, tmp_path):
        """Should support progression through all 7 defined workflow phases."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        # Advance through all 7 phases
        expected_phases = [
            "TASK_PLAN.DEFINE",
            "TASK_PLAN.REFINE_CONTEXT",
            "TASK_PLAN.DESIGN",
            "TASK_PLAN.DECOMPOSE",
            "EXEC_EVAL.TEST_PLAN",
            "EXEC_EVAL.CODING",
            "EXEC_EVAL.TESTING"
        ]

        for i in range(len(expected_phases) - 1):
            doc = load_task_document(str(task_path))
            assert doc.current_phase == expected_phases[i]

            doc = advance_phase(str(task_path))
            assert doc.current_phase == expected_phases[i + 1]

    def test_section_markers_preserved_after_roll(self, tmp_path):
        """All section markers should remain after phase advancement."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        doc = advance_phase(str(task_path))
        content = task_path.read_text()

        # Both markers should exist
        assert "<!-- TASK_PLAN.DEFINE -->" in content
        assert "<!-- TASK_PLAN.REFINE_CONTEXT -->" in content

    def test_fails_on_invalid_phase_sequence(self, tmp_path):
        """Should fail when trying to advance from final phase."""
        task_path = tmp_path / ".TASK.md"
        # Create a task at the final phase
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T11:00:00+00:00

Context refined.

<!-- TASK_PLAN.REFINE_CONTEXT -->

# PHASE TASK_PLAN.DESIGN at 2026-02-26T12:00:00+00:00

Design complete.

<!-- TASK_PLAN.DESIGN -->

# PHASE TASK_PLAN.DECOMPOSE at 2026-02-26T13:00:00+00:00

Decomposed.

<!-- TASK_PLAN.DECOMPOSE -->

# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T14:00:00+00:00

Test plan created.

<!-- EXEC_EVAL.TEST_PLAN -->

# PHASE EXEC_EVAL.CODING at 2026-02-26T15:00:00+00:00

Coding complete.

<!-- EXEC_EVAL.CODING -->

# PHASE EXEC_EVAL.TESTING at 2026-02-26T16:00:00+00:00

Testing complete.

<!-- EXEC_EVAL.TESTING -->
""")

        # Try to advance from final phase
        with pytest.raises(ValueError, match="invalid.*phase|final phase|no.*next"):
            advance_phase(str(task_path))

    def test_new_phase_has_empty_content_initially(self, tmp_path):
        """New phase should have empty or minimal content initially."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        doc = advance_phase(str(task_path))

        # New phase should exist with minimal content
        assert doc.phases[1].header.phase_name == "TASK_PLAN.REFINE_CONTEXT"
        assert isinstance(doc.phases[1].content, str)

    def test_advance_phase_returns_valid_pydantic_model(self, tmp_path):
        """advance_phase() should return valid TaskDocument model."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        doc = advance_phase(str(task_path))

        # Should be valid TaskDocument
        assert isinstance(doc, TaskDocument)
        assert isinstance(doc.phases, list)
        assert len(doc.phases) > 0

    def test_detects_concurrent_write_with_lock_file(self, tmp_path):
        """Should fail if lock file exists (concurrent write protection)."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        # Create a lock file to simulate concurrent access
        lock_path = tmp_path / ".TASK.md.lock"
        lock_path.write_text("locked")

        # Should fail with IOError about concurrent write
        with pytest.raises(IOError, match="locked|concurrent"):
            advance_phase(str(task_path))

    def test_cleanup_lock_file_after_advance(self, tmp_path):
        """Lock file should be cleaned up after successful advance."""
        task_path = tmp_path / ".TASK.md"
        task_path.write_text("""# PHASE TASK_PLAN.DEFINE at 2026-02-26T10:00:00+00:00

Task initialized.

<!-- TASK_PLAN.DEFINE -->
""")

        lock_path = tmp_path / ".TASK.md.lock"

        # Advance the phase
        advance_phase(str(task_path))

        # Lock file should be cleaned up
        assert not lock_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

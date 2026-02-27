"""
Unit tests for task_roll_back.py - rolling back to previous phase with issue tracking.

Tests validate that tasks can rollback to previous phases, with rollback entries
documenting the issue, timing, and reason for the rollback.
"""
import pytest
import time
from pathlib import Path
from datetime import datetime

from tasks_scripts.models import TaskDocument, RollbackEntry
from tasks_scripts.task_state import load_task_document, get_previous_phase, PHASE_WORKFLOW
from tasks_scripts.task_roll_back import rollback_phase


@pytest.fixture
def task_file_in_coding_phase(tmp_path):
    """Create a task file in EXEC_EVAL.CODING phase."""
    task_path = tmp_path / ".TASK.md"
    content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Initial planning phase.

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T09:30:00+00:00

Context refined.

<!-- TASK_PLAN.REFINE_CONTEXT -->

# PHASE TASK_PLAN.DESIGN at 2026-02-26T09:45:00+00:00

Design created.

<!-- TASK_PLAN.DESIGN -->

# PHASE TASK_PLAN.DECOMPOSE at 2026-02-26T10:00:00+00:00

Decomposed into tasks.

<!-- TASK_PLAN.DECOMPOSE -->

# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T10:15:00+00:00

Test plan created.

<!-- EXEC_EVAL.TEST_PLAN -->

# PHASE EXEC_EVAL.CODING at 2026-02-26T10:30:00+00:00

Coding in progress.

<!-- EXEC_EVAL.CODING -->
"""
    task_path.write_text(content)
    return task_path


class TestRollback:
    """Test rollback functionality."""

    def test_rollback_to_specified_phase(self, task_file_in_coding_phase):
        """Should rollback to a specified phase."""
        target_phase = "TASK_PLAN.REFINE_CONTEXT"
        reason = "architecture review failed"

        doc = rollback_phase(
            str(task_file_in_coding_phase),
            target_phase=target_phase,
            reason=reason
        )

        assert doc.current_phase == target_phase

    def test_rollback_to_previous_phase_when_target_not_specified(self, task_file_in_coding_phase):
        """Should rollback to previous phase if target not specified."""
        # Current phase is EXEC_EVAL.CODING, previous is TASK_PLAN.DECOMPOSE or TASK_PLAN.DESIGN
        # We need to find the previous one from PHASE_WORKFLOW
        original_phase = "EXEC_EVAL.CODING"
        expected_prev = get_previous_phase(original_phase)

        doc = rollback_phase(str(task_file_in_coding_phase), reason="error detected")

        assert doc.current_phase == expected_prev

    def test_rollback_entry_added_with_problem_description(self, task_file_in_coding_phase):
        """Rollback entry should include problem description."""
        target_phase = "TASK_PLAN.REFINE_CONTEXT"
        reason = "requirements changed"

        doc = rollback_phase(
            str(task_file_in_coding_phase),
            target_phase=target_phase,
            reason=reason
        )

        # Find the target phase in the document
        target = None
        for phase in doc.phases:
            if phase.header.phase_name == target_phase:
                target = phase
                break

        assert target is not None
        assert len(target.rollback_entries) > 0

        # Check the rollback entry
        rollback = target.rollback_entries[-1]
        assert reason in rollback.problem_description or reason.lower() in rollback.problem_description.lower()

    def test_rollback_entry_includes_timing_information(self, task_file_in_coding_phase):
        """Rollback entry should have timestamp."""
        target_phase = "TASK_PLAN.REFINE_CONTEXT"

        doc = rollback_phase(
            str(task_file_in_coding_phase),
            target_phase=target_phase,
            reason="test failed"
        )

        # Find target phase
        target = None
        for phase in doc.phases:
            if phase.header.phase_name == target_phase:
                target = phase
                break

        assert target is not None
        rollback = target.rollback_entries[-1]
        assert isinstance(rollback.timestamp, datetime)

    def test_newer_phase_data_preserved_after_rollback(self, task_file_in_coding_phase):
        """Content from newer phases should not be deleted, but current_phase should revert."""
        target_phase = "TASK_PLAN.REFINE_CONTEXT"

        doc = rollback_phase(
            str(task_file_in_coding_phase),
            target_phase=target_phase,
            reason="revert needed"
        )

        # All phases should still be in the document
        phase_names = [phase.header.phase_name for phase in doc.phases]
        assert "EXEC_EVAL.CODING" in phase_names
        assert "TASK_PLAN.REFINE_CONTEXT" in phase_names

        # Current phase should be the target
        assert doc.current_phase == target_phase

    def test_fails_on_invalid_target_phase(self, task_file_in_coding_phase):
        """Should raise error for invalid phase names."""
        with pytest.raises((ValueError, KeyError)):
            rollback_phase(
                str(task_file_in_coding_phase),
                target_phase="INVALID_PHASE",
                reason="error"
            )

    def test_rollback_entry_from_phase_recorded(self, task_file_in_coding_phase):
        """Rollback entry should record the phase being rolled back from."""
        current_phase = "EXEC_EVAL.CODING"
        target_phase = "TASK_PLAN.REFINE_CONTEXT"

        doc = rollback_phase(
            str(task_file_in_coding_phase),
            target_phase=target_phase,
            reason="test"
        )

        # Find target phase
        target = None
        for phase in doc.phases:
            if phase.header.phase_name == target_phase:
                target = phase
                break

        assert target is not None
        rollback = target.rollback_entries[-1]
        assert rollback.from_phase == current_phase

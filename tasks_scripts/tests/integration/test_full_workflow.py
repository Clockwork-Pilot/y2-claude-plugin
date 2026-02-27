"""
Integration tests for complete task management workflow.

Tests the full lifecycle: create → roll → metrics → roll → archive
"""
import json
import tempfile
from pathlib import Path

from tasks_scripts.task_create import create_task
from tasks_scripts.task_roll import advance_phase
from tasks_scripts.task_metrics import collect_metrics
from tasks_scripts.task_roll_back import rollback_phase
from tasks_scripts.task_archive import archive_task
from tasks_scripts.task_state import load_task_document


def test_complete_workflow_create_to_archive():
    """Test full workflow: create → advance → metrics → archive."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        task_file = tmp_path / ".TASK.md"

        # 1. Create task
        doc = create_task(str(task_file))
        assert task_file.exists()
        assert doc.current_phase == "TASK_PLAN.DEFINE"

        # 2. Advance through planning phases
        doc = advance_phase(str(task_file))
        assert doc.current_phase == "TASK_PLAN.REFINE_CONTEXT"

        doc = advance_phase(str(task_file))
        assert doc.current_phase == "TASK_PLAN.DESIGN"

        # 3. Advance to execution phases
        doc = advance_phase(str(task_file))
        assert doc.current_phase == "TASK_PLAN.DECOMPOSE"

        doc = advance_phase(str(task_file))
        assert doc.current_phase == "EXEC_EVAL.TEST_PLAN"

        # 4. Collect metrics
        metrics_data = {
            "coverage": 85.5,
            "tests_passed": 15,
            "tests_failed": 0,
            "test_results": ["test_one", "test_two", "test_three (FAILED)"]
        }
        doc, _ = collect_metrics(str(task_file), json.dumps(metrics_data))
        assert len(doc.phases[-1].scoring_entries) > 0

        # 5. Advance to CODING
        doc = advance_phase(str(task_file))
        assert doc.current_phase == "EXEC_EVAL.CODING"

        # 6. Add more metrics
        metrics_data2 = {"coverage": 90.0, "code_quality": 95}
        doc, _ = collect_metrics(str(task_file), json.dumps(metrics_data2))

        # 7. Advance to TESTING
        doc = advance_phase(str(task_file))
        assert doc.current_phase == "EXEC_EVAL.TESTING"

        # 8. Verify all phases present
        assert len(doc.phases) == 7

        # 9. Archive completed task
        archived_path = archive_task(str(task_file))
        assert Path(archived_path).exists()
        assert not task_file.exists()
        assert ".tasks_history" in archived_path


def test_large_document_workflow():
    """Test workflow with large document accumulation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        task_file = tmp_path / ".TASK.md"

        # Create task
        doc = create_task(str(task_file))

        # Roll through all phases adding metrics
        phases_to_traverse = [
            "TASK_PLAN.REFINE_CONTEXT",
            "TASK_PLAN.DESIGN",
            "TASK_PLAN.DECOMPOSE",
            "EXEC_EVAL.TEST_PLAN",
            "EXEC_EVAL.CODING",
            "EXEC_EVAL.TESTING",
        ]

        for i, target_phase in enumerate(phases_to_traverse):
            doc = advance_phase(str(task_file))
            assert doc.current_phase == target_phase

            # Add multiple metrics per phase
            for j in range(3):
                metrics = {"iteration": i, "attempt": j, "score": 70 + (j * 5)}
                doc, _ = collect_metrics(str(task_file), json.dumps(metrics))

        # Verify document is valid and large
        final_doc = load_task_document(str(task_file))
        assert len(final_doc.phases) == 7  # All phases created

        # Count total scoring entries
        total_scoring = sum(len(p.scoring_entries) for p in final_doc.phases)
        assert total_scoring >= 18  # At least 3 per phase for some phases

        # Archive should still work
        archived_path = archive_task(str(task_file))
        assert Path(archived_path).exists()

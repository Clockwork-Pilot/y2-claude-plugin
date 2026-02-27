"""
Unit tests for task_metrics.py - collecting and recording evaluation metrics.

Tests validate that metrics can be collected, stored in .metrics JSON file,
and appended to task document as scoring entries with test results lists.
"""
import json
import tempfile
from pathlib import Path
from datetime import datetime

import pytest

from tasks_scripts.models import TaskDocument, ScoringEntry, MetricsFile
from tasks_scripts.task_state import load_task_document, append_scoring
from tasks_scripts.task_metrics import collect_metrics


@pytest.fixture
def task_file_in_eval_phase(tmp_path):
    """Create a task file in EXEC_EVAL.TEST_PLAN phase."""
    task_path = tmp_path / ".TASK.md"
    content = """# TASK Document

# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T10:00:00+00:00

Test plan content here

<!-- EXEC_EVAL.TEST_PLAN -->
"""
    task_path.write_text(content)
    return task_path


class TestCollectMetrics:
    """Test metric collection functionality."""

    def test_collect_metrics_stores_in_metrics_json_file(self, task_file_in_eval_phase, tmp_path):
        """Metrics should be stored in .metrics JSON file."""
        metrics_data = {
            "coverage": 85.5,
            "tests_passed": 15,
            "tests_failed": 0
        }

        doc, metrics = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        metrics_file = tmp_path / ".metrics"
        assert metrics_file.exists()

        stored = json.loads(metrics_file.read_text())
        assert stored["EXEC_EVAL.TEST_PLAN"] == metrics_data

    def test_metrics_structure_supports_test_plan_coding_testing(self, task_file_in_eval_phase):
        """MetricsFile model should support TEST_PLAN, CODING, and TESTING phases."""
        metrics = MetricsFile()

        metrics.TEST_PLAN = {"coverage": 85.0}
        metrics.CODING = {"coverage": 90.0}
        metrics.TESTING = {"coverage": 95.0}

        assert metrics.TEST_PLAN["coverage"] == 85.0
        assert metrics.CODING["coverage"] == 90.0
        assert metrics.TESTING["coverage"] == 95.0

    def test_parse_test_results_list_from_metrics(self, task_file_in_eval_phase):
        """Test results list should be parsed from metrics input."""
        metrics_data = {
            "coverage": 85.0,
            "test_results": [
                "test_phase_header_valid",
                "test_parse_scoring_entry_with_metrics_dict",
                "test_append_to_phase (FAILED)"
            ]
        }

        doc, metrics = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        # The latest scoring entry should have test results
        assert len(doc.phases) > 0
        current_phase = doc.phases[-1]
        assert len(current_phase.scoring_entries) > 0

        last_entry = current_phase.scoring_entries[-1]
        assert last_entry.test_results == metrics_data["test_results"]

    def test_append_scoring_section_to_task_document(self, task_file_in_eval_phase):
        """Scoring section should be appended to task document."""
        metrics_data = {"coverage": 80.0}

        doc, metrics = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        # Reload to verify it was written
        doc_reloaded = load_task_document(str(task_file_in_eval_phase))
        current_phase = doc_reloaded.phases[-1]

        assert len(current_phase.scoring_entries) > 0

    def test_scoring_entry_includes_timestamp_and_metrics(self, task_file_in_eval_phase):
        """Scoring entry should have timestamp and metrics dict."""
        metrics_data = {
            "coverage": 85.0,
            "lines_added": 125,
            "lines_removed": 30
        }

        doc, metrics = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        current_phase = doc.phases[-1]
        entry = current_phase.scoring_entries[-1]

        assert isinstance(entry.timestamp, datetime)
        # Metrics are stored as strings in markdown, so compare keys exist
        assert all(key in entry.metrics for key in metrics_data.keys())
        # Verify the metrics were captured (values will be strings after markdown round-trip)
        assert len(entry.metrics) == len(metrics_data)

    def test_multiple_scoring_entries_timestamped_and_distinguishable(self, task_file_in_eval_phase):
        """Multiple scoring entries should have different timestamps."""
        metrics1 = {"coverage": 80.0}
        metrics2 = {"coverage": 85.0}

        doc1, _ = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics1)
        )

        # Delay to ensure different timestamps (timestamps are rounded to seconds)
        import time
        time.sleep(1.1)

        doc2, _ = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics2)
        )

        current_phase = doc2.phases[-1]
        entries = current_phase.scoring_entries

        assert len(entries) >= 2
        # Timestamps should be in chronological order
        assert entries[-2].timestamp < entries[-1].timestamp

    def test_metrics_fail_on_invalid_json_format(self, task_file_in_eval_phase):
        """Invalid JSON metrics should raise error."""
        with pytest.raises((json.JSONDecodeError, ValueError)):
            collect_metrics(
                str(task_file_in_eval_phase),
                "{ invalid json"
            )

    def test_scoring_appended_before_phase_section_marker(self, task_file_in_eval_phase):
        """Scoring should be appended before the phase section marker."""
        metrics_data = {"coverage": 88.0}

        doc, _ = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        content = task_file_in_eval_phase.read_text()

        # Check that scoring appears before the section marker
        scoring_pos = content.find("### ")
        marker_pos = content.find("<!-- EXEC_EVAL.TEST_PLAN -->")

        assert scoring_pos != -1
        assert marker_pos != -1
        assert scoring_pos < marker_pos

    def test_collect_metrics_returns_models(self, task_file_in_eval_phase):
        """collect_metrics should return TaskDocument and MetricsFile models."""
        metrics_data = {"coverage": 90.0}

        doc, metrics = collect_metrics(
            str(task_file_in_eval_phase),
            json.dumps(metrics_data)
        )

        assert isinstance(doc, TaskDocument)
        assert isinstance(metrics, MetricsFile)

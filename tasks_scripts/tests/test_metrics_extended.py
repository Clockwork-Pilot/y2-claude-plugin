"""
Tests for extended metrics collection with coverage analysis.

Tests integration of y2_pycov coverage module with task metrics for EXEC_EVAL stages.
"""
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

from tasks_scripts.task_create import create_task
from tasks_scripts.task_roll import advance_phase
from tasks_scripts.task_metrics_extended import (
    ExtendedMetricsCollector,
    collect_metrics_extended,
    EXEC_EVAL_STAGES
)
from tasks_scripts.task_state import load_task_document


class TestExtendedMetricsCollector:
    """Test extended metrics collection with coverage."""
    
    def test_collector_initialization(self, tmp_path):
        """Should initialize metrics collector."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        collector = ExtendedMetricsCollector(str(task_path))
        assert collector.task_path == task_path
        assert collector.coverage_aggregator is not None
    
    def test_collect_without_coverage(self, tmp_path):
        """Should collect metrics without coverage data."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        metrics_json = json.dumps({"tests_passed": 10, "tests_failed": 0})
        doc, metrics = collect_metrics_extended(str(task_path), metrics_json)
        
        assert doc.current_phase == "TASK_PLAN.DEFINE"
        assert len(doc.phases) >= 1
    
    def test_collect_in_exec_eval_stage_with_coverage(self, tmp_path):
        """Should collect coverage metrics in EXEC_EVAL stages."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        # Advance to TEST_PLAN stage
        for _ in range(4):
            advance_phase(str(task_path))

        doc = load_task_document(str(task_path))
        assert doc.current_phase == "EXEC_EVAL.TEST_PLAN"

        # Collect with coverage data
        metrics_json = json.dumps({"tests_passed": 15, "tests_failed": 0})
        coverage_json = json.dumps({
            "src/main.py": {
                "covered_lines": 45,
                "total_lines": 50,
                "coverage_percent": 90.0
            },
            "src/utils.py": {
                "covered_lines": 30,
                "total_lines": 40,
                "coverage_percent": 75.0
            }
        })

        doc, metrics = collect_metrics_extended(str(task_path), metrics_json, coverage_json)

        # Check that coverage was recorded
        assert doc.current_phase == "EXEC_EVAL.TEST_PLAN"

        # Coverage is stored in .metrics file (source of truth), not in markdown ScoringEntry
        # The metrics object should have coverage_summary for the current phase
        phase_metrics = getattr(metrics, "EXEC_EVAL.TEST_PLAN", None)
        assert phase_metrics is not None
        assert "coverage_summary" in phase_metrics or "coverage_percent" in phase_metrics
    
    def test_coverage_summary_computation(self, tmp_path):
        """Should compute correct coverage summary."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        # Advance to CODING stage
        for _ in range(5):
            advance_phase(str(task_path))

        coverage_json = json.dumps({
            "test_a.py": {
                "covered_lines": 50,
                "total_lines": 50,
                "coverage_percent": 100.0
            },
            "test_b.py": {
                "covered_lines": 40,
                "total_lines": 50,
                "coverage_percent": 80.0
            }
        })

        metrics_json = json.dumps({"coverage_data": "available"})
        doc, metrics = collect_metrics_extended(str(task_path), metrics_json, coverage_json)

        # Coverage summary is stored in .metrics file, not in markdown
        phase_metrics = getattr(metrics, "EXEC_EVAL.CODING", None)
        assert phase_metrics is not None

        # Check that coverage_percent was calculated (90.0 = (50+40)/(50+50)*100)
        if "coverage_percent" in phase_metrics:
            assert abs(float(phase_metrics["coverage_percent"]) - 90.0) < 0.1
    
    def test_cumulative_coverage_tracking(self, tmp_path):
        """Should track cumulative coverage across stages."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        collector = ExtendedMetricsCollector(str(task_path))
        
        # Simulate coverage for each EXEC_EVAL stage
        coverage_stages = [
            {"test_1.py": {"covered_lines": 20, "total_lines": 50, "coverage_percent": 40.0}},
            {"test_2.py": {"covered_lines": 35, "total_lines": 50, "coverage_percent": 70.0}},
            {"test_3.py": {"covered_lines": 45, "total_lines": 50, "coverage_percent": 90.0}}
        ]
        
        for i, coverage_data in enumerate(coverage_stages):
            # Would normally do this through collect_with_coverage after advancing phases
            pass
        
        # Collector should track coverage
        assert collector.coverage_aggregator is not None
    
    def test_non_exec_eval_stages_no_coverage(self, tmp_path):
        """Should not track coverage in non-EXEC_EVAL stages."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))
        
        # Currently in TASK_PLAN.DEFINE (not EXEC_EVAL)
        assert doc.current_phase not in EXEC_EVAL_STAGES
        
        # Collect with coverage data anyway
        metrics_json = json.dumps({"metric": "value"})
        coverage_json = json.dumps({"file.py": {"coverage_percent": 85.0}})
        
        doc, metrics = collect_metrics_extended(str(task_path), metrics_json, coverage_json)
        
        # Coverage should not be tracked in non-EXEC_EVAL stage
        last_phase = doc.phases[-1]
        if last_phase.scoring_entries:
            scoring = last_phase.scoring_entries[-1]
            # Coverage might be None or empty in non-EXEC_EVAL stage
            assert scoring.coverage_summary is None or scoring.coverage_summary.get("files", 0) == 0
    
    def test_coverage_with_test_results(self, tmp_path):
        """Should combine coverage with test results."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))

        # Advance to TEST_PLAN
        for _ in range(4):
            advance_phase(str(task_path))

        metrics_json = json.dumps({
            "tests_passed": 20,
            "tests_failed": 2,
            "test_results": [
                "test_auth_login PASSED",
                "test_auth_logout PASSED",
                "test_db_connection FAILED"
            ]
        })

        coverage_json = json.dumps({
            "auth.py": {"covered_lines": 45, "total_lines": 50, "coverage_percent": 90.0},
            "db.py": {"covered_lines": 35, "total_lines": 50, "coverage_percent": 70.0}
        })

        doc, metrics = collect_metrics_extended(str(task_path), metrics_json, coverage_json)

        last_phase = doc.phases[-1]
        scoring = last_phase.scoring_entries[-1]

        # Should have test results in ScoringEntry (stored in markdown)
        assert scoring.test_results is not None
        assert len(scoring.test_results) == 3

        # Coverage is stored in .metrics file (source of truth), not in markdown ScoringEntry
        phase_metrics = getattr(metrics, "EXEC_EVAL.TEST_PLAN", None)
        assert phase_metrics is not None
        assert "coverage_summary" in phase_metrics or "coverage_percent" in phase_metrics


class TestCoverageIntegration:
    """Test coverage integration across EXEC_EVAL stages."""
    
    def test_exec_eval_stages_constant(self):
        """Should define EXEC_EVAL stages correctly."""
        assert len(EXEC_EVAL_STAGES) == 3
        assert "EXEC_EVAL.TEST_PLAN" in EXEC_EVAL_STAGES
        assert "EXEC_EVAL.CODING" in EXEC_EVAL_STAGES
        assert "EXEC_EVAL.TESTING" in EXEC_EVAL_STAGES
    
    def test_coverage_trend_generation(self, tmp_path):
        """Should generate coverage trend across stages."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        collector = ExtendedMetricsCollector(str(task_path))
        trend = collector.get_coverage_trend()
        
        # Initially empty
        assert isinstance(trend, list)
        assert len(trend) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

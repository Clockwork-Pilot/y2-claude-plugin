"""
Extended metrics collection with coverage analysis for EXEC_EVAL stages.

Integrates with y2_pycov to collect per-file coverage metrics during
TEST_PLAN, CODING, and TESTING phases with cumulative tracking.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

from tasks_scripts.models import TaskDocument, ScoringEntry, MetricsFile
from tasks_scripts.task_state import (
    load_task_document,
    append_scoring,
    load_metrics,
    save_metrics,
)
from tasks_scripts.y2_pycov.metrics_aggregator import MetricsAggregator

# Supported EXEC_EVAL stages for extended coverage tracking
EXEC_EVAL_STAGES = ["EXEC_EVAL.TEST_PLAN", "EXEC_EVAL.CODING", "EXEC_EVAL.TESTING"]


class ExtendedMetricsCollector:
    """Collects metrics with extended coverage analysis for EXEC_EVAL stages."""
    
    def __init__(self, task_path: str = ".TASK.md"):
        """Initialize extended metrics collector.
        
        Args:
            task_path: Path to .TASK.md file
        """
        self.task_path = Path(task_path)
        self.coverage_aggregator = MetricsAggregator()
    
    def collect_with_coverage(
        self,
        metrics_json: str = "{}",
        coverage_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[TaskDocument, MetricsFile]:
        """Collect metrics with extended coverage analysis.
        
        For EXEC_EVAL stages, analyzes and includes per-file coverage metrics.
        
        Args:
            metrics_json: JSON string with base metrics
            coverage_data: Optional coverage data dict with per-file metrics
            
        Returns:
            Tuple of (updated TaskDocument, MetricsFile)
        """
        # Load current task
        doc = load_task_document(str(self.task_path))
        
        # Parse metrics
        try:
            metrics_dict = json.loads(metrics_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid metrics JSON: {e}") from e
        
        # Check if we're in an EXEC_EVAL stage
        is_exec_eval = doc.current_phase in EXEC_EVAL_STAGES
        
        # Extract test_results
        test_results = metrics_dict.pop("test_results", None)
        
        # Create scoring entry
        now = datetime.now(timezone.utc).replace(microsecond=0)
        
        # Build coverage data if in EXEC_EVAL stage
        coverage_info = None
        coverage_summary = None

        if is_exec_eval and coverage_data:
            try:
                coverage_info = self._process_coverage_data(coverage_data)
                coverage_summary = self._compute_coverage_summary(coverage_info, doc.current_phase)

                # Add coverage to metrics
                metrics_dict["coverage_percent"] = coverage_summary.get("overall", 0)
            except Exception as e:
                # Log but don't fail on coverage processing
                print(f"Warning: Coverage processing failed: {e}", file=sys.stderr)
                coverage_info = None
                coverage_summary = None
        
        entry = ScoringEntry(
            timestamp=now,
            metrics=metrics_dict,
            test_results=test_results,
            coverage=coverage_info,
            coverage_summary=coverage_summary
        )
        
        # If in EXEC_EVAL stage, track cumulative coverage
        if is_exec_eval:
            self.coverage_aggregator.add_stage_metrics(
                stage=doc.current_phase,
                timestamp=now,
                coverage_data=coverage_summary or {},
                file_metrics=coverage_info
            )
        
        # Read current markdown
        markdown_content = self.task_path.read_text(encoding='utf-8')
        
        # Append scoring entry
        updated_markdown = append_scoring(markdown_content, doc.current_phase, entry)
        
        # Save updated markdown
        self.task_path.write_text(updated_markdown, encoding='utf-8')
        
        # Reload document
        doc = load_task_document(str(self.task_path))
        
        # Save metrics file
        metrics_file_path = self.task_path.parent / ".metrics"
        metrics = load_metrics(str(metrics_file_path))
        
        phase_key = doc.current_phase
        phase_data = getattr(metrics, phase_key, None) or {}
        phase_data = dict(phase_data)
        phase_data.update(metrics_dict)
        
        # Add coverage summary to metrics file
        if coverage_summary:
            phase_data["coverage_summary"] = coverage_summary
        
        setattr(metrics, phase_key, phase_data)
        save_metrics(str(metrics_file_path), metrics)
        
        return doc, metrics
    
    def _process_coverage_data(self, coverage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and normalize coverage data from y2_pycov.
        
        Args:
            coverage_data: Raw coverage data dict
            
        Returns:
            Processed coverage dict with per-file metrics
        """
        processed = {}
        
        for filename, metrics in coverage_data.items():
            if isinstance(metrics, dict):
                processed[filename] = {
                    "covered_lines": metrics.get("covered_lines", 0),
                    "total_lines": metrics.get("total_lines", 0),
                    "coverage_percent": metrics.get("coverage_percent", 0.0),
                    "branch_coverage": metrics.get("branch_coverage", 0.0)
                }
        
        return processed
    
    def _compute_coverage_summary(
        self,
        coverage_info: Dict[str, Any],
        current_phase: str
    ) -> Dict[str, Any]:
        """Compute coverage summary from per-file metrics.
        
        Args:
            coverage_info: Per-file coverage dict
            current_phase: Current phase name
            
        Returns:
            Summary dict with overall and per-file coverage
        """
        if not coverage_info:
            return {"overall": 0.0, "files": {}}
        
        # Calculate overall coverage
        total_lines = sum(f.get("total_lines", 0) for f in coverage_info.values())
        covered_lines = sum(f.get("covered_lines", 0) for f in coverage_info.values())
        overall = (covered_lines / total_lines * 100) if total_lines > 0 else 0
        
        # Find best and worst coverage
        coverages = [f.get("coverage_percent", 0) for f in coverage_info.values()]
        
        return {
            "overall": round(overall, 2),
            "files": len(coverage_info),
            "best_coverage": max(coverages) if coverages else 0,
            "worst_coverage": min(coverages) if coverages else 0,
            "phase": current_phase,
            "per_file": coverage_info
        }
    
    def get_cumulative_coverage(self) -> Dict[str, Any]:
        """Get cumulative coverage across all EXEC_EVAL stages.
        
        Returns:
            Dict with cumulative coverage metrics
        """
        return self.coverage_aggregator.get_cumulative_coverage()
    
    def get_coverage_trend(self) -> list:
        """Get coverage trend across stages.
        
        Returns:
            List of coverage metrics over time
        """
        return self.coverage_aggregator.get_coverage_trend()


def collect_metrics_extended(
    task_path: str = ".TASK.md",
    metrics_json: str = "{}",
    coverage_json: Optional[str] = None
) -> Tuple[TaskDocument, MetricsFile]:
    """Collect metrics with optional extended coverage analysis.

    For EXEC_EVAL stages, integrates coverage metrics with cumulative tracking.

    Args:
        task_path: Path to .TASK.md file
        metrics_json: JSON string with base metrics
        coverage_json: Optional JSON string with per-file coverage data

    Returns:
        Tuple of (updated TaskDocument, MetricsFile)
    """
    collector = ExtendedMetricsCollector(task_path)

    coverage_data = None
    if coverage_json:
        try:
            coverage_data = json.loads(coverage_json)
        except json.JSONDecodeError:
            pass

    return collector.collect_with_coverage(metrics_json, coverage_data)


if __name__ == "__main__":
    try:
        task_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"
        metrics_json = sys.argv[2] if len(sys.argv) > 2 else "{}"
        coverage_json = sys.argv[3] if len(sys.argv) > 3 else None
        
        doc, metrics = collect_metrics_extended(task_path, metrics_json, coverage_json)
        print(f"✓ Metrics collected for phase: {doc.current_phase}")
        print(f"  Total phases: {len(doc.phases)}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

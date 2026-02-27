"""
Metrics aggregation for cumulative coverage tracking.

Aggregates and tracks coverage metrics across multiple test runs.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime


class MetricsAggregator:
    """Aggregates coverage metrics across test runs and stages."""
    
    def __init__(self):
        """Initialize metrics aggregator."""
        self.history: List[Dict[str, Any]] = []
        self.cumulative_metrics: Dict[str, Any] = {}
    
    def add_stage_metrics(
        self,
        stage: str,
        timestamp: datetime,
        coverage_data: Dict[str, Any],
        file_metrics: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add metrics from a test stage.
        
        Args:
            stage: Stage name (TEST_PLAN, CODING, TESTING)
            timestamp: When metrics were recorded
            coverage_data: Coverage metrics dict
            file_metrics: Per-file coverage metrics
        """
        entry = {
            "stage": stage,
            "timestamp": timestamp.isoformat(),
            "overall": coverage_data,
            "files": file_metrics or {}
        }
        self.history.append(entry)
    
    def get_cumulative_coverage(self) -> Dict[str, Any]:
        """Get cumulative coverage across all stages.
        
        Returns:
            Dict with cumulative metrics
        """
        if not self.history:
            return {"coverage": 0.0, "stages": []}
        
        total_coverage = sum(
            h.get("overall", {}).get("coverage_percent", 0)
            for h in self.history
        ) / len(self.history) if self.history else 0
        
        return {
            "coverage": total_coverage,
            "stages": [h["stage"] for h in self.history],
            "file_coverage": self._aggregate_file_coverage()
        }
    
    def _aggregate_file_coverage(self) -> Dict[str, Any]:
        """Aggregate per-file coverage across all stages.
        
        Returns:
            Dict with file-level coverage metrics
        """
        file_coverage = {}
        
        for entry in self.history:
            files = entry.get("files", {})
            for filename, metrics in files.items():
                if filename not in file_coverage:
                    file_coverage[filename] = {
                        "appearances": 0,
                        "total_coverage": 0.0,
                        "stages": []
                    }
                
                file_coverage[filename]["appearances"] += 1
                file_coverage[filename]["total_coverage"] += metrics.get("coverage_percent", 0)
                file_coverage[filename]["stages"].append(entry["stage"])
        
        # Calculate average coverage per file
        for filename, data in file_coverage.items():
            if data["appearances"] > 0:
                data["average_coverage"] = data["total_coverage"] / data["appearances"]
        
        return file_coverage
    
    def get_coverage_trend(self) -> List[Dict[str, Any]]:
        """Get coverage trend across stages.
        
        Returns:
            List of coverage metrics over time
        """
        return [
            {
                "stage": entry["stage"],
                "timestamp": entry["timestamp"],
                "coverage": entry["overall"].get("coverage_percent", 0)
            }
            for entry in self.history
        ]

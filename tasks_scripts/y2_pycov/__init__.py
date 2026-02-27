"""
Python Coverage Integration Module (y2_pycov)

Provides Python coverage analysis and per-file metrics tracking for task evaluation.
Integrates with task metrics to track cumulative coverage across test stages.
"""

from .coverage_analyzer import CoverageAnalyzer
from .metrics_aggregator import MetricsAggregator

__all__ = ["CoverageAnalyzer", "MetricsAggregator"]

"""
Task metrics collection script.

Collects code quality metrics at EXEC_EVAL phases and records in .metrics JSON
and .TASK.md SCORING entries. Supports test results lists for tracking test
execution across phases.
"""
import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

from tasks_scripts.models import TaskDocument, ScoringEntry, MetricsFile
from tasks_scripts.task_state import (
    load_task_document,
    append_scoring,
    load_metrics,
    save_metrics,
)


def collect_metrics(
    task_path: str = ".TASK.md",
    metrics_json: str = "{}"
) -> Tuple[TaskDocument, MetricsFile]:
    """
    Collect and record metrics at current phase.

    Args:
        task_path: Path to .TASK.md file
        metrics_json: JSON string with metrics data (dict with coverage, tests_passed, tests_failed, test_results)

    Returns:
        Tuple of (updated TaskDocument, MetricsFile)

    Raises:
        json.JSONDecodeError: If metrics_json is invalid
        FileNotFoundError: If task file not found
        ValueError: If invalid phase or structure
    """
    task_path = Path(task_path)
    metrics_dir = task_path.parent

    # Parse incoming metrics JSON
    try:
        metrics_data = json.loads(metrics_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid metrics JSON: {e}") from e

    if not isinstance(metrics_data, dict):
        raise ValueError("Metrics JSON must be a dict")

    # Load current task document
    doc = load_task_document(str(task_path))

    # Extract test_results if present (and remove from metrics_data dict)
    test_results = metrics_data.pop("test_results", None)

    # Create scoring entry
    now = datetime.now(timezone.utc).replace(microsecond=0)
    entry = ScoringEntry(
        timestamp=now,
        metrics=metrics_data,
        test_results=test_results
    )

    # Read current markdown content
    markdown_content = task_path.read_text(encoding='utf-8')

    # Append scoring entry to markdown
    updated_markdown = append_scoring(markdown_content, doc.current_phase, entry)

    # Save updated markdown
    task_path.write_text(updated_markdown, encoding='utf-8')

    # Reload document to get updated state
    doc = load_task_document(str(task_path))

    # Load or create .metrics file
    metrics_file_path = metrics_dir / ".metrics"
    metrics = load_metrics(str(metrics_file_path))

    # Update metrics for current phase
    phase_key = doc.current_phase

    # Get existing metrics for this phase, or create new dict
    phase_data = getattr(metrics, phase_key, None)
    if phase_data is None:
        phase_data = {}
    else:
        phase_data = dict(phase_data)  # Make a copy to avoid modifying original

    # Update with new metrics
    phase_data.update(metrics_data)

    # Store back in metrics object using setattr (allows extra fields with Pydantic)
    setattr(metrics, phase_key, phase_data)

    # Save metrics file
    save_metrics(str(metrics_file_path), metrics)

    return doc, metrics


if __name__ == "__main__":
    try:
        task_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"
        metrics_json = sys.argv[2] if len(sys.argv) > 2 else "{}"

        doc, metrics = collect_metrics(task_path, metrics_json)
        print(f"Metrics collected at {doc.current_phase}")
        sys.exit(0)

    except Exception as e:
        print(f"Error collecting metrics: {e}", file=sys.stderr)
        sys.exit(1)


"""
Task state management: Loading, parsing, updating, and saving task documents.

Core responsibilities:
- Load and parse .TASK.md markdown files into Pydantic models
- Validate document structure
- Append content to phases using atomic regex updates with section markers
- Save metrics to .metrics JSON files
"""
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import ValidationError

from tasks_scripts.models import (
    PhaseHeader, ScoringEntry, RollbackEntry, Phase, TaskDocument, MetricsFile
)


# Task workflow phases in order
PHASE_WORKFLOW = [
    "TASK_PLAN.DEFINE",
    "TASK_PLAN.REFINE_CONTEXT",
    "TASK_PLAN.DESIGN",
    "TASK_PLAN.DECOMPOSE",
    "EXEC_EVAL.TEST_PLAN",
    "EXEC_EVAL.CODING",
    "EXEC_EVAL.TESTING"
]


def get_next_phase(current_phase: str) -> str:
    """
    Get the next phase in the workflow.

    Args:
        current_phase: Current phase name (e.g., "TASK_PLAN.DEFINE")

    Returns:
        Next phase name in workflow

    Raises:
        ValueError: If current phase is not in workflow or is final phase
    """
    if current_phase not in PHASE_WORKFLOW:
        raise ValueError(f"Invalid phase: {current_phase}")

    current_index = PHASE_WORKFLOW.index(current_phase)

    if current_index >= len(PHASE_WORKFLOW) - 1:
        raise ValueError(f"No next phase after {current_phase} (final phase)")

    return PHASE_WORKFLOW[current_index + 1]


def get_previous_phase(current_phase: str) -> str:
    """
    Get the previous phase in the workflow.

    Args:
        current_phase: Current phase name

    Returns:
        Previous phase name in workflow

    Raises:
        ValueError: If current phase is not in workflow or is first phase
    """
    if current_phase not in PHASE_WORKFLOW:
        raise ValueError(f"Invalid phase: {current_phase}")

    current_index = PHASE_WORKFLOW.index(current_phase)

    if current_index <= 0:
        raise ValueError(f"No previous phase before {current_phase} (first phase)")

    return PHASE_WORKFLOW[current_index - 1]


def load_task_document(filepath: str) -> TaskDocument:
    """
    Load and parse a .TASK.md file into a Pydantic TaskDocument model.

    Args:
        filepath: Path to .TASK.md file

    Returns:
        TaskDocument model with all parsed phases

    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If document structure is invalid
        ValueError: If document is malformed
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Task document not found: {filepath}")

    content = path.read_text(encoding="utf-8")

    # Parse phase headers
    phase_pattern = r"^# PHASE\s+(\S+)\s+at\s+(.+)$"
    phase_matches = list(re.finditer(phase_pattern, content, re.MULTILINE))

    if not phase_matches:
        raise ValueError("No phase headers found in document")

    # Extract current phase (last phase header)
    last_match = phase_matches[-1]
    current_phase_name = last_match.group(1)

    # Parse all phases
    phases = []
    for i, match in enumerate(phase_matches):
        phase_name = match.group(1)
        timestamp_str = match.group(2)

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError as e:
            raise ValueError(f"Invalid RFC 3339 timestamp in phase header: {timestamp_str}") from e

        header = PhaseHeader(phase_name=phase_name, timestamp=timestamp)

        # Extract phase content (from current header to next header or section marker)
        start_pos = match.end()

        # Find end of this phase (next phase header or section marker)
        if i < len(phase_matches) - 1:
            end_pos = phase_matches[i + 1].start()
        else:
            # Last phase - content goes to end
            end_pos = len(content)

        phase_content = content[start_pos:end_pos].strip()

        # Extract SCORING entries
        scoring_entries = _parse_scoring_entries(phase_content)

        # Extract rollback entries
        rollback_entries = _parse_rollback_entries(phase_content)

        # Remove section markers from displayed content
        phase_content_clean = re.sub(r"<!--\s*:\S+\s*-->\s*", "", phase_content).strip()

        phase = Phase(
            header=header,
            content=phase_content_clean,
            scoring_entries=scoring_entries,
            rollback_entries=rollback_entries
        )
        phases.append(phase)

    # Get creation timestamp from first phase
    created_at = phases[0].header.timestamp if phases else datetime.now()

    # Create TaskDocument
    doc = TaskDocument(
        phases=phases,
        current_phase=current_phase_name,
        created_at=created_at
    )

    return doc


def _parse_scoring_entries(content: str) -> List[ScoringEntry]:
    """Parse SCORING entries from phase content."""
    entries = []

    # Look for SCORING section
    scoring_pattern = r"## SCORING\n(.*?)(?=<!--|\Z)"
    scoring_match = re.search(scoring_pattern, content, re.DOTALL)

    if not scoring_match:
        return entries

    scoring_section = scoring_match.group(1)

    # Find individual scoring entries (by timestamp)
    # Use [^\n]+ instead of .+ to match only the timestamp on the same line as ###
    entry_pattern = r"###\s+([^\n]+)\n(.*?)(?=###|\Z)"
    entry_matches = re.finditer(entry_pattern, scoring_section, re.DOTALL)

    for match in entry_matches:
        timestamp_str = match.group(1).strip()
        entry_content = match.group(2).strip()

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError:
            continue  # Skip invalid timestamps

        # Extract metrics from content
        metrics = {}
        test_results = None

        lines = entry_content.split("\n")
        for line in lines:
            if ":" in line and not line.startswith("-"):
                parts = line.split(":", 1)
                key = parts[0].strip().lower()
                value = parts[1].strip()
                metrics[key] = value
            elif line.startswith("-"):
                # Test result item
                if test_results is None:
                    test_results = []
                test_results.append(line[1:].strip())

        entry = ScoringEntry(
            timestamp=timestamp,
            metrics=metrics,
            test_results=test_results
        )
        entries.append(entry)

    return entries


def _parse_rollback_entries(content: str) -> List[RollbackEntry]:
    """Parse rollback entries from phase content."""
    entries = []

    # Rollback entry pattern: ### [RFC 3339 timestamp] Back from PHASE_NAME
    rollback_pattern = r"### (.+?) Back from\s+(\S+)\n(.*?)(?=###|\Z)"
    matches = re.finditer(rollback_pattern, content, re.DOTALL)

    for match in matches:
        timestamp_str = match.group(1).strip()
        from_phase = match.group(2).strip()
        problem_desc = match.group(3).strip()

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError:
            continue  # Skip invalid timestamps

        # Determine issue type from problem description
        issue_type = "loop" if "loop" in problem_desc.lower() else "metrics_regression"

        entry = RollbackEntry(
            from_phase=from_phase,
            timestamp=timestamp,
            issue_type=issue_type,
            problem_description=problem_desc
        )
        entries.append(entry)

    return entries


def append_to_phase(
    markdown_content: str,
    phase_id: str,
    new_content: str
) -> str:
    """
    Append content to a phase using atomic regex update.

    Uses section marker pattern: <!-- phase_id --> to identify phase end.
    Inserts new_content before the marker.

    Args:
        markdown_content: Full .TASK.md content as string
        phase_id: Phase identifier (e.g., "TASK_PLAN.DEFINE")
        new_content: Content to append

    Returns:
        Updated markdown content

    Raises:
        ValueError: If phase marker not found or multiple markers exist
    """
    marker = f"<!-- {phase_id} -->"

    if marker not in markdown_content:
        raise ValueError(f"Phase marker not found: {marker}")

    # Count markers - should only have one per phase
    marker_count = markdown_content.count(marker)
    if marker_count != 1:
        raise ValueError(f"Expected 1 phase marker for {phase_id}, found {marker_count}")

    # Use atomic regex: insert before marker
    pattern = rf"(<!-- {re.escape(phase_id)} -->)"
    replacement = new_content + "\n\\1"

    updated = re.sub(pattern, replacement, markdown_content)
    return updated


def append_scoring(
    markdown_content: str,
    phase_id: str,
    entry: ScoringEntry
) -> str:
    """
    Append a SCORING entry to a phase.

    Creates SCORING section if it doesn't exist, or appends to existing.

    Args:
        markdown_content: Full .TASK.md content
        phase_id: Target phase identifier
        entry: ScoringEntry model to append

    Returns:
        Updated markdown content
    """
    timestamp_str = entry.timestamp.isoformat()

    # Format metrics as markdown
    metrics_lines = [f"{k}: {v}" for k, v in entry.metrics.items()]

    # Format test results if present
    test_results_lines = []
    if entry.test_results:
        test_results_lines = [f"- {result}" for result in entry.test_results]

    # Build scoring entry
    scoring_content = f"### {timestamp_str}\n"
    scoring_content += "\n".join(metrics_lines)
    if test_results_lines:
        scoring_content += "\n\n" + "\n".join(test_results_lines)

    marker = f"<!-- {phase_id} -->"

    # Check if SCORING section exists in this phase
    # Find phase content between last "# PHASE phase_id" and the marker
    phase_pattern = rf"(# PHASE {re.escape(phase_id)} at .+?\n)(.*?)({re.escape(marker)})"
    match = re.search(phase_pattern, markdown_content, re.DOTALL)

    if match:
        phase_intro = match.group(1)
        phase_body = match.group(2)
        marker_line = match.group(3)

        if "## SCORING" in phase_body:
            # SCORING section exists - insert before marker
            pattern = rf"(<!-- {re.escape(phase_id)} -->)"
            replacement = scoring_content + "\n\n\\1"
            updated = re.sub(pattern, replacement, markdown_content)
        else:
            # Create SCORING section
            scoring_section = f"## SCORING\n\n{scoring_content}"
            pattern = rf"(<!-- {re.escape(phase_id)} -->)"
            replacement = scoring_section + "\n\n\\1"
            updated = re.sub(pattern, replacement, markdown_content)
    else:
        # Phase not found - just append before marker
        updated = append_to_phase(markdown_content, phase_id, f"## SCORING\n\n{scoring_content}")

    return updated


def append_rollback_entry(
    markdown_content: str,
    target_phase_id: str,
    entry: RollbackEntry
) -> str:
    """
    Append a rollback entry to target phase.

    Args:
        markdown_content: Full .TASK.md content
        target_phase_id: Phase to add rollback entry to
        entry: RollbackEntry model

    Returns:
        Updated markdown content
    """
    timestamp_str = entry.timestamp.isoformat()

    # Format rollback entry
    rollback_content = f"### {timestamp_str} Back from {entry.from_phase}\n{entry.problem_description}"

    # Insert before phase marker
    return append_to_phase(markdown_content, target_phase_id, rollback_content)


def validate_document_structure(markdown_content: str) -> List[str]:
    """
    Validate .TASK.md structure and return list of errors.

    Args:
        markdown_content: Full .TASK.md content

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check for phase headers
    phase_pattern = r"^# PHASE\s+(\S+)\s+at\s+(.+)$"
    phase_matches = list(re.finditer(phase_pattern, markdown_content, re.MULTILINE))

    if not phase_matches:
        errors.append("No phase headers found")
        return errors

    # Check each phase has matching section marker
    for match in phase_matches:
        phase_name = match.group(1)
        timestamp_str = match.group(2)
        line_num = markdown_content[:match.start()].count("\n") + 1

        # Validate timestamp
        try:
            datetime.fromisoformat(timestamp_str)
        except ValueError:
            errors.append(f"Line {line_num}: Invalid RFC 3339 timestamp: {timestamp_str}")

        # Check for matching section marker
        marker = f"<!-- {phase_name} -->"
        if marker not in markdown_content:
            errors.append(f"Line {line_num}: Missing section marker: {marker}")

    return errors


def load_metrics(filepath: str) -> MetricsFile:
    """
    Load .metrics JSON file into MetricsFile model.

    Args:
        filepath: Path to .metrics file

    Returns:
        MetricsFile model

    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If JSON is invalid
    """
    path = Path(filepath)

    if not path.exists():
        return MetricsFile()  # Return empty metrics

    content = path.read_text(encoding="utf-8")
    data = json.loads(content)

    return MetricsFile(**data)


def save_metrics(filepath: str, metrics: MetricsFile) -> None:
    """
    Save MetricsFile model to .metrics JSON file.

    Args:
        filepath: Path to .metrics file
        metrics: MetricsFile model to save
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Use model_dump without exclude_none to include extra fields
    data = metrics.model_dump()

    # Remove None values to keep JSON clean
    data = {k: v for k, v in data.items() if v is not None}

    content = json.dumps(data, indent=2)
    path.write_text(content, encoding="utf-8")

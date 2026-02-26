"""
Pydantic models for task management system.

Defines the data structures used to parse and represent task documents,
phases, metrics, and rollback entries.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PhaseHeader(BaseModel):
    """Represents a phase header with name and timestamp."""
    phase_name: str = Field(..., description="Phase name (e.g., TASK_PLAN.DEFINE)")
    timestamp: datetime = Field(..., description="RFC 3339 timestamp")


class ScoringEntry(BaseModel):
    """Represents a metrics scoring entry with results."""
    timestamp: datetime = Field(..., description="RFC 3339 timestamp of scoring")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Technical metrics dict")
    test_results: Optional[List[str]] = Field(None, description="List of test result items")


class RollbackEntry(BaseModel):
    """Represents a rollback entry documenting an issue and revert."""
    from_phase: str = Field(..., description="Phase being rolled back from")
    timestamp: datetime = Field(..., description="RFC 3339 timestamp of rollback")
    issue_type: str = Field(..., description="Issue type: 'loop' or 'metrics_regression'")
    problem_description: str = Field(..., description="Description of the problem")


class Phase(BaseModel):
    """Represents a complete phase section with all its content."""
    header: PhaseHeader = Field(..., description="Phase header")
    content: str = Field(default="", description="Phase body content")
    scoring_entries: List[ScoringEntry] = Field(default_factory=list, description="Scoring entries in this phase")
    rollback_entries: List[RollbackEntry] = Field(default_factory=list, description="Rollback entries in this phase")


class TaskDocument(BaseModel):
    """Represents a complete task document (.TASK.md)."""
    phases: List[Phase] = Field(default_factory=list, description="All phases in document")
    current_phase: str = Field(..., description="Current phase name")
    created_at: datetime = Field(..., description="RFC 3339 timestamp of task creation")


class MetricsFile(BaseModel):
    """Represents metrics storage (.metrics JSON)."""
    TEST_PLAN: Optional[Dict[str, Any]] = Field(None, description="TEST_PLAN phase metrics")
    CODING: Optional[Dict[str, Any]] = Field(None, description="CODING phase metrics")
    TESTING: Optional[Dict[str, Any]] = Field(None, description="TESTING phase metrics")


# Phase workflow constant
PHASE_WORKFLOW = [
    "TASK_PLAN.DEFINE",
    "TASK_PLAN.REFINE_CONTEXT",
    "TASK_PLAN.DESIGN",
    "TASK_PLAN.DECOMPOSE",
    "EXEC_EVAL.TEST_PLAN",
    "EXEC_EVAL.CODING",
    "EXEC_EVAL.TESTING",
]


def get_next_phase(current_phase: str) -> str:
    """Get the next phase in the workflow."""
    try:
        current_index = PHASE_WORKFLOW.index(current_phase)
        if current_index >= len(PHASE_WORKFLOW) - 1:
            raise ValueError(f"No next phase after {current_phase}")
        return PHASE_WORKFLOW[current_index + 1]
    except ValueError as e:
        raise ValueError(f"Invalid phase: {current_phase}") from e


def get_previous_phase(current_phase: str) -> str:
    """Get the previous phase in the workflow."""
    try:
        current_index = PHASE_WORKFLOW.index(current_phase)
        if current_index <= 0:
            raise ValueError(f"No previous phase before {current_phase}")
        return PHASE_WORKFLOW[current_index - 1]
    except ValueError as e:
        raise ValueError(f"Invalid phase: {current_phase}") from e

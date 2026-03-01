#!/usr/bin/env python3
"""
Helper functions for generating JSON Patch operations on task documents.

Provides high-level functions to create patches for common task operations:
- Advancing phases
- Adding scoring entries
- Adding rollback entries
- Loading/saving metrics

These functions generate RFC 6902 JSON Patch operations that can be applied
via apply_json_patch.py.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from .task_model import ScoringEntry, RollbackEntry, PHASE_WORKFLOW


def patch_advance_phase(current_phase: str) -> List[Dict[str, Any]]:
    """
    Generate JSON Patch to advance task to next phase.

    Creates a new phase section in the phases children dict and updates
    the task metadata.current_phase to the next phase.

    Args:
        current_phase: Current phase name (e.g., "TASK_PLAN.DEFINE")

    Returns:
        List of JSON Patch operations (RFC 6902)

    Raises:
        ValueError: If current_phase is not valid or is the final phase
    """
    if current_phase not in PHASE_WORKFLOW:
        raise ValueError(f"Invalid phase: {current_phase}")

    current_idx = PHASE_WORKFLOW.index(current_phase)
    if current_idx >= len(PHASE_WORKFLOW) - 1:
        raise ValueError(f"No next phase after {current_phase}")

    next_phase = PHASE_WORKFLOW[current_idx + 1]
    now = datetime.now().isoformat()

    # Convert phase name to display label
    phase_label = next_phase.replace(".", " - ").replace("_", " ")

    operations = [
        # Create new phase entry in phases/children
        {
            "op": "add",
            "path": f"/children/phases/children/{next_phase}",
            "value": {
                "id": next_phase,
                "label": phase_label,
                "type": "Doc",
                "metadata": {
                    "timestamp": now,
                    "content": ""
                },
                "children": {
                    "scoring": {
                        "id": "scoring",
                        "label": "Scoring",
                        "type": "Doc",
                        "children": {}
                    },
                    "rollbacks": {
                        "id": "rollbacks",
                        "label": "Rollbacks",
                        "type": "Doc",
                        "children": {}
                    }
                }
            }
        },
        # Update current_phase in metadata
        {
            "op": "replace",
            "path": "/metadata/current_phase",
            "value": next_phase
        }
    ]

    return operations


def patch_add_scoring_entry(
    phase_name: str,
    entry: ScoringEntry
) -> List[Dict[str, Any]]:
    """
    Generate JSON Patch to add a scoring entry to a phase.

    Args:
        phase_name: Phase to add scoring to (e.g., "EXEC_EVAL.TEST_PLAN")
        entry: ScoringEntry with metrics and test results

    Returns:
        List of JSON Patch operations
    """
    timestamp_str = entry.timestamp.isoformat()
    entry_id = f"entry_{timestamp_str.replace(':', '-').replace('.', '_')}"

    metadata = {
        "timestamp": timestamp_str,
        "metrics": entry.metrics,
    }

    if entry.test_results:
        metadata["test_results"] = entry.test_results

    if entry.coverage:
        metadata["coverage"] = entry.coverage

    if entry.coverage_summary:
        metadata["coverage_summary"] = entry.coverage_summary

    return [
        {
            "op": "add",
            "path": f"/children/phases/children/{phase_name}/children/scoring/children/{entry_id}",
            "value": {
                "id": entry_id,
                "label": timestamp_str,
                "type": "Doc",
                "metadata": metadata
            }
        }
    ]


def patch_add_rollback_entry(
    phase_name: str,
    entry: RollbackEntry
) -> List[Dict[str, Any]]:
    """
    Generate JSON Patch to add a rollback entry to a phase.

    Args:
        phase_name: Target phase to add rollback to
        entry: RollbackEntry with issue type and description

    Returns:
        List of JSON Patch operations
    """
    timestamp_str = entry.timestamp.isoformat()
    entry_id = f"rollback_{timestamp_str.replace(':', '-').replace('.', '_')}"

    return [
        {
            "op": "add",
            "path": f"/children/phases/children/{phase_name}/children/rollbacks/children/{entry_id}",
            "value": {
                "id": entry_id,
                "label": f"{timestamp_str} Back from {entry.from_phase}",
                "type": "Doc",
                "metadata": {
                    "timestamp": timestamp_str,
                    "from_phase": entry.from_phase,
                    "issue_type": entry.issue_type,
                    "problem_description": entry.problem_description
                }
            }
        }
    ]


def patch_update_phase_content(
    phase_name: str,
    content: str
) -> List[Dict[str, Any]]:
    """
    Generate JSON Patch to update phase content.

    Args:
        phase_name: Phase to update
        content: New content to set

    Returns:
        List of JSON Patch operations
    """
    return [
        {
            "op": "replace",
            "path": f"/children/phases/children/{phase_name}/metadata/content",
            "value": content
        }
    ]


def create_initial_task_doc(task_id: str = "task_001") -> Dict[str, Any]:
    """
    Create initial task document structure (for use with task_create).

    Args:
        task_id: Task identifier

    Returns:
        Doc model dict with initial structure ready for JSON serialization
    """
    now = datetime.now().isoformat()
    initial_phase = PHASE_WORKFLOW[0]
    phase_label = initial_phase.replace(".", " - ").replace("_", " ")

    return {
        "id": task_id,
        "label": "Task",
        "type": "Doc",
        "metadata": {
            "description": "Task execution tracking",
            "created_at": now,
            "current_phase": initial_phase
        },
        "children": {
            "phases": {
                "id": "phases",
                "label": "Phases",
                "type": "Doc",
                "children": {
                    initial_phase: {
                        "id": initial_phase,
                        "label": phase_label,
                        "type": "Doc",
                        "metadata": {
                            "timestamp": now,
                            "content": "Task initialized. Ready for planning and development."
                        },
                        "children": {
                            "scoring": {
                                "id": "scoring",
                                "label": "Scoring",
                                "type": "Doc",
                                "children": {}
                            },
                            "rollbacks": {
                                "id": "rollbacks",
                                "label": "Rollbacks",
                                "type": "Doc",
                                "children": {}
                            }
                        }
                    }
                }
            }
        }
    }

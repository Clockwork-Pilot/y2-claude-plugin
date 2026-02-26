# Implementation Plan: Task Management System

**Branch**: `001-add-task-management` | **Date**: 2026-02-26 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-add-task-management/spec.md`

## Summary

Implement a Python-based task management system that tracks task lifecycle through markdown documents (.TASK.md) with phase-based workflow (TASK_PLAN → EXEC_EVAL), supporting create/load/update operations with document structure integrity guarantees. Five scripts handle core operations: task_create.py (initialize), task_roll.py (advance phase), task_metrics.py (collect metrics), task_roll_back.py (revert phase), task_to_history.py (archive). Metrics stored in separate `.metrics` JSON file for programmatic comparison; markdown documents for human-readable documentation. File write operations use exclusive mode (O_EXCL) to prevent concurrent corruption.

## Technical Context

**Language/Version**: Python 3.10+ (uses pathlib, dataclasses, datetime.isoformat for RFC 3339)
**Primary Dependencies**: Python stdlib (datetime, json, pathlib, re, argparse); no external packages required
**Storage**: File-based (Markdown .TASK.md + JSON .metrics file in same directory as task)
**Testing**: pytest with test isolation via TEST_LOG environment variable
**Target Platform**: Unix/Linux/macOS (uses fcntl for file locking; Windows alternative with msvcrt not in initial scope)
**Project Type**: CLI utility library (five standalone scripts + shared task_state.py module)
**Performance Goals**: Phase advancement <100ms (SC-002); document parsing <50ms for 100KB files
**Constraints**: Maximum document size ~100KB (SC-006); exclusive file mode (O_EXCL) for concurrent write detection; no external APIs or databases
**Scale/Scope**: Single-task workflow; supports 10+ phases, 50+ rollback/scoring entries per document; no multi-user coordination beyond fail-fast

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I (Handler Modularity)**: ✅ PASS — Task management is a separate utility (not a Claude Code handler). If integrated as handlers later, each script will become a dedicated handler module with no cross-script imports. Currently compliant as standalone scripts.

**Principle II (Non-Interference)**: ✅ PASS — All scripts will exit with code 0 on success or controlled error codes. Error handling will not crash calling processes. No blocking I/O beyond file operations.

**Principle III (Centralized Configuration)**: ✅ PASS — Task management will use pathlib.Path for all paths. If integrated into plugin architecture, all file paths will be centralized in config.py. Currently, paths are relative to script execution location.

**Principle IV (Structured Observability)**: ✅ PASS — Task management system is accessible to handlers via `/hooks/common.py`. All handlers log "task" context (task name, current phase) using hook_logging.py and JSON serialization. Task document loading is part of handler observability pattern. Tests isolate output via TEST_LOG environment variable.

**Principle V (Simplicity)**: ✅ PASS — Five focused scripts, each with single responsibility. No premature abstractions. Shared task_state.py module contains only essential parsing/writing logic.

**Gate Status**: ✅ **PASSED** — Feature design aligns with constitution principles. No violations requiring justification.

## Integration with Claude Code Plugin Hooks

The task management system integrates with the existing hook infrastructure via `/hooks/common.py`, enabling all handlers to:
- Load current task document (.TASK.md in execution directory)
- Log task name with every handler invocation (adds "task" key to log structure)
- Access task context (current phase, metrics, prior rollbacks)

This provides **observability** (Principle IV) of which task each handler is executing within, without violating **handler modularity** (Principle I) — `/hooks/common.py` is a shared utility, not a handler, and each handler remains independently testable.

**Design Decision**: Task loading is optional (returns None if no .TASK.md), so handlers work with or without task context. Aligns with **non-interference** (Principle II) — handler execution unaffected if task document missing.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-add-task-management/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command) - CLI contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

**Structure Decision**: CLI utility library with TDD-first approach, integrated with hook handlers. Tests directory mirrors implementation structure for clarity.

```text
hooks/
├── common.py            # NEW: Task document loading + task context helper (used by all handlers)
├── [existing handlers]  # Updated to use common.py for task loading and logging
└── tests/
    └── test_common.py   # Unit tests for task loading in hook context

tasks_scripts/
├── __init__.py
├── models.py            # Pydantic models (PhaseHeader, ScoringEntry, RollbackEntry, Phase, TaskDocument, MetricsFile)
├── task_state.py        # Shared: task document parsing, writing, validation (uses models.py)
├── task_create.py       # Script: Initialize .TASK.md
├── task_roll.py         # Script: Advance phase
├── task_metrics.py      # Script: Collect and record metrics
├── task_roll_back.py    # Script: Revert to previous phase
├── task_to_history.py   # Script: Archive completed tasks
└── tests/
    ├── __init__.py
    ├── conftest.py      # Shared fixtures (temp directories, sample .TASK.md files, Pydantic factory functions)
    ├── test_parsing.py          # Parser validation: document → Pydantic models (8+ tests)
    ├── test_task_state.py       # Unit tests for task_state.py (parsing, writing, validation with Pydantic assertions)
    ├── test_task_create.py      # Unit tests for task_create.py
    ├── test_task_roll.py        # Unit tests for task_roll.py
    ├── test_task_metrics.py     # Unit tests for task_metrics.py (including test result lists)
    ├── test_task_roll_back.py   # Unit tests for task_roll_back.py
    ├── test_task_to_history.py  # Unit tests for task_to_history.py
    ├── fixtures/                # Sample .TASK.md files for testing
    │   ├── valid_single_phase.md
    │   ├── valid_multi_phase_with_scoring.md
    │   ├── valid_exec_eval_with_test_lists.md  # EXEC_EVAL phases with test result lists
    │   ├── corrupted_missing_header.md
    │   ├── corrupted_invalid_timestamp.md
    │   └── corrupted_malformed_sections.md
    └── integration/
        └── test_task_workflow.py # Full workflow integration tests
```

**TDD Approach**: Tests are written FIRST (Phase 1), confirmed to fail, then implementation code is written. Scoring gradually increases as tests pass.

## Complexity Tracking

No violations to justify. Constitution Check passed without issues.

---

## Phase 0: Research & Unknowns Resolution

**Status**: ✅ COMPLETE — No critical unknowns remain. All technical details clarified in specification and clarifications session.

**Resolved areas**:
- Task ID generation: Auto-increment (regular) + GitHub ID (issue-based)
- Concurrent write handling: Fail-fast with O_EXCL
- Rollback target: Parameter or previous phase default
- Loop detection: Manual (external logic)
- Metrics architecture: Separate .metrics JSON + SCORING markdown documentation

**Research output**: No research.md needed; specification provides sufficient technical clarity.

---

## Phase 1: Design & Test-First Implementation

### 1.1 Data Model (data-model.md)

**Entities**:

| Entity | Fields | Relationships |
|--------|--------|---------------|
| Task Document (.TASK.md) | phase, timestamps, sections, content | Contains phase headers, SCORING entries, rollback entries |
| Phase Header | phase_name, timestamp (RFC 3339) | Identifies current phase and transition time |
| SCORING Entry | timestamp, metrics_json | Appended to phase section; sourced from .metrics |
| Rollback Entry | from_phase, issue_type, start_time, rollback_time | Nested under target phase header |
| Metrics File (.metrics) | TEST_PLAN: {...}, CODING: {...}, TESTING: {...} | External JSON file; parallel to .TASK.md |
| Task Archive | task_id (auto-inc or GitHub), name, status (success/failure) | Stored in .tasks_history/; contains archived .TASK.md files |

### 1.2 Internal Data Structures (Pydantic Models)

All parsed document sections are represented as Pydantic models for type safety and validation:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PhaseHeader(BaseModel):
    phase_name: str  # e.g., "TASK_PLAN.DEFINE"
    timestamp: datetime  # RFC 3339

class ScoringEntry(BaseModel):
    timestamp: datetime
    metrics: dict  # e.g., {"coverage": 85, "tests_passed": 42}
    test_results: Optional[List[str]] = None  # List of test result items

class RollbackEntry(BaseModel):
    from_phase: str
    timestamp: datetime
    issue_type: str  # "loop" or "metrics_regression"
    problem_description: str

class Phase(BaseModel):
    header: PhaseHeader
    content: str
    scoring_entries: List[ScoringEntry] = Field(default_factory=list)
    rollback_entries: List[RollbackEntry] = Field(default_factory=list)

class TaskDocument(BaseModel):
    phases: List[Phase]
    current_phase: str
    created_at: datetime

class MetricsFile(BaseModel):
    TEST_PLAN: Optional[dict] = None
    CODING: Optional[dict] = None
    TESTING: Optional[dict] = None
```

**Example with test lists in EXEC_EVAL**:
```markdown
# PHASE EXEC_EVAL.TEST_PLAN at 2026-02-26T10:00:00Z

## SCORING

### 2026-02-26T11:00:00Z
Coverage: 85%
Tests: 42 passed, 3 failed
- test_task_create_valid_task
- test_task_roll_basic_phase
- test_task_roll_invalid_sequence (FAILED)

<!-- EXEC_EVAL.TEST_PLAN -->
```

Parses to:
```python
ScoringEntry(
    timestamp=datetime(...),
    metrics={"coverage": 85, "tests_passed": 42, "tests_failed": 3},
    test_results=["test_task_create_valid_task", "test_task_roll_basic_phase", "test_task_roll_invalid_sequence (FAILED)"]
)
```

### 1.3 Task State Module (task_state.py)

**Section Marker Convention**:
Every phase section ends with an HTML comment marker containing the phase ID:
```
<!-- {PHASE_ID} -->
```

This enables atomic regex-based updates: `re.sub(rf'(<!-- {phase_id} -->)', f'{content}\n\1', doc)`

**Core responsibilities**:
- **Parse**: Load .TASK.md → Pydantic TaskDocument (regex extraction + validation)
- **Validate**: Detect malformed headers, missing/duplicate markers, invalid phase sequences
- **Write**: Append content/rollbacks/scoring via atomic regex before section markers
- **Serialize**: Convert Pydantic models back to markdown format
- **Metrics I/O**: Load/save .metrics JSON as MetricsFile Pydantic model

**Key methods**:
```python
def load_task_document(filepath: str) -> TaskDocument:
    """Parse .TASK.md into Pydantic TaskDocument"""

def parse_phase_section(markdown_text: str) -> Phase:
    """Extract phase header, content, scoring, rollbacks as Phase model"""

def append_to_phase(doc: TaskDocument, phase_id: str, content: str) -> str:
    """Update markdown: insert content before phase marker (atomic regex)"""

def append_scoring(doc: TaskDocument, phase_id: str, entry: ScoringEntry) -> str:
    """Append SCORING entry before phase end marker"""

def load_metrics(filepath: str) -> MetricsFile:
    """Load .metrics JSON as Pydantic MetricsFile"""
```

### 1.3 Scripts (5 CLI modules)

Each script:
- Single entry point function
- Uses task_state.py for document operations
- Handles errors gracefully (exit 0 on success, 1 on error)
- Provides clear error messages to user

**Scripts**:
1. **task_create.py** — Initialize new .TASK.md
2. **task_roll.py** — Advance to next phase
3. **task_metrics.py** — Collect and record metrics
4. **task_roll_back.py** — Revert to previous phase
5. **task_to_history.py** — Archive completed tasks

### 1.4 Test Suite (TDD-First)

**Phase 1 Priority: WRITE TESTS BEFORE IMPLEMENTATION**

**Dependencies**: Add `pydantic` to test requirements

Test structure by responsibility:

**0. test_parsing.py** (Core parser validation - validates Pydantic models)
   - Test parse phase header → PhaseHeader model
   - Test parse SCORING section → List[ScoringEntry] with metrics dict
   - Test parse test results list → ScoringEntry.test_results (List[str])
   - Test parse rollback entry → RollbackEntry model
   - Test full document parse → TaskDocument model
   - Test parse invalid timestamps → Pydantic validation error
   - Test parse malformed metrics JSON → Pydantic validation error
   - Test roundtrip: markdown → TaskDocument → markdown (content unchanged)
   - Test metrics parsing → MetricsFile model with TEST_PLAN, CODING, TESTING

1. **test_task_state.py** (core parsing/writing logic with Pydantic assertions)
   - Test load_task_document() returns valid TaskDocument model
   - Test TaskDocument.phases list populated correctly for multi-phase documents
   - Test Phase.header contains correct phase_name and timestamp
   - Test Phase.scoring_entries parsed as List[ScoringEntry]
   - Test Phase.rollback_entries parsed as List[RollbackEntry]
   - Test ScoringEntry.test_results properly extracted as List[str]
   - Test load corrupted (missing header) → Pydantic validation error
   - Test load corrupted (invalid timestamp) → Pydantic validation error
   - Test load corrupted (missing section markers) → error detection
   - Test append_to_phase() preserves TaskDocument model validity
   - Test append_scoring() creates valid ScoringEntry with metrics dict
   - Test round-trip: TaskDocument → markdown → TaskDocument (equivalence)

2. **test_task_create.py**
   - Test create new .TASK.md with TASK_PLAN.DEFINE header
   - Test RFC 3339 timestamp format
   - Test file created in correct location
   - Test error if .TASK.md already exists

3. **test_task_roll.py**
   - Test phase advancement workflow (all 7 phases)
   - Test header updated with new timestamp
   - Test all prior content preserved
   - Test chronological order of phases

4. **test_task_metrics.py**
   - Test collect metrics and store in .metrics JSON
   - Test .metrics structure (TEST_PLAN, CODING, TESTING)
   - Test append SCORING section to .TASK.md
   - Test multiple SCORING entries timestamped and distinguishable

5. **test_task_roll_back.py**
   - Test rollback to specified phase
   - Test rollback to previous phase (when not specified)
   - Test rollback entry added with problem description and timing
   - Test newer phase data preserved

6. **test_task_to_history.py**
   - Test move to .tasks_history/ with auto-incremented ID
   - Test GitHub issue ID for GitHub-based tasks
   - Test __FAILURE__ prefix for failed tasks
   - Test directory created if missing

7. **test_task_workflow.py** (integration)
   - Full workflow: create → roll → metrics → roll → metrics → roll → history
   - Large document (10+ phases, 50+ entries) handling

8. **hooks/tests/test_common.py** (hook integration)
   - Test load_task_document() finds .TASK.md in current directory
   - Test load_task_document() searches parent directories
   - Test load_task_document() returns None if no .TASK.md found
   - Test load_task_document() returns valid TaskDocument model
   - Test get_task_context() extracts correct task metadata
   - Test get_task_context() returns None when task_doc is None
   - Test handler logging pattern includes "task" key with context
   - Test handler graceful error handling when task loading fails

### 1.5 Contracts (CLI interfaces)

**contracts/task-create.md**
```
Command: task_create.py [description]
Output: .TASK.md file created
Error: Exit 1 if file exists
```

**contracts/task-roll.md**
```
Command: task_roll.py
Output: Phase advanced; new header added with timestamp
Error: Exit 1 if not valid phase sequence
```

**contracts/task-metrics.md**
```
Command: task_metrics.py [--metrics-json '...']
Output: .metrics updated; SCORING appended to .TASK.md
Error: Exit 1 if JSON invalid
```

**contracts/task-roll-back.md**
```
Command: task_roll_back.py [--target PHASE] [--reason "..."]
Output: Reverted to target phase; rollback entry added
Error: Exit 1 if concurrent write (O_EXCL); Exit 1 if invalid phase
```

**contracts/task-to-history.md**
```
Command: task_to_history.py [--task-id 00001] [--is-github-issue] [--failure]
Output: .TASK.md moved to .tasks_history/ with standardized name
Error: Exit 1 if archival fails
```

### 1.6 Hook Handler Integration (hooks/common.py)

**New Module**: `/hooks/common.py` — Task management utilities for all handlers

**Responsibilities**:
- Load current .TASK.md from execution directory (or parent directories)
- Return TaskDocument Pydantic model or None if no task found
- Add task context to logging structure

**Key functions**:
```python
def load_task_document(start_dir: Optional[str] = None) -> Optional[TaskDocument]:
    """
    Search for .TASK.md in start_dir, then parent directories up to repo root.
    Returns TaskDocument model if found and valid, None otherwise.
    """

def get_task_context(task_doc: Optional[TaskDocument]) -> Optional[dict]:
    """
    Extract task metadata for logging.
    Returns: {"task_name": str, "current_phase": str, "created_at": str} or None
    """
```

**Handler Integration Pattern**:
Every handler adopts this pattern:
```python
from hooks.common import load_task_document, get_task_context
from hook_logging import setup_logger, serialize_log_data

logger = setup_logger(__name__)

def handler_main():
    # Load task context
    task_doc = load_task_document()
    task_context = get_task_context(task_doc)  # May be None if no task

    # Perform handler work
    try:
        result = do_work()

        # Log with task key
        log_data = {
            "status": "success",
            "task": task_context,  # NEW: Task name/phase logged
            "result": result
        }
        logger.info(serialize_log_data(log_data))
        return 0
    except Exception as e:
        log_data = {
            "status": "error",
            "task": task_context,
            "error": str(e)
        }
        logger.error(serialize_log_data(log_data))
        return 1
```

**Logging Output Example**:
```json
{"status": "success", "task": {"task_name": "TASK_PLAN.DEFINE", "current_phase": "TASK_PLAN.REFINE_CONTEXT", "created_at": "2026-02-26T10:00:00Z"}, "result": "..."}
```

### 1.7 Quickstart (quickstart.md)

Minimal example workflow demonstrating all five scripts and hook integration.

**Output Generation**:
- data-model.md (created)
- contracts/ (5 contract files created)
- quickstart.md (created)
- **tests/** (created with full TDD test suite)
- **hooks/common.py** (created with task loading utilities)
- **hooks/tests/test_common.py** (created with hook integration tests)

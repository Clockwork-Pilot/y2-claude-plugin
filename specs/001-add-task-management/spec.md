# Feature Specification: Task Management System

**Feature Branch**: `001-add-task-management`
**Created**: 2026-02-26
**Status**: Draft
**Input**: User description: "Add task management support. Create, update, load task stored in TASK.md. Support tracking task state. Support making correct task document updates, including those in the middle of document. We assume document has stable structure and barely editing by human."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently

  For task lifecycle management we use scripts in tasks_scripts/ dir.
-->

### User Story 1 - Create and Initialize a Task (Priority: P1)

A user initializes a new task management document to begin tracking task execution. For task creation user uses tasks_script/task_create.py script.  It creates a .TASK.md file with the proper initial structure, setting the phase to TASK_PLAN.DEFINE and recording a timestamp.

**Why this priority**: This is the foundational capability. Without being able to create a task document, no other functionality is possible.

**Independent Test**: Can create a .TASK.md file with correct initial structure and verify the phase header and timestamp are present.

**Acceptance Scenarios**:

1. **Given** no task document exists, **When** creating a new task with a description, **Then** .TASK.md is created with "# PHASE TASK_PLAN.DEFINE at [RFC 3339 timestamp]" as the header
2. **Given** a task is initialized, **When** inspecting the file, **Then** the document structure is valid markdown with proper phase header format

---

### User Story 2 - Progress Task Through Phases (Priority: P1)

A user advances a task from one phase to the next in the predefined workflow (TASK_PLAN.DEFINE → REFINE_CONTEXT → DESIGN → DECOMPOSE → EXEC_EVAL.TEST_PLAN → CODING → TESTING). Script tasks_scripts/task_roll.py used for updating the phase header with a new timestamp, preserving all prior content.

**Why this priority**: Phase progression is the core workflow. Users must be able to move tasks forward through execution stages.

**Independent Test**: Can advance a task from one phase to the next, verify the phase header is updated, and all previous content is preserved.

**Acceptance Scenarios**:

1. **Given** a task is in TASK_PLAN.DEFINE, **When** advancing to REFINE_CONTEXT, **Then** the phase header updates to "# PHASE TASK_PLAN.REFINE_CONTEXT at [new RFC 3339 timestamp]" and prior content remains
2. **Given** multiple phases have been completed, **When** viewing the document, **Then** all phase transitions are recorded in chronological order
3. **Given** a task progresses to EXEC_EVAL.TEST_PLAN, **When** advancing, **Then** the phase header reflects "# PHASE EXEC_EVAL.TEST_PLAN at [timestamp]"

---

### User Story 3 - Collect and Record Evaluation Metrics (Priority: P2)

A user executes task_metrics.py script to collect code quality and evaluation metrics at EXEC_EVAL phases. The system gathers technical metrics, updates the task document with the assessment, and records results under a SCORING subsection with RFC 3339 timestamp.

**Why this priority**: Metrics collection enables objective measurement of progress and code quality. It's essential for EXEC_EVAL phases but not required for initial task planning.

**Independent Test**: Can run task_metrics.py at an EXEC_EVAL phase, collect metrics, and append them to the document under a SCORING subsection with proper timestamp.

**Acceptance Scenarios**:

1. **Given** a task is in EXEC_EVAL.TEST_PLAN, **When** executing task_metrics.py, **Then** a "### SCORING" subsection with RFC 3339 timestamp is added containing technical metrics (coverage, test results, progression/regression indicators)
2. **Given** task_metrics.py is executed, **When** the operation completes, **Then** the task document includes technical report content under the SCORING section
3. **Given** multiple metric collections occur, **When** viewing the document, **Then** each SCORING subsection is timestamped and distinguishable

---

### User Story 4 - Rollback to Previous Phase with Issue Tracking (Priority: P1)

When a loop is detected (repeated attempts without progress) or metrics show no improvement, the user executes task_roll_back.py to revert to a previous phase. The system adds a rollback header to the target phase section documenting the issue (loop or no metrics improvement), timing when issue started, and current timestamp, while preserving all data from newer phases.

**Why this priority**: Rollback is critical for error recovery and preventing infinite loops. Teams must be able to safely go back and retry with different approach without losing prior work.

**Independent Test**: Can rollback from a later phase to an earlier one via task_roll_back.py, verify rollback entry is added to target phase with proper documentation, and all newer phase data is preserved.

**Acceptance Scenarios**:

1. **Given** a task is in EXEC_EVAL.TESTING with no metric improvements, **When** executing task_roll_back.py to revert to EXEC_EVAL.CODING, **Then** a "### [RFC 3339 timestamp] Back from TESTING" header is added to the CODING section with problem description (loop detected or metrics not improved)
2. **Given** a rollback occurs, **When** inspecting the document, **Then** the rollback header includes issue type, timing information (when started, when backed), and relevant log file reference
3. **Given** rollback is executed, **When** viewing phases after the rollback point, **Then** newer phase content remains accessible and unmodified in the document

---

### User Story 5 - Load and Parse Existing Task Document (Priority: P1)

A user loads an existing task document from .TASK.md to resume work. The system parses the document, extracts the current phase, validates the structure, and makes the content available for updates.

**Why this priority**: Users must be able to resume work on existing tasks. Loading is fundamental to the system's operability.

**Independent Test**: Can load a .TASK.md file, extract the current phase header, verify document validity, and confirm all content is accessible.

**Acceptance Scenarios**:

1. **Given** a .TASK.md file exists with multiple phases, **When** loading the document, **Then** the system correctly identifies the current phase from the header
2. **Given** a task document is loaded, **When** inspecting the structure, **Then** no parsing errors occur and all sections are intact
3. **Given** a corrupted or malformed document, **When** attempting to load, **Then** the system identifies structural issues and reports them clearly

---

### User Story 6 - Update Task Document with Mid-Document Edits (Priority: P1)

A user appends new content to the current phase section without disrupting earlier phases or the document structure. The system ensures updates are inserted at the correct location (end of current phase section) even when the document has grown with multiple phases and content.

**Why this priority**: Stable document updates are essential for multi-phase documents. Users must be confident that edits won't corrupt the structure.

**Independent Test**: Can add content to the current phase section multiple times, verify each addition appears in the correct location, and earlier sections remain unchanged.

**Acceptance Scenarios**:

1. **Given** a task has multiple phase sections, **When** adding content to the current phase, **Then** the new content is appended to the correct phase section without affecting other phases
2. **Given** content is added multiple times to the same phase, **When** loading the document, **Then** all additions appear in chronological order within that phase
3. **Given** a large document with many phases, **When** appending to the current phase, **Then** the operation completes without modifying earlier or later phase sections

---

### User Story 7 - Archive Completed Tasks with Naming Convention (Priority: P2)

When a task is completed (success or failure), the user moves the task file to .tasks_history/ with a standardized naming convention. Successful tasks use format TASK_#####_DESCRIPTION or GITHUB_ISSUE_#####_DESCRIPTION. Failed tasks include __FAILURE__ in the name.

**Why this priority**: Task archival and naming provides historical tracking and clear status indication. Important for long-term project management but not required for initial task execution.

**Independent Test**: Can archive a completed task to .tasks_history/ with correct naming convention and verify the file is properly removed from active task directory.

**Acceptance Scenarios**:

1. **Given** a task completes successfully, **When** archiving it, **Then** the file is moved to .tasks_history/ with name format "TASK_00001_TASK_DESCRIPTION_IN_UPPER_CASE"
2. **Given** a GitHub issue-based task is completed, **When** archiving, **Then** the name uses format "GITHUB_ISSUE_345345_DESCRIPTION_IN_UPPER_CASE"
3. **Given** a task fails, **When** archiving, **Then** the filename includes "__FAILURE__" immediately after the task ID (e.g., "TASK_00001__FAILURE__DESCRIPTION")

### Edge Cases

- What happens when a .TASK.md file is manually edited by a human and the structure becomes inconsistent (missing phase headers, extra line breaks)?
- How does the system detect and handle a loop condition (repeated phase transitions without progress)?
- How should metrics comparison work when previous metrics don't exist or are incomplete?
- What occurs if task_roll_back.py is executed but the target phase has no prior SCORING data to compare against?
- How does the system handle very large task documents with many phases and extensive SCORING/rollback history?
- What happens if .tasks_history/ directory doesn't exist when archiving via task_to_history.py?
- How should the system behave if multiple SCORING sections exist in the same phase for comparison purposes?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: task_create.py MUST create a new .TASK.md file with initial phase "# PHASE TASK_PLAN.DEFINE at [RFC 3339 timestamp]"
- **FR-002**: task_roll.py MUST advance the task to the next phase in workflow, updating the phase header with new timestamp while preserving all prior content
- **FR-003**: task_metrics.py MUST collect code quality metrics at EXEC_EVAL phases, store them in `.metrics` JSON file (structure: `{ "TEST_PLAN": {...}, "CODING": {...}, "TESTING": {...} }`), and append human-readable summary under "### SCORING" subsection in .TASK.md with RFC 3339 timestamp
- **FR-004**: task_roll_back.py MUST revert to specified phase (or previous phase if not specified) when user explicitly invokes it, adding rollback header documenting issue and timing; fail-fast on concurrent write attempts using exclusive file mode
- **FR-005**: task_state.py MUST read and parse .TASK.md, extract current phase, validate structure, support updates to document, and provide metrics data for external comparison logic
- **FR-006**: task_to_history.py MUST move completed task from .TASK.md to .tasks_history/ directory with auto-incremented task ID (TASK_#####) for non-GitHub tasks, or GitHub issue ID (GITHUB_ISSUE_#####) for GitHub-based tasks
- **FR-007**: System MUST maintain document structure integrity during all updates, ensuring content is appended to correct phase section without disrupting other phases
- **FR-008**: System MUST validate document structure on load and report specific structural issues (missing headers, malformed sections)
- **FR-009**: System MUST support phase advancement workflow: TASK_PLAN.DEFINE → REFINE_CONTEXT → DESIGN → DECOMPOSE → EXEC_EVAL.TEST_PLAN → CODING → TESTING
- **FR-010**: System MUST archive successful tasks with auto-incremented naming for regular tasks (TASK_#####_DESCRIPTION) or GitHub issue ID for GitHub-based tasks (GITHUB_ISSUE_#####_DESCRIPTION), where ##### is zero-padded 5-digit ID
- **FR-011**: System MUST archive failed tasks with "__FAILURE__" immediately after task ID in filename (e.g., TASK_00001__FAILURE__DESCRIPTION)
- **FR-012**: Rollback header MUST include problem description, timing information (when issue detected, when rollback occurred), and reference to relevant logs
- **FR-013**: File write operations MUST use exclusive file mode (O_EXCL) to detect concurrent writes; if concurrent write detected, operation fails with clear error message
- **FR-014**: Metrics storage MUST maintain `.metrics` JSON file with structure `{ "TEST_PLAN": { metrics }, "CODING": { metrics }, "TESTING": { metrics } }` for programmatic phase-to-phase comparison

### Key Entities

Document structure uses gradually increasing markdown heading levels (starting at # for top-level, then ##, ###, etc. for nested content).

- **Task Document (.TASK.md)**: Markdown file tracking a single task's execution lifecycle through phases, containing phase headers, timestamps, content sections, human-readable SCORING summaries, and rollback history
- **Metrics File (.metrics)**: JSON file storing structured metrics for all EXEC_EVAL phases with structure `{ "TEST_PLAN": {...}, "CODING": {...}, "TESTING": {...} }`, used for programmatic comparison and phase progression decisions
- **Phase Header**: Top-level section header "# PHASE [PHASE_NAME] at [RFC 3339 timestamp]" identifying current execution stage and transition time
- **SCORING Section**: Nested header under phase section for grouping human-readable metric summaries, containing timestamped entries as further nested headers (sourced from .metrics file)
- **Rollback Entry**: Nested header under target phase section "Back from [PHASE_NAME]" documenting issue, timing when detected, and rollback timestamp
- **Task History Archive (.tasks_history/)**: Directory containing completed/archived tasks with standardized naming (TASK_#####_NAME or GITHUB_ISSUE_#####_NAME, with optional __FAILURE__ prefix)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System correctly creates new .TASK.md files 100% of the time with valid initial phase header and timestamp
- **SC-002**: Phase advancement operations complete in under 100ms and preserve all prior document content without data loss
- **SC-003**: System correctly loads and parses 100% of well-formed .TASK.md files without parsing errors or data loss
- **SC-004**: Mid-document content appends maintain document integrity: no content corruption or misplaced sections in documents with 10+ phases and 50+ rollback/scoring entries
- **SC-005**: Rollback operations complete successfully, add rollback entry to correct target phase 100% of the time, and preserve newer phase data
- **SC-006**: Metric collection (task_metrics.py) produces consistent, reproducible metrics stored in `.metrics` JSON file with all expected fields across all three EXEC_EVAL phases
- **SC-007**: Task archival naming follows convention 100% of the time with auto-incremented IDs for regular tasks (TASK_#####), GitHub issue IDs for GitHub-based tasks, correct case handling, and __FAILURE__ placement
- **SC-008**: System detects structural issues in malformed .TASK.md files and reports them with specific location information (line number, issue type)
- **SC-009**: All five scripts (task_create.py, task_state.py, task_roll.py, task_roll_back.py, task_to_history.py) execute with zero unhandled errors on valid inputs
- **SC-010**: Concurrent write attempts to .TASK.md fail gracefully with clear error message; exclusive file mode prevents data corruption
- **SC-011**: `.metrics` JSON file maintains phase-to-phase metric history for programmatic comparison; structure supports TEST_PLAN, CODING, and TESTING metrics simultaneously

## Clarifications

### Session 2026-02-26

- Q: Task ID generation for archival? → A: Auto-increment for regular tasks (Option A); external ID from GitHub for GitHub issue-based tasks (Option E)
- Q: Concurrent edit handling? → A: Fail-fast with exclusive file mode (Option B with O_EXCL)
- Q: Rollback target phase? → A: Support both parameter-specified phase (Option A) and default to previous phase (Option B) when parameter omitted
- Q: Loop detection? → A: Manual only; user explicitly invokes task_roll_back.py when loop/issue detected
- Q: Metrics structure? → A: Separate `.metrics` JSON file with structure `{ "TEST_PLAN": {...}, "CODING": {...}, "TESTING": {...} }` for programmatic comparison; SCORING sections in .TASK.md for documentation

## Assumptions

1. .TASK.md file structure remains stable; human edits are minimal and follow documented markdown format
2. RFC 3339 timestamps are generated by the system; no manual timestamp entry or conflicts occur
3. Phase names in rollback entries exactly match the phase they're rolling back from
4. .tasks_history/ directory can be safely created if it doesn't exist
5. File system supports exclusive file mode (O_EXCL) for fail-fast concurrent write detection
6. Maximum task document size is approximately 100KB; no special handling required for larger documents
7. Metrics collection and comparison logic is provided externally; task_state.py and task_metrics.py handle document operations
8. Loop detection is manual; users explicitly invoke task_roll_back.py when issue detected

## Dependencies & Integration Points

- Python standard library: datetime.isoformat() for RFC 3339 timestamp generation
- Markdown file format validation (regex patterns for phase headers, rollback entries, SCORING sections)
- File system I/O with exclusive mode (O_EXCL) support for .TASK.md, read/write access to .metrics JSON file and .tasks_history/ directory
- JSON file format for `.metrics` with schema: `{ "TEST_PLAN": {...}, "CODING": {...}, "TESTING": {...} }`
- External metrics comparison logic (caller compares current vs. previous metrics in .metrics file to determine if rollback needed)
- Manual loop detection (user explicitly determines when to invoke task_roll_back.py)
- Task scripts directory (tasks_scripts/) must be accessible and executable
- Persistent counter/state for auto-incrementing task IDs (stored in .tasks_history/ or separate metadata file)

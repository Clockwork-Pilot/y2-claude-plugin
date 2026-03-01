# Tasks: Task Management System

**Input**: Design documents from `/specs/001-add-task-management/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Approach**: Test-Driven Development (TDD) - Write tests FIRST, confirm they fail, then implement

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Total: 80+ tasks across 10 phases.

## Format: `- [ ] [TaskID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create tasks_scripts/ directory structure with __init__.py
- [x] T002 Create pytest.ini and conftest.py at project root for TEST_LOG environment variable setup
- [x] T003 [P] Create .gitignore entries for __pycache__/, .pytest_cache/, *.pyc, .env
- [x] T004 Create tasks_scripts/tests/ subdirectories: fixtures/, integration/
- [x] T005 Create hooks/ directory and hooks/tests/ for common.py testing
- [x] T006 Add pydantic to project dependencies/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Pydantic Data Models

- [x] T007 [P] Create tasks_scripts/models.py with Pydantic models: PhaseHeader, ScoringEntry, RollbackEntry, Phase, , MetricsFile
  - PhaseHeader: phase_name (str), timestamp (datetime)
  - ScoringEntry: timestamp (datetime), metrics (dict), test_results (Optional[List[str]])
  - RollbackEntry: from_phase (str), timestamp (datetime), issue_type (str), problem_description (str)
  - Phase: header (PhaseHeader), content (str), scoring_entries (List[ScoringEntry]), rollback_entries (List[RollbackEntry])
  - : phases (List[Phase]), current_phase (str), created_at (datetime)
  - MetricsFile: TEST_PLAN (Optional[dict]), CODING (Optional[dict]), TESTING (Optional[dict])

### Parser Tests (Write FIRST)

- [x] T008 [P] Create tasks_scripts/tests/test_parsing.py with 8+ parser validation tests
  - test_parse_phase_header_valid
  - test_parse_scoring_entry_with_metrics_dict
  - test_parse_scoring_entry_with_test_results_list
  - test_parse_rollback_entry
  - test_parse_full_task_document
  - test_parse_invalid_timestamp_raises_validation_error
  - test_parse_malformed_metrics_raises_validation_error
  - test_roundtrip_markdown_to_model_to_markdown_equivalence
  - test_parse_metrics_file_with_exec_eval_structure
  - Confirm ALL tests FAIL before implementation

### Shared Task State Module

- [x] T009 Create tasks_scripts/task_state.py with core functions (uses models.py)
  - load_task_document(filepath: str) -> 
  - parse_phase_section(markdown_text: str) -> Phase
  - append_to_phase(doc: , phase_id: str, content: str) -> str (atomic regex with <!-- phase_id --> marker)
  - append_scoring(doc: , phase_id: str, entry: ScoringEntry) -> str
  - append_rollback_entry(doc: , phase_id: str, entry: RollbackEntry) -> str
  - load_metrics(filepath: str) -> MetricsFile
  - save_metrics(filepath: str, metrics: MetricsFile) -> None
  - validate_document_structure(doc: ) -> List[str] (returns list of errors if any)

- [x] T010 [P] Create tasks_scripts/tests/test_task_state.py - Unit tests for task_state.py (parsing, writing, validation with Pydantic assertions)
  - Test load_task_document() returns valid  model
  - Test .phases list populated correctly
  - Test Phase.header contains correct phase_name and timestamp
  - Test Phase.scoring_entries parsed as List[ScoringEntry]
  - Test Phase.rollback_entries parsed as List[RollbackEntry]
  - Test ScoringEntry.test_results properly extracted as List[str]
  - Test load corrupted (missing header) → Pydantic validation error
  - Test load corrupted (invalid timestamp) → Pydantic validation error
  - Test load corrupted (missing section markers) → error detection
  - Test append_to_phase() preserves  model validity (atomic regex)
  - Test append_scoring() creates valid ScoringEntry with metrics dict
  - Test round-trip:  → markdown →  (equivalence)
  - Confirm ALL tests FAIL before implementation

### Hook Integration

- [x] T011 Create hooks/common.py with task loading utilities (NO external imports beyond pydantic and pathlib)
  - load_task_document(start_dir: Optional[str] = None) -> Optional[]
    - Search for .TASK.md in start_dir, then parent directories up to repo root
    - Return  model if found and valid, None otherwise
    - Graceful error handling if file not found or corrupted
  - get_task_context(task_doc: Optional[]) -> Optional[dict]
    - Extract task metadata for logging
    - Return: {"task_name": str, "current_phase": str, "created_at": str} or None

- [x] T012 Create hooks/tests/test_common.py - Hook integration tests
  - test_load_task_document_finds_task_in_current_directory
  - test_load_task_document_searches_parent_directories
  - test_load_task_document_returns_none_if_not_found
  - test_load_task_document_returns_valid_task_document_model
  - test_get_task_context_extracts_correct_metadata
  - test_get_task_context_returns_none_when_task_doc_is_none
  - test_handler_logging_pattern_includes_task_key
  - test_handler_graceful_error_handling_when_task_loading_fails
  - Confirm ALL tests FAIL before implementation

### Test Fixtures

- [x] T013 [P] Create tasks_scripts/tests/fixtures/valid_single_phase.md - Sample .TASK.md with single TASK_PLAN.DEFINE phase
- [x] T014 [P] Create tasks_scripts/tests/fixtures/valid_multi_phase_with_scoring.md - Sample with multiple phases and SCORING entries
- [x] T015 [P] Create tasks_scripts/tests/fixtures/valid_exec_eval_with_test_lists.md - EXEC_EVAL phases with test result lists
- [x] T016 [P] Create tasks_scripts/tests/fixtures/corrupted_missing_header.md - Missing phase header for error testing
- [x] T017 [P] Create tasks_scripts/tests/fixtures/corrupted_invalid_timestamp.md - Invalid RFC 3339 timestamp
- [x] T018 [P] Create tasks_scripts/tests/fixtures/corrupted_malformed_sections.md - Malformed section markers

### Shared Test Configuration

- [x] T019 Create tasks_scripts/tests/conftest.py - Pytest fixtures for:
  - temp_task_dir (pytest tmpdir)
  - sample_task_document ( factory)
  - sample_phase (Phase factory)
  - sample_metrics (MetricsFile factory)
  - TEST_LOG environment variable setup

**Checkpoint**: Foundation ready - all tests written and failing, ready for user story implementation

---

## Phase 3: User Story 1 - Create and Initialize a Task (Priority: P1) 🎯 MVP

**Goal**: Create a new .TASK.md file with proper initial structure for task tracking

**Independent Test**: Can create a .TASK.md file with correct initial structure and verify phase header and timestamp are present

### Tests for User Story 1 (Write FIRST)

- [x] T020 [P] [US1] Create tasks_scripts/tests/test_task_create.py with unit tests
  - test_create_task_initializes_file_with_task_plan_define_header
  - test_create_task_records_rfc3339_timestamp
  - test_create_task_creates_file_in_correct_location
  - test_create_task_fails_if_file_already_exists
  - test_create_task_creates_valid_markdown_structure
  - test_create_task_pydantic_model_validation_succeeds_on_output
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 1

- [x] T021 [P] [US1] Implement tasks_scripts/task_create.py script
  - Main function: create_task(output_path: str = ".TASK.md") -> 
  - Create initial  with phase=TASK_PLAN.DEFINE, timestamp=now (RFC 3339)
  - Write to markdown file with proper header: "# PHASE TASK_PLAN.DEFINE at [timestamp]"
  - Add section marker: <!-- TASK_PLAN.DEFINE -->
  - Return  model
  - Exit code 0 on success, 1 on error (e.g., file exists)
  - Clear error messages to stdout

- [x] T022 [US1] Add error handling to task_create.py
  - Handle FileExistsError gracefully
  - Validate output path is writable
  - Log errors clearly for user

- [x] T023 [US1] Run test_task_create.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_create.py -v

**Checkpoint**: User Story 1 complete - can create new task documents

---

## Phase 4: User Story 2 - Progress Task Through Phases (Priority: P1)

**Goal**: Advance a task from one phase to the next in the predefined 7-phase workflow

**Independent Test**: Can advance task from TASK_PLAN.DEFINE → REFINE_CONTEXT, verify header updated with new timestamp, all prior content preserved

### Tests for User Story 2 (Write FIRST)

- [x] T024 [P] [US2] Create tasks_scripts/tests/test_task_roll.py with unit tests
  - test_advance_to_next_phase_in_workflow
  - test_phase_header_updated_with_new_timestamp
  - test_all_prior_content_preserved
  - test_phase_transitions_recorded_in_chronological_order
  - test_supports_all_7_phases_in_workflow
  - test_section_markers_preserved_after_roll
  - test_fails_on_invalid_phase_sequence
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 2

- [x] T025 [US2] Implement PHASE_WORKFLOW constant in tasks_scripts/task_state.py
  - PHASE_WORKFLOW = ["TASK_PLAN.DEFINE", "TASK_PLAN.REFINE_CONTEXT", "TASK_PLAN.DESIGN", "TASK_PLAN.DECOMPOSE", "EXEC_EVAL.TEST_PLAN", "EXEC_EVAL.CODING", "EXEC_EVAL.TESTING"]
  - Helper function: get_next_phase(current: str) -> str

- [x] T026 [US2] Implement tasks_scripts/task_roll.py script
  - Main function: advance_phase(task_path: str = ".TASK.md") -> 
  - Load current  from task_path
  - Get next phase from workflow
  - Create new phase header with timestamp (RFC 3339)
  - Update document using atomic regex with section markers
  - Use exclusive file mode (O_EXCL) for concurrent write detection
  - Return updated  model
  - Exit code 0 on success, 1 on error
  - Error cases: invalid phase sequence, concurrent write, file not found

- [x] T027 [US2] Add file locking to task_roll.py
  - Detect concurrent writes using O_EXCL (exclusive file mode)
  - Fail-fast with clear error message
  - Exit code 1 if concurrent access detected

- [x] T028 [US2] Run test_task_roll.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_roll.py -v

**Checkpoint**: User Story 2 complete - can advance through all phases safely

---

## Phase 5: User Story 3 - Collect and Record Evaluation Metrics (Priority: P2)

**Goal**: Collect code quality metrics at EXEC_EVAL phases and record in .metrics JSON + .TASK.md SCORING

**Independent Test**: Can run task_metrics.py at EXEC_EVAL.TEST_PLAN, append SCORING section with test results list, verify .metrics file created

### Tests for User Story 3 (Write FIRST)

- [x] T029 [P] [US3] Create tasks_scripts/tests/test_task_metrics.py with unit tests
  - test_collect_metrics_stores_in_metrics_json_file
  - test_metrics_structure_supports_test_plan_coding_testing
  - test_parse_test_results_list_from_metrics
  - test_append_scoring_section_to_task_document
  - test_scoring_entry_includes_timestamp_and_metrics
  - test_multiple_scoring_entries_timestamped_and_distinguishable
  - test_metrics_fail_on_invalid_json_format
  - test_scoring_appended_before_phase_section_marker
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 3

- [x] T030 [US3] Implement tasks_scripts/task_metrics.py script
  - Main function: collect_metrics(task_path: str = ".TASK.md", metrics_json: str = "{}") -> (, MetricsFile)
  - Parse incoming metrics JSON (dict with coverage, tests_passed, tests_failed, test_results: List[str])
  - Load current 
  - Create ScoringEntry with timestamp, metrics dict, test_results list
  - Load or create .metrics JSON file
  - Update .metrics[current_phase] with metrics
  - Append ScoringEntry to current phase in .TASK.md
  - Use atomic regex to insert before phase marker
  - Return updated  and MetricsFile models
  - Exit code 0 on success, 1 on error

- [x] T031 [US3] Add test results list parsing to task_metrics.py
  - Extract test_results: List[str] from metrics input
  - Support format: ["test_name_1", "test_name_2 (FAILED)", ...]
  - Populate ScoringEntry.test_results correctly

- [x] T032 [US3] Run test_task_metrics.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_metrics.py -v

**Checkpoint**: User Story 3 complete - can track metrics across phases

---

## Phase 6: User Story 4 - Rollback to Previous Phase with Issue Tracking (Priority: P1)

**Goal**: Revert to a previous phase when loop detected or metrics not improving, with rollback entry documentation

**Independent Test**: Can rollback from EXEC_EVAL.TESTING to EXEC_EVAL.CODING, verify rollback entry added with timing info, newer phases accessible

### Tests for User Story 4 (Write FIRST)

- [x] T033 [P] [US4] Create tasks_scripts/tests/test_task_roll_back.py with unit tests
  - test_rollback_to_specified_phase
  - test_rollback_to_previous_phase_when_target_not_specified
  - test_rollback_entry_added_with_problem_description
  - test_rollback_entry_includes_timing_information
  - test_newer_phase_data_preserved_after_rollback
  - test_fails_on_concurrent_write_with_o_excl
  - test_fails_on_invalid_target_phase
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 4

- [x] T034 [US4] Implement tasks_scripts/task_roll_back.py script
  - Main function: rollback_phase(task_path: str = ".TASK.md", target_phase: Optional[str] = None, reason: str = "loop detected") -> 
  - Load current 
  - If target_phase not specified: use get_previous_phase(current) from PHASE_WORKFLOW
  - Validate target_phase is earlier in workflow than current phase
  - Create RollbackEntry: from_phase=current, timestamp=now, issue_type=reason, problem_description provided
  - Append RollbackEntry to target_phase section before phase marker
  - Use atomic regex to insert
  - Use exclusive file mode (O_EXCL) for concurrent write detection
  - Return updated 
  - Exit code 0 on success, 1 on error

- [x] T035 [US4] Add rollback entry formatting to task_state.py
  - Format: "### [RFC 3339 timestamp] Back from [PREVIOUS_PHASE]"
  - Include problem description in section body
  - Proper markdown hierarchy

- [x] T036 [US4] Run test_task_roll_back.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_roll_back.py -v

**Checkpoint**: User Story 4 complete - can safely revert phases with history

---

## Phase 7: User Story 5 - Load and Parse Existing Task Document (Priority: P1)

**Goal**: Load .TASK.md from disk, validate structure, extract current phase and content into Pydantic models

**Independent Test**: Can load multi-phase .TASK.md, correctly identify current phase, parse all sections, report errors on corrupted files

### Tests for User Story 5 (Write FIRST)

- [x] T037 [P] [US5] Create tasks_scripts/tests/test_task_load.py with unit tests
  - test_load_valid_single_phase_document
  - test_load_valid_multi_phase_document
  - test_load_extracts_current_phase_correctly
  - test_load_parses_all_sections_into_models
  - test_load_returns_task_document_pydantic_model
  - test_load_reports_missing_phase_header_error
  - test_load_reports_invalid_section_markers_error
  - test_load_reports_line_number_for_errors
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 5

- [x] T038 [US5] Enhance task_state.py load_task_document() function (already defined in T009)
  - Read .TASK.md file
  - Use regex to detect phase headers: r"^# PHASE\s+(\S+)\s+at\s+(.+)$"
  - Extract timestamp, validate RFC 3339 format
  - Identify current phase (last phase header)
  - Parse sections using section markers: <!-- phase_id -->
  - Validate structure: all markers match phase names
  - Create Pydantic  model with full validation
  - Return  or raise Pydantic ValidationError
  - Collect errors: missing headers, invalid markers, malformed sections
  - Report errors with line numbers

- [x] T039 [US5] Add error reporting to task_state.py
  - Function: validate_document_structure(markdown: str) -> List[str]
  - Return list of error messages with line numbers
  - Error types: missing phase header, invalid timestamp, missing section marker, duplicate marker

- [x] T040 [US5] Run test_task_load.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_load.py -v

**Checkpoint**: User Story 5 complete - can safely load and validate task documents

---

## Phase 8: User Story 6 - Update Task Document with Mid-Document Edits (Priority: P1)

**Goal**: Append content to current phase safely using atomic regex updates, preventing corruption in large documents

**Independent Test**: Can append content to current phase in 10+ phase document with 50+ entries, verify all prior content unchanged, correct ordering

### Tests for User Story 6 (Write FIRST)

- [x] T041 [P] [US6] Create tasks_scripts/tests/test_task_update.py with unit tests
  - test_append_content_to_single_phase
  - test_append_content_to_current_phase_in_multi_phase
  - test_appended_content_appears_in_correct_location
  - test_appended_content_before_phase_marker
  - test_earlier_phases_unchanged_after_append
  - test_later_phases_unchanged_after_append
  - test_atomic_regex_update_preserves_all_content
  - test_large_document_10_plus_phases_50_plus_entries
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 6

- [x] T042 [US6] Enhance task_state.py append_to_phase() function (already defined in T009)
  - Load  from markdown
  - Identify current phase ID
  - Use atomic regex: `re.sub(rf'(<!-- {phase_id} -->)', f'{new_content}\n\1', markdown)`
  - Verify content inserted before phase marker
  - Return updated markdown string
  - Use exclusive file mode (O_EXCL) for atomic write
  - No partial writes on error

- [x] T043 [US6] Add content ordering validation
  - Verify appended content appears in chronological order
  - Test with multiple appends to same phase
  - Confirm SCORING entries timestamped in order

- [x] T044 [US6] Run test_task_update.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_update.py -v
  - Include large document stress test (10+ phases, 50+ entries)

**Checkpoint**: User Story 6 complete - document updates are safe and atomic

---

## Phase 9: User Story 7 - Archive Completed Tasks with Naming Convention (Priority: P2)

**Goal**: Move completed .TASK.md to .tasks_history/ with standardized naming (auto-increment or GitHub ID)

**Independent Test**: Can archive successful task as TASK_00001_DESCRIPTION, GitHub task as GITHUB_ISSUE_345345_DESCRIPTION, failed task with __FAILURE__

### Tests for User Story 7 (Write FIRST)

- [x] T045 [P] [US7] Create tasks_scripts/tests/test_task_archive.py with unit tests
  - test_archive_moves_to_tasks_history_directory
  - test_archive_generates_auto_incremented_task_id
  - test_archive_uses_github_issue_id_when_specified
  - test_archive_adds_failure_prefix_on_failure
  - test_archive_naming_format_task_#####_description
  - test_archive_naming_format_github_issue_#####_description
  - test_archive_failure_naming_includes_failure_prefix
  - test_archive_creates_directory_if_missing
  - test_archive_case_converts_description_to_uppercase
  - Confirm ALL tests FAIL before implementation

### Implementation for User Story 7

- [x] T046 [US7] Implement tasks_scripts/task_archive.py script
  - Main function: archive_task(task_path: str = ".TASK.md", task_id: Optional[int] = None, is_github_issue: bool = False, github_id: Optional[int] = None, failure: bool = False) -> str
  - Load 
  - Extract task name/description from first phase content or user input
  - If is_github_issue and github_id provided: use "GITHUB_ISSUE_{github_id:05d}"
  - Else: use "TASK_{task_id:05d}" with auto-increment if task_id not provided
  - Add "__FAILURE__" prefix immediately after ID if failure=True
  - Convert description to UPPER_CASE with underscores
  - Create .tasks_history/ directory if missing
  - Move (not copy) .TASK.md to new filename in .tasks_history/
  - Return full archived path
  - Exit code 0 on success, 1 on error

- [x] T047 [US7] Add auto-increment logic for task IDs
  - Function: get_next_task_id(history_dir: str = ".tasks_history") -> int
  - Scan directory for TASK_##### files
  - Extract all used IDs
  - Return max(IDs) + 1
  - Start at 1 if directory empty

- [x] T048 [US7] Run test_task_archive.py - ALL tests MUST PASS
  - pytest tasks_scripts/tests/test_task_archive.py -v

**Checkpoint**: User Story 7 complete - tasks properly archived with standardized naming

---

## Phase 10: Integration & Polish

**Purpose**: Cross-cutting concerns, integration testing, hook handler updates, documentation

### Integration Testing

- [x] T049 [P] Create tasks_scripts/tests/integration/test_task_workflow.py
  - Full workflow test: create → roll → metrics → roll → metrics → roll → archive
  - Large document test: 10+ phases, 50+ rollback/scoring entries
  - Concurrent write detection test (O_EXCL)
  - Error recovery test (rollback after partial operation)

- [x] T050 Run full integration test suite
  - pytest tasks_scripts/tests/integration/ -v
  - All tests MUST PASS

### Hook Handler Integration

- [x] T051 [P] Update hooks/[handler].py to integrate task loading
  - Import load_task_document, get_task_context from hooks/common.py
  - Load task at handler entry point
  - Add "task" key to all log structures via serialize_log_data()
  - Test: handler runs with and without .TASK.md present
  - Handler execution unaffected if task file missing (graceful)

- [x] T052 [P] Verify hooks/common.py integration with all existing handlers
  - Each handler logs task context
  - No handler crashes if .TASK.md absent
  - Task context available in hook_logging output

### Documentation

- [x] T053 Create tasks_scripts/README.md with:
  - Overview of task management system
  - Script usage examples (create, roll, metrics, rollback, archive)
  - Pydantic model reference
  - .TASK.md format specification
  - Section marker convention: <!-- phase_id -->
  - Atomic update pattern with regex
  - Error handling and concurrent write detection

- [x] T054 Create QUICKSTART.md with:
  - Complete workflow example (create → multiple phases → archive)
  - Hook handler integration example
  - Test results list format
  - Metrics JSON structure

### Quality Assurance

- [x] T055 [P] Run full test suite with coverage
  - pytest tasks_scripts/tests/ --cov=tasks_scripts --cov-report=html
  - Target: 95%+ coverage
  - Ensure all happy paths and error paths tested

- [x] T056 [P] Run linting and style checks
  - flake8 tasks_scripts/
  - black --check tasks_scripts/
  - mypy tasks_scripts/ (if using type hints)

- [x] T057 Verify exclusive file mode (O_EXCL) works on target platform
  - Test on Unix/Linux/macOS
  - Document Windows compatibility notes if applicable

- [x] T058 Performance validation
  - Measure task_roll.py: <100ms for phase advancement (SC-002)
  - Measure task_state parsing: <50ms for 100KB documents
  - Test with large documents: 10+ phases, 50+ entries

---

## Task Summary

**Total Tasks**: 58 core implementation tasks
**Test Tasks**: 25 unit + integration test tasks
**All Tasks**: TDD-first (tests written before implementation)

**By User Story**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 13 tasks (critical blocking prerequisites)
- Phase 3 (US1 - Create): 4 tasks
- Phase 4 (US2 - Progress): 5 tasks
- Phase 5 (US3 - Metrics): 4 tasks
- Phase 6 (US4 - Rollback): 3 tasks
- Phase 7 (US5 - Load): 3 tasks
- Phase 8 (US6 - Update): 3 tasks
- Phase 9 (US7 - Archive): 3 tasks
- Phase 10 (Polish): 9 tasks

**Parallelizable Tasks**: 25+ marked with [P]

---

## Parallel Execution Examples

### Fast Path (MVP - User Stories 1, 2, 5, 6):
1. Complete Phase 1 Setup (T001-T006)
2. Complete Phase 2 Foundational (T007-T019) - MUST complete first
3. In parallel:
   - Phase 3 US1 (T020-T023): T020 and T021 parallel
   - Phase 4 US2 (T024-T028): T024 parallel
   - Phase 7 US5 (T037-T040): T037 parallel
   - Phase 8 US6 (T041-T044): T041 parallel
4. Complete Phase 10 Integration (T049-T058)

**MVP Time**: ~2 weeks (Phases 1-2 sequential, then US1/US2/US5/US6 parallel, then polish)

### Full Implementation:
Complete all phases sequentially with parallelization within each story:
- Phase 1: 1 day
- Phase 2: 2 days (foundation critical)
- Phase 3-9: 8 days (can parallelize stories within each phase)
- Phase 10: 2 days

**Full Time**: ~3 weeks

---

## MVP Scope (Phase 1 + Phase 2 + User Stories 1, 2, 5, 6)

✅ **Minimum Viable Product includes**:
- Create task documents (US1)
- Advance through phases (US2)
- Load and parse documents (US5)
- Safe document updates (US6)
- Pydantic models with validation
- Parser tests with Pydantic assertions
- Atomic regex updates with section markers
- Concurrent write protection (O_EXCL)
- Hook handler integration

❌ **Not in MVP (Phase 2 features)**:
- Metrics collection (US3)
- Rollback functionality (US4)
- Task archival (US7)

---

## Format Validation Checklist

✅ All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story?] Description`
✅ All task IDs sequential (T001, T002, ...)
✅ All file paths explicit and absolute-ready
✅ [P] markers indicate parallelizable tasks
✅ [Story] labels on US phases only (US1-US7)
✅ No story labels on Setup (Phase 1), Foundational (Phase 2), or Polish (Phase 10)
✅ Dependencies clear (e.g., T024 depends on T022 completion)
✅ Each user story independently testable
✅ Test tasks marked with clear acceptance criteria

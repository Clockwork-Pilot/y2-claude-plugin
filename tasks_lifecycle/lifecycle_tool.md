# Task Management System

## Table of Contents

- [Overview](#overview)
  - [Purpose](#purpose)
  - [Phase Workflow](#phase-workflow)
- [Storage](#storage)
  - [task.json](#task-json)
  - [task.md](#task-md)
  - [.metrics](#metrics)
- [Task Scripts](#task-scripts)
  - [task_create.py](#task-create-py)
  - [task_roll.py](#task-roll-py)
  - [task_metrics.py](#task-metrics-py)
  - [task_roll_back.py](#task-roll-back-py)
  - [task_archive.py](#task-archive-py)
- [JSON Patch Operations](#json-patch-operations)
  - [Patch Helpers](#patch-helpers)
  - [Execution Flow](#execution-flow)
- [Integration](#integration)
  - [Data Models](#data-models)
  - [State Module (task_state.py)](#state-module--task-state-py)
  - [Rendering](#rendering)
- [Examples](#examples)
  - [Create Task](#create-task)
  - [Advance Phase](#advance-phase)
  - [Record Metrics](#record-metrics)
  - [Rollback Phase](#rollback-phase)
  - [Archive Task](#archive-task)

Task lifecycle management system for tracking execution through phases with metrics collection and rollback support

**Version:** 2.0.0

**Backend:** knowledge_base_system

## Overview
High-level overview of the task management system

### Purpose
The task management system tracks task execution through a 7-phase workflow, collecting metrics at evaluation phases and supporting rollback when issues are detected. All state is stored in task.json using the Doc model with JSON Patch operations for mutations.

### Phase Workflow
Tasks progress through 7 phases in strict order

**Phases:**
  - TASK_PLAN.DEFINE - Initial task definition
  - TASK_PLAN.REFINE_CONTEXT - Refine context and requirements
  - TASK_PLAN.DESIGN - Design solution approach
  - TASK_PLAN.DECOMPOSE - Decompose into subtasks
  - EXEC_EVAL.TEST_PLAN - Create and execute test plan
  - EXEC_EVAL.CODING - Implement solution
  - EXEC_EVAL.TESTING - Execute final testing

## Storage
How task state is stored and managed

### task.json
Primary state storage using Doc model (JSON). Contains all phase information, content, scoring entries, and rollback history.

**Format:** JSON (Doc model)

**Structure:**
  - Id: task_id
  - Label: Task Label
  - Type: Doc
  - Metadata: {'description': 'Task metadata', 'created_at': 'RFC 3339 timestamp', 'current_phase': 'Current phase name'}
  - Children: {'phases': 'Dict of phase nodes by phase_id'}

### task.md
Auto-rendered markdown from task.json for human readability. Generated automatically by apply_json_patch after every mutation.

**Format:** Markdown (auto-generated)

**Note:** Do not edit manually - always regenerated from task.json

### .metrics
Separate JSON file storing structured metrics for programmatic comparison across phases

**Format:** JSON

**Structure:**
  - Test Plan: Metrics object from EXEC_EVAL.TEST_PLAN phase
  - Coding: Metrics object from EXEC_EVAL.CODING phase
  - Testing: Metrics object from EXEC_EVAL.TESTING phase

## Task Scripts
Five scripts handle core task operations

### task_create.py
Initialize a new task with TASK_PLAN.DEFINE phase

**Usage:** python task_create.py [path]

**Default Path:** task.json

**Creates:**
  - task.json
  - task.md (auto-rendered)

**Process:**
  1. Generate initial Doc structure with create_initial_task_doc()
  2. Write task.json to disk
  3. Apply empty JSON Patch to trigger rendering
  4. Auto-render task.md from task.json

### task_roll.py
Advance task to next phase in workflow

**Usage:** python task_roll.py [path]

**Default Path:** task.json

**Process:**
  1. Load task.json and validate current phase
  2. Calculate next phase (fail if already final)
  3. Generate JSON Patch via patch_advance_phase()
  4. Apply patch with apply_json_patch()
  5. Auto-render task.md

**Concurrency:** Uses exclusive lock file to detect concurrent writes

### task_metrics.py
Collect and record metrics at current phase

**Usage:** python task_metrics.py [path] [metrics_json]

**Default Path:** task.json

**Input:** JSON dict with metrics, test_results, coverage, coverage_summary

**Process:**
  1. Parse incoming metrics JSON
  2. Create ScoringEntry with timestamp and metrics
  3. Generate JSON Patch via patch_add_scoring_entry()
  4. Apply patch to task.json
  5. Update .metrics file for programmatic comparison
  6. Auto-render task.md

### task_roll_back.py
Revert task to previous phase with issue documentation

**Usage:** python task_roll_back.py [path] [target_phase] [reason]

**Default Path:** task.json

**Parameters:**
  - target_phase: Phase to rollback to (default: previous phase)
  - reason: Issue description (loop, metrics_regression, etc.)

**Process:**
  1. Load task and determine target phase
  2. Create RollbackEntry with issue type and description
  3. Generate JSON Patch via patch_add_rollback_entry()
  4. Apply patch to add rollback to target phase
  5. Update current_phase in metadata via JSON Patch
  6. Auto-render task.md

### task_archive.py
Archive completed task to .tasks_history/ with naming convention

**Usage:** python task_archive.py [path] [task_id] [--github] [--failure]

**Default Path:** task.json

**Naming Convention:**
  - Regular Success: TASK_#####_DESCRIPTION
  - Regular Failure: TASK_#####__FAILURE__DESCRIPTION
  - Github Success: GITHUB_ISSUE_#####_DESCRIPTION
  - Github Failure: GITHUB_ISSUE_#####__FAILURE__DESCRIPTION

**Process:**
  1. Load task.json and extract description
  2. Determine archive folder name based on task ID and status
  3. Create folder in .tasks_history/
  4. Move task.json, task.md, .metrics to folder

## JSON Patch Operations
How task operations generate and apply JSON Patch operations

### Patch Helpers
Functions in knowledge_base/tools/common/task_helpers.py that generate RFC 6902 operations

**File:** tasks_lifecycle/tools/common/task_helpers.py

**Functions:**
  - patch_advance_phase(current_phase) - Generate next phase creation
  - patch_add_scoring_entry(phase_name, entry) - Add metrics entry
  - patch_add_rollback_entry(phase_name, entry) - Add rollback record
  - patch_update_phase_content(phase_name, content) - Update phase body
  - create_initial_task_doc(task_id) - Bootstrap initial structure

### Execution Flow
How patches are applied to task.json

**Steps:**
  1. Generate patch operations via task_helpers functions
  2. Serialize to JSON string (RFC 6902 format)
  3. Call apply_json_patch(path, patch_json, create=False)
  4. apply_json_patch handles: validation, atomic write, rendering

**Note:** create=True flag enables creating new documents during initialization

## Integration
How task management integrates with knowledge base system

### Data Models
Task-specific Pydantic models in tasks_lifecycle/tools/common/

**Location:** tasks_lifecycle/tools/common/task_model.py

**Models:**
  - TaskDocument - Complete task representation
  - Phase - Single phase with header, content, entries
  - PhaseHeader - Phase name and timestamp
  - ScoringEntry - Metrics, test results, coverage
  - RollbackEntry - Issue documentation
  - MetricsFile - Structured metrics by phase

### State Module (task_state.py)
Central module for task operations in tasks_lifecycle/tools/

**Functions:**
  - load_task_document(path) - Read task.json, convert to TaskDocument
  - advance_phase(path) - Advance to next phase via JSON Patch
  - append_scoring(path, phase, entry) - Add metrics via JSON Patch
  - append_rollback_entry(path, phase, entry) - Add rollback via JSON Patch
  - append_to_phase(path, phase, content) - Append content via JSON Patch
  - validate_document_structure(path) - Verify task.json validity
  - load_metrics(path) - Load .metrics file
  - save_metrics(path, metrics) - Save .metrics file

### Rendering
Automatic markdown generation from task.json

**Handler:** apply_json_patch from knowledge_base (via sys.path integration) + _render_doc_internal

**Flow:** task.json (Doc model) → apply_json_patch → auto-render task.md

**Note:** Auto-renders via knowledge_base apply_json_patch - no custom renderers needed

## Examples
Usage examples for task operations

### Create Task
```
python task_create.py task.json
```

**Result:** ✓ Created task.json
Creates task.json with TASK_PLAN.DEFINE phase and auto-renders task.md

### Advance Phase
```
python task_roll.py task.json
```

**Result:** ✓ Advanced to phase: TASK_PLAN.REFINE_CONTEXT
Adds new phase section to task.json, updates current_phase, renders task.md

### Record Metrics
```
python task_metrics.py task.json '{"coverage": 85, "tests_passed": 42, "test_results": ["test_1", "test_2"]}'
```

**Result:** ✓ Metrics collected at EXEC_EVAL.TEST_PLAN
Adds ScoringEntry to phase, updates .metrics file, renders task.md

### Rollback Phase
```
python task_roll_back.py task.json EXEC_EVAL.CODING 'loop detected'
```

**Result:** ✓ Rolled back to EXEC_EVAL.CODING
Adds RollbackEntry to target phase, updates current_phase, renders task.md

### Archive Task
```
python task_archive.py task.json --github --github-id 12345 --failure
```

**Result:** ✓ Task archived to: .tasks_history/GITHUB_ISSUE_12345__FAILURE__DESCRIPTION/
Moves task.json, task.md, .metrics to timestamped folder

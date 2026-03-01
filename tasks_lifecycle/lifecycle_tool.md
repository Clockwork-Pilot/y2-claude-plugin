# Task Management System

## Table of Contents

- [Overview](#overview)
  - [Purpose](#purpose)
  - [Iteration Workflow](#iteration-workflow)
    - [Evolution](#evolution)
      - [Linear Progression](#linear-progression)
      - [Decision Flow](#decision-flow)
    - [Process Steps](#process-steps)
- [Metrics Collection](#metrics-collection)
- [Task Scripts](#task-scripts)
  - [task_create.py](#task-create-py)
  - [task_roll.py](#task-roll-py)
  - [task_metrics.py](#task-metrics-py)
  - [task_archive.py](#task-archive-py)
- [Task Model](#task-model)
  - [Iteration](#iteration)
  - [CodeStats](#codestats)
  - [TaskTestMetrics](#tasktestmetrics)
- [State & Integration](#state---integration)
  - [State Storage](#state-storage)
  - [Rendering](#rendering)
- [Examples](#examples)
  - [Create Task](#create-task)
  - [First Iteration](#first-iteration)
  - [Metrics Collection](#metrics-collection)
  - [Second Iteration](#second-iteration)
  - [Archive Task](#archive-task)

Iteration-based task management system for tracking task execution through numbered iterations with metrics collection

**Version:** 1.0.0

**Backend:** knowledge_base_system

## Overview
High-level overview of the iteration-based task management system

### Purpose
The task management system uses the knowledge base as its state store, persisting task.json with Task model (RenderableModel). Tasks progress through iterations, collecting code and test metrics at each iteration. Iterations stop when metrics no longer change. All state mutations use Pydantic models for validation, and markdown is auto-rendered for human readability.

### Iteration Workflow
Tasks progress through iterations, each collecting metrics. Stop when metrics no longer change.

#### Evolution
Task state progression through iterations

##### Linear Progression
```
task.json → [Plan] → iteration_1 → iteration_2 → ... → iteration_n → archive
```

##### Decision Flow
```
[Create] → [Iteration] → [Metrics] → [Changed?] → YES: [Work] | NO: [Archive]
```

#### Process Steps
How each iteration progresses

**Steps:**
  1. Create task.json with plan Doc
  2. Complete work: code changes, run tests
  3. Run task_roll.py: collects metrics, creates iteration_N
  4. Check: did metrics change from previous iteration?
  5. If YES: go to step 2 | If NO: archive task

## Metrics Collection
Metrics are collected automatically at each iteration via task_metrics.py

**Metrics Types:**
  - Code Stats: Files changed, lines added/removed from git diff
  - Tests Stats: Number of passed tests vs total tests
  - Coverage Stats By Tests: Lines covered per test

**Stopping Condition:** Task stops iterating when metrics do not change from previous iteration

## Task Scripts
Four scripts handle core task lifecycle operations: create, roll iterations, collect metrics, and archive

### task_create.py
Initialize task.json with plan Doc

**Process:**
  - Fail if task.json exists
  - Create Task with initial Doc plan
  - Add created_at, updated_at metadata
  - Write task.json and auto-render task.md

### task_roll.py
Record iteration completion with metrics

**Process:**
  - Load task.json and parse as Task model
  - Collect metrics (git diff + pytest)
  - Create iteration_N with code_stats, tests_stats
  - Write updated task.json

### task_metrics.py
Collect code and test metrics

**Sources:**
  - Code metrics from git diff (added/removed lines, files changed)
  - Test metrics from pytest (passed/total tests)
  - Coverage metrics per test

### task_archive.py
Archive completed task to tasks_history/

**Naming Format:** YYYYMMDD-HHMMSS-task-ID.json and .md

## Task Model
Root task container with plan and iterations

### Iteration
Single iteration tracking code and test metrics

**Fields:**
  - Id: str - iteration_1, iteration_2, ...
  - Metadata: Dict - created_at, updated_at
  - Code Stats: CodeStats - lines added/removed, files changed
  - Tests Stats: TaskTestMetrics - passed/total tests
  - Coverage Stats By Tests: Dict - lines covered per test

### CodeStats
Code change metrics from git

**Fields:**
  - Added Lines: int
  - Removed Lines: int
  - Files Changed: int

### TaskTestMetrics
Test execution metrics from pytest

**Fields:**
  - Passed: int - tests passed
  - Total: int - total tests
  - Pass Rate: float - calculated (passed/total)*100

## State & Integration
How task state is stored and managed using knowledge base system

### State Storage
Task state persisted in knowledge base

**Format:** task.json - JSON using Task/Iteration models

**Rendering:** task.md - Auto-rendered markdown from task.json

**Validation:** Pydantic models validate on load/save

### Rendering
Task and Iteration models render to markdown

**Approach:** Pure abstraction - models handle rendering logic only

**Methods:** Task.render() and Iteration.render() return markdown strings

**File Io:** Separate from models - handled by scripts

## Examples
Usage examples for task operations

### Create Task
```
python3 -m tasks_lifecycle.tools.create_task
```

**Result:** ✓ Created task file: task.json

**Creates:** task.json with Task model (plan Doc + empty iterations)

### First Iteration
```
python3 -m tasks_lifecycle.tools.task_roll
```

**Result:** ✓ Rolled task with iteration iteration_1
  Code: +42 -5 (3 files)
  Tests: 10/12 passed (83.3%)

**Creates:** iteration_1 entry in task.json with metrics

### Metrics Collection
Metrics are collected automatically by task_roll.py

```
python3 -m tasks_lifecycle.tools.task_metrics
```

**Output:** {
  "code_stats": {"added_lines": 42, "removed_lines": 5, "files_changed": 3},
  "tests_stats": {"passed": 10, "total": 12},
  "coverage_stats_by_tests": {"test_1": 45, "test_2": 38}
}

### Second Iteration
Run another iteration after changes

```
# Make changes to code
python3 -m tasks_lifecycle.tools.task_roll
```

**Result:** ✓ Rolled task with iteration iteration_2
  Code: +15 -2 (2 files)
  Tests: 11/12 passed (91.7%)

**Note:** Process repeats until metrics no longer change

### Archive Task
```
python3 -m tasks_lifecycle.tools.task_archive
```

**Result:** ✓ Archived task task_1
  JSON: tasks_history/20260301-153021-task-task_1.json
  MD:   tasks_history/20260301-153021-task-task_1.md

**Creates:** Timestamped files in tasks_history/ directory

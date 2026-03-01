# Knowledge Tools

## Table of Contents

- [API](#api)
  - [Scripts](#scripts)
    - [apply_json_patch.py](#apply-json-patch-py)
      - [Script Example](#script-example)
  - [Functions](#functions)
    - [apply_json_patch()](#apply-json-patch)
    - [Opts Configuration](#opts-configuration)
      - [render_priority Field](#render-priority-field)
- [Architecture](#architecture)
  - [Json Patch](#json-patch)
  - [Document Rendering](#document-rendering)
  - [Workflow](#workflow)
- [Testing](#testing)

Knowledge storage system with JSON Patch API and Pydantic validation

**Version:** 1.0.0

## API
Public interfaces for knowledge tools: command-line scripts and Python functions

### Scripts
Command-line script interfaces

#### apply_json_patch.py
Apply JSON Patch operations to knowledge documents from command line with automatic markdown rendering.

```
python3 apply_json_patch.py <document_path> <json_patch>
python3 apply_json_patch.py knowledge_base/knowledge_tool.json '[{"op": "replace", "path": "/label", "value": "Updated"}]'
```

**File:** apply_json_patch.py

**Usage:** python3 apply_json_patch.py <document_path> <json_patch>

**Arguments:**
  - document_path (str): Path to Doc JSON file
  - json_patch (str): RFC 6902 JSON Patch operations as JSON string

**Exit Codes:**
  - 0: Success - patch applied
  - 1: Error - JSON returned with error details

**Output:** Success: ✓ Patch applied to <path>. Error: JSON error response

##### Script Example
Complete example of script invocation

```
python3 apply_json_patch.py knowledge_base/knowledge_tool.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'
```

**Expected Output:** ✓ Patch applied to knowledge_base/knowledge_tool.json

### Functions
Python function interfaces for programmatic use

#### apply_json_patch()
Apply JSON Patch to document file with validation and automatic markdown rendering.

```
apply_json_patch(document_path: str, json_patch: str) -> Optional[ApplyPatchErrorResponse]
```

**Parameters:**
  - document_path (str): Path to Doc JSON file
  - json_patch (str): RFC 6902 JSON Patch operations as JSON string

**Returns:** None on success, ApplyPatchErrorResponse object on error with detailed context

**Exceptions:**
  - JsonPatchException - Invalid patch format
  - ValidationError - Schema violation
  - FileNotFoundError - Document not found
  - IOError - File access issues

**Behavior:** All exceptions caught and returned as ApplyPatchErrorResponse with helpful hints

**Safety:** Atomic operations, in-memory validation before write, file protection workflow, read-only file management

**Rendering:** Every successful patch automatically generates markdown: document.json → document.md with identical file protection

#### Opts Configuration
Non-displayable rendering options for document nodes

##### render_priority Field
When true, renders node before siblings with render_priority=false

**Type:** bool

## Architecture
API-first design with JSON Patch operations

### Json Patch
RFC 6902 JSON Patch standard for describing modifications to JSON documents.

**File:** apply_json_patch.py

**Standard:** RFC 6902

**Operations:**
- add - Insert or replace value
- remove - Delete value at path
- replace - Replace value at path
- move - Move value from one path to another
- copy - Copy value from one path to another
- test - Assert value equals expected before applying

```
[{"op": "replace", "path": "/label", "value": "new_label"}, {"op": "add", "path": "/children/new_id", "value": {...}}]
```

**Operation Structure:**
  - Required Fields: ['op', 'path']
  - Optional Fields: ['value', 'from']
  - Op: Operation type (add, remove, replace, move, copy, test)
  - Path: JSON Pointer to target location
  - Value: New value for add/replace/test operations
  - From: Source path for move/copy operations

### Document Rendering
Internal automatic markdown generation on patch application (not a public API)

**File:** render_doc.py

**Status:** complete_internal_only

### Workflow
Complete knowledge tool operation workflow from API call to markdown generation.

**Main Flow:**
read JSON → validate patch → apply in memory → validate schema → write with protection → render markdown

**File Protection (within Write step):**
remove read-only → exclusive write → atomic rename → restore read-only

**Main Steps:**
  1. Read Document - Load and parse JSON file
  2. Parse & Validate Patch - Validate RFC 6902 format
  3. Apply in Memory - Execute patch operations on dict
  4. Validate Schema - Check Pydantic Doc model
  5. Write with Protection - Atomic file write with read-only management
  6. Auto-Render Markdown - Generate .md from JSON

**File Protection Phases:**
  - Remove read-only attribute
  - Exclusive write to temp file
  - Atomic rename to target
  - Restore read-only/archive attribute

## Testing
Comprehensive test suite with 18 tests covering all functionality.

```
pytest knowledge_base/tools/ -v
pytest
```

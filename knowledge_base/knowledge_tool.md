# Knowledge Tools

Knowledge storage system with JSON Patch API and Pydantic validation
**Version:** 1.0.0

## API

Public API functions for knowledge tools

### apply_json_patch.py

**File:** apply_json_patch.py
Apply JSON Patch operations to knowledge documents with automatic markdown rendering.

```bash
python3 apply_json_patch.py <document_path> <json_patch>
```

Example:
```bash
python3 apply_json_patch.py knowledge_base/knowledge_tool.json '[{"op": "replace", "path": "/label", "value": "Updated"}]'
```

#### Function Signature

**Signature:** apply_json_patch(document_path: str, json_patch: str) -> Optional[ApplyPatchErrorResponse]
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
**Script Call Convention:** python3 apply_json_patch.py <document_path> <json_patch>
**Call Example:** python3 apply_json_patch.py knowledge_base/knowledge_tool.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'
**Parameters Explanation:**
  - Document Path: Full or relative path to JSON document file
  - Json Patch: RFC 6902 JSON Patch as JSON string - array of operation objects

### Opts Configuration

Non-displayable rendering options for document nodes

#### render_priority Field

**Type:** bool
When true, renders node before siblings with render_priority=false

## Architecture

API-first design with JSON Patch operations

### Patch Operations

**Files:**
  - apply_json_patch.py
RFC 6902 JSON Patch implementation with Pydantic validation

### Error Handling

**Files:**
  - response_model.py
Categorized error responses

## Testing

Comprehensive test suite

### Test Coverage

**Count:** 17
Success, syntax, path, validation, file protection tests

## Implementation

Key implementation details and workflows

### File Protection Workflow

Multi-phase write protection: remove read-only → exclusive write → restore read-only

### Error Categories

**Count:** 4
**Types:**
  - JSON Patch Syntax
  - Path Not Found
  - Pydantic Validation
  - File Operations

## Features

Planned and implemented features

### Document Rendering

**File:** render_doc.py
**Status:** complete_internal_only
Internal automatic markdown generation on patch application (not a public API)

## Documentation

Complete API and usage documentation (from README)

### Overview

JSON document storage with Pydantic validation and JSON Patch operations

### API Reference

Single function apply_json_patch(document_path, json_patch) executes RFC 6902 JSON Patch operations on knowledge documents

### Document Format

Fields: id, label, type, metadata, children (dict or null)

### Error Responses

ApplyPatchErrorResponse with hint, example, parent_path, existing_children

### File Write Workflow

Remove read-only → exclusive write → atomic rename → restore read-only

### Type Extensibility

Type field as anchor for future document type extensions

### Document Structure Detail

Complete Doc schema with all fields and constraints

### API Process Flow

Step-by-step process: read → validate patch → apply in memory → validate schema → write with protection

#### 1. Read Document

Load JSON document from file, parse into Python dict, validate file accessibility

#### 2. Parse & Validate Patch

Parse JSON Patch string, validate RFC 6902 format, check all required fields (op, path)

#### 3. Apply in Memory

Execute patch operations (add/replace/remove) on document dict without touching file

#### 4. Validate Schema

Validate patched document against Pydantic Doc model, check all required fields and types

#### 5. Write with Protection

Remove read-only, atomic write to temp file, rename to target, restore read-only/archive

#### 6. Auto-Render Markdown

Generate markdown representation from updated JSON, save as .md file with same workflow

### Usage Examples

Apply patches to add/update/remove document nodes, with comprehensive error handling and helpful hints

#### Add Node Example

Create new child node with op=add, path=/children/new_id, value={doc object}

#### Replace Field Example

Update existing field with op=replace, path=/label, value=new_label_text

#### Remove Node Example

Delete child node with op=remove, path=/children/old_id

#### Error Handling

Returns ApplyPatchErrorResponse with contextual hints for syntax, path, or validation errors

### File Management Strategy

Before/during/after modification phases with protection attributes

### Type Extensibility Details

Requirements for adding custom document types with new Pydantic models

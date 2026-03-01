# Knowledge Tools - Document Management System

Structured JSON document storage with Pydantic validation and JSON Patch operations.

## Overview

Documents are JSON files with a strict but extensible schema:
- Schema validation via Pydantic `Doc` model
- Exclusive write mode: read-only/archive until modification
- All modifications via JSON Patch (RFC 6902)
- Type-based extensibility for adding new document types

## Document Structure

```json
{
  "id": "root",
  "label": "Root Node",
  "type": "Doc",
  "metadata": {},
  "children": {
    "child_id": {
      "id": "child_id",
      "label": "Child Node",
      "type": "Doc",
      "metadata": {},
      "children": null
    }
  }
}
```

**Fields:**
- `id` (str): Unique identifier
- `label` (str): Human-readable name
- `type` (Literal["Doc"]): Document type (extensible)
- `metadata` (dict): Flexible key-value data
- `children` (dict | null): Child documents keyed by ID (omit if none)

## API

### Single Function

```python
apply_json_patch(document_path: str, json_patch: str) -> Optional[ApplyPatchErrorResponse]
```

**Input:**
- `document_path`: Path to document JSON file
- `json_patch`: JSON Patch operations as string (RFC 6902)

**Output:**
- `None` on success (document updated)
- `ApplyPatchErrorResponse` on error (with context and hints)

**Process:**
1. Read document (exclusive lock)
2. Parse and validate JSON Patch
3. Apply patch in memory
4. Validate against Pydantic schema
5. Write changes (exclusive write mode)
6. Archive/read-only file

## Error Handling

### JSON Patch Syntax Error
Returns error with **hardcoded example**:
```json
{
  "error": "Invalid JSON Patch syntax: ...",
  "hint": "JSON Patch must be valid JSON array of operations",
  "example": [
    {"op": "add", "path": "/children/new_id", "value": {"id": "new_id", "label": "New", "type": "Doc"}},
    {"op": "replace", "path": "/label", "value": "Updated Label"},
    {"op": "remove", "path": "/children/old_id"}
  ],
  "operation": "apply_json_patch"
}
```

### Path Not Found
Checks parent path and lists **possible child paths**:
```json
{
  "error": "Path not found: ...",
  "hint": "Check parent path and available children",
  "parent_path": "/children",
  "existing_children": ["child1", "child2", "child3"],
  "operation": "apply_json_patch"
}
```

### Pydantic Validation Error
Returns **full Pydantic schema**:
```json
{
  "error": "Document validation failed: N error(s)",
  "hint": "Document must conform to Doc schema",
  "details": [{"loc": ["field"], "msg": "error message", "type": "value_error"}],
  "schema": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "label": {"type": "string"},
      "type": {"type": "string", "enum": ["Doc"]},
      "metadata": {"type": "object"},
      "children": {"type": "object", "additionalProperties": { "$ref": "#/definitions/Doc" }}
    },
    "required": ["id", "label"]
  },
  "operation": "apply_json_patch"
}
```

## File Management

**Before modification:**
- File: read-only/archived
- State: protected from direct changes

**During modification:**
- Remove read-only/archive attributes
- Exclusive write lock
- Apply changes
- Close and flush

**After modification:**
- Set read-only/archive attributes
- File: protected again

## Usage Example

```python
from knowledge_tools.api import apply_json_patch

# Single patch operation
error = apply_json_patch(
    document_path="/path/to/document.json",
    json_patch='[{"op": "add", "path": "/children/new", "value": {"id": "new", "label": "New Node", "type": "Doc"}}]'
)

if error is None:
    print("Document updated successfully")
else:
    print(f"Error: {error.error}")
    if error.hint:
        print(f"Hint: {error.hint}")
    if error.example:
        print(f"Example: {error.example}")
    if error.existing_children:
        print(f"Available children: {error.existing_children}")
    if error.schema:
        print(f"Schema: {error.schema}")
```

## Type Extensibility

The `type` field is the anchor for extensibility. Future document types:

```json
{
  "id": "unique",
  "label": "Extended Node",
  "type": "CustomType",
  "metadata": { "custom_field": "value" }
}
```

Requires:
1. New Pydantic model extending `Doc`
2. Updated validation logic
3. New type in schema

---

**Version:** 0.1 | **Status:** PoC

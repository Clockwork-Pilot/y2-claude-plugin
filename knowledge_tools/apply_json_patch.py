#!/usr/bin/env python3
"""Document API - JSON Patch operations with validation and error handling."""

import json
import os
import stat
from pathlib import Path
from typing import Any, Dict, List, Optional
from jsonpatch import JsonPatch, JsonPatchException
from pydantic import ValidationError

from knowledge_tools.doc_model import Doc
from knowledge_tools.response_model import ApplyPatchErrorResponse


def apply_json_patch(document_path: str, json_patch: str) -> Optional[ApplyPatchErrorResponse]:
    """
    Apply JSON Patch to document file with validation and error handling.

    Process:
    1. Read document from file
    2. Parse and validate JSON Patch
    3. Apply patch in memory
    4. Validate against Pydantic Doc schema
    5. Write changes with file protection

    Args:
        document_path: Path to document JSON file
        json_patch: JSON Patch operations as JSON string

    Returns:
        Dict with success status, data/error, and operation metadata
    """
    operation = "apply_json_patch"
    doc_path = Path(document_path)

    # 1. Read document
    if not doc_path.exists():
        return ApplyPatchErrorResponse(
            error=f"Document not found: {document_path}",
            operation=operation
        )

    try:
        doc_content = doc_path.read_text(encoding="utf-8")
        doc_dict = json.loads(doc_content)
    except (json.JSONDecodeError, IOError) as e:
        return ApplyPatchErrorResponse(
            error=f"Failed to read document: {str(e)}",
            operation=operation
        )

    # 2. Parse JSON Patch
    try:
        patch_ops = json.loads(json_patch)
        if not isinstance(patch_ops, list):
            raise ValueError("JSON Patch must be an array of operations")
    except (json.JSONDecodeError, ValueError) as e:
        return _error_json_patch_syntax(str(e), operation)

    # 3. Create JsonPatch object
    try:
        patch = JsonPatch(patch_ops)
    except Exception as e:
        return _error_json_patch_syntax(str(e), operation)

    # 4. Apply patch in memory
    try:
        patched_dict = patch.apply(doc_dict)
    except Exception as e:
        return _error_path_not_found(str(e), doc_dict, operation)

    # 5. Validate against Pydantic
    try:
        validated_doc = Doc(**patched_dict)
        patched_dict = json.loads(validated_doc.model_dump_json(exclude_none=True))
    except ValidationError as e:
        return _error_pydantic_validation(e, operation)
    except Exception as e:
        return ApplyPatchErrorResponse(
            error=f"Failed to validate document: {str(e)}",
            operation=operation
        )

    # 6. Write to file with protection
    try:
        _write_protected_document(doc_path, patched_dict)
    except Exception as e:
        return ApplyPatchErrorResponse(
            error=f"Failed to write document: {str(e)}",
            operation=operation
        )

    return None


def _error_json_patch_syntax(error: str, operation: str) -> ApplyPatchErrorResponse:
    """Return error for JSON Patch syntax errors with example."""
    return ApplyPatchErrorResponse(
        error=f"Invalid JSON Patch syntax: {error}",
        hint="JSON Patch must be valid JSON array of operations",
        example=[
            {
                "op": "add",
                "path": "/children/new_id",
                "value": {
                    "id": "new_id",
                    "label": "New Node",
                    "type": "Doc",
                    "metadata": {}
                }
            },
            {
                "op": "replace",
                "path": "/label",
                "value": "Updated Label"
            },
            {
                "op": "remove",
                "path": "/children/old_id"
            }
        ],
        operation=operation
    )


def _error_path_not_found(error: str, doc_dict: Dict, operation: str) -> ApplyPatchErrorResponse:
    """Return error for path not found with parent suggestions."""
    error_str = str(error)

    # Try to extract path from error message
    parent_path = None
    existing_children = []

    if "path" in error_str.lower():
        # Try common error patterns
        if "does not exist" in error_str:
            parts = error_str.split("'")
            if len(parts) >= 2:
                failed_path = parts[1]
                # Get parent path
                if "/" in failed_path:
                    parent_path = "/".join(failed_path.split("/")[:-1])
                    # Get existing children at parent
                    try:
                        parent_obj = _get_path_value(doc_dict, parent_path)
                        if isinstance(parent_obj, dict):
                            existing_children = list(parent_obj.keys())
                    except (KeyError, ValueError):
                        pass

    return ApplyPatchErrorResponse(
        error=f"Path not found: {error}",
        hint="Check parent path and available children",
        parent_path=parent_path,
        existing_children=existing_children if existing_children else None,
        operation=operation
    )


def _error_pydantic_validation(validation_error: ValidationError, operation: str) -> ApplyPatchErrorResponse:
    """Return error for Pydantic validation with schema."""
    schema = Doc.model_json_schema()
    schema_str = json.dumps(schema, indent=2)

    hint = (
        "Expected Pydantic schema:\n"
        f"{schema_str}"
    )

    return ApplyPatchErrorResponse(
        error=f"Document validation failed: {validation_error.error_count()} error(s)",
        hint=hint,
        details=validation_error.errors(),
        operation=operation
    )


def _get_path_value(doc: Dict, path: str) -> Any:
    """Get value at JSON Pointer path."""
    if path == "" or path == "/":
        return doc

    parts = path.lstrip("/").split("/")
    current = doc

    for part in parts:
        if isinstance(current, dict):
            current = current[part]
        else:
            raise ValueError(f"Cannot traverse {part} on non-dict")

    return current


def _write_protected_document(doc_path: Path, doc_dict: Dict) -> None:
    """Write document to file with protection workflow."""
    # Remove read-only/archive attributes
    if doc_path.exists():
        current_mode = doc_path.stat().st_mode
        doc_path.chmod(current_mode | stat.S_IWUSR | stat.S_IWGRP)

    # Ensure parent directory exists
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    # Write with exclusive lock semantics
    try:
        # Write to temp file first for atomicity
        temp_path = doc_path.with_suffix(doc_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(doc_dict, indent=2), encoding="utf-8")

        # Atomic rename
        temp_path.replace(doc_path)
    finally:
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()

    # Set read-only/archive attributes
    current_mode = doc_path.stat().st_mode
    doc_path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

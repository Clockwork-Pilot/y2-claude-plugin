#!/usr/bin/env python3
"""Document API - JSON Patch operations with validation and error handling."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from jsonpatch import JsonPatch, JsonPatchException
from pydantic import ValidationError

from .models import Doc, MODEL_REGISTRY
from .common.response import ApplyPatchErrorResponse
from .common.file_ops import write_protected_file
from .common.render import render


def apply_json_patch(document_path: str, json_patch: Optional[str] = None, create: bool = False) -> Optional[ApplyPatchErrorResponse]:
    """
    Apply JSON Patch to document file with validation and automatic markdown rendering.

    If json_patch is None, only re-renders the document without patching.

    Process:
    1. Read document from file (or create if create=True and document doesn't exist)
    2. If json_patch provided:
       a. Parse and validate JSON Patch (RFC 6902)
       b. Apply patch in memory
       c. Validate against Pydantic Doc schema
       d. Write changes with file protection
    3. Render markdown representation to .md file

    Args:
        document_path: Path to document JSON file
        json_patch: JSON Patch operations as JSON string (RFC 6902 format). If None, only re-renders.
        create: If True, create document with patch as initial state (default: False)

    Returns:
        None on success, ApplyPatchErrorResponse on error
    """
    operation = "apply_json_patch"
    doc_path = Path(document_path)

    # 1. Read document or initialize empty
    if not doc_path.exists():
        if not create:
            return ApplyPatchErrorResponse(
                error=f"Document not found: {document_path}",
                operation=operation,
                hint="Use create=True flag to create new documents"
            )
        # Start with empty doc dict for creation
        doc_dict = {}
    else:
        try:
            doc_content = doc_path.read_text(encoding="utf-8")
            doc_dict = json.loads(doc_content)
        except (json.JSONDecodeError, IOError) as e:
            return ApplyPatchErrorResponse(
            error=f"Failed to read document: {str(e)}",
            operation=operation
        )

    # If no patch provided, skip patching and go straight to render
    if json_patch is None:
        patched_dict = doc_dict
    else:
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

    # 5. Validate against correct model type
    try:
        model_type = patched_dict.get("type", "Doc")
        ModelClass = MODEL_REGISTRY.get(model_type)

        if not ModelClass:
            return ApplyPatchErrorResponse(
                error=f"Unknown model type: {model_type}",
                operation=operation
            )

        validated_model = ModelClass(**patched_dict)
        patched_dict = json.loads(validated_model.model_dump_json(exclude_none=True))
    except ValidationError as e:
        return _error_pydantic_validation(e, operation)
    except Exception as e:
        return ApplyPatchErrorResponse(
            error=f"Failed to validate document: {str(e)}",
            operation=operation
        )

    # 6. Write to file with protection
    try:
        write_protected_file(doc_path, json.dumps(patched_dict, indent=2))
    except Exception as e:
        return ApplyPatchErrorResponse(
            error=f"Failed to write document: {str(e)}",
            operation=operation
        )

    # 7. Render markdown representation
    try:
        render(str(doc_path))
    except Exception as e:
        # Rendering failure doesn't fail the patch operation
        # Just silently continue - the JSON was updated successfully
        pass

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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python3 apply_json_patch.py [--create] <document_path> [json_patch]",
            file=sys.stderr,
        )
        print("\nExamples:", file=sys.stderr)
        print(
            '  python3 apply_json_patch.py doc.json \'[{"op": "replace", "path": "/label", "value": "new"}]\'',
            file=sys.stderr,
        )
        print(
            '  python3 apply_json_patch.py --create doc.json \'[{"op": "add", "path": "/id", "value": "doc1"}]\'',
            file=sys.stderr,
        )
        print(
            '  python3 apply_json_patch.py doc.json  # Re-render only',
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse arguments
    create = False
    json_patch = None

    if sys.argv[1] == "--create":
        create = True
        document_path = sys.argv[2]
        if len(sys.argv) > 3:
            json_patch = sys.argv[3]
    else:
        document_path = sys.argv[1]
        if len(sys.argv) > 2:
            json_patch = sys.argv[2]

    result = apply_json_patch(document_path, json_patch, create=create)

    if result:
        # Error occurred
        error_data = result.model_dump(exclude_none=True)
        print(json.dumps(error_data, indent=2))
        sys.exit(1)
    else:
        # Success
        if create:
            action = "Created"
        elif json_patch is not None:
            action = "Patched"
        else:
            action = "Re-rendered"
        print(f"✓ {action} {document_path}")
        sys.exit(0)

#!/usr/bin/env python3
"""Internal markdown rendering for knowledge documents.

PRIVATE MODULE: Not intended for direct use. Rendering is automatic when patches are applied.
Converts Doc JSON structure to formatted markdown with proper headings,
lists, and hierarchical formatting. Saves to .md file with file protection.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .file_ops import write_protected_file


def _render_doc_internal(document_path: str) -> Optional[str]:
    """
    INTERNAL ONLY: Render a knowledge document as markdown-like text and save to .md file.

    This function is called automatically by apply_json_patch and should not be used directly.

    Args:
        document_path: Path to Doc JSON file

    Returns:
        Formatted markdown string, or None if document not found
    """
    doc_path = Path(document_path)

    if not doc_path.exists():
        print(f"Error: Document not found: {document_path}", file=sys.stderr)
        return None

    try:
        doc_content = doc_path.read_text(encoding="utf-8")
        doc_dict = json.loads(doc_content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading document: {str(e)}", file=sys.stderr)
        return None

    lines = []
    _render_node(doc_dict, lines, level=1)
    markdown_content = "\n".join(lines)

    # Save to .md file with protection
    md_path = doc_path.with_suffix(".md")
    write_protected_file(md_path, markdown_content)

    return markdown_content


def _render_node(node: Dict[str, Any], lines: list, level: int = 1) -> None:
    """Recursively render a Doc node and its children.

    Args:
        node: Doc node dictionary
        lines: Output lines list
        level: Current heading level (1-6)
    """
    # Add heading for this node
    label = node.get("label", "Untitled")
    heading = "#" * level + " " + label
    lines.append(heading)
    lines.append("")

    # Add metadata information (skip opts field - non-displayable)
    metadata = node.get("metadata", {})
    if metadata:
        lines.extend(_render_metadata(metadata))
        lines.append("")

    # Add children as list or recursively (sorted by render_priority)
    children = node.get("children", {})
    if children:
        # Sort children: render_priority=true first, then others
        sorted_children = _sort_children_by_priority(children)

        if level >= 5:
            # For deep nesting, use bullet list instead of more headings
            lines.append("**Sections:**")
            lines.append("")
            for child_id, child_node in sorted_children:
                child_label = child_node.get("label", child_id)
                lines.append(f"- {child_label}")
            lines.append("")
        else:
            # Use heading levels for shallow nesting
            for child_id, child_node in sorted_children:
                _render_node(child_node, lines, level=level + 1)


def _sort_children_by_priority(children: Dict[str, Any]) -> list:
    """Sort children by render_priority (true first, then false/absent).

    Args:
        children: Dictionary of child nodes

    Returns:
        List of (child_id, child_node) tuples sorted by priority
    """
    def get_priority(item: tuple) -> bool:
        child_id, child_node = item
        opts = child_node.get("opts", {})
        return not opts.get("render_priority", False)  # False (priority) comes first

    return sorted(children.items(), key=get_priority)


def _render_metadata(metadata: Dict[str, Any]) -> list:
    """Render metadata fields as formatted text.

    Args:
        metadata: Metadata dictionary

    Returns:
        List of formatted lines
    """
    lines = []

    for key, value in metadata.items():
        # Skip rendering "description" key label, just render the value
        if key == "description":
            if value:
                lines.append(str(value))
        elif isinstance(value, list):
            lines.append(f"**{_format_key(key)}:**")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, dict):
            lines.append(f"**{_format_key(key)}:**")
            for sub_key, sub_value in value.items():
                lines.append(f"  - {_format_key(sub_key)}: {sub_value}")
        elif value:
            # Only add non-empty values
            lines.append(f"**{_format_key(key)}:** {value}")

    return lines


def _format_key(key: str) -> str:
    """Format snake_case key to Title Case.

    Args:
        key: Input key string

    Returns:
        Formatted key
    """
    return key.replace("_", " ").title()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_doc.py <path_to_doc.json>", file=sys.stderr)
        sys.exit(1)

    doc_path = sys.argv[1]
    result = render_doc(doc_path)

    if result:
        print(result)
        sys.exit(0)
    else:
        sys.exit(1)

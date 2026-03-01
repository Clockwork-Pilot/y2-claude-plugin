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

    # Insert TOC if enabled in opts
    opts = doc_dict.get("opts", {})
    if opts.get("render_toc", False):
        toc_lines = _generate_toc(doc_dict)
        if toc_lines:
            lines.insert(1, "")
            lines.insert(2, "## Table of Contents")
            lines.insert(3, "")
            lines[4:4] = toc_lines
            lines.insert(4 + len(toc_lines), "")

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


def _generate_toc(node: Dict[str, Any], level: int = 1, parent_label: str = "") -> list:
    """Generate table of contents lines from document structure.

    Args:
        node: Doc node dictionary
        level: Current heading level (1-6)
        parent_label: Label of parent node for context

    Returns:
        List of TOC lines
    """
    toc_lines = []

    children = node.get("children", {})
    if children:
        sorted_children = _sort_children_by_priority(children)

        for child_id, child_node in sorted_children:
            label = child_node.get("label", child_id)
            anchor = label.lower()
            anchor = "".join(c if c.isalnum() else "-" for c in anchor).strip("-")

            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{label}](#{anchor})")

            # Recursively add child's children
            child_toc = _generate_toc(child_node, level + 1, label)
            toc_lines.extend(child_toc)

    return toc_lines


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
    description = metadata.get("description")
    code = metadata.get("code")
    first_field = True

    if description:
        lines.append(str(description))
        first_field = False

    if code:
        if not first_field:
            lines.append("")
        lines.append("```")
        lines.append(str(code))
        lines.append("```")
        first_field = False

    for key, value in metadata.items():
        if key in ("description", "code"):
            continue

        # Add empty line before each field (except right after description)
        if not first_field:
            lines.append("")
        first_field = False

        if isinstance(value, list):
            lines.append(f"**{_format_key(key)}:**")
            # Check if list items already start with number pattern (1., 2., etc.)
            import re
            is_ordered = all(isinstance(item, str) and re.match(r'^\d+\.\s', item) for item in value)
            for item in value:
                if is_ordered:
                    # Already numbered, render as-is
                    lines.append(f"  {item}")
                else:
                    # Bullet list
                    lines.append(f"  - {item}")
        elif isinstance(value, dict):
            lines.append(f"**{_format_key(key)}:**")
            for sub_key, sub_value in value.items():
                lines.append(f"  - {_format_key(sub_key)}: {sub_value}")
        elif value:
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
        print("Usage: _render_doc.py <path_to_doc.json>", file=sys.stderr)
        sys.exit(1)

    doc_path = sys.argv[1]
    result = _render_doc_internal(doc_path)

    if result:
        print(result)
        sys.exit(0)
    else:
        sys.exit(1)

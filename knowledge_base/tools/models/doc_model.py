#!/usr/bin/env python3
"""Document model with self-contained rendering logic."""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Literal

from pydantic import BaseModel

from .base_model import RenderableModel
from ..common.file_ops import write_protected_file


class Opts(BaseModel):
    """Non-displayable options for document rendering behavior."""

    render_priority: bool = False
    render_toc: bool = False


class Doc(RenderableModel):
    """Document node with type-based extensibility and optional children."""

    id: str
    label: str
    type: Literal["Doc"] = "Doc"
    metadata: Dict[str, Any] = {}
    opts: Optional[Opts] = None
    children: Optional[Dict[str, "Doc"]] = None

    def render(self) -> str:
        """Render Doc to markdown string and save to .md file.

        Returns:
            Formatted markdown string representation.
        """
        doc_dict = json.loads(self.model_dump_json(exclude_none=True))
        lines = []
        self._render_node(doc_dict, lines, level=1)

        # Insert TOC if enabled in opts
        opts = doc_dict.get("opts", {})
        if opts.get("render_toc", False):
            toc_lines = self._generate_toc(doc_dict)
            if toc_lines:
                lines.insert(1, "")
                lines.insert(2, "## Table of Contents")
                lines.insert(3, "")
                lines[4:4] = toc_lines
                lines.insert(4 + len(toc_lines), "")

        markdown_content = "\n".join(lines)
        return markdown_content

    def save_rendered(self, document_path: str) -> Optional[str]:
        """Render and save to .md file with protection."""
        try:
            markdown = self.render()
            doc_path = Path(document_path)
            md_path = doc_path.with_suffix(".md")
            write_protected_file(md_path, markdown)
            return markdown
        except Exception as e:
            print(f"Error rendering document: {str(e)}", file=sys.stderr)
            return None

    @staticmethod
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
            lines.extend(Doc._render_metadata(metadata))
            lines.append("")

        # Add children as list or recursively (sorted by render_priority)
        children = node.get("children", {})
        if children:
            # Sort children: render_priority=true first, then others
            sorted_children = Doc._sort_children_by_priority(children)

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
                    Doc._render_node(child_node, lines, level=level + 1)

    @staticmethod
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
            sorted_children = Doc._sort_children_by_priority(children)

            for child_id, child_node in sorted_children:
                label = child_node.get("label", child_id)
                anchor = label.lower()
                anchor = "".join(c if c.isalnum() else "-" for c in anchor).strip("-")

                indent = "  " * (level - 1)
                toc_lines.append(f"{indent}- [{label}](#{anchor})")

                # Recursively add child's children
                child_toc = Doc._generate_toc(child_node, level + 1, label)
                toc_lines.extend(child_toc)

        return toc_lines

    @staticmethod
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

    @staticmethod
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
                lines.append(f"**{Doc._format_key(key)}:**")
                # Check if list items already start with number pattern (1., 2., etc.)
                is_ordered = all(
                    isinstance(item, str) and re.match(r"^\d+\.\s", item)
                    for item in value
                )
                for item in value:
                    if is_ordered:
                        # Already numbered, render as-is
                        lines.append(f"  {item}")
                    else:
                        # Bullet list
                        lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"**{Doc._format_key(key)}:**")
                for sub_key, sub_value in value.items():
                    lines.append(f"  - {Doc._format_key(sub_key)}: {sub_value}")
            elif value:
                lines.append(f"**{Doc._format_key(key)}:** {value}")

        return lines

    @staticmethod
    def _format_key(key: str) -> str:
        """Format snake_case key to Title Case.

        Args:
            key: Input key string

        Returns:
            Formatted key
        """
        return key.replace("_", " ").title()


Doc.model_rebuild()

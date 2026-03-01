"""Shared utilities for knowledge base tools."""

from .file_ops import write_protected_file
from ._render_doc import _render_doc_internal

__all__ = [
    "write_protected_file",
    "_render_doc_internal",
]

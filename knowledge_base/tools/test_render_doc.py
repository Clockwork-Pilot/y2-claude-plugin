#!/usr/bin/env python3
"""Tests for render_doc functionality."""

import json
import tempfile
from pathlib import Path
import pytest

from common._render_doc import _render_doc_internal


class TestRenderDoc:
    """Test _render_doc_internal function (internal API)."""

    def test_render_document_with_structure(self):
        """Test rendering a document with metadata and nested structure."""
        doc = {
            "id": "test",
            "label": "Test Document",
            "type": "Doc",
            "metadata": {
                "description": "A test document",
                "version": "1.0"
            },
            "children": {
                "section1": {
                    "id": "section1",
                    "label": "First Section",
                    "type": "Doc",
                    "metadata": {"status": "complete"}
                }
            }
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(doc, f)
            temp_path = f.name

        try:
            result = _render_doc_internal(temp_path)

            assert result is not None
            assert "# Test Document" in result
            assert "## First Section" in result
            assert "A test document" in result
            assert "1.0" in result
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

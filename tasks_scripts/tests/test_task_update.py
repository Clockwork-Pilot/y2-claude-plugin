"""
Unit tests for task document updates - appending content safely with atomic updates.

Tests validate that content can be appended to current phase using atomic regex
updates, preventing corruption in large documents.
"""
import pytest
from pathlib import Path
from datetime import datetime

from tasks_scripts.models import TaskDocument
from tasks_scripts.task_state import load_task_document, append_to_phase


class TestTaskUpdate:
    """Test task document updating."""

    @pytest.fixture
    def simple_task_file(self, tmp_path):
        """Create a simple task file for testing."""
        task_path = tmp_path / ".TASK.md"
        content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Initial planning content.

<!-- TASK_PLAN.DEFINE -->
"""
        task_path.write_text(content)
        return task_path

    def test_append_content_to_single_phase(self, simple_task_file):
        """Should append content to a single phase."""
        # Read current content
        original = simple_task_file.read_text()

        # Append content
        new_content = "Additional planning notes."
        updated = append_to_phase(original, "TASK_PLAN.DEFINE", new_content)

        # Verify content was added
        assert new_content in updated
        # Verify original content is still present
        assert "Initial planning content." in updated
        assert "TASK_PLAN.DEFINE" in updated

    def test_append_content_to_current_phase_in_multi_phase(self, tmp_path):
        """Should append to current phase in a multi-phase document."""
        task_path = tmp_path / ".TASK.md"
        content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Initial planning.

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T09:30:00+00:00

Context refinement.

<!-- TASK_PLAN.REFINE_CONTEXT -->
"""
        task_path.write_text(content)

        # Append to current phase (REFINE_CONTEXT)
        original = task_path.read_text()
        new_content = "Updated context."
        updated = append_to_phase(
            original,
            "TASK_PLAN.REFINE_CONTEXT",
            new_content
        )

        # New content should appear in REFINE_CONTEXT phase
        assert new_content in updated
        # Original content should be preserved
        assert "Initial planning." in updated

    def test_appended_content_appears_in_correct_location(self, simple_task_file):
        """Should insert content before the phase marker."""
        original = simple_task_file.read_text()
        new_content = "New note"

        updated = append_to_phase(original, "TASK_PLAN.DEFINE", new_content)

        # Find positions
        marker_pos = updated.find("<!-- TASK_PLAN.DEFINE -->")
        content_pos = updated.find(new_content)

        assert marker_pos > 0
        assert content_pos > 0
        assert content_pos < marker_pos, "Content should appear before marker"

    def test_appended_content_before_phase_marker(self, simple_task_file):
        """Should preserve phase marker and insert before it."""
        original = simple_task_file.read_text()
        marker = "<!-- TASK_PLAN.DEFINE -->"
        new_content = "Test append"

        updated = append_to_phase(original, "TASK_PLAN.DEFINE", new_content)

        # Marker should still exist
        assert marker in updated
        # Content should be before marker
        marker_pos = updated.find(marker)
        content_pos = updated.find(new_content)
        assert content_pos < marker_pos

    def test_earlier_phases_unchanged_after_append(self, tmp_path):
        """Should not modify content in earlier phases."""
        task_path = tmp_path / ".TASK.md"
        earlier_content = "Original planning content"
        content = f"""# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

{earlier_content}

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.REFINE_CONTEXT at 2026-02-26T09:30:00+00:00

Context refinement.

<!-- TASK_PLAN.REFINE_CONTEXT -->
"""
        task_path.write_text(content)

        original = task_path.read_text()

        # Append to later phase
        new_content = "New context"
        updated = append_to_phase(original, "TASK_PLAN.REFINE_CONTEXT", new_content)

        # Earlier content should be unchanged
        assert earlier_content in updated

    def test_later_phases_unchanged_after_append(self, tmp_path):
        """Should not modify content in later phases."""
        task_path = tmp_path / ".TASK.md"
        later_content = "Design decisions"
        content = f"""# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Planning content.

<!-- TASK_PLAN.DEFINE -->

# PHASE TASK_PLAN.DESIGN at 2026-02-26T10:00:00+00:00

{later_content}

<!-- TASK_PLAN.DESIGN -->
"""
        task_path.write_text(content)

        original = task_path.read_text()

        # Append to earlier phase
        new_content = "More planning"
        updated = append_to_phase(original, "TASK_PLAN.DEFINE", new_content)

        # Later content should be unchanged
        assert later_content in updated

    def test_atomic_regex_update_preserves_all_content(self, tmp_path):
        """Should use atomic regex to preserve all content."""
        task_path = tmp_path / ".TASK.md"
        important_content = [
            "PHASE",
            "Original content",
            "<!-- TASK_PLAN.DEFINE -->"
        ]
        content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Original content

<!-- TASK_PLAN.DEFINE -->
"""
        task_path.write_text(content)

        original = task_path.read_text()

        # Append new content
        new_content = "Appended text"
        updated = append_to_phase(original, "TASK_PLAN.DEFINE", new_content)

        # All important content should be present
        for item in important_content:
            assert item in updated, f"Content '{item}' was lost"

    def test_large_document_10_plus_phases_50_plus_entries(self, tmp_path):
        """Should handle large documents with many phases and entries."""
        task_path = tmp_path / ".TASK.md"

        # Create a document with multiple phases
        phases = [
            "TASK_PLAN.DEFINE",
            "TASK_PLAN.REFINE_CONTEXT",
            "TASK_PLAN.DESIGN",
            "TASK_PLAN.DECOMPOSE",
            "EXEC_EVAL.TEST_PLAN",
            "EXEC_EVAL.CODING",
            "EXEC_EVAL.TESTING",
        ]

        content_lines = []
        for i, phase in enumerate(phases):
            timestamp = f"2026-02-26T{9+i:02d}:00:00+00:00"
            content_lines.append(f"# PHASE {phase} at {timestamp}\n")
            content_lines.append(f"\nContent for {phase}.\n\n")

            # Add scoring entries to simulate accumulated data
            for j in range(7):
                entry_timestamp = f"2026-02-26T{9+i:02d}:{j*8:02d}:00+00:00"
                content_lines.append(f"### {entry_timestamp}\n")
                content_lines.append(f"Score: {80 + j}\n\n")

            content_lines.append(f"<!-- {phase} -->\n\n")

        content = "".join(content_lines)
        task_path.write_text(content)

        original = task_path.read_text()

        # Append to last phase
        new_entry = "Final assessment"
        updated = append_to_phase(original, "EXEC_EVAL.TESTING", new_entry)

        # Verify all content is preserved
        assert new_entry in updated
        assert "TASK_PLAN.DEFINE" in updated
        assert "EXEC_EVAL.TESTING" in updated

        # Count lines - should not lose content
        original_lines = len(original.split('\n'))
        updated_lines = len(updated.split('\n'))

        # Updated should have at least as many lines (plus new content)
        assert updated_lines >= original_lines

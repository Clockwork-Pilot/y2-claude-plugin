"""
Unit tests for task archival - moving completed tasks to history with naming convention.

Tests validate that completed tasks can be archived with standardized naming,
auto-incrementing IDs, and GitHub issue ID support.
"""
import pytest
from pathlib import Path
from datetime import datetime

from tasks_scripts.models import TaskDocument
from tasks_scripts.task_state import load_task_document
from tasks_scripts.task_archive import archive_task, get_next_task_id


@pytest.fixture
def completed_task_file(tmp_path):
    """Create a completed task file for archival."""
    task_path = tmp_path / ".TASK.md"
    content = """# PHASE TASK_PLAN.DEFINE at 2026-02-26T09:00:00+00:00

Task planning completed.

<!-- TASK_PLAN.DEFINE -->

# PHASE EXEC_EVAL.TESTING at 2026-02-26T17:00:00+00:00

All tests passing. Task complete.

<!-- EXEC_EVAL.TESTING -->
"""
    task_path.write_text(content)
    return task_path


class TestTaskArchive:
    """Test task archival functionality."""

    def test_archive_moves_to_tasks_history_directory(self, completed_task_file, tmp_path):
        """Should move task to .tasks_history directory."""
        archived_path = archive_task(str(completed_task_file))

        # File should be in .tasks_history directory
        assert ".tasks_history" in archived_path
        assert Path(archived_path).exists()

        # Original file should be gone
        assert not completed_task_file.exists()

    def test_archive_generates_auto_incremented_task_id(self, tmp_path):
        """Should generate auto-incremented task IDs."""
        # Create first task in main directory
        task1_path = tmp_path / ".TASK.md"
        task1_path.write_text("""# PHASE EXEC_EVAL.TESTING at 2026-02-26T17:00:00+00:00
All tests passing.
<!-- EXEC_EVAL.TESTING -->
""")

        # Archive first task
        path1 = archive_task(str(task1_path))

        # Create second task in main directory (first was moved)
        task2_path = tmp_path / ".TASK.md"
        task2_path.write_text("""# PHASE EXEC_EVAL.TESTING at 2026-02-26T17:00:00+00:00
All tests passing.
<!-- EXEC_EVAL.TESTING -->
""")

        # Archive second task (should use same .tasks_history)
        path2 = archive_task(str(task2_path))

        # Extract IDs from paths
        id1 = Path(path1).name.split("_")[1]  # TASK_##### format
        id2 = Path(path2).name.split("_")[1]

        # IDs should be sequential
        assert int(id2) == int(id1) + 1

    def test_archive_uses_github_issue_id_when_specified(self, completed_task_file):
        """Should use GitHub issue ID when specified."""
        github_id = 345345

        archived_path = archive_task(
            str(completed_task_file),
            is_github_issue=True,
            github_id=github_id
        )

        filename = Path(archived_path).name
        assert f"GITHUB_ISSUE_{github_id:05d}" in filename

    def test_archive_adds_failure_prefix_on_failure(self, completed_task_file):
        """Should add __FAILURE__ prefix when task failed."""
        archived_path = archive_task(str(completed_task_file), failure=True)

        filename = Path(archived_path).name
        assert "__FAILURE__" in filename

    def test_archive_naming_format_task_id(self, completed_task_file):
        """Should use TASK_##### format for auto-incremented names."""
        archived_path = archive_task(str(completed_task_file))

        filename = Path(archived_path).name
        # Should match pattern: TASK_#####_description.md
        assert filename.startswith("TASK_")
        assert filename.endswith(".md")

        # Extract ID part
        parts = filename.split("_")
        assert len(parts) >= 2
        assert parts[1].replace(".md", "").isdigit()

    def test_archive_naming_format_github_issue_id(self, completed_task_file):
        """Should use GITHUB_ISSUE_##### format when appropriate."""
        archived_path = archive_task(
            str(completed_task_file),
            is_github_issue=True,
            github_id=12345
        )

        filename = Path(archived_path).name
        assert filename.startswith("GITHUB_ISSUE_")
        assert "12345" in filename

    def test_archive_failure_naming_includes_failure_prefix(self, completed_task_file):
        """Should include __FAILURE__ prefix in failed task names."""
        archived_path = archive_task(str(completed_task_file), failure=True)

        filename = Path(archived_path).name
        # Should be TASK_#####__FAILURE__description.md or similar
        assert "__FAILURE__" in filename

    def test_archive_creates_directory_if_missing(self, completed_task_file, tmp_path):
        """Should create .tasks_history directory if it doesn't exist."""
        # Directory shouldn't exist yet
        history_dir = completed_task_file.parent / ".tasks_history"
        assert not history_dir.exists()

        archive_task(str(completed_task_file))

        # Should be created
        assert history_dir.exists()
        assert history_dir.is_dir()

    def test_archive_case_converts_description_to_uppercase(self, completed_task_file):
        """Should convert description to uppercase with underscores."""
        archived_path = archive_task(str(completed_task_file))

        filename = Path(archived_path).name
        # Description part should be uppercase
        # Format: TASK_#####_DESCRIPTION.md
        parts = filename.replace(".md", "").split("_")
        # Everything after the ID should be uppercase
        if len(parts) > 2:
            description = "_".join(parts[2:])
            assert description == description.upper()

    def test_get_next_task_id_starts_at_1(self, tmp_path):
        """Should start at ID 1 for empty directory."""
        history_dir = tmp_path / ".tasks_history"
        history_dir.mkdir()

        next_id = get_next_task_id(str(history_dir))
        assert next_id == 1

    def test_get_next_task_id_increments(self, tmp_path):
        """Should increment based on existing files."""
        history_dir = tmp_path / ".tasks_history"
        history_dir.mkdir()

        # Create some task files
        (history_dir / "TASK_00001_FIRST.md").write_text("task 1")
        (history_dir / "TASK_00005_FIFTH.md").write_text("task 5")
        (history_dir / "TASK_00003_THIRD.md").write_text("task 3")

        next_id = get_next_task_id(str(history_dir))
        # Should return max(IDs) + 1
        assert next_id == 6

    def test_archive_returns_archived_path(self, completed_task_file):
        """Should return the path to archived file."""
        archived_path = archive_task(str(completed_task_file))

        # Should be a string path
        assert isinstance(archived_path, str)

        # Path should exist
        assert Path(archived_path).exists()

        # Path should contain .tasks_history
        assert ".tasks_history" in archived_path

    def test_archive_with_explicit_task_id(self, completed_task_file):
        """Should use explicit task ID when provided."""
        task_id = 999

        archived_path = archive_task(str(completed_task_file), task_id=task_id)

        filename = Path(archived_path).name
        assert f"TASK_{task_id:05d}" in filename

#!/usr/bin/env python3
"""Minimal tests for task lifecycle evolution."""

import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

# Add parent directories to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tasks_lifecycle.knowledge_models.task_model import Task, Iteration, CodeStats, TaskTestMetrics
from knowledge_tool.models import Doc
from .create_task import create_task
from .task_roll import roll_task
from .task_archive import archive_task


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    original_cwd = Path.cwd()
    import os
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)


class TestCreateTask:
    """Test task creation."""

    def test_create_task_creates_file(self, temp_dir):
        """Test that create_task creates task.json."""
        # Run create_task
        with patch("sys.exit"):
            create_task()

        task_file = temp_dir / "task.json"
        assert task_file.exists()

        # Verify structure
        with open(task_file) as f:
            data = json.load(f)

        assert data["type"] == "Task"
        assert data["id"] == "task_1"
        assert data["plan"]["type"] == "Doc"
        assert data["plan"]["id"] == "plan"
        assert "created_at" in data["plan"]["metadata"]
        assert "updated_at" in data["plan"]["metadata"]
        assert data.get("iterations") is None

    def test_create_task_fails_if_exists(self, temp_dir):
        """Test that create_task exits if file already exists."""
        # Create initial file
        task_file = temp_dir / "task.json"
        task_file.write_text("{}")

        # Attempt to create again should fail
        with pytest.raises(SystemExit) as exc_info:
            create_task()
        assert exc_info.value.code == 1


class TestTaskRoll:
    """Test task iteration rolling."""

    def test_roll_task_adds_first_iteration(self, temp_dir):
        """Test that roll_task adds first iteration."""
        # Create initial task
        with patch("sys.exit"):
            create_task()

        # Roll to first iteration
        exit_code = roll_task(skip_metrics=True)
        assert exit_code == 0

        # Verify iteration was added
        with open("task.json") as f:
            data = json.load(f)

        task = Task(**data)
        assert task.iterations is not None
        assert "iteration_1" in task.iterations

        iteration = task.iterations["iteration_1"]
        assert iteration.id == "iteration_1"
        assert "created_at" in iteration.metadata
        assert "updated_at" in iteration.metadata
        assert iteration.code_stats is not None
        assert iteration.tests_stats is not None

    def test_roll_task_increments_iteration(self, temp_dir):
        """Test that multiple rolls create sequential iterations."""
        # Create initial task
        with patch("sys.exit"):
            create_task()

        # Roll multiple times
        for i in range(3):
            exit_code = roll_task(skip_metrics=True)
            assert exit_code == 0

        # Verify all iterations exist
        with open("task.json") as f:
            data = json.load(f)

        task = Task(**data)
        assert len(task.iterations) == 3
        assert "iteration_1" in task.iterations
        assert "iteration_2" in task.iterations
        assert "iteration_3" in task.iterations

    def test_roll_task_records_metrics(self, temp_dir):
        """Test that roll_task records metrics from iterations."""
        # Create initial task
        with patch("sys.exit"):
            create_task()

        # Roll with metrics
        exit_code = roll_task(skip_metrics=True)
        assert exit_code == 0

        # Verify metrics are recorded
        with open("task.json") as f:
            data = json.load(f)

        task = Task(**data)
        iteration = task.iterations["iteration_1"]

        # Check code stats
        assert iteration.code_stats.added_lines == 0
        assert iteration.code_stats.removed_lines == 0
        assert iteration.code_stats.files_changed == 0

        # Check test stats
        assert iteration.tests_stats.passed == 0
        assert iteration.tests_stats.total == 0

    def test_roll_task_missing_file(self, temp_dir):
        """Test that roll_task fails gracefully if task.json doesn't exist."""
        exit_code = roll_task()
        assert exit_code == 1


class TestTaskArchive:
    """Test task archival."""

    def test_archive_task_moves_file(self, temp_dir):
        """Test that archive_task moves file to tasks_history/."""
        # Create and roll task
        with patch("sys.exit"):
            create_task()
        roll_task(skip_metrics=True)

        # Archive task
        exit_code = archive_task()
        assert exit_code == 0

        # Verify original file is gone
        assert not (temp_dir / "task.json").exists()

        # Verify files exist in tasks_history
        history_dir = temp_dir / "tasks_history"
        assert history_dir.exists()

        json_files = list(history_dir.glob("*-task-task_1.json"))
        md_files = list(history_dir.glob("*-task-task_1.md"))

        assert len(json_files) == 1
        assert len(md_files) == 1

    def test_archive_task_creates_markdown(self, temp_dir):
        """Test that archive_task creates markdown version."""
        # Create and roll task
        with patch("sys.exit"):
            create_task()
        roll_task(skip_metrics=True)

        # Archive task
        exit_code = archive_task()
        assert exit_code == 0

        # Verify markdown content
        md_files = list((temp_dir / "tasks_history").glob("*-task-task_1.md"))
        assert len(md_files) == 1

        md_content = md_files[0].read_text()
        assert "Task: task_1" in md_content
        assert "Plan" in md_content
        assert "Iterations" in md_content
        assert "iteration_1" in md_content

    def test_archive_task_missing_file(self, temp_dir):
        """Test that archive_task fails if task.json doesn't exist."""
        exit_code = archive_task()
        assert exit_code == 1


class TestTaskEvolution:
    """Test complete task lifecycle evolution."""

    def test_task_evolves_through_iterations(self, temp_dir):
        """Test that task document properly evolves through full lifecycle."""
        # Create task
        with patch("sys.exit"):
            create_task()

        # Load initial task
        with open("task.json") as f:
            initial = json.load(f)
        assert initial.get("iterations") is None

        # First iteration
        roll_task(skip_metrics=True)
        with open("task.json") as f:
            after_iter1 = json.load(f)
        assert "iteration_1" in after_iter1["iterations"]
        assert len(after_iter1["iterations"]) == 1

        # Second iteration
        roll_task(skip_metrics=True)
        with open("task.json") as f:
            after_iter2 = json.load(f)
        assert "iteration_1" in after_iter2["iterations"]
        assert "iteration_2" in after_iter2["iterations"]
        assert len(after_iter2["iterations"]) == 2

        # Verify model can deserialize evolved document
        task = Task(**after_iter2)
        assert task.id == "task_1"
        assert len(task.iterations) == 2
        for iter_id, iteration in task.iterations.items():
            assert isinstance(iteration, Iteration)
            assert iteration.code_stats is not None
            assert iteration.tests_stats is not None

    def test_task_renders_with_iterations(self, temp_dir):
        """Test that task renders correctly with iterations."""
        # Create task and add iterations
        with patch("sys.exit"):
            create_task()

        for i in range(2):
            roll_task(skip_metrics=True)

        # Load and render
        with open("task.json") as f:
            data = json.load(f)

        task = Task(**data)
        markdown = task.render()

        # Verify markdown contains expected sections
        assert "Task: task_1" in markdown
        assert "Plan" in markdown
        assert "Iterations" in markdown
        assert "iteration_1" in markdown
        assert "iteration_2" in markdown
        assert "Code Stats:" in markdown
        assert "Test Stats:" in markdown


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

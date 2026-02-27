"""
Task archival script.

Moves completed .TASK.md to .tasks_history/ with standardized naming convention
using auto-increment or GitHub issue IDs.
"""
import sys
import re
from pathlib import Path
from typing import Optional

from tasks_scripts.task_state import load_task_document


def get_next_task_id(history_dir: str = ".tasks_history") -> int:
    """
    Get the next auto-incremented task ID.

    Scans directory for TASK_##### files and returns max(IDs) + 1.

    Args:
        history_dir: Path to history directory

    Returns:
        Next task ID (starts at 1 if directory empty)
    """
    history_path = Path(history_dir)

    if not history_path.exists():
        return 1

    # Find all TASK_##### files
    task_pattern = re.compile(r"TASK_(\d+)")
    ids = []

    for file in history_path.glob("TASK_*"):
        match = task_pattern.search(file.name)
        if match:
            ids.append(int(match.group(1)))

    if not ids:
        return 1

    return max(ids) + 1


def archive_task(
    task_path: str = ".TASK.md",
    task_id: Optional[int] = None,
    is_github_issue: bool = False,
    github_id: Optional[int] = None,
    failure: bool = False
) -> str:
    """
    Archive a completed task to .tasks_history/ directory.

    Args:
        task_path: Path to .TASK.md file
        task_id: Explicit task ID (auto-incremented if not provided)
        is_github_issue: Whether this is a GitHub issue
        github_id: GitHub issue ID (used if is_github_issue=True)
        failure: Whether task failed (adds __FAILURE__ prefix)

    Returns:
        Path to archived file

    Raises:
        FileNotFoundError: If task file not found
        ValueError: If invalid parameters
    """
    task_path = Path(task_path)

    if not task_path.exists():
        raise FileNotFoundError(f"Task file not found: {task_path}")

    # Load task document to validate it exists
    doc = load_task_document(str(task_path))

    # Determine history directory
    history_dir = task_path.parent / ".tasks_history"
    history_dir.mkdir(parents=True, exist_ok=True)

    # Determine new filename
    if is_github_issue and github_id is not None:
        # GitHub issue format: GITHUB_ISSUE_#####
        name_prefix = f"GITHUB_ISSUE_{github_id:05d}"
    else:
        # Auto-increment format: TASK_#####
        if task_id is None:
            task_id = get_next_task_id(str(history_dir))
        name_prefix = f"TASK_{task_id:05d}"

    # Add failure prefix if needed
    if failure:
        name_prefix += "__FAILURE__"

    # Extract description from first phase or use generic
    description = "COMPLETED"
    if doc.phases:
        first_phase_content = doc.phases[0].content
        # Take first 50 chars or first line
        if first_phase_content:
            first_line = first_phase_content.split("\n")[0][:50]
            # Convert to uppercase with underscores
            description = re.sub(r"\W+", "_", first_line).upper()
            description = description.strip("_")[:50]

    # Build filename
    filename = f"{name_prefix}_{description}.md"
    archived_path = history_dir / filename

    # Move file
    task_path.rename(archived_path)

    return str(archived_path)


if __name__ == "__main__":
    try:
        task_path = sys.argv[1] if len(sys.argv) > 1 else ".TASK.md"
        task_id = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
        is_github = "--github" in sys.argv
        github_id = None

        if is_github:
            # Find --github-id argument
            try:
                idx = sys.argv.index("--github-id")
                if idx + 1 < len(sys.argv):
                    github_id = int(sys.argv[idx + 1])
            except (ValueError, IndexError):
                pass

        failure = "--failure" in sys.argv

        archived_path = archive_task(
            task_path,
            task_id=task_id,
            is_github_issue=is_github,
            github_id=github_id,
            failure=failure
        )

        print(f"Task archived to: {archived_path}")
        sys.exit(0)

    except Exception as e:
        print(f"Error archiving task: {e}", file=sys.stderr)
        sys.exit(1)

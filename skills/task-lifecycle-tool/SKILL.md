---
name: task-lifecycle-tool
description: Task lifecycle knowledge document management. `task.json` is the canonical task document; `task.md` is its rendered Markdown view. Both files are protected and should not be edited directly; use `apply_json_patch.py` to update `task.json` and automatically regenerate `task.md`.
---

# Task
- **`task.json`** — canonical knowledge document used to track task progress through its lifecycle.
- **`task.md`** — auto-generated Markdown representation of `task.json`.

> ⚠️ Both files are protected (read-only). Do not edit them directly.

## Task Lifecycle
1. Create `task.json` (if it does not exist) using `create_task.py`.
2. Update the task using `apply_json_patch.py`.
3. The script automatically regenerates `task.md` after updating `task.json`.

Typical lifecycle steps:
- Create initial plan
- Add iterations
- Add feedback or progress updates

**Iteration naming convention:** `iteration_<iteration_number>` (e.g., `iteration_1`)

# Task tools
Python scripts used to manage the task lifecycle.

## Create task — `create_task.py`
Creates `task.json` in the project root if it does not already exist.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/task-lifecycle-tool/scripts/create_task.py --project-root /path/to/repo
```

> If `task.json` already exists, the script exits without modifying it.

## Update task — `apply_json_patch.py`
Update `task.json` by applying a JSON Patch (RFC 6902). This will update `task.json` and automatically regenerate `task.md`.

### Update task label (example)
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py task.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'
```

### Add a new iteration (example)
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py task.json '[{"op": "add", "path": "/children/iteration_1", "value": {"id": "iteration_1", "label": "Iteration 1", "type": "Doc", "metadata": {}}}]'
```

### Add feedback to an iteration (example)
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py task.json '[{"op": "add", "path": "/children/iteration_1/children/feedback_1", "value": {"id": "feedback_1", "label": "Feedback", "type": "Doc", "metadata": {}}}]'
```

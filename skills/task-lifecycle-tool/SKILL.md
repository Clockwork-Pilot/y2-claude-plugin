---
name: task-lifecycle-tool
description: Task lifecycle knowledge document management. `task.json` is the canonical task document; `task.md` is its rendered Markdown view. Both files are protected and should not be edited directly; use `patch_knowledge_document.py` to update `task.json` and automatically regenerate `task.md`.
---

Load knowledge-tool skill

# Task
- **`task.json`** — canonical knowledge document used to track task progress through its lifecycle.
- **`task.md`** — auto-generated Markdown representation of `task.json`.

> ⚠️ Both files are protected (read-only). Do not edit them directly.

## Task Lifecycle
- Create initial plan
- Add iterations
  **Iteration naming convention:** `iteration_<iteration_number>` (e.g., `iteration_1`)
- Add feedback or progress updates

### Create task
Create `task.json` (if it does not exist).

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/create_knowledge_document.py Task task.json
```

### Update task
Update `task.json` by applying a JSON Patch (RFC 6902). This will update `task.json` and automatically regenerate `task.md`.

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py task.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'
```

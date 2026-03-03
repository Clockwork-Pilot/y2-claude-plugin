# Task Lifecycle Knowledge Models

Task lifecycle models (Task, Iteration) defined in `task_model.py`.

## Usage

### Direct Imports (Internal)
Task lifecycle tools import models directly for internal use:
```python
from tasks_lifecycle.knowledge_models.task_model import Task, Iteration
```

### Pluggable Models (apply_json_patch)
The models folder can be used as pluggable models with knowledge_tool's apply_json_patch:
```bash
python3 -m knowledge_tool.apply_json_patch --models-path tasks_lifecycle/knowledge_models task.json '[...]'
```

The model loader automatically discovers RenderableModel subclasses in this folder.

## Structure
- `task_model.py` - Task and Iteration models with rendering methods
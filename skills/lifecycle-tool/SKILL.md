---
name: lifecycle-tool
description: task.json - lifecycle knowledge document created as read-only. Use apply_json_patch.py script to create or update it and render task.md.
---

# Create task
`python ${CLAUDE_PLUGIN_ROOT}/lifecycle_tool/task_lifecycle/cli/create_task.py`

# Apply json patch
Script uses JSON patches (RFC 6902) for manipulation with .json files.

**Syntax:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py <json_file> '[{"op": "replace", "path": "/label", "value": "New Label"}]'
```

**Examples:**
```bash
# Create or update a document
apply-json-patch task.json '[{"op": "add", "path": "/id", "value": "task1"}]'

# List available models (built-in + configured)
apply-json-patch --schemas

# Re-render existing document
apply-json-patch task.json
```

**Configure pluggable models:**
Edit `knowledge_config.yaml` in the knowledge_tool directory:
```yaml
pluggable_models_dirs:
  - ./models
  - ./custom_models
```

Or override config location with environment variable:
```bash
export KNOWLEDGE_TOOL_CONFIG_ROOT=/path/to/config
```

**Knowledge tool capabilities:**
- Updating lifecycle .json files (knowledge base)
- Rendering .md documentation from lifecycle .json files
- RFC 6902 JSON patches for document manipulation
- Automatic model discovery from pluggable_models_dirs
- Built-in models always available (Doc, Task, etc.)

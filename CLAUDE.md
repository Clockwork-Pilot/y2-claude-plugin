# Notes

## protected_files.txt

Files listed in `protected_files.txt` (root and `/knowledge_tool/`) are auto-protected (read-only) by hooks.

These are auto-generated files: `task.json`, `task.md`, `knowledge_tool.json`, `knowledge_tool.md`, etc.

To modify: remove from `protected_files.txt`, edit, then re-add if needed.

## Tools

- **Knowledge Tool**: `apply_json_patch.py` - JSON patches and markdown rendering
- **Lifecycle Tool**: `create_task.py` - Create task.json files

## Test

```bash
pytest -xvs  # 29 tests should pass
```

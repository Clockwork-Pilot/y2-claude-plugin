# Notes

## protected_files.txt

**Auto-generated file** - Do not edit manually.

Located in:
- `/project/protected_files.txt` (main project)
- `/project/knowledge_tool/protected_files.txt` (plugin root)

Files listed in `protected_files.txt` are auto-protected (read-only) by hooks.

Protected files: `task.json`, `task.md`, `knowledge_tool.json`, `knowledge_tool.md`, etc.

## Tools

- **Knowledge Tool**: `apply_json_patch.py` - JSON patches and markdown rendering
- **Lifecycle Tool**: `create_task.py` - Create task.json files

## Test

```bash
pytest -xvs  # 29 tests should pass
```

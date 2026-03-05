---
name: knowledge-tool
description: apply_json_patch.py script updates knowledge base .json files and renders its .md equivalent.
---

Script uses Json patches for manipulation with .json files.
Syntax:
`python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py doc.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'`

# Use apply_patch_json.py for:
- Updating knowledge base .json files
- Rendering .md documentation from knowledge .json files
- Json patches used for manipulation with .json files


---
name: knowledge-tool
description: Apply JSON Patch to knowledge documents and render Markdown equivalents.
---

This tool drives the knowledge document workflow by applying **RFC 6902 JSON Patch** operations to `.json` files and then automatically generating the corresponding `.md` representation.

# Knowledge documents
Knowledge documents are structured JSON files that represent various types of knowledge (tasks, docs, etc.). Each document has a corresponding Markdown file that is generated from the JSON source.

- **`xxxxxxx.json`** — is the source of truth canonical knowledge document in JSON format.
- **`xxxxxxx.md`** — auto-generated Markdown representation of `xxxxxxx.json`.

> ⚠️ Both files are protected (read-only). Do not edit them directly.

## Tool for updating knowledge documents — `apply_json_patch.py`
This script applies JSON Patch operations to a specified `.json` knowledge document, validates the result, and regenerates the corresponding `.md` file.

## Usage
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/apply_json_patch.py <doc.json> '<json-patch>'
```

## Prevent Direct updates enforcement
- `apply_json_patch` registers both files in the knowledge file registry
- Both files are protected (read-only) to prevent direct edits
- All updates must go through `apply_json_patch.py` to ensure consistency and proper rendering
- In case of Edit|Write hooks are triggered, the script will raise an error to enforce the workflow

## When to use
- Updating existing knowledge documents (tasks, docs, etc.)
- Generating or refreshing the Markdown representation
- Applying structured edits without hand-editing JSON

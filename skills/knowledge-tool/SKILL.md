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

## Prevent direct updates  Direct updates enforcement
- `patch_knowledge_document` registers both files in the knowledge file registry
- Both files are protected (read-only) to prevent direct edits
- All updates must go through `patch_knowledge_document.py` to ensure consistency and proper rendering
- In case of Edit|Write hooks are triggered, the script will raise an error to enforce the workflow

## When to use
- Updating existing knowledge documents (tasks, docs, etc.)
- Generating or refreshing the Markdown representation
- Applying structured edits without hand-editing JSON


## Tool for updating knowledge documents — `patch_knowledge_document.py`
This script applies JSON Patch operations to a specified `.json` knowledge document, validates the result, and regenerates the corresponding `.md` file.

## Usage
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py <doc.json> '<json-patch>'
```

## Tool for creating knowledge documents — `create_knowledge_document.py`
This script creates a new knowledge document of a specified model type and initializes it with default values.

## Usage
```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/create_knowledge_document.py <model_type> <document_path>
```

## Supported model types
- `Doc` — Create a basic knowledge document
- `Task` — Create a task document with a plan section
- `Iteration` — Create an iteration document

## Examples
```bash
# Create a new Doc
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/create_knowledge_document.py Doc doc.json

# Create a new Task
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/create_knowledge_document.py Task task.json
```

## Error handling
- Returns an error if the document already exists
- Returns an error if the model type is not found in the registry
- Supports both built-in models and pluggable custom models configured in `knowledge_config.yaml`

## When to use
- Creating new knowledge documents of a specific type
- Initializing document structure with metadata and default values
- Working with custom models registered in the knowledge configuration

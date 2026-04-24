---
name: knowledge_document_tools
description: Apply JSON Patch to knowledge documents tools and render Markdown equivalents.
---

This tool drives the knowledge document workflow by applying **RFC 6902 JSON Patch** operations to `.k.json` files and then automatically generating `.k.md` file with markdown representation.

# Knowledge documents
Knowledge documents are structured JSON files that represent various types of knowledge (tasks, docs, etc.). Each document has a corresponding Markdown file that is generated from the JSON source.

We claim that all the files matched by following patterns are protected knowledge documents:

- **`xxxxxxx.k.json`** — is the source of truth canonical knowledge document in JSON format.
- **`xxxxxxx.k.md`** — auto-generated Markdown representation of `xxxxxxx.k.json`.

> ⚠️ Both files are protected (read-only). Do not edit them directly.
> Sometimes user omits `.k` sub-extension in knowledge files. We support `*.json`, `*.md` natively as well.

## Prevent direct updates  Direct updates enforcement
- All updates must go through `${PLUGIN_ROOT}/bin/patch-knowledge-document` to ensure consistency and proper rendering
- `${PLUGIN_ROOT}/bin/patch-knowledge-document` registers both files in the knowledge file registry
- Both files are protected (read-only) to prevent direct edits
- In case of Edit|Write hooks are triggered, the script will raise an error to enforce the workflow

## When to use
- Updating existing knowledge documents (tasks, docs, etc.)
- Generating or refreshing the Markdown representation
- Applying structured edits without hand-editing JSON


## Tool for updating knowledge documents — `${PLUGIN_ROOT}/bin/patch-knowledge-document`
Applies JSON Patch operations to a `.k.json` knowledge document, validates the result, and regenerates the corresponding `.k.md` file.

## Usage
```bash
${PLUGIN_ROOT}/bin/patch-knowledge-document <doc.k.json> '<json-patch>'
```

## Tool for creating knowledge documents — `bin/create-knowledge-document`
Creates a new knowledge document of a specified model type and initializes it with default values.

## Usage
```bash
${PLUGIN_ROOT}/bin/create-knowledge-document <model_type> <document_path>
```

## Supported model types
- `Doc` — Create a basic knowledge document
- `Spec` — Create a specification document with features and constraints
- `Project` — Create a project document indexing specs across a repository

## Examples
```bash
# Create a new Doc
${PLUGIN_ROOT}/bin/create-knowledge-document Doc doc.k.json

# Create a new Spec
${PLUGIN_ROOT}/bin/create-knowledge-document Spec spec.k.json

# Create a new Project
${PLUGIN_ROOT}/bin/create-knowledge-document Project project.k.json
```

## Error handling
- Returns an error if the document already exists
- Returns an error if the model type is not found in the registry
- Supports both built-in models and pluggable custom models configured in `knowledge_config.yaml`

## When to use
- Creating new knowledge documents of a specific type
- Initializing document structure with metadata and default values
- Working with custom models registered in the knowledge configuration

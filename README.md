# Claude Code Plugin

A minimal Claude plugin written in Python that implements hook handlers and logs all hook invocations.

# Prerequisites

This plugin is for claude code.

## Git submodules

- **knowledge_tool** - Knowledge tool system (https://github.com/Clockwork-Pilot/y2-claude-plugin)

To clone with submodules:
```bash
git clone --recurse-submodules <repository-url>
```

To update submodules after cloning:
```bash
git submodule update --init --recursive
```

## Run

```
claude --plugin-dir /path/to/y2-claude-plugin
```


## The Flow

1. User start Claude with y2 plugin
2. User asks "Load y2 skills, Add feature: <Create bla bla bla>, Add constraints."
3. Claude loads skills from y2 plugin
4. y2:knowledge_document_tools skills instructs Claude to use knowledge tool
5. y2:features_and_constraints instructs Claude to create/patch `spec.k.json` knowledge file
6. Claude adds feature and related constraints to `spec.k.json` using above tools
7. Right after constraints were added they immediately affect development enforcing constraints verification. 
   If there are any freshly added constraints didn't fail yet - plugin treats them as 
   unverified blocking constraints and all Edit|Write operations rejected on any files.
   Claude instructed to run `bin/check` that performs constraints checks.
   At soon as constraints proven to fail at least once - Edit|Write operations are allowed.
9. Claude starts implementing features, and worwking until all constraints checks are OK.
10. As soon as plugin "Stop" hook called it runs `bin/check` script and
    if there are still failing constraints left - it blocks stop operation keeping dev in loop.
11. Claude stops if tests pass, and constraints checks successfull.


## Features

### Hook-Based Features
- **Constraint Enforcement** — Stop hook blocks session termination if constraints are failing
- **Unverified Constraints Blocking** — Newly added constraints block Edit/Write operations until verified
- **Development Loop** — Keeps Claude in development loop until all constraints pass
- **File Modification Control** — Pre/Post Edit and Write hooks validate file modifications
- **Event Logging** — All hook events logged to `hooks.log`
- **Session Management** — SessionStart/SessionEnd hooks for initialization and cleanup
- **Notification Monitoring** — Tracks permission prompts, idle notifications, auth success, and dialogs
- **Conversation Compaction** — PreCompact hooks handle manual and automatic compaction
- **Worktree Tracking** — Create/Remove hooks monitor worktree lifecycle
- **Task Completion Handling** — TaskCompleted hook processes task completion events

### Skill-Based Features

#### knowledge_document_tools Skill
- **JSON Patch Operations** — Apply RFC 6902 JSON Patch to `.k.json` knowledge documents
- **Auto-generated Markdown** — Automatically generates `.k.md` markdown representation from JSON
- **Protected Documents** — Read-only enforcement on `.k.json` and `.k.md` files
- **Knowledge Document Creation** — Create Doc, Spec, and Project documents
- **Consistency Enforcement** — All updates through `${PLUGIN_ROOT}/bin/patch-knowledge-document`

#### features_and_constraints Skill
- **Constraint Suite Design** — Define comprehensive test suites with 4 coverage categories (Structural, Behavioral, Environmental, Negative/Security)
- **Zero-State Rule** — All constraints must fail on empty codebase
- **Constraint Execution** — Execute bash and prompt constraints via `${PLUGIN_ROOT}/bin/check`
- **History Tracking** — Track constraint failure counts and verification status
- **Unverified Constraint Blocking** — Lock code modifications until constraints verified
- **Constraint Protection** — Lock verified constraint commands to prevent bypass attempts
- **End-to-End Validation** — Design → Validate → Implement → Verify workflow

## Core Tools

### Knowledge Base Tool
API-first knowledge base system using JSON Patch operations (RFC 6902) with automatic markdown rendering. Features atomic file writes, file protection with read-only attributes, and pluggable RenderableModel classes for document rendering. Provides both command-line scripts and Python functions for applying patches to knowledge documents.

### Constraints Tool
Specification validation system that executes bash constraints, tracks failure history, and generates verification reports. Supports feature-scoped constraint checking and integrates with hook handlers for development loop enforcement.

## Architecture

### Multiple Handlers
The plugin uses a modular handler structure with separate handler files in the `hooks/` directory:
- Each hook type has its own dedicated handler module
- Handlers are dynamically loaded and executed based on configuration
- New handlers can be added without modifying the core plugin logic
- Absolute paths used for both interpreter and handlers

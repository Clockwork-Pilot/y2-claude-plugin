<!--
SYNC IMPACT REPORT
==================
Version change: [TEMPLATE] → 1.0.0
Modified principles: N/A — initial ratification; all sections created from scratch.
Added sections:
  - Core Principles (5 principles: Handler Modularity, Non-Interference,
    Centralized Configuration, Structured Observability, Simplicity)
  - Technology Stack
  - Development Workflow
  - Governance
Removed sections: N/A
Templates checked:
  - .specify/templates/plan-template.md ✅ aligned — "Constitution Check" gate present;
    no agent-specific names found that require updating.
  - .specify/templates/spec-template.md ✅ aligned — mandatory sections (User Scenarios,
    Requirements, Success Criteria) consistent with principle-driven development.
  - .specify/templates/tasks-template.md ✅ aligned — phase structure (Setup →
    Foundational → User Stories → Polish) reflects Modularity and Simplicity principles;
    observability tasks (logging) already called out in Phase N.
Deferred TODOs: None.
-->

# Claude Code Plugin Constitution

## Core Principles

### I. Handler Modularity

Each Claude Code hook type MUST have its own dedicated handler module located in the
`hooks/` directory. The core plugin logic MUST NOT be modified when adding support for
a new hook type. Handlers are dynamically loaded and executed based on the `hooks.json`
configuration. Every handler module MUST implement a single, clearly named entry-point
function and remain self-contained with no cross-handler imports.

**Rationale**: Isolation prevents unintended coupling. Adding a new hook type is a
configuration change, not a surgery on shared code.

### II. Non-Interference

Handlers MUST always exit with code 0 so that Claude Code can proceed unimpeded.
Exception handling MUST be implemented inside every handler: errors MUST be caught,
logged, and silently absorbed — never propagated to crash the Claude Code process.
A handler MUST NOT perform blocking I/O that could stall Claude Code beyond a
short, bounded operation.

**Rationale**: The plugin's role is observation, not control. Claude Code MUST
continue to function even when a handler encounters an unexpected condition.

### III. Centralized Configuration

All file-system paths and tunable settings MUST be declared in `config.py` as the
single source of truth. Handler code MUST import path constants from `config.py`
and MUST NOT embed hard-coded paths. `config.py` MUST derive all paths from
`pathlib.Path(__file__).parent.resolve()` to guarantee portability.

**Rationale**: Relocating or containerizing the project requires changing one file,
not hunting scattered string literals throughout the codebase.

### IV. Structured Observability

Every handler MUST obtain its logger through `setup_logger` from `hook_logging.py`.
Log payloads MUST be serialized as JSON via `serialize_log_data` before writing.
The log level MUST be governed by `HOOKS_LOG_LEVEL` in `config.py`; no local
overrides are permitted inside handler files. Tests MUST set the `TEST_LOG`
environment variable to redirect log output to an in-memory stream, keeping
the file system clean during test runs.

**Rationale**: Structured, machine-readable logs enable post-hoc analysis and
debugging without manual parsing. Test isolation via `TEST_LOG` keeps test suites
deterministic and side-effect-free.

### V. Simplicity (YAGNI)

The plugin MUST remain minimal. New abstractions, base classes, or shared utilities
MUST NOT be introduced without a concrete need present in at least two existing
handlers. Each handler MUST have a single, clear responsibility. Complexity MUST
be justified in writing (e.g., in a plan or PR description) before it is merged.

**Rationale**: A plugin that accumulates accidental complexity becomes harder to
reason about and maintain. Simplicity is a feature, not a shortcut.

## Technology Stack

- **Language**: Python 3 (resolved via absolute interpreter path in plugin config)
- **Path management**: `pathlib.Path` — no raw string paths in source files
- **Testing**: pytest (`pytest.ini` at repository root)
- **Test log isolation**: `TEST_LOG` environment variable routes log output to `StringIO`
- **Log format**: JSON-serialized entries via `hook_logging.serialize_log_data`
- **Container runtime**: Docker image `y2-coder` (see `README.md` for run instructions)

All third-party dependencies MUST be declared explicitly. No implicit system-level
dependencies are permitted.

## Development Workflow

- **Test-first**: Tests MUST be written and confirmed to fail before implementation
  begins for any new handler or modification to an existing handler.
- **Handler independence**: Each handler MUST be independently testable without
  requiring other handlers to be present or active.
- **Commit discipline**: Commit after each logically complete unit of work (one
  handler, one fix). Commits MUST NOT bundle unrelated changes.
- **Quality gate**: Every PR MUST confirm compliance with all five Core Principles
  before merge. The "Constitution Check" section in `plan.md` MUST be completed.
- **No orphan handlers**: A handler file MUST be referenced in `hooks.json`; unused
  handler files MUST be removed promptly.

## Governance

This constitution supersedes all other development practices and informal agreements.
Amendments require:

1. A written rationale explaining what changed and why.
2. An updated version number following semantic versioning:
   - **MAJOR**: Principle removal or redefinition that breaks existing handlers.
   - **MINOR**: New principle or section added, or material guidance expanded.
   - **PATCH**: Clarifications, wording improvements, or typo fixes.
3. Propagation of any changes to dependent templates in `.specify/templates/`.
4. A migration plan if existing handlers are affected by the amendment.

All PRs and reviews MUST verify compliance with the Core Principles. Complexity
deviations from Principle V MUST be justified in the PR description with explicit
reference to the Complexity Tracking table in the relevant `plan.md`.

Runtime development guidance is maintained in `README.md`.

**Version**: 1.0.0 | **Ratified**: 2026-02-26 | **Last Amended**: 2026-02-26

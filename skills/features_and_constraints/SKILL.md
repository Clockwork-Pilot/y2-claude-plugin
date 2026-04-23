---
name: features_and_constraints
description: Design and add features, create comprehensive constraints testing those features. Check constraints, by executing them ensuring every new constraint failed once after creation. Print features spec report.
---

## What This Skill Does

This skill provides two critical capabilities:

1. **Constraint Suite Design**
   - Define comprehensive test suites that guard against lazy implementations
   - Create diverse constraints covering structure, behavior, environment, and security
   - Design tests that fail on empty codebase (Zero-State Rule)
   - Prevent implementation bypass attempts with bulletproof validation

2. **Constraint Execution & Verification** (check_constraints)
   - Execute bash and prompt constraints from task documents
   - Aggregate results into ChecksResults documents
   - Track constraint history and failure counts
   - Generate markdown reports for review

---

# Features and Constraints: End-to-End Validation

This skill spans the complete feature constraint lifecycle: **design** -> **validate** -> **implement** -> **verify**.

## Quick Reference

| Phase | Tool | Purpose |
|---|---|---|
| Design | `patch_knowledge_document.py` | Add features and constraints to `spec.k.json` |
| Validate | `check_spec_constraints.py` | Verify constraints fail on empty codebase |
| Implement | Direct code edits | Build feature to satisfy constraints |
| Verify | `check_spec_constraints.py` | Confirm all constraints PASS |

---

# Phase 1: Design Feature Constraints

## Step 1 — Define the Feature

Add a feature to `spec.k.json` via the knowledge tool:

```bash
python ${PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py spec.k.json '[
  {
    "op": "add",
    "path": "/features/my_feature",
    "value": {
      "type": "Feature",
      "model_version": 1,
      "id": "my_feature",
      "description": "Concise summary (max 100 chars). Used for quick reference.",
      "goals": "Detailed knowledge about the feature. Drives constraint design.",
      "constraints": {}
    }
  }
]'
```

**Fields:**
- `id` — snake_case identifier
- `description` — High-level summary (max 100 chars)
- `goals` — Detailed knowledge structure driving constraint design
- `constraints` — Dict of ConstraintBash objects (start empty)

## Step 2 — Design the Constraint Suite

### Diversity Requirement

Include at least one constraint from each category:

| Category | What It Checks |
|---|---|
| **Structural** | File presence, imports, naming conventions, schema shape |
| **Behavioral** | Input A -> Output B via CLI/API call |
| **Environmental** | Side effect: file written, DB record created, port opened |
| **Negative/Security** | Bad or unauthorized input is strictly rejected |

### ConstraintBash Format

```json
{
  "id": "constraint_file_exists",
  "cmd": "test -f $PROJECT_ROOT/src/main.py || { echo 'missing'; exit 1; }",
  "description": "Verify src/main.py exists"
}
```

**Fields:**
- `id` — snake_case, unique within feature
- `cmd` — Shell command; exit 0 = PASS, non-zero = FAIL
- `description` — What the constraint checks and why it matters
- `scope` — `"local"` (default)

### Constraint Rules

**Exit Code Rule (Critical):** The shell command's exit code must reflect the test result, not the echo result.

```bash
# WRONG - always exits 0, even on failure:
grep -q 'pattern' file && echo 'Found' || echo 'Not found'

# CORRECT - exit code reflects result:
grep -q 'pattern' file
# or
test -f file || { echo "Error: missing"; exit 1; }
```

**Zero-State Rule:** Every constraint MUST FAIL on a completely empty codebase. If it passes on an empty repo, it is worthless — rewrite it.

**Path Rule:** Always use `$PROJECT_ROOT`, never absolute paths:
```bash
test -f $PROJECT_ROOT/src/feature.py    # Correct
test -f /project/src/feature.py         # Wrong
```

**No Grep-for-Success Rule:** Check specific data payloads, not success messages:
```bash
grep -q '"status": "active"' output.json    # Correct
grep -q "success" output.log                 # Wrong
```

## Step 3 — Add Constraints to the Feature

```bash
python ${PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py spec.k.json '[
  {
    "op": "add",
    "path": "/features/my_feature/constraints/constraint_file_exists",
    "value": {
      "id": "constraint_file_exists",
      "cmd": "test -f $PROJECT_ROOT/src/main.py || { echo missing; exit 1; }",
      "description": "Verify src/main.py exists"
    }
  }
]'
```

After adding constraints, immediately proceed to Phase 2 to validate them.

---

# Phase 2: Validate and Execute Constraints

## CRITICAL: Use check_spec_constraints.py Exclusively

**DO NOT manually run constraint commands or create custom validation scripts.** Manual execution bypasses exit code validation, error filtering, constraint history recording, and ChecksResults generation.

## Command

```bash
python3 ${PLUGIN_ROOT}/constraints_tool/constraints_tool/check_spec_constraints.py \
    <spec.k.json> \
    [--features feature1,feature2,...] \
    [--output-checks-path spec-checks.k.json] \
    [--dry-run]
```

**Arguments:**
- `spec.k.json` — Input specification document with features containing constraints
- `--features` — Optional comma-separated feature IDs (omit to check all)
- `--output-checks-path` — Optional output file for ChecksResults
- `--dry-run` — Skip execution; load the existing ChecksResults file at `--output-checks-path` and print the report for the previous run. Useful for re-displaying the last results without re-running constraints.

### Printing a Report Without Running Constraints

To print the report for a **previous** constraint check run — without invoking any constraint commands — use `--dry-run`:

```bash
# print report for previous constraint check run, for project in workspace
python3 ${PLUGIN_ROOT}/constraints_tool/constraints_tool/check_spec_constraints.py --dry-run
```

This reads the prior `spec-checks.k.json` and renders its report. No constraint `cmd` is executed, no history is updated, and no `fails_count` is incremented. Use this whenever you need to re-display or review the last results (e.g., after context loss, or to share the report) instead of re-running the full suite.

### When to Run

- After adding new constraints (expect all FAIL on empty codebase)
- After completing implementation work on any task
- Before marking iteration as complete
- When merging code changes that affect features

## Results Structure

```json
{
  "type": "ChecksResults",
  "feature_results": {
    "feature_id": {
      "feature_id": "feature_id",
      "constraint_results": {
        "constraint_id": {
          "constraint_id": "constraint_id",
          "verdict": true,
          "shrunken_output": "...",
          "constraint_type": "bash"
        }
      }
    }
  }
}
```

## Interpreting and Addressing Failures

1. Read constraint description — understand what's required
2. Run the constraint command manually to debug
3. Fix the underlying issue in code
4. Re-run `check_spec_constraints.py` to validate
5. Repeat until all constraints pass

---

# Handling Unverified Constraints (TOP PRIORITY)

When `spec.k.json` contains unverified constraints (`fails_count < 1` and `contains_unverified_constraints=True`):

**Unverified constraints BLOCK all file editing and become TOP PRIORITY.** Fix them before any other work.

## Constraint Protection Rules

When a constraint is verified (`fails_count > 0`):
- **Locked fields:** `cmd`, `fails_count` — cannot be modified
- **Free field:** `description` — can be changed
- Reason: Verified constraints failed at least once, so their command is known to be valid. Changing it would risk bypassing the verification. Description can be updated for clarity without affecting validation.

When a constraint is unverified (`fails_count < 1`):
- All fields can be modified freely to fix the constraint and achieve the first failure.

## Fix Workflow

### 1. Understand the Constraint
Read the constraint in `spec.k.json`. What does `cmd` do? What does `description` require?

### 2. Fix (choose one or combine)

cmd may only be fixed for unverified constraints. Verified constraints require fixing the underlying issue in code, not the constraint itself.

**Option A — Refine the constraint command** (cmd is buggy or incomplete):
```bash
python ${PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py spec.k.json '[
  {
    "op": "replace",
    "path": "/features/my_feature/constraints/constraint_id/cmd",
    "value": "corrected command here"
  }
]'
```

**Option B — Fix source code** (constraint is correct, implementation is missing):
Directly edit source files to implement the feature/behavior the constraint tests.

**Option C — Both** (fix cmd AND source code, then iterate).

### 3. Verify
```bash
python3 constraints_tool/constraints_tool/check_spec_constraints.py \
    spec.k.json --features feature_id --output-checks-path spec-checks.k.json
```
Constraint should FAIL (exit non-zero) -> `fails_count` increments to 1 -> constraint becomes verified.

### 4. Resume Normal Work
Once all unverified constraints have `fails_count > 0`, blocking is removed.

---

# Critical Rules

## Knowledge Documents (`.k.json`)
- **NEVER** edit directly
- **ALWAYS** use `patch_knowledge_document.py` API

## Constraint Execution
- **NEVER** manually run constraint commands for validation
- **ALWAYS** use `check_spec_constraints.py`

## Constraint Design
- Constraints must test real implementation requirements — no fake checks or temporary hacks
- Every constraint must fail on empty codebase (Zero-State Rule)
- Exit codes must reflect test result, not echo result

---

# Design Checklist

Before finalizing a constraint suite, verify:

- [ ] Feature has clear `id`, `description`, `goals`
- [ ] All constraints have unique snake_case `id`
- [ ] All constraints FAIL on empty codebase (Zero-State Rule)
- [ ] Suite covers all 4 categories (Structural, Behavioral, Environmental, Negative)
- [ ] Exit codes reflect test results (not echo output)
- [ ] All paths use `$PROJECT_ROOT`
- [ ] Descriptions explain what and why

---

# Complete Example

```json
{
  "type": "Feature",
  "model_version": 1,
  "id": "api_rate_limiter",
  "description": "Per-user rate limiting on POST /api/data. Max 10 req/min, 429 on excess.",
  "goals": "Implement per-user rate limiting on POST /api/data. Max 10 requests/minute per user. Excess requests return HTTP 429 with Retry-After header. Persist state in Redis.",
  "constraints": {
    "constraint_limiter_module_exists": {
      "id": "constraint_limiter_module_exists",
      "cmd": "test -f $PROJECT_ROOT/src/rate_limiter.py || { echo 'rate_limiter.py missing'; exit 1; }",
      "description": "Structural: rate_limiter.py module must exist"
    },
    "constraint_limiter_imported_in_api": {
      "id": "constraint_limiter_imported_in_api",
      "cmd": "grep -q 'from.*rate_limiter import\\|import.*rate_limiter' $PROJECT_ROOT/src/api.py || { echo 'rate_limiter not imported'; exit 1; }",
      "description": "Structural: rate_limiter must be imported in api.py"
    },
    "constraint_tenth_request_passes": {
      "id": "constraint_tenth_request_passes",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 10 --expect-pass || { echo '10th request should pass'; exit 1; }",
      "description": "Behavioral: the 10th request within a minute must return 200"
    },
    "constraint_eleventh_request_rejected": {
      "id": "constraint_eleventh_request_rejected",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 11 --expect-status 429 || { echo '11th request must return 429'; exit 1; }",
      "description": "Negative: the 11th request within a minute must return HTTP 429"
    },
    "constraint_redis_persisted": {
      "id": "constraint_redis_persisted",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 1 && redis-cli keys 'rate:*' | grep -q 'rate:' || exit 1",
      "description": "Environmental: rate state persisted in Redis"
    }
  }
}
```

---

# Workflow Integration

| Skill | When to Use |
|---|---|
| `y2:knowledge_document_tools` | Apply JSON Patch operations to `.k.json` documents |
| `y2:task-lifecycle-tool` | Create Task, transition status, add Iterations |
| `y2:features_and_constraints` | Design constraints + validate implementation |

## Implementation Details

- **Constraint checker**: `constraints_tool/constraints_tool/check_spec_constraints.py`
- **Knowledge patcher**: `${PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py`
- **Features location**: `spec.k.json` at path `/features/<feature_id>`
- **Results output**: `spec-checks.k.json` (ChecksResults model)
- `$PROJECT_ROOT` is substituted automatically in constraint commands
- Recursive execution of `check_spec_constraints.py` within constraints is detected and prevented
- All timestamps are ISO8601 formatted

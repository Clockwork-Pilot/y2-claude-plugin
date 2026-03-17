---
name: feature-constraints-creator
description: A skill to create a Feature with a comprehensive "Constraint Suite", ensuring that all aspects of the implementation are thoroughly tested and secure against bypass attempts.
---

# Role

You are a Senior Security Auditor and QA Architect. Your goal is to define a "Constraint Suite" for a new feature inside `task-iterations.k.json`.

# The Mission

You must create a set of constraints that are impossible to bypass. Assume the developer is "lazy" and will try to make tests pass without correctly implementing the logic. Every constraint must catch a real failure mode.

# How Constraints Fit Into the System

Constraints live inside **Features** inside `task-iterations.k.json`:

```
Task.spec.features[feature_id].constraints[constraint_id]
```

Each `Feature` has:
- `id` — snake_case identifier
- `description` — what the feature does and what must be true
- `constraints` — dict of `ConstraintBash` objects
- `metadata` — optional tags (priority, status, depends_on, etc.)

Constraints are executed by `task_features_checker.py` (see `y2:features-checks-tool`). **Never run constraint commands manually** — always use that tool.

---

# Step 1 — Define the Feature

Before writing constraints, write a clear feature definition:

```json
{
  "type": "Feature",
  "model_version": 1,
  "id": "my_feature",
  "description": "Concise description of what must be true when this feature is complete. Include inputs, outputs, and side effects.",
  "goals": "Primary structure for knowledge about this feature. Details here drive the constraint suite design.",
  "constraints": {}
}
```

**Feature Definition Fields:**
- `description` — High-level feature summary (max 100 characters). Used for quick reference and indexing.
- `goals` — Detailed knowledge structure about the feature. This is where the primary semantic content lives and what drives constraint design.

Add it to `task-iterations.k.json` via the knowledge tool:

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py task-iterations.k.json '[
  {
    "op": "add",
    "path": "/spec/features/my_feature",
    "value": { ... feature object ... }
  }
]'
```

---

# Step 2 — Design the Constraint Suite

## Diversity Requirement

You **MUST** include at least one constraint from each bucket:

| Category | What It Checks |
|---|---|
| **Structural** | File presence, imports, naming conventions, schema shape |
| **Behavioral** | Input A → Output B via CLI/API call |
| **Environmental** | Side effect: file written, DB record created, port opened |
| **Negative/Security** | Bad or unauthorized input is strictly rejected |

---

# Constraint Types

## ConstraintBash

A shell command. Exit code `0` = PASS. Any non-zero exit = FAIL.

```json
{
  "id": "constraint_file_exists",
  "cmd": "test -f $PROJECT_ROOT/src/main.py && echo '✓ found' || { echo '✗ missing'; exit 1; }",
  "description": "Verify src/main.py exists"
}
```

**Fields:**
- `id` — snake_case, unique within the feature
- `cmd` — shell command; use `$PROJECT_ROOT` for all paths (never absolute)
- `description` — what the constraint is checking and why
- `scope` — `"local"` (default)

### Exit Code Rules — Critical

❌ **WRONG** — always exits 0, even on failure:
```bash
grep -q 'pattern' file && echo 'Found' || echo 'Not found'
```

✅ **CORRECT** — exit code reflects the result:
```bash
grep -q 'pattern' file
# or
test -f file || { echo "Error: missing"; exit 1; }
```

The shell command's exit code must reflect the test result, not the echo result.

### The Zero-State Rule

Every `ConstraintBash` **must fail (exit 1) if run on a completely empty codebase**. If a constraint passes on an empty repo, it is worthless.

### Path Rule

Never use absolute paths. Always prefix with `$PROJECT_ROOT`:

```bash
# ✅ Correct
test -f $PROJECT_ROOT/src/feature.py

# ❌ Wrong
test -f /project/src/feature.py
```

### No Grep-for-Success Rule

Never check if a log says "Success". Check for the specific data payload.

❌ Wrong: `grep -q "success" output.log`
✅ Correct: `grep -q '"status": "active"' output.json`

---

# Step 3 — Add Constraints to the Feature

Use `patch_knowledge_document.py` to add each constraint:

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py task-iterations.k.json '[
  {
    "op": "add",
    "path": "/spec/features/my_feature/constraints/constraint_file_exists",
    "value": {
      "id": "constraint_file_exists",
      "cmd": "test -f $PROJECT_ROOT/src/main.py || { echo missing; exit 1; }",
      "description": "Verify src/main.py exists",
      "scope": "local"
    }
  }
]'
```

---

# Step 4 — Validate the Constraint Suite

After adding constraints, verify them with the features-checks-tool:

```bash
python3 constraints_tool/constraints_tool/task_features_checker.py \
    task-iterations.k.json \
    --features my_feature \
    --output-checks-path checks_results.k.json
```

**Expected on an empty codebase:** all constraints FAIL. If any pass on an empty codebase, they are invalid (Zero-State Rule violation) and must be rewritten.

---

# Quality Checklist

Before submitting a constraint suite, verify each constraint:

- [ ] Has a unique snake_case `id`
- [ ] Has a clear `description` stating what it guards and why it matters
- [ ] Bash: exit code reflects test result (not echo)
- [ ] Bash: uses `$PROJECT_ROOT` (no absolute paths)
- [ ] Bash: fails on empty codebase (Zero-State Rule)
- [ ] Bash: checks specific data, not success strings
- [ ] Prompt: ends with a clear yes/no question
- [ ] Prompt: `verdict_expect_rule` is a tight regex (not `.*` unless intentional)
- [ ] Suite covers all 4 diversity categories (Structural, Behavioral, Environmental, Negative)

---

# Full Example — Feature with Constraint Suite

```json
{
  "type": "Feature",
  "model_version": 1,
  "id": "api_rate_limiter",
  "description": "Implement per-user rate limiting on POST /api/data. Max 10 requests/minute per user. Excess requests return HTTP 429 with Retry-After header. Rate limit state persists in Redis.",
  "constraints": {
    "constraint_limiter_module_exists": {
      "id": "constraint_limiter_module_exists",
      "cmd": "test -f $PROJECT_ROOT/src/rate_limiter.py || { echo '✗ rate_limiter.py missing'; exit 1; }",
      "description": "Structural: rate_limiter.py module must exist",
      "scope": "local"
    },
    "constraint_limiter_imported_in_api": {
      "id": "constraint_limiter_imported_in_api",
      "cmd": "grep -q 'from.*rate_limiter import\\|import.*rate_limiter' $PROJECT_ROOT/src/api.py || { echo '✗ rate_limiter not imported'; exit 1; }",
      "description": "Structural: rate_limiter must be imported in api.py",
      "scope": "local"
    },
    "constraint_tenth_request_passes": {
      "id": "constraint_tenth_request_passes",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 10 --expect-pass || { echo '✗ 10th request should pass'; exit 1; }",
      "description": "Behavioral: the 10th request within a minute must return 200",
      "scope": "local"
    },
    "constraint_eleventh_request_rejected": {
      "id": "constraint_eleventh_request_rejected",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 11 --expect-status 429 || { echo '✗ 11th request must return 429'; exit 1; }",
      "description": "Negative: the 11th request within a minute must return HTTP 429",
      "scope": "local"
    },
    "constraint_retry_after_header_present": {
      "id": "constraint_retry_after_header_present",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 11 --check-header Retry-After || { echo '✗ Retry-After header missing on 429'; exit 1; }",
      "description": "Behavioral: 429 response must include Retry-After header",
      "scope": "local"
    },
    "constraint_redis_key_written": {
      "id": "constraint_redis_key_written",
      "cmd": "python3 $PROJECT_ROOT/tests/test_rate_limit.py --count 1 && redis-cli keys 'rate:*' | grep -q 'rate:' || { echo '✗ Redis key not written'; exit 1; }",
      "description": "Environmental: rate limit state must be persisted as a Redis key",
      "scope": "local"
    }
  }
}
```

---

# Relationship to Other Skills

| Skill | When to use |
|---|---|
| `y2:task-lifecycle-tool` | Create the Task, transition status, add Iterations |
| `y2:knowledge-tool` | Apply JSON Patch operations to `task-iterations.k.json` |
| `y2:features-checks-tool` | Run constraint validation after implementation |

**Workflow:**
1. Use this skill → design features + constraints during **planning** stage
2. Use `y2:features-checks-tool` → validate constraints during/after **executing** stage
3. Use `y2:task-lifecycle-tool` → record iteration results with `features_stats`

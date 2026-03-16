---
name: task-lifecycle-tool
description: Task lifecycle knowledge document management. `task.k.json` is the canonical task document; `task.k.md` is its rendered Markdown view. Both files are protected and should not be edited directly; use `patch_knowledge_document.py` to update `task.k.json` and automatically regenerate `task.k.md`.
---

Load knowledge-tool skill

# Task
- **`task.k.json`** — canonical knowledge document used to track task progress through its lifecycle.
- **`task.k.md`** — auto-generated Markdown representation of `task.k.json`.

> ⚠️ Both files are protected (read-only). Do not edit them directly.

### Create task
Create `task.k.json` (if it does not exist).

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/create_knowledge_document.py Task task.k.json
```

### Update task
Update `task.k.json` by applying a JSON Patch (RFC 6902). This will update `task.k.json` and automatically regenerate `task.k.md`.

```bash
python ${CLAUDE_PLUGIN_ROOT}/knowledge_tool/knowledge_tool/patch_knowledge_document.py task.k.json '[{"op": "replace", "path": "/label", "value": "New Label"}]'
```

## Task Lifecycle
Task status indicates the current stage of the task lifecycle:
- `planning` — Task is being planned; specifications can be edited.
- `executing` — Task is being executed; specifications become read-only.
- `failed` — Task execution failed; specifications are read-only.
- `succeed` — Task execution succeeded; specifications are read-only.

**Create Task -> Planning -> Executing -> Failed|Succeed**

## Task status

### Task.status is "planning"
**Spec** section is editable with knowledge tool primitives when task is in "planning" stage.

**Spec** has *Description* and *Features* during the planning stage before execution begins.

```
Spec {
    description: str,
    features: Dict[str, Feature],
    ...
}
```

**Feature** has *Description* and a *Constraints*, enforced during the "executing" stage.

```
Feature {
    description: str,
    constraints: Dict[str, Constraint],
    ...
}
```

**Constraint**  has *ConstraintBash* fields.
Constraint is a validation rule which isd a prerequisite for the feature to be considered working. Constraint validation is a bash command or a prompt-based.

constraint_bash: **ConstraintBash** - contains `cmd` that should be executed to validate the constraint, and exit code 0 indicates that the constraint is satisfied. The command can be a simple check or a more complex validation script.
**Limitations:** 
- `task_features_checker.py` API Script checks features constraints, and should not be used directly in constraints' `cmd`. Attempt to call it recursively will immediately fail.
- Absolute paths in `cmd` should not be used. Instead path should be starting with `${CLAUDE_PROJECT_ROOT}`.

### Task.status is "executing"
**Spec** section becomes read-only when task is in "executing" stage to ensure consistency and prevent changes that could affect the execution process.

This is the only implementation stage, where the task is being worked on based on the specifications defined in the planning stage. During this stage, the focus is on executing the plan and implementing the features outlined in the specification.

Implementation steps are tracked in **Iterations**. Each iteration is an instance of *Iteration* models and can include feedback or progress updates such as metrics and constraints checks defined in the specification.

**Iteration** has a naming convention: `iteration_<iteration_number>` (e.g., `iteration_1`)

**Iteration** can include the following metrics and statistics:
- **code_stats**: Code changes (lines added/removed, files changed)
- **tests_stats**: Test execution results (passed/total, pass rate)
- **coverage_stats_by_tests**: Coverage metrics per test
- **features_stats**: Feature constraint validation results (✨ NEW)

### Iteration.features_stats — Feature Constraint Validation

When a coding agent adds a new Iteration after completing work, it MUST include `features_stats` containing:
- **features_checks**: Dict[str, bool] - Status of ALL task features (True=passed, False=failed)
- **failed**: Dict[str, FeatureResult] - Details of failed features only

**Display Format:**
When an Iteration is added via the lifecycle tool, the agent MUST display iteration stats summary:
```
📈 Iteration Stats Summary:
  Code Changes: X files, Y lines added, Z lines removed
  Tests: N/M passed (pass_rate%)
  Feature Validation: X/Y features passed, Z features failed
    ✓ feature_1
    ✓ feature_2
    ✗ feature_3 (constraints failed)
```

This ensures visibility into which features are validated in each iteration and highlights areas needing attention.


### Task.status is "failed" or "succeed"
Spec section becomes read-only when task is in "failed" or "succeed" stage.
Both are termination statuses, indicating that the task has reached its conclusion. When a task is marked as "failed," it signifies that the task did not achieve its intended goals or outcomes. Conversely, when a task is marked as "succeed," it indicates that the task was completed successfully and met its objectives.


# Task document structure

## Status field tracks the lifecycle stage of the task, with possible
"status" valuues are: planning, executing, failed, succeed.

## Spec section
The `spec` field of the task document is Spec model containing description and features.

### Spec.description
The `spec.description` field is a Doc model that contains the main specification content of the task. It is rendered as a section in the generated Markdown document.

### Spec.features
The `spec.features` field is a list of Feature models that represent specific features or requirements of the task. Each feature contains a description and constraints dict.

#### Spec.features constraints
The `spec.features.constraints` field is a dictionary containing validation rules and constraints for each feature.

# Task document migrations
To migrate existing task documents that still has "plan": field.

Use knowledge tool primitives to copy content from Task.plan to Task.spec.description.

# Features and constraints displaying
Example of whowing features and constraints directly on the screen, shown below:

# Adding Iterations with Feature Validation

When coding agents complete work and add a new iteration to task.k.json:

1. **Run feature constraint checks** using the features-checks-tool:
   ```bash
   python constraints_tool/constraints_tool/task_features_checker.py task.k.json --output-checks-path checks_results.k.json
   ```

2. **Extract features_stats** from the ChecksResults output (automatically generated by task_features_checker.py)

3. **Include features_stats in the new Iteration** with:
   - Complete list of all task features in `features_checks`
   - Failed feature details in `failed` dict (only if failures exist)

4. **Display stats summary** showing which features passed/failed

Example patch operation to add Iteration with features_stats:
```json
[{
  "op": "add",
  "path": "/iterations/iteration_1",
  "value": {
    "type": "Iteration",
    "id": "iteration_1",
    "features_stats": {
      "features_checks": {
        "feature_1": true,
        "feature_2": false,
        "feature_3": true
      },
      "failed": {
        "feature_2": {
          "feature_id": "feature_2",
          "constraints_results": { ... }
        }
      }
    },
    "code_stats": { ... },
    "metadata": { ... }
  }
}]
```

# Compact features list
Use numbered lists when showing lists of features. Every listed feature includes list number, feature id, feature description, and constraints ids list (if any). For example:
1. Feature ID: feature_1
   - **Description**: This is the description of feature 1.
   - **Constraints**: (constraint_1: result, constraint_2: result, ...)
2. Feature ID: feature_2
   - **Description**: This is the description of feature 2.
   - **Constraints**: (constraint_3: result, constraint_4: result, ...)
...

# Showing single Feature
Feature ID: feature_2
  **Description**: This is the description of feature 2.
  **Constraints**:
    1 **Constraint ID**: constraint_1
       **Type**: ConstraintBash
       **Validation Command**: `echo "Validating constraint 1" && exit 0`

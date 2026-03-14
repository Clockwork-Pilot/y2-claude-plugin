---
name: features-checks
description: Execute and validate feature constraints from task.json, capturing results to checks_results.json using task_features_checker.py
---

# Features Checks Tool

Execute feature constraint validation workflows: bash commands and LLM prompts with results tracking.

## Purpose

This skill validates feature constraints embedded in task documents:
- Execute **bash constraints** from features (shell commands with pass/fail validation)
- Execute **prompt constraints** from features (Claude evaluations with regex-based verdict validation)
- Support filtering constraints by feature ID
- Aggregate results into a ChecksResults document
- Track constraint execution history and outcomes with full output details

## How It Works

The skill uses task_features_checker.py to validate constraints from task documents:
1. Load task document (task.json) containing features with embedded constraints
2. Extract constraints from specified features (or all if none specified)
3. Execute each constraint:
   - **Bash constraints**: Run shell command, capture output, determine pass/fail
   - **Prompt constraints**: Send to Claude for evaluation, validate verdict against expected pattern
4. Aggregate all results into `checks_results.json` (ChecksResults model)

## Workflow

### Bash Constraints
```
Constraint (bash_cmd="test -f file.txt")
    ↓
Execute: subprocess.run(cmd, shell=True)
    ↓
ConstraintBashResult(verdict=True/False, output="...")
    ↓
Test(result=ConstraintBashResult)
```

### Prompt Constraints
```
Agent executes:
  1. Reads prompt from Constraint
  2. Calls Claude with prompt
  3. Writes ConstraintPromptResult to credentials-tests.json

Executor reads:
  1. Check credentials-tests.json for result
  2. Validate verdict matches verdict_expect_rule regex
  3. Create ConstraintPromptResult with validated verdict
  4. Test(result=ConstraintPromptResult)
```

## Usage

### Command Pattern
```bash
python3 constraints_tool/constraints_tool/task_features_checker.py \
    <task.json> \
    [--features feature1,feature2,...] \
    [--output-checks-path checks_results.json]
```

### Arguments
- `task.json` — Input task document with features containing constraints
- `--features` — Optional comma-separated list of feature IDs to check (if not provided, checks all features)
- `--output-checks-path` — Optional output file for check results (ChecksResults model)

### Example
```bash
# Check all features and their constraints
python3 constraints_tool/constraints_tool/task_features_checker.py task.json

# Check specific features only
python3 constraints_tool/constraints_tool/task_features_checker.py \
    task.json \
    --features forbid_task_status_downgrade,render_spec_features_in_task

# Save results to file with markdown rendering via patch_knowledge_document.py
python3 constraints_tool/constraints_tool/task_features_checker.py \
    task.json \
    --output-checks-path checks_results.json
```

## Supported Model Types

- **Input**: `Task` — Root document with features containing constraints
  - Contains: Task.spec.features with embedded constraints
  - Features: Dict[str, Feature] with Feature.constraints definitions

- **Output**: `ChecksResults` — Root document with check results
  - Contains: Dict[str, FeatureResult] mapping features to their constraint results
  - Results: Union[ConstraintBashResult, ConstraintPromptResult]

## Constraint Types

### ConstraintBash
```json
{
  "id": "check_file",
  "cmd": "test -f README.md",
  "description": "Verify README exists",
  "scope": "local"
}
```
- **cmd**: Shell command to execute
- **verdict**: True if exit code is 0, False otherwise

### ConstraintPrompt
```json
{
  "id": "validate_logic",
  "prompt": "Is this logic correct? [code]",
  "verdict_expect_rule": "(yes|pass|correct)",
  "description": "Validate code logic",
  "scope": "local"
}
```
- **prompt**: Question/instruction for Claude
- **verdict_expect_rule**: Regex pattern for valid verdicts
- **verdict**: String that must match the regex

## Implementation

- **File**: `constraints_tool/constraints_tool/task_features_checker.py`
- **Features**:
  - Load Task document and extract features with constraints
  - Filter features by optional `--features` argument
  - Execute ConstraintBash commands with shell execution
  - Execute ConstraintPrompt with Claude API evaluation
  - Support `$PROJECT_ROOT` substitution in constraint commands
  - Prevent recursive execution of constraints
  - Aggregate results into ChecksResults model
- **Models**: From `knowledge_tool/knowledge_tool/src/models/`
  - Task, Feature, ConstraintBash, ConstraintPrompt
  - ChecksResults, FeatureResult, ConstraintBashResult, ConstraintPromptResult

## Check Results

Results are captured in a ChecksResults document with:
- **Feature results**: Organized by feature ID
- **Constraint results**: For each constraint in a feature
- **Verdict tracking**: Pass/fail for bash, verdict text for prompt
- **Output/answers**: Detailed bash output and prompt evaluation results
- **Timestamps**: When each constraint was executed
- **Metadata**: Total counts, execution details, $PROJECT_ROOT substitution info

## Example Constraint Structure in Task

### Constraints in task.json (within Feature)
```json
{
  "type": "Feature",
  "id": "example_feature",
  "description": "Example feature with constraints",
  "constraints": {
    "constraint_file_exists": {
      "id": "constraint_file_exists",
      "cmd": "test -f $PROJECT_ROOT/src/main.py",
      "description": "Check main.py exists",
      "scope": "local"
    },
    "constraint_code_quality": {
      "id": "constraint_code_quality",
      "prompt": "Is the code well-structured? Review the implementation in $PROJECT_ROOT/src/main.py and provide feedback.",
      "verdict_expect_rule": "(yes|excellent|good|well-structured)",
      "description": "Code quality check",
      "scope": "local"
    }
  }
}
```

### checks_results.json Output Structure
```json
{
  "type": "ChecksResults",
  "feature_results": {
    "example_feature": {
      "feature_id": "example_feature",
      "constraint_results": {
        "constraint_file_exists": {
          "constraint_id": "constraint_file_exists",
          "verdict": true,
          "shrunken_output": "File exists",
          "constraint_type": "bash"
        },
        "constraint_code_quality": {
          "constraint_id": "constraint_code_quality",
          "verdict": "excellent",
          "short_answer": "Code follows best practices and is well-structured",
          "constraint_type": "prompt"
        }
      }
    }
  }
}
```

## Notes

- Bash constraints execute immediately with `$PROJECT_ROOT` substitution support
- Prompt constraints are evaluated by Claude with verdict validation against verdict_expect_rule regex
- Recursive execution detection prevents infinite loops in constraint evaluation
- All timestamps are ISO8601 formatted
- Results can be rendered to markdown via knowledge_tool skill with patch_knowledge_document.py
- Feature filtering with --features allows selective constraint validation
- ChecksResults output includes metadata about substitutions and execution details

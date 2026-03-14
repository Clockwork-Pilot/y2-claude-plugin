---
name: test-constraints
description: Execute and validate constraints from constraints.json, capturing results to tests.json
---

# Test Constraints Skill

Execute constraint validation workflows: bash commands and LLM prompts with results tracking.

## Purpose

This skill drives constraint execution and testing:
- Execute **bash constraints** (shell commands with pass/fail validation)
- Execute **prompt constraints** (LLM evaluations with regex-based verdict validation)
- Aggregate results into a Tests document
- Track constraint execution history and outcomes

## How It Works

The skill uses a constraints execution engine:
1. Load constraints from `constraints.json` (Constraints root document)
2. Execute each constraint:
   - **Bash constraints**: Run shell command, capture output, determine pass/fail
   - **Prompt constraints**: Read verdict from `credentials-tests.json` (populated by agent workflow)
3. Validate prompt verdicts against expected regex patterns
4. Aggregate all results into `tests.json` (Tests root document)

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
python3 /y2-plugin/constraints_tool/constraints_tool/constraints_executor.py \
    <constraints.json> \
    [tests.json] \
    [credentials-tests.json]
```

### Arguments
- `constraints.json` — Input constraints document (Constraints model)
- `tests.json` — Output file for test results (Tests model) [optional]
- `credentials-tests.json` — File for agent-written prompt results [optional, default: credentials-tests.json]

### Example
```bash
# Create and test constraints
python3 /y2-plugin/constraints_tool/constraints_tool/constraints_executor.py \
    constraints.json \
    tests.json \
    credentials-tests.json

# Results saved to tests.json with markdown rendering via patch_knowledge_document.py
```

## Supported Model Types

- **Input**: `Constraints` — Root document with constraint definitions
  - Contains: Dict[str, Constraint] with bash or prompt variants

- **Output**: `Tests` — Root document with test results
  - Contains: Dict[str, Test] linking constraints to results
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

- **File**: `/y2-plugin/constraints_tool/constraints_tool/constraints_executor.py`
- **Dependencies**:
  - `bash_executor.py` — Execute bash constraints
  - `prompt_executor.py` — Execute prompt constraints via knowledge documents
  - `result_aggregator.py` — Combine results into Tests document
- **Models**: From `y2-plugin/knowledge_tool/knowledge_tool/src/models/`
  - Constraints, Constraint, ConstraintBash, ConstraintPrompt
  - Test, Tests, ConstraintBashResult, ConstraintPromptResult

## Test Results

Results are captured in a Tests document with:
- **Filter info**: Scope and constraint type
- **Tests by type**: Organized bash and prompt results
- **Verdict tracking**: Pass/fail for bash, verdict text for prompt
- **Timestamps**: When each constraint was executed
- **Metadata**: Total counts, execution details

## Example Constraint Files

### constraints.json Structure
```json
{
  "type": "Constraints",
  "constraints": {
    "c1": {
      "id": "c1",
      "scope": "local",
      "constraint_bash": {
        "id": "c1",
        "cmd": "test -f src/main.py",
        "description": "Check main.py exists",
        "scope": "local"
      }
    },
    "p1": {
      "id": "p1",
      "scope": "local",
      "constraint_prompt": {
        "id": "p1",
        "prompt": "Is the code well-structured?",
        "verdict_expect_rule": "(yes|excellent|good)",
        "description": "Code quality check",
        "scope": "local"
      }
    }
  }
}
```

### tests.json Output Structure
```json
{
  "type": "Tests",
  "scope": "all",
  "constraint_type": "all",
  "tests": {
    "test_bash_1": {
      "id": "test_bash_1",
      "constraint_id": "c1",
      "result": {
        "constraint_id": "c1",
        "verdict": true,
        "shrunken_output": "test passed"
      }
    },
    "test_prompt_1": {
      "id": "test_prompt_1",
      "constraint_id": "p1",
      "result": {
        "constraint_id": "p1",
        "verdict": "good",
        "short_answer": "Code follows best practices"
      }
    }
  }
}
```

## Notes

- Bash constraints execute immediately and capture exit codes
- Prompt constraints wait for agent to write results to credentials-tests.json
- Verdict validation happens at aggregation time for prompts
- All timestamps are ISO8601 formatted
- Results can be rendered to markdown via knowledge_tool skill

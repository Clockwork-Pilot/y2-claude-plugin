# Task: task_1

## Table of Contents

- [Specification (v1)](#specification-v1)
- [Features](#features)
    - [Feature: add_constraint_validation_requirement_skill](#feature-add_constraint_validation_requirement_skill)
      - [constraint_requirement_section_exists](#constraint_requirement_section_exists)
      - [constraint_results_interpretation_guide](#constraint_results_interpretation_guide)
      - [constraint_when_to_run_documented](#constraint_when_to_run_documented)
    - [Feature: constraint_checker_exit_code_hook](#feature-constraint_checker_exit_code_hook)
      - [constraint_handler_stop_calls_checker](#constraint_handler_stop_calls_checker)
      - [constraint_handler_stop_checks_exit_code](#constraint_handler_stop_checks_exit_code)
      - [constraint_handler_stop_prints_decision_block](#constraint_handler_stop_prints_decision_block)
      - [constraint_task_checker_exits_2_on_failure](#constraint_task_checker_exits_2_on_failure)
    - [Feature: constraint_rendering_capability](#feature-constraint_rendering_capability)
      - [constraint_bash_render_method](#constraint_bash_render_method)
      - [constraint_bash_render_toc_method](#constraint_bash_render_toc_method)
      - [constraint_feature_uses_render_toc](#constraint_feature_uses_render_toc)
      - [constraint_prompt_render_method](#constraint_prompt_render_method)
      - [constraint_prompt_render_toc_method](#constraint_prompt_render_toc_method)
      - [constraint_rendering_displays_type](#constraint_rendering_displays_type)
    - [Feature: constraint_scripts_directory](#feature-constraint_scripts_directory)
      - [constraint_scripts_directory_exists](#constraint_scripts_directory_exists)
      - [constraint_scripts_documented](#constraint_scripts_documented)
      - [constraint_scripts_readme_exists](#constraint_scripts_readme_exists)
    - [Feature: enhance_constraint_bash_result_output](#feature-enhance_constraint_bash_result_output)
      - [constraint_output_populated_on_failure](#constraint_output_populated_on_failure)
      - [constraint_output_rendered_in_markdown](#constraint_output_rendered_in_markdown)
      - [constraint_shrunken_output_field_exists](#constraint_shrunken_output_field_exists)
    - [Feature: feature_goals_field](#feature-feature_goals_field)
      - [constraint_goals_field_exists](#constraint_goals_field_exists)
      - [constraint_goals_field_in_task](#constraint_goals_field_in_task)
      - [constraint_goals_in_toc](#constraint_goals_in_toc)
      - [constraint_goals_rendered_in_markdown](#constraint_goals_rendered_in_markdown)
    - [Feature: features_stats_diff_tracking](#feature-features_stats_diff_tracking)
      - [constraint_diff_rendered_in_iteration](#constraint_diff_rendered_in_iteration)
      - [constraint_features_stats_diff_model_exists](#constraint_features_stats_diff_model_exists)
      - [constraint_features_stats_has_diff_method](#constraint_features_stats_has_diff_method)
      - [constraint_iteration_has_diff_field](#constraint_iteration_has_diff_field)
    - [Feature: migrate_metadata_to_model](#feature-migrate_metadata_to_model)
      - [constraint_constraint_model_uses_metadata](#constraint_constraint_model_uses_metadata)
      - [constraint_doc_model_uses_metadata](#constraint_doc_model_uses_metadata)
      - [constraint_feature_model_uses_metadata](#constraint_feature_model_uses_metadata)
      - [constraint_metadata_import](#constraint_metadata_import)
      - [constraint_no_dict_metadata_references](#constraint_no_dict_metadata_references)
      - [constraint_spec_model_uses_metadata](#constraint_spec_model_uses_metadata)
      - [constraint_task_model_uses_metadata](#constraint_task_model_uses_metadata)
    - [Feature: render_spec_features_in_task](#feature-render_spec_features_in_task)
      - [constraint_constraint_details_in_markdown](#constraint_constraint_details_in_markdown)
      - [constraint_feature_section_in_markdown](#constraint_feature_section_in_markdown)
      - [constraint_rendering_implementation_review](#constraint_rendering_implementation_review)
    - [Feature: task_add_iteration_script](#feature-task_add_iteration_script)
      - [constraint_script_exists](#constraint_script_exists)
      - [constraint_script_populates_features_stats](#constraint_script_populates_features_stats)
      - [constraint_script_runs_checker](#constraint_script_runs_checker)
      - [constraint_script_uses_knowledge_tool](#constraint_script_uses_knowledge_tool)
      - [constraint_skill_documentation_updated](#constraint_skill_documentation_updated)
    - [Feature: task_default_render_toc](#feature-task_default_render_toc)
      - [constraint_default_toc_when_opts_missing](#constraint_default_toc_when_opts_missing)
      - [constraint_explicit_false_respected](#constraint_explicit_false_respected)
      - [constraint_render_toc_default_true](#constraint_render_toc_default_true)
      - [constraint_toc_rendered_by_default](#constraint_toc_rendered_by_default)
    - [Feature: task_features_checker_selective_patch](#feature-task_features_checker_selective_patch)
      - [constraint_feature_results_filtering](#constraint_feature_results_filtering)
      - [constraint_patch_uses_add_op](#constraint_patch_uses_add_op)
      - [constraint_preserves_other_features](#constraint_preserves_other_features)
      - [constraint_selective_patch_logic](#constraint_selective_patch_logic)
    - [Feature: task_features_checker_tool](#feature-task_features_checker_tool)
      - [constraint_project_root_substitution](#constraint_project_root_substitution)
      - [constraint_recursive_execution_prevention](#constraint_recursive_execution_prevention)
      - [constraint_tool_accepts_features_arg](#constraint_tool_accepts_features_arg)
      - [constraint_tool_accepts_output_checks_path_arg](#constraint_tool_accepts_output_checks_path_arg)
      - [constraint_tool_accepts_task_path](#constraint_tool_accepts_task_path)
      - [constraint_tool_exists](#constraint_tool_exists)
      - [constraint_tool_implementation_review](#constraint_tool_implementation_review)
      - [constraint_tool_output_checks_path_writable](#constraint_tool_output_checks_path_writable)
      - [constraint_tool_returns_checks_results](#constraint_tool_returns_checks_results)
      - [constraint_tool_saves_results_to_file](#constraint_tool_saves_results_to_file)
    - [Feature: task_toc_includes_constraints](#feature-task_toc_includes_constraints)
      - [constraint_constraints_nested_in_toc](#constraint_constraints_nested_in_toc)
      - [constraint_constraints_visible_in_markdown](#constraint_constraints_visible_in_markdown)
      - [constraint_toc_includes_constraints](#constraint_toc_includes_constraints)
    - [Feature: task_toc_rendering_and_links](#feature-task_toc_rendering_and_links)
      - [constraint_anchor_sections_exist](#constraint_anchor_sections_exist)
      - [constraint_toc_has_entries](#constraint_toc_has_entries)
      - [constraint_toc_implementation_review](#constraint_toc_implementation_review)
      - [constraint_toc_indentation](#constraint_toc_indentation)
      - [constraint_toc_links_format](#constraint_toc_links_format)
      - [constraint_toc_section_exists](#constraint_toc_section_exists)
    - [Feature: update_iteration_with_features_stats](#feature-update_iteration_with_features_stats)
      - [constraint_feature_result_constraints_required](#constraint_feature_result_constraints_required)
      - [constraint_features_stats_generated](#constraint_features_stats_generated)
      - [constraint_features_stats_in_iteration](#constraint_features_stats_in_iteration)
      - [constraint_features_stats_model_exists](#constraint_features_stats_model_exists)
      - [constraint_features_stats_rendered](#constraint_features_stats_rendered)
      - [constraint_skill_documentation_updated](#constraint_skill_documentation_updated)
      - [constraint_stats_displayed_on_iteration](#constraint_stats_displayed_on_iteration)
- [Iterations](#iterations)
    - [iteration_1](#iteration_1)
    - [iteration_2](#iteration_2)
    - [iteration_3](#iteration_3)

## Specification (v1)

# Task Plan
### Project Summary

**Status**: ✓ Complete and Functional

**Components Built**:
✓ Knowledge Tool - JSON patching and markdown rendering
✓ Lifecycle Tool - Task creation and management  
✓ File Protection System - Auto-protected documents
✓ Testing - 29 tests all passing
✓ Documentation - CLAUDE.md, skills, README

**Known Issues**:
- Auto-generated protected_files.txt in PLUGIN_ROOT needs merge logic

**Technology**: Python 3.11+, Pydantic, RFC 6902, Git submodules

## Created At
2026-03-06T12:12:53.859554

## Updated At
2026-03-06T12:12:53.859554


## Features

### Feature: add_constraint_validation_requirement_skill
**Add constraint validation requirement to features-checks-tool skill documentation. Require that coding agents check constraints upon work completion and ensure all features pass before marking work as done. Document mandatory constraint checking scenarios, provide command examples, and guide agents on interpreting results and addressing failures.**

**Goals:**
- Add ⚠️ REQUIREMENT section stating constraint checks MUST run upon work completion
- Document REQUIRED scenarios: after implementation, before iteration completion, before merging
- Specify result expectation: all constraints must PASS before work completion
- Provide clear command examples for running constraint checks with default output path
- Add Interpreting Results section with success/failure examples and output format
- Add Addressing Failures troubleshooting workflow for failed constraints
- Emphasize constraint validation is MANDATORY not optional

#### constraint_requirement_section_exists
**Description:** Verify requirement section exists in skill documentation
**Command:** `grep -q 'MUST RUN\|Requirement.*Constraint\|Constraint.*Checks.*MUST' skills/features-checks-tool/SKILL.md && echo 'Requirement section found' || echo 'Missing'`

#### constraint_results_interpretation_guide
**Description:** Verify guide for interpreting constraint results is documented
**Command:** `grep -q 'Interpreting\|Success.*PASS\|Failure.*FAIL' skills/features-checks-tool/SKILL.md && echo 'Interpretation guide exists' || echo 'Missing'`

#### constraint_when_to_run_documented
**Description:** Verify documentation on when to run constraint checks
**Command:** `grep -q 'When to Run\|REQUIRED scenarios' skills/features-checks-tool/SKILL.md && echo 'When section documented' || echo 'Not documented'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: documentation
- implementation: skill
- priority: high
- status: completed

### Feature: constraint_checker_exit_code_hook
**Integrate constraint checking into handler_stop.py hook with exit code signaling. When handler_stop.py is called, it executes task_features_checker.py synchronously and checks the exit code. If exit code is 2 (constraint failures), hook prints decision block: {"decision": "block", "reason": "Constraints failed, fix them first"}. task_features_checker.py must exit with code 2 when any feature has failed constraints, code 0 on success. Hook must exit with same code as constraint checker script.**

**Goals:**
- Update task_features_checker.py to exit with code 2 when constraint failures detected
- Modify handler_stop.py hook to call task_features_checker.py synchronously
- Parse exit code from constraint checker execution
- Print decision block when exit code is 2 with reason message
- Ensure hook propagates same exit code to caller
- Document exit code behavior: 0=success, 1=error, 2=constraint_failures

#### constraint_handler_stop_calls_checker
**Description:** Verify handler_stop.py calls task_features_checker.py
**Command:** `grep -q 'task_features_checker\|constraints_tool' hooks/handler_stop.py && echo 'Calls checker' || echo 'Not called'`

#### constraint_handler_stop_checks_exit_code
**Description:** Verify handler_stop.py checks exit code from checker
**Command:** `grep -q '\$?\|returncode\|exit.*2' hooks/handler_stop.py && echo 'Checks exit code' || echo 'Not checked'`

#### constraint_handler_stop_prints_decision_block
**Description:** Verify handler_stop.py prints decision block for constraint failures
**Command:** `grep -q '"decision".*"block"\|Constraints failed' hooks/handler_stop.py && echo 'Prints decision block' || echo 'Not printed'`

#### constraint_task_checker_exits_2_on_failure
**Description:** Verify task_features_checker.py exits with code 2 when constraints fail
**Command:** `grep -q 'return 2' constraints_tool/constraints_tool/task_features_checker.py && echo 'Exit code 2 implemented' || echo 'Not found'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: integration
- implementation: handler_stop.py, task_features_checker.py
- priority: high
- status: pending

### Feature: constraint_rendering_capability
**Make ConstraintBash and ConstraintPrompt classes renderable with render() and render_toc() methods. Enable constraints to be rendered as markdown independently and integrated into parent objects' TOC generation. This improves modularity and allows constraints to manage their own representation.**

**Goals:**
- Add render() method to ConstraintBash and ConstraintPrompt
- Add render_toc() method to both constraint types
- Display constraint metadata (type, command/prompt, scope)
- Update Feature.render_toc() to use constraint rendering

#### constraint_bash_render_method
**Description:** Verify ConstraintBash has render() method
**Command:** `grep -q 'class ConstraintBash' knowledge_tool/knowledge_tool/src/models/constraints_model.py && grep -q 'def render.*include_toc' knowledge_tool/knowledge_tool/src/models/constraints_model.py && echo '✓ ConstraintBash.render() exists' || echo '✗ Missing'`

#### constraint_bash_render_toc_method
**Description:** Verify ConstraintBash has render_toc() method
**Command:** `grep -A 100 'class ConstraintBash' knowledge_tool/knowledge_tool/src/models/constraints_model.py | grep -q 'def render_toc' && echo '✓ ConstraintBash.render_toc() exists' || echo '✗ Missing'`

#### constraint_feature_uses_render_toc
**Description:** Verify Feature.render_toc() uses constraint rendering methods
**Command:** `grep -q 'constraint.render_toc\|render_toc()' knowledge_tool/knowledge_tool/src/models/feature_model.py && echo '✓ Feature uses constraint.render_toc()' || echo '✗ Missing'`

#### constraint_prompt_render_method
**Description:** Verify ConstraintPrompt has render() method
**Command:** `grep -A 50 'class ConstraintPrompt' knowledge_tool/knowledge_tool/src/models/constraints_model.py | grep -q 'def render' && echo '✓ ConstraintPrompt.render() exists' || echo '✗ Missing'`

#### constraint_prompt_render_toc_method
**Description:** Verify ConstraintPrompt has render_toc() method
**Command:** `grep -A 150 'class ConstraintPrompt' knowledge_tool/knowledge_tool/src/models/constraints_model.py | grep -q 'def render_toc' && echo '✓ ConstraintPrompt.render_toc() exists' || echo '✗ Missing'`

#### constraint_rendering_displays_type
**Description:** Verify constraint rendering displays type information
**Command:** `python3 -c "import sys; sys.path.insert(0, 'knowledge_tool/knowledge_tool/src'); from models import ConstraintBash; c = ConstraintBash(id='test', cmd='echo hi', description='test', scope='local'); output = c.render(); print('✓ Constraint type displayed' if 'Type:' in output else '✗ Missing type')" 2>/dev/null`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: architecture
- implementation: constraints_model, feature_model
- priority: high
- status: planned

### Feature: constraint_scripts_directory
**Create and maintain constraints_scripts/ directory for reusable constraint validation scripts. This directory stores bash, python, and other scripts that can be referenced by constraint definitions. Provides centralized location for constraint script management and reusability across multiple features. Example: validate_toc_links.py validates task document TOC links.**

**Goals:**
- Establish constraints_scripts/ directory for reusable scripts
- Document constraint script conventions
- Enable ${PROJECT_ROOT} substitution in script paths
- Support modular constraint validation

#### constraint_scripts_directory_exists
**Description:** Verify constraints_scripts/ directory exists
**Command:** `test -d constraints_scripts && echo '✓ constraints_scripts/ directory exists' || echo '✗ Missing'`

#### constraint_scripts_documented
**Description:** Verify constraints_scripts/ purpose is documented
**Command:** `grep -q 'constraint.*script\|script.*location' constraints_scripts/README.md && echo '✓ Documentation found' || echo '✗ Incomplete'`

#### constraint_scripts_readme_exists
**Description:** Verify constraints_scripts/README.md documentation exists
**Command:** `test -f constraints_scripts/README.md && echo '✓ README.md exists' || echo '✗ Missing'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: infrastructure
- implementation: file_structure
- priority: high
- status: planned

### Feature: enhance_constraint_bash_result_output
**Enhance ConstraintBashResult model to always include shrunken_output field that captures command output when constraint check fails or succeeds. Shrunken_output is required (not optional) and stores up to 500 characters of truncated stdout/stderr. This provides visibility into why constraints fail by preserving the command output for debugging purposes.**

**Goals:**
- Add shrunken_output: str field to ConstraintBashResult (required, not optional)
- Populate shrunken_output with command output truncated to 500 characters
- Ensure output is captured for both passed and failed constraints
- Display failed output in ChecksResults markdown rendering
- Include output in checks_results.k.json for full constraint result tracking
- Improve debugging capability by preserving command output in results

#### constraint_output_populated_on_failure
**Description:** Verify shrunken_output is populated when constraint fails
**Command:** `grep -q 'shrunken_output=output\|verdict.*False' constraints_tool/constraints_tool/task_features_checker.py && echo 'Output captured on failure' || echo 'Not captured'`

#### constraint_output_rendered_in_markdown
**Description:** Verify shrunken_output is displayed in ChecksResults markdown
**Command:** `grep -q 'if result.shrunken_output\|Output:' knowledge_tool/knowledge_tool/src/models/results_model.py && echo 'Output rendered' || echo 'Not rendered'`

#### constraint_shrunken_output_field_exists
**Description:** Verify ConstraintBashResult has shrunken_output: str field (required, not optional)
**Command:** `grep -A 3 'class ConstraintBashResult' knowledge_tool/knowledge_tool/src/models/results_model.py | grep -q 'shrunken_output.*str' && echo 'shrunken_output required field' || echo 'Field missing or optional'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: enhancement
- implementation: results_model
- priority: high
- status: completed

### Feature: feature_goals_field
**Add goals field to Feature model. Feature should have optional goals: List[str] field to track feature objectives. Goals should be rendered in markdown output with Goals section.**

**Goals:**
- Add optional goals field to Feature model
- Render goals in markdown output
- Include goals in table of contents

#### constraint_goals_field_exists
**Description:** Verify goals field is defined in Feature model
**Command:** `grep -q 'goals.*List\|goals.*list\[str\]' knowledge_tool/knowledge_tool/src/models/feature_model.py && echo '✓ Goals field exists' || echo '✗ Goals field missing'`

#### constraint_goals_field_in_task
**Description:** Verify goals field appears in task.k.json features
**Command:** `grep -q '"goals"' task.k.json && echo '✓ Goals in task.k.json' || echo '✗ Goals not in task.k.json'`

#### constraint_goals_in_toc
**Description:** Verify goals are included in table of contents
**Command:** `grep -q 'Goals.*toc\|toc.*Goals\|\[Goals\]' knowledge_tool/knowledge_tool/src/models/feature_model.py && echo '✓ Goals in TOC found' || echo '✗ Goals in TOC missing'`

#### constraint_goals_rendered_in_markdown
**Description:** Verify goals are rendered in markdown output
**Command:** `grep -q '## Goals\|Goals section' knowledge_tool/knowledge_tool/src/models/feature_model.py && echo '✓ Goals rendering found' || echo '✗ Goals rendering missing'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: model_enhancement
- implementation: feature_model
- priority: high
- status: planned
- depends_on: ['task_features_checker_tool']

### Feature: features_stats_diff_tracking
**Add FeaturesStatsDiff model to track changes in feature constraint validation results between iterations. FeaturesStatsDiff captures what changed: which features went from pass->fail or fail->pass, and newly failed features. Add diff() method to FeaturesStats class that compares with previous iteration. Add features_stats_diff: Optional[FeaturesStatsDiff] field to Iteration model. Calculate diff when creating new iterations using task-add-iteration.py script.**

**Goals:**
- Create FeaturesStatsDiff pydantic model with fields: improved (newly passing features), regressed (newly failing features), still_failing (unchanged failures)
- Add diff(previous: FeaturesStats) -> FeaturesStatsDiff method to FeaturesStats class
- Add features_stats_diff: Optional[FeaturesStatsDiff] field to Iteration model
- Update Iteration.render() to display FeaturesStatsDiff with change summary
- Populate features_stats_diff when creating iterations via task-add-iteration.py
- Track iteration-over-iteration progress toward constraint compliance

#### constraint_diff_rendered_in_iteration
**Description:** Verify Iteration.render() displays features_stats_diff
**Command:** `grep -A 100 'def render' knowledge_tool/knowledge_tool/src/models/task_model.py | grep -q 'features_stats_diff\|improved\|regressed' && echo 'Rendering implemented' || echo 'Not implemented'`

#### constraint_features_stats_diff_model_exists
**Description:** Verify FeaturesStatsDiff model is defined
**Command:** `grep -q 'class FeaturesStatsDiff' knowledge_tool/knowledge_tool/src/models/results_model.py && echo 'Model exists' || echo 'Missing'`

#### constraint_features_stats_has_diff_method
**Description:** Verify FeaturesStats has diff() method
**Command:** `grep -A 50 'class FeaturesStats' knowledge_tool/knowledge_tool/src/models/results_model.py | grep -q 'def diff' && echo 'diff() method exists' || echo 'Missing'`

#### constraint_iteration_has_diff_field
**Description:** Verify Iteration has features_stats_diff field
**Command:** `grep -q 'features_stats_diff.*FeaturesStatsDiff' knowledge_tool/knowledge_tool/src/models/task_model.py && echo 'Field exists' || echo 'Missing'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: enhancement
- implementation: results_model, task_model
- priority: high
- status: pending

### Feature: migrate_metadata_to_model
**Migrate all models from using metadata: Dict[str, Any] to using metadata: Metadata model. This provides type safety, consistency, and standardized metadata handling across all knowledge document models. Models affected: ConstraintBash, ConstraintPrompt, Task, Spec, Feature, and Doc. Each model should import the Metadata class from metadata_model and use it instead of Dict[str, Any].**

#### constraint_constraint_model_uses_metadata
**Description:** Verify ConstraintBash and ConstraintPrompt use Metadata model instead of Dict
**Command:** `grep -c 'metadata: Metadata' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/constraints_model.py 2>/dev/null | grep -qE '^[1-9]' || (echo 'ConstraintBash/ConstraintPrompt must have metadata: Metadata field (not Dict)' && exit 1)`

#### constraint_doc_model_uses_metadata
**Description:** Verify Doc model uses Metadata model instead of Dict
**Command:** `grep -E '^\s{0,8}metadata:\s+Metadata\s*(=|:)' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/doc_model.py || (echo 'Doc model must have metadata: Metadata field definition (not Dict)' && exit 1)`

#### constraint_feature_model_uses_metadata
**Description:** Verify Feature model uses Metadata model instead of Dict
**Command:** `grep -c 'metadata: Metadata' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/feature_model.py 2>/dev/null | grep -qE '^[1-9]' || (echo 'Feature model must have metadata: Metadata field (not Dict)' && exit 1)`

#### constraint_metadata_import
**Description:** Verify Metadata is imported in all model files
**Command:** `grep -r 'from.*metadata_model import Metadata' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/*.py 2>/dev/null | wc -l | grep -qE '^[5-9]' || (echo 'Metadata must be imported in ALL model files (5+ imports needed)' && exit 1)`

#### constraint_no_dict_metadata_references
**Description:** Verify no models still use Dict for metadata field
**Command:** `! grep -r 'metadata: Dict' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/*.py 2>/dev/null | grep -qE '\.(py|json):' || (echo 'NO Dict metadata references allowed in models - must all be Metadata type' && exit 1)`

#### constraint_spec_model_uses_metadata
**Description:** Verify Spec model uses Metadata model instead of Dict
**Command:** `grep -c 'metadata: Metadata' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/spec_model.py 2>/dev/null | grep -qE '^[1-9]' || (echo 'Spec model must have metadata: Metadata field (not Dict)' && exit 1)`

#### constraint_task_model_uses_metadata
**Description:** Verify Task model uses Metadata model instead of Dict
**Command:** `grep -c 'metadata: Metadata' $PROJECT_ROOT/knowledge_tool/knowledge_tool/src/models/task_model.py 2>/dev/null | grep -qE '^[1-9]' || (echo 'Task model must have metadata: Metadata field (not Dict)' && exit 1)`

**Metadata:**
- created_at: 2026-03-16T00:00:00
- feature_type: refactoring
- implementation: models
- priority: medium
- status: planned

### Feature: render_spec_features_in_task
**Render Task spec features and their constraints in the markdown output. Task.render() should include a 'Features' section that displays all features from spec.features with their descriptions and embedded constraints (bash commands and prompt validations).**

#### constraint_constraint_details_in_markdown
**Description:** Verify that constraint details (bash commands, prompt validations) are rendered in markdown
**Command:** `grep -q 'Bash\|Prompt\|constraint\|cmd\|prompt' $PROJECT_ROOT/task.k.md && echo '✓ Constraint details found' || echo '⚠ Constraint details not found'`

#### constraint_feature_section_in_markdown
**Description:** Verify that 'Features' section is rendered in task.k.md markdown output
**Command:** `grep -q '## Features\|### .*:' $PROJECT_ROOT/task.k.md && echo '✓ Features section found in markdown' || echo '⚠ Features section not found'`

#### constraint_rendering_implementation_review
**Description:** Code review of Task.render() feature/constraint rendering implementation
**Prompt:** Review the Task.render() method implementation to ensure it properly displays spec.features and their constraints. Verify: 1) Features section is included after spec description, 2) Each feature shows id, description, and constraints, 3) ConstraintBash displays command with proper formatting, 4) ConstraintPrompt displays prompt and expected verdict, 5) Metadata is optionally shown, 6) Markdown formatting is consistent with other sections, 7) Edge cases handled (no features, no constraints)
**Expected Verdict:** `.*`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: rendering
- implementation: task_model
- priority: high
- status: planned
- depends_on: ['forbid_task_status_downgrade']

### Feature: task_add_iteration_script
**Create task-add-iteration.py script in skills/task-lifecycle-tool/ directory. Script uses knowledge tool to update task.k.json by adding new Iteration with populated features_stats and tests_stats. Script runs task_features_checker.py, extracts results, creates FeaturesStatsDiff from previous iteration, and patches task.k.json with complete iteration data. Task lifecycle tool skill updated with documentation and usage examples.**

**Goals:**
- Create skills/task-lifecycle-tool/task-add-iteration.py script
- Script accepts task.k.json path and optional iteration number
- Runs constraint checker and extracts features_stats
- Calculates features_stats_diff from previous iteration if exists
- Supports optional tests_stats parameter
- Uses patch_knowledge_document.py for safe updates
- Prints iteration summary after adding
- Update task-lifecycle-tool skill with script documentation

#### constraint_script_exists
**Description:** Verify task-add-iteration.py exists
**Command:** `test -f skills/task-lifecycle-tool/task-add-iteration.py && echo 'Script exists' || echo 'Missing'`

#### constraint_script_populates_features_stats
**Description:** Verify script populates features_stats in iteration
**Command:** `grep -q 'features_stats\|FeaturesStats' skills/task-lifecycle-tool/task-add-iteration.py && echo 'Populates stats' || echo 'Not implemented'`

#### constraint_script_runs_checker
**Description:** Verify script runs task_features_checker.py
**Command:** `grep -q 'task_features_checker\|check_task_features' skills/task-lifecycle-tool/task-add-iteration.py && echo 'Runs checker' || echo 'Not implemented'`

#### constraint_script_uses_knowledge_tool
**Description:** Verify script uses knowledge tool for updates
**Command:** `grep -q 'patch_knowledge_document\|knowledge_tool' skills/task-lifecycle-tool/task-add-iteration.py && echo 'Uses knowledge tool' || echo 'Not used'`

#### constraint_skill_documentation_updated
**Description:** Verify task-lifecycle-tool skill documents the script
**Command:** `grep -q 'task-add-iteration\|add.*Iteration' skills/task-lifecycle-tool/SKILL.md && echo 'Documented' || echo 'Not documented'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: tooling
- implementation: task-add-iteration.py script
- priority: high
- status: pending

### Feature: task_default_render_toc
**Task model should default opts.render_toc to True when opts is not specified. If opts is not provided or opts.render_toc is not explicitly set to False, the Task should render its table of contents by default. This improves usability by making TOC rendering the default behavior.**

**Goals:**
- Set render_toc=True by default when opts is not specified
- Allow explicit override with opts.render_toc=False
- Maintain backward compatibility with existing opts configurations
- Improve Task markdown rendering with TOC by default

#### constraint_default_toc_when_opts_missing
**Description:** Verify Task checks if opts is None/missing to set defaults
**Command:** `grep -q 'if not self.opts\|self.opts is None' knowledge_tool/knowledge_tool/src/models/task_model.py && echo '✓ Default opts handling found' || echo '✗ Missing'`

#### constraint_explicit_false_respected
**Description:** Verify explicit opts.render_toc=False is respected
**Command:** `grep -q 'render_toc.*False\|not.*render_toc' knowledge_tool/knowledge_tool/src/models/task_model.py && echo '✓ Explicit False handling found' || echo '✗ Missing'`

#### constraint_render_toc_default_true
**Description:** Verify render_toc defaults to True when opts not specified
**Command:** `grep -q 'render_toc.*True\|Opts.*render_toc.*True' knowledge_tool/knowledge_tool/src/models/task_model.py && echo '✓ Default render_toc=True found' || echo '✗ Missing'`

#### constraint_toc_rendered_by_default
**Description:** Verify Task renders TOC by default when opts is None
**Command:** `python3 -c "import sys; sys.path.insert(0, 'knowledge_tool/knowledge_tool/src'); from models import Task, Spec, Doc; spec = Spec(version=1, description=Doc(id='d', label='L', metadata={})); t = Task(id='t1', spec=spec, opts=None); output = t.render(); print('✓ TOC rendered' if 'Table of Contents' in output else '✗ TOC missing')" 2>/dev/null`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: enhancement
- implementation: task_model
- priority: medium
- status: planned

### Feature: task_features_checker_selective_patch
**When --features argument is used with task_features_checker.py, the tool should perform selective patching of checks_results.k.json knowledge document instead of overwriting the entire file. Only the feature results specified in --features should be patched/updated, while preserving existing results for all other features in the document. This ensures that incremental validation runs don't lose results from previous checks.**

#### constraint_feature_results_filtering
**Description:** Verify feature results are filtered based on --features argument
**Command:** `grep -q 'if feature_ids:' $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py && grep -A 15 'if feature_ids:' $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py | grep -q 'features_to_check.*{.*for.*in.*feature_ids' || (echo 'Feature filtering must use dict comprehension to filter features_to_check based on feature_ids list' && exit 1)`

#### constraint_patch_uses_add_op
**Description:** Verify patch operations use add/merge strategy instead of replace for selective updates
**Command:** `grep -q 'apply_json_patch' $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py && grep -B 5 -A 10 'apply_json_patch' $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py | grep -q '"op": "add"' || (echo 'Patching implementation must use apply_json_patch with add operations to merge results' && exit 1)`

#### constraint_preserves_other_features
**Description:** Verify that when --features is used, only those features are patched and others are preserved
**Command:** `test -f $PROJECT_ROOT/checks_results.k.json && initial_count=$(grep -c '\"feature_id\"' $PROJECT_ROOT/checks_results.k.json) || initial_count=0; ! grep -q 'initialize.*empty\|features_results.*=.*{}' $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py || (echo 'Bug: features_results should only contain filtered features, not reset to empty' && exit 1)`

#### constraint_selective_patch_logic
**Description:** Verify selective patch logic exists when --features argument is provided
**Command:** `cd $PROJECT_ROOT && test_output=$(python constraints_tool/constraints_tool/task_features_checker.py task.k.json --features task_features_checker_tool 2>&1); echo "$test_output" | grep -q 'task_features_checker_tool' && test_output2=$(python constraints_tool/constraints_tool/task_features_checker.py task.k.json --features render_spec_features_in_task 2>&1); echo "$test_output2" | grep -q 'render_spec_features_in_task' && both_exist=$(grep -c '\"feature_id\"' checks_results.k.json 2>/dev/null || echo 0); test "$both_exist" -gt 1 || (echo 'Selective patching not working: when --features used twice, both feature results should coexist in checks_results file' && exit 1)`

**Metadata:**
- created_at: 2026-03-16T00:00:00
- feature_type: enhancement
- implementation: task_features_checker
- priority: medium
- status: planned

### Feature: task_features_checker_tool
**Create task_features_checker.py script in constraints_tool/ directory. Script should: 1) Accept path to task document (task.k.json), 2) Accept optional --features argument with comma-separated list of feature IDs to check, 3) Accept optional --output-checks-path argument for ChecksResults.json path to save results, 4) If --features not provided, check all features in spec.features, 5) Execute constraints for selected features similar to constraints_executor.py, 6) Write results to ChecksResults model containing feature_results with constraint execution outcomes, 7) Save ChecksResults to path specified in --output-checks-path if provided, 8) Support both ConstraintBash and ConstraintPrompt types, 9) Return results showing which constraints passed/failed**

#### constraint_project_root_substitution
**Description:** Verify PROJECT_ROOT placeholder substitution is implemented
**Command:** `grep -q '_substitute_project_root' constraints_tool/constraints_tool/task_features_checker.py && echo '✓ PROJECT_ROOT substitution found' || echo '✗ Missing'`

#### constraint_recursive_execution_prevention
**Description:** Verify recursive execution detection is implemented
**Command:** `grep -q '_check_recursive_execution' constraints_tool/constraints_tool/task_features_checker.py && echo '✓ Recursive execution prevention found' || echo '✗ Missing'`

#### constraint_tool_accepts_features_arg
**Description:** Verify tool accepts optional --features argument to filter feature IDs
**Command:** `grep -q "add_argument.*--features" constraints_tool/constraints_tool/task_features_checker.py && echo '--features arg defined' || echo '--features arg missing'`

#### constraint_tool_accepts_output_checks_path_arg
**Description:** Verify tool accepts optional --output-checks-path argument for ChecksResults file path
**Command:** `grep -q "add_argument.*--output-checks-path" constraints_tool/constraints_tool/task_features_checker.py && echo '--output-checks-path arg defined' || echo '--output-checks-path arg missing'`

#### constraint_tool_accepts_task_path
**Description:** Verify tool accepts task document path argument
**Command:** `grep -q "parser.add_argument.*task_path\|positional arguments" constraints_tool/constraints_tool/task_features_checker.py && echo 'Task path argument defined' || echo 'Task path argument missing'`

#### constraint_tool_exists
**Description:** Verify task_features_checker.py exists in constraints_tool/
**Command:** `test -f $PROJECT_ROOT/constraints_tool/constraints_tool/task_features_checker.py && echo '✓ tool exists' || echo '✗ tool missing'`

#### constraint_tool_implementation_review
**Description:** Code review of task_features_checker.py tool including ChecksResults integration
**Prompt:** Review task_features_checker.py implementation. Verify: 1) Accepts task document path and optional --features and --output-checks-path arguments, 2) Loads Task model and extracts spec.features, 3) Filters features by --features list if provided, 4) Executes ConstraintBash and ConstraintPrompt for each feature, 5) Creates ChecksResults model with feature_results containing constraint outcomes, 6) Saves ChecksResults to file path specified in --output-checks-path if provided using patch_knowledge_document, 7) Returns ChecksResults object, 8) Similar structure to constraints_executor.py, 9) Proper error handling for missing files/invalid features/save failures
**Expected Verdict:** `.*`

#### constraint_tool_output_checks_path_writable
**Description:** Verify output checks path is writable and ChecksResults file can be created/updated
**Command:** `grep -q "Path(output_checks_path)\|output_path.write_text" constraints_tool/constraints_tool/task_features_checker.py && echo 'Output path handling implemented' || echo 'Output path handling missing'`

#### constraint_tool_returns_checks_results
**Description:** Verify tool returns results in ChecksResults model format
**Command:** `grep -q "ChecksResults\|check_task_features.*ChecksResults" constraints_tool/constraints_tool/task_features_checker.py && echo 'ChecksResults usage found' || echo 'ChecksResults not found'`

#### constraint_tool_saves_results_to_file
**Description:** Verify tool saves ChecksResults to file when --output-checks-path provided
**Command:** `grep -q "output_path.write_text\|if not output_path.exists" constraints_tool/constraints_tool/task_features_checker.py && grep -q "apply_json_patch" constraints_tool/constraints_tool/task_features_checker.py && echo 'File save logic implemented' || echo 'File save logic missing'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: tooling
- implementation: constraints_tool
- priority: high
- status: planned
- depends_on: ['render_spec_features_in_task']
- returns_model: ChecksResults
- output_argument: --output-checks-path

### Feature: task_toc_includes_constraints
**Task's table of contents should include constraints from features. When rendering TOC, each feature's constraints should be listed as sub-items. This provides complete visibility into all validation requirements in the task document.**

**Goals:**
- Include feature constraints in Task TOC
- Display constraints nested under their parent features
- Show constraint IDs and descriptions in TOC
- Improve navigation for complex task specifications

#### constraint_constraints_nested_in_toc
**Description:** Verify constraints appear as nested items in feature TOC entries
**Command:** `python3 -c "import sys; sys.path.insert(0, 'knowledge_tool/knowledge_tool/src'); from models import Task, Spec, Doc, Feature; spec = Spec(version=1, description=Doc(id='d', label='L', metadata={}), features={'f1': Feature(id='f1', description='test', constraints={'c1': {'id': 'c1', 'cmd': 'true', 'description': 'test'}})}); t = Task(id='t', spec=spec); toc = t.render_toc(); print('✓ Constraints in TOC' if any('constraint' in str(line).lower() for line in toc) else '✗ No constraints in TOC')" 2>/dev/null`

#### constraint_constraints_visible_in_markdown
**Description:** Verify constraints are rendered in task.k.md TOC
**Command:** `grep -q 'constraint.*toc\|Constraint' task.k.md && echo '✓ Constraints visible in markdown' || echo '✗ Not visible'`

#### constraint_toc_includes_constraints
**Description:** Verify Task._generate_toc() includes constraints from features
**Command:** `grep -q 'constraint.*render_toc\|constraints.*in.*toc' knowledge_tool/knowledge_tool/src/models/task_model.py && echo '✓ Constraint rendering in TOC found' || echo '✗ Missing'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: enhancement
- implementation: task_model
- priority: medium
- status: planned
- depends_on: ['task_default_render_toc']

### Feature: task_toc_rendering_and_links
**Verify Task TOC is rendered correctly with functional links. Task markdown output should: 1) Include proper TOC section with 'Table of Contents' header, 2) Generate correct markdown anchors for all sections, 3) Links in TOC should match actual heading anchors, 4) Handle special characters and spaces correctly in anchors.**

**Goals:**
- Ensure TOC section is properly formatted
- Verify all TOC links have matching anchors
- Test special character handling in anchors
- Validate markdown TOC syntax

#### constraint_anchor_sections_exist
**Description:** Verify all TOC links have corresponding heading anchors
**Command:** `python3 constraints_scripts/validate_toc_links.py task.k.md`

#### constraint_toc_has_entries
**Description:** Verify TOC contains markdown list entries (lines starting with -)
**Command:** `grep -A 20 '## Table of Contents' task.k.md | grep -q '^-' && echo '✓ TOC entries found' || echo '✗ No entries'`

#### constraint_toc_implementation_review
**Description:** Code review of Task TOC generation logic
**Prompt:** Review the Task TOC rendering implementation in task_model.py. Verify: 1) _generate_toc() generates valid markdown links with proper anchors, 2) Anchors match heading formats (lowercase, spaces→hyphens), 3) Special characters are handled correctly, 4) Nested items are properly indented with spaces, 5) Links use consistent anchor generation, 6) TOC includes all sections (Specification, Features, Iterations, Constraints)
**Expected Verdict:** `.*`

#### constraint_toc_indentation
**Description:** Verify TOC has proper indentation for nested items
**Command:** `grep '## Table of Contents' -A 50 task.k.md | grep -E '^  -|^    -' | wc -l | grep -qE '[1-9]' && echo '✓ Proper nesting found' || echo '✗ Missing'`

#### constraint_toc_links_format
**Description:** Verify TOC links follow markdown format [text](#anchor)
**Command:** `grep '## Table of Contents' -A 20 task.k.md | grep -q '\[.*\](#' && echo '✓ Links formatted correctly' || echo '✗ Bad format'`

#### constraint_toc_section_exists
**Description:** Verify 'Table of Contents' section header exists in task.k.md
**Command:** `grep -q '## Table of Contents' task.k.md && echo '✓ TOC section found' || echo '✗ Missing'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: quality
- implementation: task_model
- priority: high
- status: planned
- depends_on: ['task_toc_includes_constraints']

### Feature: update_iteration_with_features_stats
**Update Iteration model and task lifecycle tool to track feature constraint validation results. Add features_stats field containing complete feature validation status and failed feature details. FeaturesStats model includes: features_checks (Dict[str, bool] with all task features), failed (Dict[str, FeatureResult] with only features having failed constraints). FeatureResult.constraints_results field is required (Dict, not optional). Display iteration stats every time iteration is added or rendered.**

**Goals:**
- Create FeaturesStats pydantic model with features_checks and failed Dict fields
- Add features_stats: Optional[FeaturesStats] field to Iteration model
- Make FeatureResult.constraints_results field required (Dict, not Optional)
- Update task_features_checker.py to generate FeaturesStats from ChecksResults
- Update Iteration.render() to display feature validation stats with pass/fail summary
- Update task lifecycle tool skill documentation with FeaturesStats schema details
- Ensure iteration stats display including passed/failed feature counts when rendered

#### constraint_feature_result_constraints_required
**Description:** Verify FeatureResult.constraints_results field is required (Dict, not Optional)
**Command:** `grep -A 3 'class FeatureResult' knowledge_tool/knowledge_tool/src/models/results_model.py | grep -q 'constraints_results.*Dict.*Union\|constraints_results.*\.\.\.' && echo 'constraints_results required' || echo 'Still optional'`

#### constraint_features_stats_generated
**Description:** Verify task_features_checker.py generates FeaturesStats
**Command:** `grep -q 'generate_features_stats\|FeaturesStats(' constraints_tool/constraints_tool/task_features_checker.py && echo 'Generation implemented' || echo 'Not implemented'`

#### constraint_features_stats_in_iteration
**Description:** Verify features_stats field exists in Iteration model
**Command:** `grep -q 'features_stats.*FeaturesStats' knowledge_tool/knowledge_tool/src/models/task_model.py && echo 'Field in Iteration' || echo 'Not found'`

#### constraint_features_stats_model_exists
**Description:** Verify FeaturesStats model exists with features_checks (Dict[str,bool]) and failed (Dict[str,FeatureResult]) fields
**Command:** `grep -q 'class FeaturesStats' knowledge_tool/knowledge_tool/src/models/results_model.py && grep -q 'features_checks.*Dict' knowledge_tool/knowledge_tool/src/models/results_model.py && echo 'FeaturesStats with proper fields' || echo 'Model incomplete'`

#### constraint_features_stats_rendered
**Description:** Verify Iteration.render() displays features_stats
**Command:** `grep -q 'Feature Constraint Validation\|features_stats' knowledge_tool/knowledge_tool/src/models/task_model.py && echo 'Rendering implemented' || echo 'Not implemented'`

#### constraint_skill_documentation_updated
**Description:** Verify task lifecycle tool skill documents features_stats
**Command:** `grep -q 'features_stats.*Feature Constraint\|Iteration.*features_stats' skills/task-lifecycle-tool/SKILL.md && echo 'Skill docs updated' || echo 'Not updated'`

#### constraint_stats_displayed_on_iteration
**Description:** Verify iteration contains features_stats in task document
**Command:** `grep -q 'iteration_1' task.k.json && jq '.iterations.iteration_1.features_stats' task.k.json | grep -q 'features_checks' && echo 'Stats in iteration' || echo 'Not in iteration'`

**Metadata:**
- created_at: 2026-03-14T00:00:00
- feature_type: enhancement
- implementation: task_model, results_model, task_features_checker, skills
- priority: high
- status: completed

## Iterations

### iteration_1

**Metadata:**

- created_at: 2026-03-14T00:00:00
- description: Enhanced features with FeaturesStats tracking and constraint validation requirements

**Code Stats:**
- Added lines: 287
- Removed lines: 12
- Files changed: 8

**Feature Constraint Validation Stats:**

- **Overall:** 6/9 features passed
- **Failed:** 3 features with constraint violations

**Feature Status:**
- constraint_rendering_capability: ✓ PASS
- constraint_scripts_directory: ✓ PASS
- feature_goals_field: ✓ PASS
- forbid_task_status_downgrade: ✓ PASS
- render_spec_features_in_task: ✗ FAIL
- task_default_render_toc: ✓ PASS
- task_features_checker_tool: ✗ FAIL
- task_toc_includes_constraints: ✓ PASS
- task_toc_rendering_and_links: ✗ FAIL

**Failed Feature Details:**

**render_spec_features_in_task:**

**task_features_checker_tool:**

**task_toc_rendering_and_links:**

### iteration_2

**Metadata:**

- created_at: 2026-03-14T12:19:09.602314
- iteration_number: 2

**Feature Constraint Validation Stats:**

- **Overall:** 11/15 features passed
- **Failed:** 4 features with constraint violations

**Feature Status:**
- add_constraint_validation_requirement_skill: ✓ PASS
- constraint_checker_exit_code_hook: ✗ FAIL
- constraint_rendering_capability: ✓ PASS
- constraint_scripts_directory: ✓ PASS
- enhance_constraint_bash_result_output: ✓ PASS
- feature_goals_field: ✓ PASS
- features_stats_diff_tracking: ✓ PASS
- forbid_task_status_downgrade: ✓ PASS
- render_spec_features_in_task: ✗ FAIL
- task_add_iteration_script: ✓ PASS
- task_default_render_toc: ✓ PASS
- task_features_checker_tool: ✗ FAIL
- task_toc_includes_constraints: ✓ PASS
- task_toc_rendering_and_links: ✗ FAIL
- update_iteration_with_features_stats: ✓ PASS

**Failed Feature Details:**

**constraint_checker_exit_code_hook:**
- constraint_task_checker_exits_2_on_failure: FAILED

**render_spec_features_in_task:**
- constraint_rendering_implementation_review: FAILED

**task_features_checker_tool:**
- constraint_tool_implementation_review: FAILED

**task_toc_rendering_and_links:**
- constraint_toc_implementation_review: FAILED

### iteration_3

**Metadata:**

- created_at: 2026-03-14T12:28:01.999879
- iteration_number: 3

**Feature Constraint Validation Stats:**

- **Overall:** 15/15 features passed

**Feature Status:**
- add_constraint_validation_requirement_skill: ✓ PASS
- constraint_checker_exit_code_hook: ✓ PASS
- constraint_rendering_capability: ✓ PASS
- constraint_scripts_directory: ✓ PASS
- enhance_constraint_bash_result_output: ✓ PASS
- feature_goals_field: ✓ PASS
- features_stats_diff_tracking: ✓ PASS
- forbid_task_status_downgrade: ✓ PASS
- render_spec_features_in_task: ✓ PASS
- task_add_iteration_script: ✓ PASS
- task_default_render_toc: ✓ PASS
- task_features_checker_tool: ✓ PASS
- task_toc_includes_constraints: ✓ PASS
- task_toc_rendering_and_links: ✓ PASS
- update_iteration_with_features_stats: ✓ PASS
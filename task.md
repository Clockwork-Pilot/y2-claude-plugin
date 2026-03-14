# Task: task_1

## Table of Contents

- [Specification (v1)](#specification-v1)
- [Features](#features)
    - [Feature: add_constraint_validation_requirement_skill](#feature-add_constraint_validation_requirement_skill)
      - [constraint_requirement_section_exists](#constraint_requirement_section_exists)
      - [constraint_results_interpretation_guide](#constraint_results_interpretation_guide)
      - [constraint_when_to_run_documented](#constraint_when_to_run_documented)
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
    - [Feature: forbid_task_status_downgrade](#feature-forbid_task_status_downgrade)
      - [constraint_status_locked_in_executing](#constraint_status_locked_in_executing)
      - [constraint_status_validation_exists](#constraint_status_validation_exists)
    - [Feature: render_spec_features_in_task](#feature-render_spec_features_in_task)
      - [constraint_constraint_details_in_markdown](#constraint_constraint_details_in_markdown)
      - [constraint_feature_section_in_markdown](#constraint_feature_section_in_markdown)
      - [constraint_rendering_implementation_review](#constraint_rendering_implementation_review)
    - [Feature: task_default_render_toc](#feature-task_default_render_toc)
      - [constraint_default_toc_when_opts_missing](#constraint_default_toc_when_opts_missing)
      - [constraint_explicit_false_respected](#constraint_explicit_false_respected)
      - [constraint_render_toc_default_true](#constraint_render_toc_default_true)
      - [constraint_toc_rendered_by_default](#constraint_toc_rendered_by_default)
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
- Include output in checks_results.json for full constraint result tracking
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
**Description:** Verify goals field appears in task.json features
**Command:** `grep -q '"goals"' task.json && echo '✓ Goals in task.json' || echo '✗ Goals not in task.json'`

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

### Feature: forbid_task_status_downgrade
**Prevent Task status changes once in executing state. Implementation: Use validation in PLUGIN_ROOT/hooks/ or patch_knowledge_document to ensure: 1) Status can only transition: planning → executing, 2) Once in executing state, no further status changes are allowed (locked state), 3) Reject any attempts to manually change status from executing/failed/succeed with clear error messages**

#### constraint_status_locked_in_executing
**Description:** Verify status is locked when task in executing state
**Command:** `python3 knowledge_tool/knowledge_tool/patch_knowledge_document.py task.json '[{"op": "replace", "path": "/status", "value": "succeed"}]' 2>&1 | grep -q 'locked\|not allowed' && echo '✓ Status locked' || echo '✗ Locked check failed'`

#### constraint_status_validation_exists
**Description:** Verify status validation code exists in hooks directory
**Command:** `grep -r 'forbid.*downgrade\|status.*validation\|executing.*planning\|failed.*planning\|succeed.*planning' $PROJECT_ROOT/hooks/ && echo 'Hook validation found'`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: validation
- implementation: hooks
- priority: high
- status: planned

### Feature: render_spec_features_in_task
**Render Task spec features and their constraints in the markdown output. Task.render() should include a 'Features' section that displays all features from spec.features with their descriptions and embedded constraints (bash commands and prompt validations).**

#### constraint_constraint_details_in_markdown
**Description:** Verify that constraint details (bash commands, prompt validations) are rendered in markdown
**Command:** `grep -q 'Bash\|Prompt\|constraint\|cmd\|prompt' $PROJECT_ROOT/task.md && echo '✓ Constraint details found' || echo '⚠ Constraint details not found'`

#### constraint_feature_section_in_markdown
**Description:** Verify that 'Features' section is rendered in task.md markdown output
**Command:** `grep -q '## Features\|### .*:' $PROJECT_ROOT/task.md && echo '✓ Features section found in markdown' || echo '⚠ Features section not found'`

#### constraint_rendering_implementation_review
**Description:** Code review of Task.render() feature/constraint rendering implementation
**Prompt:** Review the Task.render() method implementation to ensure it properly displays spec.features and their constraints. Verify: 1) Features section is included after spec description, 2) Each feature shows id, description, and constraints, 3) ConstraintBash displays command with proper formatting, 4) ConstraintPrompt displays prompt and expected verdict, 5) Metadata is optionally shown, 6) Markdown formatting is consistent with other sections, 7) Edge cases handled (no features, no constraints)
**Expected Verdict:** `PASS`

**Metadata:**
- created_at: 2026-03-13T00:00:00
- feature_type: rendering
- implementation: task_model
- priority: high
- status: planned
- depends_on: ['forbid_task_status_downgrade']

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

### Feature: task_features_checker_tool
**Create task_features_checker.py script in constraints_tool/ directory. Script should: 1) Accept path to task document (task.json), 2) Accept optional --features argument with comma-separated list of feature IDs to check, 3) Accept optional --output-checks-path argument for ChecksResults.json path to save results, 4) If --features not provided, check all features in spec.features, 5) Execute constraints for selected features similar to constraints_executor.py, 6) Write results to ChecksResults model containing feature_results with constraint execution outcomes, 7) Save ChecksResults to path specified in --output-checks-path if provided, 8) Support both ConstraintBash and ConstraintPrompt types, 9) Return results showing which constraints passed/failed**

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
**Expected Verdict:** `PASS`

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
**Description:** Verify constraints are rendered in task.md TOC
**Command:** `grep -q 'constraint.*toc\|Constraint' task.md && echo '✓ Constraints visible in markdown' || echo '✗ Not visible'`

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
**Command:** `python3 constraints_scripts/validate_toc_links.py task.md`

#### constraint_toc_has_entries
**Description:** Verify TOC contains markdown list entries (lines starting with -)
**Command:** `grep -A 20 '## Table of Contents' task.md | grep -q '^-' && echo '✓ TOC entries found' || echo '✗ No entries'`

#### constraint_toc_implementation_review
**Description:** Code review of Task TOC generation logic
**Prompt:** Review the Task TOC rendering implementation in task_model.py. Verify: 1) _generate_toc() generates valid markdown links with proper anchors, 2) Anchors match heading formats (lowercase, spaces→hyphens), 3) Special characters are handled correctly, 4) Nested items are properly indented with spaces, 5) Links use consistent anchor generation, 6) TOC includes all sections (Specification, Features, Iterations, Constraints)
**Expected Verdict:** `PASS`

#### constraint_toc_indentation
**Description:** Verify TOC has proper indentation for nested items
**Command:** `grep '## Table of Contents' -A 50 task.md | grep -E '^  -|^    -' | wc -l | grep -qE '[1-9]' && echo '✓ Proper nesting found' || echo '✗ Missing'`

#### constraint_toc_links_format
**Description:** Verify TOC links follow markdown format [text](#anchor)
**Command:** `grep '## Table of Contents' -A 20 task.md | grep -q '\[.*\](#' && echo '✓ Links formatted correctly' || echo '✗ Bad format'`

#### constraint_toc_section_exists
**Description:** Verify 'Table of Contents' section header exists in task.md
**Command:** `grep -q '## Table of Contents' task.md && echo '✓ TOC section found' || echo '✗ Missing'`

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
**Command:** `grep -q 'iteration_1' task.json && jq '.iterations.iteration_1.features_stats' task.json | grep -q 'features_checks' && echo 'Stats in iteration' || echo 'Not in iteration'`

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
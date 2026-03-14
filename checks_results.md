## Table of Contents

- [Constraint Results](#constraint-results)
  - [Feature: add_constraint_validation_requirement_skill](#add-constraint-validation-requirement-skill)
    - [constraint_requirement_section_exists](#add-constraint-validation-requirement-skill-constraint-requirement-section-exists)
    - [constraint_results_interpretation_guide](#add-constraint-validation-requirement-skill-constraint-results-interpretation-guide)
    - [constraint_when_to_run_documented](#add-constraint-validation-requirement-skill-constraint-when-to-run-documented)
  - [Feature: constraint_checker_exit_code_hook](#constraint-checker-exit-code-hook)
    - [constraint_handler_stop_calls_checker](#constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker)
    - [constraint_handler_stop_checks_exit_code](#constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code)
    - [constraint_handler_stop_prints_decision_block](#constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block)
    - [constraint_task_checker_exits_2_on_failure](#constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure)
  - [Feature: constraint_rendering_capability](#constraint-rendering-capability)
    - [constraint_bash_render_method](#constraint-rendering-capability-constraint-bash-render-method)
    - [constraint_bash_render_toc_method](#constraint-rendering-capability-constraint-bash-render-toc-method)
    - [constraint_feature_uses_render_toc](#constraint-rendering-capability-constraint-feature-uses-render-toc)
    - [constraint_prompt_render_method](#constraint-rendering-capability-constraint-prompt-render-method)
    - [constraint_prompt_render_toc_method](#constraint-rendering-capability-constraint-prompt-render-toc-method)
    - [constraint_rendering_displays_type](#constraint-rendering-capability-constraint-rendering-displays-type)
  - [Feature: constraint_scripts_directory](#constraint-scripts-directory)
    - [constraint_scripts_directory_exists](#constraint-scripts-directory-constraint-scripts-directory-exists)
    - [constraint_scripts_documented](#constraint-scripts-directory-constraint-scripts-documented)
    - [constraint_scripts_readme_exists](#constraint-scripts-directory-constraint-scripts-readme-exists)
  - [Feature: enhance_constraint_bash_result_output](#enhance-constraint-bash-result-output)
    - [constraint_output_populated_on_failure](#enhance-constraint-bash-result-output-constraint-output-populated-on-failure)
    - [constraint_output_rendered_in_markdown](#enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown)
    - [constraint_shrunken_output_field_exists](#enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists)
  - [Feature: feature_goals_field](#feature-goals-field)
    - [constraint_goals_field_exists](#feature-goals-field-constraint-goals-field-exists)
    - [constraint_goals_field_in_task](#feature-goals-field-constraint-goals-field-in-task)
    - [constraint_goals_in_toc](#feature-goals-field-constraint-goals-in-toc)
    - [constraint_goals_rendered_in_markdown](#feature-goals-field-constraint-goals-rendered-in-markdown)
  - [Feature: features_stats_diff_tracking](#features-stats-diff-tracking)
    - [constraint_diff_rendered_in_iteration](#features-stats-diff-tracking-constraint-diff-rendered-in-iteration)
    - [constraint_features_stats_diff_model_exists](#features-stats-diff-tracking-constraint-features-stats-diff-model-exists)
    - [constraint_features_stats_has_diff_method](#features-stats-diff-tracking-constraint-features-stats-has-diff-method)
    - [constraint_iteration_has_diff_field](#features-stats-diff-tracking-constraint-iteration-has-diff-field)
  - [Feature: forbid_task_status_downgrade](#forbid-task-status-downgrade)
    - [constraint_status_locked_in_executing](#forbid-task-status-downgrade-constraint-status-locked-in-executing)
    - [constraint_status_validation_exists](#forbid-task-status-downgrade-constraint-status-validation-exists)
  - [Feature: render_spec_features_in_task](#render-spec-features-in-task)
    - [constraint_constraint_details_in_markdown](#render-spec-features-in-task-constraint-constraint-details-in-markdown)
    - [constraint_feature_section_in_markdown](#render-spec-features-in-task-constraint-feature-section-in-markdown)
    - [constraint_rendering_implementation_review](#render-spec-features-in-task-constraint-rendering-implementation-review)
  - [Feature: task_add_iteration_script](#task-add-iteration-script)
    - [constraint_script_exists](#task-add-iteration-script-constraint-script-exists)
    - [constraint_script_populates_features_stats](#task-add-iteration-script-constraint-script-populates-features-stats)
    - [constraint_script_runs_checker](#task-add-iteration-script-constraint-script-runs-checker)
    - [constraint_script_uses_knowledge_tool](#task-add-iteration-script-constraint-script-uses-knowledge-tool)
    - [constraint_skill_documentation_updated](#task-add-iteration-script-constraint-skill-documentation-updated)
  - [Feature: task_default_render_toc](#task-default-render-toc)
    - [constraint_default_toc_when_opts_missing](#task-default-render-toc-constraint-default-toc-when-opts-missing)
    - [constraint_explicit_false_respected](#task-default-render-toc-constraint-explicit-false-respected)
    - [constraint_render_toc_default_true](#task-default-render-toc-constraint-render-toc-default-true)
    - [constraint_toc_rendered_by_default](#task-default-render-toc-constraint-toc-rendered-by-default)
  - [Feature: task_features_checker_tool](#task-features-checker-tool)
    - [constraint_project_root_substitution](#task-features-checker-tool-constraint-project-root-substitution)
    - [constraint_recursive_execution_prevention](#task-features-checker-tool-constraint-recursive-execution-prevention)
    - [constraint_tool_accepts_features_arg](#task-features-checker-tool-constraint-tool-accepts-features-arg)
    - [constraint_tool_accepts_output_checks_path_arg](#task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg)
    - [constraint_tool_accepts_task_path](#task-features-checker-tool-constraint-tool-accepts-task-path)
    - [constraint_tool_exists](#task-features-checker-tool-constraint-tool-exists)
    - [constraint_tool_implementation_review](#task-features-checker-tool-constraint-tool-implementation-review)
    - [constraint_tool_output_checks_path_writable](#task-features-checker-tool-constraint-tool-output-checks-path-writable)
    - [constraint_tool_returns_checks_results](#task-features-checker-tool-constraint-tool-returns-checks-results)
    - [constraint_tool_saves_results_to_file](#task-features-checker-tool-constraint-tool-saves-results-to-file)
  - [Feature: task_toc_includes_constraints](#task-toc-includes-constraints)
    - [constraint_constraints_nested_in_toc](#task-toc-includes-constraints-constraint-constraints-nested-in-toc)
    - [constraint_constraints_visible_in_markdown](#task-toc-includes-constraints-constraint-constraints-visible-in-markdown)
    - [constraint_toc_includes_constraints](#task-toc-includes-constraints-constraint-toc-includes-constraints)
  - [Feature: task_toc_rendering_and_links](#task-toc-rendering-and-links)
    - [constraint_anchor_sections_exist](#task-toc-rendering-and-links-constraint-anchor-sections-exist)
    - [constraint_toc_has_entries](#task-toc-rendering-and-links-constraint-toc-has-entries)
    - [constraint_toc_implementation_review](#task-toc-rendering-and-links-constraint-toc-implementation-review)
    - [constraint_toc_indentation](#task-toc-rendering-and-links-constraint-toc-indentation)
    - [constraint_toc_links_format](#task-toc-rendering-and-links-constraint-toc-links-format)
    - [constraint_toc_section_exists](#task-toc-rendering-and-links-constraint-toc-section-exists)
  - [Feature: update_iteration_with_features_stats](#update-iteration-with-features-stats)
    - [constraint_feature_result_constraints_required](#update-iteration-with-features-stats-constraint-feature-result-constraints-required)
    - [constraint_features_stats_generated](#update-iteration-with-features-stats-constraint-features-stats-generated)
    - [constraint_features_stats_in_iteration](#update-iteration-with-features-stats-constraint-features-stats-in-iteration)
    - [constraint_features_stats_model_exists](#update-iteration-with-features-stats-constraint-features-stats-model-exists)
    - [constraint_features_stats_rendered](#update-iteration-with-features-stats-constraint-features-stats-rendered)
    - [constraint_skill_documentation_updated](#update-iteration-with-features-stats-constraint-skill-documentation-updated)
    - [constraint_stats_displayed_on_iteration](#update-iteration-with-features-stats-constraint-stats-displayed-on-iteration)

## Constraint Results

<a id="add-constraint-validation-requirement-skill"></a>
### Feature: add_constraint_validation_requirement_skill

**Bash Constraints:**

<a id="add-constraint-validation-requirement-skill-constraint-requirement-section-exists"></a>
#### add_constraint_validation_requirement_skill.constraint_requirement_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.138111
**Output:** `Requirement section found
`

<a id="add-constraint-validation-requirement-skill-constraint-results-interpretation-guide"></a>
#### add_constraint_validation_requirement_skill.constraint_results_interpretation_guide
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.140564
**Output:** `Interpretation guide exists
`

<a id="add-constraint-validation-requirement-skill-constraint-when-to-run-documented"></a>
#### add_constraint_validation_requirement_skill.constraint_when_to_run_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.139316
**Output:** `When section documented
`


<a id="constraint-checker-exit-code-hook"></a>
### Feature: constraint_checker_exit_code_hook

**Bash Constraints:**

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_calls_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.180654
**Output:** `Calls checker
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_checks_exit_code
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.181970
**Output:** `Checks exit code
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_prints_decision_block
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.183478
**Output:** `Prints decision block
`

<a id="constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure"></a>
#### constraint_checker_exit_code_hook.constraint_task_checker_exits_2_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.179359
**Output:** `Exit code 2 implemented
`


<a id="constraint-rendering-capability"></a>
### Feature: constraint_rendering_capability

**Bash Constraints:**

<a id="constraint-rendering-capability-constraint-bash-render-method"></a>
#### constraint_rendering_capability.constraint_bash_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.951086
**Output:** `✓ ConstraintBash.render() exists
`

<a id="constraint-rendering-capability-constraint-bash-render-toc-method"></a>
#### constraint_rendering_capability.constraint_bash_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.953835
**Output:** `✓ ConstraintBash.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-feature-uses-render-toc"></a>
#### constraint_rendering_capability.constraint_feature_uses_render_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.956534
**Output:** `✓ Feature uses constraint.render_toc()
`

<a id="constraint-rendering-capability-constraint-prompt-render-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.952489
**Output:** `✓ ConstraintPrompt.render() exists
`

<a id="constraint-rendering-capability-constraint-prompt-render-toc-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.955185
**Output:** `✓ ConstraintPrompt.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-rendering-displays-type"></a>
#### constraint_rendering_capability.constraint_rendering_displays_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.132366
**Output:** `✓ Constraint type displayed
`


<a id="constraint-scripts-directory"></a>
### Feature: constraint_scripts_directory

**Bash Constraints:**

<a id="constraint-scripts-directory-constraint-scripts-directory-exists"></a>
#### constraint_scripts_directory.constraint_scripts_directory_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.947441
**Output:** `✓ constraints_scripts/ directory exists
`

<a id="constraint-scripts-directory-constraint-scripts-documented"></a>
#### constraint_scripts_directory.constraint_scripts_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.949272
**Output:** `✓ Documentation found
`

<a id="constraint-scripts-directory-constraint-scripts-readme-exists"></a>
#### constraint_scripts_directory.constraint_scripts_readme_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.948040
**Output:** `✓ README.md exists
`


<a id="enhance-constraint-bash-result-output"></a>
### Feature: enhance_constraint_bash_result_output

**Bash Constraints:**

<a id="enhance-constraint-bash-result-output-constraint-output-populated-on-failure"></a>
#### enhance_constraint_bash_result_output.constraint_output_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.135394
**Output:** `Not captured
`

<a id="enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown"></a>
#### enhance_constraint_bash_result_output.constraint_output_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.136706
**Output:** `Output rendered
`

<a id="enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists"></a>
#### enhance_constraint_bash_result_output.constraint_shrunken_output_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.134042
**Output:** `Field missing or optional
`


<a id="feature-goals-field"></a>
### Feature: feature_goals_field

**Bash Constraints:**

<a id="feature-goals-field-constraint-goals-field-exists"></a>
#### feature_goals_field.constraint_goals_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.550037
**Output:** `✓ Goals field exists
`

<a id="feature-goals-field-constraint-goals-field-in-task"></a>
#### feature_goals_field.constraint_goals_field_in_task
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.554044
**Output:** `✓ Goals in task.json
`

<a id="feature-goals-field-constraint-goals-in-toc"></a>
#### feature_goals_field.constraint_goals_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.552748
**Output:** `✓ Goals in TOC found
`

<a id="feature-goals-field-constraint-goals-rendered-in-markdown"></a>
#### feature_goals_field.constraint_goals_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.551345
**Output:** `✓ Goals rendering found
`


<a id="features-stats-diff-tracking"></a>
### Feature: features_stats_diff_tracking

**Bash Constraints:**

<a id="features-stats-diff-tracking-constraint-diff-rendered-in-iteration"></a>
#### features_stats_diff_tracking.constraint_diff_rendered_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.188892
**Output:** `Not implemented
`

<a id="features-stats-diff-tracking-constraint-features-stats-diff-model-exists"></a>
#### features_stats_diff_tracking.constraint_features_stats_diff_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.184788
**Output:** `Model exists
`

<a id="features-stats-diff-tracking-constraint-features-stats-has-diff-method"></a>
#### features_stats_diff_tracking.constraint_features_stats_has_diff_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.186170
**Output:** `diff() method exists
`

<a id="features-stats-diff-tracking-constraint-iteration-has-diff-field"></a>
#### features_stats_diff_tracking.constraint_iteration_has_diff_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.187485
**Output:** `Field exists
`


<a id="forbid-task-status-downgrade"></a>
### Feature: forbid_task_status_downgrade

**Bash Constraints:**

<a id="forbid-task-status-downgrade-constraint-status-locked-in-executing"></a>
#### forbid_task_status_downgrade.constraint_status_locked_in_executing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.532285
**Output:** `✓ Status locked
`

<a id="forbid-task-status-downgrade-constraint-status-validation-exists"></a>
#### forbid_task_status_downgrade.constraint_status_validation_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.327593
**Output:** `/project/hooks/__init__.py:    Prevents status downgrades: executing/failed/succeed cannot go back to planning.
Hook validation found
grep: /project/hooks/__pycache__/__init__.cpython-313.pyc: binary file matches
grep: /project/hooks/__pycache__/__init__.cpython-311.pyc: binary file matches
`


<a id="render-spec-features-in-task"></a>
### Feature: render_spec_features_in_task

**Bash Constraints:**

<a id="render-spec-features-in-task-constraint-constraint-details-in-markdown"></a>
#### render_spec_features_in_task.constraint_constraint_details_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.535698
**Output:** `✓ Constraint details found
`

<a id="render-spec-features-in-task-constraint-feature-section-in-markdown"></a>
#### render_spec_features_in_task.constraint_feature_section_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.534251
**Output:** `✓ Features section found in markdown
`

**Prompt Constraints:**

<a id="render-spec-features-in-task-constraint-rendering-implementation-review"></a>
#### render_spec_features_in_task.constraint_rendering_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-14T12:30:31.535715


<a id="task-add-iteration-script"></a>
### Feature: task_add_iteration_script

**Bash Constraints:**

<a id="task-add-iteration-script-constraint-script-exists"></a>
#### task_add_iteration_script.constraint_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.189545
**Output:** `Script exists
`

<a id="task-add-iteration-script-constraint-script-populates-features-stats"></a>
#### task_add_iteration_script.constraint_script_populates_features_stats
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.193184
**Output:** `Populates stats
`

<a id="task-add-iteration-script-constraint-script-runs-checker"></a>
#### task_add_iteration_script.constraint_script_runs_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.191998
**Output:** `Runs checker
`

<a id="task-add-iteration-script-constraint-script-uses-knowledge-tool"></a>
#### task_add_iteration_script.constraint_script_uses_knowledge_tool
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.190756
**Output:** `Uses knowledge tool
`

<a id="task-add-iteration-script-constraint-skill-documentation-updated"></a>
#### task_add_iteration_script.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.194468
**Output:** `Documented
`


<a id="task-default-render-toc"></a>
### Feature: task_default_render_toc

**Bash Constraints:**

<a id="task-default-render-toc-constraint-default-toc-when-opts-missing"></a>
#### task_default_render_toc.constraint_default_toc_when_opts_missing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.555354
**Output:** `✓ Default opts handling found
`

<a id="task-default-render-toc-constraint-explicit-false-respected"></a>
#### task_default_render_toc.constraint_explicit_false_respected
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.558106
**Output:** `✓ Explicit False handling found
`

<a id="task-default-render-toc-constraint-render-toc-default-true"></a>
#### task_default_render_toc.constraint_render_toc_default_true
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.556684
**Output:** `✓ Default render_toc=True found
`

<a id="task-default-render-toc-constraint-toc-rendered-by-default"></a>
#### task_default_render_toc.constraint_toc_rendered_by_default
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.740200
**Output:** `✓ TOC rendered
`


<a id="task-features-checker-tool"></a>
### Feature: task_features_checker_tool

**Bash Constraints:**

<a id="task-features-checker-tool-constraint-project-root-substitution"></a>
#### task_features_checker_tool.constraint_project_root_substitution
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.546967
**Output:** `✓ PROJECT_ROOT substitution found
`

<a id="task-features-checker-tool-constraint-recursive-execution-prevention"></a>
#### task_features_checker_tool.constraint_recursive_execution_prevention
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.545633
**Output:** `✓ Recursive execution prevention found
`

<a id="task-features-checker-tool-constraint-tool-accepts-features-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_features_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.539259
**Output:** `--features arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_output_checks_path_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.540646
**Output:** `--output-checks-path arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-task-path"></a>
#### task_features_checker_tool.constraint_tool_accepts_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.537924
**Output:** `Task path argument missing
`

<a id="task-features-checker-tool-constraint-tool-exists"></a>
#### task_features_checker_tool.constraint_tool_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.536461
**Output:** `✓ tool exists
`

<a id="task-features-checker-tool-constraint-tool-output-checks-path-writable"></a>
#### task_features_checker_tool.constraint_tool_output_checks_path_writable
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.548389
**Output:** `Output path handling implemented
`

<a id="task-features-checker-tool-constraint-tool-returns-checks-results"></a>
#### task_features_checker_tool.constraint_tool_returns_checks_results
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.542079
**Output:** `ChecksResults usage found
`

<a id="task-features-checker-tool-constraint-tool-saves-results-to-file"></a>
#### task_features_checker_tool.constraint_tool_saves_results_to_file
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.544257
**Output:** `File save logic implemented
`

**Prompt Constraints:**

<a id="task-features-checker-tool-constraint-tool-implementation-review"></a>
#### task_features_checker_tool.constraint_tool_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-14T12:30:31.544274


<a id="task-toc-includes-constraints"></a>
### Feature: task_toc_includes_constraints

**Bash Constraints:**

<a id="task-toc-includes-constraints-constraint-constraints-nested-in-toc"></a>
#### task_toc_includes_constraints.constraint_constraints_nested_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.915921
**Output:** `✗ No constraints in TOC
`

<a id="task-toc-includes-constraints-constraint-constraints-visible-in-markdown"></a>
#### task_toc_includes_constraints.constraint_constraints_visible_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.917526
**Output:** `✓ Constraints visible in markdown
`

<a id="task-toc-includes-constraints-constraint-toc-includes-constraints"></a>
#### task_toc_includes_constraints.constraint_toc_includes_constraints
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.742090
**Output:** `✗ Missing
`


<a id="task-toc-rendering-and-links"></a>
### Feature: task_toc_rendering_and_links

**Bash Constraints:**

<a id="task-toc-rendering-and-links-constraint-anchor-sections-exist"></a>
#### task_toc_rendering_and_links.constraint_anchor_sections_exist
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.945119
**Output:** `✓ All 88 TOC links have matching anchors
`

<a id="task-toc-rendering-and-links-constraint-toc-has-entries"></a>
#### task_toc_rendering_and_links.constraint_toc_has_entries
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.920208
**Output:** `✓ TOC entries found
`

<a id="task-toc-rendering-and-links-constraint-toc-indentation"></a>
#### task_toc_rendering_and_links.constraint_toc_indentation
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.946782
**Output:** `✓ Proper nesting found
`

<a id="task-toc-rendering-and-links-constraint-toc-links-format"></a>
#### task_toc_rendering_and_links.constraint_toc_links_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.921640
**Output:** `✓ Links formatted correctly
`

<a id="task-toc-rendering-and-links-constraint-toc-section-exists"></a>
#### task_toc_rendering_and_links.constraint_toc_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:31.918831
**Output:** `✓ TOC section found
`

**Prompt Constraints:**

<a id="task-toc-rendering-and-links-constraint-toc-implementation-review"></a>
#### task_toc_rendering_and_links.constraint_toc_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-14T12:30:31.946799


<a id="update-iteration-with-features-stats"></a>
### Feature: update_iteration_with_features_stats

**Bash Constraints:**

<a id="update-iteration-with-features-stats-constraint-feature-result-constraints-required"></a>
#### update_iteration_with_features_stats.constraint_feature_result_constraints_required
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.178064
**Output:** `Still optional
`

<a id="update-iteration-with-features-stats-constraint-features-stats-generated"></a>
#### update_iteration_with_features_stats.constraint_features_stats_generated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.144973
**Output:** `Generation implemented
`

<a id="update-iteration-with-features-stats-constraint-features-stats-in-iteration"></a>
#### update_iteration_with_features_stats.constraint_features_stats_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.143730
**Output:** `Field in Iteration
`

<a id="update-iteration-with-features-stats-constraint-features-stats-model-exists"></a>
#### update_iteration_with_features_stats.constraint_features_stats_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.142467
**Output:** `FeaturesStats with proper fields
`

<a id="update-iteration-with-features-stats-constraint-features-stats-rendered"></a>
#### update_iteration_with_features_stats.constraint_features_stats_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.146233
**Output:** `Rendering implemented
`

<a id="update-iteration-with-features-stats-constraint-skill-documentation-updated"></a>
#### update_iteration_with_features_stats.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.147616
**Output:** `Skill docs updated
`

<a id="update-iteration-with-features-stats-constraint-stats-displayed-on-iteration"></a>
#### update_iteration_with_features_stats.constraint_stats_displayed_on_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-14T12:30:32.176518
**Output:** `Stats in iteration
`
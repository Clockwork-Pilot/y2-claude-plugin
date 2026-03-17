## Table of Contents

- [Constraint Results](#constraint-results)
  - [Feature: add_constraint_validation_requirement_skill](#add-constraint-validation-requirement-skill)
    - [constraint_requirement_section_exists](#add-constraint-validation-requirement-skill-constraint-requirement-section-exists)
    - [constraint_results_interpretation_guide](#add-constraint-validation-requirement-skill-constraint-results-interpretation-guide)
    - [constraint_when_to_run_documented](#add-constraint-validation-requirement-skill-constraint-when-to-run-documented)
  - [Feature: constraint_bash_fails_count_cmd_protection](#constraint-bash-fails-count-cmd-protection)
    - [constraint_no_default_fails_count_in_json](#constraint-bash-fails-count-cmd-protection-constraint-no-default-fails-count-in-json)
    - [constraint_proven_constraint_removal_blocked](#constraint-bash-fails-count-cmd-protection-constraint-proven-constraint-removal-blocked)
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
  - [Feature: migrate_metadata_to_model](#migrate-metadata-to-model)
    - [constraint_constraint_model_uses_metadata](#migrate-metadata-to-model-constraint-constraint-model-uses-metadata)
    - [constraint_doc_model_uses_metadata](#migrate-metadata-to-model-constraint-doc-model-uses-metadata)
    - [constraint_feature_model_uses_metadata](#migrate-metadata-to-model-constraint-feature-model-uses-metadata)
    - [constraint_metadata_import](#migrate-metadata-to-model-constraint-metadata-import)
    - [constraint_no_dict_metadata_references](#migrate-metadata-to-model-constraint-no-dict-metadata-references)
    - [constraint_spec_model_uses_metadata](#migrate-metadata-to-model-constraint-spec-model-uses-metadata)
    - [constraint_task_model_uses_metadata](#migrate-metadata-to-model-constraint-task-model-uses-metadata)
  - [Feature: project_spec_lifecycle](#project-spec-lifecycle)
    - [constraint_check_project_constraints_exists](#project-spec-lifecycle-constraint-check-project-constraints-exists)
    - [constraint_complete_task_runs_project_checker](#project-spec-lifecycle-constraint-complete-task-runs-project-checker)
    - [constraint_complete_task_runs_task_checker](#project-spec-lifecycle-constraint-complete-task-runs-task-checker)
    - [constraint_complete_task_script_exists](#project-spec-lifecycle-constraint-complete-task-script-exists)
    - [constraint_project_spec_dir_created](#project-spec-lifecycle-constraint-project-spec-dir-created)
    - [constraint_raw_tasks_directory_created](#project-spec-lifecycle-constraint-raw-tasks-directory-created)
    - [constraint_spec_snapshot_format](#project-spec-lifecycle-constraint-spec-snapshot-format)
    - [constraint_task_json_preserved](#project-spec-lifecycle-constraint-task-json-preserved)
  - [Feature: remove_scope_from_constraint_bash](#remove-scope-from-constraint-bash)
    - [constraint_all_model_tests_pass](#remove-scope-from-constraint-bash-constraint-all-model-tests-pass)
    - [constraint_no_scope_field_usage](#remove-scope-from-constraint-bash-constraint-no-scope-field-usage)
    - [constraint_no_scope_in_constraint_bash](#remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash)
    - [constraint_scope_field_removed_from_definition](#remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition)
  - [Feature: render_spec_features_in_task](#render-spec-features-in-task)
    - [constraint_constraint_details_in_markdown](#render-spec-features-in-task-constraint-constraint-details-in-markdown)
    - [constraint_feature_section_in_markdown](#render-spec-features-in-task-constraint-feature-section-in-markdown)
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
  - [Feature: task_features_checker_selective_patch](#task-features-checker-selective-patch)
    - [constraint_feature_results_filtering](#task-features-checker-selective-patch-constraint-feature-results-filtering)
    - [constraint_patch_uses_add_op](#task-features-checker-selective-patch-constraint-patch-uses-add-op)
    - [constraint_preserves_other_features](#task-features-checker-selective-patch-constraint-preserves-other-features)
    - [constraint_selective_patch_logic](#task-features-checker-selective-patch-constraint-selective-patch-logic)
  - [Feature: task_features_checker_tool](#task-features-checker-tool)
    - [constraint_project_root_substitution](#task-features-checker-tool-constraint-project-root-substitution)
    - [constraint_recursive_execution_prevention](#task-features-checker-tool-constraint-recursive-execution-prevention)
    - [constraint_tool_accepts_features_arg](#task-features-checker-tool-constraint-tool-accepts-features-arg)
    - [constraint_tool_accepts_output_checks_path_arg](#task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg)
    - [constraint_tool_accepts_task_path](#task-features-checker-tool-constraint-tool-accepts-task-path)
    - [constraint_tool_exists](#task-features-checker-tool-constraint-tool-exists)
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
    - [constraint_toc_indentation](#task-toc-rendering-and-links-constraint-toc-indentation)
    - [constraint_toc_links_format](#task-toc-rendering-and-links-constraint-toc-links-format)
    - [constraint_toc_section_exists](#task-toc-rendering-and-links-constraint-toc-section-exists)
  - [Feature: two_phase_constraint_validation](#two-phase-constraint-validation)
    - [constraint_cmd_protection_verified](#two-phase-constraint-validation-constraint-cmd-protection-verified)
    - [constraint_cmd_protection_when_proven](#two-phase-constraint-validation-constraint-cmd-protection-when-proven)
    - [constraint_cmd_update_warning](#two-phase-constraint-validation-constraint-cmd-update-warning)
    - [constraint_external_proven_red_blocked](#two-phase-constraint-validation-constraint-external-proven-red-blocked)
    - [constraint_only_proven_affects_result](#two-phase-constraint-validation-constraint-only-proven-affects-result)
    - [constraint_patch_protects_proven_red](#two-phase-constraint-validation-constraint-patch-protects-proven-red)
    - [constraint_print_proven_summary](#two-phase-constraint-validation-constraint-print-proven-summary)
    - [constraint_proven_red_default_none](#two-phase-constraint-validation-constraint-proven-red-default-none)
    - [constraint_proven_red_excluded](#two-phase-constraint-validation-constraint-proven-red-excluded)
    - [constraint_proven_red_field_exists](#two-phase-constraint-validation-constraint-proven-red-field-exists)
    - [constraint_proven_red_in_task_json](#two-phase-constraint-validation-constraint-proven-red-in-task-json)
    - [constraint_set_proven_red_on_failure](#two-phase-constraint-validation-constraint-set-proven-red-on-failure)
    - [constraint_unprovided_constraints_logged_not_failed](#two-phase-constraint-validation-constraint-unprovided-constraints-logged-not-failed)
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

<a id="add-constraint-validation-requirement-skill-constraint-requirement-section-exists"></a>
#### add_constraint_validation_requirement_skill.constraint_requirement_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.387290
**Output:** `Requirement section found
`

<a id="add-constraint-validation-requirement-skill-constraint-results-interpretation-guide"></a>
#### add_constraint_validation_requirement_skill.constraint_results_interpretation_guide
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.389835
**Output:** `Interpretation guide exists
`

<a id="add-constraint-validation-requirement-skill-constraint-when-to-run-documented"></a>
#### add_constraint_validation_requirement_skill.constraint_when_to_run_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.388543
**Output:** `When section documented
`


<a id="constraint-bash-fails-count-cmd-protection"></a>
### Feature: constraint_bash_fails_count_cmd_protection

<a id="constraint-bash-fails-count-cmd-protection-constraint-no-default-fails-count-in-json"></a>
#### constraint_bash_fails_count_cmd_protection.constraint_no_default_fails_count_in_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.482964
**Output:** `OK: no default fails_count in spec.features constraints
`

<a id="constraint-bash-fails-count-cmd-protection-constraint-proven-constraint-removal-blocked"></a>
#### constraint_bash_fails_count_cmd_protection.constraint_proven_constraint_removal_blocked
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:26.041322


<a id="constraint-checker-exit-code-hook"></a>
### Feature: constraint_checker_exit_code_hook

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_calls_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.430586
**Output:** `Calls checker
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_checks_exit_code
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.431876
**Output:** `Checks exit code
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_prints_decision_block
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.433168
**Output:** `Prints decision block
`

<a id="constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure"></a>
#### constraint_checker_exit_code_hook.constraint_task_checker_exits_2_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.429268
**Output:** `Exit code 2 implemented
`


<a id="constraint-rendering-capability"></a>
### Feature: constraint_rendering_capability

<a id="constraint-rendering-capability-constraint-bash-render-method"></a>
#### constraint_rendering_capability.constraint_bash_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.375060
**Output:** `✓ ConstraintBash.render() exists
`

<a id="constraint-rendering-capability-constraint-bash-render-toc-method"></a>
#### constraint_rendering_capability.constraint_bash_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.377893
**Output:** `✓ ConstraintBash.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-feature-uses-render-toc"></a>
#### constraint_rendering_capability.constraint_feature_uses_render_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.380487
**Output:** `✓ Feature uses constraint.render_toc()
`

<a id="constraint-rendering-capability-constraint-prompt-render-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.376448
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-prompt-render-toc-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.379230
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-rendering-displays-type"></a>
#### constraint_rendering_capability.constraint_rendering_displays_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.381781


<a id="constraint-scripts-directory"></a>
### Feature: constraint_scripts_directory

<a id="constraint-scripts-directory-constraint-scripts-directory-exists"></a>
#### constraint_scripts_directory.constraint_scripts_directory_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.370792
**Output:** `✓ constraints_scripts/ directory exists
`

<a id="constraint-scripts-directory-constraint-scripts-documented"></a>
#### constraint_scripts_directory.constraint_scripts_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.372878
**Output:** `✓ Documentation found
`

<a id="constraint-scripts-directory-constraint-scripts-readme-exists"></a>
#### constraint_scripts_directory.constraint_scripts_readme_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.371429
**Output:** `✓ README.md exists
`


<a id="enhance-constraint-bash-result-output"></a>
### Feature: enhance_constraint_bash_result_output

<a id="enhance-constraint-bash-result-output-constraint-output-populated-on-failure"></a>
#### enhance_constraint_bash_result_output.constraint_output_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.384558
**Output:** `Not captured
`

<a id="enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown"></a>
#### enhance_constraint_bash_result_output.constraint_output_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.385877
**Output:** `Output rendered
`

<a id="enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists"></a>
#### enhance_constraint_bash_result_output.constraint_shrunken_output_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.383224
**Output:** `Field missing or optional
`


<a id="feature-goals-field"></a>
### Feature: feature_goals_field

<a id="feature-goals-field-constraint-goals-field-exists"></a>
#### feature_goals_field.constraint_goals_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.979044
**Output:** `✓ Goals field exists
`

<a id="feature-goals-field-constraint-goals-field-in-task"></a>
#### feature_goals_field.constraint_goals_field_in_task
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.983207
**Output:** `✓ Goals in task.k.json
`

<a id="feature-goals-field-constraint-goals-in-toc"></a>
#### feature_goals_field.constraint_goals_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.981725
**Output:** `✓ Goals in TOC found
`

<a id="feature-goals-field-constraint-goals-rendered-in-markdown"></a>
#### feature_goals_field.constraint_goals_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.980382
**Output:** `✓ Goals rendering found
`


<a id="features-stats-diff-tracking"></a>
### Feature: features_stats_diff_tracking

<a id="features-stats-diff-tracking-constraint-diff-rendered-in-iteration"></a>
#### features_stats_diff_tracking.constraint_diff_rendered_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.438583
**Output:** `Not implemented
`

<a id="features-stats-diff-tracking-constraint-features-stats-diff-model-exists"></a>
#### features_stats_diff_tracking.constraint_features_stats_diff_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.434454
**Output:** `Model exists
`

<a id="features-stats-diff-tracking-constraint-features-stats-has-diff-method"></a>
#### features_stats_diff_tracking.constraint_features_stats_has_diff_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.435792
**Output:** `diff() method exists
`

<a id="features-stats-diff-tracking-constraint-iteration-has-diff-field"></a>
#### features_stats_diff_tracking.constraint_iteration_has_diff_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.437113
**Output:** `Field exists
`


<a id="forbid-task-status-downgrade"></a>
### Feature: forbid_task_status_downgrade

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


<a id="migrate-metadata-to-model"></a>
### Feature: migrate_metadata_to_model

<a id="migrate-metadata-to-model-constraint-constraint-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_constraint_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.444951

<a id="migrate-metadata-to-model-constraint-doc-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_doc_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.447444

<a id="migrate-metadata-to-model-constraint-feature-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_feature_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.446856

<a id="migrate-metadata-to-model-constraint-metadata-import"></a>
#### migrate_metadata_to_model.constraint_metadata_import
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.448076

<a id="migrate-metadata-to-model-constraint-no-dict-metadata-references"></a>
#### migrate_metadata_to_model.constraint_no_dict_metadata_references
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.449614

<a id="migrate-metadata-to-model-constraint-spec-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_spec_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.446205

<a id="migrate-metadata-to-model-constraint-task-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_task_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.445587


<a id="project-spec-lifecycle"></a>
### Feature: project_spec_lifecycle

<a id="project-spec-lifecycle-constraint-check-project-constraints-exists"></a>
#### project_spec_lifecycle.constraint_check_project_constraints_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.458207
**Output:** `✓ check_project_constraints.py exists
`

<a id="project-spec-lifecycle-constraint-complete-task-runs-project-checker"></a>
#### project_spec_lifecycle.constraint_complete_task_runs_project_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.461303
**Output:** `✓ calls check_project_constraints
`

<a id="project-spec-lifecycle-constraint-complete-task-runs-task-checker"></a>
#### project_spec_lifecycle.constraint_complete_task_runs_task_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.460050
**Output:** `✓ calls task_features_checker
`

<a id="project-spec-lifecycle-constraint-complete-task-script-exists"></a>
#### project_spec_lifecycle.constraint_complete_task_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.458834
**Output:** `✓ complete_task.py exists
`

<a id="project-spec-lifecycle-constraint-project-spec-dir-created"></a>
#### project_spec_lifecycle.constraint_project_spec_dir_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.457639
**Output:** `✓ project-spec directory exists
`

<a id="project-spec-lifecycle-constraint-raw-tasks-directory-created"></a>
#### project_spec_lifecycle.constraint_raw_tasks_directory_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.461933
**Output:** `✓ raw-tasks directory exists
`

<a id="project-spec-lifecycle-constraint-spec-snapshot-format"></a>
#### project_spec_lifecycle.constraint_spec_snapshot_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.463757
**Output:** `✓ timestamp handling present
`

<a id="project-spec-lifecycle-constraint-task-json-preserved"></a>
#### project_spec_lifecycle.constraint_task_json_preserved
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.462529
**Output:** `✓ task.k.json preserved
`


<a id="remove-scope-from-constraint-bash"></a>
### Feature: remove_scope_from_constraint_bash

<a id="remove-scope-from-constraint-bash-constraint-all-model-tests-pass"></a>
#### remove_scope_from_constraint_bash.constraint_all_model_tests_pass
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.457009
**Output:** `Tests exist
`

<a id="remove-scope-from-constraint-bash-constraint-no-scope-field-usage"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_field_usage
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.456368

<a id="remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_in_constraint_bash
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.454974

<a id="remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition"></a>
#### remove_scope_from_constraint_bash.constraint_scope_field_removed_from_definition
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.453541


<a id="render-spec-features-in-task"></a>
### Feature: render_spec_features_in_task

<a id="render-spec-features-in-task-constraint-constraint-details-in-markdown"></a>
#### render_spec_features_in_task.constraint_constraint_details_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.965321
**Output:** `✓ Constraint details found
`

<a id="render-spec-features-in-task-constraint-feature-section-in-markdown"></a>
#### render_spec_features_in_task.constraint_feature_section_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.963902
**Output:** `✓ Features section found in markdown
`


<a id="task-add-iteration-script"></a>
### Feature: task_add_iteration_script

<a id="task-add-iteration-script-constraint-script-exists"></a>
#### task_add_iteration_script.constraint_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.439228
**Output:** `Script exists
`

<a id="task-add-iteration-script-constraint-script-populates-features-stats"></a>
#### task_add_iteration_script.constraint_script_populates_features_stats
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.442992
**Output:** `Populates stats
`

<a id="task-add-iteration-script-constraint-script-runs-checker"></a>
#### task_add_iteration_script.constraint_script_runs_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.441775
**Output:** `Runs checker
`

<a id="task-add-iteration-script-constraint-script-uses-knowledge-tool"></a>
#### task_add_iteration_script.constraint_script_uses_knowledge_tool
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.440486
**Output:** `Uses knowledge tool
`

<a id="task-add-iteration-script-constraint-skill-documentation-updated"></a>
#### task_add_iteration_script.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.444304
**Output:** `Documented
`


<a id="task-default-render-toc"></a>
### Feature: task_default_render_toc

<a id="task-default-render-toc-constraint-default-toc-when-opts-missing"></a>
#### task_default_render_toc.constraint_default_toc_when_opts_missing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.984716
**Output:** `✓ Default opts handling found
`

<a id="task-default-render-toc-constraint-explicit-false-respected"></a>
#### task_default_render_toc.constraint_explicit_false_respected
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.987458
**Output:** `✓ Explicit False handling found
`

<a id="task-default-render-toc-constraint-render-toc-default-true"></a>
#### task_default_render_toc.constraint_render_toc_default_true
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.986045
**Output:** `✓ Default render_toc=True found
`

<a id="task-default-render-toc-constraint-toc-rendered-by-default"></a>
#### task_default_render_toc.constraint_toc_rendered_by_default
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.160717
**Output:** `✓ TOC rendered
`


<a id="task-features-checker-selective-patch"></a>
### Feature: task_features_checker_selective_patch

<a id="task-features-checker-selective-patch-constraint-feature-results-filtering"></a>
#### task_features_checker_selective_patch.constraint_feature_results_filtering
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.452149

<a id="task-features-checker-selective-patch-constraint-patch-uses-add-op"></a>
#### task_features_checker_selective_patch.constraint_patch_uses_add_op
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.451528

<a id="task-features-checker-selective-patch-constraint-preserves-other-features"></a>
#### task_features_checker_selective_patch.constraint_preserves_other_features
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.450903

<a id="task-features-checker-selective-patch-constraint-selective-patch-logic"></a>
#### task_features_checker_selective_patch.constraint_selective_patch_logic
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.450266


<a id="task-features-checker-tool"></a>
### Feature: task_features_checker_tool

<a id="task-features-checker-tool-constraint-project-root-substitution"></a>
#### task_features_checker_tool.constraint_project_root_substitution
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.976302
**Output:** `✓ PROJECT_ROOT substitution found
`

<a id="task-features-checker-tool-constraint-recursive-execution-prevention"></a>
#### task_features_checker_tool.constraint_recursive_execution_prevention
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.975070
**Output:** `✓ Recursive execution prevention found
`

<a id="task-features-checker-tool-constraint-tool-accepts-features-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_features_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.969052
**Output:** `--features arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_output_checks_path_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.970541
**Output:** `--output-checks-path arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-task-path"></a>
#### task_features_checker_tool.constraint_tool_accepts_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.967481
**Output:** `Task path argument missing
`

<a id="task-features-checker-tool-constraint-tool-exists"></a>
#### task_features_checker_tool.constraint_tool_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.966009
**Output:** `✓ tool exists
`

<a id="task-features-checker-tool-constraint-tool-output-checks-path-writable"></a>
#### task_features_checker_tool.constraint_tool_output_checks_path_writable
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.977639
**Output:** `Output path handling implemented
`

<a id="task-features-checker-tool-constraint-tool-returns-checks-results"></a>
#### task_features_checker_tool.constraint_tool_returns_checks_results
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.971907
**Output:** `ChecksResults usage found
`

<a id="task-features-checker-tool-constraint-tool-saves-results-to-file"></a>
#### task_features_checker_tool.constraint_tool_saves_results_to_file
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:24.973849
**Output:** `File save logic implemented
`


<a id="task-toc-includes-constraints"></a>
### Feature: task_toc_includes_constraints

<a id="task-toc-includes-constraints-constraint-constraints-nested-in-toc"></a>
#### task_toc_includes_constraints.constraint_constraints_nested_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.338752
**Output:** `✗ No constraints in TOC
`

<a id="task-toc-includes-constraints-constraint-constraints-visible-in-markdown"></a>
#### task_toc_includes_constraints.constraint_constraints_visible_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.340390
**Output:** `✓ Constraints visible in markdown
`

<a id="task-toc-includes-constraints-constraint-toc-includes-constraints"></a>
#### task_toc_includes_constraints.constraint_toc_includes_constraints
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.162393
**Output:** `✗ Missing
`


<a id="task-toc-rendering-and-links"></a>
### Feature: task_toc_rendering_and_links

<a id="task-toc-rendering-and-links-constraint-anchor-sections-exist"></a>
#### task_toc_rendering_and_links.constraint_anchor_sections_exist
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.368375
**Output:** `✓ All 119 TOC links have matching anchors
`

<a id="task-toc-rendering-and-links-constraint-toc-has-entries"></a>
#### task_toc_rendering_and_links.constraint_toc_has_entries
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.343232
**Output:** `✓ TOC entries found
`

<a id="task-toc-rendering-and-links-constraint-toc-indentation"></a>
#### task_toc_rendering_and_links.constraint_toc_indentation
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.370058
**Output:** `✓ Proper nesting found
`

<a id="task-toc-rendering-and-links-constraint-toc-links-format"></a>
#### task_toc_rendering_and_links.constraint_toc_links_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.344797
**Output:** `✓ Links formatted correctly
`

<a id="task-toc-rendering-and-links-constraint-toc-section-exists"></a>
#### task_toc_rendering_and_links.constraint_toc_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.341739
**Output:** `✓ TOC section found
`


<a id="two-phase-constraint-validation"></a>
### Feature: two_phase_constraint_validation

<a id="two-phase-constraint-validation-constraint-cmd-protection-verified"></a>
#### two_phase_constraint_validation.constraint_cmd_protection_verified
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.712327
**Output:** `Traceback (most recent call last):
  File "<string>", line 4, in <module>
ImportError: cannot import name '_protect_cmd_updates' from 'patch_knowledge_document' (/project/knowledge_tool/knowledge_tool/patch_knowledge_document.py)
✗ Cmd protection test failed
`

<a id="two-phase-constraint-validation-constraint-cmd-protection-when-proven"></a>
#### two_phase_constraint_validation.constraint_cmd_protection_when_proven
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.307090
**Output:** `✗ cmd protection missing
`

<a id="two-phase-constraint-validation-constraint-cmd-update-warning"></a>
#### two_phase_constraint_validation.constraint_cmd_update_warning
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.308534
**Output:** `✗ Warning message missing
`

<a id="two-phase-constraint-validation-constraint-external-proven-red-blocked"></a>
#### two_phase_constraint_validation.constraint_external_proven_red_blocked
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.305608
**Output:** `✗ proven_red not protected in patch_knowledge_document.py
`

<a id="two-phase-constraint-validation-constraint-only-proven-affects-result"></a>
#### two_phase_constraint_validation.constraint_only_proven_affects_result
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.311266
**Output:** `✗ Proven result logic missing
`

<a id="two-phase-constraint-validation-constraint-patch-protects-proven-red"></a>
#### two_phase_constraint_validation.constraint_patch_protects_proven_red
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.522501
**Output:** `Traceback (most recent call last):
  File "<string>", line 4, in <module>
ImportError: cannot import name '_restore_proven_red_values' from 'patch_knowledge_document' (/project/knowledge_tool/knowledge_tool/patch_knowledge_document.py)
✗ Protection test failed
`

<a id="two-phase-constraint-validation-constraint-print-proven-summary"></a>
#### two_phase_constraint_validation.constraint_print_proven_summary
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.312744
**Output:** `✗ Proven summary missing
`

<a id="two-phase-constraint-validation-constraint-proven-red-default-none"></a>
#### two_phase_constraint_validation.constraint_proven_red_default_none
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.304174
**Output:** `✗ Default not set correctly
`

<a id="two-phase-constraint-validation-constraint-proven-red-excluded"></a>
#### two_phase_constraint_validation.constraint_proven_red_excluded
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T21:41:48.302702
**Output:** `✓ proven_red not excluded from serialization
`

<a id="two-phase-constraint-validation-constraint-proven-red-field-exists"></a>
#### two_phase_constraint_validation.constraint_proven_red_field_exists
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.301179
**Output:** `✗ proven_red field missing
`

<a id="two-phase-constraint-validation-constraint-proven-red-in-task-json"></a>
#### two_phase_constraint_validation.constraint_proven_red_in_task_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T21:41:48.333874
**Output:** `✓ 7 constraints have proven_red set
`

<a id="two-phase-constraint-validation-constraint-set-proven-red-on-failure"></a>
#### two_phase_constraint_validation.constraint_set_proven_red_on_failure
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.309923
**Output:** `✗ Function missing
`

<a id="two-phase-constraint-validation-constraint-unprovided-constraints-logged-not-failed"></a>
#### two_phase_constraint_validation.constraint_unprovided_constraints_logged_not_failed
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T21:41:48.314173
**Output:** `✗ Unproven handling missing
`


<a id="update-iteration-with-features-stats"></a>
### Feature: update_iteration_with_features_stats

<a id="update-iteration-with-features-stats-constraint-feature-result-constraints-required"></a>
#### update_iteration_with_features_stats.constraint_feature_result_constraints_required
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.428032
**Output:** `Still optional
`

<a id="update-iteration-with-features-stats-constraint-features-stats-generated"></a>
#### update_iteration_with_features_stats.constraint_features_stats_generated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.394560
**Output:** `Generation implemented
`

<a id="update-iteration-with-features-stats-constraint-features-stats-in-iteration"></a>
#### update_iteration_with_features_stats.constraint_features_stats_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.393249
**Output:** `Field in Iteration
`

<a id="update-iteration-with-features-stats-constraint-features-stats-model-exists"></a>
#### update_iteration_with_features_stats.constraint_features_stats_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.391871
**Output:** `FeaturesStats with proper fields
`

<a id="update-iteration-with-features-stats-constraint-features-stats-rendered"></a>
#### update_iteration_with_features_stats.constraint_features_stats_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.395872
**Output:** `Rendering implemented
`

<a id="update-iteration-with-features-stats-constraint-skill-documentation-updated"></a>
#### update_iteration_with_features_stats.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.397295
**Output:** `Skill docs updated
`

<a id="update-iteration-with-features-stats-constraint-stats-displayed-on-iteration"></a>
#### update_iteration_with_features_stats.constraint_stats_displayed_on_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T12:28:25.426302
**Output:** `Stats in iteration
`
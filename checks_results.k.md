## Table of Contents

- [Constraint Results](#constraint-results)
  - [Feature: add_constraint_validation_requirement_skill](#add-constraint-validation-requirement-skill)
    - [constraint_requirement_section_exists](#add-constraint-validation-requirement-skill-constraint-requirement-section-exists)
    - [constraint_results_interpretation_guide](#add-constraint-validation-requirement-skill-constraint-results-interpretation-guide)
    - [constraint_when_to_run_documented](#add-constraint-validation-requirement-skill-constraint-when-to-run-documented)
  - [Feature: complete_task_refactor](#complete-task-refactor)
    - [constraint_complete_task_has_project_data_dir_arg](#complete-task-refactor-constraint-complete-task-has-project-data-dir-arg)
    - [constraint_complete_task_imports_config](#complete-task-refactor-constraint-complete-task-imports-config)
    - [constraint_complete_task_moves_to_iterations](#complete-task-refactor-constraint-complete-task-moves-to-iterations)
    - [constraint_complete_task_moves_to_raw_specs](#complete-task-refactor-constraint-complete-task-moves-to-raw-specs)
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
  - [Feature: decouple_spec_from_task](#decouple-spec-from-task)
    - [constraint_task_spec_document_created](#decouple-spec-from-task-constraint-task-spec-document-created)
    - [constraint_task_spec_has_spec_type](#decouple-spec-from-task-constraint-task-spec-has-spec-type)
    - [constraint_task_spec_markdown_rendered](#decouple-spec-from-task-constraint-task-spec-markdown-rendered)
    - [constraint_task_spec_no_iterations](#decouple-spec-from-task-constraint-task-spec-no-iterations)
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
    - [constraint_diff_improved_has_constraint_list](#features-stats-diff-tracking-constraint-diff-improved-has-constraint-list)
    - [constraint_diff_populates_constraint_ids](#features-stats-diff-tracking-constraint-diff-populates-constraint-ids)
    - [constraint_diff_regressed_has_constraint_list](#features-stats-diff-tracking-constraint-diff-regressed-has-constraint-list)
    - [constraint_diff_rendered_in_iteration](#features-stats-diff-tracking-constraint-diff-rendered-in-iteration)
    - [constraint_diff_still_failing_has_constraint_list](#features-stats-diff-tracking-constraint-diff-still-failing-has-constraint-list)
    - [constraint_features_stats_diff_model_exists](#features-stats-diff-tracking-constraint-features-stats-diff-model-exists)
    - [constraint_features_stats_has_diff_method](#features-stats-diff-tracking-constraint-features-stats-has-diff-method)
    - [constraint_iteration_has_diff_field](#features-stats-diff-tracking-constraint-iteration-has-diff-field)
  - [Feature: forbid_task_status_downgrade](#forbid-task-status-downgrade)
    - [constraint_status_locked_in_executing](#forbid-task-status-downgrade-constraint-status-locked-in-executing)
    - [constraint_status_validation_exists](#forbid-task-status-downgrade-constraint-status-validation-exists)
  - [Feature: iteration_always_recorded_with_test_metrics](#iteration-always-recorded-with-test-metrics)
    - [constraint_add_iteration_uses_metadata_now](#iteration-always-recorded-with-test-metrics-constraint-add-iteration-uses-metadata-now)
    - [constraint_add_iteration_uses_task_test_metrics](#iteration-always-recorded-with-test-metrics-constraint-add-iteration-uses-task-test-metrics)
    - [constraint_iteration_always_added_regardless_of_tests](#iteration-always-recorded-with-test-metrics-constraint-iteration-always-added-regardless-of-tests)
    - [constraint_metadata_has_now_factory](#iteration-always-recorded-with-test-metrics-constraint-metadata-has-now-factory)
    - [constraint_task_test_metrics_has_failed_tests](#iteration-always-recorded-with-test-metrics-constraint-task-test-metrics-has-failed-tests)
  - [Feature: iteration_summary_field](#iteration-summary-field)
    - [constraint_iteration_has_summary_field](#iteration-summary-field-constraint-iteration-has-summary-field)
  - [Feature: metadata_class_adoption](#metadata-class-adoption)
    - [constraint_doc_metadata_uses_metadata_class](#metadata-class-adoption-constraint-doc-metadata-uses-metadata-class)
    - [constraint_feature_metadata_uses_metadata_class](#metadata-class-adoption-constraint-feature-metadata-uses-metadata-class)
    - [constraint_iteration_metadata_uses_metadata_class](#metadata-class-adoption-constraint-iteration-metadata-uses-metadata-class)
    - [constraint_metadata_imported_in_doc_model](#metadata-class-adoption-constraint-metadata-imported-in-doc-model)
    - [constraint_metadata_imported_in_feature_model](#metadata-class-adoption-constraint-metadata-imported-in-feature-model)
    - [constraint_metadata_imported_in_task_model](#metadata-class-adoption-constraint-metadata-imported-in-task-model)
  - [Feature: migrate_metadata_to_model](#migrate-metadata-to-model)
    - [constraint_constraint_model_uses_metadata](#migrate-metadata-to-model-constraint-constraint-model-uses-metadata)
    - [constraint_doc_model_uses_metadata](#migrate-metadata-to-model-constraint-doc-model-uses-metadata)
    - [constraint_feature_model_uses_metadata](#migrate-metadata-to-model-constraint-feature-model-uses-metadata)
    - [constraint_metadata_import](#migrate-metadata-to-model-constraint-metadata-import)
    - [constraint_no_dict_metadata_references](#migrate-metadata-to-model-constraint-no-dict-metadata-references)
    - [constraint_spec_model_uses_metadata](#migrate-metadata-to-model-constraint-spec-model-uses-metadata)
    - [constraint_task_model_uses_metadata](#migrate-metadata-to-model-constraint-task-model-uses-metadata)
  - [Feature: project_data_dir_structure](#project-data-dir-structure)
    - [constraint_config_has_project_data_dir](#project-data-dir-structure-constraint-config-has-project-data-dir)
    - [constraint_iterations_dir_exists](#project-data-dir-structure-constraint-iterations-dir-exists)
    - [constraint_project_data_dir_path](#project-data-dir-structure-constraint-project-data-dir-path)
    - [constraint_raw_specs_dir_exists](#project-data-dir-structure-constraint-raw-specs-dir-exists)
  - [Feature: project_spec_lifecycle](#project-spec-lifecycle)
    - [constraint_check_project_constraints_exists](#project-spec-lifecycle-constraint-check-project-constraints-exists)
    - [constraint_complete_task_runs_project_checker](#project-spec-lifecycle-constraint-complete-task-runs-project-checker)
    - [constraint_complete_task_runs_task_checker](#project-spec-lifecycle-constraint-complete-task-runs-task-checker)
    - [constraint_complete_task_script_exists](#project-spec-lifecycle-constraint-complete-task-script-exists)
    - [constraint_project_spec_dir_created](#project-spec-lifecycle-constraint-project-spec-dir-created)
    - [constraint_raw_tasks_directory_created](#project-spec-lifecycle-constraint-raw-tasks-directory-created)
    - [constraint_spec_snapshot_format](#project-spec-lifecycle-constraint-spec-snapshot-format)
    - [constraint_task_json_preserved](#project-spec-lifecycle-constraint-task-json-preserved)
  - [Feature: protect_constraint_updates_when_failed](#protect-constraint-updates-when-failed)
    - [constraint_cmd_update_blocked_when_failed](#protect-constraint-updates-when-failed-constraint-cmd-update-blocked-when-failed)
    - [constraint_update_blocked_with_fails_count](#protect-constraint-updates-when-failed-constraint-update-blocked-with-fails-count)
  - [Feature: refactor_features_stats](#refactor-features-stats)
    - [constraint_diff_output_with_task_path](#refactor-features-stats-constraint-diff-output-with-task-path)
    - [constraint_diff_uses_failed_keys](#refactor-features-stats-constraint-diff-uses-failed-keys)
    - [constraint_failed_populated_on_failure](#refactor-features-stats-constraint-failed-populated-on-failure)
    - [constraint_features_checks_not_in_model](#refactor-features-stats-constraint-features-checks-not-in-model)
    - [constraint_generate_stats_no_features_checks](#refactor-features-stats-constraint-generate-stats-no-features-checks)
    - [constraint_generate_stats_returns_failed](#refactor-features-stats-constraint-generate-stats-returns-failed)
    - [constraint_script_accepts_task_iterations_path](#refactor-features-stats-constraint-script-accepts-task-iterations-path)
    - [constraint_task_model_no_features_checks](#refactor-features-stats-constraint-task-model-no-features-checks)
  - [Feature: remove_scope_from_constraint_bash](#remove-scope-from-constraint-bash)
    - [constraint_all_model_tests_pass](#remove-scope-from-constraint-bash-constraint-all-model-tests-pass)
    - [constraint_no_scope_field_usage](#remove-scope-from-constraint-bash-constraint-no-scope-field-usage)
    - [constraint_no_scope_in_constraint_bash](#remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash)
    - [constraint_scope_field_removed_from_definition](#remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition)
  - [Feature: remove_spec_field_from_task](#remove-spec-field-from-task)
    - [constraint_no_spec_in_task_json](#remove-spec-field-from-task-constraint-no-spec-in-task-json)
    - [constraint_spec_field_removed_from_model](#remove-spec-field-from-task-constraint-spec-field-removed-from-model)
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
    - [constraint_constraints_visible_in_markdown](#task-toc-includes-constraints-constraint-constraints-visible-in-markdown)
    - [constraint_toc_includes_constraints](#task-toc-includes-constraints-constraint-toc-includes-constraints)
  - [Feature: task_toc_rendering_and_links](#task-toc-rendering-and-links)
    - [constraint_anchor_sections_exist](#task-toc-rendering-and-links-constraint-anchor-sections-exist)
    - [constraint_toc_has_entries](#task-toc-rendering-and-links-constraint-toc-has-entries)
    - [constraint_toc_indentation](#task-toc-rendering-and-links-constraint-toc-indentation)
    - [constraint_toc_links_format](#task-toc-rendering-and-links-constraint-toc-links-format)
    - [constraint_toc_section_exists](#task-toc-rendering-and-links-constraint-toc-section-exists)
  - [Feature: track_unverified_constraints](#track-unverified-constraints)
    - [constraint_flag_false_with_all_proven](#track-unverified-constraints-constraint-flag-false-with-all-proven)
    - [constraint_flag_true_with_unproven](#track-unverified-constraints-constraint-flag-true-with-unproven)
    - [constraint_flag_updated_on_add](#track-unverified-constraints-constraint-flag-updated-on-add)
    - [constraint_spec_has_unverified_field](#track-unverified-constraints-constraint-spec-has-unverified-field)
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
**Timestamp:** 2026-03-18T15:51:55.911961
**Output:** `Missing
grep: skills/check_constraints/SKILL.md: No such file or directory
`

<a id="add-constraint-validation-requirement-skill-constraint-results-interpretation-guide"></a>
#### add_constraint_validation_requirement_skill.constraint_results_interpretation_guide
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.914552
**Output:** `Missing
grep: skills/check_constraints/SKILL.md: No such file or directory
`

<a id="add-constraint-validation-requirement-skill-constraint-when-to-run-documented"></a>
#### add_constraint_validation_requirement_skill.constraint_when_to_run_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.913215
**Output:** `Not documented
grep: skills/check_constraints/SKILL.md: No such file or directory
`


<a id="complete-task-refactor"></a>
### Feature: complete_task_refactor

<a id="complete-task-refactor-constraint-complete-task-has-project-data-dir-arg"></a>
#### complete_task_refactor.constraint_complete_task_has_project_data_dir_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.484108
**Output:** `def complete_task(task_path: str = 'task-iterations.k.json', task_spec_path: str = 'task-spec.k.json', project_`

<a id="complete-task-refactor-constraint-complete-task-imports-config"></a>
#### complete_task_refactor.constraint_complete_task_imports_config
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.485568
**Output:** `from config import PROJECT_DATA_DIR
        project_data_dir: Project data directory (defaults to PR`

<a id="complete-task-refactor-constraint-complete-task-moves-to-iterations"></a>
#### complete_task_refactor.constraint_complete_task_moves_to_iterations
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.487096
**Output:** `    iterations_dir = Path(project_data_dir) / 'iterations'
        # Move task-iterations.k.json to iterations/`

<a id="complete-task-refactor-constraint-complete-task-moves-to-raw-specs"></a>
#### complete_task_refactor.constraint_complete_task_moves_to_raw_specs
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.488572
**Output:** `    raw_specs_dir = Path(project_data_dir) / 'raw-specs'
        # Move task-spec.k.json to raw-spec`


<a id="constraint-bash-fails-count-cmd-protection"></a>
### Feature: constraint_bash_fails_count_cmd_protection

<a id="constraint-bash-fails-count-cmd-protection-constraint-no-default-fails-count-in-json"></a>
#### constraint_bash_fails_count_cmd_protection.constraint_no_default_fails_count_in_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.003602
**Output:** `OK: no default fails_count in spec.features constraints
`

<a id="constraint-bash-fails-count-cmd-protection-constraint-proven-constraint-removal-blocked"></a>
#### constraint_bash_fails_count_cmd_protection.constraint_proven_constraint_removal_blocked
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.546986


<a id="constraint-checker-exit-code-hook"></a>
### Feature: constraint_checker_exit_code_hook

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_calls_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.953537
**Output:** `Calls checker
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_checks_exit_code
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.954783
**Output:** `Checks exit code
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_prints_decision_block
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.956110
**Output:** `Prints decision block
`

<a id="constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure"></a>
#### constraint_checker_exit_code_hook.constraint_task_checker_exits_2_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.952254
**Output:** `Exit code 2 implemented
`


<a id="constraint-rendering-capability"></a>
### Feature: constraint_rendering_capability

<a id="constraint-rendering-capability-constraint-bash-render-method"></a>
#### constraint_rendering_capability.constraint_bash_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.899762
**Output:** `✓ ConstraintBash.render() exists
`

<a id="constraint-rendering-capability-constraint-bash-render-toc-method"></a>
#### constraint_rendering_capability.constraint_bash_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.902547
**Output:** `✓ ConstraintBash.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-feature-uses-render-toc"></a>
#### constraint_rendering_capability.constraint_feature_uses_render_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.905239
**Output:** `✓ Feature uses constraint.render_toc()
`

<a id="constraint-rendering-capability-constraint-prompt-render-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.901124
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-prompt-render-toc-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.903944
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-rendering-displays-type"></a>
#### constraint_rendering_capability.constraint_rendering_displays_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.906509


<a id="constraint-scripts-directory"></a>
### Feature: constraint_scripts_directory

<a id="constraint-scripts-directory-constraint-scripts-directory-exists"></a>
#### constraint_scripts_directory.constraint_scripts_directory_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.895900
**Output:** `✓ constraints_scripts/ directory exists
`

<a id="constraint-scripts-directory-constraint-scripts-documented"></a>
#### constraint_scripts_directory.constraint_scripts_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.897824
**Output:** `✓ Documentation found
`

<a id="constraint-scripts-directory-constraint-scripts-readme-exists"></a>
#### constraint_scripts_directory.constraint_scripts_readme_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.896525
**Output:** `✓ README.md exists
`


<a id="decouple-spec-from-task"></a>
### Feature: decouple_spec_from_task

<a id="decouple-spec-from-task-constraint-task-spec-document-created"></a>
#### decouple_spec_from_task.constraint_task_spec_document_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.547747
**Output:** `task-spec.k.json exists
`

<a id="decouple-spec-from-task-constraint-task-spec-has-spec-type"></a>
#### decouple_spec_from_task.constraint_task_spec_has_spec_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.567150

<a id="decouple-spec-from-task-constraint-task-spec-markdown-rendered"></a>
#### decouple_spec_from_task.constraint_task_spec_markdown_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.586891
**Output:** `task-spec.k.md rendered
`

<a id="decouple-spec-from-task-constraint-task-spec-no-iterations"></a>
#### decouple_spec_from_task.constraint_task_spec_no_iterations
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.586177


<a id="enhance-constraint-bash-result-output"></a>
### Feature: enhance_constraint_bash_result_output

<a id="enhance-constraint-bash-result-output-constraint-output-populated-on-failure"></a>
#### enhance_constraint_bash_result_output.constraint_output_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.909335
**Output:** `Not captured
`

<a id="enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown"></a>
#### enhance_constraint_bash_result_output.constraint_output_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.910647
**Output:** `Output rendered
`

<a id="enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists"></a>
#### enhance_constraint_bash_result_output.constraint_shrunken_output_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.907961
**Output:** `Field missing or optional
`


<a id="feature-goals-field"></a>
### Feature: feature_goals_field

<a id="feature-goals-field-constraint-goals-field-exists"></a>
#### feature_goals_field.constraint_goals_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.691111
**Output:** `✓ Goals field exists
`

<a id="feature-goals-field-constraint-goals-field-in-task"></a>
#### feature_goals_field.constraint_goals_field_in_task
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.694887
**Output:** `✗ Goals not in task-iterations.k.json
`

<a id="feature-goals-field-constraint-goals-in-toc"></a>
#### feature_goals_field.constraint_goals_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.693648
**Output:** `✓ Goals in TOC found
`

<a id="feature-goals-field-constraint-goals-rendered-in-markdown"></a>
#### feature_goals_field.constraint_goals_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.692422
**Output:** `✓ Goals rendering found
`


<a id="features-stats-diff-tracking"></a>
### Feature: features_stats_diff_tracking

<a id="features-stats-diff-tracking-constraint-diff-improved-has-constraint-list"></a>
#### features_stats_diff_tracking.constraint_diff_improved_has_constraint_list
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.962846

<a id="features-stats-diff-tracking-constraint-diff-populates-constraint-ids"></a>
#### features_stats_diff_tracking.constraint_diff_populates_constraint_ids
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.966993

<a id="features-stats-diff-tracking-constraint-diff-regressed-has-constraint-list"></a>
#### features_stats_diff_tracking.constraint_diff_regressed_has_constraint_list
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.964214

<a id="features-stats-diff-tracking-constraint-diff-rendered-in-iteration"></a>
#### features_stats_diff_tracking.constraint_diff_rendered_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.961502
**Output:** `Not implemented
`

<a id="features-stats-diff-tracking-constraint-diff-still-failing-has-constraint-list"></a>
#### features_stats_diff_tracking.constraint_diff_still_failing_has_constraint_list
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.965604

<a id="features-stats-diff-tracking-constraint-features-stats-diff-model-exists"></a>
#### features_stats_diff_tracking.constraint_features_stats_diff_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.957355
**Output:** `Model exists
`

<a id="features-stats-diff-tracking-constraint-features-stats-has-diff-method"></a>
#### features_stats_diff_tracking.constraint_features_stats_has_diff_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.958739
**Output:** `diff() method exists
`

<a id="features-stats-diff-tracking-constraint-iteration-has-diff-field"></a>
#### features_stats_diff_tracking.constraint_iteration_has_diff_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.960053
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


<a id="iteration-always-recorded-with-test-metrics"></a>
### Feature: iteration_always_recorded_with_test_metrics

<a id="iteration-always-recorded-with-test-metrics-constraint-add-iteration-uses-metadata-now"></a>
#### iteration_always_recorded_with_test_metrics.constraint_add_iteration_uses_metadata_now
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.200027

<a id="iteration-always-recorded-with-test-metrics-constraint-add-iteration-uses-task-test-metrics"></a>
#### iteration_always_recorded_with_test_metrics.constraint_add_iteration_uses_task_test_metrics
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.201267

<a id="iteration-always-recorded-with-test-metrics-constraint-iteration-always-added-regardless-of-tests"></a>
#### iteration_always_recorded_with_test_metrics.constraint_iteration_always_added_regardless_of_tests
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.202464

<a id="iteration-always-recorded-with-test-metrics-constraint-metadata-has-now-factory"></a>
#### iteration_always_recorded_with_test_metrics.constraint_metadata_has_now_factory
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.197479

<a id="iteration-always-recorded-with-test-metrics-constraint-task-test-metrics-has-failed-tests"></a>
#### iteration_always_recorded_with_test_metrics.constraint_task_test_metrics_has_failed_tests
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.198760


<a id="iteration-summary-field"></a>
### Feature: iteration_summary_field

<a id="iteration-summary-field-constraint-iteration-has-summary-field"></a>
#### iteration_summary_field.constraint_iteration_has_summary_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.187388


<a id="metadata-class-adoption"></a>
### Feature: metadata_class_adoption

<a id="metadata-class-adoption-constraint-doc-metadata-uses-metadata-class"></a>
#### metadata_class_adoption.constraint_doc_metadata_uses_metadata_class
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.188749

<a id="metadata-class-adoption-constraint-feature-metadata-uses-metadata-class"></a>
#### metadata_class_adoption.constraint_feature_metadata_uses_metadata_class
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.190110

<a id="metadata-class-adoption-constraint-iteration-metadata-uses-metadata-class"></a>
#### metadata_class_adoption.constraint_iteration_metadata_uses_metadata_class
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.191466

<a id="metadata-class-adoption-constraint-metadata-imported-in-doc-model"></a>
#### metadata_class_adoption.constraint_metadata_imported_in_doc_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.193041

<a id="metadata-class-adoption-constraint-metadata-imported-in-feature-model"></a>
#### metadata_class_adoption.constraint_metadata_imported_in_feature_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.194570

<a id="metadata-class-adoption-constraint-metadata-imported-in-task-model"></a>
#### metadata_class_adoption.constraint_metadata_imported_in_task_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.196159


<a id="migrate-metadata-to-model"></a>
### Feature: migrate_metadata_to_model

<a id="migrate-metadata-to-model-constraint-constraint-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_constraint_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.973284

<a id="migrate-metadata-to-model-constraint-doc-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_doc_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.975670

<a id="migrate-metadata-to-model-constraint-feature-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_feature_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.975089

<a id="migrate-metadata-to-model-constraint-metadata-import"></a>
#### migrate_metadata_to_model.constraint_metadata_import
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.976289

<a id="migrate-metadata-to-model-constraint-no-dict-metadata-references"></a>
#### migrate_metadata_to_model.constraint_no_dict_metadata_references
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.977741

<a id="migrate-metadata-to-model-constraint-spec-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_spec_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.974489

<a id="migrate-metadata-to-model-constraint-task-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_task_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.973889


<a id="project-data-dir-structure"></a>
### Feature: project_data_dir_structure

<a id="project-data-dir-structure-constraint-config-has-project-data-dir"></a>
#### project_data_dir_structure.constraint_config_has_project_data_dir
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.628807
**Output:** `ok
`

<a id="project-data-dir-structure-constraint-iterations-dir-exists"></a>
#### project_data_dir_structure.constraint_iterations_dir_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.650589
**Output:** `ok
`

<a id="project-data-dir-structure-constraint-project-data-dir-path"></a>
#### project_data_dir_structure.constraint_project_data_dir_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.649930

<a id="project-data-dir-structure-constraint-raw-specs-dir-exists"></a>
#### project_data_dir_structure.constraint_raw_specs_dir_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.651259
**Output:** `ok
`


<a id="project-spec-lifecycle"></a>
### Feature: project_spec_lifecycle

<a id="project-spec-lifecycle-constraint-check-project-constraints-exists"></a>
#### project_spec_lifecycle.constraint_check_project_constraints_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.409695
**Output:** `✓ check_project_constraints.py exists
`

<a id="project-spec-lifecycle-constraint-complete-task-runs-project-checker"></a>
#### project_spec_lifecycle.constraint_complete_task_runs_project_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.412761
**Output:** `✓ calls check_project_constraints
`

<a id="project-spec-lifecycle-constraint-complete-task-runs-task-checker"></a>
#### project_spec_lifecycle.constraint_complete_task_runs_task_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.411486
**Output:** `✓ calls task_features_checker
`

<a id="project-spec-lifecycle-constraint-complete-task-script-exists"></a>
#### project_spec_lifecycle.constraint_complete_task_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.410317
**Output:** `✓ complete_task.py exists
`

<a id="project-spec-lifecycle-constraint-project-spec-dir-created"></a>
#### project_spec_lifecycle.constraint_project_spec_dir_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.409099
**Output:** `✓ project-spec directory exists
`

<a id="project-spec-lifecycle-constraint-raw-tasks-directory-created"></a>
#### project_spec_lifecycle.constraint_raw_tasks_directory_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.413388
**Output:** `✓ raw-tasks directory exists
`

<a id="project-spec-lifecycle-constraint-spec-snapshot-format"></a>
#### project_spec_lifecycle.constraint_spec_snapshot_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.415261
**Output:** `✓ timestamp handling present
`

<a id="project-spec-lifecycle-constraint-task-json-preserved"></a>
#### project_spec_lifecycle.constraint_task_json_preserved
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.413999
**Output:** `✓ task-iterations.k.json preserved
`


<a id="protect-constraint-updates-when-failed"></a>
### Feature: protect_constraint_updates_when_failed

<a id="protect-constraint-updates-when-failed-constraint-cmd-update-blocked-when-failed"></a>
#### protect_constraint_updates_when_failed.constraint_cmd_update_blocked_when_failed
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:57.191667

<a id="protect-constraint-updates-when-failed-constraint-update-blocked-with-fails-count"></a>
#### protect_constraint_updates_when_failed.constraint_update_blocked_with_fails_count
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:57.744916


<a id="refactor-features-stats"></a>
### Feature: refactor_features_stats

<a id="refactor-features-stats-constraint-diff-output-with-task-path"></a>
#### refactor_features_stats.constraint_diff_output_with_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.186083

<a id="refactor-features-stats-constraint-diff-uses-failed-keys"></a>
#### refactor_features_stats.constraint_diff_uses_failed_keys
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.013339

<a id="refactor-features-stats-constraint-failed-populated-on-failure"></a>
#### refactor_features_stats.constraint_failed_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.182824

<a id="refactor-features-stats-constraint-features-checks-not-in-model"></a>
#### refactor_features_stats.constraint_features_checks_not_in_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:58.824760

<a id="refactor-features-stats-constraint-generate-stats-no-features-checks"></a>
#### refactor_features_stats.constraint_generate_stats_no_features_checks
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:58.826248

<a id="refactor-features-stats-constraint-generate-stats-returns-failed"></a>
#### refactor_features_stats.constraint_generate_stats_returns_failed
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.184535

<a id="refactor-features-stats-constraint-script-accepts-task-iterations-path"></a>
#### refactor_features_stats.constraint_script_accepts_task_iterations_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.011631

<a id="refactor-features-stats-constraint-task-model-no-features-checks"></a>
#### refactor_features_stats.constraint_task_model_no_features_checks
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:59.014859


<a id="remove-scope-from-constraint-bash"></a>
### Feature: remove_scope_from_constraint_bash

<a id="remove-scope-from-constraint-bash-constraint-all-model-tests-pass"></a>
#### remove_scope_from_constraint_bash.constraint_all_model_tests_pass
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.984955
**Output:** `Tests exist
`

<a id="remove-scope-from-constraint-bash-constraint-no-scope-field-usage"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_field_usage
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.984330

<a id="remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_in_constraint_bash
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.982914

<a id="remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition"></a>
#### remove_scope_from_constraint_bash.constraint_scope_field_removed_from_definition
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.981508


<a id="remove-spec-field-from-task"></a>
### Feature: remove_spec_field_from_task

<a id="remove-spec-field-from-task-constraint-no-spec-in-task-json"></a>
#### remove_spec_field_from_task.constraint_no_spec_in_task_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.627379

<a id="remove-spec-field-from-task-constraint-spec-field-removed-from-model"></a>
#### remove_spec_field_from_task.constraint_spec_field_removed_from_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:56.608805


<a id="render-spec-features-in-task"></a>
### Feature: render_spec_features_in_task

<a id="render-spec-features-in-task-constraint-constraint-details-in-markdown"></a>
#### render_spec_features_in_task.constraint_constraint_details_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.678123
**Output:** `✓ Constraint details found
`

<a id="render-spec-features-in-task-constraint-feature-section-in-markdown"></a>
#### render_spec_features_in_task.constraint_feature_section_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.676762
**Output:** `⚠ Features section not found
`


<a id="task-add-iteration-script"></a>
### Feature: task_add_iteration_script

<a id="task-add-iteration-script-constraint-script-exists"></a>
#### task_add_iteration_script.constraint_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.967625
**Output:** `Script exists
`

<a id="task-add-iteration-script-constraint-script-populates-features-stats"></a>
#### task_add_iteration_script.constraint_script_populates_features_stats
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.971419
**Output:** `Populates stats
`

<a id="task-add-iteration-script-constraint-script-runs-checker"></a>
#### task_add_iteration_script.constraint_script_runs_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.970085
**Output:** `Runs checker
`

<a id="task-add-iteration-script-constraint-script-uses-knowledge-tool"></a>
#### task_add_iteration_script.constraint_script_uses_knowledge_tool
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.968815
**Output:** `Uses knowledge tool
`

<a id="task-add-iteration-script-constraint-skill-documentation-updated"></a>
#### task_add_iteration_script.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.972695
**Output:** `Documented
`


<a id="task-default-render-toc"></a>
### Feature: task_default_render_toc

<a id="task-default-render-toc-constraint-default-toc-when-opts-missing"></a>
#### task_default_render_toc.constraint_default_toc_when_opts_missing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.696249
**Output:** `✓ Default opts handling found
`

<a id="task-default-render-toc-constraint-explicit-false-respected"></a>
#### task_default_render_toc.constraint_explicit_false_respected
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.699024
**Output:** `✓ Explicit False handling found
`

<a id="task-default-render-toc-constraint-render-toc-default-true"></a>
#### task_default_render_toc.constraint_render_toc_default_true
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.697646
**Output:** `✓ Default render_toc=True found
`

<a id="task-default-render-toc-constraint-toc-rendered-by-default"></a>
#### task_default_render_toc.constraint_toc_rendered_by_default
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.863714
**Output:** `✓ TOC rendered
`


<a id="task-features-checker-selective-patch"></a>
### Feature: task_features_checker_selective_patch

<a id="task-features-checker-selective-patch-constraint-feature-results-filtering"></a>
#### task_features_checker_selective_patch.constraint_feature_results_filtering
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.980154

<a id="task-features-checker-selective-patch-constraint-patch-uses-add-op"></a>
#### task_features_checker_selective_patch.constraint_patch_uses_add_op
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.979554

<a id="task-features-checker-selective-patch-constraint-preserves-other-features"></a>
#### task_features_checker_selective_patch.constraint_preserves_other_features
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.978951

<a id="task-features-checker-selective-patch-constraint-selective-patch-logic"></a>
#### task_features_checker_selective_patch.constraint_selective_patch_logic
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.978350


<a id="task-features-checker-tool"></a>
### Feature: task_features_checker_tool

<a id="task-features-checker-tool-constraint-project-root-substitution"></a>
#### task_features_checker_tool.constraint_project_root_substitution
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.688562
**Output:** `✓ PROJECT_ROOT substitution found
`

<a id="task-features-checker-tool-constraint-recursive-execution-prevention"></a>
#### task_features_checker_tool.constraint_recursive_execution_prevention
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.687182
**Output:** `✓ Recursive execution prevention found
`

<a id="task-features-checker-tool-constraint-tool-accepts-features-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_features_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.681431
**Output:** `--features arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_output_checks_path_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.682714
**Output:** `--output-checks-path arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-task-path"></a>
#### task_features_checker_tool.constraint_tool_accepts_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.680138
**Output:** `Task path argument missing
`

<a id="task-features-checker-tool-constraint-tool-exists"></a>
#### task_features_checker_tool.constraint_tool_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.678797
**Output:** `✓ tool exists
`

<a id="task-features-checker-tool-constraint-tool-output-checks-path-writable"></a>
#### task_features_checker_tool.constraint_tool_output_checks_path_writable
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.689812
**Output:** `Output path handling implemented
`

<a id="task-features-checker-tool-constraint-tool-returns-checks-results"></a>
#### task_features_checker_tool.constraint_tool_returns_checks_results
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.683975
**Output:** `ChecksResults usage found
`

<a id="task-features-checker-tool-constraint-tool-saves-results-to-file"></a>
#### task_features_checker_tool.constraint_tool_saves_results_to_file
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.685876
**Output:** `File save logic implemented
`


<a id="task-toc-includes-constraints"></a>
### Feature: task_toc_includes_constraints

<a id="task-toc-includes-constraints-constraint-constraints-visible-in-markdown"></a>
#### task_toc_includes_constraints.constraint_constraints_visible_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.866840
**Output:** `✓ Constraints visible in markdown
`

<a id="task-toc-includes-constraints-constraint-toc-includes-constraints"></a>
#### task_toc_includes_constraints.constraint_toc_includes_constraints
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.865419
**Output:** `✗ Missing
`


<a id="task-toc-rendering-and-links"></a>
### Feature: task_toc_rendering_and_links

<a id="task-toc-rendering-and-links-constraint-anchor-sections-exist"></a>
#### task_toc_rendering_and_links.constraint_anchor_sections_exist
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.893585
**Output:** `✓ All 32 TOC links have matching anchors
`

<a id="task-toc-rendering-and-links-constraint-toc-has-entries"></a>
#### task_toc_rendering_and_links.constraint_toc_has_entries
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.869561
**Output:** `✓ TOC entries found
`

<a id="task-toc-rendering-and-links-constraint-toc-indentation"></a>
#### task_toc_rendering_and_links.constraint_toc_indentation
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.895239
**Output:** `✓ Proper nesting found
`

<a id="task-toc-rendering-and-links-constraint-toc-links-format"></a>
#### task_toc_rendering_and_links.constraint_toc_links_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.871016
**Output:** `✓ Links formatted correctly
`

<a id="task-toc-rendering-and-links-constraint-toc-section-exists"></a>
#### task_toc_rendering_and_links.constraint_toc_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.868173
**Output:** `✓ TOC section found
`


<a id="track-unverified-constraints"></a>
### Feature: track_unverified_constraints

<a id="track-unverified-constraints-constraint-flag-false-with-all-proven"></a>
#### track_unverified_constraints.constraint_flag_false_with_all_proven
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:58.465687

<a id="track-unverified-constraints-constraint-flag-true-with-unproven"></a>
#### track_unverified_constraints.constraint_flag_true_with_unproven
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:58.107400

<a id="track-unverified-constraints-constraint-flag-updated-on-add"></a>
#### track_unverified_constraints.constraint_flag_updated_on_add
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:58.823115

<a id="track-unverified-constraints-constraint-spec-has-unverified-field"></a>
#### track_unverified_constraints.constraint_spec_has_unverified_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:57.746366
**Output:** `✓ Field exists
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
**Timestamp:** 2026-03-18T15:51:55.951032
**Output:** `Still optional
`

<a id="update-iteration-with-features-stats-constraint-features-stats-generated"></a>
#### update_iteration_with_features_stats.constraint_features_stats_generated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.918870
**Output:** `Generation implemented
`

<a id="update-iteration-with-features-stats-constraint-features-stats-in-iteration"></a>
#### update_iteration_with_features_stats.constraint_features_stats_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.917601
**Output:** `Field in Iteration
`

<a id="update-iteration-with-features-stats-constraint-features-stats-model-exists"></a>
#### update_iteration_with_features_stats.constraint_features_stats_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.916335
**Output:** `Model incomplete
`

<a id="update-iteration-with-features-stats-constraint-features-stats-rendered"></a>
#### update_iteration_with_features_stats.constraint_features_stats_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.920169
**Output:** `Rendering implemented
`

<a id="update-iteration-with-features-stats-constraint-skill-documentation-updated"></a>
#### update_iteration_with_features_stats.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.921608
**Output:** `Skill docs updated
`

<a id="update-iteration-with-features-stats-constraint-stats-displayed-on-iteration"></a>
#### update_iteration_with_features_stats.constraint_stats_displayed_on_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-18T15:51:55.949629
**Output:** `Not in iteration
`
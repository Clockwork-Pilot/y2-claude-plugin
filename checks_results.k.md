## Table of Contents

- [Table of Contents](#table-of-contents)
- [Constraint Results](#constraint-results)
  - [Feature: add\_constraint\_validation\_requirement\_skill](#feature-add_constraint_validation_requirement_skill)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_requirement\_section\_exists](#add_constraint_validation_requirement_skillconstraint_requirement_section_exists)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_results\_interpretation\_guide](#add_constraint_validation_requirement_skillconstraint_results_interpretation_guide)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_when\_to\_run\_documented](#add_constraint_validation_requirement_skillconstraint_when_to_run_documented)
  - [Feature: complete\_task\_refactor](#feature-complete_task_refactor)
    - [complete\_task\_refactor.constraint\_complete\_task\_has\_project\_data\_dir\_arg](#complete_task_refactorconstraint_complete_task_has_project_data_dir_arg)
    - [complete\_task\_refactor.constraint\_complete\_task\_imports\_config](#complete_task_refactorconstraint_complete_task_imports_config)
    - [complete\_task\_refactor.constraint\_complete\_task\_moves\_to\_iterations](#complete_task_refactorconstraint_complete_task_moves_to_iterations)
    - [complete\_task\_refactor.constraint\_complete\_task\_moves\_to\_raw\_specs](#complete_task_refactorconstraint_complete_task_moves_to_raw_specs)
  - [Feature: constraint\_bash\_fails\_count\_cmd\_protection](#feature-constraint_bash_fails_count_cmd_protection)
    - [constraint\_bash\_fails\_count\_cmd\_protection.constraint\_no\_default\_fails\_count\_in\_json](#constraint_bash_fails_count_cmd_protectionconstraint_no_default_fails_count_in_json)
    - [constraint\_bash\_fails\_count\_cmd\_protection.constraint\_proven\_constraint\_removal\_blocked](#constraint_bash_fails_count_cmd_protectionconstraint_proven_constraint_removal_blocked)
  - [Feature: constraint\_checker\_exit\_code\_hook](#feature-constraint_checker_exit_code_hook)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_calls\_checker](#constraint_checker_exit_code_hookconstraint_handler_stop_calls_checker)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_checks\_exit\_code](#constraint_checker_exit_code_hookconstraint_handler_stop_checks_exit_code)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_prints\_decision\_block](#constraint_checker_exit_code_hookconstraint_handler_stop_prints_decision_block)
    - [constraint\_checker\_exit\_code\_hook.constraint\_task\_checker\_exits\_2\_on\_failure](#constraint_checker_exit_code_hookconstraint_task_checker_exits_2_on_failure)
  - [Feature: constraint\_rendering\_capability](#feature-constraint_rendering_capability)
    - [constraint\_rendering\_capability.constraint\_bash\_render\_method](#constraint_rendering_capabilityconstraint_bash_render_method)
    - [constraint\_rendering\_capability.constraint\_bash\_render\_toc\_method](#constraint_rendering_capabilityconstraint_bash_render_toc_method)
    - [constraint\_rendering\_capability.constraint\_feature\_uses\_render\_toc](#constraint_rendering_capabilityconstraint_feature_uses_render_toc)
    - [constraint\_rendering\_capability.constraint\_prompt\_render\_method](#constraint_rendering_capabilityconstraint_prompt_render_method)
    - [constraint\_rendering\_capability.constraint\_prompt\_render\_toc\_method](#constraint_rendering_capabilityconstraint_prompt_render_toc_method)
    - [constraint\_rendering\_capability.constraint\_rendering\_displays\_type](#constraint_rendering_capabilityconstraint_rendering_displays_type)
  - [Feature: constraint\_scripts\_directory](#feature-constraint_scripts_directory)
    - [constraint\_scripts\_directory.constraint\_scripts\_directory\_exists](#constraint_scripts_directoryconstraint_scripts_directory_exists)
    - [constraint\_scripts\_directory.constraint\_scripts\_documented](#constraint_scripts_directoryconstraint_scripts_documented)
    - [constraint\_scripts\_directory.constraint\_scripts\_readme\_exists](#constraint_scripts_directoryconstraint_scripts_readme_exists)
  - [Feature: decouple\_spec\_from\_task](#feature-decouple_spec_from_task)
    - [decouple\_spec\_from\_task.constraint\_task\_spec\_document\_created](#decouple_spec_from_taskconstraint_task_spec_document_created)
    - [decouple\_spec\_from\_task.constraint\_task\_spec\_has\_spec\_type](#decouple_spec_from_taskconstraint_task_spec_has_spec_type)
    - [decouple\_spec\_from\_task.constraint\_task\_spec\_markdown\_rendered](#decouple_spec_from_taskconstraint_task_spec_markdown_rendered)
    - [decouple\_spec\_from\_task.constraint\_task\_spec\_no\_iterations](#decouple_spec_from_taskconstraint_task_spec_no_iterations)
  - [Feature: enhance\_constraint\_bash\_result\_output](#feature-enhance_constraint_bash_result_output)
    - [enhance\_constraint\_bash\_result\_output.constraint\_output\_populated\_on\_failure](#enhance_constraint_bash_result_outputconstraint_output_populated_on_failure)
    - [enhance\_constraint\_bash\_result\_output.constraint\_output\_rendered\_in\_markdown](#enhance_constraint_bash_result_outputconstraint_output_rendered_in_markdown)
    - [enhance\_constraint\_bash\_result\_output.constraint\_shrunken\_output\_field\_exists](#enhance_constraint_bash_result_outputconstraint_shrunken_output_field_exists)
  - [Feature: feature\_goals\_field](#feature-feature_goals_field)
    - [feature\_goals\_field.constraint\_goals\_field\_exists](#feature_goals_fieldconstraint_goals_field_exists)
    - [feature\_goals\_field.constraint\_goals\_field\_in\_task](#feature_goals_fieldconstraint_goals_field_in_task)
    - [feature\_goals\_field.constraint\_goals\_in\_toc](#feature_goals_fieldconstraint_goals_in_toc)
    - [feature\_goals\_field.constraint\_goals\_rendered\_in\_markdown](#feature_goals_fieldconstraint_goals_rendered_in_markdown)
  - [Feature: features\_stats\_diff\_tracking](#feature-features_stats_diff_tracking)
    - [features\_stats\_diff\_tracking.constraint\_diff\_rendered\_in\_iteration](#features_stats_diff_trackingconstraint_diff_rendered_in_iteration)
    - [features\_stats\_diff\_tracking.constraint\_features\_stats\_diff\_model\_exists](#features_stats_diff_trackingconstraint_features_stats_diff_model_exists)
    - [features\_stats\_diff\_tracking.constraint\_features\_stats\_has\_diff\_method](#features_stats_diff_trackingconstraint_features_stats_has_diff_method)
    - [features\_stats\_diff\_tracking.constraint\_iteration\_has\_diff\_field](#features_stats_diff_trackingconstraint_iteration_has_diff_field)
  - [Feature: forbid\_task\_status\_downgrade](#feature-forbid_task_status_downgrade)
    - [forbid\_task\_status\_downgrade.constraint\_status\_locked\_in\_executing](#forbid_task_status_downgradeconstraint_status_locked_in_executing)
    - [forbid\_task\_status\_downgrade.constraint\_status\_validation\_exists](#forbid_task_status_downgradeconstraint_status_validation_exists)
  - [Feature: migrate\_metadata\_to\_model](#feature-migrate_metadata_to_model)
    - [migrate\_metadata\_to\_model.constraint\_constraint\_model\_uses\_metadata](#migrate_metadata_to_modelconstraint_constraint_model_uses_metadata)
    - [migrate\_metadata\_to\_model.constraint\_doc\_model\_uses\_metadata](#migrate_metadata_to_modelconstraint_doc_model_uses_metadata)
    - [migrate\_metadata\_to\_model.constraint\_feature\_model\_uses\_metadata](#migrate_metadata_to_modelconstraint_feature_model_uses_metadata)
    - [migrate\_metadata\_to\_model.constraint\_metadata\_import](#migrate_metadata_to_modelconstraint_metadata_import)
    - [migrate\_metadata\_to\_model.constraint\_no\_dict\_metadata\_references](#migrate_metadata_to_modelconstraint_no_dict_metadata_references)
    - [migrate\_metadata\_to\_model.constraint\_spec\_model\_uses\_metadata](#migrate_metadata_to_modelconstraint_spec_model_uses_metadata)
    - [migrate\_metadata\_to\_model.constraint\_task\_model\_uses\_metadata](#migrate_metadata_to_modelconstraint_task_model_uses_metadata)
  - [Feature: project\_data\_dir\_structure](#feature-project_data_dir_structure)
    - [project\_data\_dir\_structure.constraint\_config\_has\_project\_data\_dir](#project_data_dir_structureconstraint_config_has_project_data_dir)
    - [project\_data\_dir\_structure.constraint\_iterations\_dir\_exists](#project_data_dir_structureconstraint_iterations_dir_exists)
    - [project\_data\_dir\_structure.constraint\_project\_data\_dir\_path](#project_data_dir_structureconstraint_project_data_dir_path)
    - [project\_data\_dir\_structure.constraint\_raw\_specs\_dir\_exists](#project_data_dir_structureconstraint_raw_specs_dir_exists)
  - [Feature: project\_spec\_lifecycle](#feature-project_spec_lifecycle)
    - [project\_spec\_lifecycle.constraint\_check\_project\_constraints\_exists](#project_spec_lifecycleconstraint_check_project_constraints_exists)
    - [project\_spec\_lifecycle.constraint\_complete\_task\_runs\_project\_checker](#project_spec_lifecycleconstraint_complete_task_runs_project_checker)
    - [project\_spec\_lifecycle.constraint\_complete\_task\_runs\_task\_checker](#project_spec_lifecycleconstraint_complete_task_runs_task_checker)
    - [project\_spec\_lifecycle.constraint\_complete\_task\_script\_exists](#project_spec_lifecycleconstraint_complete_task_script_exists)
    - [project\_spec\_lifecycle.constraint\_project\_spec\_dir\_created](#project_spec_lifecycleconstraint_project_spec_dir_created)
    - [project\_spec\_lifecycle.constraint\_raw\_tasks\_directory\_created](#project_spec_lifecycleconstraint_raw_tasks_directory_created)
    - [project\_spec\_lifecycle.constraint\_spec\_snapshot\_format](#project_spec_lifecycleconstraint_spec_snapshot_format)
    - [project\_spec\_lifecycle.constraint\_task\_json\_preserved](#project_spec_lifecycleconstraint_task_json_preserved)
  - [Feature: remove\_scope\_from\_constraint\_bash](#feature-remove_scope_from_constraint_bash)
    - [remove\_scope\_from\_constraint\_bash.constraint\_all\_model\_tests\_pass](#remove_scope_from_constraint_bashconstraint_all_model_tests_pass)
    - [remove\_scope\_from\_constraint\_bash.constraint\_no\_scope\_field\_usage](#remove_scope_from_constraint_bashconstraint_no_scope_field_usage)
    - [remove\_scope\_from\_constraint\_bash.constraint\_no\_scope\_in\_constraint\_bash](#remove_scope_from_constraint_bashconstraint_no_scope_in_constraint_bash)
    - [remove\_scope\_from\_constraint\_bash.constraint\_scope\_field\_removed\_from\_definition](#remove_scope_from_constraint_bashconstraint_scope_field_removed_from_definition)
  - [Feature: remove\_spec\_field\_from\_task](#feature-remove_spec_field_from_task)
    - [remove\_spec\_field\_from\_task.constraint\_no\_spec\_in\_task\_json](#remove_spec_field_from_taskconstraint_no_spec_in_task_json)
    - [remove\_spec\_field\_from\_task.constraint\_spec\_field\_removed\_from\_model](#remove_spec_field_from_taskconstraint_spec_field_removed_from_model)
  - [Feature: render\_spec\_features\_in\_task](#feature-render_spec_features_in_task)
    - [render\_spec\_features\_in\_task.constraint\_constraint\_details\_in\_markdown](#render_spec_features_in_taskconstraint_constraint_details_in_markdown)
    - [render\_spec\_features\_in\_task.constraint\_feature\_section\_in\_markdown](#render_spec_features_in_taskconstraint_feature_section_in_markdown)
  - [Feature: task\_add\_iteration\_script](#feature-task_add_iteration_script)
    - [task\_add\_iteration\_script.constraint\_script\_exists](#task_add_iteration_scriptconstraint_script_exists)
    - [task\_add\_iteration\_script.constraint\_script\_populates\_features\_stats](#task_add_iteration_scriptconstraint_script_populates_features_stats)
    - [task\_add\_iteration\_script.constraint\_script\_runs\_checker](#task_add_iteration_scriptconstraint_script_runs_checker)
    - [task\_add\_iteration\_script.constraint\_script\_uses\_knowledge\_tool](#task_add_iteration_scriptconstraint_script_uses_knowledge_tool)
    - [task\_add\_iteration\_script.constraint\_skill\_documentation\_updated](#task_add_iteration_scriptconstraint_skill_documentation_updated)
  - [Feature: task\_default\_render\_toc](#feature-task_default_render_toc)
    - [task\_default\_render\_toc.constraint\_default\_toc\_when\_opts\_missing](#task_default_render_tocconstraint_default_toc_when_opts_missing)
    - [task\_default\_render\_toc.constraint\_explicit\_false\_respected](#task_default_render_tocconstraint_explicit_false_respected)
    - [task\_default\_render\_toc.constraint\_render\_toc\_default\_true](#task_default_render_tocconstraint_render_toc_default_true)
    - [task\_default\_render\_toc.constraint\_toc\_rendered\_by\_default](#task_default_render_tocconstraint_toc_rendered_by_default)
  - [Feature: task\_features\_checker\_selective\_patch](#feature-task_features_checker_selective_patch)
    - [task\_features\_checker\_selective\_patch.constraint\_feature\_results\_filtering](#task_features_checker_selective_patchconstraint_feature_results_filtering)
    - [task\_features\_checker\_selective\_patch.constraint\_patch\_uses\_add\_op](#task_features_checker_selective_patchconstraint_patch_uses_add_op)
    - [task\_features\_checker\_selective\_patch.constraint\_preserves\_other\_features](#task_features_checker_selective_patchconstraint_preserves_other_features)
    - [task\_features\_checker\_selective\_patch.constraint\_selective\_patch\_logic](#task_features_checker_selective_patchconstraint_selective_patch_logic)
  - [Feature: task\_features\_checker\_tool](#feature-task_features_checker_tool)
    - [task\_features\_checker\_tool.constraint\_project\_root\_substitution](#task_features_checker_toolconstraint_project_root_substitution)
    - [task\_features\_checker\_tool.constraint\_recursive\_execution\_prevention](#task_features_checker_toolconstraint_recursive_execution_prevention)
    - [task\_features\_checker\_tool.constraint\_tool\_accepts\_features\_arg](#task_features_checker_toolconstraint_tool_accepts_features_arg)
    - [task\_features\_checker\_tool.constraint\_tool\_accepts\_output\_checks\_path\_arg](#task_features_checker_toolconstraint_tool_accepts_output_checks_path_arg)
    - [task\_features\_checker\_tool.constraint\_tool\_accepts\_task\_path](#task_features_checker_toolconstraint_tool_accepts_task_path)
    - [task\_features\_checker\_tool.constraint\_tool\_exists](#task_features_checker_toolconstraint_tool_exists)
    - [task\_features\_checker\_tool.constraint\_tool\_output\_checks\_path\_writable](#task_features_checker_toolconstraint_tool_output_checks_path_writable)
    - [task\_features\_checker\_tool.constraint\_tool\_returns\_checks\_results](#task_features_checker_toolconstraint_tool_returns_checks_results)
    - [task\_features\_checker\_tool.constraint\_tool\_saves\_results\_to\_file](#task_features_checker_toolconstraint_tool_saves_results_to_file)
  - [Feature: task\_toc\_includes\_constraints](#feature-task_toc_includes_constraints)
    - [task\_toc\_includes\_constraints.constraint\_constraints\_nested\_in\_toc](#task_toc_includes_constraintsconstraint_constraints_nested_in_toc)
    - [task\_toc\_includes\_constraints.constraint\_constraints\_visible\_in\_markdown](#task_toc_includes_constraintsconstraint_constraints_visible_in_markdown)
    - [task\_toc\_includes\_constraints.constraint\_toc\_includes\_constraints](#task_toc_includes_constraintsconstraint_toc_includes_constraints)
  - [Feature: task\_toc\_rendering\_and\_links](#feature-task_toc_rendering_and_links)
    - [task\_toc\_rendering\_and\_links.constraint\_anchor\_sections\_exist](#task_toc_rendering_and_linksconstraint_anchor_sections_exist)
    - [task\_toc\_rendering\_and\_links.constraint\_toc\_has\_entries](#task_toc_rendering_and_linksconstraint_toc_has_entries)
    - [task\_toc\_rendering\_and\_links.constraint\_toc\_indentation](#task_toc_rendering_and_linksconstraint_toc_indentation)
    - [task\_toc\_rendering\_and\_links.constraint\_toc\_links\_format](#task_toc_rendering_and_linksconstraint_toc_links_format)
    - [task\_toc\_rendering\_and\_links.constraint\_toc\_section\_exists](#task_toc_rendering_and_linksconstraint_toc_section_exists)
  - [Feature: two\_phase\_constraint\_validation](#feature-two_phase_constraint_validation)
    - [two\_phase\_constraint\_validation.constraint\_cmd\_protection\_verified](#two_phase_constraint_validationconstraint_cmd_protection_verified)
    - [two\_phase\_constraint\_validation.constraint\_cmd\_protection\_when\_proven](#two_phase_constraint_validationconstraint_cmd_protection_when_proven)
    - [two\_phase\_constraint\_validation.constraint\_cmd\_update\_warning](#two_phase_constraint_validationconstraint_cmd_update_warning)
    - [two\_phase\_constraint\_validation.constraint\_external\_proven\_red\_blocked](#two_phase_constraint_validationconstraint_external_proven_red_blocked)
    - [two\_phase\_constraint\_validation.constraint\_only\_proven\_affects\_result](#two_phase_constraint_validationconstraint_only_proven_affects_result)
    - [two\_phase\_constraint\_validation.constraint\_patch\_protects\_proven\_red](#two_phase_constraint_validationconstraint_patch_protects_proven_red)
    - [two\_phase\_constraint\_validation.constraint\_print\_proven\_summary](#two_phase_constraint_validationconstraint_print_proven_summary)
    - [two\_phase\_constraint\_validation.constraint\_proven\_red\_default\_none](#two_phase_constraint_validationconstraint_proven_red_default_none)
    - [two\_phase\_constraint\_validation.constraint\_proven\_red\_excluded](#two_phase_constraint_validationconstraint_proven_red_excluded)
    - [two\_phase\_constraint\_validation.constraint\_proven\_red\_field\_exists](#two_phase_constraint_validationconstraint_proven_red_field_exists)
    - [two\_phase\_constraint\_validation.constraint\_proven\_red\_in\_task\_json](#two_phase_constraint_validationconstraint_proven_red_in_task_json)
    - [two\_phase\_constraint\_validation.constraint\_set\_proven\_red\_on\_failure](#two_phase_constraint_validationconstraint_set_proven_red_on_failure)
    - [two\_phase\_constraint\_validation.constraint\_unprovided\_constraints\_logged\_not\_failed](#two_phase_constraint_validationconstraint_unprovided_constraints_logged_not_failed)
  - [Feature: update\_iteration\_with\_features\_stats](#feature-update_iteration_with_features_stats)
    - [update\_iteration\_with\_features\_stats.constraint\_feature\_result\_constraints\_required](#update_iteration_with_features_statsconstraint_feature_result_constraints_required)
    - [update\_iteration\_with\_features\_stats.constraint\_features\_stats\_generated](#update_iteration_with_features_statsconstraint_features_stats_generated)
    - [update\_iteration\_with\_features\_stats.constraint\_features\_stats\_in\_iteration](#update_iteration_with_features_statsconstraint_features_stats_in_iteration)
    - [update\_iteration\_with\_features\_stats.constraint\_features\_stats\_model\_exists](#update_iteration_with_features_statsconstraint_features_stats_model_exists)
    - [update\_iteration\_with\_features\_stats.constraint\_features\_stats\_rendered](#update_iteration_with_features_statsconstraint_features_stats_rendered)
    - [update\_iteration\_with\_features\_stats.constraint\_skill\_documentation\_updated](#update_iteration_with_features_statsconstraint_skill_documentation_updated)
    - [update\_iteration\_with\_features\_stats.constraint\_stats\_displayed\_on\_iteration](#update_iteration_with_features_statsconstraint_stats_displayed_on_iteration)
  - [Feature: y2\_skills\_update](#feature-y2_skills_update)
    - [y2\_skills\_update.constraint\_features\_checks\_tool\_updated](#y2_skills_updateconstraint_features_checks_tool_updated)
    - [y2\_skills\_update.constraint\_knowledge\_tool\_docs\_updated](#y2_skills_updateconstraint_knowledge_tool_docs_updated)

## Constraint Results

<a id="add-constraint-validation-requirement-skill"></a>
### Feature: add_constraint_validation_requirement_skill

<a id="add-constraint-validation-requirement-skill-constraint-requirement-section-exists"></a>
#### add_constraint_validation_requirement_skill.constraint_requirement_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.338392
**Output:** `Requirement section found
`

<a id="add-constraint-validation-requirement-skill-constraint-results-interpretation-guide"></a>
#### add_constraint_validation_requirement_skill.constraint_results_interpretation_guide
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.341052
**Output:** `Interpretation guide exists
`

<a id="add-constraint-validation-requirement-skill-constraint-when-to-run-documented"></a>
#### add_constraint_validation_requirement_skill.constraint_when_to_run_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.339665
**Output:** `When section documented
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
**Timestamp:** 2026-03-17T13:27:45.435067
**Output:** `OK: no default fails_count in spec.features constraints
`

<a id="constraint-bash-fails-count-cmd-protection-constraint-proven-constraint-removal-blocked"></a>
#### constraint_bash_fails_count_cmd_protection.constraint_proven_constraint_removal_blocked
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:46.016244


<a id="constraint-checker-exit-code-hook"></a>
### Feature: constraint_checker_exit_code_hook

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_calls_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.381996
**Output:** `Calls checker
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_checks_exit_code
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.383322
**Output:** `Checks exit code
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_prints_decision_block
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.384608
**Output:** `Prints decision block
`

<a id="constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure"></a>
#### constraint_checker_exit_code_hook.constraint_task_checker_exits_2_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.380729
**Output:** `Exit code 2 implemented
`


<a id="constraint-rendering-capability"></a>
### Feature: constraint_rendering_capability

<a id="constraint-rendering-capability-constraint-bash-render-method"></a>
#### constraint_rendering_capability.constraint_bash_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.326314
**Output:** `✓ ConstraintBash.render() exists
`

<a id="constraint-rendering-capability-constraint-bash-render-toc-method"></a>
#### constraint_rendering_capability.constraint_bash_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.329082
**Output:** `✓ ConstraintBash.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-feature-uses-render-toc"></a>
#### constraint_rendering_capability.constraint_feature_uses_render_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.331654
**Output:** `✓ Feature uses constraint.render_toc()
`

<a id="constraint-rendering-capability-constraint-prompt-render-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.327721
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-prompt-render-toc-method"></a>
#### constraint_rendering_capability.constraint_prompt_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.330434
**Output:** `✗ Missing
`

<a id="constraint-rendering-capability-constraint-rendering-displays-type"></a>
#### constraint_rendering_capability.constraint_rendering_displays_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.332867


<a id="constraint-scripts-directory"></a>
### Feature: constraint_scripts_directory

<a id="constraint-scripts-directory-constraint-scripts-directory-exists"></a>
#### constraint_scripts_directory.constraint_scripts_directory_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.321828
**Output:** `✓ constraints_scripts/ directory exists
`

<a id="constraint-scripts-directory-constraint-scripts-documented"></a>
#### constraint_scripts_directory.constraint_scripts_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.324085
**Output:** `✓ Documentation found
`

<a id="constraint-scripts-directory-constraint-scripts-readme-exists"></a>
#### constraint_scripts_directory.constraint_scripts_readme_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.322473
**Output:** `✓ README.md exists
`


<a id="decouple-spec-from-task"></a>
### Feature: decouple_spec_from_task

<a id="decouple-spec-from-task-constraint-task-spec-document-created"></a>
#### decouple_spec_from_task.constraint_task_spec_document_created
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.367998
**Output:** `task-spec.k.json exists
`

<a id="decouple-spec-from-task-constraint-task-spec-has-spec-type"></a>
#### decouple_spec_from_task.constraint_task_spec_has_spec_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.387907

<a id="decouple-spec-from-task-constraint-task-spec-markdown-rendered"></a>
#### decouple_spec_from_task.constraint_task_spec_markdown_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.409283
**Output:** `task-spec.k.md rendered
`

<a id="decouple-spec-from-task-constraint-task-spec-no-iterations"></a>
#### decouple_spec_from_task.constraint_task_spec_no_iterations
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.408473


<a id="enhance-constraint-bash-result-output"></a>
### Feature: enhance_constraint_bash_result_output

<a id="enhance-constraint-bash-result-output-constraint-output-populated-on-failure"></a>
#### enhance_constraint_bash_result_output.constraint_output_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.335705
**Output:** `Not captured
`

<a id="enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown"></a>
#### enhance_constraint_bash_result_output.constraint_output_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.337003
**Output:** `Output rendered
`

<a id="enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists"></a>
#### enhance_constraint_bash_result_output.constraint_shrunken_output_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.334274
**Output:** `Field missing or optional
`


<a id="feature-goals-field"></a>
### Feature: feature_goals_field

<a id="feature-goals-field-constraint-goals-field-exists"></a>
#### feature_goals_field.constraint_goals_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.940808
**Output:** `✓ Goals field exists
`

<a id="feature-goals-field-constraint-goals-field-in-task"></a>
#### feature_goals_field.constraint_goals_field_in_task
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.944575
**Output:** `✓ Goals in task-iterations.k.json
`

<a id="feature-goals-field-constraint-goals-in-toc"></a>
#### feature_goals_field.constraint_goals_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.943350
**Output:** `✓ Goals in TOC found
`

<a id="feature-goals-field-constraint-goals-rendered-in-markdown"></a>
#### feature_goals_field.constraint_goals_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.942091
**Output:** `✓ Goals rendering found
`


<a id="features-stats-diff-tracking"></a>
### Feature: features_stats_diff_tracking

<a id="features-stats-diff-tracking-constraint-diff-rendered-in-iteration"></a>
#### features_stats_diff_tracking.constraint_diff_rendered_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.390147
**Output:** `Not implemented
`

<a id="features-stats-diff-tracking-constraint-features-stats-diff-model-exists"></a>
#### features_stats_diff_tracking.constraint_features_stats_diff_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.385885
**Output:** `Model exists
`

<a id="features-stats-diff-tracking-constraint-features-stats-has-diff-method"></a>
#### features_stats_diff_tracking.constraint_features_stats_has_diff_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.387333
**Output:** `diff() method exists
`

<a id="features-stats-diff-tracking-constraint-iteration-has-diff-field"></a>
#### features_stats_diff_tracking.constraint_iteration_has_diff_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.388656
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
**Timestamp:** 2026-03-17T13:27:45.396385

<a id="migrate-metadata-to-model-constraint-doc-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_doc_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.398824

<a id="migrate-metadata-to-model-constraint-feature-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_feature_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.398206

<a id="migrate-metadata-to-model-constraint-metadata-import"></a>
#### migrate_metadata_to_model.constraint_metadata_import
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.399437

<a id="migrate-metadata-to-model-constraint-no-dict-metadata-references"></a>
#### migrate_metadata_to_model.constraint_no_dict_metadata_references
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.400932

<a id="migrate-metadata-to-model-constraint-spec-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_spec_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.397602

<a id="migrate-metadata-to-model-constraint-task-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_task_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.396994


<a id="project-data-dir-structure"></a>
### Feature: project_data_dir_structure

<a id="project-data-dir-structure-constraint-config-has-project-data-dir"></a>
#### project_data_dir_structure.constraint_config_has_project_data_dir
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.455191
**Output:** `ok
`

<a id="project-data-dir-structure-constraint-iterations-dir-exists"></a>
#### project_data_dir_structure.constraint_iterations_dir_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.481793
**Output:** `ok
`

<a id="project-data-dir-structure-constraint-project-data-dir-path"></a>
#### project_data_dir_structure.constraint_project_data_dir_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.480927

<a id="project-data-dir-structure-constraint-raw-specs-dir-exists"></a>
#### project_data_dir_structure.constraint_raw_specs_dir_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.482505
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


<a id="remove-scope-from-constraint-bash"></a>
### Feature: remove_scope_from_constraint_bash

<a id="remove-scope-from-constraint-bash-constraint-all-model-tests-pass"></a>
#### remove_scope_from_constraint_bash.constraint_all_model_tests_pass
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.408451
**Output:** `Tests exist
`

<a id="remove-scope-from-constraint-bash-constraint-no-scope-field-usage"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_field_usage
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.407804

<a id="remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_in_constraint_bash
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.406356

<a id="remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition"></a>
#### remove_scope_from_constraint_bash.constraint_scope_field_removed_from_definition
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.404788


<a id="remove-spec-field-from-task"></a>
### Feature: remove_spec_field_from_task

<a id="remove-spec-field-from-task-constraint-no-spec-in-task-json"></a>
#### remove_spec_field_from_task.constraint_no_spec_in_task_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.453446

<a id="remove-spec-field-from-task-constraint-spec-field-removed-from-model"></a>
#### remove_spec_field_from_task.constraint_spec_field_removed_from_model
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.432748


<a id="render-spec-features-in-task"></a>
### Feature: render_spec_features_in_task

<a id="render-spec-features-in-task-constraint-constraint-details-in-markdown"></a>
#### render_spec_features_in_task.constraint_constraint_details_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.927531
**Output:** `✓ Constraint details found
`

<a id="render-spec-features-in-task-constraint-feature-section-in-markdown"></a>
#### render_spec_features_in_task.constraint_feature_section_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.926168
**Output:** `✓ Features section found in markdown
`


<a id="task-add-iteration-script"></a>
### Feature: task_add_iteration_script

<a id="task-add-iteration-script-constraint-script-exists"></a>
#### task_add_iteration_script.constraint_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.390803
**Output:** `Script exists
`

<a id="task-add-iteration-script-constraint-script-populates-features-stats"></a>
#### task_add_iteration_script.constraint_script_populates_features_stats
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.394446
**Output:** `Populates stats
`

<a id="task-add-iteration-script-constraint-script-runs-checker"></a>
#### task_add_iteration_script.constraint_script_runs_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.393257
**Output:** `Runs checker
`

<a id="task-add-iteration-script-constraint-script-uses-knowledge-tool"></a>
#### task_add_iteration_script.constraint_script_uses_knowledge_tool
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.392025
**Output:** `Uses knowledge tool
`

<a id="task-add-iteration-script-constraint-skill-documentation-updated"></a>
#### task_add_iteration_script.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.395757
**Output:** `Documented
`


<a id="task-default-render-toc"></a>
### Feature: task_default_render_toc

<a id="task-default-render-toc-constraint-default-toc-when-opts-missing"></a>
#### task_default_render_toc.constraint_default_toc_when_opts_missing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.945905
**Output:** `✓ Default opts handling found
`

<a id="task-default-render-toc-constraint-explicit-false-respected"></a>
#### task_default_render_toc.constraint_explicit_false_respected
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.948625
**Output:** `✓ Explicit False handling found
`

<a id="task-default-render-toc-constraint-render-toc-default-true"></a>
#### task_default_render_toc.constraint_render_toc_default_true
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.947243
**Output:** `✓ Default render_toc=True found
`

<a id="task-default-render-toc-constraint-toc-rendered-by-default"></a>
#### task_default_render_toc.constraint_toc_rendered_by_default
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.124624
**Output:** `✓ TOC rendered
`


<a id="task-features-checker-selective-patch"></a>
### Feature: task_features_checker_selective_patch

<a id="task-features-checker-selective-patch-constraint-feature-results-filtering"></a>
#### task_features_checker_selective_patch.constraint_feature_results_filtering
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.403356

<a id="task-features-checker-selective-patch-constraint-patch-uses-add-op"></a>
#### task_features_checker_selective_patch.constraint_patch_uses_add_op
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.402745

<a id="task-features-checker-selective-patch-constraint-preserves-other-features"></a>
#### task_features_checker_selective_patch.constraint_preserves_other_features
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.402134

<a id="task-features-checker-selective-patch-constraint-selective-patch-logic"></a>
#### task_features_checker_selective_patch.constraint_selective_patch_logic
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.401527


<a id="task-features-checker-tool"></a>
### Feature: task_features_checker_tool

<a id="task-features-checker-tool-constraint-project-root-substitution"></a>
#### task_features_checker_tool.constraint_project_root_substitution
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.938192
**Output:** `✓ PROJECT_ROOT substitution found
`

<a id="task-features-checker-tool-constraint-recursive-execution-prevention"></a>
#### task_features_checker_tool.constraint_recursive_execution_prevention
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.936931
**Output:** `✓ Recursive execution prevention found
`

<a id="task-features-checker-tool-constraint-tool-accepts-features-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_features_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.930958
**Output:** `--features arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_output_checks_path_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.932324
**Output:** `--output-checks-path arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-task-path"></a>
#### task_features_checker_tool.constraint_tool_accepts_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.929622
**Output:** `Task path argument missing
`

<a id="task-features-checker-tool-constraint-tool-exists"></a>
#### task_features_checker_tool.constraint_tool_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.928178
**Output:** `✓ tool exists
`

<a id="task-features-checker-tool-constraint-tool-output-checks-path-writable"></a>
#### task_features_checker_tool.constraint_tool_output_checks_path_writable
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.939511
**Output:** `Output path handling implemented
`

<a id="task-features-checker-tool-constraint-tool-returns-checks-results"></a>
#### task_features_checker_tool.constraint_tool_returns_checks_results
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.933663
**Output:** `ChecksResults usage found
`

<a id="task-features-checker-tool-constraint-tool-saves-results-to-file"></a>
#### task_features_checker_tool.constraint_tool_saves_results_to_file
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:44.935619
**Output:** `File save logic implemented
`


<a id="task-toc-includes-constraints"></a>
### Feature: task_toc_includes_constraints

<a id="task-toc-includes-constraints-constraint-constraints-nested-in-toc"></a>
#### task_toc_includes_constraints.constraint_constraints_nested_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.289460
**Output:** `✗ No constraints in TOC
`

<a id="task-toc-includes-constraints-constraint-constraints-visible-in-markdown"></a>
#### task_toc_includes_constraints.constraint_constraints_visible_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.291010
**Output:** `✓ Constraints visible in markdown
`

<a id="task-toc-includes-constraints-constraint-toc-includes-constraints"></a>
#### task_toc_includes_constraints.constraint_toc_includes_constraints
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.126281
**Output:** `✗ Missing
`


<a id="task-toc-rendering-and-links"></a>
### Feature: task_toc_rendering_and_links

<a id="task-toc-rendering-and-links-constraint-anchor-sections-exist"></a>
#### task_toc_rendering_and_links.constraint_anchor_sections_exist
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.319326
**Output:** `✓ All 141 TOC links have matching anchors
`

<a id="task-toc-rendering-and-links-constraint-toc-has-entries"></a>
#### task_toc_rendering_and_links.constraint_toc_has_entries
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.293928
**Output:** `✓ TOC entries found
`

<a id="task-toc-rendering-and-links-constraint-toc-indentation"></a>
#### task_toc_rendering_and_links.constraint_toc_indentation
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.321119
**Output:** `✓ Proper nesting found
`

<a id="task-toc-rendering-and-links-constraint-toc-links-format"></a>
#### task_toc_rendering_and_links.constraint_toc_links_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.295390
**Output:** `✓ Links formatted correctly
`

<a id="task-toc-rendering-and-links-constraint-toc-section-exists"></a>
#### task_toc_rendering_and_links.constraint_toc_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.292380
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
**Timestamp:** 2026-03-17T13:27:45.379381
**Output:** `Still optional
`

<a id="update-iteration-with-features-stats-constraint-features-stats-generated"></a>
#### update_iteration_with_features_stats.constraint_features_stats_generated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.345758
**Output:** `Generation implemented
`

<a id="update-iteration-with-features-stats-constraint-features-stats-in-iteration"></a>
#### update_iteration_with_features_stats.constraint_features_stats_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.344459
**Output:** `Field in Iteration
`

<a id="update-iteration-with-features-stats-constraint-features-stats-model-exists"></a>
#### update_iteration_with_features_stats.constraint_features_stats_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.343135
**Output:** `FeaturesStats with proper fields
`

<a id="update-iteration-with-features-stats-constraint-features-stats-rendered"></a>
#### update_iteration_with_features_stats.constraint_features_stats_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.347095
**Output:** `Rendering implemented
`

<a id="update-iteration-with-features-stats-constraint-skill-documentation-updated"></a>
#### update_iteration_with_features_stats.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.348423
**Output:** `Skill docs updated
`

<a id="update-iteration-with-features-stats-constraint-stats-displayed-on-iteration"></a>
#### update_iteration_with_features_stats.constraint_stats_displayed_on_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T13:27:45.377709
**Output:** `Stats in iteration
`


<a id="y2-skills-update"></a>
### Feature: y2_skills_update

<a id="y2-skills-update-constraint-features-checks-tool-updated"></a>
#### y2_skills_update.constraint_features_checks_tool_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.491496
**Output:** `ok
`

<a id="y2-skills-update-constraint-knowledge-tool-docs-updated"></a>
#### y2_skills_update.constraint_knowledge_tool_docs_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-17T14:05:09.490097
**Output:** `## Task-Spec Document Pattern
As of the spec decoupling refactor, specifications are now maintained `
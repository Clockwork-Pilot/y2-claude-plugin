## Table of Contents

- [Table of Contents](#table-of-contents)
- [Constraint Results](#constraint-results)
  - [Feature: add\_constraint\_validation\_requirement\_skill](#feature-add_constraint_validation_requirement_skill)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_requirement\_section\_exists](#add_constraint_validation_requirement_skillconstraint_requirement_section_exists)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_results\_interpretation\_guide](#add_constraint_validation_requirement_skillconstraint_results_interpretation_guide)
    - [add\_constraint\_validation\_requirement\_skill.constraint\_when\_to\_run\_documented](#add_constraint_validation_requirement_skillconstraint_when_to_run_documented)
  - [Feature: constraint\_checker\_exit\_code\_hook](#feature-constraint_checker_exit_code_hook)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_calls\_checker](#constraint_checker_exit_code_hookconstraint_handler_stop_calls_checker)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_checks\_exit\_code](#constraint_checker_exit_code_hookconstraint_handler_stop_checks_exit_code)
    - [constraint\_checker\_exit\_code\_hook.constraint\_handler\_stop\_prints\_decision\_block](#constraint_checker_exit_code_hookconstraint_handler_stop_prints_decision_block)
    - [constraint\_checker\_exit\_code\_hook.constraint\_task\_checker\_exits\_2\_on\_failure](#constraint_checker_exit_code_hookconstraint_task_checker_exits_2_on_failure)
  - [Feature: constraint\_rendering\_capability](#feature-constraint_rendering_capability)
    - [constraint\_rendering\_capability.constraint\_bash\_render\_method](#constraint_rendering_capabilityconstraint_bash_render_method)
    - [constraint\_rendering\_capability.constraint\_bash\_render\_toc\_method](#constraint_rendering_capabilityconstraint_bash_render_toc_method)
    - [constraint\_rendering\_capability.constraint\_feature\_uses\_render\_toc](#constraint_rendering_capabilityconstraint_feature_uses_render_toc)
    - [constraint\_rendering\_capability.constraint\_rendering\_displays\_type](#constraint_rendering_capabilityconstraint_rendering_displays_type)
  - [Feature: constraint\_scripts\_directory](#feature-constraint_scripts_directory)
    - [constraint\_scripts\_directory.constraint\_scripts\_directory\_exists](#constraint_scripts_directoryconstraint_scripts_directory_exists)
    - [constraint\_scripts\_directory.constraint\_scripts\_documented](#constraint_scripts_directoryconstraint_scripts_documented)
    - [constraint\_scripts\_directory.constraint\_scripts\_readme\_exists](#constraint_scripts_directoryconstraint_scripts_readme_exists)
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
  - [Feature: remove\_scope\_from\_constraint\_bash](#feature-remove_scope_from_constraint_bash)
    - [remove\_scope\_from\_constraint\_bash.constraint\_all\_model\_tests\_pass](#remove_scope_from_constraint_bashconstraint_all_model_tests_pass)
    - [remove\_scope\_from\_constraint\_bash.constraint\_no\_scope\_field\_usage](#remove_scope_from_constraint_bashconstraint_no_scope_field_usage)
    - [remove\_scope\_from\_constraint\_bash.constraint\_no\_scope\_in\_constraint\_bash](#remove_scope_from_constraint_bashconstraint_no_scope_in_constraint_bash)
    - [remove\_scope\_from\_constraint\_bash.constraint\_scope\_field\_removed\_from\_definition](#remove_scope_from_constraint_bashconstraint_scope_field_removed_from_definition)
  - [Feature: render\_spec\_features\_in\_task](#feature-render_spec_features_in_task)
    - [render\_spec\_features\_in\_task.constraint\_constraint\_details\_in\_markdown](#render_spec_features_in_taskconstraint_constraint_details_in_markdown)
    - [render\_spec\_features\_in\_task.constraint\_feature\_section\_in\_markdown](#render_spec_features_in_taskconstraint_feature_section_in_markdown)
    - [render\_spec\_features\_in\_task.constraint\_rendering\_implementation\_review](#render_spec_features_in_taskconstraint_rendering_implementation_review)
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
    - [task\_features\_checker\_tool.constraint\_tool\_implementation\_review](#task_features_checker_toolconstraint_tool_implementation_review)
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
    - [task\_toc\_rendering\_and\_links.constraint\_toc\_implementation\_review](#task_toc_rendering_and_linksconstraint_toc_implementation_review)
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

## Constraint Results

<a id="add-constraint-validation-requirement-skill"></a>
### Feature: add_constraint_validation_requirement_skill

**Bash Constraints:**

<a id="add-constraint-validation-requirement-skill-constraint-requirement-section-exists"></a>
#### add_constraint_validation_requirement_skill.constraint_requirement_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.133353
**Output:** `Requirement section found
`

<a id="add-constraint-validation-requirement-skill-constraint-results-interpretation-guide"></a>
#### add_constraint_validation_requirement_skill.constraint_results_interpretation_guide
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.136003
**Output:** `Interpretation guide exists
`

<a id="add-constraint-validation-requirement-skill-constraint-when-to-run-documented"></a>
#### add_constraint_validation_requirement_skill.constraint_when_to_run_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.134554
**Output:** `When section documented
`


<a id="constraint-checker-exit-code-hook"></a>
### Feature: constraint_checker_exit_code_hook

**Bash Constraints:**

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-calls-checker"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_calls_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.177419
**Output:** `Calls checker
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-checks-exit-code"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_checks_exit_code
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.178722
**Output:** `Checks exit code
`

<a id="constraint-checker-exit-code-hook-constraint-handler-stop-prints-decision-block"></a>
#### constraint_checker_exit_code_hook.constraint_handler_stop_prints_decision_block
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.179998
**Output:** `Prints decision block
`

<a id="constraint-checker-exit-code-hook-constraint-task-checker-exits-2-on-failure"></a>
#### constraint_checker_exit_code_hook.constraint_task_checker_exits_2_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.176126
**Output:** `Exit code 2 implemented
`


<a id="constraint-rendering-capability"></a>
### Feature: constraint_rendering_capability

**Bash Constraints:**

<a id="constraint-rendering-capability-constraint-bash-render-method"></a>
#### constraint_rendering_capability.constraint_bash_render_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.120905
**Output:** `✓ ConstraintBash.render() exists
`

<a id="constraint-rendering-capability-constraint-bash-render-toc-method"></a>
#### constraint_rendering_capability.constraint_bash_render_toc_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.123763
**Output:** `✓ ConstraintBash.render_toc() exists
`

<a id="constraint-rendering-capability-constraint-feature-uses-render-toc"></a>
#### constraint_rendering_capability.constraint_feature_uses_render_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.126528
**Output:** `✓ Feature uses constraint.render_toc()
`


<a id="constraint-rendering-capability-constraint-rendering-displays-type"></a>
#### constraint_rendering_capability.constraint_rendering_displays_type
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.127891


<a id="constraint-scripts-directory"></a>
### Feature: constraint_scripts_directory

**Bash Constraints:**

<a id="constraint-scripts-directory-constraint-scripts-directory-exists"></a>
#### constraint_scripts_directory.constraint_scripts_directory_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.116918
**Output:** `✓ constraints_scripts/ directory exists
`

<a id="constraint-scripts-directory-constraint-scripts-documented"></a>
#### constraint_scripts_directory.constraint_scripts_documented
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.118879
**Output:** `✓ Documentation found
`

<a id="constraint-scripts-directory-constraint-scripts-readme-exists"></a>
#### constraint_scripts_directory.constraint_scripts_readme_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.117546
**Output:** `✓ README.md exists
`


<a id="enhance-constraint-bash-result-output"></a>
### Feature: enhance_constraint_bash_result_output

**Bash Constraints:**

<a id="enhance-constraint-bash-result-output-constraint-output-populated-on-failure"></a>
#### enhance_constraint_bash_result_output.constraint_output_populated_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.130642
**Output:** `Not captured
`

<a id="enhance-constraint-bash-result-output-constraint-output-rendered-in-markdown"></a>
#### enhance_constraint_bash_result_output.constraint_output_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.131938
**Output:** `Output rendered
`

<a id="enhance-constraint-bash-result-output-constraint-shrunken-output-field-exists"></a>
#### enhance_constraint_bash_result_output.constraint_shrunken_output_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.129337
**Output:** `Field missing or optional
`


<a id="feature-goals-field"></a>
### Feature: feature_goals_field

**Bash Constraints:**

<a id="feature-goals-field-constraint-goals-field-exists"></a>
#### feature_goals_field.constraint_goals_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.728054
**Output:** `✓ Goals field exists
`

<a id="feature-goals-field-constraint-goals-field-in-task"></a>
#### feature_goals_field.constraint_goals_field_in_task
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.732141
**Output:** `✓ Goals in task.k.json
`

<a id="feature-goals-field-constraint-goals-in-toc"></a>
#### feature_goals_field.constraint_goals_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.730738
**Output:** `✓ Goals in TOC found
`

<a id="feature-goals-field-constraint-goals-rendered-in-markdown"></a>
#### feature_goals_field.constraint_goals_rendered_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.729343
**Output:** `✓ Goals rendering found
`


<a id="features-stats-diff-tracking"></a>
### Feature: features_stats_diff_tracking

**Bash Constraints:**

<a id="features-stats-diff-tracking-constraint-diff-rendered-in-iteration"></a>
#### features_stats_diff_tracking.constraint_diff_rendered_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.185509
**Output:** `Not implemented
`

<a id="features-stats-diff-tracking-constraint-features-stats-diff-model-exists"></a>
#### features_stats_diff_tracking.constraint_features_stats_diff_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.181288
**Output:** `Model exists
`

<a id="features-stats-diff-tracking-constraint-features-stats-has-diff-method"></a>
#### features_stats_diff_tracking.constraint_features_stats_has_diff_method
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.182740
**Output:** `diff() method exists
`

<a id="features-stats-diff-tracking-constraint-iteration-has-diff-field"></a>
#### features_stats_diff_tracking.constraint_iteration_has_diff_field
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.184047
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


<a id="migrate-metadata-to-model"></a>
### Feature: migrate_metadata_to_model

**Bash Constraints:**

<a id="migrate-metadata-to-model-constraint-constraint-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_constraint_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.192361

<a id="migrate-metadata-to-model-constraint-doc-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_doc_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.195119

<a id="migrate-metadata-to-model-constraint-feature-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_feature_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.194478

<a id="migrate-metadata-to-model-constraint-metadata-import"></a>
#### migrate_metadata_to_model.constraint_metadata_import
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.195747

<a id="migrate-metadata-to-model-constraint-no-dict-metadata-references"></a>
#### migrate_metadata_to_model.constraint_no_dict_metadata_references
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.197256

<a id="migrate-metadata-to-model-constraint-spec-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_spec_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.193706

<a id="migrate-metadata-to-model-constraint-task-model-uses-metadata"></a>
#### migrate_metadata_to_model.constraint_task_model_uses_metadata
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.193081


<a id="remove-scope-from-constraint-bash"></a>
### Feature: remove_scope_from_constraint_bash

**Bash Constraints:**

<a id="remove-scope-from-constraint-bash-constraint-all-model-tests-pass"></a>
#### remove_scope_from_constraint_bash.constraint_all_model_tests_pass
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.204696
**Output:** `Tests exist
`

<a id="remove-scope-from-constraint-bash-constraint-no-scope-field-usage"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_field_usage
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.204083

<a id="remove-scope-from-constraint-bash-constraint-no-scope-in-constraint-bash"></a>
#### remove_scope_from_constraint_bash.constraint_no_scope_in_constraint_bash
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.202707

<a id="remove-scope-from-constraint-bash-constraint-scope-field-removed-from-definition"></a>
#### remove_scope_from_constraint_bash.constraint_scope_field_removed_from_definition
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.201247


<a id="render-spec-features-in-task"></a>
### Feature: render_spec_features_in_task

**Bash Constraints:**

<a id="render-spec-features-in-task-constraint-constraint-details-in-markdown"></a>
#### render_spec_features_in_task.constraint_constraint_details_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.714467
**Output:** `✓ Constraint details found
`

<a id="render-spec-features-in-task-constraint-feature-section-in-markdown"></a>
#### render_spec_features_in_task.constraint_feature_section_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.713077
**Output:** `✓ Features section found in markdown
`

**Prompt Constraints:**

<a id="render-spec-features-in-task-constraint-rendering-implementation-review"></a>
#### render_spec_features_in_task.constraint_rendering_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-16T19:20:20.714479


<a id="task-add-iteration-script"></a>
### Feature: task_add_iteration_script

**Bash Constraints:**

<a id="task-add-iteration-script-constraint-script-exists"></a>
#### task_add_iteration_script.constraint_script_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.186253
**Output:** `Script exists
`

<a id="task-add-iteration-script-constraint-script-populates-features-stats"></a>
#### task_add_iteration_script.constraint_script_populates_features_stats
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.190252
**Output:** `Populates stats
`

<a id="task-add-iteration-script-constraint-script-runs-checker"></a>
#### task_add_iteration_script.constraint_script_runs_checker
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.188875
**Output:** `Runs checker
`

<a id="task-add-iteration-script-constraint-script-uses-knowledge-tool"></a>
#### task_add_iteration_script.constraint_script_uses_knowledge_tool
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.187601
**Output:** `Uses knowledge tool
`

<a id="task-add-iteration-script-constraint-skill-documentation-updated"></a>
#### task_add_iteration_script.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.191621
**Output:** `Documented
`


<a id="task-default-render-toc"></a>
### Feature: task_default_render_toc

**Bash Constraints:**

<a id="task-default-render-toc-constraint-default-toc-when-opts-missing"></a>
#### task_default_render_toc.constraint_default_toc_when_opts_missing
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.733640
**Output:** `✓ Default opts handling found
`

<a id="task-default-render-toc-constraint-explicit-false-respected"></a>
#### task_default_render_toc.constraint_explicit_false_respected
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.736444
**Output:** `✓ Explicit False handling found
`

<a id="task-default-render-toc-constraint-render-toc-default-true"></a>
#### task_default_render_toc.constraint_render_toc_default_true
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.735102
**Output:** `✓ Default render_toc=True found
`

<a id="task-default-render-toc-constraint-toc-rendered-by-default"></a>
#### task_default_render_toc.constraint_toc_rendered_by_default
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.910789
**Output:** `✓ TOC rendered
`


<a id="task-features-checker-selective-patch"></a>
### Feature: task_features_checker_selective_patch

**Bash Constraints:**

<a id="task-features-checker-selective-patch-constraint-feature-results-filtering"></a>
#### task_features_checker_selective_patch.constraint_feature_results_filtering
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.199849

<a id="task-features-checker-selective-patch-constraint-patch-uses-add-op"></a>
#### task_features_checker_selective_patch.constraint_patch_uses_add_op
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.199168

<a id="task-features-checker-selective-patch-constraint-preserves-other-features"></a>
#### task_features_checker_selective_patch.constraint_preserves_other_features
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.198547

<a id="task-features-checker-selective-patch-constraint-selective-patch-logic"></a>
#### task_features_checker_selective_patch.constraint_selective_patch_logic
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.197881


<a id="task-features-checker-tool"></a>
### Feature: task_features_checker_tool

**Bash Constraints:**

<a id="task-features-checker-tool-constraint-project-root-substitution"></a>
#### task_features_checker_tool.constraint_project_root_substitution
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.725302
**Output:** `✓ PROJECT_ROOT substitution found
`

<a id="task-features-checker-tool-constraint-recursive-execution-prevention"></a>
#### task_features_checker_tool.constraint_recursive_execution_prevention
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.724023
**Output:** `✓ Recursive execution prevention found
`

<a id="task-features-checker-tool-constraint-tool-accepts-features-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_features_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.717995
**Output:** `--features arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-output-checks-path-arg"></a>
#### task_features_checker_tool.constraint_tool_accepts_output_checks_path_arg
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.719302
**Output:** `--output-checks-path arg missing
`

<a id="task-features-checker-tool-constraint-tool-accepts-task-path"></a>
#### task_features_checker_tool.constraint_tool_accepts_task_path
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.716657
**Output:** `Task path argument missing
`

<a id="task-features-checker-tool-constraint-tool-exists"></a>
#### task_features_checker_tool.constraint_tool_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.715231
**Output:** `✓ tool exists
`

<a id="task-features-checker-tool-constraint-tool-output-checks-path-writable"></a>
#### task_features_checker_tool.constraint_tool_output_checks_path_writable
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.726701
**Output:** `Output path handling implemented
`

<a id="task-features-checker-tool-constraint-tool-returns-checks-results"></a>
#### task_features_checker_tool.constraint_tool_returns_checks_results
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.720642
**Output:** `ChecksResults usage found
`

<a id="task-features-checker-tool-constraint-tool-saves-results-to-file"></a>
#### task_features_checker_tool.constraint_tool_saves_results_to_file
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.722700
**Output:** `File save logic implemented
`

**Prompt Constraints:**

<a id="task-features-checker-tool-constraint-tool-implementation-review"></a>
#### task_features_checker_tool.constraint_tool_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-16T19:20:20.722712


<a id="task-toc-includes-constraints"></a>
### Feature: task_toc_includes_constraints

**Bash Constraints:**

<a id="task-toc-includes-constraints-constraint-constraints-nested-in-toc"></a>
#### task_toc_includes_constraints.constraint_constraints_nested_in_toc
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.085359
**Output:** `✗ No constraints in TOC
`

<a id="task-toc-includes-constraints-constraint-constraints-visible-in-markdown"></a>
#### task_toc_includes_constraints.constraint_constraints_visible_in_markdown
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.086957
**Output:** `✓ Constraints visible in markdown
`

<a id="task-toc-includes-constraints-constraint-toc-includes-constraints"></a>
#### task_toc_includes_constraints.constraint_toc_includes_constraints
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:20.912425
**Output:** `✗ Missing
`


<a id="task-toc-rendering-and-links"></a>
### Feature: task_toc_rendering_and_links

**Bash Constraints:**

<a id="task-toc-rendering-and-links-constraint-anchor-sections-exist"></a>
#### task_toc_rendering_and_links.constraint_anchor_sections_exist
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.114482
**Output:** `✓ All 117 TOC links have matching anchors
`

<a id="task-toc-rendering-and-links-constraint-toc-has-entries"></a>
#### task_toc_rendering_and_links.constraint_toc_has_entries
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.089741
**Output:** `✓ TOC entries found
`

<a id="task-toc-rendering-and-links-constraint-toc-indentation"></a>
#### task_toc_rendering_and_links.constraint_toc_indentation
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.116235
**Output:** `✓ Proper nesting found
`

<a id="task-toc-rendering-and-links-constraint-toc-links-format"></a>
#### task_toc_rendering_and_links.constraint_toc_links_format
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.091249
**Output:** `✓ Links formatted correctly
`

<a id="task-toc-rendering-and-links-constraint-toc-section-exists"></a>
#### task_toc_rendering_and_links.constraint_toc_section_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.088260
**Output:** `✓ TOC section found
`

**Prompt Constraints:**

<a id="task-toc-rendering-and-links-constraint-toc-implementation-review"></a>
#### task_toc_rendering_and_links.constraint_toc_implementation_review
**Verdict:** (empty)
**Timestamp:** 2026-03-16T19:20:21.116250


<a id="two-phase-constraint-validation"></a>
### Feature: two_phase_constraint_validation

**Bash Constraints:**

<a id="two-phase-constraint-validation-constraint-cmd-protection-verified"></a>
#### two_phase_constraint_validation.constraint_cmd_protection_verified
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.625300
**Output:** `Traceback (most recent call last):
  File "<string>", line 4, in <module>
ImportError: cannot import name '_protect_cmd_updates' from 'patch_knowledge_document' (/project/knowledge_tool/knowledge_tool/patch_knowledge_document.py)
✗ Cmd protection test failed
`

<a id="two-phase-constraint-validation-constraint-cmd-protection-when-proven"></a>
#### two_phase_constraint_validation.constraint_cmd_protection_when_proven
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.211907
**Output:** `✗ cmd protection missing
`

<a id="two-phase-constraint-validation-constraint-cmd-update-warning"></a>
#### two_phase_constraint_validation.constraint_cmd_update_warning
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.213365
**Output:** `✗ Warning message missing
`

<a id="two-phase-constraint-validation-constraint-external-proven-red-blocked"></a>
#### two_phase_constraint_validation.constraint_external_proven_red_blocked
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.210490
**Output:** `✗ proven_red not protected in patch_knowledge_document.py
`

<a id="two-phase-constraint-validation-constraint-only-proven-affects-result"></a>
#### two_phase_constraint_validation.constraint_only_proven_affects_result
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.215966
**Output:** `✓ Proven-only result logic exists
`

<a id="two-phase-constraint-validation-constraint-patch-protects-proven-red"></a>
#### two_phase_constraint_validation.constraint_patch_protects_proven_red
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.430722
**Output:** `Traceback (most recent call last):
  File "<string>", line 4, in <module>
ImportError: cannot import name '_restore_proven_red_values' from 'patch_knowledge_document' (/project/knowledge_tool/knowledge_tool/patch_knowledge_document.py)
✗ Protection test failed
`

<a id="two-phase-constraint-validation-constraint-print-proven-summary"></a>
#### two_phase_constraint_validation.constraint_print_proven_summary
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.217381
**Output:** `✓ Proven summary printed
`

<a id="two-phase-constraint-validation-constraint-proven-red-default-none"></a>
#### two_phase_constraint_validation.constraint_proven_red_default_none
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.209091
**Output:** `✗ Default not set correctly
`

<a id="two-phase-constraint-validation-constraint-proven-red-excluded"></a>
#### two_phase_constraint_validation.constraint_proven_red_excluded
**Verdict:** ✗ FAIL
**Timestamp:** 2026-03-16T19:20:21.207615
**Output:** `✗ proven_red has exclude=True - should be removed
`

<a id="two-phase-constraint-validation-constraint-proven-red-field-exists"></a>
#### two_phase_constraint_validation.constraint_proven_red_field_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.205905
**Output:** `✓ proven_red field exists
`

<a id="two-phase-constraint-validation-constraint-proven-red-in-task-json"></a>
#### two_phase_constraint_validation.constraint_proven_red_in_task_json
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.238435
**Output:** `ℹ No proven_red constraints yet (expected before first failure run)
`

<a id="two-phase-constraint-validation-constraint-set-proven-red-on-failure"></a>
#### two_phase_constraint_validation.constraint_set_proven_red_on_failure
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.214646
**Output:** `✓ _set_proven_red_in_task function exists
`

<a id="two-phase-constraint-validation-constraint-unprovided-constraints-logged-not-failed"></a>
#### two_phase_constraint_validation.constraint_unprovided_constraints_logged_not_failed
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.218697
**Output:** `✓ Unproven constraints are logged only
`


<a id="update-iteration-with-features-stats"></a>
### Feature: update_iteration_with_features_stats

**Bash Constraints:**

<a id="update-iteration-with-features-stats-constraint-feature-result-constraints-required"></a>
#### update_iteration_with_features_stats.constraint_feature_result_constraints_required
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.174856
**Output:** `Still optional
`

<a id="update-iteration-with-features-stats-constraint-features-stats-generated"></a>
#### update_iteration_with_features_stats.constraint_features_stats_generated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.140880
**Output:** `Generation implemented
`

<a id="update-iteration-with-features-stats-constraint-features-stats-in-iteration"></a>
#### update_iteration_with_features_stats.constraint_features_stats_in_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.139309
**Output:** `Field in Iteration
`

<a id="update-iteration-with-features-stats-constraint-features-stats-model-exists"></a>
#### update_iteration_with_features_stats.constraint_features_stats_model_exists
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.137972
**Output:** `FeaturesStats with proper fields
`

<a id="update-iteration-with-features-stats-constraint-features-stats-rendered"></a>
#### update_iteration_with_features_stats.constraint_features_stats_rendered
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.142544
**Output:** `Rendering implemented
`

<a id="update-iteration-with-features-stats-constraint-skill-documentation-updated"></a>
#### update_iteration_with_features_stats.constraint_skill_documentation_updated
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.144082
**Output:** `Skill docs updated
`

<a id="update-iteration-with-features-stats-constraint-stats-displayed-on-iteration"></a>
#### update_iteration_with_features_stats.constraint_stats_displayed_on_iteration
**Verdict:** ✓ PASS
**Timestamp:** 2026-03-16T19:20:21.173215
**Output:** `Stats in iteration
`
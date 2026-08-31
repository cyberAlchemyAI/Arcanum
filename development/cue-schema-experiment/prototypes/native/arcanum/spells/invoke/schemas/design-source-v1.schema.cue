// Invoke Design Source v1
//
// Sole authored W2 architecture authority. Every W1 obligation is applied
// exactly once, facts are typed once, and six views contain ID projections
// only.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-source/v1")
	close({
		$schema!:         "https://arcanum.dev/schemas/invoke/design-source/v1"
		activation_kind!: "normal"
		applications!: [...matchN(4, [matchIf({
			disposition!: "preserved" | "satisfied"
		}, {
			decision_ref?: null
			fact_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}, matchIf({
			disposition!: "changed-by-exact-decision"
		}, {
			decision_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			fact_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}, matchIf({
			disposition!: "not-applicable-with-evidence"
		}, {
			decision_ref?: null
			evidence_refs?: null | bool | number | string | [_, ...] | {}
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			disposition!: "block"
		}, {
			decision_ref?: null
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}]) & close({
			decision_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			disposition!: "preserved" | "satisfied" | "changed-by-exact-decision" | "not-applicable-with-evidence" | "block"
			evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			rationale!:    =~".*\\S.*"
			subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
		})] & [_, ...]
		authority_effect!: "none"
		design_kind!: matchN(1, [close({
			determination_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			kind!: "greenfield"
		}), close({
			deltas!: [...close({
				change!: "added" | "preserved" | "modified" | "removed"
				current_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				decision_ref!: matchN(1, [close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				}), null])
				delta_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				prior_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				rationale!: =~".*\\S.*"
			})] & [_, ...]
			kind!: "evolution"
			predecessor_artifact_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			predecessor_stage_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})])
		dispatch_trace!: close({
			evidence_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			techniques!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		})
		distill_contract!: close({
			classification!:          "required"
			coherent_unit_candidate!: =~".*\\S.*"
			expected_receipt!:        "DISTILL-RECEIPT.json"
			split_pressure_question!: =~".*\\S.*"
			validator_owner!:         "distill"
		})
		facts!: [...matchN(22, [matchIf({
			fact_kind!: "actor"
		}, {
			attributes?: close({
				acts!:                bool
				assistive_operation!: bool
				decides!:             bool
				natural_person!:      bool
				navigates!:           bool
				reads!:               bool
				recovers!:            bool
				surfaces!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			})
		}, _) & {}, matchIf({
			fact_kind!: "system"
		}, {
			attributes?: close({
				responsibility!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "relationship"
		}, {
			attributes?: close({
				from_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				relationship_kind!: =~".*\\S.*"
				to_id!:             =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})
		}, _) & {}, matchIf({
			fact_kind!: "component"
		}, {
			attributes?: close({
				contract_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				level!: "high-level" | "low-level"
				parent_component_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				responsibility!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "rendered-surface"
		}, {
			attributes?: close({
				modality!:              =~".*\\S.*"
				semantic_change!:       "none" | "new" | "changed"
				semantic_contract_ref!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "contract"
		}, {
			attributes?: close({
				contract_kind!:    =~".*\\S.*"
				failure_boundary!: =~".*\\S.*"
				preservation!:     "preserved" | "new" | "changed"
				statement!:        =~".*\\S.*"
				versioning!:       =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "interface"
		}, {
			attributes?: close({
				contract_ref!: =~".*\\S.*"
				direction!:    "inbound" | "outbound" | "bidirectional"
				kind!:         =~".*\\S.*"
				peer!:         =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "workflow-step"
		}, {
			attributes?: close({
				action!:                =~".*\\S.*"
				actor_or_component_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				next_step_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			})
		}, _) & {}, matchIf({
			fact_kind!: "state"
		}, {
			attributes?: close({
				allowed_next_state_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				subject_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})
		}, _) & {}, matchIf({
			fact_kind!: "decision"
		}, {
			attributes?: close({
				decision!: =~".*\\S.*"
				outcomes!: [...close({
					condition!: =~".*\\S.*"
					next_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
					result!: =~".*\\S.*"
				})] & [_, ...]
				question!:  =~".*\\S.*"
				rationale!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "dependency"
		}, {
			attributes?: close({
				consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				dependency_kind!: =~".*\\S.*"
				failure_policy!:  =~".*\\S.*"
				target_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})
		}, _) & {}, matchIf({
			fact_kind!: "store"
		}, {
			attributes?: close({
				authority!: =~".*\\S.*"
				data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
				writers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			})
		}, _) & {}, matchIf({
			fact_kind!: "queue"
		}, {
			attributes?: close({
				consumers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
				ordering!: =~".*\\S.*"
				producers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			})
		}, _) & {}, matchIf({
			fact_kind!: "writer"
		}, {
			attributes?: close({
				concurrency!: =~".*\\S.*"
				targets!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			})
		}, _) & {}, matchIf({
			fact_kind!: "normative-rule"
		}, {
			attributes?: close({
				enforcement_hint!: =~".*\\S.*"
				object!:           =~".*\\S.*"
				subject!:          =~".*\\S.*"
				verb!:             =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "effect"
		}, {
			attributes?: close({
				external!:   bool
				privileged!: bool
				reversible!: bool
			})
		}, _) & {}, matchIf({
			fact_kind!: "data-log-sink"
		}, {
			attributes?: close({
				data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
				retention_hint!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "deployment"
		}, {
			attributes?: close({
				environment!:  =~".*\\S.*"
				release_mode!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "compatibility-boundary"
		}, {
			attributes?: close({
				new_contract!: =~".*\\S.*"
				old_contract!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "quality-claim"
		}, {
			attributes?: close({
				required!:              bool
				source_kind!:           =~".*\\S.*"
				threshold_or_tradeoff!: =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "acceptance-readiness-claim"
		}, {
			attributes?: close({
				evidence_state!: "authored-complete"
				selector!:       =~".*\\S.*"
			})
		}, _) & {}, matchIf({
			fact_kind!: "risk"
		}, {
			attributes?: close({
				mitigation!: =~".*\\S.*"
				risk!:       =~".*\\S.*"
			})
		}, _) & {}]) & close({
			attributes!: {}
			fact_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			fact_kind!: "actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"
			name!:      =~".*\\S.*"
			owner!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			requirement_refs!: [...close({
				subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
			})] & [_, ...]
		})] & [_, ...]
		glossary_application!: close({
			mappings!: [...close({
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
				term!: =~".*\\S.*"
			})]
			source_glossary_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			unmapped_terms!: list.UniqueItems() & [...=~".*\\S.*"]
		})
		layering!: matchN(1, [close({
			decision!:     =~".*\\S.*"
			kind!:         "seed"
			minimum_unit!: =~".*\\S.*"
		}), close({
			kind!:      "gap"
			rationale!: =~".*\\S.*"
		})])
		next_route!: "design-bundle-production"
		planned_witnesses!: [...close({
			claim_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			concern_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_state!:     "planned-contract"
			execution_owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			execution_phase!:    "plan" | "implementation" | "validation"
			expected_result!:    =~".*\\S.*"
			input_or_violation!: =~".*\\S.*"
			polarity!:           "positive" | "negative"
			target_fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			witness_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})]
		profile_binding!: close({
			profile_id!: "invoke.generic-design-baseline.v1"
			profile_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		schema_version!: "invoke.design-source.v1"
		selected_companions!: [...close({
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			output_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			requirement_refs!: [...close({
				subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
			})] & [_, ...]
		})]
		selected_outputs!: list.MatchN(>=1, "architecture") & list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		source_digest!: =~"^[a-f0-9]{64}$"
		source_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		target_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		template_selection!: close({
			evidence_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			selected_profile_id!: "invoke.generic-design-baseline.v1"
		})
		transport_policy!: close({
			append_existing_only!: true
			targets!:              list.MaxItems(0)
			upstream_mutation!:    false
		})
		unresolved_gaps!: [...close({
			effect!:       =~".*\\S.*"
			gap_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			repair_route!: =~".*\\S.*"
			severity!:     "flag" | "block"
		})]
		upstream_bindings!: close({
			denominator_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			design_input_closure_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			design_input_closure_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			design_input_production_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			scope_manifest_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			selection_result_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		views!: close({
			context!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:context"
			}])
			decision_flow!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:decision-flow"
			}])
			dependency_interface!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:dependency-interface"
			}])
			high_level_structure!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:high-level-structure"
			}])
			low_level_components!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:low-level-components"
			}])
			workflow_process!: matchN(2, [matchN(2, [matchIf({
				applicability!: "applicable"
			}, {
				fact_ids?: null | bool | number | string | [_, ...] | {}
				na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				applicability!: "not-applicable-with-evidence"
			}, {
				fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
				na_evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				applicability!: "applicable" | "not-applicable-with-evidence"
				fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				na_evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), {
				view_id?: "view:workflow-process"
			}])
		})
	})

	#acceptanceClaimAttributes: close({
		evidence_state!: "authored-complete"
		selector!:       =~".*\\S.*"
	})

	#actorAttributes: close({
		acts!:                bool
		assistive_operation!: bool
		decides!:             bool
		natural_person!:      bool
		navigates!:           bool
		reads!:               bool
		recovers!:            bool
		surfaces!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
	})

	#application: matchN(4, [matchIf({
		disposition!: "preserved" | "satisfied"
	}, {
		decision_ref?: null
		fact_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		disposition!: "changed-by-exact-decision"
	}, {
		decision_ref?: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		fact_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		disposition!: "not-applicable-with-evidence"
	}, {
		decision_ref?: null
		evidence_refs?: null | bool | number | string | [_, ...] | {}
		fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		disposition!: "block"
	}, {
		decision_ref?: null
		fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		decision_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		disposition!: "preserved" | "satisfied" | "changed-by-exact-decision" | "not-applicable-with-evidence" | "block"
		evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		rationale!:    =~".*\\S.*"
		subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
	})

	#companion: close({
		fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		output_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		requirement_refs!: [...close({
			subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
		})] & [_, ...]
	})

	#compatibilityAttributes: close({
		new_contract!: =~".*\\S.*"
		old_contract!: =~".*\\S.*"
	})

	#componentAttributes: close({
		contract_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		level!: "high-level" | "low-level"
		parent_component_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		responsibility!: =~".*\\S.*"
	})

	#contractAttributes: close({
		contract_kind!:    =~".*\\S.*"
		failure_boundary!: =~".*\\S.*"
		preservation!:     "preserved" | "new" | "changed"
		statement!:        =~".*\\S.*"
		versioning!:       =~".*\\S.*"
	})

	#decisionAttributes: close({
		decision!: =~".*\\S.*"
		outcomes!: [...close({
			condition!: =~".*\\S.*"
			next_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
			result!: =~".*\\S.*"
		})] & [_, ...]
		question!:  =~".*\\S.*"
		rationale!: =~".*\\S.*"
	})

	#delta: close({
		change!: "added" | "preserved" | "modified" | "removed"
		current_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		decision_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		delta_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		prior_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		rationale!: =~".*\\S.*"
	})

	#dependencyAttributes: close({
		consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		dependency_kind!: =~".*\\S.*"
		failure_policy!:  =~".*\\S.*"
		target_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#deploymentAttributes: close({
		environment!:  =~".*\\S.*"
		release_mode!: =~".*\\S.*"
	})

	#designKind: matchN(1, [close({
		determination_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		kind!: "greenfield"
	}), close({
		deltas!: [...close({
			change!: "added" | "preserved" | "modified" | "removed"
			current_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
			decision_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			delta_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			prior_fact_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
			rationale!: =~".*\\S.*"
		})] & [_, ...]
		kind!: "evolution"
		predecessor_artifact_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		predecessor_stage_receipt_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
	})])

	#digest: =~"^[a-f0-9]{64}$"

	#effectAttributes: close({
		external!:   bool
		privileged!: bool
		reversible!: bool
	})

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#fact: matchN(22, [matchIf({
		fact_kind!: "actor"
	}, {
		attributes?: close({
			acts!:                bool
			assistive_operation!: bool
			decides!:             bool
			natural_person!:      bool
			navigates!:           bool
			reads!:               bool
			recovers!:            bool
			surfaces!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		})
	}, _) & {}, matchIf({
		fact_kind!: "system"
	}, {
		attributes?: close({
			responsibility!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "relationship"
	}, {
		attributes?: close({
			from_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			relationship_kind!: =~".*\\S.*"
			to_id!:             =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})
	}, _) & {}, matchIf({
		fact_kind!: "component"
	}, {
		attributes?: close({
			contract_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			level!: "high-level" | "low-level"
			parent_component_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
			responsibility!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "rendered-surface"
	}, {
		attributes?: close({
			modality!:              =~".*\\S.*"
			semantic_change!:       "none" | "new" | "changed"
			semantic_contract_ref!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "contract"
	}, {
		attributes?: close({
			contract_kind!:    =~".*\\S.*"
			failure_boundary!: =~".*\\S.*"
			preservation!:     "preserved" | "new" | "changed"
			statement!:        =~".*\\S.*"
			versioning!:       =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "interface"
	}, {
		attributes?: close({
			contract_ref!: =~".*\\S.*"
			direction!:    "inbound" | "outbound" | "bidirectional"
			kind!:         =~".*\\S.*"
			peer!:         =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "workflow-step"
	}, {
		attributes?: close({
			action!:                =~".*\\S.*"
			actor_or_component_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			next_step_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		})
	}, _) & {}, matchIf({
		fact_kind!: "state"
	}, {
		attributes?: close({
			allowed_next_state_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			subject_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})
	}, _) & {}, matchIf({
		fact_kind!: "decision"
	}, {
		attributes?: close({
			decision!: =~".*\\S.*"
			outcomes!: [...close({
				condition!: =~".*\\S.*"
				next_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				result!: =~".*\\S.*"
			})] & [_, ...]
			question!:  =~".*\\S.*"
			rationale!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "dependency"
	}, {
		attributes?: close({
			consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			dependency_kind!: =~".*\\S.*"
			failure_policy!:  =~".*\\S.*"
			target_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})
	}, _) & {}, matchIf({
		fact_kind!: "store"
	}, {
		attributes?: close({
			authority!: =~".*\\S.*"
			data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			writers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		})
	}, _) & {}, matchIf({
		fact_kind!: "queue"
	}, {
		attributes?: close({
			consumers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			ordering!: =~".*\\S.*"
			producers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		})
	}, _) & {}, matchIf({
		fact_kind!: "writer"
	}, {
		attributes?: close({
			concurrency!: =~".*\\S.*"
			targets!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		})
	}, _) & {}, matchIf({
		fact_kind!: "normative-rule"
	}, {
		attributes?: close({
			enforcement_hint!: =~".*\\S.*"
			object!:           =~".*\\S.*"
			subject!:          =~".*\\S.*"
			verb!:             =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "effect"
	}, {
		attributes?: close({
			external!:   bool
			privileged!: bool
			reversible!: bool
		})
	}, _) & {}, matchIf({
		fact_kind!: "data-log-sink"
	}, {
		attributes?: close({
			data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			retention_hint!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "deployment"
	}, {
		attributes?: close({
			environment!:  =~".*\\S.*"
			release_mode!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "compatibility-boundary"
	}, {
		attributes?: close({
			new_contract!: =~".*\\S.*"
			old_contract!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "quality-claim"
	}, {
		attributes?: close({
			required!:              bool
			source_kind!:           =~".*\\S.*"
			threshold_or_tradeoff!: =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "acceptance-readiness-claim"
	}, {
		attributes?: close({
			evidence_state!: "authored-complete"
			selector!:       =~".*\\S.*"
		})
	}, _) & {}, matchIf({
		fact_kind!: "risk"
	}, {
		attributes?: close({
			mitigation!: =~".*\\S.*"
			risk!:       =~".*\\S.*"
		})
	}, _) & {}]) & close({
		attributes!: {}
		fact_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		fact_kind!: "actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"
		name!:      =~".*\\S.*"
		owner!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		requirement_refs!: [...close({
			subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
		})] & [_, ...]
	})

	#factKind: "actor" | "system" | "relationship" | "component" | "rendered-surface" | "contract" | "interface" | "workflow-step" | "state" | "decision" | "dependency" | "store" | "queue" | "writer" | "normative-rule" | "effect" | "data-log-sink" | "deployment" | "compatibility-boundary" | "quality-claim" | "acceptance-readiness-claim" | "risk"

	#gap: close({
		effect!:       =~".*\\S.*"
		gap_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		severity!:     "flag" | "block"
	})

	#glossaryApplication: close({
		mappings!: [...close({
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			term!: =~".*\\S.*"
		})]
		source_glossary_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		unmapped_terms!: list.UniqueItems() & [...=~".*\\S.*"]
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#idSet: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]

	#interfaceAttributes: close({
		contract_ref!: =~".*\\S.*"
		direction!:    "inbound" | "outbound" | "bidirectional"
		kind!:         =~".*\\S.*"
		peer!:         =~".*\\S.*"
	})

	#nonEmpty: =~".*\\S.*"

	#normativeRuleAttributes: close({
		enforcement_hint!: =~".*\\S.*"
		object!:           =~".*\\S.*"
		subject!:          =~".*\\S.*"
		verb!:             =~".*\\S.*"
	})

	#optionalIdSet: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	#plannedWitness: close({
		claim_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		concern_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_state!:     "planned-contract"
		execution_owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		execution_phase!:    "plan" | "implementation" | "validation"
		expected_result!:    =~".*\\S.*"
		input_or_violation!: =~".*\\S.*"
		polarity!:           "positive" | "negative"
		target_fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		witness_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#qualityClaimAttributes: close({
		required!:              bool
		source_kind!:           =~".*\\S.*"
		threshold_or_tradeoff!: =~".*\\S.*"
	})

	#queueAttributes: close({
		consumers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		ordering!: =~".*\\S.*"
		producers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
	})

	#relationshipAttributes: close({
		from_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		relationship_kind!: =~".*\\S.*"
		to_id!:             =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#relativePath: string

	#renderedSurfaceAttributes: close({
		modality!:              =~".*\\S.*"
		semantic_change!:       "none" | "new" | "changed"
		semantic_contract_ref!: =~".*\\S.*"
	})

	#requirementRef: close({
		subject_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		subject_kind!: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"
	})

	#riskAttributes: close({
		mitigation!: =~".*\\S.*"
		risk!:       =~".*\\S.*"
	})

	#sinkAttributes: close({
		data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		retention_hint!: =~".*\\S.*"
	})

	#stateAttributes: close({
		allowed_next_state_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		subject_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#storeAttributes: close({
		authority!: =~".*\\S.*"
		data_classes!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
		writers!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
	})

	#stringSet: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]

	#subjectKind: "input" | "conditional-resolution" | "constraint" | "invariant" | "prior-decision" | "resolved-conflict" | "scope-signal" | "selection-concern" | "selected-output" | "planned-witness" | "design-kind" | "evolution-delta"

	#systemAttributes: close({
		responsibility!: =~".*\\S.*"
	})

	#viewProjection: matchN(2, [matchIf({
		applicability!: "applicable"
	}, {
		fact_ids?: null | bool | number | string | [_, ...] | {}
		na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		applicability!: "not-applicable-with-evidence"
	}, {
		fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
		na_evidence_refs?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		applicability!: "applicable" | "not-applicable-with-evidence"
		fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		na_evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#views: close({
		context!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:context"
		}])
		decision_flow!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:decision-flow"
		}])
		dependency_interface!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:dependency-interface"
		}])
		high_level_structure!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:high-level-structure"
		}])
		low_level_components!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:low-level-components"
		}])
		workflow_process!: matchN(2, [matchN(2, [matchIf({
			applicability!: "applicable"
		}, {
			fact_ids?: null | bool | number | string | [_, ...] | {}
			na_evidence_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			applicability!: "not-applicable-with-evidence"
		}, {
			fact_ids?: null | bool | number | string | list.MaxItems(0) | {}
			na_evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			applicability!: "applicable" | "not-applicable-with-evidence"
			fact_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			na_evidence_refs!: [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			view_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}), {
			view_id?: "view:workflow-process"
		}])
	})

	#workflowAttributes: close({
		action!:                =~".*\\S.*"
		actor_or_component_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		next_step_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
	})

	#writerAttributes: close({
		concurrency!: =~".*\\S.*"
		targets!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
	})
}

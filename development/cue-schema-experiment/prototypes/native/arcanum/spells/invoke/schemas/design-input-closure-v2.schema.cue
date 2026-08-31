// Invoke Design Input Closure v2
//
// Successor Design input source. Normal activation exact-binds a current Define
// v3 stage and its independent v1 admission; evolution also exact-binds a
// current Design v3 stage and v2 admission.
package prototype

import (
	"net"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-input-closure/v2")
	close({
		$schema!: "https://arcanum.dev/schemas/invoke/design-input-closure/v2"
		activation!: matchN(1, [close({
			approval_ref!: matchN(2, [close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			}), {
				expected_schema_id?:      "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1"
				expected_schema_version?: "invoke.design-input-boundary-approval.v1"
			}])
			define_admission_receipt_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			define_stage_receipt_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			kind!: "normal"
		}), close({
			approval_ref!: matchN(2, [close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			}), {
				expected_schema_id?:      "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1"
				expected_schema_version?: "invoke.design-input-boundary-approval.v1"
			}])
			kind!:      "discovery"
			rationale!: =~".*\\S.*"
		})])
		authored_by!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		authority_effect!: "none"
		closure_digest!:   =~"^[a-f0-9]{64}$"
		closure_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		conditional_input_resolutions!: [...close({
			evidence_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			outcome!:  "included" | "excluded"
			owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})]
		constraints!: [...close({
			class!:         "constraint" | "invariant"
			obligation_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			owner!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			source_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			statement!: =~".*\\S.*"
		})]
		design_kind!: matchN(1, [close({
			kind!: "greenfield"
			no_prior_design_determination_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
		}), close({
			current_state_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			declared_delta_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			kind!: "evolution"
			prior_design_admission_receipt_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			prior_design_artifact_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			prior_design_stage_receipt_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
		})])
		discovery_boundary!: close({
			boundary_digest!: =~"^[a-f0-9]{64}$"
			discovery_rules!: [...close({
				include_globs!: list.UniqueItems() & [...string] & [_, ...]
				input_class!: "define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"
				root_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})] & [_, ...]
			observation_epoch!: =~".*\\S.*"
			permitted_exclusions!: [...close({
				evidence_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				path!: string
			})]
			required_input_classes!: list.UniqueItems() & [..."define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"] & [_, ...]
			roots!: [...close({
				path!:    string
				root_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				sha256!:  =~"^[a-f0-9]{64}$"
				size!:    int & >=0
			})] & [_, ...]
		})
		exclusions!: [...close({
			evidence_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			exclusion_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:         string
			reason!:       =~".*\\S.*"
		})]
		input_catalog!: [...matchN(2, [matchIf({
			classification!: "excluded"
		}, {
			exclusion_evidence_ref?: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
		}, _) & {}, matchIf({
			classification!: "required" | "conditional"
		}, {
			exclusion_evidence_ref?: null
		}, _) & {}]) & close({
			applicability_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			applies_to!: list.UniqueItems() & [...=~".*\\S.*"] & [_, ...]
			authority_class!: "normative" | "owner-decision" | "observed-current-state" | "advisory" | "historical"
			authority_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			classification!:  "required" | "conditional" | "excluded"
			exclusion_evidence_ref!: matchN(1, [close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			}), null])
			freshness!: close({
				observed_epoch!: =~".*\\S.*"
				status!:         "current" | "historical"
			})
			input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			kind!:     "define-artifact" | "current-design" | "current-implementation" | "interface-contract" | "state-workflow" | "data-store" | "queue-writer" | "deployment-topology" | "authority-policy" | "security-policy" | "privacy-policy" | "compatibility-policy" | "quality-constraint" | "observability-contract" | "architecture-pattern" | "research-evidence" | "ux-evidence" | "owner-decision" | "other"
			selector!: string
			source_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
		})] & [_, ...]
		input_conflicts!: [...matchN(2, [matchIf({
			resolution_status!: "resolved"
		}, {
			decision_ref?: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
		}, _) & {}, matchIf({
			resolution_status!: "unresolved"
		}, {
			decision_ref?: null
		}, _) & {}]) & close({
			conflict_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			decision_ref!: matchN(1, [close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			}), null])
			input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			resolution_status!: "resolved" | "unresolved"
		})]
		invariants!: [...close({
			class!:         "constraint" | "invariant"
			obligation_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			owner!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			source_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			statement!: =~".*\\S.*"
		})]
		prior_decisions!: [...close({
			decision_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			decision_ref!: close({
				expected_schema_id!: matchN(1, [net.AbsURL, null])
				expected_schema_version!: matchN(1, [=~".*\\S.*", null])
				path!:       string
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			owner!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!: "preserved" | "eligible-for-supersession"
		})]
		schema_version!: "invoke.design-input-closure.v2"
		scope_manifest_contract_ref!: matchN(2, [close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		}), {
			expected_schema_id?:      "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0"
			expected_schema_version?: "1.0.0"
			path?:                    "arcanum/spells/invoke/schemas/design-scope-manifest.schema.json"
			visibility?:              "public"
		}])
		scope_signals!: close({
			acceptance_and_readiness_claims!: [...close({
				claim_id!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_state!:  "authored-complete"
				selector!:        =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			compatibility_boundaries!: [...close({
				boundary_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				new_contract!:    =~".*\\S.*"
				old_contract!:    =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			data_and_log_sinks!: [...close({
				data_classes!: list.UniqueItems() & [...=~".*\\S.*"]
				retention_hint!:  =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				sink_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			deployment_targets!: [...close({
				deployment_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				environment!:     =~".*\\S.*"
				release_mode!:    =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			effects!: [...close({
				effect_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				external!:        bool
				privileged!:      bool
				reversible!:      bool
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			human_actors!: [...close({
				actor_id!:            =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				acts!:                bool
				assistive_operation!: bool
				decides!:             bool
				natural_person!:      bool
				navigates!:           bool
				reads!:               bool
				recovers!:            bool
				signal_id!:           =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				surfaces!: list.UniqueItems() & [...=~".*\\S.*"]
			})]
			interfaces!: [...close({
				contract_ref!:    =~".*\\S.*"
				direction!:       "inbound" | "outbound" | "bidirectional"
				interface_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				kind!:            =~".*\\S.*"
				peer!:            =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			normative_rules!: [...close({
				enforcement_hint!: =~".*\\S.*"
				object!:           =~".*\\S.*"
				rule_id!:          =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				signal_id!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				subject!:          =~".*\\S.*"
				verb!:             =~".*\\S.*"
			})]
			quality_claims!: [...close({
				claim_id!:              =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				required!:              bool
				signal_id!:             =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_kind!:           =~".*\\S.*"
				threshold_or_tradeoff!: =~".*\\S.*"
			})]
			queues!: [...close({
				consumers!: list.UniqueItems() & [...=~".*\\S.*"]
				ordering!: =~".*\\S.*"
				producers!: list.UniqueItems() & [...=~".*\\S.*"]
				queue_id!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			rendered_surfaces!: [...close({
				modality!:              =~".*\\S.*"
				semantic_change!:       "none" | "new" | "changed"
				semantic_contract_ref!: =~".*\\S.*"
				signal_id!:             =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				surface_id!:            =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			stores!: [...close({
				authority!: =~".*\\S.*"
				data_classes!: list.UniqueItems() & [...=~".*\\S.*"]
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				store_id!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				writers!: list.UniqueItems() & [...=~".*\\S.*"]
			})]
			writers!: [...close({
				concurrency!:     =~".*\\S.*"
				signal_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				targets!: list.UniqueItems() & [...=~".*\\S.*"]
				writer_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
		})
		selection_inputs!: close({
			authored_concerns!: [...close({
				concern_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				disposition!: "required" | "recommended" | "not-applicable-with-rationale" | "block"
				evidence_selectors!: list.UniqueItems() & [...string]
				ownership!: close({
					accountable_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
					artifact_owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
					contributing_owners!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
					validator_owner!: "invoke-design-selection-validator"
				})
				primary_class!:      "authority" | "security" | "state-event" | "persistence" | "failure" | "reliability" | "integration" | "migration" | "rollout" | "privacy-data" | "performance" | "ux" | "validation"
				rationale!:          =~".*\\S.*"
				required_predicate!: bool
				revisit_condition!: matchN(1, [=~".*\\S.*", null])
				selected!: bool
			})]
			planned_witness_requirements!: [...close({
				claim_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				concern_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_state!: "planned-contract"
				witness_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			predicate_inputs!: [...close({
				concern_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				expected!:     bool
				predicate_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			})]
		})
		target!: close({
			id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			objective!:  =~".*\\S.*"
			owner!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			title!:      =~".*\\S.*"
			visibility!: "public" | "private"
		})
	})

	#activation: matchN(1, [close({
		approval_ref!: matchN(2, [close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		}), {
			expected_schema_id?:      "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1"
			expected_schema_version?: "invoke.design-input-boundary-approval.v1"
		}])
		define_admission_receipt_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
		define_stage_receipt_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
		kind!: "normal"
	}), close({
		approval_ref!: matchN(2, [close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		}), {
			expected_schema_id?:      "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1"
			expected_schema_version?: "invoke.design-input-boundary-approval.v1"
		}])
		kind!:      "discovery"
		rationale!: =~".*\\S.*"
	})])

	#designKind: matchN(1, [close({
		kind!: "greenfield"
		no_prior_design_determination_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
	}), close({
		current_state_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		declared_delta_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		kind!: "evolution"
		prior_design_admission_receipt_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
		prior_design_artifact_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
		prior_design_stage_receipt_ref!: close({
			expected_schema_id!: matchN(1, [net.AbsURL, null])
			expected_schema_version!: matchN(1, [=~".*\\S.*", null])
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
	})])

	#selectionInputs: close({
		authored_concerns!: [...close({
			concern_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			disposition!: "required" | "recommended" | "not-applicable-with-rationale" | "block"
			evidence_selectors!: list.UniqueItems() & [...string]
			ownership!: close({
				accountable_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				artifact_owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				contributing_owners!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
				validator_owner!: "invoke-design-selection-validator"
			})
			primary_class!:      "authority" | "security" | "state-event" | "persistence" | "failure" | "reliability" | "integration" | "migration" | "rollout" | "privacy-data" | "performance" | "ux" | "validation"
			rationale!:          =~".*\\S.*"
			required_predicate!: bool
			revisit_condition!: matchN(1, [=~".*\\S.*", null])
			selected!: bool
		})]
		planned_witness_requirements!: [...close({
			claim_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			concern_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_state!: "planned-contract"
			witness_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})]
		predicate_inputs!: [...close({
			concern_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			expected!:     bool
			predicate_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			source_input_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
		})]
	})

	#target: close({
		id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		objective!:  =~".*\\S.*"
		owner!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		title!:      =~".*\\S.*"
		visibility!: "public" | "private"
	})
}

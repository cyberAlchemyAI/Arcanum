// WorkPackReadinessAuditConfigV2
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/config/2-0-0")
	matchIf({
		admission_timing!: "selected-unit-at-task-session"
	}, {
		execution_bindings?: null | bool | number | string | [...matchN(2, [#executionBinding, null | bool | number | string | [...] | {
			task_id!:              _
			swu_id!:               _
			lifecycle_owner!:      _
			authority_class!:      _
			publication_class!:    _
			attempt_contract!:     _
			validation_contracts!: _
		}])] | {}
		runtime_binding?: null | bool | number | string | [...] | {
			task_session_admission_receipt_ref?: null
		}
		execution_policy!: _
	}, _) & {} & close({
		schema_version!:     "2.0.0"
		admission_timing?:   "full-frontier" | "selected-unit-at-task-session"
		execution_policy?:   #executionPolicy
		audit_id!:           strings.MinRunes( 1)
		repository_root!:    "."
		evidence_ceiling!:   "frozen-input-contractual-readiness"
		classifier_version!: strings.MinRunes( 1)
		objective_ref!:      #bindingRef
		closure_receipt_refs!: [_, ...] & [...#bindingRef]
		authority_bindings!: close({
			canonical_authority_refs!: [_, ...] & [...#bindingRef]
			semantic_bindings!: close({
				owner!:      #bindingRef
				material!:   #bindingRef
				validation!: #bindingRef
				receipt!:    #bindingRef
				closeout!:   #bindingRef
			})
		})
		execution_bindings!: [_, ...] & [...#executionBinding]
		execution_entry_closure?: close({
			closure_ref!:      #bindingRef
			units_ref!:        #bindingRef
			validator_ref!:    #opaqueExactArtifactBindingRef
			rehearsal_effect!: "deterministic-no-effect"
		})
		receipt_bindings!: close({
			terminal_schema_ref!:    #nullableBindingRef
			semantic_validator_ref!: #nullableSemanticValidatorBindingRef
			expected_receipt_refs!: [_, ...] & [...#bindingRef]
		})
		closeout_bindings!: [_, ...] & [...close({
			unit_id!:                    strings.MinRunes( 1)
			allowed_delta_policy_ref!:   #nullableBindingRef
			owner_receipt_contract_ref!: #nullableBindingRef
			compensation!:               #compensation
		})]
		task_session_closeout_contracts?: [_, ...] & [...#taskSessionCloseoutContract]
		runtime_binding!: close({
			requested_task_session_execution_mode!: strings.MinRunes(1)
			task_session_admission_receipt_ref!:    #nullableBindingRef
		})
		status_receipt_refs!:   #statusRefs
		lifecycle_status_refs!: #lifecycleRefs
		approval_policy!: close({
			approval_owner_ref!:        strings.MinRunes( 1)
			decision_gate_receipt_ref!: #bindingRef
			run_budget!: close({
				max_task_session_requests!: int & >=1
			})
			risk_policy_ref!: #bindingRef
			allowed_audit_verdicts!: list.UniqueItems() & [_, ...] & [..."pass" | "flag"]
			allowed_flag_classes!: list.UniqueItems() & [..."observability-residue"]
		})
		continuity_projection!: close({
			cursor!: strings.MinRunes( 1)
			completed_unit_receipt_refs!: [...#bindingRef]
			joined_closeout_receipt_refs!: [...matchN(1, [#bindingRef, #joinedOwnerCloseoutEvidence])]
			projected_next_successor!: close({
				unit_id!:                                      null | string
				canonical_successor_ref!:                      #nullableBindingRef
				projection_owner_ref!:                         strings.MinRunes( 1)
				equivalence_validator_ref!:                    #bindingRef
				continuation_router_verification_receipt_ref!: #nullableBindingRef
				authority_effect!:                             "none"
			})
		})
		expected_source_snapshot_digest?: null | =~"^[a-f0-9]{64}$"
		expected_material_digests?: [string]: =~"^[a-f0-9]{64}$"
		expected_semantic_digest?: null | =~"^[a-f0-9]{64}$"
	})

	#allowedRoute: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: "repository-local-reversible"
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#attemptContract: close({
		id_policy!:        strings.MinRunes( 1)
		collision_policy!: strings.MinRunes( 1)
		success_teardown!: strings.MinRunes( 1)
		failure_teardown!: strings.MinRunes( 1)
	})

	#bindingRef: close({
		binding_id!:   strings.MinRunes( 1)
		owner_ref!:    strings.MinRunes( 1)
		artifact_ref!: #exactArtifactRef
		selector!:     string
	})

	#byteBaseline: close({
		path!:   strings.MinRunes( 1)
		sha256!: =~"^[a-f0-9]{64}$"
	})

	#command: close({
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		cwd!:        strings.MinRunes( 1)
		risk_class!: "read-only" | "bounded-write" | "browser" | "network"
	})

	#compensation: matchN(1, [close({
		mode!:      "none"
		rationale!: strings.MinRunes( 1)
	}), close({
		mode!:         "owner-routed"
		owner_ref!:    strings.MinRunes( 1)
		contract_ref!: #bindingRef
	})])

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#executionBinding: close({
		task_id?:           strings.MinRunes( 1)
		swu_id?:            strings.MinRunes( 1)
		lifecycle_owner?:   strings.MinRunes( 1)
		authority_class?:   "public" | "private"
		publication_class?: "public" | "private" | "internal"
		attempt_contract?:  #attemptContract
		unit_id!:           strings.MinRunes( 1)
		dependencies!: list.UniqueItems() & [...strings.MinRunes( 1)]
		canonical_successors!: list.UniqueItems() & [...strings.MinRunes( 1)]
		producer_id!: strings.MinRunes( 1)
		command!:     #command
		target_dispositions!: [_, ...] & [...#targetDisposition]
		validation_contracts!: [_, ...] & [...#structuredValidationCommand]
		output_contracts!: [...#outputContract]
		material_writes!: list.UniqueItems() & [...strings.MinRunes( 1)]
		execution_outputs!: list.UniqueItems() & [...strings.MinRunes( 1)]
		allowed_writes!: list.UniqueItems() & [...strings.MinRunes( 1)]
		material_package!: #materialPackage
		byte_baselines!: [...#byteBaseline]
	})

	#executionPolicy: close({
		work_pack_id!: strings.MinRunes( 1)
		route_policy!: "automatic-in-scope"
		allowed_routes!: [_, ...] & [...#allowedRoute]
		allowed_routes_digest!: =~"^[a-f0-9]{64}$"
		automatic_decisions!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		stop_decisions!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		scope_source!:      "exact-work-pack-and-captured-frontier"
		validation_policy!: "owner-gates-remain-mandatory"
	})

	#joinedOwnerCloseoutEvidence: close({
		evidence_profile!:         "task-session-joined-owner-closeout-v1"
		binding_id!:               strings.MinRunes( 1)
		owner_ref!:                "task-session"
		terminal_receipt_ref!:     #exactArtifactRef
		joined_owner_receipt_ref!: #exactArtifactRef
		owner_receipt_schema_ref!: #bindingRef
		continuation_cursor_ref!:  #exactArtifactRef
	})

	#lifecycleRefs: close({
		plan_artifact_status!: #status
		audit_status!:         #status
		approval_status!:      #status
		chain_status!:         #status
	})

	#materialPackage: close({
		package_ref!:          #nullableBindingRef
		producer_owner_ref!:   null | strings.MinRunes( 1)
		producer_receipt_ref!: #nullableBindingRef
		schema_ref!:           #nullableBindingRef
		declared_sha256!:      null | =~"^[a-f0-9]{64}$"
		target_inventory_ref!: #nullableBindingRef
	})

	#nullableBindingRef: matchN(1, [#bindingRef, null])

	#nullableSemanticValidatorBindingRef: matchN(1, [#bindingRef, #opaqueExactArtifactBindingRef, null])

	#opaqueExactArtifactBindingRef: close({
		binding_id!:   strings.MinRunes( 1)
		owner_ref!:    strings.MinRunes( 1)
		binding_mode!: "opaque-exact-artifact"
		artifact_ref!: #exactArtifactRef
	})

	#outputContract: matchN(1, [{
		schema_ref!: #bindingRef
	}, {
		semantic_predicate!: string
	}]) & close({
		expected_path!:      strings.MinRunes( 1)
		disposition!:        "create" | "update" | "delete" | "transient"
		producer_id!:        strings.MinRunes( 1)
		schema_ref!:         #nullableBindingRef
		semantic_predicate!: null | strings.MinRunes( 1)
		failure_behavior!:   "block-before-successor"
		validation_phase!:   "post-produce" | "closeout"
	})

	#status: close({
		value!:       strings.MinRunes( 1)
		owner_ref!:   strings.MinRunes( 1)
		receipt_ref!: #bindingRef
	})

	#statusRefs: close({
		artifact_authored_status!:      #status
		registry_released_status!:      #status
		mutation_runtime_ready_status!: #status
		audit_verdict!:                 #status
	})

	#structuredValidationCommand: close({
		command_id!: strings.MinRunes( 1)
		phase!:      "pre-execution" | "post-produce" | "closeout"
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		cwd!:              strings.MinRunes( 1)
		timeout_seconds!:  int & >=1 & <=86400
		max_output_bytes!: int & >=1 & <=16777216
	})

	#targetDisposition: close({
		path!:                strings.MinRunes( 1)
		disposition!:         "create" | "update" | "delete" | "read" | "transient"
		producer_id!:         null | strings.MinRunes( 1)
		parent_path!:         strings.MinRunes( 1)
		collision_policy!:    "fail-if-exists" | "replace-declared" | "not-applicable"
		baseline_obligation!: "none" | "required-at-admission"
	})

	#taskSessionCloseoutContract: close({
		unit_id!:                                strings.MinRunes( 1)
		receipt_profile!:                        "precloseout-execution-v1"
		precloseout_execution_schema_ref!:       #bindingRef
		expected_owner_receipt_schema_ref!:      #bindingRef
		declared_owner_receipt_schema_identity!: strings.MinRunes(1)
		final_terminal_schema_ref!:              #bindingRef
		continuity_schema_ref!:                  #bindingRef
		continuation_router_schema_ref!:         #bindingRef
	})
}

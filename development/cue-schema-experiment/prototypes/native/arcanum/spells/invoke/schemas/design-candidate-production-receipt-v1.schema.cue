// Invoke Design Candidate Production Receipt v1
//
// Failure-capable receipt for deterministic W2 candidate projection,
// independent coherence validation, and atomic candidate closure.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1")
	matchN(2, [matchIf({
		result!: "pass"
	}, {
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		coherence_block_receipt?: null
		evidence_ceiling?: null | bool | number | string | [...] | {
			candidate_projected?: true
			coherence_validated?: true
			normal_w1_bound?:     true
			source_complete?:     true
		}
		next_route?: "design-bundle-production"
		outputs?: null | bool | number | string | list.MaxItems(2) & [_, _, ...] | {}
		stage_results?: null | bool | number | string | [...null | bool | number | string | [...] | {
			status?: "pass"
		}] | {}
	}, _) & {}, matchIf({
		result!: "block"
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
		next_route?: "repair-w1-input" | "repair-installed-contract" | "repair-design-source"
		outputs?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1"
		authority_effect!: "none"
		bindings!: close({
			policy!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			process!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			profile!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		blockers!: [...close({
			blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			code!:         "SOURCE_SCHEMA_INVALID" | "SOURCE_DIGEST_MISMATCH" | "SOURCE_PATH_UNSAFE" | "W1_RECEIPT_INVALID" | "W1_RECEIPT_NOT_NORMAL" | "W1_OUTPUT_BINDING_MISMATCH" | "TARGET_BINDING_MISMATCH" | "PROFILE_INVALID" | "PROFILE_BINDING_MISMATCH" | "APPLICATION_DENOMINATOR_MISMATCH" | "APPLICATION_INVALID" | "FACT_REGISTRY_INVALID" | "VIEW_PROJECTION_INVALID" | "SELECTION_CLOSURE_INVALID" | "EVOLUTION_INVALID" | "GOVERNANCE_OVERCLAIM" | "ARTIFACT_PROJECTION_FAILED" | "ARTIFACT_PROJECTION_MISMATCH" | "COHERENCE_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"
			message!:      =~".*\\S.*"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			repair_route!: =~".*\\S.*"
			selector!: matchN(1, [=~".*\\S.*", null])
		})]
		coherence_block_receipt!: matchN(1, [_#defs."/properties/coherence_block_receipt/oneOf/0", null])
		evidence_ceiling!: close({
			acceptance!:           false
			candidate_projected!:  bool
			coherence_validated!:  bool
			deployment!:           false
			design_stage_pass!:    false
			execution!:            false
			external_effect!:      false
			human_views_produced!: false
			normal_w1_bound!:      bool
			plan_evidence!:        false
			publication!:          false
			source_complete!:      bool
		})
		next_route!: "design-bundle-production" | "repair-w1-input" | "repair-installed-contract" | "repair-design-source"
		outputs!: list.MaxItems(2) & [matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "design-artifact"
			path?: "DESIGN.json"
		}]), matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "coherence-receipt"
			path?: "DESIGN-COHERENCE-RECEIPT.json"
		}])]
		producer!: close({
			identity!: "invoke.compile-design-candidate.v1"
			owner!:    "invoke-design-candidate-producer"
			path!:     "arcanum/spells/invoke/scripts/compile_design_candidate.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		result!:         "pass" | "block"
		schema_version!: "invoke.design-candidate-production-receipt.v1"
		source_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		stage_results!: list.MaxItems(4) & list.UniqueItems() & [matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			stage_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			stage_id?: "source-validation"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			stage_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			stage_id?: "artifact-projection"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			stage_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			stage_id?: "coherence-validation"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			stage_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			stage_id?: "candidate-output-closure"
		}])] & [_, _, _, _, ...]
		w1_production_receipt_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
	})

	#blocker: close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         "SOURCE_SCHEMA_INVALID" | "SOURCE_DIGEST_MISMATCH" | "SOURCE_PATH_UNSAFE" | "W1_RECEIPT_INVALID" | "W1_RECEIPT_NOT_NORMAL" | "W1_OUTPUT_BINDING_MISMATCH" | "TARGET_BINDING_MISMATCH" | "PROFILE_INVALID" | "PROFILE_BINDING_MISMATCH" | "APPLICATION_DENOMINATOR_MISMATCH" | "APPLICATION_INVALID" | "FACT_REGISTRY_INVALID" | "VIEW_PROJECTION_INVALID" | "SELECTION_CLOSURE_INVALID" | "EVOLUTION_INVALID" | "GOVERNANCE_OVERCLAIM" | "ARTIFACT_PROJECTION_FAILED" | "ARTIFACT_PROJECTION_MISMATCH" | "COHERENCE_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	#diagnosticCode: "SOURCE_SCHEMA_INVALID" | "SOURCE_DIGEST_MISMATCH" | "SOURCE_PATH_UNSAFE" | "W1_RECEIPT_INVALID" | "W1_RECEIPT_NOT_NORMAL" | "W1_OUTPUT_BINDING_MISMATCH" | "TARGET_BINDING_MISMATCH" | "PROFILE_INVALID" | "PROFILE_BINDING_MISMATCH" | "APPLICATION_DENOMINATOR_MISMATCH" | "APPLICATION_INVALID" | "FACT_REGISTRY_INVALID" | "VIEW_PROJECTION_INVALID" | "SELECTION_CLOSURE_INVALID" | "EVOLUTION_INVALID" | "GOVERNANCE_OVERCLAIM" | "ARTIFACT_PROJECTION_FAILED" | "ARTIFACT_PROJECTION_MISMATCH" | "COHERENCE_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"

	#digest: =~"^[a-f0-9]{64}$"

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#nonEmpty: =~".*\\S.*"

	#outputRef: close({
		kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#relativePath: string

	#stageResult: matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		stage_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		status!:   "pass" | "block" | "not_evaluable"
	})

	// Invoke Design Coherence Receipt v1
	//
	// Independent semantic-coherence verdict bound to the exact staged Design
	// artifact and its installed process and policy.
	_#defs: "/properties/coherence_block_receipt/oneOf/0": {
		@jsonschema(id="https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1")
		matchN(3, [matchIf({
			verdict!: "pass"
		}, {
			coherence_state?:    "pass"
			design_stage_state?: "pending-bundle-closure"
			diagnostics?: null | bool | number | string | list.MaxItems(0) | {}
			evaluated_rules?: null | bool | number | string | [...null | bool | number | string | [...] | {
				status?: "pass"
			}] | {}
		}, _) & {}, matchIf({
			verdict!: "flag"
		}, {
			coherence_state?:    "flag"
			design_stage_state?: "ineligible"
			diagnostics?: null | bool | number | string | [_, ...] | {}
		}, _) & {}, matchIf({
			verdict!: "block"
		}, {
			coherence_state?:    "block"
			design_stage_state?: "ineligible"
			diagnostics?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			$schema!:          "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1"
			authority_effect!: "none"
			bindings!: close({
				coherence_policy_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				denominator_receipt_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				design_artifact_ref!: close({
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
				design_source_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				process_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				profile_ref!: close({
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
			coherence_state!:    "pass" | "flag" | "block"
			design_stage_state!: "pending-bundle-closure" | "ineligible"
			diagnostics!: [...close({
				causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				code!:          =~"^[A-Z][A-Z0-9_]{2,127}$"
				diagnostic_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				message!:       =~".*\\S.*"
				owner!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				repair!: =~".*\\S.*"
				selector!: matchN(1, [=~".*\\S.*", null])
			})]
			evaluated_rules!: list.UniqueItems() & [...matchN(2, [matchIf({
				status!: "pass"
			}, {
				causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
				evidence_refs?: null | bool | number | string | [_, ...] | {}
			}, _) & {}, matchIf({
				status!: "flag" | "block" | "not_evaluable"
			}, {
				causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				rule_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				status!:  "pass" | "flag" | "block" | "not_evaluable"
			})] & [_, ...]
			plan_evidence_state!: "plan-evidence-pending"
			policy_rule_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"] & [_, ...]
			policy_rule_set_digest!:   =~"^[a-f0-9]{64}$"
			receipt_digest!:           =~"^[a-f0-9]{64}$"
			receipt_id!:               =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			schema_version!:           "invoke.design-coherence-receipt.v1"
			selection_evidence_state!: "design-validator-pass"
			validator!: close({
				identity!: "invoke.validate-design-coherence.v1"
				owner!:    "invoke-design-coherence-validator"
				path!:     "arcanum/spells/invoke/scripts/validate_design_coherence.py"
				sha256!:   =~"^[a-f0-9]{64}$"
			})
			verdict!: "pass" | "flag" | "block"
		})
	}

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/diagnostic": close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		code!:          =~"^[A-Z][A-Z0-9_]{2,127}$"
		diagnostic_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		message!:       =~".*\\S.*"
		owner!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		repair!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/digest": =~"^[a-f0-9]{64}$"

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/exactRef": close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/id": =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/nonEmpty": =~".*\\S.*"

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/optionalIdSet": list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/relativePath": string

	_#defs: "/properties/coherence_block_receipt/oneOf/0/$defs/ruleResult": matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		evidence_refs?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		status!: "flag" | "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		rule_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		status!:  "pass" | "flag" | "block" | "not_evaluable"
	})
}

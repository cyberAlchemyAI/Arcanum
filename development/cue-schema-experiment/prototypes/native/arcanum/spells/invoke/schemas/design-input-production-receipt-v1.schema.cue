// Invoke Design Input Production Receipt v1
//
// Failure-capable receipt for the atomic W1 closure, manifest, denominator, and
// fixed-point selection bundle.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1")
	matchN(4, [matchIf({
		result!: "pass"
	}, {
		activation_kind?: "normal" | "discovery"
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		evidence_ceiling?: null | bool | number | string | [...] | {
			boundary_relative_input_closure?: true
			denominator_compatibility?:       true
			manifest_projection?:             true
			selection_fixed_point?:           true
		}
		input_closure_receipt?: null | bool | number | string | [...] | {
			verdict?: "pass"
		}
		outputs?: null | bool | number | string | list.MaxItems(4) & [_, _, _, _, ...] | {}
		stage_results?: null | bool | number | string | [...null | bool | number | string | [...] | {
			status?: "pass"
		}] | {}
	}, _) & {}, matchIf({
		result!: "block"
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
		next_route?: "repair-input"
		outputs?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		activation_kind!: "normal"
		result!:          "pass"
	}, {
		next_route?: "design-authoring"
	}, _) & {}, matchIf({
		activation_kind!: "discovery"
		result!:          "pass"
	}, {
		next_route?: "input-review"
	}, _) & {}]) & close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1"
		activation_kind!:  "normal" | "discovery" | "invalid"
		authority_effect!: "none"
		blockers!: [...close({
			blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			code!:         "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH" | "DENOMINATOR_BLOCKED" | "PREDICATE_ASSERTION_MISMATCH" | "SELECTION_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"
			message!:      =~".*\\S.*"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			repair_route!: =~".*\\S.*"
			selector!: matchN(1, [=~".*\\S.*", null])
		})]
		evidence_ceiling!: close({
			acceptance!:                      false
			artifact_authored!:               false
			boundary_relative_input_closure!: bool
			denominator_compatibility!:       bool
			deployment!:                      false
			execution!:                       false
			external_effect!:                 false
			manifest_projection!:             bool
			plan_evidence!:                   false
			publication!:                     false
			selection_fixed_point!:           bool
		})

		// Invoke Design Input Closure Receipt v1
		//
		// Independent, failure-capable evidence for approved-boundary-relative
		// discovery, exact input closure, and the one legal DesignScopeManifest
		// projection.
		input_closure_receipt!: _#defs."/properties/input_closure_receipt"
		next_route!:            "design-authoring" | "input-review" | "repair-input"
		outputs!: list.MaxItems(4) & list.UniqueItems() & [matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "input-closure-receipt"
			path?: "DESIGN-INPUT-CLOSURE-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "scope-manifest"
			path?: "DESIGN-SCOPE-MANIFEST.json"
		}]), matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "denominator-receipt"
			path?: "DESIGN-DENOMINATOR-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "selection-result"
			path?: "DESIGN-SELECTION-RESULT.json"
		}])]
		producer!: close({
			identity!: "invoke.compile-design-input-bundle.v1"
			owner!:    "invoke-design-input-producer"
			path!:     "arcanum/spells/invoke/scripts/compile_design_input_bundle.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		result!:         "pass" | "block"
		schema_version!: "invoke.design-input-production-receipt.v1"
		source_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		stage_results!: list.MaxItems(4) & [matchN(2, [matchN(2, [matchIf({
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
			stage_id?: "input-closure-validation"
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
			stage_id?: "scope-projection"
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
			stage_id?: "denominator-extraction"
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
			stage_id?: "selection"
		}])] & [_, _, _, _, ...]
	})

	#blocker: close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH" | "DENOMINATOR_BLOCKED" | "PREDICATE_ASSERTION_MISMATCH" | "SELECTION_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	#diagnosticCode: "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH" | "DENOMINATOR_BLOCKED" | "PREDICATE_ASSERTION_MISMATCH" | "SELECTION_BLOCKED" | "LATE_VALIDATION_FAILED" | "OUTPUT_INVENTORY_MISMATCH"

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

	// Invoke Design Input Closure Receipt v1
	//
	// Independent, failure-capable evidence for approved-boundary-relative
	// discovery, exact input closure, and the one legal DesignScopeManifest
	// projection.
	_#defs: "/properties/input_closure_receipt": {
		@jsonschema(id="https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1")
		matchN(2, [matchIf({
			verdict!: "pass"
		}, {
			activation_kind?: "normal" | "discovery"
			bindings?: null | bool | number | string | [...] | {
				boundary_approval_ref?: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
			}
			blockers?: null | bool | number | string | list.MaxItems(0) | {}
			checks?: null | bool | number | string | [...null | bool | number | string | [...] | {
				status?: "pass"
			}] | {}
			discovery?: null | bool | number | string | [...] | {
				ambiguous_paths?: null | bool | number | string | list.MaxItems(0) | {}
				unclassified_paths?: null | bool | number | string | list.MaxItems(0) | {}
			}
			expected_manifest?: {}
			prior_design_determination?: null | bool | number | string | [...] | {
				status?: "pass"
			}
		}, _) & {}, matchIf({
			verdict!: "block"
		}, {
			blockers?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			$schema!:          "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1"
			activation_kind!:  "normal" | "discovery" | "invalid"
			authority_effect!: "none"
			bindings!: close({
				boundary_approval_ref!: matchN(1, [close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				}), null])
				closure_digest!: =~"^[a-f0-9]{64}$"
				design_input_closure_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				discovery_boundary_digest!: =~"^[a-f0-9]{64}$"
				process_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
			})
			blockers!: [...close({
				blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				code!:         "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH"
				message!:      =~".*\\S.*"
				owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				repair_route!: =~".*\\S.*"
				selector!: matchN(1, [=~".*\\S.*", null])
			})]
			checks!: list.MaxItems(15) & [matchN(2, [matchN(2, [matchIf({
				status!: "pass"
			}, {
				causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			}, _) & {}, matchIf({
				status!: "block" | "not_evaluable"
			}, {
				causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
			}, _) & {}]) & close({
				causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "closure-schema"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "closure-digest"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "process-binding"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "boundary-approval"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "path-safety"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "boundary-freshness"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "discovery-enumeration"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "catalog-closure"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "input-freshness"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "visibility"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "conditional-resolution"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "conflict-closure"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "prior-design"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "scope-signal-coverage"
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
				check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				status!: "pass" | "block" | "not_evaluable"
			}), {
				check_id?: "manifest-projection"
			}])] & [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ...]
			conditional_resolutions!: [...close({
				evidence_ref!: close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})
				input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				outcome!:  "included" | "excluded"
				owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			})]
			discovery!: close({
				ambiguous_paths!: list.UniqueItems() & [...string]
				cataloged_paths!: list.UniqueItems() & [...string]
				excluded_paths!: list.UniqueItems() & [...string]
				inventory!: [...close({
					input_class!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
					path!:        string
					rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
					sha256!:      =~"^[a-f0-9]{64}$"
					size!:        int & >=0
				})]
				inventory_digest!: =~"^[a-f0-9]{64}$"
				per_class!: [...close({
					candidate_count!: int & >=0
					excluded_count!:  int & >=0
					included_count!:  int & >=0
					input_class!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
					status!:          "pass" | "block"
				})]
				unclassified_paths!: list.UniqueItems() & [...string]
			})
			expected_manifest!: matchN(1, [close({
				input_digest!: =~"^[a-f0-9]{64}$"
				manifest_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}), null])
			inspected_boundary!: close({
				required_input_classes!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
				root_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				rule_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			})
			prior_design_determination!: close({
				candidate_paths!: list.UniqueItems() & [...string]
				evidence_refs!: [...close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				})]
				kind!:   "greenfield" | "evolution" | "invalid"
				status!: "pass" | "block" | "not_evaluable"
			})
			receipt_digest!: =~"^[a-f0-9]{64}$"
			receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			schema_version!: "invoke.design-input-closure-receipt.v1"
			validator!: close({
				identity!: "invoke.validate-design-input-closure.v1"
				owner!:    "invoke-design-input-closure-validator"
				path!:     "arcanum/spells/invoke/scripts/validate_design_input_closure.py"
				sha256!:   =~"^[a-f0-9]{64}$"
			})
			verdict!: "pass" | "block"
		})
	}

	_#defs: "/properties/input_closure_receipt/$defs/blocker": close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	_#defs: "/properties/input_closure_receipt/$defs/checkResult": matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	})

	_#defs: "/properties/input_closure_receipt/$defs/classResult": close({
		candidate_count!: int & >=0
		excluded_count!:  int & >=0
		included_count!:  int & >=0
		input_class!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		status!:          "pass" | "block"
	})

	_#defs: "/properties/input_closure_receipt/$defs/conditionalResult": close({
		evidence_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		outcome!:  "included" | "excluded"
		owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	_#defs: "/properties/input_closure_receipt/$defs/diagnosticCode": "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH"

	_#defs: "/properties/input_closure_receipt/$defs/digest": =~"^[a-f0-9]{64}$"

	_#defs: "/properties/input_closure_receipt/$defs/discoveredCandidate": close({
		input_class!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		path!:        string
		rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		sha256!:      =~"^[a-f0-9]{64}$"
		size!:        int & >=0
	})

	_#defs: "/properties/input_closure_receipt/$defs/exactRef": close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	_#defs: "/properties/input_closure_receipt/$defs/id": =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	_#defs: "/properties/input_closure_receipt/$defs/nonEmpty": =~".*\\S.*"

	_#defs: "/properties/input_closure_receipt/$defs/optionalIdSet": list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	_#defs: "/properties/input_closure_receipt/$defs/pathSet": list.UniqueItems() & [...string]

	_#defs: "/properties/input_closure_receipt/$defs/priorDesignResult": close({
		candidate_paths!: list.UniqueItems() & [...string]
		evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		kind!:   "greenfield" | "evolution" | "invalid"
		status!: "pass" | "block" | "not_evaluable"
	})

	_#defs: "/properties/input_closure_receipt/$defs/relativePath": string
}

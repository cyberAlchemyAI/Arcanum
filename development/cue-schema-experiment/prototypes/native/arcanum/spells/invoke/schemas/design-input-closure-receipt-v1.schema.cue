// Invoke Design Input Closure Receipt v1
//
// Independent, failure-capable evidence for approved-boundary-relative
// discovery, exact input closure, and the one legal DesignScopeManifest
// projection.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
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

	#blocker: close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	#checkResult: matchN(2, [matchIf({
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

	#classResult: close({
		candidate_count!: int & >=0
		excluded_count!:  int & >=0
		included_count!:  int & >=0
		input_class!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		status!:          "pass" | "block"
	})

	#conditionalResult: close({
		evidence_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		input_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		outcome!:  "included" | "excluded"
		owner!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#diagnosticCode: "CLOSURE_SCHEMA_INVALID" | "CLOSURE_DIGEST_MISMATCH" | "PROCESS_REF_STALE" | "ACTIVATION_RECEIPT_INVALID" | "BOUNDARY_APPROVAL_INVALID" | "BOUNDARY_APPROVAL_MISMATCH" | "BOUNDARY_REF_ESCAPE" | "BOUNDARY_REF_MISSING" | "BOUNDARY_REF_STALE" | "SYMLINK_UNSUPPORTED" | "DISCOVERY_RULE_EMPTY" | "DISCOVERY_INPUT_UNDECLARED" | "DISCOVERY_INPUT_AMBIGUOUS" | "CATALOG_INPUT_OUTSIDE_BOUNDARY" | "REQUIRED_INPUT_CLASS_MISSING" | "INPUT_DUPLICATE" | "INPUT_REF_STALE" | "INPUT_SCHEMA_ID_MISMATCH" | "INPUT_SCHEMA_VERSION_MISMATCH" | "INPUT_VISIBILITY_LEAK" | "INPUT_AUTHORITY_UNRESOLVED" | "CONDITIONAL_INPUT_UNRESOLVED" | "EXCLUSION_UNJUSTIFIED" | "CONFLICT_UNRESOLVED" | "PRIOR_DESIGN_MISSING" | "PRIOR_DESIGN_AMBIGUOUS" | "PRIOR_DESIGN_RECEIPT_INVALID" | "GREENFIELD_CONTRADICTED" | "SCOPE_SIGNAL_INVALID" | "MANIFEST_PROJECTION_MISMATCH"

	#digest: =~"^[a-f0-9]{64}$"

	#discoveredCandidate: close({
		input_class!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		path!:        string
		rule_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		sha256!:      =~"^[a-f0-9]{64}$"
		size!:        int & >=0
	})

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#nonEmpty: =~".*\\S.*"

	#optionalIdSet: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	#pathSet: list.UniqueItems() & [...string]

	#priorDesignResult: close({
		candidate_paths!: list.UniqueItems() & [...string]
		evidence_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		kind!:   "greenfield" | "evolution" | "invalid"
		status!: "pass" | "block" | "not_evaluable"
	})

	#relativePath: string
}

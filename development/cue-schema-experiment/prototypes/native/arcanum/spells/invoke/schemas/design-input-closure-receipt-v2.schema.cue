// Invoke Design Input Closure Receipt v2
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v2")
	matchN(4, [matchIf({
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
		design_kind?: "greenfield" | "evolution"
	}, _) & {}, matchIf({
		verdict!: "block"
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		activation_kind!: "normal"
		verdict!:         "pass"
	}, {
		bindings?: null | bool | number | string | [...] | {
			define_admission_receipt_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			define_stage_receipt_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		}
	}, _) & {}, matchIf({
		design_kind!: "evolution"
		verdict!:     "pass"
	}, {
		bindings?: null | bool | number | string | [...] | {
			prior_design_admission_receipt_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			prior_design_stage_receipt_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		}
	}, _) & {}]) & close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v2"
		activation_kind!:  "normal" | "discovery" | "invalid"
		authority_effect!: "none"
		bindings!: close({
			boundary_approval_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			closure_digest!: =~"^[a-f0-9]{64}$"
			define_admission_receipt_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			define_stage_receipt_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			design_input_closure_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			discovery_boundary_digest!: =~"^[a-f0-9]{64}$"
			prior_design_admission_receipt_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			prior_design_stage_receipt_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			process_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		blockers!: [...close({
			blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			code!:         =~"^[A-Z][A-Z0-9_]{2,127}$"
			message!:      =~".*\\S.*"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			repair_route!: =~".*\\S.*"
			selector!: matchN(1, [=~".*\\S.*", null])
		})]
		checks!: list.MaxItems(17) & [matchN(2, [matchN(2, [matchIf({
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
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
			check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ...]
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
		design_kind!: "greenfield" | "evolution" | "invalid"
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
		schema_version!: "invoke.design-input-closure-receipt.v2"
		validator!: close({
			identity!: "invoke.validate-design-input-closure.v2"
			owner!:    "invoke-design-input-closure-validator"
			path!:     "arcanum/spells/invoke/scripts/validate_design_input_closure_v2.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		verdict!: "pass" | "block"
	})

	#blocker: close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         =~"^[A-Z][A-Z0-9_]{2,127}$"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	#check: matchN(2, [matchN(2, [matchIf({
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
		check_id?: "closure-schema" | "closure-digest" | "process-binding" | "boundary-approval" | "define-predecessor-admission" | "path-safety" | "boundary-freshness" | "discovery-enumeration" | "catalog-closure" | "input-freshness" | "visibility" | "conditional-resolution" | "conflict-closure" | "prior-design" | "design-predecessor-admission" | "scope-signal-coverage" | "manifest-projection"
	}])

	#discovery: close({
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

	#inspectedBoundary: close({
		required_input_classes!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		root_refs!: [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		rule_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
	})
}

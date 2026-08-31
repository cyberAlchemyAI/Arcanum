// Invoke Design Coherence Receipt v1
//
// Independent semantic-coherence verdict bound to the exact staged Design
// artifact and its installed process and policy.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
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

	#diagnostic: close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		code!:          =~"^[A-Z][A-Z0-9_]{2,127}$"
		diagnostic_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		message!:       =~".*\\S.*"
		owner!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		repair!: =~".*\\S.*"
		selector!: matchN(1, [=~".*\\S.*", null])
	})

	#digest: =~"^[a-f0-9]{64}$"

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#nonEmpty: =~".*\\S.*"

	#optionalIdSet: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	#relativePath: string

	#ruleResult: matchN(2, [matchIf({
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

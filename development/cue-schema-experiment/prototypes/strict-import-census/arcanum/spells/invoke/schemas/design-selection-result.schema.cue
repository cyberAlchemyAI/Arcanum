// InvokeDesignSelectionResult
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-selection-result/1-0-0")
	matchN(2, [matchIf({
		verdict!: "pass"
	}, {
		fixed_point?:    true
		evidence_state?: "design-validator-pass"
		diagnostics?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		verdict!: "block"
	}, {
		fixed_point?:    false
		evidence_state?: "authored-complete"
		diagnostics?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		schema_version!:             "1.0.0"
		manifest_id!:                #id
		manifest_input_digest!:      #digest
		denominator_receipt_digest!: #digest
		concerns!: [...#concern]
		selected_outputs!: list.UniqueItems() & [...#id]
		pass_1_digest!:  #digest
		pass_2_digest!:  #digest
		fixed_point!:    bool
		evidence_state!: "authored-complete" | "design-validator-pass"
		verdict!:        "pass" | "block"
		diagnostics!: [...#diagnostic]
		result_digest!: #digest
	})

	#concern: matchN(4, [matchIf({
		disposition!: "required"
	}, {
		selected?:  true
		output_id?: #id
		predicate_evidence?: null | bool | number | string | [...] | {
			required_predicate?: true
		}
	}, _) & {}, matchIf({
		disposition!: "recommended" | "not-applicable-with-rationale" | "block"
	}, {
		selected?: false
	}, _) & {}, matchIf({
		disposition!: "not-applicable-with-rationale"
	}, {
		predicate_evidence?: null | bool | number | string | [...] | {
			required_predicate?: false
			detector_negative?:  true
			evidence_selectors?: null | bool | number | string | [_, ...] | {}
		}
		output_id?: null
	}, _) & {}, matchIf({
		disposition!: "recommended"
	}, {
		revisit_condition?: strings.MinRunes( 1)
	}, _) & {}]) & close({
		concern_id!: #id
		signal_ids!: list.UniqueItems() & [_, ...] & [...#id]
		primary_class!:      "authority" | "security" | "state-event" | "persistence" | "failure" | "reliability" | "integration" | "migration" | "rollout" | "privacy-data" | "performance" | "ux" | "validation"
		ownership!:          #ownership
		disposition!:        "required" | "recommended" | "not-applicable-with-rationale" | "block"
		predicate_evidence!: #predicateEvidence
		output_id!: matchN(>=1, [#id, null])
		selected!:          bool
		rationale!:         strings.MinRunes( 1)
		revisit_condition!: null | strings.MinRunes( 1)
	})

	#diagnostic: close({
		code!:     "MANIFEST_NOT_CLOSED" | "MISSING_DETECTOR_INPUT" | "STALE_DENOMINATOR_RECEIPT" | "SELF_ISSUED_RECEIPT" | "UNBOUND_SIGNAL" | "OWNER_UNRESOLVED" | "FALSE_NA" | "ILLEGAL_SELECTION" | "CHANGED_PASS_TWO" | "ILLEGAL_EVIDENCE_STATE"
		message!:  strings.MinRunes( 1)
		selector!: null | string
		owner!:    null | string
		repair!:   strings.MinRunes( 1)
	})

	#digest: =~"^[a-f0-9]{64}$"

	#id: strings.MinRunes(1) & =~"^[a-zA-Z0-9][a-zA-Z0-9._:-]*$"

	#ownership: close({
		accountable_owner!: #id
		contributing_owners!: list.UniqueItems() & [...#id]
		artifact_owner!:  #id
		validator_owner!: "invoke-design-selection-validator"
	})

	#predicateEvidence: close({
		required_predicate!: bool
		detector_negative!:  bool
		evidence_selectors!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

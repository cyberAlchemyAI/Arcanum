// Invoke Design Coherence Policy v1
//
// Versioned rule catalog consumed by the independent Design coherence validator.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-coherence-policy/v1")
	close({
		$schema!:         "https://arcanum.dev/schemas/invoke/design-coherence-policy/v1"
		schema_version!:  "invoke.design-coherence-policy.v1"
		policy_id!:       #id
		validator_owner!: "invoke-design-coherence-validator"
		rules!: list.MaxItems(12) & [matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:w1-entry"
			diagnostic_code?: "DESIGN_W1_ENTRY_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:application-denominator"
			diagnostic_code?: "DESIGN_APPLICATION_DENOMINATOR_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:profile-closure"
			diagnostic_code?: "DESIGN_PROFILE_CLOSURE_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:registry-integrity"
			diagnostic_code?: "DESIGN_FACT_REGISTRY_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:view-projection"
			diagnostic_code?: "DESIGN_VIEW_PROJECTION_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:artifact-projection"
			diagnostic_code?: "DESIGN_ARTIFACT_PROJECTION_MISMATCH"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:contract-preservation"
			diagnostic_code?: "DESIGN_CONTRACT_PRESERVATION_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:selection-closure"
			diagnostic_code?: "DESIGN_SELECTION_CLOSURE_INVALID"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:glossary-consistency"
			diagnostic_code?: "DESIGN_GLOSSARY_CONFLICT"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:evolution-delta"
			diagnostic_code?: "DESIGN_EVOLUTION_DELTA_INCOMPLETE"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:plan-evidence-separation"
			diagnostic_code?: "DESIGN_PLAN_EVIDENCE_OVERCLAIM"
		}]), matchN(2, [#rule, null | bool | number | string | [...] | {
			rule_id?:         "rule:authority-ceiling"
			diagnostic_code?: "DESIGN_AUTHORITY_CEILING_EXCEEDED"
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, ...]
		rule_order!: ["rule:w1-entry", "rule:application-denominator", "rule:profile-closure", "rule:registry-integrity", "rule:view-projection", "rule:artifact-projection", "rule:contract-preservation", "rule:selection-closure", "rule:glossary-consistency", "rule:evolution-delta", "rule:plan-evidence-separation", "rule:authority-ceiling"]
		rule_set_digest!:  #digest
		pass_requires!:    "all-blocking-rules-pass"
		authority_effect!: "none"
		policy_digest!:    #digest
	})

	#digest: =~"^[a-f0-9]{64}$"

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#nonEmpty: =~".*\\S.*"

	#rule: close({
		rule_id!:         #id
		category!:        "input-coverage" | "w1-entry" | "application-denominator" | "profile-closure" | "registry-integrity" | "view-projection" | "artifact-projection" | "manifest-coverage" | "cross-view-identity" | "ownership" | "contract-preservation" | "selection-closure" | "glossary-consistency" | "evolution-delta" | "plan-evidence-separation" | "authority-ceiling" | "output-closure"
		severity!:        "block" | "flag"
		applies_to!:      #stringSet
		diagnostic_code!: =~"^[A-Z][A-Z0-9_]{2,127}$"
		description!:     #nonEmpty
		repair_route!:    #nonEmpty
	})

	#stringSet: list.UniqueItems() & [_, ...] & [...#nonEmpty]
}

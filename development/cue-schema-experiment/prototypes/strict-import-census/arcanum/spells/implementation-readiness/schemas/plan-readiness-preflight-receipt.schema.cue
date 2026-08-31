// PlanReadinessPreflightReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/plan-readiness-preflight-receipt/1-0-0")
	close({
		schema_version!:            "implementation-readiness.plan-readiness-preflight-receipt/v1"
		status!:                    "pass"
		code!:                      "PLAN_IMPLEMENTATION_READY"
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #digest
		frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		initial_unit!:          strings.MinRunes( 1)
		policy_digest!:         #digest
		allowed_routes_digest!: #digest
		audit_config_digest!:   #digest
		audit_report_digest!:   #digest
		route_coverage!: [_, ...] & [...close({
			unit_id!:  strings.MinRunes( 1)
			route_id!: strings.MinRunes( 1)
		})]
		validation_contract_digests!: [_, ...] & [...close({
			unit_id!: strings.MinRunes( 1)
			digest!:  #digest
		})]
		proof_invocation_id!: strings.MinRunes( 1)
		proof_created_at!:    strings.MinRunes( 1)
		fast_entry_proof!: close({
			request_digest!:    #digest
			receipt_digest!:    #digest
			binding_digest!:    #digest
			route_fingerprint!: #digest
			decision!:          "proceed"
			code!:              "TASK_READY"
			mutation_count!:    0
		})
		reusable_for_execution!: false
		mutation_ready!:         false
		authority_effect!:       "none"
		claim_ceiling!:          strings.MinRunes( 1)
	})

	#digest: =~"^[a-f0-9]{64}$"
}

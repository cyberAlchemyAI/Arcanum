// WorkPackReadinessAuditReport
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/report/1-0-0")
	close({
		schema_version!:           "1.0.0"
		audit_id!:                 strings.MinRunes( 1)
		canonical_spell_id!:       "work-pack-readiness-audit"
		verdict!:                  "pass" | "flag" | "block"
		plan_contract_status!:     "pass" | "flag" | "block"
		runtime_admission_status!: "pass" | "flag" | "block"
		receipt_semantics_status!: "pass" | "block"
		snapshot!: close({
			digest!:         =~"^[a-f0-9]{64}$"
			artifact_count!: int & >=1
			drift!:          bool
		})
		unit_counts!: [string]: int & >=0
		ready_frontier!: list.UniqueItems() & [...strings.MinRunes( 1)]
		selected_unit!: null
		findings!: [...#finding]
		unit_results!: [...close({
			unit_id!:           strings.MinRunes( 1)
			plan_contract!:     "pass" | "block"
			runtime_admission!: "pass" | "block"
			blocker_ids!: list.UniqueItems() & [...strings.MinRunes( 1)]
		})]
		authority_effect!: "none"
		mutation_ready!:   false
		next_owner!:       "invoke:refresh"
	})

	#finding: close({
		id!:       strings.MinRunes( 1)
		category!: "snapshot" | "graph" | "command" | "path" | "write-algebra" | "runtime-admission" | "dependency-receipt" | "receipt-semantics" | "attempt" | "closeout" | "handoff" | "authority"
		severity!: "blocker" | "flag"
		scope!:    strings.MinRunes( 1)
		claim!:    strings.MinRunes( 1)
		evidence!: [_, ...] & [...strings.MinRunes( 1)]
		target_paths!: [_, ...] & [...strings.MinRunes( 1)]
	})
}

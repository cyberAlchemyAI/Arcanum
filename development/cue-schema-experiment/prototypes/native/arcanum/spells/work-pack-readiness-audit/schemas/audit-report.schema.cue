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
		audit_id!:           strings.MinRunes(1)
		authority_effect!:   "none"
		canonical_spell_id!: "work-pack-readiness-audit"
		findings!: [...close({
			category!: "snapshot" | "graph" | "command" | "path" | "write-algebra" | "runtime-admission" | "dependency-receipt" | "receipt-semantics" | "attempt" | "closeout" | "handoff" | "authority"
			claim!:    strings.MinRunes(1)
			evidence!: [...strings.MinRunes(1)] & [_, ...]
			id!:       strings.MinRunes(1)
			scope!:    strings.MinRunes(1)
			severity!: "blocker" | "flag"
			target_paths!: [...strings.MinRunes(1)] & [_, ...]
		})]
		mutation_ready!:       false
		next_owner!:           "invoke:refresh"
		plan_contract_status!: "pass" | "flag" | "block"
		ready_frontier!: list.UniqueItems() & [...strings.MinRunes(1)]
		receipt_semantics_status!: "pass" | "block"
		runtime_admission_status!: "pass" | "flag" | "block"
		schema_version!:           "1.0.0"
		selected_unit!:            null
		snapshot!: close({
			artifact_count!: int & >=1
			digest!:         =~"^[a-f0-9]{64}$"
			drift!:          bool
		})
		unit_counts!: [string]: int & >=0
		unit_results!: [...close({
			blocker_ids!: list.UniqueItems() & [...strings.MinRunes(1)]
			plan_contract!:     "pass" | "block"
			runtime_admission!: "pass" | "block"
			unit_id!:           strings.MinRunes(1)
		})]
		verdict!: "pass" | "flag" | "block"
	})

	#finding: close({
		category!: "snapshot" | "graph" | "command" | "path" | "write-algebra" | "runtime-admission" | "dependency-receipt" | "receipt-semantics" | "attempt" | "closeout" | "handoff" | "authority"
		claim!:    strings.MinRunes(1)
		evidence!: [...strings.MinRunes(1)] & [_, ...]
		id!:       strings.MinRunes(1)
		scope!:    strings.MinRunes(1)
		severity!: "blocker" | "flag"
		target_paths!: [...strings.MinRunes(1)] & [_, ...]
	})
}

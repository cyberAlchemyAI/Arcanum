// WorkPackReadinessRefreshSignalPack
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/refresh-signal-pack/1-0-0")
	close({
		schema_version!: "1.0.0"
		audit_id!:       strings.MinRunes( 1)
		source_report!: close({
			path!:       "work-pack-readiness-report.json"
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=1
		})
		mutation_mode!:    "proposal-only"
		mutation_ready!:   false
		authority_effect!: "none"
		signals!: [...close({
			id!:          strings.MinRunes( 1)
			signal_type!: "evidence_added" | "blocker_opened" | "artifact_drift" | "no_op"
			claim!:       strings.MinRunes( 1)
			evidence!: [_, ...] & [...strings.MinRunes( 1)]
			target_artifacts!: [_, ...] & [...strings.MinRunes( 1)]
			confidence!:      "high" | "medium" | "low"
			mutation_safety!: "safe" | "needs_review" | "blocked"
		})]
		target_inventory!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		next_owner!: "invoke:refresh"
	})
}

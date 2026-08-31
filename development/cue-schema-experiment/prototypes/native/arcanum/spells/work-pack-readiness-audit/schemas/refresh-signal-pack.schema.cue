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
		audit_id!:         strings.MinRunes(1)
		authority_effect!: "none"
		mutation_mode!:    "proposal-only"
		mutation_ready!:   false
		next_owner!:       "invoke:refresh"
		schema_version!:   "1.0.0"
		signals!: [...close({
			claim!:      strings.MinRunes(1)
			confidence!: "high" | "medium" | "low"
			evidence!: [...strings.MinRunes(1)] & [_, ...]
			id!:              strings.MinRunes(1)
			mutation_safety!: "safe" | "needs_review" | "blocked"
			signal_type!:     "evidence_added" | "blocker_opened" | "artifact_drift" | "no_op"
			target_artifacts!: [...strings.MinRunes(1)] & [_, ...]
		})]
		source_report!: close({
			path!:       "work-pack-readiness-report.json"
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=1
		})
		target_inventory!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
	})
}

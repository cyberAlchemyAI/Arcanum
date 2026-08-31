// ExecutionEntryProjection
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/execution-entry-projection/1-0-0")
	close({
		schema_version!:            "1.0.0"
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #sha256
		allowed_routes_digest!:     #sha256
		entry_state!:               "selection-ready" | "owner-prerequisite" | "context-ready" | "task-ready" | "blocked"
		selected_unit!:             null | strings.MinRunes( 1)
		route_id!:                  null | strings.MinRunes( 1)
		next_owner!: matchN(1, [null, close({
			capability!: strings.MinRunes( 1)
			mode!:       strings.MinRunes( 1)
			target!:     strings.MinRunes( 1)
		})])
		blocker_code!:     null | strings.MinRunes( 1)
		authority_effect!: "none"
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

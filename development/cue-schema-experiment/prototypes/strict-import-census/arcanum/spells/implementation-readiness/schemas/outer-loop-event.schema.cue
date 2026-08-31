// WorkPackOuterLoopEvent
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/outer-loop-event/1-1-0")
	matchIf({
		result!: "retry"
	}, {
		event_type?:        "owner-joined"
		receipt_id?:        strings.MinRunes( 1)
		session_id?:        null
		selected_unit?:     strings.MinRunes( 1)
		route_fingerprint?: #sha256
		next_entry?: {}
		stop_decision?: null
		blocker_code?:  "REPAIRABLE_OWNER_CONDITION"
	}, _) & {} & close({
		schema_version!: "1.1.0"
		action_id!:      =~"^wpoa-[a-f0-9]{24}$"
		event_type!:     "selection-materialized" | "owner-joined" | "task-session-joined"
		receipt_id!:     null | strings.MinRunes( 1)
		session_id!:     null | strings.MinRunes( 1)
		result!:         "pass" | "block" | "retry"
		selected_unit!:  null | strings.MinRunes( 1)
		route_fingerprint!: matchN(1, [#sha256, null])
		next_entry!: null | {}
		stop_decision!:    null | strings.MinRunes( 1)
		blocker_code!:     null | strings.MinRunes( 1)
		authority_effect!: "none"
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

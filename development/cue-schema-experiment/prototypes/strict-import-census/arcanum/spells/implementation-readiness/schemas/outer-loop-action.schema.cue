// WorkPackOuterLoopAction
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/outer-loop-action/1-0-0")
	close({
		schema_version!: "1.0.0"
		action_id!:      =~"^wpoa-[a-f0-9]{24}$"
		action_type!:    "select-unit" | "route-owner" | "start-task-session" | "stop" | "complete"
		phase_before!:   strings.MinRunes( 1)
		phase_after!:    strings.MinRunes( 1)
		selected_unit!:  null | strings.MinRunes( 1)
		owner_route!: null | {}
		route_admission!: null | {}
		task_session_id!:               null | strings.MinRunes( 1)
		authorization_source!:          "work-pack-binding" | "not-required" | "none"
		authorization_prompt_required!: false
		automatic_decision!:            null | strings.MinRunes( 1)
		stop_reason!:                   null | strings.MinRunes( 1)
		authority_effect!:              "none"
	})
}

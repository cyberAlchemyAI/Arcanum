// DistillRuntimeEvent
//
// One append-only Invoke-side runtime evidence event. Event validity carries no
// verdict or mutation authority.
package prototype

import (
	"strings"
	"time"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/distill-runtime-event/1-0-0")
	matchN(3, [matchIf({
		event_type?: "role_start" | "role_result"
	}, {
		role?: "proposer" | "balancer"
	}, {
		role?:           null
		invocation_ref?: null
	}) & {}, matchIf({
		execution_path?: "role_simulation"
	}, {
		invocation_ref?: null
	}, _) & {}, matchIf({
		execution_path?: "true_subagent"
		event_type?:     "role_start" | "role_result"
	}, {
		invocation_ref?: strings.MinRunes( 1)
	}, _) & {}]) & close({
		schema_version!: "1.0.0"
		event_id!:       strings.MinRunes( 1)
		run_id!:         strings.MinRunes( 1)
		sequence!:       int & >=0
		event_type!:     "capability_probe" | "role_start" | "role_result" | "reconciliation" | "termination"
		execution_path!: "true_subagent" | "role_simulation"
		role!:           null | "proposer" | "balancer"
		invocation_ref!: null | string
		payload_ref!:    #exactArtifactRef
		emitted_at!:     time.Time
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

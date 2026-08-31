// FiniteStreamExecutionAcceptance
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/finite-stream-execution-acceptance/1-0-0")
	close({
		schema_version!:            "task-session-until-blocker.finite-stream-execution-acceptance/v1"
		approval_status!:           "approved"
		supervisor_id!:             strings.MinRunes( 1)
		scope_id!:                  strings.MinRunes( 1)
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: =~"^[a-f0-9]{64}$"
		allowed_routes_digest!:     =~"^[a-f0-9]{64}$"
		source_invocation_id!:      strings.MinRunes( 1)
		execution_mode!:            "finite-frontier"
		captured_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		chain_config_ref!:          #exactArtifactRef
		fast_entry_request_ref!:    #exactArtifactRef
		fast_entry_receipt_ref!:    #exactArtifactRef
		max_task_session_requests!: int & >=1
		risk_ceiling!:              "read-only" | "bounded-write" | "browser" | "network"
		automatic_decisions!: list.UniqueItems() & [...strings.MinRunes( 1)]
		stop_decisions!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		authority_effect!: "bounded-execution-only"
		claim_ceiling!:    strings.MinRunes( 1)
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

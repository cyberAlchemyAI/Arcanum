// TaskSessionUntilBlockerTransition
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/chain-transition/1-0-0")
	close({
		schema_version!:             "1.0.0"
		chain_id!:                   strings.MinRunes( 1)
		transition_id!:              strings.MinRunes( 1)
		transition_digest!:          null | =~"^[a-f0-9]{64}$"
		previous_transition_digest!: null | =~"^[a-f0-9]{64}$"
		epoch_id!:                   =~"^epoch-[a-f0-9]{24}$"
		cursor!:                     strings.MinRunes( 1)
		selector!:                   strings.MinRunes( 1)
		request_ordinal!:            int & >=1
		risk_class!:                 "read-only" | "bounded-write" | "browser" | "network"
		task_session_result!:        "PASS" | "FLAG" | "BLOCK"
		task_session_flags!: list.UniqueItems() & [..."observability-residue"]
		terminal_receipt_ref!: #exactArtifactRef
		wpra_v2_evidence?: close({
			selection_request_ref!:          #exactArtifactRef
			selection_receipt_ref!:          #exactArtifactRef
			mutation_admission_request_ref!: #exactArtifactRef
			mutation_admission_receipt_ref!: #exactArtifactRef
		})
		closeout!: close({
			result!:            "PASS" | "NO_OP" | "BLOCK"
			owner_receipt_ref!: #nullableArtifactRef
			no_op_proof!: null | {}
			continuation_router_verification_receipt_ref!: #nullableArtifactRef
		})
		successor!: close({
			unit_id!:          null | string
			candidate_count!:  int & >=0
			declared!:         bool
			dependency_ready!: bool
			scope_digest!:     =~"^[a-f0-9]{64}$"
		})
		observed_frontier_digest!: =~"^[a-f0-9]{64}$"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#nullableArtifactRef: matchN(1, [#exactArtifactRef, null])
}

// DistillExecutionReceipt
//
// Non-authoritative structural projection of reported Distill evidence.
// Validation requires separately resolving every reference.
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/distill-execution-receipt/1-0-0")
	close({
		schema_version!: "1.0.0"
		receipt_id!:     strings.MinRunes( 1)
		run_id!:         strings.MinRunes( 1)
		request_ref!:    #exactArtifactRef
		event_refs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		role_trace!: [_, _, ...] & [...#roleTraceEntry]
		objections!: [...#evidenceStatement]
		reconciliations!: [...#evidenceStatement]
		technique_trace!: [_, ...] & [...#techniqueTraceEntry]
		termination!: close({
			reason!:      strings.MinRunes( 1)
			round_count!: int & >=1
		})
		verdict!: "pass" | "flag" | "block"
		gaps!: [...strings.MinRunes( 1)]
		recomposition!: close({
			summary!:    strings.MinRunes( 1)
			result_ref!: #exactArtifactRef
		})
		next_route!: close({
			capability!: strings.MinRunes( 1)
			status!:     "ready" | "blocked"
		})
		reviewed_input_provenance!: [_, ...] & [...#exactArtifactRef]
	})

	#evidenceStatement: close({
		statement!:     strings.MinRunes( 1)
		objection_id?:  strings.MinRunes( 1)
		category?:      "authority" | "coverage" | "process" | "provenance" | "role" | "scope" | "technique" | "other"
		objection_ref?: strings.MinRunes( 1)
		disposition?:   "accept" | "revise" | "reject" | "defer" | "route"
		evidence_refs!: [_, ...] & [...strings.MinRunes( 1)]
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#roleTraceEntry: close({
		role!:           "proposer" | "balancer"
		execution_path!: "true_subagent" | "role_simulation"
		invocation_ref?: null | string
		evidence_refs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		result_ref!: #exactArtifactRef
	})

	#techniqueTraceEntry: close({
		technique!: strings.MinRunes( 1)
		status!:    "applied" | "not_applicable" | "failed"
		evidence_refs!: [_, ...] & [...strings.MinRunes( 1)]
	})
}

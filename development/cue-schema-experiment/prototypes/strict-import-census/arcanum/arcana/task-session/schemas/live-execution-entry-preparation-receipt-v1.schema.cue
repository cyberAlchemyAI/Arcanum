// TaskSessionLiveExecutionEntryPreparationReceiptV1
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/live-execution-entry-preparation-receipt/1-0-0")
	close({
		schema_version!:                 "task-session.live-execution-entry-preparation-receipt.v1"
		result!:                         "pass"
		attempt_id!:                     strings.MinRunes( 1)
		request_ref!:                    #exactArtifactRef
		owner_acceptance_request_ref!:   #exactArtifactRef
		owner_acceptance_response_ref!:  #exactArtifactRef
		authority_write_ceiling_digest!: #sha256
		partition_ref!:                  #exactArtifactRef
		step_outputs!: list.UniqueItems() & [_, ...] & [...#exactArtifactRef]
		effect!:         "accepted-control-preparation-only"
		receipt_digest!: #sha256
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

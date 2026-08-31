// InvokePreExecutionBlockOwnerReceiptV1
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/pre-execution-block-owner-receipt/1-0-0")
	close({
		schema_version!:                   "invoke.pre-execution-block-owner-receipt.v1"
		result!:                           "block"
		owner_capability!:                 "invoke"
		work_pack_id!:                     strings.MinRunes( 1)
		task_id!:                          strings.MinRunes( 1)
		swu_id!:                           strings.MinRunes( 1)
		attempt_id!:                       strings.MinRunes( 1)
		owner_acceptance_request_ref!:     #exactArtifactRef
		owner_acceptance_response_ref!:    #exactArtifactRef
		task_session_failure_receipt_ref!: #exactArtifactRef
		blocker_fingerprint!:              #sha256
		owner_closeout_claim!:             "unavailable-pre-execution"
		effect_summary!: close({
			material_writes!:    0
			external_effects!:   0
			selection!:          false
			admission!:          false
			execution!:          false
			successor_executed!: false
		})
		receipt_digest!: #sha256
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

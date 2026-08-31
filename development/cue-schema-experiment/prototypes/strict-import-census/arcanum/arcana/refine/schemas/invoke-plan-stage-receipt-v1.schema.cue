// InvokePlanStageReceiptV1
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/refine/invoke-plan-stage-receipt/1-0-0")
	close({
		schema_version!:        "refine.invoke-plan-stage-receipt/v1"
		receipt_id!:            strings.MinRunes( 1)
		stage_id!:              "s09-invoke-plan"
		owner_capability!:      "invoke"
		mode!:                  "plan"
		terminal_status!:       "pass"
		result!:                "pass"
		execution_designation!: "execution-candidate"
		work_pack_id!:          strings.MinRunes( 1)
		invoke_outputs!: [_, _, _, _, _, _, ...] & [...#invokeOutput]
		readiness_receipt_ref!: #exactArtifactRef
		authority_effect!:      "none"
		receipt_digest!:        =~"^[a-f0-9]{64}$"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=1
	})

	#invokeOutput: close({
		output_kind!:  strings.MinRunes( 1)
		artifact_ref!: #exactArtifactRef
	})
}

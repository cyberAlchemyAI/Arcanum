// InvokePlanReadinessBindingV2
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/refine/invoke-plan-readiness-binding/2-0-0")
	matchIf({
		execution_designation!: "execution-candidate"
	}, {
		work_pack_id?:                  strings.MinRunes( 1)
		invoke_plan_stage_receipt_ref?: #exactArtifactRef
		invoke_outputs?: [_, _, _, _, _, _, ...]
		readiness_receipt_ref?: #exactArtifactRef
		non_execution_reason?:  null
	}, {
		work_pack_id?:                  null
		invoke_plan_stage_receipt_ref?: null
		invoke_outputs?:                list.MaxItems(0)
		readiness_receipt_ref?:         null
		non_execution_reason?:          strings.MinRunes( 1)
	}) & {} & close({
		schema_version!:        "refine.invoke-plan-readiness-binding/v2"
		execution_designation!: "execution-candidate" | "non-executing"
		work_pack_id!:          null | strings.MinRunes( 1)
		invoke_plan_stage_receipt_ref!: matchN(1, [#exactArtifactRef, null])
		invoke_outputs!: [...#invokeOutput]
		readiness_receipt_ref!: matchN(1, [#exactArtifactRef, null])
		non_execution_reason!: null | strings.MinRunes( 1)
		authority_effect!:     "none"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=1
	})

	#invokeOutput: close({
		output_kind!:  "plan-artifact" | "work-pack" | "implementation-layering" | "distill-validation" | "invoke-result" | "implementation-readiness-preflight" | "task-contract" | "swu-manifest" | "execution-entry-projection" | "validation-strategy" | "transport-report" | "runtime-handoff"
		artifact_ref!: #exactArtifactRef
	})
}

// InvokePreacceptanceClosureAdoptionV1
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/preacceptance-closure-adoption/1-0-0")
	close({
		schema_version!:        "invoke.preacceptance-closure-adoption.v1"
		adoption_id!:           #nonEmptyString
		proposal_id!:           #nonEmptyString
		source_reflection_ref!: #exactArtifactRef
		implementation_owner!:  "spellcraft"
		target_contract_refs!: [_, ...] & [...#exactArtifactRef]
		negative_regression_ref!:         #regressionRef
		cross_capability_regression_ref!: #regressionRef
		rollout_evidence_ref!:            #exactArtifactRef
		later_observability_check!: close({
			status!:  "scheduled" | "pass" | "block"
			trigger!: #nonEmptyString
			owner!:   "workflow-reflect"
		})
		status!:           "proposed" | "implemented" | "enforced" | "rejected-with-reason"
		authority_effect!: "none"
		claim_ceiling!:    #nonEmptyString
		receipt_digest!:   #sha256
	})

	#exactArtifactRef: close({
		path!:       #nonEmptyString
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#nonEmptyString: strings.MinRunes(1)

	#regressionRef: close({
		artifact_ref!: #exactArtifactRef
		result!:       "pass" | "block"
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

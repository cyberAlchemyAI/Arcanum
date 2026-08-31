// InvokePreacceptanceClosureReceiptV1
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/preacceptance-closure-receipt/1-0-0")
	close({
		schema_version!:       "invoke.preacceptance-closure-receipt.v1"
		closure_id!:           #nonEmptyString
		manifest_ref!:         #exactArtifactRef
		closure_graph_digest!: #sha256
		runner_ref!:           #exactArtifactRef
		result!:               "pass" | "block"
		blockers!: list.UniqueItems() & [...#nonEmptyString]
		stage_results!: list.MaxItems(11) & [...#stageResult]
		protected_inputs!: close({
			count!:         int & >=0
			before_digest!: #sha256
			after_digest!:  #sha256
			unchanged!:     bool
		})
		repository_state!: close({
			before_digest!: #sha256
			after_digest!:  #sha256
			unchanged!:     bool
		})
		write_observation!: close({
			repository_writes!:         0
			protected_writes!:          0
			external_effects_observed!: false
		})
		determinism!: close({
			runs!:              2
			run_result_digest!: #sha256
			byte_stable!:       bool
		})
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

	#sha256: =~"^[a-f0-9]{64}$"

	#stageResult: close({
		stage_id!:          #nonEmptyString
		runner_ref!:        #exactArtifactRef
		invocation_digest!: #sha256
		exit_code!:         int
		schema_checks!: [...#nonEmptyString]
		result!: "pass" | "block"
	})
}

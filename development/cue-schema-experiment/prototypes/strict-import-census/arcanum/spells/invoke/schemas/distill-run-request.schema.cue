// DistillRunRequest
//
// Structural projection of an Invoke-owned request to execute Distill. Schema
// validity is not execution evidence.
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/distill-run-request/1-0-0")
	close({
		schema_version!:       "1.0.0"
		run_id!:               strings.MinRunes( 1)
		parent_invoke_run_id!: strings.MinRunes( 1)
		invoke_mode!:          strings.MinRunes( 1)
		distill_mode!:         strings.MinRunes( 1)
		round_budget!: close({
			max_rounds!:           int & >=1
			max_role_invocations!: int & >=2
		})
		reviewed_inputs!: [_, ...] & [...#exactArtifactRef]
		requested_techniques!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

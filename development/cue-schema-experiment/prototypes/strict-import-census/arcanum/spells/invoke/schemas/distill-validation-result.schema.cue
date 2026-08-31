// DistillValidationResult
//
// Structural shape for a validator-owned result. This schema cannot establish
// validator identity, resolve evidence, or authorize mutation by itself.
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/distill-validation-result/1-0-0")
	close({
		schema_version!:       "1.0.0"
		validation_result_id!: strings.MinRunes( 1)
		validator_version!:    strings.MinRunes( 1)
		receipt_ref!:          #exactArtifactRef
		status!:               "pass" | "flag" | "block"
		checks!: [_, ...] & [...close({
			check_id!: strings.MinRunes( 1)
			status!:   "pass" | "flag" | "block"
			evidence_refs!: [...strings.MinRunes( 1)]
		})]
		diagnostics!: [...strings.MinRunes( 1)]
		owned_gaps!: [...strings.MinRunes( 1)]
		mutation_handoff_allowed!: bool
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

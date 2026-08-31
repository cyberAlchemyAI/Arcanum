// InvokePreacceptanceClosureReviewV1
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/preacceptance-closure-review/1-0-0")
	close({
		schema_version!:       "invoke.preacceptance-closure-review.v1"
		review_id!:            #nonEmptyString
		manifest_ref!:         #exactArtifactRef
		closure_receipt_ref!:  #exactArtifactRef
		closure_graph_digest!: #sha256
		reviewer!: close({
			identity!: #nonEmptyString
			role!:     "independent-preacceptance-review"
			independent_from!: list.UniqueItems() & [_, ...] & [...#nonEmptyString]
		})
		result!: "pass" | "block"
		checks!: [_, _, _, _, _, _, _, _, _, _, ...] & [...#reviewCheck]
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

	#reviewCheck: close({
		check_id!: "final_postimages" | "execution_projection" | "consumer_closure" | "write_partition" | "runner_identity" | "schema_locator" | "runtime_derivation" | "requested_effect" | "reflection_adoption" | "no_effect_determinism"
		result!:   "pass" | "block"
		detail!:   #nonEmptyString
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

// InvokeOwnerAcceptanceRequestV2
package prototype

import (
	"struct"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/owner-acceptance-request/2-0-0")
	close({
		schema_version!:   "invoke.owner-acceptance-request.v2"
		request_id!:       #nonEmptyString
		base_request_ref!: #exactArtifactRef
		base_request!: {}
		requested_effect!: struct.MinFields(1)
		preacceptance_closure!: close({
			manifest_ref!:           #exactArtifactRef
			closure_receipt_ref!:    #exactArtifactRef
			independent_review_ref!: #exactArtifactRef
			adoption_ref!:           #exactArtifactRef
			closure_graph_digest!:   #sha256
		})
		emission_gate!:    "pass"
		authority_effect!: "none"
		claim_ceiling!:    #nonEmptyString
		request_digest!:   #sha256
	})

	#exactArtifactRef: close({
		path!:       #nonEmptyString
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#nonEmptyString: strings.MinRunes(1)

	#sha256: =~"^[a-f0-9]{64}$"
}

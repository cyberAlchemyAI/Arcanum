// InvokeOwnerAcceptanceRequestV3
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/owner-acceptance-request/3-0-0")
	close({
		schema_version!:     "invoke.owner-acceptance-request.v3"
		request_id!:         strings.MinRunes(1)
		request_digest!:     #hash
		bundle_ref!:         #ref
		accepted_stream_id!: #hash
		graph_digest!:       #hash
		requested_effect!: {}
		authority!: {}
		epoch!:           strings.MinRunes(1)
		frontier_digest!: #hash
		budgets!: close({
			request!:     1
			frontier!:    int & >=1
			child!:       1
			concurrency!: 1
		})
	})

	#hash: =~"^[a-f0-9]{64}$"

	#ref: close({
		path!:   strings.MinRunes(1)
		sha256!: #hash
	})
}

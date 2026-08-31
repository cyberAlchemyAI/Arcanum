// InvokeOwnerAcceptanceResponseV2
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/owner-acceptance-response/2-0-0")
	close({
		schema_version!:     "invoke.owner-acceptance-response.v2"
		request_id!:         strings.MinRunes(1)
		request_digest!:     #hash
		accepted_stream_id!: #hash
		literal_token!:      strings.MinRunes(1)
		decision!:           "accepted"
	})

	#hash: =~"^[a-f0-9]{64}$"
}

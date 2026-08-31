// InvokeAcceptedStreamStaticBundleV1
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-static-bundle/1-0-0")
	close({
		schema_version!: "invoke.accepted-stream-static-bundle.v1"
		graph_digest!:   #hash
		epoch!:          strings.MinRunes(1)
		requested_effect!: close({
			kind!:            "bounded-write" | "no-effect"
			external_effect!: "none"
		})
		frontier!: [_, ...] & [...close({
			ordinal!:  int & >=0
			swu_id!:   #swuId
			child_id!: #hash
		})]
		write_partitions!: {}
		accepted_write_paths!: list.UniqueItems() & [...string]
		accepted_stream_id!: #hash
	})

	#hash: =~"^[a-f0-9]{64}$"

	#swuId: =~"^SWU-[A-Za-z0-9][A-Za-z0-9._-]*$"
}

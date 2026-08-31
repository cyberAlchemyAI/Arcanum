// InvokeAcceptedStreamUnitManifestV1
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-unit-manifest/1-0-0")
	close({
		schema_version!:     "invoke.accepted-stream-unit-manifest.v1"
		accepted_stream_id!: #hash
		child_id!:           #hash
		ordinal!:            int & >=0
		swu_id!:             #swuId
		producer_id!:        strings.MinRunes(1)
		schema_ref!:         strings.MinRunes(1)
		validator_argv!: [_, ...] & [...string]
		source_selectors!:   #strings
		output_paths!:       #strings
		failure_paths!:      #strings
		invocation_closure!: #hash
	})

	#hash: =~"^[a-f0-9]{64}$"

	#strings: list.UniqueItems() & [_, ...] & [...strings.MinRunes(1)]

	#swuId: =~"^SWU-[A-Za-z0-9][A-Za-z0-9._-]*$"
}

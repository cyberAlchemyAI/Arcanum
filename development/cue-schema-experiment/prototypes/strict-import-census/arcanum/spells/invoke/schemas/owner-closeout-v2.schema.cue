package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")

	close({
		schema_version!:     "invoke.owner-closeout/v2"
		stream_id!:          strings.MinRunes( 1)
		child_id!:           strings.MinRunes( 1)
		precloseout_digest!: =~"^[a-f0-9]{64}$"
		owner!:              "invoke:refresh"
		status!:             "pass" | "block"
	})
}

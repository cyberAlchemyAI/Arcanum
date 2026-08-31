package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/post-produce-validation-receipt/1-0-0")
	close({
		schema_version!: "task-session.post-produce-validation-receipt.v1"
		unit_id!:        strings.MinRunes(1)
		result!:         "pass" | "block"
		actual_postimages!: [...close({
			path!:       string
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})]
		commands!: [...close({
			argv!: [...string]
			exit_code!: int
		})]
		undeclared_outputs!: [...string]
		authority_effect!: "none"
	})
}

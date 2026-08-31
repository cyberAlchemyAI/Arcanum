// Distill v2 Common Structural Primitives
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/common/2-0-0")
	_

	#authority_effect_none: "none"

	#bounded_count: close({
		default!: int & >=1
		maximum!: int & >=1
		minimum!: int & >=1
	})

	#canonical_identifier: string

	#exact_artifact_reference: close({
		path!:       strings.MinRunes(1)
		sha256!:     string
		size_bytes!: int & >=0
	})

	#non_empty_string: strings.MinRunes(1)

	#positive_integer: int & >=1

	#repository_relative_path: strings.MinRunes(1)

	#sha256: string

	#unique_non_empty_string_array: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]

	#utc_timestamp: =~"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z$"
}

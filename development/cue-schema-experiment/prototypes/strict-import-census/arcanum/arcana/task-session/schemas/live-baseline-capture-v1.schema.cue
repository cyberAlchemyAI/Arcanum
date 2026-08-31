package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")

	close({
		schema_version!: "task-session.live-baseline-capture/v1"
		stream_id!:      strings.MinRunes(1)
		unit_id!:        strings.MinRunes(1)
		ordinal!:        int & >=0
		paths!: list.UniqueItems() & [...close({
			path!:   strings.MinRunes(1)
			state!:  "present" | "absent"
			sha256?: null | =~"^[a-f0-9]{64}$"
		})]
		baseline_digest!: =~"^[a-f0-9]{64}$"
	})
}

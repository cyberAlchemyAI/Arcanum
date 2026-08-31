package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")

	close({
		schema_version!: "task-session-until-blocker.accepted-stream-driver-request/v1"
		stream_id!:      string
		frontier!: list.UniqueItems() & [_, ...] & [...string]
		units!: [_, ...]
		no_effect!: bool
	})
}

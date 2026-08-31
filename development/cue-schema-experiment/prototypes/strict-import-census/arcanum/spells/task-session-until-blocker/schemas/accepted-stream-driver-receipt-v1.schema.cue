package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")

	close({
		schema_version!: "task-session-until-blocker.accepted-stream-driver-receipt/v1"
		stream_id!:      string
		status!:         "complete" | "blocked"
		ordered_units!:  list.UniqueItems()
		event_digests!: [...]
		candidate_count!: 0
	})
}

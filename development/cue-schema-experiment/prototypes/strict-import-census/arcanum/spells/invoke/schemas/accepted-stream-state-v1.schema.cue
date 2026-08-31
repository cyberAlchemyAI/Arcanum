// InvokeAcceptedStreamStateV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-state/1-0-0")
	close({
		schema_version!: "invoke.accepted-stream-state.v1"
		stream_id!:      #hash
		status!:         "pending" | "current" | "completed" | "blocked" | "superseded"
		next_ordinal!:   int & >=0
		active_child!: null | {}
		completed!: [...]
		frontier!: [_, ...]
	})

	#hash: =~"^[a-f0-9]{64}$"
}

// InvokeAcceptedStreamCompletionV1
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-completion/1-0-0")
	close({
		schema_version!:     "invoke.accepted-stream-completion.v1"
		accepted_stream_id!: #hash
		frontier_digest!:    #hash
		completed_child_ids!: list.UniqueItems() & [_, ...] & [...#hash]
		final_state_digest!: #hash
		status!:             "completed"
	})

	#hash: =~"^[a-f0-9]{64}$"
}

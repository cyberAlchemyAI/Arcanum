// InvokeChildTransitionV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/child-transition/1-0-0")
	close({
		schema_version!:           "invoke.child-transition.v1"
		accepted_stream_id!:       #hash
		child_id!:                 #hash
		ordinal!:                  int & >=0
		from!:                     "unclaimed" | "active"
		to!:                       "active" | "completed" | "blocked"
		predecessor_state_digest!: #hash
	})

	#hash: =~"^[a-f0-9]{64}$"
}

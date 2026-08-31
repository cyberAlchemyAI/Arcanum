// InvokeChildClaimV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/child-claim/1-0-0")
	close({
		schema_version!:     "invoke.child-claim.v1"
		accepted_stream_id!: #hash
		child_id!:           #hash
		ordinal!:            int & >=0
		swu_id!:             #swuId
		baseline_digest!:    #hash
		status!:             "active"
	})

	#hash: =~"^[a-f0-9]{64}$"

	#swuId: =~"^SWU-[A-Za-z0-9][A-Za-z0-9._-]*$"
}

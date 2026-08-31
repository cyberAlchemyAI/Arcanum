// InvokeAcceptedStreamReceiptV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-receipt/1-0-0")
	close({
		schema_version!:     "invoke.accepted-stream-receipt.v1"
		accepted_stream_id!: #hash
		consumption_digest!: #hash
		state_digest!:       #hash
		status!:             "current"
	})

	#hash: =~"^[a-f0-9]{64}$"
}

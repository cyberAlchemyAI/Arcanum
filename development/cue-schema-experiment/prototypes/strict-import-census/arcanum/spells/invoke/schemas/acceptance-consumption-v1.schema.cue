// InvokeAcceptanceConsumptionV1
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/acceptance-consumption/1-0-0")
	close({
		schema_version!:     "invoke.acceptance-consumption.v1"
		accepted_stream_id!: #hash
		request_digest!:     #hash
		response_digest!:    #hash
		payload_digest!:     #hash
	})

	#hash: =~"^[a-f0-9]{64}$"
}

// IntentRouteTransportError
package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/intent-route/error/1")
	close({
		schema!:           "intent-route.error@1"
		reason_code!:      "IR_TRANSPORT_MALFORMED_JSON" | "IR_CAPABILITY_DENIED" | "IR_REQUEST_VERSION_UNSUPPORTED" | "IR_PORT_VERSION_UNSUPPORTED" | "IR_CORE_VERSION_MISMATCH" | "IR_MANIFEST_VERSION_MISMATCH" | "IR_CATALOG_DIGEST_MISMATCH" | "IR_CONTENT_DIGEST_MISMATCH"
		message!:          strings.MinRunes( 1)
		authority_effect!: null
	})
}

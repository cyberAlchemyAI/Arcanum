// IntentRouteDisposition
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/intent-route/disposition/1")
	close({
		schema!:         "intent-route.disposition@1"
		request_id!:     strings.MinRunes( 1)
		catalog_id!:     strings.MinRunes( 1)
		catalog_digest!: =~"^[0-9a-f]{64}$"
		kind!:           "candidate" | "ambiguous" | "no-match" | "invalid"
		reason_code!:    "IR_CANDIDATE" | "IR_AMBIGUOUS" | "IR_NO_MATCH" | "IR_INVALID_REQUEST" | "IR_INVALID_CATALOG"
		evaluated_routes!: [...close({
			route_id!:    strings.MinRunes( 1)
			eligibility!: "eligible" | "ineligible" | "unresolved" | "dominated"
			reason_codes!: [...strings.MinRunes( 1)]
			unresolved_discriminators!: list.UniqueItems() & [...strings.MinRunes( 1)]
		})]
		candidate_route_id!: null | strings.MinRunes( 1)
		clarification!: matchN(1, [null, close({
			discriminator!: strings.MinRunes( 1)
			prompt!:        strings.MinRunes( 1)
		})])
		integrity_digest!: =~"^[0-9a-f]{64}$"
		authority_effect!: "none"
	})
}

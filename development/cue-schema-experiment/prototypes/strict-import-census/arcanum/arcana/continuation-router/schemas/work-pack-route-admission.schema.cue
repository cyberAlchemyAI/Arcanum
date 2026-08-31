// WorkPackRouteAdmissionReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/continuation-router/work-pack-route-admission/1-0-0")
	matchIf({
		verdict!: "pass"
	}, {
		code?:                 "ROUTE_ADMITTED"
		authorization_source?: "work-pack-binding"
		dispatch_allowed?:     true
		candidate_count?:      1
		binding_id?:           strings.MinRunes( 1)
		binding_digest?:       #sha256
		matched_route?:        #route
		route_fingerprint?:    #sha256
		blocking_detail?:      null
	}, {
		authorization_source?: "none"
		dispatch_allowed?:     false
		matched_route?:        null
		blocking_detail?:      strings.MinRunes( 1)
	}) & {} & close({
		schema_version!:                "1.0.0"
		verdict!:                       "pass" | "block"
		code!:                          =~"^[A-Z0-9_]+$"
		authorization_source!:          "work-pack-binding" | "none"
		authorization_prompt_required!: false
		dispatch_allowed!:              bool
		candidate_count!:               int & >=0 & <=3
		binding_id!:                    null | strings.MinRunes( 1)
		binding_digest!: matchN(1, [#sha256, null])
		matched_route!: matchN(1, [#route, null])
		route_fingerprint!: matchN(1, [#sha256, null])
		blocking_detail!:  null | strings.MinRunes( 1)
		authority_effect!: "none"
	})

	#route: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...]
		effect_class!: strings.MinRunes( 1)
		required_inputs!: list.UniqueItems() & [_, ...]
		expected_receipt!: strings.MinRunes( 1)
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

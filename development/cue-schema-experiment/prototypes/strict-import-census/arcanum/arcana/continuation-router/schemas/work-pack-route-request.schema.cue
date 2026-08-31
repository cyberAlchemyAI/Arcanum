// WorkPackRouteRequest
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/continuation-router/work-pack-route-request/1-0-0")
	close({
		schema_version!: "1.0.0"
		execution_policy!: {}
		execution_entry!: {}
		execution_binding!: {}
		candidate_routes!: list.MaxItems(3) & [_, ...] & [...#route]
		installed_owner_routes!: list.UniqueItems() & [_, ...] & [...#ownerRoute]
		available_inputs!: list.UniqueItems() & [...strings.MinRunes( 1)]
		consumed_route_fingerprints!: list.UniqueItems() & [...#sha256]
		authorization_flag!: null
		authority_effect!:   "none"
	})

	#ownerRoute: close({
		capability!: strings.MinRunes( 1)
		mode!:       strings.MinRunes( 1)
	})

	#route: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: strings.MinRunes( 1)
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

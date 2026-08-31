// ExecutionIntentBinding
package prototype

import (
	"strings"
	"time"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/execution-intent-binding/1-1-0")
	close({
		schema_version!:            "1.1.0"
		binding_id!:                =~"^wpeb-[a-f0-9]{24}$"
		source_invocation_id!:      strings.MinRunes( 1)
		created_at!:                time.Time
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #sha256
		captured_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		completion_continuity_digest!: #sha256
		selected_unit!:                null | strings.MinRunes( 1)
		execution_mode!:               "one-unit" | "finite-frontier" | "until-real-blocker"
		allowed_routes_digest!:        #sha256
		current_route!: matchN(1, [null, #allowedRoute])
		write_scope_union!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		validation_commands!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		automatic_decisions!: list.UniqueItems() & [_, ...]
		stop_decisions!: list.UniqueItems() & [_, ...]
		route_fingerprint!: #sha256
		authority_effect!:  "bounded-execution-only"
		binding_digest!:    #sha256
	})

	#allowedRoute: close({
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

// PlanSelectionHandoff
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/selection-handoff/1-0-0")
	close({
		schema_version!: "1.0.0"
		audit_id!:       strings.MinRunes( 1)
		plan_epoch_id!:  =~"^epoch-[a-f0-9]{24}$"
		manifest_ref!:   #exactArtifactRef
		ready_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		allowed_routes!: [_, ...] & [...#allowedRoute]
		allowed_routes_digest!: =~"^[a-f0-9]{64}$"
		execution_entry!:       #executionEntry
		next_owner!:            "implementation-readiness:execute"
		approval_status!:       "unapproved"
		selection_required!:    true
		authority_effect!:      "none"
		mutation_ready!:        false
	})

	#allowedRoute: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...]
		effect_class!: "repository-local-reversible"
		required_inputs!: list.UniqueItems() & [_, ...]
		expected_receipt!: strings.MinRunes( 1)
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#executionEntry: close({
		entry_state!:   "selection-ready"
		selected_unit!: null
		route_id!:      null
		next_owner!: close({
			capability!: "implementation-readiness"
			mode!:       "execute"
			target!:     strings.MinRunes( 1)
		})
		blocker_code!: null
	})
}

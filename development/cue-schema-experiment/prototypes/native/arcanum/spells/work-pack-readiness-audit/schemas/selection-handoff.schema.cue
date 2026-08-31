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
		allowed_routes!: [...close({
			capability!:       strings.MinRunes(1)
			effect_class!:     "repository-local-reversible"
			expected_receipt!: strings.MinRunes(1)
			frontier_swu!:     strings.MinRunes(1)
			mode!:             strings.MinRunes(1)
			required_inputs!: list.UniqueItems() & [_, ...]
			route_id!: strings.MinRunes(1)
			target!:   strings.MinRunes(1)
			write_scope!: list.UniqueItems() & [_, ...]
		})] & [_, ...]
		allowed_routes_digest!: =~"^[a-f0-9]{64}$"
		approval_status!:       "unapproved"
		audit_id!:              strings.MinRunes(1)
		authority_effect!:      "none"
		execution_entry!: close({
			blocker_code!: null
			entry_state!:  "selection-ready"
			next_owner!: close({
				capability!: "implementation-readiness"
				mode!:       "execute"
				target!:     strings.MinRunes(1)
			})
			route_id!:      null
			selected_unit!: null
		})
		manifest_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		mutation_ready!: false
		next_owner!:     "implementation-readiness:execute"
		plan_epoch_id!:  =~"^epoch-[a-f0-9]{24}$"
		ready_frontier!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		schema_version!:     "1.0.0"
		selection_required!: true
	})

	#allowedRoute: close({
		capability!:       strings.MinRunes(1)
		effect_class!:     "repository-local-reversible"
		expected_receipt!: strings.MinRunes(1)
		frontier_swu!:     strings.MinRunes(1)
		mode!:             strings.MinRunes(1)
		required_inputs!: list.UniqueItems() & [_, ...]
		route_id!: strings.MinRunes(1)
		target!:   strings.MinRunes(1)
		write_scope!: list.UniqueItems() & [_, ...]
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes(1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#executionEntry: close({
		blocker_code!: null
		entry_state!:  "selection-ready"
		next_owner!: close({
			capability!: "implementation-readiness"
			mode!:       "execute"
			target!:     strings.MinRunes(1)
		})
		route_id!:      null
		selected_unit!: null
	})
}

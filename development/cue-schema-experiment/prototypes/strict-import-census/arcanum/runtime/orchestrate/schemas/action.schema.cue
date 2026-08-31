// Native Dispatch Runner Spawn Action
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/runtime/orchestrate/schemas/action.schema.json")
	close({
		schema_version!: "arcanum.native-dispatch-runner.action.v0.1"
		action_id!:      =~"^spawn-[0-9]{4}$"
		action!:         "spawn"
		dispatch_id!:    strings.MinRunes( 1)
		run_id!:         strings.MinRunes( 1)
		wave_id!:        strings.MinRunes( 1)
		step_id!:        strings.MinRunes( 1)
		applies_to_steps!: [_, ...] & [...strings.MinRunes( 1)]
		role!:            strings.MinRunes( 1)
		agent_ordinal!:   int & >=0
		agent_count!:     int & >=1
		capability_ref!:  strings.MinRunes( 1)
		target!:          strings.MinRunes( 1)
		mode!:            strings.MinRunes( 1)
		mutation_policy!: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
		write_scope!: [...string]
		forbidden_write_scopes!: [...string]
		briefing_binding!: #role_briefing_binding
		input_refs!: [...string]
		output_refs!: [...string]
	})

	#role_briefing_binding: close({
		contract_version!: "arcanum.confirmed-role-briefing.v0.1"
		source_binding!: close({
			artifact_path!:           strings.MinRunes( 1)
			artifact_sha256!:         =~"^[0-9a-f]{64}$"
			selector!:                =~"^/"
			selected_payload_sha256!: =~"^[0-9a-f]{64}$"
		})
		briefing!: close({
			agent_identity!: strings.MinRunes( 1)
			angle!:          strings.MinRunes( 1)
			instructions!:   strings.MinRunes( 1)
			status_semantics!: close({
				task_status_field!:        strings.MinRunes( 1)
				task_complete_value!:      strings.MinRunes( 1)
				task_blocked_value!:       strings.MinRunes( 1)
				domain_gate_status_field!: strings.MinRunes( 1)
				domain_gate_is_separate!:  true
			})
			read_policy!: close({
				input_refs!: [...string]
				allowed_read_scopes!: [...string]
				forbidden_read_scopes!: [...string]
				required_input_refs_readable!: true
			})
			write_policy!: close({
				mutation_policy!: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
				write_scope!: [...string]
				forbidden_write_scopes!: [...string]
			})
			receipt_shape!: close({
				required_fields!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
				completion_requires_all_fields!: true
			})
			authority_ceiling!: close({
				summary!: strings.MinRunes( 1)
				allowed_actions!: [...string]
				forbidden_actions!: [...string]
			})
		})
		briefing_sha256!: =~"^[0-9a-f]{64}$"
	})
}

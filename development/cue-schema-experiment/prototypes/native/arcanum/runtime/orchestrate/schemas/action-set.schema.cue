// Native Dispatch Runner Next Action Set
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/runtime/orchestrate/schemas/action-set.schema.json")
	matchN(2, [matchIf({
		schema_version?: "arcanum.native-dispatch-runner.action-set.v0.1"
	}, {
		decision?: "gate_pass" | "gate_block"
	}, {
		source_gate_id?: strings.MinRunes(1)
	}) & {}, matchIf({
		decision?: "gate_resolved"
	}, {
		actions?: null | bool | number | string | list.MaxItems(0) | {}
		next_wave_id?: null
	}, _) & {}]) & close({
		actions!: [..._#defs."/properties/actions/items"]
		decision!:       "gate_pass" | "gate_block" | "gate_resolved"
		dispatch_id!:    strings.MinRunes(1)
		next_wave_id!:   null | string
		run_id!:         strings.MinRunes(1)
		schema_version!: "arcanum.native-dispatch-runner.action-set.v0.1" | "arcanum.native-dispatch-runner.action-set.v0.2"
		source_gate_id!: null | string
		source_wave_id!: strings.MinRunes(1)
	})

	// Native Dispatch Runner Spawn Action
	_#defs: "/properties/actions/items": {
		@jsonschema(id="https://arcanum.local/runtime/orchestrate/schemas/action.schema.json")
		close({
			action!:        "spawn"
			action_id!:     =~"^spawn-[0-9]{4}$"
			agent_count!:   int & >=1
			agent_ordinal!: int & >=0
			applies_to_steps!: [...strings.MinRunes(1)] & [_, ...]
			briefing_binding!: close({
				briefing!: close({
					agent_identity!: strings.MinRunes(1)
					angle!:          strings.MinRunes(1)
					authority_ceiling!: close({
						allowed_actions!: [...string]
						forbidden_actions!: [...string]
						summary!: strings.MinRunes(1)
					})
					instructions!: strings.MinRunes(1)
					read_policy!: close({
						allowed_read_scopes!: [...string]
						forbidden_read_scopes!: [...string]
						input_refs!: [...string]
						required_input_refs_readable!: true
					})
					receipt_shape!: close({
						completion_requires_all_fields!: true
						required_fields!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
					})
					status_semantics!: close({
						domain_gate_is_separate!:  true
						domain_gate_status_field!: strings.MinRunes(1)
						task_blocked_value!:       strings.MinRunes(1)
						task_complete_value!:      strings.MinRunes(1)
						task_status_field!:        strings.MinRunes(1)
					})
					write_policy!: close({
						forbidden_write_scopes!: [...string]
						mutation_policy!: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
						write_scope!: [...string]
					})
				})
				briefing_sha256!:  =~"^[0-9a-f]{64}$"
				contract_version!: "arcanum.confirmed-role-briefing.v0.1"
				source_binding!: close({
					artifact_path!:           strings.MinRunes(1)
					artifact_sha256!:         =~"^[0-9a-f]{64}$"
					selected_payload_sha256!: =~"^[0-9a-f]{64}$"
					selector!:                =~"^/"
				})
			})
			capability_ref!: strings.MinRunes(1)
			dispatch_id!:    strings.MinRunes(1)
			forbidden_write_scopes!: [...string]
			input_refs!: [...string]
			mode!:            strings.MinRunes(1)
			mutation_policy!: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
			output_refs!: [...string]
			role!:           strings.MinRunes(1)
			run_id!:         strings.MinRunes(1)
			schema_version!: "arcanum.native-dispatch-runner.action.v0.1"
			step_id!:        strings.MinRunes(1)
			target!:         strings.MinRunes(1)
			wave_id!:        strings.MinRunes(1)
			write_scope!: [...string]
		})
	}

	_#defs: "/properties/actions/items/$defs/role_briefing_binding": close({
		briefing!: close({
			agent_identity!: strings.MinRunes(1)
			angle!:          strings.MinRunes(1)
			authority_ceiling!: close({
				allowed_actions!: [...string]
				forbidden_actions!: [...string]
				summary!: strings.MinRunes(1)
			})
			instructions!: strings.MinRunes(1)
			read_policy!: close({
				allowed_read_scopes!: [...string]
				forbidden_read_scopes!: [...string]
				input_refs!: [...string]
				required_input_refs_readable!: true
			})
			receipt_shape!: close({
				completion_requires_all_fields!: true
				required_fields!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			})
			status_semantics!: close({
				domain_gate_is_separate!:  true
				domain_gate_status_field!: strings.MinRunes(1)
				task_blocked_value!:       strings.MinRunes(1)
				task_complete_value!:      strings.MinRunes(1)
				task_status_field!:        strings.MinRunes(1)
			})
			write_policy!: close({
				forbidden_write_scopes!: [...string]
				mutation_policy!: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
				write_scope!: [...string]
			})
		})
		briefing_sha256!:  =~"^[0-9a-f]{64}$"
		contract_version!: "arcanum.confirmed-role-briefing.v0.1"
		source_binding!: close({
			artifact_path!:           strings.MinRunes(1)
			artifact_sha256!:         =~"^[0-9a-f]{64}$"
			selected_payload_sha256!: =~"^[0-9a-f]{64}$"
			selector!:                =~"^/"
		})
	})
}

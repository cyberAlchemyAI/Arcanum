// Distill v2 ModeSpec
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/mode-spec/2-0-0")
	close({
		closeout_policy!: close({
			navigation_required!: true
			required_techniques!: list.UniqueItems() & [...string] & [_, ...]
			verdict_owner!: "core_engine"
		})
		cycle_policy!: close({
			maximum_repeated_structure!: int & >=1
			maximum_stagnant_rounds!:    int & >=1
		})
		display_name!: strings.MinRunes(1)
		human_gate_policy!: close({
			trigger!: "never" | "no_justified_winner" | "blocker_decision"
		})
		mode_id!: string
		pitch_off_policy!: close({
			behavior!: "never" | "multiple_viable_tracks"
			comparison_dimensions!: list.UniqueItems() & [..."fit" | "option_value" | "risk" | "cost" | "assumptions" | "elimination_conditions"]
		})
		role_program!: close({
			execution_paths!: list.UniqueItems() & [..."true_subagent" | "role_simulation"] & [_, ...]
			preserve_role_trace!: true
			roles!: list.UniqueItems() & [..."proposer" | "balancer"] & [_, ...]
		})
		rounds_per_track!: close({
			default!: int & >=1
			maximum!: int & >=1
			minimum!: int & >=1
		})
		schema_version!: "distill.mode_spec.v2"
		technique_policy!: close({
			always_required!: list.UniqueItems() & [...string] & [_, ...]
			conditional_allowed!: list.UniqueItems() & [...string]
			skipped_reason_required!: true
		})
		tracks!: close({
			default!: int & >=1
			maximum!: int & >=1
			minimum!: int & >=1
		})
	})

	#closeout_policy: close({
		navigation_required!: true
		required_techniques!: list.UniqueItems() & [...string] & [_, ...]
		verdict_owner!: "core_engine"
	})

	#cycle_policy: close({
		maximum_repeated_structure!: int & >=1
		maximum_stagnant_rounds!:    int & >=1
	})

	#human_gate_policy: close({
		trigger!: "never" | "no_justified_winner" | "blocker_decision"
	})

	#pitch_off_policy: close({
		behavior!: "never" | "multiple_viable_tracks"
		comparison_dimensions!: list.UniqueItems() & [..."fit" | "option_value" | "risk" | "cost" | "assumptions" | "elimination_conditions"]
	})

	#role_program: close({
		execution_paths!: list.UniqueItems() & [..."true_subagent" | "role_simulation"] & [_, ...]
		preserve_role_trace!: true
		roles!: list.UniqueItems() & [..."proposer" | "balancer"] & [_, ...]
	})

	#technique_policy: close({
		always_required!: list.UniqueItems() & [...string] & [_, ...]
		conditional_allowed!: list.UniqueItems() & [...string]
		skipped_reason_required!: true
	})
}

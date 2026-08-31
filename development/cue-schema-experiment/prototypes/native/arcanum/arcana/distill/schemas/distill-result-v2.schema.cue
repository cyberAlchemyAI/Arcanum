// Distill v2 ResultEnvelope
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/result/2-0-0")
	matchN(3, [matchIf({
		verdict?: "pass"
	}, {
		current_smallest_coherent_unit?: close({
			abstraction_level!: "purpose" | "value_constraint" | "capability" | "function" | "workflow_process" | "policy_rule" | "interface" | "artifact" | "operation"
			inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			name!: strings.MinRunes(1)
			outputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			responsibility!:   strings.MinRunes(1)
			selected_unit_id!: string
		})
		readiness_effects?: null | bool | number | string | list.MaxItems(0) | {}
		selected_unit_id?: string
		tension_ledger?: matchN(0, [null | bool | number | string | list.MatchN(>=1, null | bool | number | string | [...] | {
			effect!: "block"
		}) | {}])
	}, _) & {}, matchIf({
		verdict?: "flag"
	}, {
		current_smallest_coherent_unit?: close({
			abstraction_level!: "purpose" | "value_constraint" | "capability" | "function" | "workflow_process" | "policy_rule" | "interface" | "artifact" | "operation"
			inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			name!: strings.MinRunes(1)
			outputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			responsibility!:   strings.MinRunes(1)
			selected_unit_id!: string
		})
		readiness_effects?: null | bool | number | string | [_, ...] | {}
		selected_unit_id?: string
	}, _) & {}, matchIf({
		verdict?: "block"
	}, {
		current_smallest_coherent_unit?: null
		next_route?:                     "robot_talks" | "decision_gate" | "deferred"
		selected_unit_id?:               null
	}, _) & {}]) & close({
		authority_effect!: "none"
		closure_and_recomposition_proof!: close({
			abstraction_level_explicit!: bool
			inputs_outputs_named!:       bool
			no_hidden_glue!:             bool
			no_meaning_loss!:            bool
			no_smuggled_scale!:          bool
			recomposes_upward!:          bool
			responsibility_closed!:      bool
		})
		concept_layer_map!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		current_smallest_coherent_unit!: matchN(1, [close({
			abstraction_level!: "purpose" | "value_constraint" | "capability" | "function" | "workflow_process" | "policy_rule" | "interface" | "artifact" | "operation"
			inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			name!: strings.MinRunes(1)
			outputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			responsibility!:   strings.MinRunes(1)
			selected_unit_id!: string
		}), null])
		deferred_complexity!: [...strings.MinRunes(1)]
		evidence_emission!: "complete" | "partial" | "failed" | "not_required" | "not_configured"
		evolution_profile!: strings.MinRunes(1)
		frame_expiry_note!: strings.MinRunes(1)
		mode_budget!: close({
			rounds_per_track!: int & >=1
			tracks!:           int & >=1
		})
		mode_id!: string
		navigation_guide!: close({
			how_to_use!: strings.MinRunes(1)
			start_here!: strings.MinRunes(1)
			unresolved!: [...strings.MinRunes(1)]
			what_changed!: strings.MinRunes(1)
		})
		next_route!:         "implementation_layering" | "robot_talks" | "decision_gate" | "invoke_design" | "invoke_plan" | "task_session" | "deferred"
		objective!:          strings.MinRunes(1)
		optimization_point!: strings.MinRunes(1)
		output_artifact!:    strings.MinRunes(1)
		premortem!:          strings.MinRunes(1)
		proposal_tracks!: [...close({
			status!:   "selected" | "viable" | "eliminated"
			summary!:  strings.MinRunes(1)
			track_id!: string
		})] & [_, ...]
		readiness_effects!: [...close({
			effect!:       "flag"
			route_status!: "available" | "deferred" | "blocked"
			tension_id!:   string
		})]
		recursive_rounds!: [...close({
			outcome!:  strings.MinRunes(1)
			round!:    int & >=1
			track_id!: string
		})] & [_, ...]
		role_conversation_trace!: [...close({
			balancer_objection!:  strings.MinRunes(1)
			proposer_claim!:      strings.MinRunes(1)
			reconciliation!:      strings.MinRunes(1)
			round!:               int & >=1
			stable_disagreement!: bool
			track_id!:            string
		})] & [_, ...]
		run_id!:           string
		schema_version!:   "distill.result.v2"
		selected_unit_id!: null | string
		source_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})
		target_context!: strings.MinRunes(1)
		technique_pack_trace!: [...close({
			decision!:         "pass" | "flag" | "block" | "skip_with_reason"
			hook_id!:          string
			readiness_effect!: "none" | "flag" | "block"
			technique_id!:     string
		})] & [_, ...]
		telemetry!: "recorded" | "failed_with_residue" | "not_configured"
		tension_ledger!: [...close({
			effect!:     "none" | "flag" | "block"
			status!:     "resolved" | "stable_disagreement" | "unresolved"
			summary!:    strings.MinRunes(1)
			tension_id!: string
		})]
		verdict!: "pass" | "flag" | "block"
	})

	#closure_proof: close({
		abstraction_level_explicit!: bool
		inputs_outputs_named!:       bool
		no_hidden_glue!:             bool
		no_meaning_loss!:            bool
		no_smuggled_scale!:          bool
		recomposes_upward!:          bool
		responsibility_closed!:      bool
	})

	#coherent_unit: close({
		abstraction_level!: "purpose" | "value_constraint" | "capability" | "function" | "workflow_process" | "policy_rule" | "interface" | "artifact" | "operation"
		inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		name!: strings.MinRunes(1)
		outputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		responsibility!:   strings.MinRunes(1)
		selected_unit_id!: string
	})

	#navigation_guide: close({
		how_to_use!: strings.MinRunes(1)
		start_here!: strings.MinRunes(1)
		unresolved!: [...strings.MinRunes(1)]
		what_changed!: strings.MinRunes(1)
	})

	#proposal_track: close({
		status!:   "selected" | "viable" | "eliminated"
		summary!:  strings.MinRunes(1)
		track_id!: string
	})

	#readiness_effect: close({
		effect!:       "flag"
		route_status!: "available" | "deferred" | "blocked"
		tension_id!:   string
	})

	#recursive_round: close({
		outcome!:  strings.MinRunes(1)
		round!:    int & >=1
		track_id!: string
	})

	#role_exchange: close({
		balancer_objection!:  strings.MinRunes(1)
		proposer_claim!:      strings.MinRunes(1)
		reconciliation!:      strings.MinRunes(1)
		round!:               int & >=1
		stable_disagreement!: bool
		track_id!:            string
	})

	#technique_outcome: close({
		decision!:         "pass" | "flag" | "block" | "skip_with_reason"
		hook_id!:          string
		readiness_effect!: "none" | "flag" | "block"
		technique_id!:     string
	})

	#tension: close({
		effect!:     "none" | "flag" | "block"
		status!:     "resolved" | "stable_disagreement" | "unresolved"
		summary!:    strings.MinRunes(1)
		tension_id!: string
	})
}

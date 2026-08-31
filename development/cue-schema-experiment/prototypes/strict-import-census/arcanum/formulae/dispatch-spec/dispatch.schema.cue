// Arcanum Dispatch Spec
//
// Draft schema for describing governed Arcanum routes, including
// capability-bound delegated execution waves.
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/formulae/dispatch-spec/dispatch.schema.yml")
	dispatch_id!:        strings.MinRunes(1)
	parent_dispatch_id?: null | string
	intent!: {
		raw!:             strings.MinRunes(1)
		objective!:       strings.MinRunes(1)
		target_artifact?: string
		arcanum_vocabulary?: [...string]
		operator_sentence?: string
		...
	}
	mode!: "single" | "sequence" | "fanout" | "dialectic" | "tournament" | "research" | "validation" | "spell-design" | "implementation-research" | "mixed"

	// ChoiceCard-like bounded menu of possible routes or capabilities.
	route_menu?: {
		context_hint?: string
		items?: list.MaxItems(9) & [_, ...] & [...{
			id!:             strings.MinRunes(1)
			label!:          strings.MinRunes(1)
			description!:    strings.MinRunes(1)
			capability_ref?: string
			pattern?:        string
			...
		}]
		selected_item_id?: null | string
		...
	}

	// Dispatch-level technique ids selected from TECHNIQUE-CATALOG.md or locally justified extensions.
	techniques?: [...#technique_ref]

	// Optional named technique profiles a route proposer may activate without
	// changing the core dispatch schema.
	technique_overlays?: [...{
		overlay_id!: strings.MinRunes(1)
		trigger!:    strings.MinRunes(1)
		techniques!: [_, ...] & [...#technique_ref]
		applies_to_steps!: [_, ...] & [...string]
		validation_expectation!: strings.MinRunes(1)
		...
	}]

	// Optional execution strategy for role-bound subagents or delegated sibling agents.
	subagent_strategy?: matchIf({
		binding_mode!: "capability-bound"
	}, {
		execution_owner!: null | bool | number | strings.MinRunes(
			1) | [...] | {}
		roles!: null | bool | number | string | [_, ...] & [...null | bool | number | string | [...] | {
			role_id!:           _
			purpose!:           _
			owns!:              _
			capability_ref!:    _
			capability_target!: _
			capability_mode!:   _
			agent_count!:       _
			mutation_policy!:   _
			applies_to_steps!:  _
			output_refs!:       _
		}] | {}
		execution_waves!: null | bool | number | string | [_, ...] | {}
		receipt_requirements!: null | bool | number | string | [_, ...] | {}
	}, _) & {} & {
		status!:      "none" | "recommended" | "required" | "blocked"
		trigger?:     string
		explanation!: strings.MinRunes(1)
		context?: [...string]

		// Use capability-bound when each delegated role must be executable through one
		// named owner capability.
		binding_mode?: "descriptive" | "capability-bound"

		// Parent capability that owns spawn, join, gates, and final synthesis.
		execution_owner?:            string
		execution_contract_version?: "arcanum.capability-bound-execution.v0.2"
		roles?: [...{
			role_id!: strings.MinRunes(1)
			purpose!: strings.MinRunes(1)
			owns!:    strings.MinRunes(1)

			// Lifecycle or execution capability governing this worker.
			capability_ref?: string

			// Sigil, spell, artifact, or bounded task operated on by the capability.
			capability_target?: string

			// Mode passed to the governing capability, such as update, reflect, validate, or execute.
			capability_mode?: string
			agent_count?:     int & >=1 & <=16
			mutation_policy?: "read-only" | "proposal-only" | "lifecycle-owned" | "artifact-only"
			write_scope?: [...string]
			forbidden_write_scopes?: [...string]
			briefing_binding?: #role_briefing_binding
			depends_on_roles?: [...string]
			input_refs?: [...string]
			output_refs?: [...string]
			applies_to_steps?: [...string]
			...
		}]

		// Ordered worker waves. Roles within one parallel wave may run together; later
		// waves wait for declared joins and gates.
		execution_waves?: [...{
			wave_id!: strings.MinRunes(1)
			role_ids!: [_, ...] & [...string]
			parallel!:    bool
			join_policy!: "all" | "quorum" | "ranked" | "pareto" | "parent_synthesis" | "human_gate"
			depends_on_waves?: [...string]
			gate_after?:    string
			on_incomplete!: "block" | "flag" | "defer" | "reroute"
			...
		}]
		parallelism?:       "none" | "fanout" | "dialectic" | "tournament" | "mixed"
		join_policy?:       "none" | "all" | "quorum" | "ranked" | "pareto" | "parent_synthesis" | "human_gate"
		authorization!:     "not_needed" | "requires_user_permission" | "approved" | "blocked"
		permission_prompt?: string

		// Exact-sheet registration proof required by the native runtime before any approved subagent spawn.
		registration?: close({
			schema_version!:              "arcanum.subagent-strategy-registration.v0.2"
			ledger!:                      ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml"
			sheet_schema_version!:        "0.6.1"
			sheet_sha256!:                =~"^[0-9a-f]{64}$"
			execution_projection_sha256!: =~"^[0-9a-f]{64}$"
			temporary_sheet!:             strings.MinRunes(1)
			temporary_close!:             strings.MinRunes(1)
		})

		// Preconfirmation registration declaration. Post-confirmation evidence is
		// carried by a separate run-local execution entry so the closure-bound
		// dispatch remains immutable.
		registration_intent?: close({
			schema_version!: "arcanum.subagent-strategy-registration-intent.v0.1"
			profile_id!:     strings.MinRunes(1)
			profile_ref!: close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[0-9a-f]{64}$"
				size!:   int & >=1
			})
			confirmation_mode!:           "exact_sheet" | "material_projection"
			source_lifecycle!:            "consumed" | "durable"
			registration_schema_version!: "arcanum.subagent-strategy-registration.v0.3"
		})
		receipt_requirements?: [...string]
		...
	}

	// Optional runtime ledger proving each delegated subagent was joined, closed,
	// blocked, timed out with residue, or handed off.
	subagent_lifecycle?: {
		status!: "none" | "pass" | "flag" | "block"
		agents!: [...{
			agent_id!:          strings.MinRunes(1)
			role_id!:           strings.MinRunes(1)
			capability_ref?:    string
			capability_target?: string
			capability_mode?:   string
			wave_id?:           string
			write_scope?: [...string]
			lane_name?:        string
			spawn_status!:     "spawned" | "blocked"
			spawn_error?:      string
			join_status?:      "not_needed" | "pending" | "completed" | "timed_out" | "blocked" | "handed_off" | "closed_without_result"
			join_timeout_ms?:  int & >=0
			receipt_artifact?: string
			close_status?:     "not_needed" | "pending" | "closed" | "already_closed" | "handed_off" | "blocked"
			close_error?:      string
			residue?:          string
			reroute?:          string
			...
		}]
		...
	}

	// Expected or observed receipts for native runtime-backed dispatch stages.
	native_stage_receipts?: [...{
		dispatch_id?:    string
		step_id!:        strings.MinRunes(1)
		capability_ref!: strings.MinRunes(1)
		receipt_kind!:   "native-stage" | "subagent" | "handoff" | "blocked"
		status!:         "pass" | "flag" | "block" | "not_run"
		artifacts?: [...string]
		validation?: [...string]
		observer_status?: string
		blockers?: [...string]
		residue?:      string
		handoff_note?: string
		...
	}]
	steps!: [_, ...] & [...{
		step_id!:        strings.MinRunes(1)
		name!:           strings.MinRunes(1)
		capability_ref!: strings.MinRunes(1)
		mode?:           string
		pattern!:        "route" | "sequential" | "fanout" | "dialectic" | "tournament" | "distill" | "xray" | "decision" | "validation" | "toy_game" | "synthesis" | "handoff"
		parallel?:       bool
		depends_on_steps?: [...string]

		// Technique ids used by this step. Use catalog ids where possible; local
		// extensions must include a source note.
		techniques?: [...#technique_ref]
		roles?: [...string]
		inputs!: [_, ...] & [...{
			kind!: "intent" | "frame" | "handle" | "decision" | "ledger" | "human_answer" | "external_context" | "artifact" | "receipt"
			ref!:  strings.MinRunes(1)
			...
		}]
		outputs!: [_, ...] & [...{
			kind!: "frame" | "handle" | "decision" | "ledger" | "artifact" | "route_menu" | "handoff" | "trace_event" | "receipt"
			ref!:  strings.MinRunes(1)
			...
		}]
		join_policy?: "none" | "all" | "quorum" | "ranked" | "pareto" | "parent_synthesis" | "human_gate"
		convergence_criteria?: [...string]
		evidence_artifact?: string
		stop_conditions?: [...string]
		...
	}]
	gates!: [_, ...] & [...{
		gate_id!:   strings.MinRunes(1)
		kind!:      "policy" | "decision" | "quality" | "promotion_guardrail" | "validation" | "human_approval"
		owner!:     strings.MinRunes(1)
		condition!: strings.MinRunes(1)

		// Capability-bound execution wave whose join this gate evaluates.
		applies_after_wave?: string

		// Exact role output refs that must pass before a dependent wave starts.
		requires_role_receipts?: [...string]
		evaluation?: matchN(1, [close({
			mode!: "receipt_status"
		}), close({
			mode!:           "domain_status"
			source_role_id!: strings.MinRunes(1)
			source_field!:   strings.MinRunes(1)
			pass_values!: list.UniqueItems() & [_, ...] & [...strings.MinRunes(1)]
			resolved_values?: list.UniqueItems() & [...strings.MinRunes(1)]
		})])
		on_fail?: "block" | "flag" | "defer" | "ask" | "reroute"
		...
	}]
	observability!: {
		dispatch_id_required?: bool
		parent_dispatch_id?:   null | string
		trace_events!: [_, ...] & [...string]
		signal_grouping?: string
		...
	}

	// Optional boundary/evidence contract for cross-capability handoffs, authority
	// ownership, receipts, state namespaces, and promotion splits.
	boundary_evidence?: {
		boundaries?: [...#boundary]
		authority?: #authority_map
		receipts?: [...#receipt_expectation]
		state_namespaces?: [...#state_namespace]
		promotion_splits?: [...#promotion_split]
		...
	}
	promotion_guardrails?: [...string]

	#authority_map: {
		lifecycle?:  string
		execution?:  string
		validation?: string
		evidence?:   string
		memory?:     string
		promotion?:  string
		{[!~"^(lifecycle|execution|validation|evidence|memory|promotion)$"]: string}
	}

	#boundary: {
		boundary_id!: strings.MinRunes(1)
		kind!:        "capability_handoff" | "artifact_import" | "human_approval" | "evidence_return" | "memory_interaction" | "state_write" | "external_context"
		from_owner?:  string
		to_owner?:    string
		applies_to_steps?: [...string]
		contract!:     strings.MinRunes(1)
		on_violation!: #gate_action
		...
	}

	#gate_action: "block" | "flag" | "defer" | "ask" | "reroute"

	#promotion_split: {
		source!:       strings.MinRunes(1)
		target!:       strings.MinRunes(1)
		rule!:         strings.MinRunes(1)
		on_violation!: #gate_action
		...
	}

	#receipt_expectation: {
		receipt_id!: strings.MinRunes(1)
		producer!:   strings.MinRunes(1)
		required_fields!: [_, ...] & [..."run_id" | "session_id" | "artifacts" | "validation_result" | "dispatch_id" | "step_id" | "capability_ref" | "status" | "validation" | "observer_status" | "blockers" | "handoff_note" | "approval_record" | "audit_reference" | "residue"]
		stores?: [...string]
		on_missing!: #gate_action
		...
	}

	#role_briefing_binding: close({
		contract_version!: "arcanum.confirmed-role-briefing.v0.1"
		source_binding!: close({
			artifact_path!:           strings.MinRunes(1)
			artifact_sha256!:         =~"^[0-9a-f]{64}$"
			selector!:                =~"^/"
			selected_payload_sha256!: =~"^[0-9a-f]{64}$"
		})
		briefing!: close({
			agent_identity!: strings.MinRunes(1)
			angle!:          strings.MinRunes(1)
			instructions!:   strings.MinRunes(1)
			status_semantics!: close({
				task_status_field!:        strings.MinRunes(1)
				task_complete_value!:      strings.MinRunes(1)
				task_blocked_value!:       strings.MinRunes(1)
				domain_gate_status_field!: strings.MinRunes(1)
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
				required_fields!: list.UniqueItems() & [_, ...] & [...strings.MinRunes(1)]
				completion_requires_all_fields!: true
			})
			authority_ceiling!: close({
				summary!: strings.MinRunes(1)
				allowed_actions!: [...string]
				forbidden_actions!: [...string]
			})
		})
		briefing_sha256!: =~"^[0-9a-f]{64}$"
	})

	#state_namespace: {
		namespace!:    strings.MinRunes(1)
		owner!:        strings.MinRunes(1)
		write_policy!: strings.MinRunes(1)
		...
	}

	#technique_ref: matchN(1, [strings.MinRunes(1), {
		id!:              strings.MinRunes(1)
		source!:          "arcanum-dispatch-synthesis" | "pole-data-standards" | "local-extension"
		purpose?:         string
		validation_note?: string
		...
	}])
	...
}

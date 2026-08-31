// WorkPackOuterLoopState
package prototype

import (
	"strings"
	"time"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/outer-loop-state/1-2-0")
	close({
		schema_version!:            "1.2.0"
		loop_id!:                   =~"^wpol-[a-f0-9]{24}$"
		source_invocation_id!:      strings.MinRunes( 1)
		created_at!:                time.Time
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #sha256
		allowed_routes_digest!:     #sha256
		execution_mode!:            "one-unit" | "finite-frontier" | "until-real-blocker"
		captured_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		completion_continuity!: #completionContinuity
		phase!:                 "ready" | "awaiting-selection" | "awaiting-owner" | "awaiting-task-session" | "complete" | "blocked"
		current_entry!: {}
		current_binding!: {}
		binding_ids!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		pending_action_id!:       null | strings.MinRunes( 1)
		pending_task_session_id!: null | strings.MinRunes( 1)
		step_budget!:             int & >=1
		steps_used!:              int & >=0
		visited_units!: list.UniqueItems() & [...strings.MinRunes( 1)]
		consumed_route_fingerprints!: list.UniqueItems() & [...#sha256]
		route_retry_counts!: close({
			{[=~"^[a-f0-9]{64}$"]: 1 & int}
		})
		pending_retry!: matchN(1, [null, close({
			route_fingerprint!: #sha256
			blocker_code!:      "REPAIRABLE_OWNER_CONDITION"
			owner_receipt_id!:  strings.MinRunes( 1)
		})])
		owner_receipts!: [...#ownerReceipt]
		task_session_receipts!: [...#taskSessionReceipt]
		automatic_decisions!: [...#automaticDecision]
		authorization_prompt_count!: 0
		pending_stop_decision!:      null | strings.MinRunes(1)
		stop_reason!:                null | strings.MinRunes( 1)
		authority_effect!:           "none"
	})

	#automaticDecision: close({
		sequence!:       int & >=1
		decision_class!: strings.MinRunes( 1)
		action_type!:    "select-unit" | "route-owner" | "start-task-session"
		selected_unit!:  null | strings.MinRunes( 1)
	})

	#completedPrefixItem: close({
		unit_id!:                 strings.MinRunes( 1)
		unit_contract_digest!:    #sha256
		completion_binding_id!:   strings.MinRunes( 1)
		completion_artifact_ref!: #exactArtifactRef
		closeout_binding_id!:     strings.MinRunes( 1)
	})

	#completionContinuity: close({
		source_audit_id!:           strings.MinRunes( 1)
		source_projection_digest!:  #sha256
		work_pack_semantic_digest!: #sha256
		plan_epoch_id!:             =~"^epoch-[a-f0-9]{24}$"
		completed_prefix!: list.UniqueItems() & [...#completedPrefixItem]
		next_unit!:         null | strings.MinRunes( 1)
		authority_effect!:  "none"
		continuity_digest!: #sha256
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#ownerReceipt: matchN(2, [matchIf({
		result!: "retry"
	}, {
		blocker_code?: "REPAIRABLE_OWNER_CONDITION"
	}, _) & {}, matchIf({
		result!: "pass"
	}, {
		blocker_code?: null
	}, _) & {}]) & close({
		receipt_id!:        strings.MinRunes( 1)
		result!:            "pass" | "block" | "retry"
		capability!:        strings.MinRunes( 1)
		mode!:              strings.MinRunes( 1)
		route_fingerprint!: #sha256
		blocker_code!:      null | strings.MinRunes( 1)
	})

	#sha256: =~"^[a-f0-9]{64}$"

	#taskSessionReceipt: close({
		receipt_id!:        strings.MinRunes( 1)
		session_id!:        strings.MinRunes( 1)
		selected_unit!:     strings.MinRunes( 1)
		result!:            "pass" | "block"
		route_fingerprint!: #sha256
	})
}

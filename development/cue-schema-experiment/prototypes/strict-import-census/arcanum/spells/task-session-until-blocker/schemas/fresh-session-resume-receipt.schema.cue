// FreshSessionResumeReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/fresh-session-resume-receipt/1-0-0")
	matchN(2, [matchIf({
		decision!: "start-fresh-session"
	}, {
		code?:                           "FRESH_TASK_SESSION_READY"
		detail?:                         null
		joined_owner_receipt_count?:     1
		owner_join?:                     #ownerJoin
		fresh_task_session_start_count?: 1
		fresh_task_session?:             #freshSession
		task_session_receipt_slot?:      #receiptSlot
		evidence_write_count?:           1
		ledger_event_ref?:               #exactArtifactRef
	}, _) & {}, matchIf({
		decision!: "block"
	}, {
		detail?:                         strings.MinRunes( 1)
		fresh_task_session_start_count?: 0
		fresh_task_session?:             null
		task_session_receipt_slot?:      null
		evidence_write_count?:           0
		ledger_event_ref?:               null
	}, _) & {}]) & close({
		schema_version!: "1.0.0"
		receipt_id!:     =~"^fsr-[a-f0-9]{24}$"
		chain_id!:       null | strings.MinRunes( 1)
		loop_id!:        null | strings.MinRunes( 1)
		loop_state_digest!: matchN(1, [#sha256, null])
		work_pack_id!: null | strings.MinRunes( 1)
		work_pack_semantic_digest!: matchN(1, [#sha256, null])
		selected_unit!: null | strings.MinRunes( 1)
		decision!:      "start-fresh-session" | "block"
		code!:          =~"^[A-Z0-9_]+$"
		detail!:        null | strings.MinRunes( 1)
		captured_frontier!: list.UniqueItems() & [...strings.MinRunes( 1)]
		session_budget!: close({
			captured!:    int & >=0
			current!:     int & >=0
			used_before!: int & >=0
			used_after!:  int & >=0
		})
		original_task_session_id!:   null | strings.MinRunes( 1)
		joined_owner_receipt_count!: int & >=0 & <=1
		owner_join!: matchN(1, [#ownerJoin, null])
		resumed_route_fingerprints!: list.UniqueItems() & [...#sha256]
		fresh_task_session_start_count!: int & >=0 & <=1
		fresh_task_session!: matchN(1, [#freshSession, null])
		task_session_receipt_slot!: matchN(1, [#receiptSlot, null])
		evidence_write_count!: int & >=0 & <=1
		ledger_event_ref!: matchN(1, [#exactArtifactRef, null])
		authorization_prompt_count!: 0
		recursive_resume!:           false
		mutation_count!:             0
		protected_effect_count!:     0
		authority_effect!:           "none"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#freshSession: close({
		session_id!:        =~"^task-session-[a-f0-9]{24}$"
		cursor!:            =~"^cursor-[a-f0-9]{24}$"
		selector!:          strings.MinRunes( 1)
		action!:            "task-session:execute"
		binding_id!:        strings.MinRunes( 1)
		binding_digest!:    #sha256
		route_fingerprint!: #sha256
		expected_receipt!:  strings.MinRunes( 1)
	})

	#ownerJoin: close({
		receipt_id!:        strings.MinRunes( 1)
		receipt_ref!:       #exactArtifactRef
		binding_id!:        strings.MinRunes( 1)
		binding_digest!:    #sha256
		route_fingerprint!: #sha256
	})

	#receiptSlot: close({
		unit_id!:          strings.MinRunes( 1)
		expected_receipt!: strings.MinRunes( 1)
		maximum_receipts!: 1
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

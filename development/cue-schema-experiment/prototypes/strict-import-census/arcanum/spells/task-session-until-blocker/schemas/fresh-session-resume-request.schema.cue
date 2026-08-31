// FreshSessionResumeRequest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/fresh-session-resume-request/1-0-0")
	close({
		schema_version!:            "1.0.0"
		chain_id!:                  strings.MinRunes( 1)
		loop_id!:                   strings.MinRunes( 1)
		loop_state_digest!:         #sha256
		repository_root!:           "."
		resume_state_directory!:    strings.MinRunes( 1)
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #sha256
		captured_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		selected_unit!: strings.MinRunes( 1)
		original_task_session!: close({
			session_id!: strings.MinRunes( 1)
			cursor!:     strings.MinRunes( 1)
		})
		original_guard!: #guardPair
		route_admission!: close({
			request!: {}
			receipt!: {}
		})
		owner_join!: close({
			receipt_ref!: #exactArtifactRef
			receipt!:     #ownerReceipt
		})
		reclassification!: #guardPair
		resumed_route_fingerprints!: list.UniqueItems() & [...#sha256]
		visited_task_session_ids!: list.UniqueItems() & [...strings.MinRunes( 1)]
		visited_session_cursors!: list.UniqueItems() & [...strings.MinRunes( 1)]
		task_session_receipts!: [...close({
			unit_id!:    strings.MinRunes( 1)
			session_id!: strings.MinRunes( 1)
			receipt_id!: strings.MinRunes( 1)
		})]
		session_budget!: close({
			captured_max_task_sessions!: int & >=1
			current_max_task_sessions!:  int & >=1
			task_sessions_started!:      int & >=0
		})
		authority_effect!: "none"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#guardPair: close({
		request!: {}
		receipt!: {}
	})

	#ownerReceipt: close({
		schema_version!:                "1.0.0"
		receipt_id!:                    strings.MinRunes( 1)
		result!:                        "pass" | "block"
		work_pack_id!:                  strings.MinRunes( 1)
		selected_unit!:                 strings.MinRunes( 1)
		binding_id!:                    strings.MinRunes( 1)
		binding_digest!:                #sha256
		route_fingerprint!:             #sha256
		route!:                         #route
		authorization_prompt_required!: false
		authority_effect!:              "none"
	})

	#route: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: strings.MinRunes( 1)
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

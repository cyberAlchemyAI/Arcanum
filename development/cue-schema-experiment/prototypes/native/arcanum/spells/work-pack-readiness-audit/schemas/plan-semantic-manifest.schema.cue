// PlanSemanticManifest
package prototype

import (
	"strings"
	"list"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/plan-semantic-manifest/1-0-0")
	close({
		admission_timing!: "selected-unit-at-task-session"
		allowed_routes!: [...close({
			capability!:       strings.MinRunes(1)
			effect_class!:     "repository-local-reversible"
			expected_receipt!: strings.MinRunes(1)
			frontier_swu!:     strings.MinRunes(1)
			mode!:             strings.MinRunes(1)
			required_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			route_id!: strings.MinRunes(1)
			target!:   strings.MinRunes(1)
			write_scope!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		})] & [_, ...]
		allowed_routes_digest!:     =~"^[a-f0-9]{64}$"
		approval_status!:           "unapproved"
		audit_id!:                  strings.MinRunes(1)
		authority_effect!:          "none"
		canonical_semantic_digest!: =~"^[a-f0-9]{64}$"
		completion_continuity!: close({
			authority_effect!: "none"
			completed_prefix!: list.UniqueItems() & [...close({
				canonical_successor!: strings.MinRunes(1)
				closeout_binding_id!: strings.MinRunes(1)
				completion_artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				completion_binding_id!: strings.MinRunes(1)
				continuation_cursor_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				evidence_profile!:        "task-session-joined-owner-closeout-v1"
				joined_owner_capability!: strings.MinRunes(1)
				joined_owner_receipt_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				joined_owner_result!:             "pass" | "no-op"
				owner_receipt_schema_binding_id!: strings.MinRunes(1)
				owner_receipt_schema_identity!:   strings.MinRunes(1)
				owner_receipt_schema_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				unit_contract_digest!: =~"^[a-f0-9]{64}$"
				unit_id!:              strings.MinRunes(1)
			})]
			continuity_digest!:         =~"^[a-f0-9]{64}$"
			next_unit!:                 null | strings.MinRunes(1)
			plan_epoch_id!:             =~"^epoch-[a-f0-9]{24}$"
			source_audit_id!:           strings.MinRunes(1)
			source_projection_digest!:  =~"^[a-f0-9]{64}$"
			work_pack_semantic_digest!: =~"^[a-f0-9]{64}$"
		})
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
		manifest_id!:        =~"^psm-[a-f0-9]{24}$"
		mutation_ready!:     false
		normalizer_version!: =~"^[0-9]+\\.[0-9]+\\.[0-9]+$"
		plan_epoch_id!:      =~"^epoch-[a-f0-9]{24}$"
		ready_frontier!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		runtime_admission_status!: "pending-selection"
		schema_version!:           "1.0.0"
		selected_unit!:            null
		selection_required!:       true
		semantic_component_digests!: struct.MinFields(1) & {
			[string]: =~"^[a-f0-9]{64}$"
		}
		source_snapshot_digest!: =~"^[a-f0-9]{64}$"
		unit_contract_digests!: struct.MinFields(1) & {
			[string]: =~"^[a-f0-9]{64}$"
		}
		work_pack_id!: strings.MinRunes(1)
	})

	#allowedRoute: close({
		capability!:       strings.MinRunes(1)
		effect_class!:     "repository-local-reversible"
		expected_receipt!: strings.MinRunes(1)
		frontier_swu!:     strings.MinRunes(1)
		mode!:             strings.MinRunes(1)
		required_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		route_id!: strings.MinRunes(1)
		target!:   strings.MinRunes(1)
		write_scope!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
	})

	#completedPrefixItem: close({
		canonical_successor!: strings.MinRunes(1)
		closeout_binding_id!: strings.MinRunes(1)
		completion_artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		completion_binding_id!: strings.MinRunes(1)
		continuation_cursor_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		evidence_profile!:        "task-session-joined-owner-closeout-v1"
		joined_owner_capability!: strings.MinRunes(1)
		joined_owner_receipt_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		joined_owner_result!:             "pass" | "no-op"
		owner_receipt_schema_binding_id!: strings.MinRunes(1)
		owner_receipt_schema_identity!:   strings.MinRunes(1)
		owner_receipt_schema_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		unit_contract_digest!: =~"^[a-f0-9]{64}$"
		unit_id!:              strings.MinRunes(1)
	})

	#completionContinuity: close({
		authority_effect!: "none"
		completed_prefix!: list.UniqueItems() & [...close({
			canonical_successor!: strings.MinRunes(1)
			closeout_binding_id!: strings.MinRunes(1)
			completion_artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			completion_binding_id!: strings.MinRunes(1)
			continuation_cursor_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			evidence_profile!:        "task-session-joined-owner-closeout-v1"
			joined_owner_capability!: strings.MinRunes(1)
			joined_owner_receipt_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			joined_owner_result!:             "pass" | "no-op"
			owner_receipt_schema_binding_id!: strings.MinRunes(1)
			owner_receipt_schema_identity!:   strings.MinRunes(1)
			owner_receipt_schema_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			unit_contract_digest!: =~"^[a-f0-9]{64}$"
			unit_id!:              strings.MinRunes(1)
		})]
		continuity_digest!:         =~"^[a-f0-9]{64}$"
		next_unit!:                 null | strings.MinRunes(1)
		plan_epoch_id!:             =~"^epoch-[a-f0-9]{24}$"
		source_audit_id!:           strings.MinRunes(1)
		source_projection_digest!:  =~"^[a-f0-9]{64}$"
		work_pack_semantic_digest!: =~"^[a-f0-9]{64}$"
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

	#sha256: =~"^[a-f0-9]{64}$"
}

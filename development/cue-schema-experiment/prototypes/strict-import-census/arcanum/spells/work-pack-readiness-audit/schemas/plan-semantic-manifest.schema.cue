// PlanSemanticManifest
package prototype

import (
	"strings"
	"struct"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/plan-semantic-manifest/1-0-0")
	close({
		schema_version!:            "1.0.0"
		manifest_id!:               =~"^psm-[a-f0-9]{24}$"
		audit_id!:                  strings.MinRunes( 1)
		work_pack_id!:              strings.MinRunes( 1)
		normalizer_version!:        =~"^[0-9]+\\.[0-9]+\\.[0-9]+$"
		admission_timing!:          "selected-unit-at-task-session"
		plan_epoch_id!:             =~"^epoch-[a-f0-9]{24}$"
		canonical_semantic_digest!: #sha256
		semantic_component_digests!: struct.MinFields(1) & {
			[string]: #sha256
		}
		unit_contract_digests!: struct.MinFields(1) & {
			[string]: #sha256
		}
		ready_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		source_snapshot_digest!:   #sha256
		completion_continuity!:    #completionContinuity
		approval_status!:          "unapproved"
		selection_required!:       true
		runtime_admission_status!: "pending-selection"
		allowed_routes!: [_, ...] & [...#allowedRoute]
		allowed_routes_digest!: #sha256
		execution_entry!:       #executionEntry
		authority_effect!:      "none"
		selected_unit!:         null
		mutation_ready!:        false
	})

	#allowedRoute: close({
		route_id!:     strings.MinRunes( 1)
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: "repository-local-reversible"
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#completedPrefixItem: close({
		unit_id!:                         strings.MinRunes( 1)
		unit_contract_digest!:            #sha256
		completion_binding_id!:           strings.MinRunes( 1)
		completion_artifact_ref!:         #exactArtifactRef
		closeout_binding_id!:             strings.MinRunes( 1)
		evidence_profile!:                "task-session-joined-owner-closeout-v1"
		joined_owner_capability!:         strings.MinRunes( 1)
		joined_owner_result!:             "pass" | "no-op"
		joined_owner_receipt_ref!:        #exactArtifactRef
		owner_receipt_schema_binding_id!: strings.MinRunes( 1)
		owner_receipt_schema_ref!:        #exactArtifactRef
		owner_receipt_schema_identity!:   strings.MinRunes( 1)
		continuation_cursor_ref!:         #exactArtifactRef
		canonical_successor!:             strings.MinRunes( 1)
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

	#executionEntry: close({
		entry_state!:   "selection-ready"
		selected_unit!: null
		route_id!:      null
		next_owner!: close({
			capability!: "implementation-readiness"
			mode!:       "execute"
			target!:     strings.MinRunes( 1)
		})
		blocker_code!: null
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

// WorkPackReadinessAuditConfig
package prototype

import (
	"strings"
	"list"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/config/1-0-0")
	close({
		schema_version!:    "1.0.0"
		audit_id!:          strings.MinRunes( 1)
		repository_root!:   "."
		authority_class!:   "public" | "private"
		publication_class!: "public" | "private" | "internal"
		work_pack!:         #exactArtifactRef
		control_artifacts!: list.UniqueItems() & [_, ...] & [...#exactArtifactRef]
		task_session_request_schema!: #exactArtifactRef
		terminal_receipt_schema!:     #exactArtifactRef
		terminal_receipt_semantic_validator?: matchN(1, [#exactArtifactRef, null])
		units!: [_, ...] & [...#unit]
		immutable_paths!: list.UniqueItems() & [...strings.MinRunes( 1)]
		shared_write_owners!: [...close({
			path!:  strings.MinRunes( 1)
			owner!: strings.MinRunes( 1)
			ordered_units!: list.UniqueItems() & [_, _, ...] & [...strings.MinRunes( 1)]
		})]
		source_selectors!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		closeout_directory!: close({
			path!:              strings.MinRunes( 1)
			create_if_missing!: bool
		})
		handoff_state?: close({
			artifact_ref!:    #exactArtifactRef
			expected_fields!: struct.MinFields(1)
		})
		refresh_targets!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		next_owner!: "invoke:refresh"
	})

	#attempt: close({
		required!:         bool
		id_algorithm!:     string
		collision_policy!: "fail-if-exists" | "append-only"
		retention_policy!: "retain-receipt-only" | "retain-all" | "ephemeral"
		teardown_on_success!: [...#command]
		teardown_on_failure!: [...#command]
	})

	#command: close({
		cwd!: strings.MinRunes( 1)
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		expected_exit_code!: int
		timeout_seconds!:    int & >=1
		environment!: [string]: string
		runtime_identity!: close({
			executable!:     strings.MinRunes( 1)
			version_policy!: strings.MinRunes( 1)
			hash_policy!:    strings.MinRunes( 1)
		})
		risk_class!: "read-only" | "bounded-write" | "browser" | "network" | "destructive"
	})

	#dependencyReceipt: close({
		dependency_id!:    strings.MinRunes( 1)
		receipt_ref!:      #exactArtifactRef
		expected_unit_id!: strings.MinRunes( 1)
		expected_step_id!: strings.MinRunes( 1)
		expected_status!:  "pass"
		work_pack_sha256!: =~"^[a-f0-9]{64}$"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#unit: close({
		unit_id!:                  strings.MinRunes( 1)
		task_class!:               "material-mutation" | "output-only" | "audit-only" | "read-only-validation"
		state!:                    "planned" | "complete" | "blocked"
		requested_execution_mode!: "routed-mutation" | "reusable-mutation" | "standalone-nonmutating"
		contract_kind!:            "full-task" | "row-only"
		contract_ref!:             #exactArtifactRef
		dependencies!: list.UniqueItems() & [...strings.MinRunes( 1)]
		dependency_receipts!: [...#dependencyReceipt]
		successor!:     null | strings.MinRunes(1)
		dispatch_step!: strings.MinRunes( 1)
		material_writes!: list.UniqueItems() & [...strings.MinRunes( 1)]
		execution_outputs!: list.UniqueItems() & [...strings.MinRunes( 1)]
		allowed_writes!: list.UniqueItems() & [...strings.MinRunes( 1)]
		validation_commands!: [...#command]
		attempt!: #attempt
		material_package?: matchN(1, [close({
			package_ref!: #exactArtifactRef
			receipt_ref!: #exactArtifactRef
		}), null])
		terminal_receipt!: strings.MinRunes( 1)
		closeout_receipt!: strings.MinRunes( 1)
	})
}

// InvokeMaterialPackage
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/material-package/1-0-0")
	matchN(2, [matchIf({
		mutation_state!: "materialized"
	}, {
		mutation_mode?: "apply-approved"
		source_artifacts?: null | bool | number | string | [_, ...] | {}
		changes?: null | bool | number | string | [_, ...] | {}
		target_inventory?: null | bool | number | string | [_, ...] | {}
		approval?: null | bool | number | string | [...] | {
			class?: "explicit-apply"
		}
		validation_commands?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		mutation_state!: "proposal-only"
	}, {
		mutation_mode?: "proposal-only"
		changes?: null | bool | number | string | list.MaxItems(0) | {}
		target_inventory?: null | bool | number | string | list.MaxItems(0) | {}
		dependencies?: null | bool | number | string | list.MaxItems(0) | {}
		mirror_groups?: null | bool | number | string | list.MaxItems(0) | {}
		approval?: null | bool | number | string | [...] | {
			class?: "none"
		}
		validation_commands?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		schema_version!:    "1.0.0"
		package_id!:        strings.MinRunes( 1)
		mutation_mode!:     "proposal-only" | "apply-approved"
		mutation_state!:    "proposal-only" | "materialized"
		lifecycle_owner!:   strings.MinRunes( 1)
		authority_class!:   "public" | "private"
		publication_class!: "public" | "private" | "internal"
		source_artifacts!: [...#sourceArtifact]
		changes!: [...#change]
		target_inventory!: [...#targetInventoryEntry]
		dependencies!: [...#dependency]
		mirror_groups!: [...#mirrorGroup]
		approval!: #approval
		validation_commands!: list.UniqueItems() & [...strings.MinRunes( 1)]
		plan_binding?: #planBinding
	})

	#approval: close({
		class!: "none" | "explicit-apply"
		owner!: null | strings.MinRunes( 1)
		scope_paths!: list.UniqueItems() & [...strings.MinRunes( 1)]
		authority_classes!: list.UniqueItems() & [..."public" | "private"]
		publication_classes!: list.UniqueItems() & [..."public" | "private" | "internal"]
	})

	#baselineEntry: matchN(2, [matchIf({
		state?: "absent"
	}, {
		sha256?:     null
		size_bytes?: null
	}, _) & {}, matchIf({
		state?: "present"
	}, {
		sha256?:     =~"^[a-f0-9]{64}$"
		size_bytes?: int & >=0
	}, _) & {}]) & close({
		path!:  strings.MinRunes( 1)
		state!: "absent" | "present"
		sha256!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		size_bytes!: null | int & >=0
	})

	#change: close({
		target_path!: strings.MinRunes( 1)
		operation!:   "create" | "update"
		output_ref!:  #exactArtifactRef
	})

	#dependency: close({
		dependency_id!: strings.MinRunes( 1)
		artifact_ref!:  #exactArtifactRef
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#mirrorGroup: close({
		group_id!:         strings.MinRunes( 1)
		parity!:           "exact"
		canonical_target!: strings.MinRunes( 1)
		generated_targets!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
	})

	#planBinding: close({
		task_id!:                    strings.MinRunes( 1)
		swu_id!:                     strings.MinRunes( 1)
		plan_epoch_id!:              =~"^epoch-[a-f0-9]{24}$"
		unit_contract_digest!:       =~"^[a-f0-9]{64}$"
		selection_receipt_digest!:   =~"^[a-f0-9]{64}$"
		attempt_id!:                 strings.MinRunes( 1)
		validation_contract_digest!: =~"^[a-f0-9]{64}$"
		validation_contracts!: [_, ...] & [...#structuredValidationCommand]
		target_baselines!: [_, ...] & [...#baselineEntry]
	})

	#sourceArtifact: close({
		path!:            strings.MinRunes( 1)
		sha256!:          =~"^[a-f0-9]{64}$"
		size_bytes!:      int & >=0
		authority_class!: "public" | "private"
	})

	#structuredValidationCommand: close({
		command_id!: strings.MinRunes( 1)
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		cwd!:              strings.MinRunes( 1)
		timeout_seconds!:  int & >=1 & <=86400
		max_output_bytes!: int & >=1 & <=16777216
	})

	#targetInventoryEntry: close({
		target_path!:       strings.MinRunes( 1)
		lifecycle_owner!:   strings.MinRunes( 1)
		authority_class!:   "public" | "private"
		publication_class!: "public" | "private" | "internal"
		dependency_ids!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

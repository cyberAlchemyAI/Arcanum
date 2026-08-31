// InvokeMaterialPackageReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/material-package-receipt/1-0-0")
	close({
		schemaVersion!:   "1.0.0"
		packageId!:       strings.MinRunes( 1)
		patchVerdict!:    "pass" | "reject" | "not-applicable"
		mutationHandoff!: "ready" | "gated" | "deferred" | "blocked"
		packageDigest!:   null | =~"^[a-f0-9]{64}$"
		validatedPaths!: list.UniqueItems() & [...strings.MinRunes( 1)]
		dependencyResult!:          "pass" | "reject" | "not-applicable"
		ownerBoundaryResult!:       "pass" | "reject"
		publicationBoundaryResult!: "pass" | "reject"
		validationCommands!: list.UniqueItems() & [...strings.MinRunes( 1)]
		lifecycleOwner!:   null | strings.MinRunes( 1)
		authorityClass!:   "public" | "private" | null
		publicationClass!: "public" | "private" | "internal" | null
		planBinding?: matchN(1, [#planBinding, null])
		reasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})

	#baselineEntry: close({
		path!:       strings.MinRunes( 1)
		state!:      "absent" | "present"
		sha256!:     null | =~"^[a-f0-9]{64}$"
		size_bytes!: null | int & >=0
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

	#structuredValidationCommand: close({
		command_id!: strings.MinRunes( 1)
		argv!: [_, ...] & [...strings.MinRunes( 1)]
		cwd!:              strings.MinRunes( 1)
		timeout_seconds!:  int & >=1 & <=86400
		max_output_bytes!: int & >=1 & <=16777216
	})
}

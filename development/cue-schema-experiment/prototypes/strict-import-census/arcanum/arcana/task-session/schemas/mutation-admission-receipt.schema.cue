// TaskSessionMutationAdmissionReceipt
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/mutation-admission-receipt/1-3-0")
	matchN(8, [matchIf({
		schemaVersion!: "1.3.0"
	}, {
		transientOutputs!: _
	}, matchN(0, [null | bool | number | string | [...] | {
		transientOutputs!: _
	}]) & {}) & {}, matchIf({
		admissionVerdict!: "admit"
	}, {
		mutationReady?:          true
		liveValidationRequired?: true
		reasons?: null | bool | number | string | list.MaxItems(0) | {}
		transientOutputs?: matchIf([...], [_, ...], _)
	}, _) & {}, matchIf({
		admissionProfile!: "plan-once-selected-unit"
		admissionVerdict!: "admit"
	}, {
		planEpochId!:            string
		unitContractDigest!:     #sha256
		attemptId!:              string
		planManifestDigest!:     #sha256
		selectionReceiptDigest!: #sha256
		targetBaselineDigest!:   #sha256
		targetBaselines!: [_, ...]
		validationContractDigest!: #sha256
		admissionToken!:           #sha256
		singleUse!:                true
	}, _) & {}, matchIf({
		admissionVerdict!: "block"
	}, {
		mutationReady?: false
		reasons?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		writeProfile!: "material-bound"
	}, {
		materialWrites?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		writeProfile!:     "material-bound"
		admissionVerdict!: "admit"
	}, {
		producerSchemaDigest?:  =~"^[a-f0-9]{64}$"
		materialReceiptDigest?: =~"^[a-f0-9]{64}$"
		materialPackageDigest?: =~"^[a-f0-9]{64}$"
	}, _) & {}, matchIf({
		writeProfile!: "execution-output-only"
	}, {
		producerSchemaDigest?:  null
		materialReceiptDigest?: null
		materialPackageDigest?: null
		materialWrites?: null | bool | number | string | list.MaxItems(0) | {}
		executionOutputs?: null | bool | number | string | [_, ...] | {}
		liveValidationRequired?: true
	}, _) & {}, matchIf({
		admissionVerdict!: "not-applicable"
	}, {
		executionMode?:          "standalone-nonmutating"
		writeProfile?:           "nonmutating"
		mutationReady?:          false
		liveValidationRequired?: false
		reasons?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		schemaVersion!: "1.2.0" | "1.3.0"
		admissionProfile?: matchN(1, ["plan-once-selected-unit", null])
		executionMode!:         "routed-mutation" | "reusable-mutation" | "standalone-nonmutating" | "invalid"
		writeProfile!:          "material-bound" | "execution-output-only" | "nonmutating" | "invalid"
		admissionVerdict!:      "admit" | "block" | "not-applicable"
		mutationReady!:         bool
		taskId!:                null | strings.MinRunes( 1)
		swuId!:                 null | strings.MinRunes( 1)
		requestDigest!:         null | =~"^[a-f0-9]{64}$"
		producerSchemaDigest!:  null | =~"^[a-f0-9]{64}$"
		materialReceiptDigest!: null | =~"^[a-f0-9]{64}$"
		materialPackageDigest!: null | =~"^[a-f0-9]{64}$"
		controllingPaths!: list.UniqueItems() & [...strings.MinRunes( 1)]
		dependencyIds!: list.UniqueItems() & [...strings.MinRunes( 1)]
		materialWrites!: list.UniqueItems() & [...strings.MinRunes( 1)]
		executionOutputs!: list.UniqueItems() & [...strings.MinRunes( 1)]
		transientOutputs?: list.UniqueItems() & [...strings.MinRunes( 1)]
		allowedWrites!: list.UniqueItems() & [...strings.MinRunes( 1)]
		validationCommands!: list.UniqueItems() & [...strings.MinRunes( 1)]
		lifecycleOwner!:         null | strings.MinRunes( 1)
		authorityClass!:         "public" | "private" | null
		publicationClass!:       "public" | "private" | "internal" | null
		planEpochId?:            null | =~"^epoch-[a-f0-9]{24}$"
		unitContractDigest?:     #nullableSha256
		attemptId?:              null | strings.MinRunes( 1)
		planManifestDigest?:     #nullableSha256
		selectionReceiptDigest?: #nullableSha256
		targetBaselineDigest?:   #nullableSha256
		targetBaselines?: null | [...#baselineEntry]
		validationContractDigest?: #nullableSha256
		admissionToken?:           #nullableSha256
		singleUse?:                null | bool
		liveValidationRequired!:   bool
		reasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})

	#baselineEntry: close({
		path!:      strings.MinRunes( 1)
		state!:     "absent" | "present"
		sha256!:    null | =~"^[a-f0-9]{64}$"
		sizeBytes!: null | int & >=0
	})

	#nullableSha256: matchN(1, [#sha256, null])

	#sha256: =~"^[a-f0-9]{64}$"
}

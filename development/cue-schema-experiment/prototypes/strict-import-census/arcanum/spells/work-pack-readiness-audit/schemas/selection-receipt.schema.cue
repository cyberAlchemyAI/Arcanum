// PlanSelectionReceipt
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/selection-receipt/1-0-0")
	matchN(2, [matchIf({
		selectionVerdict?: "select"
	}, {
		terminalCode?:               "SELECTION_READY"
		requestDigest?:              #sha256
		manifestDigest?:             #sha256
		planEpochId?:                string
		canonicalSemanticDigest?:    #sha256
		taskId?:                     string
		swuId?:                      string
		unitContractDigest?:         #sha256
		lifecycleEligibilityDigest?: #sha256
		selectionIntentSource?:      "execution-intent-binding" | "explicit-confirmation"
		selectionIntentDigest?:      #sha256
		reasons?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		selectionVerdict?: "block"
	}, {
		reasons?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		schemaVersion!:           "1.0.0"
		selectionVerdict!:        "select" | "block"
		terminalCode!:            =~"^[A-Z][A-Z0-9_]+$"
		requestDigest!:           #nullableSha256
		manifestDigest!:          #nullableSha256
		planEpochId!:             null | =~"^epoch-[a-f0-9]{24}$"
		canonicalSemanticDigest!: #nullableSha256
		taskId!:                  null | strings.MinRunes( 1)
		swuId!:                   null | strings.MinRunes( 1)
		unitContractDigest!:      #nullableSha256
		dependencyReceiptDigests!: list.UniqueItems() & [...#sha256]
		lifecycleEligibilityDigest!: #nullableSha256
		explicitConfirmationDigest!: #nullableSha256
		selectionIntentSource!:      "execution-intent-binding" | "explicit-confirmation" | "invalid"
		selectionIntentDigest!:      #nullableSha256
		authorityEffect!:            "none"
		mutationReady!:              false
		reasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})

	#nullableSha256: matchN(1, [#sha256, null])

	#sha256: =~"^[a-f0-9]{64}$"
}

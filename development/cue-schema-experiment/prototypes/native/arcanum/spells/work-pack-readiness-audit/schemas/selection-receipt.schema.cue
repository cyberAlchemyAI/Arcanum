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
		canonicalSemanticDigest?:    =~"^[a-f0-9]{64}$"
		lifecycleEligibilityDigest?: =~"^[a-f0-9]{64}$"
		manifestDigest?:             =~"^[a-f0-9]{64}$"
		planEpochId?:                string
		reasons?: null | bool | number | string | list.MaxItems(0) | {}
		requestDigest?:         =~"^[a-f0-9]{64}$"
		selectionIntentDigest?: =~"^[a-f0-9]{64}$"
		selectionIntentSource?: "execution-intent-binding" | "explicit-confirmation"
		swuId?:                 string
		taskId?:                string
		terminalCode?:          "SELECTION_READY"
		unitContractDigest?:    =~"^[a-f0-9]{64}$"
	}, _) & {}, matchIf({
		selectionVerdict?: "block"
	}, {
		reasons?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		authorityEffect!: "none"
		canonicalSemanticDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		dependencyReceiptDigests!: list.UniqueItems() & [...=~"^[a-f0-9]{64}$"]
		explicitConfirmationDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		lifecycleEligibilityDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		manifestDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		mutationReady!: false
		planEpochId!:   null | =~"^epoch-[a-f0-9]{24}$"
		reasons!: list.UniqueItems() & [...strings.MinRunes(1)]
		requestDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		schemaVersion!: "1.0.0"
		selectionIntentDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
		selectionIntentSource!: "execution-intent-binding" | "explicit-confirmation" | "invalid"
		selectionVerdict!:      "select" | "block"
		swuId!:                 null | strings.MinRunes(1)
		taskId!:                null | strings.MinRunes(1)
		terminalCode!:          =~"^[A-Z][A-Z0-9_]+$"
		unitContractDigest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
	})

	#nullableSha256: matchN(1, [=~"^[a-f0-9]{64}$", null])

	#sha256: =~"^[a-f0-9]{64}$"
}

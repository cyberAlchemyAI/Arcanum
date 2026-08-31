// DecisionGateOptionAdmissibilityReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/decision-gate/option-admissibility-receipt/1-0-0")
	close({
		schemaVersion!:        "1.0.0"
		decisionId!:           null | strings.MinRunes( 1)
		requestDigest!:        null | =~"^[a-f0-9]{64}$"
		routeOutcome!:         "block" | "direct" | "gate"
		decisionGateRequired!: bool
		admissibleOptionIds!: list.UniqueItems() & [...strings.MinRunes( 1)]
		presentedOptionIds!: list.UniqueItems() & [...strings.MinRunes( 1)]
		directOptionId!: null | strings.MinRunes( 1)
		ownerGate!:      null | strings.MinRunes( 1)
		rejectedOptions!: [...close({
			optionId!: strings.MinRunes( 1)
			reasons!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		})]
		reasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

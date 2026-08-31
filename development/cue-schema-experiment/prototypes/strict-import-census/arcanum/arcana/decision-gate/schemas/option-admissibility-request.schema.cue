// DecisionGateOptionAdmissibilityRequest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/decision-gate/option-admissibility-request/1-0-0")
	close({
		schemaVersion!: "1.0.0"
		decisionId!:    strings.MinRunes( 1)
		candidates!: [_, ...] & [...#candidate]
	})

	#candidate: matchN(2, [matchIf({
		structuralStatus!: "admissible"
	}, {
		evidence?: null | bool | number | string | [_, ...] | {}
		rejectionReasons?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		structuralStatus!: "inadmissible"
	}, {
		rejectionReasons?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		optionId!:         strings.MinRunes( 1)
		label!:            strings.MinRunes( 1)
		optionKind!:       "action" | "defer" | "stop"
		structuralStatus!: "admissible" | "inadmissible"
		reversibility!:    "reversible" | "irreversible"
		hazardClass!:      "reversible" | "destructive" | "authority" | "promotion" | "publication" | "spend" | "other"
		ownerGate!:        null | strings.MinRunes( 1)
		evidence!: list.UniqueItems() & [...strings.MinRunes( 1)]
		rejectionReasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

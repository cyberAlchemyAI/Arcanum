// DecisionGateOverrideConsumptionRequest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/decision-gate/override-consumption-request/1-0-0")
	close({
		schema_version!: "1.0.0"
		run_id!:         strings.MinRunes( 1)
		target!:         strings.MinRunes( 1)
		scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		hazard_class!: "reversible" | "destructive" | "authority" | "promotion" | "publication" | "spend" | "other"
	})
}

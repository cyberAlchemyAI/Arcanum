// DecisionGateOverride
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/decision-gate/override/1-0-0")
	close({
		schema_version!: "1.0.0"
		override_id!:    strings.MinRunes( 1)
		target!:         strings.MinRunes( 1)
		scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		hazard_class!:       "reversible" | "destructive" | "authority" | "promotion" | "publication" | "spend" | "other"
		issuer!:             strings.MinRunes( 1)
		rationale!:          strings.MinRunes( 1)
		issued_at!:          strings.MinRunes( 1)
		expires_at!:         null | strings.MinRunes( 1)
		owner_gate_receipt!: null | strings.MinRunes( 1)
		consumed_by!:        null | strings.MinRunes( 1)
	})
}

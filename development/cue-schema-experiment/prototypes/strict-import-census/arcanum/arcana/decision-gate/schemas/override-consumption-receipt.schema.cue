// DecisionGateOverrideConsumptionReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/decision-gate/override-consumption-receipt/1-0-0")
	close({
		schema_version!: "1.0.0"
		override_id!:    null | strings.MinRunes( 1)
		verdict!:        "consumed" | "block"
		consumed_by!:    null | strings.MinRunes( 1)
		target!:         null | strings.MinRunes( 1)
		scope!: list.UniqueItems() & [...strings.MinRunes( 1)]
		hazard_class!:           "reversible" | "destructive" | "authority" | "promotion" | "publication" | "spend" | "other" | null
		owner_gate_receipt!:     null | strings.MinRunes( 1)
		owner_route_required!:   bool
		override_digest_before!: null | =~"^[a-f0-9]{64}$"
		override_digest_after!:  null | =~"^[a-f0-9]{64}$"
		consumed_at!:            null | strings.MinRunes( 1)
		reasons!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

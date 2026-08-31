// Arcanum Continuation Route Receipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://cyberalchemy.ai/arcanum/continuation-route.schema.json")
	close({
		schema_version!: "arcanum.continuation_route.v1"
		route_id!:       strings.MinRunes(1)
		source!: close({
			capability!:          strings.MinRunes( 1)
			mode!:                strings.MinRunes( 1)
			result!:              "pass" | "block" | "flag" | "completed" | "blocked" | "flagged" | "completed_at_next_blocker"
			receipt!:             strings.MinRunes( 1)
			blocker_fingerprint!: strings.MinRunes( 1)
			legacy_adaptation?:   bool
		})
		authorization!: close({
			requested!:   bool
			exact_route!: null | string
			evidence!:    null | string
		})
		candidates!: list.MaxItems(3) & [_, ...] & [...#candidate]
		selection!: close({
			status!:         "selected" | "ambiguous" | "not-authorized" | "blocked" | "none"
			candidate_rank!: null | int & >=1 & <=3
			reason!:         strings.MinRunes( 1)
		})
		dispatch!: close({
			status!:          "not-requested" | "not-authorized" | "blocked" | "completed" | "flagged"
			runtime!:         null | string
			owner_receipt!:   null | string
			helper_closeout!: "n/a" | "pass" | "flag" | "block"
		})
		owner_boundary!: "pass" | "block"
		returned_next_route!: matchN(1, [null, close({
			capability!: strings.MinRunes( 1)
			mode!:       strings.MinRunes( 1)
			target!:     null | string
		})])
	})

	#candidate: close({
		rank!:          int & >=1 & <=3
		capability!:    strings.MinRunes( 1)
		mode!:          strings.MinRunes( 1)
		mutation_mode!: null | string
		owner!:         strings.MinRunes( 1)
		evidence!: [_, ...] & [...strings.MinRunes( 1)]
		required_inputs!: [...strings.MinRunes( 1)]
		missing_inputs!: [...strings.MinRunes( 1)]
		mutation_risk!:        "none" | "low" | "medium" | "high"
		approval_required!:    bool
		authorization_status!: "not-required" | "matched" | "missing" | "mismatch"
		expected_receipt!:     strings.MinRunes( 1)
		fallback!:             strings.MinRunes( 1)
	})
}

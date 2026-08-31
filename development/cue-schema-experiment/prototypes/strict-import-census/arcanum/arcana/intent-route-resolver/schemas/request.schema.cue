// IntentRouteRequest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/intent-route/request/1")
	close({
		schema!:     "intent-route.request@1"
		request_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"
		intent!: close({
			text!: strings.MinRunes(1) & strings.MaxRunes(8192)
			discriminators!: {
				[=~"^[A-Za-z][A-Za-z0-9._-]{0,63}$"]: _
			} & {
				[string]: #discriminator
			}
		})
		support_evidence_refs!: list.UniqueItems() & [...#evidenceRef]
		constraints!: close({
			required_capabilities!: list.UniqueItems() & [...strings.MinRunes( 1)]
			forbidden_route_ids!: list.UniqueItems() & [...strings.MinRunes( 1)]
		})
		catalog_id!:            strings.MinRunes(1) & strings.MaxRunes(128)
		catalog_digest!:        =~"^[0-9a-f]{64}$"
		supersedes_request_id?: null | =~"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"
	})

	#discriminator: matchN(2, [matchIf({
		posture?: "unresolved"
	}, {
		value?: null
	}, _) & {}, matchIf({
		posture?: "declared" | "inferred"
	}, {
		value?: matchN(0, [null])
	}, _) & {}]) & close({
		posture!: "declared" | "inferred" | "unresolved"
		value!:   #jsonScalar
	})

	#evidenceRef: close({
		artifact_ref!:   strings.MinRunes( 1)
		content_digest!: =~"^[0-9a-f]{64}$"
	})

	#jsonScalar: null | bool | int | string
}

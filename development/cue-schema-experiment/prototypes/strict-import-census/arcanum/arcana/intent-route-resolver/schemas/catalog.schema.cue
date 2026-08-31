// IntentRouteCatalog
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/intent-route/catalog/1")
	close({
		schema!:         "intent-route.catalog@1"
		catalog_id!:     strings.MinRunes(1) & strings.MaxRunes(128)
		content_digest!: =~"^[0-9a-f]{64}$"
		derived_from!: close({
			owner!:          strings.MinRunes( 1)
			revision!:       strings.MinRunes( 1)
			content_digest!: =~"^[0-9a-f]{64}$"
		})
		routes!: [_, ...] & [...#route]
	})

	#jsonScalar: bool | int | string

	#predicateMap: {
		[=~"^[A-Za-z][A-Za-z0-9._-]{0,63}$"]: _
	} & {
		[string]: #jsonScalar
	}

	#route: close({
		route_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"
		label!:    strings.MinRunes(1) & strings.MaxRunes(256)
		required!: #predicateMap
		excluded!: #predicateMap
		capabilities!: list.UniqueItems() & [...strings.MinRunes( 1)]
		dominates!: list.UniqueItems() & [...strings.MinRunes( 1)]
	})
}

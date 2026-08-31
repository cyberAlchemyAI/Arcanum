// Distill v2 Profile
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/profile/2-0-0")
	close({
		display_name!: strings.MinRunes(1)
		mode_refs!: list.UniqueItems() & [...close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})] & [_, ...]
		objection_categories!: list.UniqueItems() & [..."boundary" | "closure" | "evidence" | "evolution" | "fit" | "governance" | "recomposition" | "risk" | "scope"] & [_, ...]
		output_contract_version!: strings.MinRunes(1)
		override_policy!: close({
			allowed_fields!: list.UniqueItems() & [..."tracks" | "rounds_per_track"]
			require_within_mode_maxima!: true
		})
		profile_id!:     string
		schema_version!: "distill.profile.v2"
		technique_refs!: list.UniqueItems() & [...close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})] & [_, ...]
	})

	#override_policy: close({
		allowed_fields!: list.UniqueItems() & [..."tracks" | "rounds_per_track"]
		require_within_mode_maxima!: true
	})
}

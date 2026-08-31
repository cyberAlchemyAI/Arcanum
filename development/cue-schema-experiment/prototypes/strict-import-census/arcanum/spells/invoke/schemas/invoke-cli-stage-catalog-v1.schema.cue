// Invoke CLI Stage Catalog v1
package prototype

import (
	"struct"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/cli-stage-catalog/v1")
	close({
		$schema!:        "https://arcanum.dev/schemas/invoke/cli-stage-catalog/v1"
		schema_version!: "invoke.cli-stage-catalog.v1"
		cli_version!:    "0.5.0"
		modes!: close({
			define!:  #activeMode
			design!:  #activeMode
			plan!:    #deferredMode
			handoff!: #deferredMode
			refresh!: #deferredMode
		})
	})

	#activeMode: close({
		status!:             "active"
		native_skill_route!: ".agents/skills/invoke/SKILL.md"
		stages!: struct.MinFields(1) & {
			[string]: #stage
		}
	})

	#deferredMode: close({
		status!:             "unsupported"
		native_skill_route!: ".agents/skills/invoke/SKILL.md"
		reason!:             #nonEmpty
	})

	#derivedDigest: close({
		pointer!: #pointer
		projection!: null | list.UniqueItems() & [...#pointer]
	})

	#derivedId: close({
		pointer!: #pointer
		prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
	})

	#fixedValue: close({
		pointer!: #pointer
		value!:   _
	})

	#nonEmpty: =~".*\\S.*"

	#operation: "check" | "author" | "produce" | "admit" | "status"

	#pointer: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"

	#stage: close({
		operations!: list.UniqueItems() & [_, ...] & [...#operation]
		description!:    #nonEmpty
		next_stage!:     null | string
		request_schema!: null | string
		output_schema!:  null | string
		fixed_fields!: [...#fixedValue]
		derived_ids!: [...#derivedId]
		derived_digests!: [...#derivedDigest]
		runner!: null | string
	})
}

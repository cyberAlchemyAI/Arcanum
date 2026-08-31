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
		$schema!:     "https://arcanum.dev/schemas/invoke/cli-stage-catalog/v1"
		cli_version!: "0.5.0"
		modes!: close({
			define!: close({
				native_skill_route!: ".agents/skills/invoke/SKILL.md"
				stages!: struct.MinFields(1) & {
					[string]: close({
						derived_digests!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							projection!: null | list.UniqueItems() & [...=~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"]
						})]
						derived_ids!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
						})]
						description!: =~".*\\S.*"
						fixed_fields!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							value!:   _
						})]
						next_stage!: null | string
						operations!: list.UniqueItems() & [..."check" | "author" | "produce" | "admit" | "status"] & [_, ...]
						output_schema!:  null | string
						request_schema!: null | string
						runner!:         null | string
					})
				}
				status!: "active"
			})
			design!: close({
				native_skill_route!: ".agents/skills/invoke/SKILL.md"
				stages!: struct.MinFields(1) & {
					[string]: close({
						derived_digests!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							projection!: null | list.UniqueItems() & [...=~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"]
						})]
						derived_ids!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
						})]
						description!: =~".*\\S.*"
						fixed_fields!: [...close({
							pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
							value!:   _
						})]
						next_stage!: null | string
						operations!: list.UniqueItems() & [..."check" | "author" | "produce" | "admit" | "status"] & [_, ...]
						output_schema!:  null | string
						request_schema!: null | string
						runner!:         null | string
					})
				}
				status!: "active"
			})
			handoff!: close({
				native_skill_route!: ".agents/skills/invoke/SKILL.md"
				reason!:             =~".*\\S.*"
				status!:             "unsupported"
			})
			plan!: close({
				native_skill_route!: ".agents/skills/invoke/SKILL.md"
				reason!:             =~".*\\S.*"
				status!:             "unsupported"
			})
			refresh!: close({
				native_skill_route!: ".agents/skills/invoke/SKILL.md"
				reason!:             =~".*\\S.*"
				status!:             "unsupported"
			})
		})
		schema_version!: "invoke.cli-stage-catalog.v1"
	})

	#activeMode: close({
		native_skill_route!: ".agents/skills/invoke/SKILL.md"
		stages!: struct.MinFields(1) & {
			[string]: close({
				derived_digests!: [...close({
					pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
					projection!: null | list.UniqueItems() & [...=~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"]
				})]
				derived_ids!: [...close({
					pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
					prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
				})]
				description!: =~".*\\S.*"
				fixed_fields!: [...close({
					pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
					value!:   _
				})]
				next_stage!: null | string
				operations!: list.UniqueItems() & [..."check" | "author" | "produce" | "admit" | "status"] & [_, ...]
				output_schema!:  null | string
				request_schema!: null | string
				runner!:         null | string
			})
		}
		status!: "active"
	})

	#deferredMode: close({
		native_skill_route!: ".agents/skills/invoke/SKILL.md"
		reason!:             =~".*\\S.*"
		status!:             "unsupported"
	})

	#derivedDigest: close({
		pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
		projection!: null | list.UniqueItems() & [...=~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"]
	})

	#derivedId: close({
		pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
		prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
	})

	#fixedValue: close({
		pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
		value!:   _
	})

	#nonEmpty: =~".*\\S.*"

	#operation: "check" | "author" | "produce" | "admit" | "status"

	#pointer: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"

	#stage: close({
		derived_digests!: [...close({
			pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
			projection!: null | list.UniqueItems() & [...=~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"]
		})]
		derived_ids!: [...close({
			pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
			prefix!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
		})]
		description!: =~".*\\S.*"
		fixed_fields!: [...close({
			pointer!: =~"^/(?:[^~/]|~0|~1)+(?:/(?:[^~/]|~0|~1)+)*$"
			value!:   _
		})]
		next_stage!: null | string
		operations!: list.UniqueItems() & [..."check" | "author" | "produce" | "admit" | "status"] & [_, ...]
		output_schema!:  null | string
		request_schema!: null | string
		runner!:         null | string
	})
}

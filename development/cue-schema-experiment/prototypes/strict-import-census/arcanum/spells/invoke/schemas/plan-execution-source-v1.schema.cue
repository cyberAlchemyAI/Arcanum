// InvokePlanExecutionSourceV1
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/plan-execution-source/v1")
	close({
		schema_version!: "invoke.plan-execution-source.v1"
		source_id!:      strings.MinRunes( 1)
		work_pack!: close({
			work_pack_id!:          strings.MinRunes( 1)
			title!:                 strings.MinRunes( 1)
			objective!:             strings.MinRunes( 1)
			execution_designation!: "execution-candidate"
		})
		requested_effect!: close({
			effect_class!:    "repository-local-reversible"
			external_effect!: "none"
			publication!:     "forbidden"
			deployment!:      "forbidden"
		})
		route_contracts!: [_, ...] & [...close({
			route_id!:     strings.MinRunes( 1)
			frontier_swu!: strings.MinRunes( 1)
			capability!:   strings.MinRunes( 1)
			mode!:         strings.MinRunes( 1)
			target!:       strings.MinRunes( 1)
			write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
			effect_class!: "repository-local-reversible"
			required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
			expected_receipt!: strings.MinRunes( 1)
		})]
		wpra_config!: {}
	})
}

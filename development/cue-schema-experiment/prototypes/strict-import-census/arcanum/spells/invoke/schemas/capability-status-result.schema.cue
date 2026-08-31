// InvokeCapabilityStatusResult
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/capability-status-result/1-0-0")
	close({
		schema_version!:         "invoke.capability-status.result.v1"
		mode!:                   "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		capability_sha256!:      =~"^[a-f0-9]{64}$"
		artifact_authored!:      #artifact_axis
		registry_released!:      #boolean_axis
		mutation_runtime_ready!: #boolean_axis
	})

	#artifact_axis: matchN(2, [#common_axis, close({
		status!: "pass" | "flag" | "block" | "unsupported"
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
	})]) & {}

	#boolean_axis: matchN(2, [#common_axis, close({
		status!: bool
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
	})]) & {}

	#common_axis: {
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: _
	}
}

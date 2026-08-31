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
		artifact_authored!: matchN(2, [{
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: _
		}, close({
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: "pass" | "flag" | "block" | "unsupported"
		})])
		capability_sha256!: =~"^[a-f0-9]{64}$"
		mode!:              "define" | "design" | "plan" | "handoff" | "refresh" | "full" | "validate"
		mutation_runtime_ready!: matchN(2, [{
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: _
		}, close({
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: bool
		})])
		registry_released!: matchN(2, [{
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: _
		}, close({
			diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
			evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			status!: bool
		})])
		schema_version!: "invoke.capability-status.result.v1"
	})

	#artifact_axis: matchN(2, [{
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: _
	}, close({
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: "pass" | "flag" | "block" | "unsupported"
	})])

	#boolean_axis: matchN(2, [{
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: _
	}, close({
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: bool
	})])

	#common_axis: {
		diagnostics!: list.UniqueItems() & [...strings.MinRunes(1)]
		evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		status!: _
	}
}

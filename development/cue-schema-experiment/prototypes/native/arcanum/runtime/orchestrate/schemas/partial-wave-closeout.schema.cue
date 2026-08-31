// Native Dispatch Runner Partial-Wave Blocked Closeout
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/runtime/orchestrate/schemas/partial-wave-closeout.schema.json")
	close({
		blockers!: [...strings.MinRunes(1)] & [_, ...]
		cleaned_action_ids!: list.UniqueItems() & [...strings.MinRunes(1)]
		dependent_action_ids!:    list.MaxItems(0)
		dispatch_id!:             strings.MinRunes(1)
		event_validation_status!: "pass"
		failed_action_ids!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		run_id!:         strings.MinRunes(1)
		schema_version!: "arcanum.native-dispatch-runner.partial-wave-closeout.v0.1"
		state!:          "blocked"
		status!:         "block"
		unattempted_action_ids!: list.UniqueItems() & [...strings.MinRunes(1)]
		wave_id!: strings.MinRunes(1)
	})
}

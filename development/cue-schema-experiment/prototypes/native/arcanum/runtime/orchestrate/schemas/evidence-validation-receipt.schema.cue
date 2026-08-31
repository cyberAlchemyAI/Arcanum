// Native Dispatch Runner Evidence Validation Receipt
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/runtime/orchestrate/schemas/evidence-validation-receipt.schema.json")
	matchN(2, [matchIf({
		valid?: true
	}, {
		errors?: null | bool | number | string | list.MaxItems(0) | {}
		status?: "pass"
	}, _) & {}, matchIf({
		valid?: false
	}, {
		errors?: null | bool | number | string | [_, ...] | {}
		status?: "block"
	}, _) & {}]) & close({
		errors!: [...close({
			action_id!: null | string
			code!:      strings.MinRunes(1)
			message!:   strings.MinRunes(1)
			sequence!:  null | int & >=1
		})]
		event_count!:    int & >=0
		schema_version!: "arcanum.native-dispatch-runner.evidence-validation.v0.1"
		source!:         strings.MinRunes(1)
		status!:         "pass" | "block"
		valid!:          bool
		validator!:      "validate_run_evidence.py"
	})
}

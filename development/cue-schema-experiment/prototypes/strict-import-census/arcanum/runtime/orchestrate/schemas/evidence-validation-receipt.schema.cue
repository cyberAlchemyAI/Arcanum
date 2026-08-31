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
		status?: "pass"
		errors?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		valid?: false
	}, {
		status?: "block"
		errors?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		schema_version!: "arcanum.native-dispatch-runner.evidence-validation.v0.1"
		validator!:      "validate_run_evidence.py"
		source!:         strings.MinRunes( 1)
		event_count!:    int & >=0
		valid!:          bool
		status!:         "pass" | "block"
		errors!: [...close({
			code!:      strings.MinRunes( 1)
			sequence!:  null | int & >=1
			action_id!: null | string
			message!:   strings.MinRunes( 1)
		})]
	})
}

// Goal Staged Delta
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/staged-delta.schema.json")
	close({
		delta_id!:         string
		source_authority!: string
		target!:           string
		operation!:        "add" | "update" | "delete" | "move" | "annotate"
		framed_diff!:      string
		validation_expectation!: [...string] & [_, ...]
		promotion_state!:    "staged" | "held" | "approved" | "rejected" | "applied" | "blocked"
		created_by_receipt!: string
	})
}

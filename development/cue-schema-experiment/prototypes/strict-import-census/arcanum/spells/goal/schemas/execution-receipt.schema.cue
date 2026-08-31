// Goal Execution Receipt
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/execution-receipt.schema.json")
	close({
		receipt_id!: string
		route_id!:   string
		owner!:      string
		status!:     "closed" | "blocked" | "timed-out" | "handed-off"
		terminal!:   true
		evidence!: [...string] & [_, ...]
		files_touched?: [...string]
		validation?: [...string]
		residue?: [...string]
		reroute?: string
	})
}

// Goal Approval Token
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/approval-token.schema.json")
	close({
		token_id!:            string
		batch_id!:            string
		approver_ref?:        string
		approval_state!:      "approved" | "rejected" | "held" | "expired"
		decision_record_ref!: string
		scope!: [...string] & [_, ...]
		reuse_policy?: "single-use" | "batch-scoped"
	})
}

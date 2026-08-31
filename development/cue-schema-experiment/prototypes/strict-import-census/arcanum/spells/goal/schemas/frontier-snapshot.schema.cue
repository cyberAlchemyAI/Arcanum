// Goal Frontier Snapshot
package prototype

import "time"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/frontier-snapshot.schema.json")
	close({
		snapshot_id!:     string
		goal_context_id!: string
		source_ref!:      string
		captured_at!:     time.Time
		nodes!: [...close({
			node_id!:      string
			kind!:         string
			status!:       string
			summary!:      string
			evidence_ref?: string
		})]
		active_blockers?: [...string]
		active_gaps?: [...string]
	})
}

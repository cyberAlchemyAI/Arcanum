// Goal Telemetry Signal
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/telemetry-signal.schema.json")
	close({
		spell!:           "goal"
		goal_context_id!: string
		round_index!:     int & >=0
		frontier_size!:   int & >=0
		nodes_classified!: close({
			T0!: int & >=0
			T1!: int & >=0
			T2!: int & >=0
			T3!: int & >=0
		})
		nodes_dispatched?: int & >=0
		staged_deltas?:    int & >=0
		stop_reason!:      string
	})
}

// Goal Loop Result
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/goal/goal-loop-result.schema.json")
	close({
		spell!:            "goal"
		goal!:             string
		result!:           "PASS" | "STOP" | "BLOCK" | "FLAG"
		rounds!:           int & >=0
		decision_profile?: string
		frontier!: close({
			start!: int & >=0
			end!:   int & >=0
		})
		risk_tiers_seen!: close({
			T0!: int & >=0
			T1!: int & >=0
			T2!: int & >=0
			T3!: int & >=0
		})
		stop_reason!: string
		extra_sources?: [...string]
		next_route!: string
	})
}

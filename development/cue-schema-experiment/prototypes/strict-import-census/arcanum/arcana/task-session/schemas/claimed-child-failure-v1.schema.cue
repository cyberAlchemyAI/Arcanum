package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")

	close({
		schema_version!:          "task-session.claimed-child-failure/v1"
		stream_id!:               strings.MinRunes(1)
		child_id!:                null | string
		ordinal?:                 int & >=0
		baseline_digest?:         #sha
		partition_digest?:        #sha
		governance_digest?:       #sha
		invocation_digest?:       #sha
		execution_ticket_digest?: #sha
		request_digest?:          #sha
		completion_digest?:       #sha
		executable_digest?:       #sha
		precloseout_digest?:      #sha
		owner_closeout_digest?:   #sha
		terminal_digest?:         #sha
		predecessor_continuity_digest?: matchN(1, [#sha, null])
		continuity_digest?:     #sha
		successor_digest?:      #sha
		reconciliation_digest?: #sha
		owner?:                 string
		executable?:            string
		inputs?: [...]
		owner_joins?: [...]
		write_scope?: [...]
		output_digests?: [...]
		observed_writes?: [...]
		result?:     "pass" | "block"
		status?:     "pass" | "block"
		reason!:     string
		phase!:      string
		state?:      "pending" | "running" | "complete" | "blocked"
		join_count?: 1
		completed_prefix?: [...]
		frontier_size?:   int & >=1
		candidate_count!: 0 | 1
		candidate?:       null | string
	})

	#sha: =~"^[a-f0-9]{64}$"
}

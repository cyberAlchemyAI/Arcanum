// InvokeAcceptedStreamDriverJoinV1
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/accepted-stream-driver-join/1-0-0")
	close({
		schema_version!:          "invoke.accepted-stream-driver-join.v1"
		accepted_stream_id!:      #hash
		graph_digest!:            #hash
		epoch!:                   strings.MinRunes( 1)
		requested_effect_digest!: #hash
		authority_digest!:        #hash
		frontier_digest!:         #hash
		baseline_digest!:         #hash
		driver_identity!: close({
			executable_ref!: #exactRef
			invocation!: list.MaxItems(4) & ["python3", "arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py", "--request", "<exact-request-path>"] & [_, _, _, _, ...]
		})
		request_digest!:       #hash
		receipt_digest!:       #hash
		receipt_status!:       "complete" | "blocked"
		joined_receipt_count!: 1
		no_effect!:            bool
		join_digest!:          #hash
	})

	#exactRef: close({
		path!:   strings.MinRunes( 1)
		sha256!: #hash
	})

	#hash: =~"^[a-f0-9]{64}$"
}

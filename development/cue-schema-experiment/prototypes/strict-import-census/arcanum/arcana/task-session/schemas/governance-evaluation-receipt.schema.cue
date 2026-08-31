// TaskSessionGovernanceEvaluationReceipt
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session/governance-evaluation-receipt/1-0-0")
	matchN(4, [matchIf({
		evaluation_kind?: "series-intent"
	}, {
		outcome?: "ROUTE_TASK_SESSION_UNTIL_BLOCKER" | "CONTINUE_SINGLE_TASK_SESSION"
		allowed_outcomes?: ["CONTINUE_SINGLE_TASK_SESSION", "ROUTE_TASK_SESSION_UNTIL_BLOCKER"]
	}, _) & {}, matchIf({
		evaluation_kind?: "automatic-choice" | "closeout-preflight"
	}, {
		outcome?: "PROCEED" | "BLOCK"
		allowed_outcomes?: ["BLOCK", "PROCEED"]
	}, _) & {}, matchIf({
		evaluation_kind?: "validation"
	}, {
		outcome?: "PASS" | "FLAG" | "BLOCK"
		allowed_outcomes?: ["BLOCK", "FLAG", "PASS"]
	}, _) & {}, matchIf({
		evaluation_kind?: "closeout-sync"
	}, {
		outcome?: "PASS" | "NO_OP" | "BLOCK"
		allowed_outcomes?: ["BLOCK", "NO_OP", "PASS"]
	}, _) & {}]) & close({
		schema_version!:  "task-session.governance-evaluation-receipt.v1"
		request_id!:      strings.MinRunes(1)
		evaluation_kind!: "series-intent" | "automatic-choice" | "closeout-preflight" | "validation" | "closeout-sync"
		policy_ref!:      #exactArtifactRef
		input_sha256!:    =~"^[a-f0-9]{64}$"
		outcome!:         "PROCEED" | "PASS" | "NO_OP" | "FLAG" | "BLOCK" | "ROUTE_TASK_SESSION_UNTIL_BLOCKER" | "CONTINUE_SINGLE_TASK_SESSION"
		allowed_outcomes!: list.UniqueItems() & [_, _, ...] & [..."PROCEED" | "PASS" | "NO_OP" | "FLAG" | "BLOCK" | "ROUTE_TASK_SESSION_UNTIL_BLOCKER" | "CONTINUE_SINGLE_TASK_SESSION"]
		evaluator_sha256!: =~"^[a-f0-9]{64}$"
		diagnostics!: [...string]
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes(1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

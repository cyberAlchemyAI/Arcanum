// Task Session Continuity Cursor
//
// Repository-local selector evidence for resuming one bounded Task Session. A
// cursor is never readiness authority; the live work pack must be revalidated.
package prototype

import (
	"strings"
	"time"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/schemas/task-session-continuity-v1.json")
	close({
		schema_version!:         "task-session.continuity.v1"
		session_id!:             strings.MinRunes(1)
		updated_at!:             time.Time
		scope_root!:             strings.MinRunes(1)
		work_pack!:              strings.MinRunes(1)
		source_swu?:             null | string
		source_result!:          "PASS" | "BLOCK" | "FLAG"
		source_receipt!:         strings.MinRunes(1)
		closeout_owner_receipt?: null | string
		next_swu?:               null | string
		next_route!: matchN(1, [null, close({
			capability!: strings.MinRunes(1)
			mode!:       strings.MinRunes(1)
			target!:     strings.MinRunes(1)
			work_pack?:  string
			swu?:        null | string
		})])
		blocker_fingerprint?:    null | string
		source_receipt_profile?: "pre-execution-failure-terminalization-v1"
		owner_closeout_state?:   "unavailable-pre-execution"
		attempt_id?:             strings.MinRunes(1)
		authority_effect?:       "none"
	})
}

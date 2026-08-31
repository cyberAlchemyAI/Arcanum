// Whisper Editorial Correction Event
//
// Append-only correction event shape. State reduction and replay policy are evaluated separately.
package prototype

import (
	"time"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/spells/whisper/schemas/editorial-correction-event.schema.json")
	close({
		schema_version!:           "whisper.editorial_correction_event.v0.1"
		event_id!:                 #stableId
		event_kind!:               "operator_correction" | "reader_correction" | "false_positive_readiness"
		run_id!:                   #stableId
		invalidates_receipt!:      #stableId
		meaning_core_changed!:     bool
		related_correction_count!: int & >=0
		affected_surface_sha256!:  #sha256
		new_intent_state!:         "volatile" | "frozen"
		next_route!:               "re_audition" | "workflow_reflect" | "ordinary_revision"
		recorded_at!:              time.Time
		residue!: [...{
			code!:    #stableId
			message!: strings.MinRunes( 1)
			owner?:   strings.MinRunes( 1)
			...
		}]
	})

	#sha256: =~"^[a-f0-9]{64}$"

	#stableId: =~"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"
}

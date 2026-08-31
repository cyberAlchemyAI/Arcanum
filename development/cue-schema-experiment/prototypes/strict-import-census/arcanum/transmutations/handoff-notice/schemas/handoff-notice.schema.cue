// Handoff Notice Publish Input
package prototype

import (
	"strings"
	"time"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="urn:arcanum:handoff-notice:0.1.0")
	close({
		schema_version!: "0.1.0"
		notice_type!:    "incoming" | "outgoing" | "session-handoff" | "discussion-draft" | "resolution"
		to!:             #party
		from!:           #party
		subject!:        strings.MinRunes(1)
		project_scope!:  strings.MinRunes(1)
		status!:         "draft" | "open" | "flag" | "blocked" | "consumed" | "resolved" | "superseded"
		created_at?:     time.Time
		why_now!:        strings.MinRunes(1)
		key_points!: [_, ...] & [...strings.MinRunes(1)]
		open_calls!: [...close({
			owner!:    strings.MinRunes(1)
			question!: strings.MinRunes(1)
			status!:   "open" | "blocked" | "resolved"
		})]
		boundaries!: [_, ...] & [...strings.MinRunes(1)]
		next_actions!: [_, ...] & [...close({
			owner!:  strings.MinRunes(1)
			action!: strings.MinRunes(1)
		})]
		source_refs!: [_, ...] & [...close({
			ref!:   strings.MinRunes(1)
			label!: strings.MinRunes(1)
		})]
		next_route?: close({
			capability!:    strings.MinRunes(1)
			mode!:          strings.MinRunes(1)
			target!:        strings.MinRunes(1)
			authorization!: "not-granted"
		})
		terminal_receipt_ref?: strings.MinRunes(1)
		supersedes?:           =~"^HN-[0-9A-F]{12,64}$"
		resolution_ref?:       strings.MinRunes(1)
	})

	#party: close({
		kind!:  "person" | "role" | "future-session" | "agent" | "agent-lane" | "team" | "owner-route" | "any"
		label!: strings.MinRunes(1)
	})
}

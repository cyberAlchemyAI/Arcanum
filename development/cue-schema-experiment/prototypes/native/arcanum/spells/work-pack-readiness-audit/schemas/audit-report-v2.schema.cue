// WorkPackReadinessAuditReportV2
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/report/2-0-0")
	matchN(4, [matchIf({
		admission_timing!: "selected-unit-at-task-session"
	}, {
		execution_entry!: _
	}, _) & {}, matchIf({
		execution_entry!: null | bool | number | string | [...] | {
			entry_state!: "owner-prerequisite"
		}
	}, {
		execution_entry?: null | bool | number | string | [...] | {
			blocker_code?: null
			next_owner?: null | bool | number | string | [...] | {
				capability?: "invoke"
				mode?:       "refresh"
			}
			route_id?:      string
			selected_unit?: string
		}
	}, _) & {}, matchIf({
		verdict!: "block"
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
		manifest?: null
	}, _) & {}, matchIf({
		verdict!: "pass" | "flag"
	}, {
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		manifest?: {}
	}, _) & {}]) & close({
		admission_timing?:        "full-frontier" | "selected-unit-at-task-session"
		audit_id!:                strings.MinRunes(1)
		audit_projection_digest!: null | =~"^[a-f0-9]{64}$"
		authority_effect!:        "none"
		blockers!: [...close({
			binding_id!: strings.MinRunes(1)
			claim!:      strings.MinRunes(1)
			code!:       =~"^[A-Z][A-Z0-9_]+$"
		})]
		canonical_semantic_digest!:    null | =~"^[a-f0-9]{64}$"
		canonical_spell_id!:           "work-pack-readiness-audit"
		configured_commands_executed!: false
		evidence_ceiling!:             "frozen-input-contractual-readiness"
		execution_entry?: close({
			blocker_code!: null | strings.MinRunes(1)
			entry_state!:  "selection-ready" | "owner-prerequisite" | "blocked"
			next_owner!: close({
				capability!: "implementation-readiness" | "invoke"
				mode!:       "execute" | "refresh"
				target!:     strings.MinRunes(1)
			})
			route_id!:      null | strings.MinRunes(1)
			selected_unit!: null | strings.MinRunes(1)
		})
		flags!: list.UniqueItems() & [..."observability-residue"]
		manifest!: null | {}
		mutation_ready!:           false
		next_owner!:               strings.MinRunes(1)
		runtime_admission_status?: "pending-selection" | "pass" | "flag" | "block"
		schema_version!:           "2.0.0"
		selected_unit!:            null
		semantic_component_digests!: [string]: =~"^[a-f0-9]{64}$"
		source_snapshot!: close({
			artifact_count!: int & >=0
			digest!:         =~"^[a-f0-9]{64}$"
			drift!:          bool
		})
		terminal_code!: =~"^[A-Z][A-Z0-9_]+$"
		verdict!:       "pass" | "flag" | "block"
	})
}

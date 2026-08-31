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
			selected_unit?: string
			route_id?:      string
			next_owner?: null | bool | number | string | [...] | {
				capability?: "invoke"
				mode?:       "refresh"
			}
			blocker_code?: null
		}
	}, _) & {}, matchIf({
		verdict!: "block"
	}, {
		manifest?: null
		blockers?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		verdict!: "pass" | "flag"
	}, {
		manifest?: {}
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		schema_version!:     "2.0.0"
		admission_timing?:   "full-frontier" | "selected-unit-at-task-session"
		audit_id!:           strings.MinRunes( 1)
		canonical_spell_id!: "work-pack-readiness-audit"
		verdict!:            "pass" | "flag" | "block"
		terminal_code!:      =~"^[A-Z][A-Z0-9_]+$"
		evidence_ceiling!:   "frozen-input-contractual-readiness"
		manifest!: null | {}
		blockers!: [...close({
			code!:       =~"^[A-Z][A-Z0-9_]+$"
			binding_id!: strings.MinRunes( 1)
			claim!:      strings.MinRunes( 1)
		})]
		flags!: list.UniqueItems() & [..."observability-residue"]
		source_snapshot!: close({
			digest!:         =~"^[a-f0-9]{64}$"
			artifact_count!: int & >=0
			drift!:          bool
		})
		semantic_component_digests!: [string]: =~"^[a-f0-9]{64}$"
		canonical_semantic_digest!:    null | =~"^[a-f0-9]{64}$"
		audit_projection_digest!:      null | =~"^[a-f0-9]{64}$"
		configured_commands_executed!: false
		selected_unit!:                null
		authority_effect!:             "none"
		mutation_ready!:               false
		runtime_admission_status?:     "pending-selection" | "pass" | "flag" | "block"
		execution_entry?: close({
			entry_state!:   "selection-ready" | "owner-prerequisite" | "blocked"
			selected_unit!: null | strings.MinRunes( 1)
			route_id!:      null | strings.MinRunes( 1)
			next_owner!: close({
				capability!: "implementation-readiness" | "invoke"
				mode!:       "execute" | "refresh"
				target!:     strings.MinRunes( 1)
			})
			blocker_code!: null | strings.MinRunes( 1)
		})
		next_owner!: strings.MinRunes( 1)
	})
}

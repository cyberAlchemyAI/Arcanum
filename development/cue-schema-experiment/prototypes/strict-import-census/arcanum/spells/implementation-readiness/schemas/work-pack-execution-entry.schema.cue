// InvokeAuthoredWorkPackExecutionEntry
package prototype

import (
	"strings"
	"list"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/work-pack-execution-entry/1-0-0")
	close({
		schema_version!:   "arcanum.work-pack-execution-entry/v1"
		work_pack_id!:     strings.MinRunes( 1)
		admission_timing!: "full-frontier" | "selected-unit-at-task-session"
		frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		execution_policy!: #executionPolicy
		execution_entry!:  #executionEntry
		pre_execution_owner_prerequisite!: matchN(1, [null, struct.MinFields( 1)])
		continuation_rule!: strings.MinRunes( 1)
		authority_effect!:  "none"
	})

	#allowedRoute: close({
		route_id!:     =~"^[A-Za-z0-9._:-]+$"
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: "repository-local-reversible"
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#declaredRetry: close({
		max!:                    1
		only_after!:             "REPAIRABLE_OWNER_CONDITION"
		same_route_and_binding!: true
	})

	#executionEntry: close({
		state!:         "selection-ready" | "owner-prerequisite" | "task-ready" | "blocked"
		selected_unit!: null | strings.MinRunes( 1)
		route_id!:      null | strings.MinRunes( 1)
		next_owner!:    null | strings.MinRunes( 1)
	})

	#executionPolicy: close({
		route_policy!: "automatic-in-scope"
		allowed_routes!: [_, ...] & [...#allowedRoute]
		allowed_routes_digest!: #sha256
		digest_algorithm!:      "sha256 of RFC8785-compatible canonical JSON for allowed_routes"
		automatic_decisions!: list.UniqueItems() & [_, ...] & [..."internal-tool-selection" | "capability-owner-routing" | "reversible-local-default" | "declared-fallback" | "declared-retry" | "fresh-task-session-resumption"]
		stop_decisions!: list.UniqueItems() & [_, ...] & [..."product-or-semantic-choice" | "scope-expansion" | "destructive-or-irreversible-effect" | "credentials-or-secret-access" | "external-message-or-network-effect" | "cost-policy-or-risk-acceptance" | "authority-promotion-publication-deployment" | "failed-acceptance-critical-validation"]
		scope_source!:      "exact-work-pack-and-captured-frontier"
		validation_policy!: "owner-gates-remain-mandatory"
		declared_retry?:    #declaredRetry
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

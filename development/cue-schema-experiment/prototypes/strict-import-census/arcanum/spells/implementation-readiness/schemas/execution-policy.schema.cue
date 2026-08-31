// WorkPackExecutionPolicy
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/implementation-readiness/execution-policy/1-1-0")
	matchIf({
		schema_version!: "1.1.0"
	}, {
		completion_continuity!: _
	}, _) & {} & close({
		schema_version!:            "1.0.0" | "1.1.0"
		work_pack_id!:              strings.MinRunes( 1)
		work_pack_semantic_digest!: #sha256
		frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		completion_continuity?: #completionContinuity
		allowed_routes!: [_, ...] & [...#allowedRoute]
		allowed_routes_digest!: #sha256
		automatic_decisions!: list.UniqueItems() & [_, ...] & [..."internal-tool-selection" | "capability-owner-routing" | "reversible-local-default" | "declared-fallback" | "declared-retry" | "fresh-task-session-resumption"]
		stop_decisions!: list.UniqueItems() & [_, ...] & [..."product-or-semantic-choice" | "scope-expansion" | "destructive-or-irreversible-effect" | "credentials-or-secret-access" | "external-message-or-network-effect" | "cost-policy-or-risk-acceptance" | "authority-promotion-publication-deployment" | "failed-acceptance-critical-validation"]
		validation_commands!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		scope_source!:      "exact-work-pack-and-captured-frontier"
		validation_policy!: "owner-gates-remain-mandatory"
		authority_effect!:  "none"
	})

	#allowedRoute: close({
		route_id!:     =~"^[A-Za-z0-9._:-]+$"
		frontier_swu!: strings.MinRunes( 1)
		capability!:   strings.MinRunes( 1)
		mode!:         strings.MinRunes( 1)
		target!:       strings.MinRunes( 1)
		write_scope!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		effect_class!: "repository-local-reversible" | "destructive-or-irreversible" | "external-network-or-message" | "authority-or-promotion" | "publication-or-deployment"
		required_inputs!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		expected_receipt!: strings.MinRunes( 1)
	})

	#completedPrefixItem: close({
		unit_id!:                 strings.MinRunes( 1)
		unit_contract_digest!:    #sha256
		completion_binding_id!:   strings.MinRunes( 1)
		completion_artifact_ref!: #exactArtifactRef
		closeout_binding_id!:     strings.MinRunes( 1)
	})

	#completionContinuity: close({
		source_audit_id!:           strings.MinRunes( 1)
		source_projection_digest!:  #sha256
		work_pack_semantic_digest!: #sha256
		plan_epoch_id!:             =~"^epoch-[a-f0-9]{24}$"
		completed_prefix!: list.UniqueItems() & [...#completedPrefixItem]
		next_unit!:         null | strings.MinRunes( 1)
		authority_effect!:  "none"
		continuity_digest!: #sha256
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     #sha256
		size_bytes!: int & >=0
	})

	#sha256: =~"^[a-f0-9]{64}$"
}

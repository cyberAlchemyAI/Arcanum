// ObjectiveExecutionManifest
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/objective-execution-manifest/1-0-0")
	close({
		schema_version!:     "1.0.0"
		manifest_id!:        =~"^oem-[a-f0-9]{24}$"
		evidence_ceiling!:   "frozen-input-contractual-readiness"
		classifier_version!: strings.MinRunes( 1)
		objective_ref!: {}
		closure_receipt_refs!: [_, ...]
		authority_bindings!: {
			canonical_authority_refs!: _
			derived_projection_refs!:  _
			execution_byte_baselines!: _
			semantic_bindings!:        _
		}
		canonical_plan_graph!: close({
			units!: [_, ...]
			finite_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		})
		execution_bindings!: [_, ...]
		receipt_bindings!: {}
		closeout_bindings!: [_, ...]
		runtime_binding!: {}
		status_receipt_refs!: {}
		lifecycle_status_refs!: {}
		epoch_binding!: close({
			epoch_id!:                  =~"^epoch-[a-f0-9]{24}$"
			audit_projection_digest!:   =~"^[a-f0-9]{64}$"
			canonical_semantic_digest!: =~"^[a-f0-9]{64}$"
			source_snapshot_digest!:    =~"^[a-f0-9]{64}$"
			approved_frontier_ref!: [_, ...]
			run_budget!: {}
			risk_policy_ref!: {}
			decision_gate_approval_receipt_ref!: {}
			approval_status!: "unapproved"
		})
		continuity_projection!: {}
		semantic_component_digests!: [string]: =~"^[a-f0-9]{64}$"
		authority_effect!: "none"
		selected_unit!:    null
		mutation_ready!:   false
	})
}

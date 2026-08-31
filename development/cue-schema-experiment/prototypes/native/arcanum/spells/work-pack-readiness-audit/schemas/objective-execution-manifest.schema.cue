// ObjectiveExecutionManifest
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/objective-execution-manifest/1-0-0")
	close({
		authority_bindings!: {
			canonical_authority_refs!: _
			derived_projection_refs!:  _
			execution_byte_baselines!: _
			semantic_bindings!:        _
		}
		authority_effect!: "none"
		canonical_plan_graph!: close({
			finite_frontier!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			units!: [_, ...]
		})
		classifier_version!: strings.MinRunes(1)
		closeout_bindings!: [_, ...]
		closure_receipt_refs!: [_, ...]
		continuity_projection!: {}
		epoch_binding!: close({
			approval_status!: "unapproved"
			approved_frontier_ref!: [_, ...]
			audit_projection_digest!:   =~"^[a-f0-9]{64}$"
			canonical_semantic_digest!: =~"^[a-f0-9]{64}$"
			decision_gate_approval_receipt_ref!: {}
			epoch_id!: =~"^epoch-[a-f0-9]{24}$"
			risk_policy_ref!: {}
			run_budget!: {}
			source_snapshot_digest!: =~"^[a-f0-9]{64}$"
		})
		evidence_ceiling!: "frozen-input-contractual-readiness"
		execution_bindings!: [_, ...]
		lifecycle_status_refs!: {}
		manifest_id!:    =~"^oem-[a-f0-9]{24}$"
		mutation_ready!: false
		objective_ref!: {}
		receipt_bindings!: {}
		runtime_binding!: {}
		schema_version!: "1.0.0"
		selected_unit!:  null
		semantic_component_digests!: [string]: =~"^[a-f0-9]{64}$"
		status_receipt_refs!: {}
	})
}

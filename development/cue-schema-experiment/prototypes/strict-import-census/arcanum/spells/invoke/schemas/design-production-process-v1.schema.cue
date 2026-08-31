// Invoke Design Production Process v1
//
// Machine contract for the ordered, authority-free Invoke Design production process.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-production-process/v1")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-production-process/v1"
		schema_version!:   "invoke.design-production-process.v1"
		process_id!:       #id
		owner_capability!: "invoke"
		mode!:             "design"
		artifact_chain!: list.MaxItems(19) & ["define-stage-receipt", "design-input-boundary-approval", "design-input-closure", "design-input-closure-receipt", "design-scope-manifest", "design-denominator-receipt", "design-selection-result", "design-input-production-receipt", "design-profile", "design-source", "design-artifact-staged", "design-coherence-receipt", "design-candidate-production-receipt", "design-bundle-closure", "distill-execution-evidence", "deterministic-views", "design-stage-receipt-v2", "design-bundle-admission-receipt", "capability-artifact-admission"] & [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ...]
		stages!: [_, ...] & [...#stage]
		transitions!: [_, ...] & [...#transition]
		compatibility!: close({
			historical_evidence!: "read-only"
			new_pass_requires!:   "invoke.design-stage-receipt.v2 plus invoke.design-bundle-admission-receipt.v1"
			supersession_policy!: "restart-from-earliest-changed-binding"
		})
		evidence_ceiling!: close({
			artifact_authored!:      bool
			plan_evidence!:          false
			registry_released!:      false
			mutation_runtime_ready!: false
			acceptance!:             false
			execution!:              false
			publication!:            false
			deployment!:             false
			external_effect!:        false
		})
		authority_effect!: "none"
		process_digest!:   #digest
	})

	#digest: =~"^[a-f0-9]{64}$"

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#nonEmpty: =~".*\\S.*"

	#stage: close({
		stage_id!:         #id
		owner!:            #id
		input_kinds!:      #stringSet
		output_kinds!:     #stringSet
		entry_gate!:       #nonEmpty
		exit_gate!:        #nonEmpty
		failure_state!:    #id
		authority_effect!: "none"
	})

	#stringSet: list.UniqueItems() & [_, ...] & [...#nonEmpty]

	#transition: close({
		from!:       #id
		to!:         #id
		condition!:  #nonEmpty
		on_failure!: #id
	})
}

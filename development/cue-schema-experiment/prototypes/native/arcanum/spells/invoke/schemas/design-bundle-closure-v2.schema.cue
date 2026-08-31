// Invoke Design Bundle Closure v2
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-bundle-closure/v2")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-bundle-closure/v2"
		authority_effect!: "none"
		candidate_receipt_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		closure_digest!: =~"^[a-f0-9]{64}$"
		closure_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		distill_evidence!: close({
			events_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			execution_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			request_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			validation_result_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		output_contracts!: close({
			architecture!:         "ARCHITECTURE.md"
			coherence_receipt!:    "DESIGN-COHERENCE-RECEIPT.json"
			denominator_receipt!:  "DESIGN-DENOMINATOR-RECEIPT.json"
			design_artifact!:      "DESIGN.json"
			dispatch_trace!:       "DISPATCH-TRACE.json"
			distill!:              "DISTILL-RECEIPT.json"
			glossary_consistency!: "GLOSSARY-CONSISTENCY-REPORT.json"
			layering!:             "IMPLEMENTATION-LAYERING.md"
			planned_witnesses!:    "PLANNED-WITNESS-CONTRACTS.json"
			scope_manifest!:       "DESIGN-SCOPE-MANIFEST.json"
			selected_companions!:  "SELECTED-COMPANIONS.md"
			selection_result!:     "DESIGN-SELECTION-RESULT.json"
			stage_receipt!:        "INVOKE-DESIGN-STAGE-RECEIPT.json"
			template_selection!:   "TEMPLATE-SELECTION-RECEIPT.json"
			transport!:            "DESIGN-TRANSPORT-REPORT.json"
		})
		schema_version!: "invoke.design-bundle-closure.v2"
		target_id!:      =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})
}

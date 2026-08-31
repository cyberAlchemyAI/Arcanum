// Invoke Design Stage Receipt v3
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-result/v3")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-result/v3"
		activation_kind!:  "normal"
		authority_effect!: "none"
		bindings!: close({
			bundle_closure_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			candidate_production_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			coherence_policy_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			coherence_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			design_artifact_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			design_source_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
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
			process_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			profile_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			w1_production_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		coherence_state!: "pass"
		distill_state!:   "pass"
		evidence_ceiling!: close({
			acceptance!:             false
			artifact_authored!:      true
			coherence_validated!:    true
			deployment!:             false
			design_stage_pass!:      true
			execution!:              false
			external_effect!:        false
			human_views_produced!:   true
			mutation_runtime_ready!: false
			plan_evidence!:          false
			publication!:            false
			registry_released!:      false
		})
		evidence_state!:    "design-stage-pass"
		human_views_state!: "pass"
		mode!:              "design"
		next_route!:        "plan" | "spellcraft" | "sigil-development" | "deferred"
		outputs!: list.MaxItems(14) & [matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "design-artifact"
			path?: "DESIGN.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "architecture"
			path?: "ARCHITECTURE.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "selected-companions"
			path?: "SELECTED-COMPANIONS.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "glossary-consistency"
			path?: "GLOSSARY-CONSISTENCY-REPORT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "planned-witnesses"
			path?: "PLANNED-WITNESS-CONTRACTS.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "layering"
			path?: "IMPLEMENTATION-LAYERING.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "template-selection"
			path?: "TEMPLATE-SELECTION-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "dispatch-trace"
			path?: "DISPATCH-TRACE.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "distill"
			path?: "DISTILL-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "scope-manifest"
			path?: "DESIGN-SCOPE-MANIFEST.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "denominator-receipt"
			path?: "DESIGN-DENOMINATOR-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "selection-result"
			path?: "DESIGN-SELECTION-RESULT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "coherence-receipt"
			path?: "DESIGN-COHERENCE-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "transport"
			path?: "DESIGN-TRANSPORT-REPORT.json"
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, _, _, ...]
		owner_capability!:    "invoke"
		plan_evidence_state!: "plan-evidence-pending"
		producer!: close({
			identity!: "invoke.compile-design-source.v3"
			owner!:    "invoke-design-producer"
			path!:     "arcanum/spells/invoke/scripts/compile_design_source_v3.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		profile_id!:               "invoke.generic-design-baseline.v1"
		receipt_digest!:           =~"^[a-f0-9]{64}$"
		receipt_id!:               =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		result!:                   "pass"
		schema_version!:           "invoke.design-stage-receipt.v3"
		selection_evidence_state!: "design-validator-pass"
		target_id!:                =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})
}

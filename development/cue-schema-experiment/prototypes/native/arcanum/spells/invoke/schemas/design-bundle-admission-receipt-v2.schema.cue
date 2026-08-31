// Invoke Design Bundle Admission Receipt v2
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2")
	matchIf({
		result!: "pass"
	}, {
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		checks?: null | bool | number | string | [...null | bool | number | string | [...] | {
			status?: "pass"
		}] | {}
		evidence_ceiling?: null | bool | number | string | [...] | {
			artifact_authored?: true
		}
		replay?: null | bool | number | string | [...] | {
			comparison?: "pass"
			differences?: null | bool | number | string | list.MaxItems(0) | {}
		}
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
		checks?: null | bool | number | string | list.MatchN(>=1, {
			status!: "block"
		}) | {}
		evidence_ceiling?: null | bool | number | string | [...] | {
			artifact_authored?: false
		}
	}) & {} & close({
		$schema!:          "https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2"
		authority_effect!: "none"
		blockers!: [...close({
			blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			check_id!:     "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			code!:         "STAGE_RECEIPT_INVALID" | "PRODUCER_IDENTITY_MISMATCH" | "BUNDLE_CLOSURE_BINDING_MISMATCH" | "OUTPUT_INVENTORY_MISMATCH" | "PROJECTION_REPLAY_MISMATCH" | "DISTILL_EVIDENCE_INVALID" | "AUTHORITY_CEILING_INVALID" | "REFERENCE_UNAVAILABLE" | "REFERENCE_DIGEST_MISMATCH"
			message!:      strings.MinRunes(1)
			repair_route!: "repair-design-bundle" | "repair-installed-contract" | "repair-distill-evidence" | "recompile-design-bundle"
			selector!:     null | string
		})]
		bundle_root!: string
		checks!: list.MaxItems(7) & [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "stage-receipt-validation"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "producer-identity"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "bundle-closure-binding"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "output-inventory"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "projection-replay"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "distill-evidence"
		}]), matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}) & {} & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: "stage-receipt-validation" | "producer-identity" | "bundle-closure-binding" | "output-inventory" | "projection-replay" | "distill-evidence" | "authority-ceiling"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "authority-ceiling"
		}])] & [_, _, _, _, _, _, _, ...]
		evidence_ceiling!: close({
			acceptance!:             false
			artifact_authored!:      bool
			deployment!:             false
			execution!:              false
			external_effect!:        false
			mutation_runtime_ready!: false
			publication!:            false
			registry_released!:      false
		})
		output_inventory!: list.MaxItems(15) & [matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "design-artifact"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "architecture"
			path?: null | bool | number | =~"^(?:[^/]+/)*ARCHITECTURE\\.md$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "selected-companions"
			path?: null | bool | number | =~"^(?:[^/]+/)*SELECTED-COMPANIONS\\.md$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "glossary-consistency"
			path?: null | bool | number | =~"^(?:[^/]+/)*GLOSSARY-CONSISTENCY-REPORT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "planned-witnesses"
			path?: null | bool | number | =~"^(?:[^/]+/)*PLANNED-WITNESS-CONTRACTS\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "layering"
			path?: null | bool | number | =~"^(?:[^/]+/)*IMPLEMENTATION-LAYERING\\.md$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "template-selection"
			path?: null | bool | number | =~"^(?:[^/]+/)*TEMPLATE-SELECTION-RECEIPT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "dispatch-trace"
			path?: null | bool | number | =~"^(?:[^/]+/)*DISPATCH-TRACE\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "distill"
			path?: null | bool | number | =~"^(?:[^/]+/)*DISTILL-RECEIPT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "scope-manifest"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN-SCOPE-MANIFEST\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "denominator-receipt"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN-DENOMINATOR-RECEIPT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "selection-result"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN-SELECTION-RESULT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "coherence-receipt"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN-COHERENCE-RECEIPT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "transport"
			path?: null | bool | number | =~"^(?:[^/]+/)*DESIGN-TRANSPORT-REPORT\\.json$" | [...] | {}
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "stage-receipt"
			path?: null | bool | number | =~"^(?:[^/]+/)*INVOKE-DESIGN-STAGE-RECEIPT\\.json$" | [...] | {}
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, ...]
		producer_binding!: close({
			producer!: close({
				identity!: "invoke.compile-design-source.v3"
				owner!:    "invoke-design-producer"
				path!:     "arcanum/spells/invoke/scripts/compile_design_source_v3.py"
				sha256!:   =~"^[a-f0-9]{64}$"
			})
			profile_id!:     "invoke.generic-design-baseline.v1"
			receipt_digest!: =~"^[a-f0-9]{64}$"
			receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		replay!: close({
			bundle_closure_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			candidate_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			comparison!: "pass" | "block" | "not-evaluable"
			differences!: [...close({
				expected!: null | int | string
				kind!:     "missing" | "unexpected" | "digest-mismatch" | "size-mismatch" | "schema-mismatch" | "content-mismatch"
				observed!: null | int | string
				path!:     string
			})]
			output_inventory_digest!: =~"^[a-f0-9]{64}$"
		})
		result!:         "pass" | "block"
		schema_version!: "invoke.design-bundle-admission-receipt.v2"
		stage_receipt_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		validator!: close({
			identity!: "invoke.validate-design-bundle-admission.v2"
			owner!:    "invoke-design-bundle-admission-validator"
			path!:     "arcanum/spells/invoke/scripts/validate_design_bundle_admission_v2.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
	})
}

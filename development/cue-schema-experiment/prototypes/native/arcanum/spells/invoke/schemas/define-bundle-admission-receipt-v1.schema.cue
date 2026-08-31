// Invoke Define v3 Bundle Admission Receipt v1
//
// Point-in-time admission evidence for one exact Define v3 bundle. It records
// clean replay parity and typed semantic-drift classification without granting
// registry, mutation, publication, or promotion authority.
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-bundle-admission-receipt/v1")
	matchIf({
		result?: "pass"
	}, {
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		checks?: null | bool | number | string | [null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, null | bool | number | string | [...] | {
			status?: "pass"
		}, ...] | {}
		drift_analysis?: null | bool | number | string | [...] | {
			compile_window?: "current"
			summary?: null | bool | number | string | [...] | {
				authority_state?:  "unchanged"
				evidence_state?:   "current"
				overall?:          "current"
				projection_state?: "unchanged"
				semantic_state?:   "unchanged"
				topology_state?:   "unchanged"
			}
		}
		output_inventory?: null | bool | number | string | list.MaxItems(13) & [_, _, _, _, _, _, _, _, _, _, _, _, _, ...] | {}
		producer_binding?: close({
			producer!: close({
				identity!: "invoke.compile-define-source.v3"
				path!:     "arcanum/spells/invoke/scripts/compile_define_source_v3.py"
				sha256!:   =~"^[a-f0-9]{64}$"
			})
			profile_id!:     "invoke.generic-definitions-baseline.v3"
			receipt_digest!: =~"^[a-f0-9]{64}$"
			receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		})
		replay?: null | bool | number | string | [...] | {
			clean_bundle_digest?: =~"^[a-f0-9]{64}$"
			comparison?:          "pass"
			source_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		}
		stage_receipt_ref?: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
	}, _) & {} & close({
		$schema!:          "https://arcanum.dev/schemas/invoke/define-bundle-admission-receipt/v1"
		authority_effect!: "none"
		blockers!: list.UniqueItems() & [...close({
			caused_by!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"]
			code!:    =~"^[A-Z][A-Z0-9_]{2,95}$"
			message!: strings.MinRunes(1)
		})]
		bundle_digest!: =~"^[a-f0-9]{64}$"
		bundle_root!:   string
		checks!: list.MaxItems(13) & list.UniqueItems() & [matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:bundle-shape"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:stage-receipt"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:producer-identity"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:schema-bindings"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:ordered-inventory"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:semantic-closure"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:clean-replay"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:definitions"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:generated-views"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:structural-schemas"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:semantic-outcome"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:authority-effect"
		}]), matchN(2, [close({
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			detail!:   strings.MinRunes(1)
			status!:   "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:prior-admission"
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, _, ...]
		drift_analysis!: close({
			compile_window!: "current" | "changed" | "not_evaluable"
			differences!: list.UniqueItems() & [...close({
				after_ref!: matchN(1, [close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				}), null])
				before_ref!: matchN(1, [close({
					path!:   string
					sha256!: =~"^[a-f0-9]{64}$"
					size!:   int & >=0
				}), null])
				category!: "source_evidence" | "selector" | "label_alias" | "definition_meaning" | "boundary" | "relation" | "semantic_application" | "authority" | "registry_topology" | "consumer_topology" | "structural_schema" | "identity_denominator" | "generated_projection" | "bundle_inventory"
				change!:   "added" | "removed" | "modified" | "missing" | "not_evaluable"
				drift_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
				invalidates!: list.UniqueItems() & [..."semantic_context" | "semantic_closure" | "define_source" | "bundle" | "admission" | "artifact_pass"] & [_, ...]
				locator!:         strings.MinRunes(1)
				repair_route!:    "recompile" | "rerun_semantic_closure" | "reauthor_define_source" | "definitions_governance" | "identity_denominator" | "stop"
				semantic_effect!: "none" | "meaning_changed" | "authority_changed" | "topology_changed" | "review_required" | "not_evaluable"
			})]
			prior_admission!: "not_provided" | "current" | "changed" | "not_evaluable"
			summary!: close({
				authority_state!:  "unchanged" | "changed" | "unresolved" | "not_evaluable"
				evidence_state!:   "current" | "stale" | "missing" | "not_evaluable"
				overall!:          "current" | "recompile_required" | "closure_refresh_required" | "semantic_reassessment_required" | "blocked"
				projection_state!: "unchanged" | "changed" | "not_evaluable"
				semantic_state!:   "unchanged" | "changed" | "review_required" | "not_evaluable"
				topology_state!:   "unchanged" | "changed" | "not_evaluable"
			})
		})
		output_inventory!: [...close({
			kind!:   strings.MinRunes(1)
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		producer_binding!: matchN(1, [close({
			producer!: close({
				identity!: "invoke.compile-define-source.v3"
				path!:     "arcanum/spells/invoke/scripts/compile_define_source_v3.py"
				sha256!:   =~"^[a-f0-9]{64}$"
			})
			profile_id!:     "invoke.generic-definitions-baseline.v3"
			receipt_digest!: =~"^[a-f0-9]{64}$"
			receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		}), null])
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		replay!: close({
			clean_bundle_digest!: matchN(1, [=~"^[a-f0-9]{64}$", null])
			comparison!: "pass" | "block" | "not_evaluable"
			discovery_roots!: list.UniqueItems() & [...string]
			public_roots!: list.UniqueItems() & [...string]
			source_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
		})
		result!: "pass" | "block"
		schema_bindings!: close({
			admission_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			closure_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			context_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			definitions_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			result_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		schema_version!: "invoke.define-bundle-admission-receipt.v1"
		stage_receipt_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		structural_schema_refs!: list.UniqueItems() & [...close({
			definition_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			path!:          string
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
		})]
		validator!: close({
			identity!: "invoke.validate-define-bundle-admission.v1"
			path!:     "arcanum/spells/invoke/scripts/validate_define_bundle_admission.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
	})

	#blocker: close({
		caused_by!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"]
		code!:    =~"^[A-Z][A-Z0-9_]{2,95}$"
		message!: strings.MinRunes(1)
	})

	#check: close({
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		detail!:   strings.MinRunes(1)
		status!:   "pass" | "block" | "not_evaluable"
	})

	#difference: close({
		after_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		before_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		category!: "source_evidence" | "selector" | "label_alias" | "definition_meaning" | "boundary" | "relation" | "semantic_application" | "authority" | "registry_topology" | "consumer_topology" | "structural_schema" | "identity_denominator" | "generated_projection" | "bundle_inventory"
		change!:   "added" | "removed" | "modified" | "missing" | "not_evaluable"
		drift_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		invalidates!: list.UniqueItems() & [..."semantic_context" | "semantic_closure" | "define_source" | "bundle" | "admission" | "artifact_pass"] & [_, ...]
		locator!:         strings.MinRunes(1)
		repair_route!:    "recompile" | "rerun_semantic_closure" | "reauthor_define_source" | "definitions_governance" | "identity_denominator" | "stop"
		semantic_effect!: "none" | "meaning_changed" | "authority_changed" | "topology_changed" | "review_required" | "not_evaluable"
	})

	#digest: =~"^[a-f0-9]{64}$"

	#driftAnalysis: close({
		compile_window!: "current" | "changed" | "not_evaluable"
		differences!: list.UniqueItems() & [...close({
			after_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			before_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			category!: "source_evidence" | "selector" | "label_alias" | "definition_meaning" | "boundary" | "relation" | "semantic_application" | "authority" | "registry_topology" | "consumer_topology" | "structural_schema" | "identity_denominator" | "generated_projection" | "bundle_inventory"
			change!:   "added" | "removed" | "modified" | "missing" | "not_evaluable"
			drift_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
			invalidates!: list.UniqueItems() & [..."semantic_context" | "semantic_closure" | "define_source" | "bundle" | "admission" | "artifact_pass"] & [_, ...]
			locator!:         strings.MinRunes(1)
			repair_route!:    "recompile" | "rerun_semantic_closure" | "reauthor_define_source" | "definitions_governance" | "identity_denominator" | "stop"
			semantic_effect!: "none" | "meaning_changed" | "authority_changed" | "topology_changed" | "review_required" | "not_evaluable"
		})]
		prior_admission!: "not_provided" | "current" | "changed" | "not_evaluable"
		summary!: close({
			authority_state!:  "unchanged" | "changed" | "unresolved" | "not_evaluable"
			evidence_state!:   "current" | "stale" | "missing" | "not_evaluable"
			overall!:          "current" | "recompile_required" | "closure_refresh_required" | "semantic_reassessment_required" | "blocked"
			projection_state!: "unchanged" | "changed" | "not_evaluable"
			semantic_state!:   "unchanged" | "changed" | "review_required" | "not_evaluable"
			topology_state!:   "unchanged" | "changed" | "not_evaluable"
		})
	})

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"

	#outputRef: close({
		kind!:   strings.MinRunes(1)
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#pathSet: list.UniqueItems() & [...string]

	#producerBinding: close({
		producer!: close({
			identity!: "invoke.compile-define-source.v3"
			path!:     "arcanum/spells/invoke/scripts/compile_define_source_v3.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		profile_id!:     "invoke.generic-definitions-baseline.v3"
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
	})

	#relativePath: string

	#structuralSchemaRef: close({
		definition_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,191}$"
		path!:          string
		sha256!:        =~"^[a-f0-9]{64}$"
		size!:          int & >=0
	})
}

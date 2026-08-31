// Invoke Define Stage Receipt v3
//
// Success-only receipt for the installed Define v3 producer. It binds an exact
// ready semantic closure and a complete ordered output inventory while
// granting no registry or runtime authority.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-result/v3")
	close({
		$schema!:          "https://arcanum.dev/schemas/invoke/define-result/v3"
		authority_effect!: "none"
		mode!:             "define"
		next_route!:       "design" | "spellcraft" | "sigil-development" | "deferred"
		outputs!: list.MaxItems(12) & [matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "semantic-context"
			path?: "DEFINE-SEMANTIC-CONTEXT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "semantic-closure-receipt"
			path?: "DEFINE-SEMANTIC-CLOSURE-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "spec"
			path?: "SPEC.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "definitions"
			path?: "DEFINITIONS.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "definitions-view"
			path?: "DEFINITIONS.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "glossary"
			path?: "GLOSSARY.md"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "layering"
			path?: "IMPLEMENTATION-LAYERING.md" | "LAYERING-GAP.md"
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
			kind?: "identity-denominator"
			path?: "IDENTITY-DENOMINATOR-RECEIPT.json"
		}]), matchN(2, [close({
			kind!:   string
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), {
			kind?: "transport"
			path?: "DEFINE-TRANSPORT-REPORT.json"
		}])] & [_, _, _, _, _, _, _, _, _, _, _, _, ...]
		owner_capability!: "invoke"
		producer!: close({
			identity!: "invoke.compile-define-source.v3"
			path!:     "arcanum/spells/invoke/scripts/compile_define_source_v3.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		profile_id!:     "invoke.generic-definitions-baseline.v3"
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		result!:         "pass"
		schema_bindings!: close({
			definitions_v1_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			definitions_v2_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			profile_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			result_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			source_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		schema_version!: "invoke.define-stage-receipt.v3"
		semantic_evidence!: close({
			closure_receipt_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			context_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		semantic_outcome!: "candidate-definitions" | "reference-only" | "mixed"
		source_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		structural_schema_refs!: list.UniqueItems() & [...close({
			definition_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			path!:          string
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
		})]
	})

	#definitionsOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "definitions"
		path?: "DEFINITIONS.json"
	}])

	#definitionsViewOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "definitions-view"
		path?: "DEFINITIONS.md"
	}])

	#digest: =~"^[a-f0-9]{64}$"

	#dispatchTraceOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "dispatch-trace"
		path?: "DISPATCH-TRACE.json"
	}])

	#distillOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "distill"
		path?: "DISTILL-RECEIPT.json"
	}])

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#glossaryOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "glossary"
		path?: "GLOSSARY.md"
	}])

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#identityDenominatorOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "identity-denominator"
		path?: "IDENTITY-DENOMINATOR-RECEIPT.json"
	}])

	#layeringOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "layering"
		path?: "IMPLEMENTATION-LAYERING.md" | "LAYERING-GAP.md"
	}])

	#outputRef: close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#relativePath: string

	#semanticClosureOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "semantic-closure-receipt"
		path?: "DEFINE-SEMANTIC-CLOSURE-RECEIPT.json"
	}])

	#semanticContextOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "semantic-context"
		path?: "DEFINE-SEMANTIC-CONTEXT.json"
	}])

	#specOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "spec"
		path?: "SPEC.md"
	}])

	#structuralSchemaRef: close({
		definition_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		path!:          string
		sha256!:        =~"^[a-f0-9]{64}$"
		size!:          int & >=0
	})

	#templateSelectionOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "template-selection"
		path?: "TEMPLATE-SELECTION-RECEIPT.json"
	}])

	#transportOutput: matchN(2, [close({
		kind!:   string
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	}), {
		kind?: "transport"
		path?: "DEFINE-TRANSPORT-REPORT.json"
	}])
}

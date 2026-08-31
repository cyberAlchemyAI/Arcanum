// Invoke Define Stage Receipt v2
package prototype

import (
	"strings"
	"list"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-result-v2")
	close({
		schema_version!:   "invoke.define-stage-receipt.v2"
		receipt_id!:       strings.MinRunes( 1)
		owner_capability!: "invoke"
		mode!:             "define"
		producer!: close({
			identity!: "invoke.compile-define-source.v2"
			path!:     "arcanum/spells/invoke/scripts/compile_define_source_v2.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		profile_id!: "invoke.generic-definitions-baseline.v2"
		source_ref!: #exact_ref
		outputs!: list.MaxItems(10) & list.UniqueItems() & [_, _, _, _, _, _, _, _, _, _, ...] & [...#output_ref]
		result!:           "pass"
		next_route!:       "design" | "spellcraft" | "sigil-development" | "deferred"
		authority_effect!: "none"
		receipt_digest!:   =~"^[a-f0-9]{64}$"
	})

	#exact_ref: close({
		path!:   strings.MinRunes( 1)
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#output_ref: close({
		kind!:   "spec" | "definitions" | "definitions-view" | "glossary" | "layering" | "template-selection" | "dispatch-trace" | "distill" | "identity-denominator" | "transport"
		path!:   strings.MinRunes( 1)
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})
}

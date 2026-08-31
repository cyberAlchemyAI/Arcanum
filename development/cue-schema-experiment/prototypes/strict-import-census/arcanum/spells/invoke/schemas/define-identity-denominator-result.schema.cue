// Invoke Define Identity Denominator Result
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.local/schemas/define-identity-denominator-result.schema.json")
	matchIf({
		verdict!: "pass"
	}, {
		selector?: {}
		request?: #proof_input_binding
		schemas?: {
			request_schema?: #proof_input_binding
			result_schema?:  #proof_input_binding
		}
		inputs?: {
			artifact?: #proof_artifact_binding
			authority_source?: matchN(2, [#proof_source_binding, null | bool | number | string | [...] | {
				role?: "authority"
			}])
			corroborating_sources?: [...matchN(2, [#proof_source_binding, null | bool | number | string | [...] | {
				role?: "corroborating"
			}])]
		}
		expected_count?: null | bool | >=1 | string | [...] | {}
		observed_count?: null | bool | >=1 | string | [...] | {}
		matched_count?: null | bool | >=1 | string | [...] | {}
		identities?: [_, ...] & [...#proof_identity]
		diagnostics?: null | bool | number | string | list.MaxItems(0) | {}
	}, {
		diagnostics?: null | bool | number | string | [_, ...] | {}
	}) & {} & close({
		schema_version!: "invoke.define-identity-denominator-result/v1"
		validator!: close({
			id!:      "invoke-define-identity-denominator-validator"
			version!: =~"^[0-9]+\\.[0-9]+\\.[0-9]+$"
		})
		request!: #input_binding
		schemas!: close({
			request_schema!: #input_binding
			result_schema!:  #input_binding
		})
		selector!: matchN(1, [close({
			heading!:       strings.MinRunes( 1)
			heading_level!: int & >=1 & <=6
			id_column!:     strings.MinRunes( 1)
			label_column!:  strings.MinRunes( 1)
			coverage!:      "exact"
		}), null])
		inputs!: close({
			artifact!: matchN(1, [#artifact_binding, null])
			authority_source!: matchN(1, [#source_binding, null])
			corroborating_sources!: [...#source_binding]
		})
		expected_count!: int & >=0
		observed_count!: int & >=0
		matched_count!:  int & >=0
		identities!: [...#identity]
		verdict!: "pass" | "block"
		diagnostics!: [...#diagnostic]
		authority_effect!: "none"
	})

	#artifact_binding: close({
		path!: strings.MinRunes( 1)
		sha256!: matchN(1, [#sha256, null])
		expected_sha256!: matchN(1, [#sha256, null])
		format!: "markdown"
	})

	#corroborating_match: close({
		source_id!: strings.MinRunes( 1)
		match!:     bool
	})

	#diagnostic: close({
		code!:    =~"^DEFINE_IDENTITY_[A-Z0-9_]+$"
		message!: strings.MinRunes( 1)
		selector!: matchN(1, [strings.MinRunes( 1), null])
		details!: {}
	})

	#filter: close({
		field!:  strings.MinRunes( 1)
		equals!: null | bool | int | string
	})

	#identity: close({
		id!:    strings.MinRunes( 1)
		label!: strings.MinRunes( 1)
		row!:   int & >=1
		expected_label!: matchN(1, [strings.MinRunes( 1), null])
		authority_match!: bool
		corroborating_matches!: [...#corroborating_match]
	})

	#input_binding: close({
		path!: strings.MinRunes( 1)
		sha256!: matchN(1, [#sha256, null])
		expected_sha256!: matchN(1, [#sha256, null])
	})

	#proof_artifact_binding: matchN(2, [#artifact_binding, null | bool | number | string | [...] | {
		sha256?:          #sha256
		expected_sha256?: #sha256
	}])

	#proof_identity: matchN(2, [#identity, null | bool | number | string | [...] | {
		expected_label?:  strings.MinRunes( 1)
		authority_match?: true
		corroborating_matches?: [...matchN(2, [#corroborating_match, null | bool | number | string | [...] | {
			match?: true
		}])]
	}])

	#proof_input_binding: matchN(2, [#input_binding, null | bool | number | string | [...] | {
		sha256?:          #sha256
		expected_sha256?: #sha256
	}])

	#proof_source_binding: matchN(2, [#source_binding, null | bool | number | string | [...] | {
		sha256?:          #sha256
		expected_sha256?: #sha256
	}])

	#sha256: =~"^[0-9a-f]{64}$"

	#source_binding: close({
		path!: strings.MinRunes( 1)
		sha256!: matchN(1, [#sha256, null])
		expected_sha256!: matchN(1, [#sha256, null])
		source_id!:          strings.MinRunes( 1)
		role!:               "authority" | "corroborating"
		format!:             "json" | "yaml"
		collection_pointer!: string
		fields!: close({
			id!:    strings.MinRunes( 1)
			label!: strings.MinRunes( 1)
		})
		filters!: [...#filter]
	})
}

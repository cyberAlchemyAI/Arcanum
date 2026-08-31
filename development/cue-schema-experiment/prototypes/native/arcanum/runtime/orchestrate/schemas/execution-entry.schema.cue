package prototype

import "strings"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://cue.jsonschema.invalid/arcanum.subagent-strategy-execution-entry.v0.1")
	close({
		authorization!: "approved"
		canonical_dispatch_ref!: close({
			path!:   strings.MinRunes(1)
			sha256!: =~"^[0-9a-f]{64}$"
			size!:   int & >=1
		})
		confirmation_handle!: strings.MinRunes(1)
		registration!:        _#defs."/properties/registration"
		schema_version!:      "arcanum.subagent-strategy-execution-entry.v0.1"
	})

	_#defs: "/properties/registration": {
		@jsonschema(id="https://cue.jsonschema.invalid/arcanum.subagent-strategy-registration.v0.3")
		close({
			admission_receipt_ref!: matchN(>=1, [close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[0-9a-f]{64}$"
				size!:   int & >=1
			}), null])
			confirmation!: close({
				binding_sha256!: =~"^[0-9a-f]{64}$"
				handle!:         strings.MinRunes(1)
				material_equivalence_ref!: matchN(>=1, [close({
					path!:   strings.MinRunes(1)
					sha256!: =~"^[0-9a-f]{64}$"
					size!:   int & >=1
				}), null])
				mode!: "exact_sheet" | "material_projection"
			})
			execution_projection_sha256!: =~"^[0-9a-f]{64}$"
			ledger!:                      strings.MinRunes(1)
			profile_id!:                  strings.MinRunes(1)
			profile_ref!: close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[0-9a-f]{64}$"
				size!:   int & >=1
			})
			registration_envelope_ref!: close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[0-9a-f]{64}$"
				size!:   int & >=1
			})
			schema_version!:       "arcanum.subagent-strategy-registration.v0.3"
			sheet_schema_version!: strings.MinRunes(1)
			source_lifecycle!:     "consumed" | "durable"
			source_sheet_ref!: close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[0-9a-f]{64}$"
				size!:   int & >=1
			})
			temporary_close!: strings.MinRunes(1)
		})
	}

	_#defs: "/properties/registration/$defs/exactRef": close({
		path!:   strings.MinRunes(1)
		sha256!: =~"^[0-9a-f]{64}$"
		size!:   int & >=1
	})

	_#defs: "/properties/registration/$defs/path": strings.MinRunes(1)

	_#defs: "/properties/registration/$defs/sha256": =~"^[0-9a-f]{64}$"
}

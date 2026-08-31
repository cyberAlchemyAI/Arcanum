// Invoke Generic Definitions Profile v3
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-profile/v3")
	close({
		$schema!:                 "https://arcanum.dev/schemas/invoke/define-profile/v3"
		schema_version!:          "invoke.define-profile.v3"
		profile_id!:              "invoke.generic-definitions-baseline.v3"
		public_contract!:         true
		v2_compatibility_policy!: "preserve-byte-and-validate-only"
		outputs!: ["semantic-context", "semantic-closure-receipt", "spec", "definitions", "definitions-view", "glossary", "layering", "template-selection", "dispatch-trace", "distill", "identity-denominator", "transport", "stage-receipt"]
	})
}

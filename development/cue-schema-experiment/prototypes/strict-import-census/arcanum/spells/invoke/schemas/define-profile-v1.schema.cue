// Invoke Generic Define Profile
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-profile-v1")
	close({
		schema_version!:             "invoke.define-profile.v1"
		profile_id!:                 "invoke.generic-spec-baseline.v1"
		public_contract!:            true
		historical_template_policy!: "compatibility-read-only"
		outputs!: ["spec", "glossary", "layering", "template-selection", "dispatch-trace", "distill", "identity-denominator", "transport", "stage-receipt"]
	})
}

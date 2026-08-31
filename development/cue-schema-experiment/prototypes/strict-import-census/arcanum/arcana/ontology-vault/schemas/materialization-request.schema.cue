package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://cue.jsonschema.invalid/ontology-vault-materialization-request/v1")
	close({
		schema_version!: "ontology-vault-materialization-request/v1"
		intent!: close({
			one_off!:           bool
			durable!:           bool
			reusable!:          bool
			evolving!:          bool
			package_requested!: bool
		})
		scope!: close({
			ontology_type_count!: int & >=0
			branch_count!:        int & >=0
			view_count!:          int & >=0
			bridge!:              bool
		})
		state!: close({
			stable_identity_survives_run!: bool
			enriches_existing_ontology!:   bool
			needs_schemas!:                bool
			needs_source_bindings!:        bool
			needs_human_navigation!:       bool
			needs_reusable_projections!:   bool
			runtime_profile_mutation!:     bool
			invocation_evidence_only!:     bool
		})
		ownership!: close({
			owner_route!:                 null | string
			package_root!:                null | string
			crosses_visibility_boundary!: bool
			visibility!:                  "public" | "private" | null
		})
	})
}

// Reading Learning Package Preset Profile
package prototype

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	preset_profile!: {
		preset_id!: "deep_voice_reading" | "quick_video" | "medium_explanation" | "learning_distill" | "custom_from_examples"
		source!: {
			tower_root!:       _
			source_artifacts!: _
		}
		resonance_core!: {}
		relevance_core!: {}
		trajectory_core!: {}
		examples!: {
			accepted!: _
			rejected!: _
		}
		pdf_preferences!: {}
		approval!: preset_preview_status!: _
	}
}

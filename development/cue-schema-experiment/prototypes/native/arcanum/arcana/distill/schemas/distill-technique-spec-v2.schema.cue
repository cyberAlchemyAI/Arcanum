// Distill v2 TechniqueSpec
package prototype

import (
	"list"
	"strings"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/technique-spec/2-0-0")
	close({
		activation!: "always" | "condition" | "mode_required" | "risk_required" | "user_requested"
		allowed_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		block_condition!: strings.MinRunes(1)
		display_name!:    strings.MinRunes(1)
		emits!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		emitted_field_constraints!: struct.MinFields(1) & {
			...
		} & {
			[string]: matchN(1, [close({
				const_value!: strings.MinRunes(1)
				value_kind!:  "const"
			}), close({
				definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/canonical_identifier"
				value_kind!:     "canonical_identifier"
			}), close({
				value_kind!: "enum"
				values!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			}), close({
				definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/non_empty_string"
				value_kind!:     "non_empty_string"
			}), close({
				value_kind!: "boolean"
			})])
		}
		failure_behavior!: "pass" | "flag" | "block" | "skip_with_reason" | "route"
		flag_condition!:   strings.MinRunes(1)
		hooks!: matchN(2, [list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...], [..."after_intent_confirmation" | "before_layer_split" | "after_proposer_pass" | "after_balancer_pass" | "before_accept_split" | "before_pitch_off" | "before_verdict" | "after_verdict"]])
		pass_condition!: strings.MinRunes(1)
		phases!: matchN(2, [list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...], [..."setup" | "concept_mapping" | "proposal" | "balance" | "closure" | "pitch_off" | "final_synthesis" | "handoff"]])
		schema_version!: "distill.technique_spec.v2"
		technique_id!:   string
		type!:           "gate" | "lens" | "classifier" | "mode_mechanic" | "check" | "closeout"
	})

	#boolean_constraint: close({
		value_kind!: "boolean"
	})

	#canonical_identifier_constraint: close({
		definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/canonical_identifier"
		value_kind!:     "canonical_identifier"
	})

	#const_constraint: close({
		const_value!: strings.MinRunes(1)
		value_kind!:  "const"
	})

	#emitted_field_constraint: matchN(1, [close({
		const_value!: strings.MinRunes(1)
		value_kind!:  "const"
	}), close({
		definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/canonical_identifier"
		value_kind!:     "canonical_identifier"
	}), close({
		value_kind!: "enum"
		values!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
	}), close({
		definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/non_empty_string"
		value_kind!:     "non_empty_string"
	}), close({
		value_kind!: "boolean"
	})])

	#enum_constraint: close({
		value_kind!: "enum"
		values!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
	})

	#non_empty_string_constraint: close({
		definition_ref!: "https://arcanum.dev/schemas/distill/common/2-0-0#/$defs/non_empty_string"
		value_kind!:     "non_empty_string"
	})
}

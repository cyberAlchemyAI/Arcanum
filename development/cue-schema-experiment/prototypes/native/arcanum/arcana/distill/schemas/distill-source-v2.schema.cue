// Distill v2 Normalized Source RunFrame
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/distill/source/2-0-0")
	close({
		artifacts!: list.UniqueItems() & [...close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     string
				size_bytes!: int & >=0
			})
			semantic_role!: "input" | "context" | "output_target" | "reference"
		})] & [_, ...]
		constraints!: close({
			cost!: list.UniqueItems() & [...strings.MinRunes(1)]
			domain!: list.UniqueItems() & [...strings.MinRunes(1)]
			governance!: list.UniqueItems() & [...strings.MinRunes(1)]
			quality!: list.UniqueItems() & [...strings.MinRunes(1)]
			stop_rule_tightening!: list.UniqueItems() & [...strings.MinRunes(1)]
			time!: list.UniqueItems() & [...strings.MinRunes(1)]
		})
		discovery!: close({
			assumptions!: list.UniqueItems() & [...strings.MinRunes(1)]
			blocker_unknowns!: list.UniqueItems() & [...strings.MinRunes(1)]
			non_blocker_unknowns!: list.UniqueItems() & [...strings.MinRunes(1)]
			provided_evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
			searched_sources!: list.UniqueItems() & [...strings.MinRunes(1)]
		})
		evidence_context?: close({
			authority_effect!: "none"
			refs!: list.UniqueItems() & [...close({
				path!:       strings.MinRunes(1)
				sha256!:     string
				size_bytes!: int & >=0
			})]
			status!: "accepted" | "unavailable" | "none"
		})
		identity!: close({
			created_at!:        =~"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z$"
			invocation_source!: "direct" | "invoked_by"
			run_id!:            string
			source_id!:         string
		})
		intent!: close({
			objective!:         strings.MinRunes(1)
			optimization_goal!: strings.MinRunes(1)
			output_artifact!:   strings.MinRunes(1)
			seed_point!:        strings.MinRunes(1)
			target_context!:    strings.MinRunes(1)
		})
		lineage!: matchIf({
			objective_output_revision?: {}
		}, {
			parent_run_id?:    string
			parent_source_id?: string
		}, _) & {} & close({
			objective_output_revision!: matchN(1, [null, close({
				prior_objective!:       strings.MinRunes(1)
				prior_output_artifact!: strings.MinRunes(1)
				reason!:                strings.MinRunes(1)
			})])
			parent_run_id!:    null | string
			parent_source_id!: null | string
		})
		policy!: close({
			mode_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     string
				size_bytes!: int & >=0
			})
			overrides?: close({
				rounds_per_track?: int & >=1
				tracks?:           int & >=1
			})
			profile_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     string
				size_bytes!: int & >=0
			})
			requested_technique_refs!: list.UniqueItems() & [...close({
				path!:       strings.MinRunes(1)
				sha256!:     string
				size_bytes!: int & >=0
			})] & [_, ...]
		})
		schema_version!: "distill.source.v2"
	})

	#artifacts: list.UniqueItems() & [...close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})
		semantic_role!: "input" | "context" | "output_target" | "reference"
	})] & [_, ...]

	#constraints: close({
		cost!: list.UniqueItems() & [...strings.MinRunes(1)]
		domain!: list.UniqueItems() & [...strings.MinRunes(1)]
		governance!: list.UniqueItems() & [...strings.MinRunes(1)]
		quality!: list.UniqueItems() & [...strings.MinRunes(1)]
		stop_rule_tightening!: list.UniqueItems() & [...strings.MinRunes(1)]
		time!: list.UniqueItems() & [...strings.MinRunes(1)]
	})

	#discovery: close({
		assumptions!: list.UniqueItems() & [...strings.MinRunes(1)]
		blocker_unknowns!: list.UniqueItems() & [...strings.MinRunes(1)]
		non_blocker_unknowns!: list.UniqueItems() & [...strings.MinRunes(1)]
		provided_evidence!: list.UniqueItems() & [...strings.MinRunes(1)]
		searched_sources!: list.UniqueItems() & [...strings.MinRunes(1)]
	})

	#evidence_context: close({
		authority_effect!: "none"
		refs!: list.UniqueItems() & [...close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})]
		status!: "accepted" | "unavailable" | "none"
	})

	#identity: close({
		created_at!:        =~"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z$"
		invocation_source!: "direct" | "invoked_by"
		run_id!:            string
		source_id!:         string
	})

	#intent: close({
		objective!:         strings.MinRunes(1)
		optimization_goal!: strings.MinRunes(1)
		output_artifact!:   strings.MinRunes(1)
		seed_point!:        strings.MinRunes(1)
		target_context!:    strings.MinRunes(1)
	})

	#lineage: matchIf({
		objective_output_revision?: {}
	}, {
		parent_run_id?:    string
		parent_source_id?: string
	}, _) & {} & close({
		objective_output_revision!: matchN(1, [null, close({
			prior_objective!:       strings.MinRunes(1)
			prior_output_artifact!: strings.MinRunes(1)
			reason!:                strings.MinRunes(1)
		})])
		parent_run_id!:    null | string
		parent_source_id!: null | string
	})

	#policy: close({
		mode_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})
		overrides?: close({
			rounds_per_track?: int & >=1
			tracks?:           int & >=1
		})
		profile_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})
		requested_technique_refs!: list.UniqueItems() & [...close({
			path!:       strings.MinRunes(1)
			sha256!:     string
			size_bytes!: int & >=0
		})] & [_, ...]
	})

	#string_array: list.UniqueItems() & [...strings.MinRunes(1)]
}

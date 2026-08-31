// Invoke Define Definitions Artifact v2
//
// Candidate-only Define v3 registry. It may contain new or specialized
// candidate definitions and exact authority bindings to existing canonical
// definitions without copying their normative prose.
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/definitions/v2")
	matchN(2, [matchN(>=1, [{
		definitions?: null | bool | number | string | [_, ...] | {}
	}, {
		authority_bindings?: null | bool | number | string | [_, ...] | {}
	}]), matchIf({
		visibility!: "public"
	}, {
		authority_bindings?: null | bool | number | string | [...null | bool | number | string | [...] | {
			authority_ref?: null | bool | number | string | [...] | {
				visibility!: "public"
			}
		}] | {}
		definitions?: null | bool | number | string | [...null | bool | number | string | [...] | {
			source_refs?: null | bool | number | string | [...null | bool | number | string | [...] | {
				visibility!: "public"
			}] | {}
		}] | {}
	}, _) & {}]) & close({
		$schema!: "https://arcanum.dev/schemas/invoke/definitions/v2"
		authority_bindings!: list.UniqueItems() & [...close({
			authority_ref!: close({
				path!:       string
				selector!:   =~".*\\S.*"
				sha256!:     =~"^[a-f0-9]{64}$"
				size!:       int & >=0
				visibility!: "public" | "private"
			})
			authority_scope!: close({
				kind!: "repository" | "project" | "feature" | "artifact"
				ref!:  strings.MinRunes(1)
			})
			authority_status!: "active"
			binding_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			definition_id!:    =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
			probe_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			role!:             "reuse" | "specialization-basis"
			term!:             =~".*\\S.*"
		})]
		authority_effect!: "none"
		authority_kind!:   "kind.definition"
		authority_scope!: close({
			kind!: "repository" | "project" | "feature" | "artifact"
			ref!:  strings.MinRunes(1)
		})
		definitions!: list.UniqueItems() & [...matchN(2, [matchN(3, [matchIf({
			status!: "deferred"
		}, {
			deferred_as?: string
		}, {
			deferred_as?: null
		}) & {}, matchIf({
			status!: "superseded"
		}, {
			superseded_by?: =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
		}, _) & {}, matchIf({
			status!: "candidate" | "active" | "deferred"
		}, {
			superseded_by?: null
		}, _) & {}]) & close({
			aliases!: list.UniqueItems() & [...strings.MinRunes(1)]
			boundary!: matchN(>=1, [{
				includes?: null | bool | number | string | [_, ...] | {}
			}, {
				excludes?: null | bool | number | string | [_, ...] | {}
			}, {
				conditions?: null | bool | number | string | [_, ...] | {}
			}]) & close({
				conditions!: list.UniqueItems() & [...strings.MinRunes(1)]
				excludes!: list.UniqueItems() & [...strings.MinRunes(1)]
				includes!: list.UniqueItems() & [...strings.MinRunes(1)]
			})
			challenge_contract!: matchN(1, [close({
				blocking_question!: strings.MinRunes(1)
				claim_or_edge!:     strings.MinRunes(1)
				gate!:              strings.MinRunes(1)
				modes!: list.UniqueItems() & [..."contradiction" | "scope" | "evidence" | "authority"] & [_, ...]
				owner_route!:   strings.MinRunes(1)
				residue_route!: strings.MinRunes(1)
			}), null])
			deferred_as!: matchN(1, [=~"^[a-z0-9][a-z0-9-]{1,63}$", null])
			definition_version!: =~"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$"
			drift_route!:        strings.MinRunes(1)
			id!:                 =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
			misuse_warning!: matchN(1, [strings.MinRunes(1), null])
			notation!: [...close({
				meaning!: strings.MinRunes(1)
				symbol!:  strings.MinRunes(1)
			})]
			primary_consumers!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			promotion_boundary!: matchN(1, [strings.MinRunes(1), null])
			relations!: [...close({
				id!:   =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
				type!: "references" | "depends-on" | "contrasts-with" | "supersedes"
			})]
			source_kinds!: list.UniqueItems() & [..."operator-reading" | "local-inference" | "synthesis" | "method-vocabulary" | "domain-vocabulary" | "historical"] & [_, ...]
			source_refs!: list.MatchN(>=1, null | bool | number | string | [...] | {
				role!: "normative" | "provenance" | "evidence"
			}) & list.UniqueItems() & [...matchN(2, [matchIf({
				selector_type!: "line-span"
			}, {
				end_line?:   int & >=1
				start_line?: int & >=1
			}, {
				end_line?:   null
				start_line?: null
			}) & {}, matchIf({
				role!: "normative" | "provenance" | "evidence"
			}, {
				sha256?: =~"^[a-f0-9]{64}$"
				size?:   int & >=0
			}, _) & {}]) & close({
				end_line!: matchN(1, [int & >=1, null])
				path!: matchN(1, [=~"^https://[^\\s]+$", string])
				role!:          "normative" | "provenance" | "evidence" | "example"
				selector!:      strings.MinRunes(1)
				selector_type!: "heading" | "anchor" | "line-span" | "json-pointer" | "yaml-path" | "symbol"
				sha256!: matchN(1, [=~"^[a-f0-9]{64}$", null])
				size!: matchN(1, [int & >=0, null])
				start_line!: matchN(1, [int & >=1, null])
				visibility!: "public" | "private"
			})] & [_, ...]
			status!: "candidate" | "active" | "deferred" | "superseded" | "deprecated"
			status_detail!: matchN(1, [strings.MinRunes(1), null])
			structural_schema!: matchN(1, [matchIf({
				status!: "machine-checkable"
			}, {
				ref?: strings.MinRunes(1)
			}, _) & {} & close({
				handle!: =~"^[A-Za-z0-9][A-Za-z0-9._-]*-SCHEMA(?:-[1-9][0-9]*)?$"
				ref!: matchN(1, [strings.MinRunes(1), null])
				status!: "documentary" | "machine-checkable"
			}), null])
			superseded_by!: matchN(1, [=~"^[A-Za-z][A-Za-z0-9._-]{1,127}$", null])
			supersedes!: list.UniqueItems() & [...=~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"]
			term!: strings.MinRunes(1)
			use_carefully!: matchN(1, [strings.MinRunes(1), null])
			voices!: close({
				domain_context!: strings.MinRunes(1)
				formal!: matchN(1, [strings.MinRunes(1), null])
				normative!: strings.MinRunes(1)
				operational!: matchN(1, [strings.MinRunes(1), null])
				plain_language!: strings.MinRunes(1)
			})
		}), {
			aliases?: null | bool | number | string | [...=~".*\\S.*"] | {}
			deferred_as?: null
			relations?: null | bool | number | string | [...null | bool | number | string | [...] | {
				type?: "references" | "depends-on" | "contrasts-with"
			}] | {}
			source_refs?: null | bool | number | string | [...null | bool | number | string | [...] | {
				path?:   string
				sha256?: =~"^[a-f0-9]{64}$"
				size?:   int & >=0
			}] | {}
			status?:        "candidate"
			superseded_by?: null
			supersedes?: null | bool | number | string | list.MaxItems(0) | {}
			term?: =~".*\\S.*"
			voices?: null | bool | number | string | [...] | {
				domain_context?: =~".*\\S.*"
				formal?: matchN(1, [=~".*\\S.*", null])
				normative?: =~".*\\S.*"
				operational?: matchN(1, [=~".*\\S.*", null])
				plain_language?: =~".*\\S.*"
			}
		}])]
		owner_route!:     strings.MinRunes(1)
		registry_id!:     =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
		registry_status!: "candidate"
		schema_version!:  "definitions/v2"
		semantic_applications!: list.UniqueItems() & [...matchN(3, [matchIf({
			disposition!: "reuse-existing"
		}, {
			authority_binding_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
			definition_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			disposition!: "new-scoped-term"
		}, {
			authority_binding_ids?: null | bool | number | string | list.MaxItems(0) | {}
			definition_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		}, _) & {}, matchIf({
			disposition!: "specialize-existing"
		}, {
			authority_binding_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
			definition_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		}, _) & {}]) & close({
			authority_binding_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			definition_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing"
			probe_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			rationale!:   =~".*\\S.*"
		})] & [_, ...]
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
		title!:      strings.MinRunes(1)
		visibility!: "public" | "private"
	})

	#authorityBinding: close({
		authority_ref!: close({
			path!:       string
			selector!:   =~".*\\S.*"
			sha256!:     =~"^[a-f0-9]{64}$"
			size!:       int & >=0
			visibility!: "public" | "private"
		})
		authority_scope!: close({
			kind!: "repository" | "project" | "feature" | "artifact"
			ref!:  strings.MinRunes(1)
		})
		authority_status!: "active"
		binding_id!:       =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		definition_id!:    =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
		probe_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		role!:             "reuse" | "specialization-basis"
		term!:             =~".*\\S.*"
	})

	#authorityMaterialRef: close({
		path!:       string
		selector!:   =~".*\\S.*"
		sha256!:     =~"^[a-f0-9]{64}$"
		size!:       int & >=0
		visibility!: "public" | "private"
	})

	#candidateDefinition: matchN(2, [matchN(3, [matchIf({
		status!: "deferred"
	}, {
		deferred_as?: string
	}, {
		deferred_as?: null
	}) & {}, matchIf({
		status!: "superseded"
	}, {
		superseded_by?: =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
	}, _) & {}, matchIf({
		status!: "candidate" | "active" | "deferred"
	}, {
		superseded_by?: null
	}, _) & {}]) & close({
		aliases!: list.UniqueItems() & [...strings.MinRunes(1)]
		boundary!: matchN(>=1, [{
			includes?: null | bool | number | string | [_, ...] | {}
		}, {
			excludes?: null | bool | number | string | [_, ...] | {}
		}, {
			conditions?: null | bool | number | string | [_, ...] | {}
		}]) & close({
			conditions!: list.UniqueItems() & [...strings.MinRunes(1)]
			excludes!: list.UniqueItems() & [...strings.MinRunes(1)]
			includes!: list.UniqueItems() & [...strings.MinRunes(1)]
		})
		challenge_contract!: matchN(1, [close({
			blocking_question!: strings.MinRunes(1)
			claim_or_edge!:     strings.MinRunes(1)
			gate!:              strings.MinRunes(1)
			modes!: list.UniqueItems() & [..."contradiction" | "scope" | "evidence" | "authority"] & [_, ...]
			owner_route!:   strings.MinRunes(1)
			residue_route!: strings.MinRunes(1)
		}), null])
		deferred_as!: matchN(1, [=~"^[a-z0-9][a-z0-9-]{1,63}$", null])
		definition_version!: =~"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$"
		drift_route!:        strings.MinRunes(1)
		id!:                 =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
		misuse_warning!: matchN(1, [strings.MinRunes(1), null])
		notation!: [...close({
			meaning!: strings.MinRunes(1)
			symbol!:  strings.MinRunes(1)
		})]
		primary_consumers!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		promotion_boundary!: matchN(1, [strings.MinRunes(1), null])
		relations!: [...close({
			id!:   =~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"
			type!: "references" | "depends-on" | "contrasts-with" | "supersedes"
		})]
		source_kinds!: list.UniqueItems() & [..."operator-reading" | "local-inference" | "synthesis" | "method-vocabulary" | "domain-vocabulary" | "historical"] & [_, ...]
		source_refs!: list.MatchN(>=1, null | bool | number | string | [...] | {
			role!: "normative" | "provenance" | "evidence"
		}) & list.UniqueItems() & [...matchN(2, [matchIf({
			selector_type!: "line-span"
		}, {
			end_line?:   int & >=1
			start_line?: int & >=1
		}, {
			end_line?:   null
			start_line?: null
		}) & {}, matchIf({
			role!: "normative" | "provenance" | "evidence"
		}, {
			sha256?: =~"^[a-f0-9]{64}$"
			size?:   int & >=0
		}, _) & {}]) & close({
			end_line!: matchN(1, [int & >=1, null])
			path!: matchN(1, [=~"^https://[^\\s]+$", string])
			role!:          "normative" | "provenance" | "evidence" | "example"
			selector!:      strings.MinRunes(1)
			selector_type!: "heading" | "anchor" | "line-span" | "json-pointer" | "yaml-path" | "symbol"
			sha256!: matchN(1, [=~"^[a-f0-9]{64}$", null])
			size!: matchN(1, [int & >=0, null])
			start_line!: matchN(1, [int & >=1, null])
			visibility!: "public" | "private"
		})] & [_, ...]
		status!: "candidate" | "active" | "deferred" | "superseded" | "deprecated"
		status_detail!: matchN(1, [strings.MinRunes(1), null])
		structural_schema!: matchN(1, [matchIf({
			status!: "machine-checkable"
		}, {
			ref?: strings.MinRunes(1)
		}, _) & {} & close({
			handle!: =~"^[A-Za-z0-9][A-Za-z0-9._-]*-SCHEMA(?:-[1-9][0-9]*)?$"
			ref!: matchN(1, [strings.MinRunes(1), null])
			status!: "documentary" | "machine-checkable"
		}), null])
		superseded_by!: matchN(1, [=~"^[A-Za-z][A-Za-z0-9._-]{1,127}$", null])
		supersedes!: list.UniqueItems() & [...=~"^[A-Za-z][A-Za-z0-9._-]{1,127}$"]
		term!: strings.MinRunes(1)
		use_carefully!: matchN(1, [strings.MinRunes(1), null])
		voices!: close({
			domain_context!: strings.MinRunes(1)
			formal!: matchN(1, [strings.MinRunes(1), null])
			normative!: strings.MinRunes(1)
			operational!: matchN(1, [strings.MinRunes(1), null])
			plain_language!: strings.MinRunes(1)
		})
	}), {
		aliases?: null | bool | number | string | [...=~".*\\S.*"] | {}
		deferred_as?: null
		relations?: null | bool | number | string | [...null | bool | number | string | [...] | {
			type?: "references" | "depends-on" | "contrasts-with"
		}] | {}
		source_refs?: null | bool | number | string | [...null | bool | number | string | [...] | {
			path?:   string
			sha256?: =~"^[a-f0-9]{64}$"
			size?:   int & >=0
		}] | {}
		status?:        "candidate"
		superseded_by?: null
		supersedes?: null | bool | number | string | list.MaxItems(0) | {}
		term?: =~".*\\S.*"
		voices?: null | bool | number | string | [...] | {
			domain_context?: =~".*\\S.*"
			formal?: matchN(1, [=~".*\\S.*", null])
			normative?: =~".*\\S.*"
			operational?: matchN(1, [=~".*\\S.*", null])
			plain_language?: =~".*\\S.*"
		}
	}])

	#digest: =~"^[a-f0-9]{64}$"

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#idSet: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]

	#nonEmpty: =~".*\\S.*"

	#relativePath: string

	#semanticApplication: matchN(3, [matchIf({
		disposition!: "reuse-existing"
	}, {
		authority_binding_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		definition_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		disposition!: "new-scoped-term"
	}, {
		authority_binding_ids?: null | bool | number | string | list.MaxItems(0) | {}
		definition_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
	}, _) & {}, matchIf({
		disposition!: "specialize-existing"
	}, {
		authority_binding_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		definition_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
	}, _) & {}]) & close({
		authority_binding_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		definition_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing"
		probe_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		rationale!:   =~".*\\S.*"
	})
}

// Invoke Define Semantic Context v1
//
// Finite context for cross-registry semantic inspection before Define v3
// authoring. Discovery roots are admitted independently by the validator
// invocation and use one fixed semantic-surface profile; this document cannot
// establish repository visibility, a collision verdict, definition authority,
// or promotion by declaration alone.
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-semantic-context/v1")
	matchIf({
		target!: null | bool | number | string | [...] | {
			visibility!: "public"
		}
	}, {
		adjacent_registries?: null | bool | number | string | [...null | bool | number | string | [...] | {
			source_ref?: matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])
		}] | {}
		authority_boundary?: null | bool | number | string | [...] | {
			canonical_source_refs?: null | bool | number | string | [...matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])] | {}
			index_refs?: null | bool | number | string | [...matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])] | {}
			resolution_evidence_refs?: null | bool | number | string | [...matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])] | {}
		}
		concept_probes?: null | bool | number | string | [...null | bool | number | string | [...] | {
			claimed_matches?: null | bool | number | string | [...null | bool | number | string | [...] | {
				source_ref?: matchN(2, [matchN(5, [matchIf({
					selector_type!: "whole-file"
				}, {
					selector?: "$"
				}, _) & {}, matchIf({
					selector_type!: "heading" | "anchor"
				}, {
					format?: "markdown"
				}, _) & {}, matchIf({
					selector_type!: "json-pointer"
				}, {
					format?:   "json"
					selector?: =~"^/"
				}, _) & {}, matchIf({
					selector_type!: "yaml-path"
				}, {
					format?: "yaml"
				}, _) & {}, matchIf({
					selector_type!: "symbol"
				}, {
					format?: "markdown" | "yaml" | "text"
				}, _) & {}]) & close({
					format!:        "markdown" | "json" | "yaml" | "text"
					path!:          string
					selector!:      =~".*\\S.*"
					selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
					sha256!:        =~"^[a-f0-9]{64}$"
					size!:          int & >=0
					visibility!:    "public" | "private"
				}), {
					visibility!: "public"
				}])
			}] | {}
			evidence_refs?: null | bool | number | string | [...matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])] | {}
		}] | {}
		consumer_boundary?: null | bool | number | string | [...] | {
			consumers?: null | bool | number | string | [...null | bool | number | string | [...] | {
				source_ref?: matchN(2, [matchN(5, [matchIf({
					selector_type!: "whole-file"
				}, {
					selector?: "$"
				}, _) & {}, matchIf({
					selector_type!: "heading" | "anchor"
				}, {
					format?: "markdown"
				}, _) & {}, matchIf({
					selector_type!: "json-pointer"
				}, {
					format?:   "json"
					selector?: =~"^/"
				}, _) & {}, matchIf({
					selector_type!: "yaml-path"
				}, {
					format?: "yaml"
				}, _) & {}, matchIf({
					selector_type!: "symbol"
				}, {
					format?: "markdown" | "yaml" | "text"
				}, _) & {}]) & close({
					format!:        "markdown" | "json" | "yaml" | "text"
					path!:          string
					selector!:      =~".*\\S.*"
					selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
					sha256!:        =~"^[a-f0-9]{64}$"
					size!:          int & >=0
					visibility!:    "public" | "private"
				}), {
					visibility!: "public"
				}])
			}] | {}
		}
		discovery?: matchIf(null | bool | number | string | [...] | {
			kind!: "artifact"
		}, null | bool | number | string | [...] | {
			ref!: matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])
		}, _)
		discovery_contract?: null | bool | number | string | [...] | {
			roots?: null | bool | number | string | [...null | bool | number | string | [...] | {
				visibility!: "public"
			}] | {}
		}
		exclusions?: null | bool | number | string | [...null | bool | number | string | [...] | {
			evidence_ref?: matchN(2, [matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			}), {
				visibility!: "public"
			}])
		}] | {}
	}, _) & {} & close({
		$schema!: "https://arcanum.dev/schemas/invoke/define-semantic-context/v1"
		adjacent_registries!: list.UniqueItems() & [...close({
			authority_class!: "candidate" | "local" | "advisory" | "historical"
			format_profile!:  "definitions-json-v1" | "definitions-json-v2"
			reason_in_scope!: =~".*\\S.*"
			registry_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			source_ref!: matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})
		})]
		assessed_by!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		authored_by!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		authority_boundary!: matchN(2, [matchIf({
			declaration!: "configured"
		}, {
			canonical_source_refs?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
			index_refs?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		}, _) & {}, matchIf({
			declaration!: "no-canonical-source"
		}, {
			canonical_source_refs?: null | bool | number | string | list.MaxItems(0) | {}
			index_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}]) & close({
			canonical_scope!: close({
				kind!: "repository" | "project" | "feature" | "artifact"
				ref!:  =~".*\\S.*"
			})
			canonical_source_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})]
			declaration!:    "configured" | "no-canonical-source" | "unresolved"
			declared_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			index_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})]
			profile!: "markdown-index-v1"
			resolution_evidence_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})] & [_, ...]
		})
		authority_effect!: "none"
		concept_probes!: list.UniqueItems() & [...matchN(3, [matchIf({
			proposed_disposition!: "new-scoped-term"
		}, {
			proposed_basis_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			proposed_disposition!: "reuse-existing" | "specialize-existing" | "canonical-change-proposal"
		}, {
			claimed_matches?: null | bool | number | string | list.MatchN(>=1, null | bool | number | string | [...] | {
				authority_class!: "canonical"
				definition_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			}) | {}
			proposed_basis_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		}, _) & {}, matchIf({
			proposed_disposition!: "blocked-conflict"
		}, {
			claimed_matches?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			aliases!: list.UniqueItems() & [...=~".*\\S.*"]
			assessment_rationale!: =~".*\\S.*"
			claimed_matches!: list.UniqueItems() & [...close({
				authority_class!: "canonical" | "candidate" | "local" | "narrative" | "historical"
				authority_scope!: close({
					kind!: "repository" | "project" | "feature" | "artifact"
					ref!:  =~".*\\S.*"
				})
				definition_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
				kind!:     "id" | "term" | "alias" | "normalized-collision" | "semantic-overlap" | "consumer-use"
				match_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				source_ref!: matchN(5, [matchIf({
					selector_type!: "whole-file"
				}, {
					selector?: "$"
				}, _) & {}, matchIf({
					selector_type!: "heading" | "anchor"
				}, {
					format?: "markdown"
				}, _) & {}, matchIf({
					selector_type!: "json-pointer"
				}, {
					format?:   "json"
					selector?: =~"^/"
				}, _) & {}, matchIf({
					selector_type!: "yaml-path"
				}, {
					format?: "yaml"
				}, _) & {}, matchIf({
					selector_type!: "symbol"
				}, {
					format?: "markdown" | "yaml" | "text"
				}, _) & {}]) & close({
					format!:        "markdown" | "json" | "yaml" | "text"
					path!:          string
					selector!:      =~".*\\S.*"
					selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
					sha256!:        =~"^[a-f0-9]{64}$"
					size!:          int & >=0
					visibility!:    "public" | "private"
				})
				term!: =~".*\\S.*"
			})]
			evidence_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})] & [_, ...]
			intended_scope!: close({
				kind!: "repository" | "project" | "feature" | "artifact"
				ref!:  =~".*\\S.*"
			})
			intent!:   =~".*\\S.*"
			probe_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			proposed_basis_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			proposed_disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing" | "canonical-change-proposal" | "blocked-conflict"
			term!:                 =~".*\\S.*"
		})] & [_, ...]
		consumer_boundary!: matchN(2, [matchIf({
			classification!: "catalogued"
		}, {
			consumers?: null | bool | number | string | [_, ...] | {}
			rationale?: null
		}, _) & {}, matchIf({
			classification!: "none-with-rationale"
		}, {
			consumers?: null | bool | number | string | list.MaxItems(0) | {}
			rationale?: =~".*\\S.*"
		}, _) & {}]) & close({
			classification!: "catalogued" | "none-with-rationale"
			consumers!: list.UniqueItems() & [...close({
				consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				kind!:            "narrative" | "protocol" | "schema" | "runtime" | "index" | "other"
				reason_in_scope!: =~".*\\S.*"
				source_ref!: matchN(5, [matchIf({
					selector_type!: "whole-file"
				}, {
					selector?: "$"
				}, _) & {}, matchIf({
					selector_type!: "heading" | "anchor"
				}, {
					format?: "markdown"
				}, _) & {}, matchIf({
					selector_type!: "json-pointer"
				}, {
					format?:   "json"
					selector?: =~"^/"
				}, _) & {}, matchIf({
					selector_type!: "yaml-path"
				}, {
					format?: "yaml"
				}, _) & {}, matchIf({
					selector_type!: "symbol"
				}, {
					format?: "markdown" | "yaml" | "text"
				}, _) & {}]) & close({
					format!:        "markdown" | "json" | "yaml" | "text"
					path!:          string
					selector!:      =~".*\\S.*"
					selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
					sha256!:        =~"^[a-f0-9]{64}$"
					size!:          int & >=0
					visibility!:    "public" | "private"
				})
			})]
			rationale!: matchN(1, [=~".*\\S.*", null])
		})
		context_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		discovery!: matchN(1, [close({
			kind!: "artifact"
			ref!: matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})
		}), close({
			kind!:          "waiver"
			waiver_owner!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			waiver_reason!: strings.MinRunes(8) & =~".*\\S.*"
		})])
		discovery_contract!: close({
			claim_scope!: "configured-roots-complete"
			profile!:     "semantic-surface-v1"
			roots!: list.UniqueItems() & [...close({
				consumer_globs!: ["**/*.md"]
				path!: string
				registry_globs!: ["**/DEFINITIONS.md", "**/DEFINITIONS-INDEX.md", "**/DEFINITIONS.json", "**/GLOSSARY.md"]
				root_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
				visibility!: "public" | "private"
			})] & [_, ...]
		})
		exclusions!: list.UniqueItems() & [...close({
			evidence_ref!: matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})
			exclusion_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			reason!:       =~".*\\S.*"
			selector!:     string
		})]
		schema_version!: "invoke.define-semantic-context.v1"
		target!: close({
			authority_scope!: close({
				kind!: "repository" | "project" | "feature" | "artifact"
				ref!:  =~".*\\S.*"
			})
			id!:         =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			objective!:  =~".*\\S.*"
			visibility!: "public" | "private"
		})
	})

	#adjacentRegistry: close({
		authority_class!: "candidate" | "local" | "advisory" | "historical"
		format_profile!:  "definitions-json-v1" | "definitions-json-v2"
		reason_in_scope!: =~".*\\S.*"
		registry_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		source_ref!: matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})
	})

	#authorityBoundary: matchN(2, [matchIf({
		declaration!: "configured"
	}, {
		canonical_source_refs?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
		index_refs?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
	}, _) & {}, matchIf({
		declaration!: "no-canonical-source"
	}, {
		canonical_source_refs?: null | bool | number | string | list.MaxItems(0) | {}
		index_refs?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		canonical_scope!: close({
			kind!: "repository" | "project" | "feature" | "artifact"
			ref!:  =~".*\\S.*"
		})
		canonical_source_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})]
		declaration!:    "configured" | "no-canonical-source" | "unresolved"
		declared_owner!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		index_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})]
		profile!: "markdown-index-v1"
		resolution_evidence_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})] & [_, ...]
	})

	#authorityScope: close({
		kind!: "repository" | "project" | "feature" | "artifact"
		ref!:  =~".*\\S.*"
	})

	#claimedMatch: close({
		authority_class!: "canonical" | "candidate" | "local" | "narrative" | "historical"
		authority_scope!: close({
			kind!: "repository" | "project" | "feature" | "artifact"
			ref!:  =~".*\\S.*"
		})
		definition_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
		kind!:     "id" | "term" | "alias" | "normalized-collision" | "semantic-overlap" | "consumer-use"
		match_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		source_ref!: matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})
		term!: =~".*\\S.*"
	})

	#conceptProbe: matchN(3, [matchIf({
		proposed_disposition!: "new-scoped-term"
	}, {
		proposed_basis_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		proposed_disposition!: "reuse-existing" | "specialize-existing" | "canonical-change-proposal"
	}, {
		claimed_matches?: null | bool | number | string | list.MatchN(>=1, null | bool | number | string | [...] | {
			authority_class!: "canonical"
			definition_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		}) | {}
		proposed_basis_ids?: null | bool | number | string | list.MaxItems(1) & [_, ...] | {}
	}, _) & {}, matchIf({
		proposed_disposition!: "blocked-conflict"
	}, {
		claimed_matches?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		aliases!: list.UniqueItems() & [...=~".*\\S.*"]
		assessment_rationale!: =~".*\\S.*"
		claimed_matches!: list.UniqueItems() & [...close({
			authority_class!: "canonical" | "candidate" | "local" | "narrative" | "historical"
			authority_scope!: close({
				kind!: "repository" | "project" | "feature" | "artifact"
				ref!:  =~".*\\S.*"
			})
			definition_id!: matchN(1, [=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$", null])
			kind!:     "id" | "term" | "alias" | "normalized-collision" | "semantic-overlap" | "consumer-use"
			match_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			source_ref!: matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})
			term!: =~".*\\S.*"
		})]
		evidence_refs!: list.UniqueItems() & [...matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})] & [_, ...]
		intended_scope!: close({
			kind!: "repository" | "project" | "feature" | "artifact"
			ref!:  =~".*\\S.*"
		})
		intent!:   =~".*\\S.*"
		probe_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		proposed_basis_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		proposed_disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing" | "canonical-change-proposal" | "blocked-conflict"
		term!:                 =~".*\\S.*"
	})

	#consumer: close({
		consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		kind!:            "narrative" | "protocol" | "schema" | "runtime" | "index" | "other"
		reason_in_scope!: =~".*\\S.*"
		source_ref!: matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})
	})

	#consumerBoundary: matchN(2, [matchIf({
		classification!: "catalogued"
	}, {
		consumers?: null | bool | number | string | [_, ...] | {}
		rationale?: null
	}, _) & {}, matchIf({
		classification!: "none-with-rationale"
	}, {
		consumers?: null | bool | number | string | list.MaxItems(0) | {}
		rationale?: =~".*\\S.*"
	}, _) & {}]) & close({
		classification!: "catalogued" | "none-with-rationale"
		consumers!: list.UniqueItems() & [...close({
			consumer_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			kind!:            "narrative" | "protocol" | "schema" | "runtime" | "index" | "other"
			reason_in_scope!: =~".*\\S.*"
			source_ref!: matchN(5, [matchIf({
				selector_type!: "whole-file"
			}, {
				selector?: "$"
			}, _) & {}, matchIf({
				selector_type!: "heading" | "anchor"
			}, {
				format?: "markdown"
			}, _) & {}, matchIf({
				selector_type!: "json-pointer"
			}, {
				format?:   "json"
				selector?: =~"^/"
			}, _) & {}, matchIf({
				selector_type!: "yaml-path"
			}, {
				format?: "yaml"
			}, _) & {}, matchIf({
				selector_type!: "symbol"
			}, {
				format?: "markdown" | "yaml" | "text"
			}, _) & {}]) & close({
				format!:        "markdown" | "json" | "yaml" | "text"
				path!:          string
				selector!:      =~".*\\S.*"
				selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
				sha256!:        =~"^[a-f0-9]{64}$"
				size!:          int & >=0
				visibility!:    "public" | "private"
			})
		})]
		rationale!: matchN(1, [=~".*\\S.*", null])
	})

	#digest: =~"^[a-f0-9]{64}$"

	#discoveryContract: close({
		claim_scope!: "configured-roots-complete"
		profile!:     "semantic-surface-v1"
		roots!: list.UniqueItems() & [...close({
			consumer_globs!: ["**/*.md"]
			path!: string
			registry_globs!: ["**/DEFINITIONS.md", "**/DEFINITIONS-INDEX.md", "**/DEFINITIONS.json", "**/GLOSSARY.md"]
			root_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			visibility!: "public" | "private"
		})] & [_, ...]
	})

	#discoveryRoot: close({
		consumer_globs!: ["**/*.md"]
		path!: string
		registry_globs!: ["**/DEFINITIONS.md", "**/DEFINITIONS-INDEX.md", "**/DEFINITIONS.json", "**/GLOSSARY.md"]
		root_id!:    =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		visibility!: "public" | "private"
	})

	#exclusion: close({
		evidence_ref!: matchN(5, [matchIf({
			selector_type!: "whole-file"
		}, {
			selector?: "$"
		}, _) & {}, matchIf({
			selector_type!: "heading" | "anchor"
		}, {
			format?: "markdown"
		}, _) & {}, matchIf({
			selector_type!: "json-pointer"
		}, {
			format?:   "json"
			selector?: =~"^/"
		}, _) & {}, matchIf({
			selector_type!: "yaml-path"
		}, {
			format?: "yaml"
		}, _) & {}, matchIf({
			selector_type!: "symbol"
		}, {
			format?: "markdown" | "yaml" | "text"
		}, _) & {}]) & close({
			format!:        "markdown" | "json" | "yaml" | "text"
			path!:          string
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			sha256!:        =~"^[a-f0-9]{64}$"
			size!:          int & >=0
			visibility!:    "public" | "private"
		})
		exclusion_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		reason!:       =~".*\\S.*"
		selector!:     string
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#materialRef: matchN(5, [matchIf({
		selector_type!: "whole-file"
	}, {
		selector?: "$"
	}, _) & {}, matchIf({
		selector_type!: "heading" | "anchor"
	}, {
		format?: "markdown"
	}, _) & {}, matchIf({
		selector_type!: "json-pointer"
	}, {
		format?:   "json"
		selector?: =~"^/"
	}, _) & {}, matchIf({
		selector_type!: "yaml-path"
	}, {
		format?: "yaml"
	}, _) & {}, matchIf({
		selector_type!: "symbol"
	}, {
		format?: "markdown" | "yaml" | "text"
	}, _) & {}]) & close({
		format!:        "markdown" | "json" | "yaml" | "text"
		path!:          string
		selector!:      =~".*\\S.*"
		selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
		sha256!:        =~"^[a-f0-9]{64}$"
		size!:          int & >=0
		visibility!:    "public" | "private"
	})

	#nonEmpty: =~".*\\S.*"

	#publicMaterialRef: matchN(2, [matchN(5, [matchIf({
		selector_type!: "whole-file"
	}, {
		selector?: "$"
	}, _) & {}, matchIf({
		selector_type!: "heading" | "anchor"
	}, {
		format?: "markdown"
	}, _) & {}, matchIf({
		selector_type!: "json-pointer"
	}, {
		format?:   "json"
		selector?: =~"^/"
	}, _) & {}, matchIf({
		selector_type!: "yaml-path"
	}, {
		format?: "yaml"
	}, _) & {}, matchIf({
		selector_type!: "symbol"
	}, {
		format?: "markdown" | "yaml" | "text"
	}, _) & {}]) & close({
		format!:        "markdown" | "json" | "yaml" | "text"
		path!:          string
		selector!:      =~".*\\S.*"
		selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
		sha256!:        =~"^[a-f0-9]{64}$"
		size!:          int & >=0
		visibility!:    "public" | "private"
	}), {
		visibility!: "public"
	}])

	#relativePath: string
}

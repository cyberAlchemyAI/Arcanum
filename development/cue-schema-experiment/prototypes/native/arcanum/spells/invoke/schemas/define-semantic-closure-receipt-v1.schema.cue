// Invoke Define Semantic Closure Receipt v1
//
// Independent, failure-capable inspection of one exact Define semantic context.
// The receipt classifies the finite denominator and returns a typed routing
// outcome without defining or promoting terminology.
package prototype

import "list"

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/invoke/define-semantic-closure-receipt/v1")
	matchN(3, [matchIf({
		outcome!: "ready-for-define"
	}, {
		authority_resolution?: null | bool | number | string | [...] | {
			status!: "resolved"
		}
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		checks?: null | bool | number | string | [...null | bool | number | string | [...] | {
			status!: "pass"
		}] | {}
		inspected_sources?: null | bool | number | string | [...null | bool | number | string | [...] | {
			causal_blocker_ids!: null | bool | number | string | list.MaxItems(0) | {}
			status!: "current" | "excluded"
		}] | {}
		next_route?: "define-v3"
		probe_results?: null | bool | number | string | [...null | bool | number | string | [...] | {
			causal_blocker_ids!: null | bool | number | string | list.MaxItems(0) | {}
			disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing"
		}] | {}
	}, _) & {}, matchIf({
		outcome!: "definitions-governance-required"
	}, {
		authority_resolution?: null | bool | number | string | [...] | {
			status!: "resolved"
		}
		blockers?: null | bool | number | string | list.MaxItems(0) | {}
		checks?: null | bool | number | string | [...null | bool | number | string | [...] | {
			status!: "pass"
		}] | {}
		inspected_sources?: null | bool | number | string | [...null | bool | number | string | [...] | {
			causal_blocker_ids!: null | bool | number | string | list.MaxItems(0) | {}
			status!: "current" | "excluded"
		}] | {}
		next_route?: "definitions-governance"
		probe_results?: null | bool | number | string | list.MatchN(>=1, null | bool | number | string | [...] | {
			disposition!: "canonical-change-proposal"
		}) & [...null | bool | number | string | [...] | {
			causal_blocker_ids!: null | bool | number | string | list.MaxItems(0) | {}
			disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing" | "canonical-change-proposal"
		}] | {}
	}, _) & {}, matchIf({
		outcome!: "blocked"
	}, {
		blockers?: null | bool | number | string | [_, ...] | {}
		next_route?: "stop"
	}, _) & {}]) & close({
		$schema!: "https://arcanum.dev/schemas/invoke/define-semantic-closure-receipt/v1"
		assessment!: close({
			assessed_by!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			authored_by!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})
		authority_effect!: "none"
		authority_resolution!: matchN(2, [matchIf({
			status!: "resolved"
		}, {
			canonical_source_refs?: null | bool | number | string | [_, ...] | {}
			evidence_refs?: null | bool | number | string | [_, ...] | {}
			index_refs?: null | bool | number | string | [_, ...] | {}
		}, _) & {}, matchIf({
			status!: "absent"
		}, {
			canonical_source_refs?: null | bool | number | string | list.MaxItems(0) | {}
			index_refs?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}]) & close({
			canonical_source_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			index_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			owner!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			status!: "resolved" | "absent" | "ambiguous"
		})
		blockers!: list.UniqueItems() & [...close({
			blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			code!:         =~"^[A-Z][A-Z0-9_]{2,127}$"
			message!:      =~".*\\S.*"
			owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			repair_route!: =~".*\\S.*"
		})]
		checks!: list.MaxItems(8) & list.UniqueItems() & [matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:authority-resolution"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:source-freshness"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:probe-coverage"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:canonical-index-parity"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:normalized-collision"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:semantic-overlap"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:consumer-coverage"
		}]), matchN(2, [matchN(2, [matchIf({
			status!: "pass"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			status!: "block" | "not_evaluable"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			evidence_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			status!: "pass" | "block" | "not_evaluable"
		}), {
			check_id?: "check:independent-owner"
		}])] & [_, _, _, _, _, _, _, _, ...]
		claim_scope!: "configured-roots-complete"
		context_ref!: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
		discovery_snapshots!: list.UniqueItems() & [...close({
			consumer_paths!: list.UniqueItems() & [...string]
			content_refs!: list.UniqueItems() & [...close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})]
			excluded_paths!: list.UniqueItems() & [...string]
			membership_digest!: =~"^[a-f0-9]{64}$"
			path!:              string
			registry_paths!: list.UniqueItems() & [...string]
			root_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		})] & [_, ...]
		inspected_sources!: list.UniqueItems() & [...matchN(2, [matchIf({
			status!: "current" | "excluded"
		}, {
			causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
			observed_ref?: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		}, _) & {}, matchIf({
			status!: "missing" | "stale" | "conflicting"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			declared_path!: string
			format!:        "markdown" | "json" | "yaml" | "text"
			inspection_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			observed_ref!: matchN(1, [close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			}), null])
			role!:          "canonical-source" | "canonical-index" | "candidate-registry" | "local-glossary" | "consumer" | "resolution-evidence" | "discovery-source" | "probe-evidence" | "exclusion-evidence" | "historical"
			selector!:      =~".*\\S.*"
			selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
			status!:        "current" | "missing" | "stale" | "excluded" | "conflicting"
			visibility!:    "public" | "private"
		})] & [_, ...]
		next_route!: "define-v3" | "definitions-governance" | "stop"
		outcome!:    "ready-for-define" | "definitions-governance-required" | "blocked"
		probe_results!: list.UniqueItems() & [...matchN(3, [matchIf({
			disposition!: "new-scoped-term"
		}, {
			basis_ids?: null | bool | number | string | list.MaxItems(0) | {}
		}, _) & {}, matchIf({
			disposition!: "reuse-existing" | "specialize-existing" | "canonical-change-proposal"
		}, {
			basis_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}, matchIf({
			disposition!: "blocked-conflict"
		}, {
			causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
		}, _) & {}]) & close({
			basis_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
			disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing" | "canonical-change-proposal" | "blocked-conflict"
			matches!: list.UniqueItems() & [...close({
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
			probe_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
			rationale!: =~".*\\S.*"
		})] & [_, ...]
		receipt_digest!: =~"^[a-f0-9]{64}$"
		receipt_id!:     =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		schema_bindings!: close({
			context_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
			receipt_schema_ref!: close({
				path!:   string
				sha256!: =~"^[a-f0-9]{64}$"
				size!:   int & >=0
			})
		})
		schema_version!: "invoke.define-semantic-closure-receipt.v1"
		validator!: close({
			identity!: "invoke.validate-define-semantic-closure.v1"
			owner!:    "invoke-define-semantic-closure-validator"
			path!:     "arcanum/spells/invoke/scripts/validate_define_semantic_closure.py"
			sha256!:   =~"^[a-f0-9]{64}$"
		})
		visibility_boundary!: close({
			discovery_roots!: list.UniqueItems() & [...string] & [_, ...]
			public_roots!: list.UniqueItems() & [...string]
			repository_root!: "."
			source!:          "validator-invocation"
		})
	})

	#authorityResolution: matchN(2, [matchIf({
		status!: "resolved"
	}, {
		canonical_source_refs?: null | bool | number | string | [_, ...] | {}
		evidence_refs?: null | bool | number | string | [_, ...] | {}
		index_refs?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		status!: "absent"
	}, {
		canonical_source_refs?: null | bool | number | string | list.MaxItems(0) | {}
		index_refs?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}]) & close({
		canonical_source_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		index_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		owner!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		status!: "resolved" | "absent" | "ambiguous"
	})

	#authorityResolutionCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:authority-resolution"
	}])

	#blocker: close({
		blocker_id!:   =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		code!:         =~"^[A-Z][A-Z0-9_]{2,127}$"
		message!:      =~".*\\S.*"
		owner!:        =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		repair_route!: =~".*\\S.*"
	})

	#canonicalIndexParityCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:canonical-index-parity"
	}])

	#check: matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	})

	#consumerCoverageCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:consumer-coverage"
	}])

	#digest: =~"^[a-f0-9]{64}$"

	#discoverySnapshot: close({
		consumer_paths!: list.UniqueItems() & [...string]
		content_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		excluded_paths!: list.UniqueItems() & [...string]
		membership_digest!: =~"^[a-f0-9]{64}$"
		path!:              string
		registry_paths!: list.UniqueItems() & [...string]
		root_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
	})

	#exactRef: close({
		path!:   string
		sha256!: =~"^[a-f0-9]{64}$"
		size!:   int & >=0
	})

	#id: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"

	#independentOwnerCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:independent-owner"
	}])

	#inspectedSource: matchN(2, [matchIf({
		status!: "current" | "excluded"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
		observed_ref?: close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})
	}, _) & {}, matchIf({
		status!: "missing" | "stale" | "conflicting"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		declared_path!: string
		format!:        "markdown" | "json" | "yaml" | "text"
		inspection_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		observed_ref!: matchN(1, [close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		}), null])
		role!:          "canonical-source" | "canonical-index" | "candidate-registry" | "local-glossary" | "consumer" | "resolution-evidence" | "discovery-source" | "probe-evidence" | "exclusion-evidence" | "historical"
		selector!:      =~".*\\S.*"
		selector_type!: "whole-file" | "heading" | "anchor" | "json-pointer" | "yaml-path" | "symbol"
		status!:        "current" | "missing" | "stale" | "excluded" | "conflicting"
		visibility!:    "public" | "private"
	})

	#match: close({
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

	#normalizedCollisionCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:normalized-collision"
	}])

	#probeCoverageCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:probe-coverage"
	}])

	#probeResult: matchN(3, [matchIf({
		disposition!: "new-scoped-term"
	}, {
		basis_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		disposition!: "reuse-existing" | "specialize-existing" | "canonical-change-proposal"
	}, {
		basis_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}, matchIf({
		disposition!: "blocked-conflict"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		basis_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		disposition!: "reuse-existing" | "new-scoped-term" | "specialize-existing" | "canonical-change-proposal" | "blocked-conflict"
		matches!: list.UniqueItems() & [...close({
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
		probe_id!:  =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		rationale!: =~".*\\S.*"
	})

	#relativePath: string

	#semanticOverlapCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:semantic-overlap"
	}])

	#sourceFreshnessCheck: matchN(2, [matchN(2, [matchIf({
		status!: "pass"
	}, {
		causal_blocker_ids?: null | bool | number | string | list.MaxItems(0) | {}
	}, _) & {}, matchIf({
		status!: "block" | "not_evaluable"
	}, {
		causal_blocker_ids?: null | bool | number | string | [_, ...] | {}
	}, _) & {}]) & close({
		causal_blocker_ids!: list.UniqueItems() & [...=~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"]
		check_id!: =~"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$"
		evidence_refs!: list.UniqueItems() & [...close({
			path!:   string
			sha256!: =~"^[a-f0-9]{64}$"
			size!:   int & >=0
		})]
		status!: "pass" | "block" | "not_evaluable"
	}), {
		check_id?: "check:source-freshness"
	}])
}

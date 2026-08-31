// WorkPackReadinessAuditConfigV2
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/config/2-0-0")
	matchIf({
		admission_timing!: "selected-unit-at-task-session"
	}, {
		execution_bindings?: null | bool | number | string | [...matchN(2, [close({
			allowed_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			attempt_contract?: close({
				collision_policy!: strings.MinRunes(1)
				failure_teardown!: strings.MinRunes(1)
				id_policy!:        strings.MinRunes(1)
				success_teardown!: strings.MinRunes(1)
			})
			authority_class?: "public" | "private"
			byte_baselines!: [...close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[a-f0-9]{64}$"
			})]
			canonical_successors!: list.UniqueItems() & [...strings.MinRunes(1)]
			command!: close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				cwd!:        strings.MinRunes(1)
				risk_class!: "read-only" | "bounded-write" | "browser" | "network"
			})
			dependencies!: list.UniqueItems() & [...strings.MinRunes(1)]
			execution_outputs!: list.UniqueItems() & [...strings.MinRunes(1)]
			lifecycle_owner?: strings.MinRunes(1)
			material_package!: close({
				declared_sha256!: null | =~"^[a-f0-9]{64}$"
				package_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				producer_owner_ref!: null | strings.MinRunes(1)
				producer_receipt_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				schema_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				target_inventory_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
			})
			material_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			output_contracts!: [...matchN(1, [{
				schema_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
			}, {
				semantic_predicate!: string
			}]) & close({
				disposition!:      "create" | "update" | "delete" | "transient"
				expected_path!:    strings.MinRunes(1)
				failure_behavior!: "block-before-successor"
				producer_id!:      strings.MinRunes(1)
				schema_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				semantic_predicate!: null | strings.MinRunes(1)
				validation_phase!:   "post-produce" | "closeout"
			})]
			producer_id!:       strings.MinRunes(1)
			publication_class?: "public" | "private" | "internal"
			swu_id?:            strings.MinRunes(1)
			target_dispositions!: [...close({
				baseline_obligation!: "none" | "required-at-admission"
				collision_policy!:    "fail-if-exists" | "replace-declared" | "not-applicable"
				disposition!:         "create" | "update" | "delete" | "read" | "transient"
				parent_path!:         strings.MinRunes(1)
				path!:                strings.MinRunes(1)
				producer_id!:         null | strings.MinRunes(1)
			})] & [_, ...]
			task_id?: strings.MinRunes(1)
			unit_id!: strings.MinRunes(1)
			validation_contracts!: [...close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				command_id!:       strings.MinRunes(1)
				cwd!:              strings.MinRunes(1)
				max_output_bytes!: int & <=16777216 & >=1
				phase!:            "pre-execution" | "post-produce" | "closeout"
				timeout_seconds!:  int & <=86400 & >=1
			})] & [_, ...]
		}), {
			task_id!:              _
			swu_id!:               _
			lifecycle_owner!:      _
			authority_class!:      _
			publication_class!:    _
			attempt_contract!:     _
			validation_contracts!: _
		}])] | {}
		runtime_binding?: null | bool | number | string | [...] | {
			task_session_admission_receipt_ref?: null
		}
		execution_policy!: _
	}, _) & {} & close({
		admission_timing?: "full-frontier" | "selected-unit-at-task-session"
		approval_policy!: close({
			allowed_audit_verdicts!: list.UniqueItems() & [..."pass" | "flag"] & [_, ...]
			allowed_flag_classes!: list.UniqueItems() & [..."observability-residue"]
			approval_owner_ref!: strings.MinRunes(1)
			decision_gate_receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			risk_policy_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			run_budget!: close({
				max_task_session_requests!: int & >=1
			})
		})
		audit_id!: strings.MinRunes(1)
		authority_bindings!: close({
			canonical_authority_refs!: [...close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})] & [_, ...]
			semantic_bindings!: close({
				closeout!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				material!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				owner!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				receipt!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				validation!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
			})
		})
		classifier_version!: strings.MinRunes(1)
		closeout_bindings!: [...close({
			allowed_delta_policy_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			compensation!: matchN(1, [close({
				mode!:      "none"
				rationale!: strings.MinRunes(1)
			}), close({
				contract_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				mode!:      "owner-routed"
				owner_ref!: strings.MinRunes(1)
			})])
			owner_receipt_contract_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			unit_id!: strings.MinRunes(1)
		})] & [_, ...]
		closure_receipt_refs!: [...close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})] & [_, ...]
		continuity_projection!: close({
			completed_unit_receipt_refs!: [...close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})]
			cursor!: strings.MinRunes(1)
			joined_closeout_receipt_refs!: [...matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), close({
				binding_id!: strings.MinRunes(1)
				continuation_cursor_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				evidence_profile!: "task-session-joined-owner-closeout-v1"
				joined_owner_receipt_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				owner_receipt_schema_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				owner_ref!: "task-session"
				terminal_receipt_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
			})])]
			projected_next_successor!: close({
				authority_effect!: "none"
				canonical_successor_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				continuation_router_verification_receipt_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				equivalence_validator_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				projection_owner_ref!: strings.MinRunes(1)
				unit_id!:              null | string
			})
		})
		evidence_ceiling!: "frozen-input-contractual-readiness"
		execution_bindings!: [...close({
			allowed_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			attempt_contract?: close({
				collision_policy!: strings.MinRunes(1)
				failure_teardown!: strings.MinRunes(1)
				id_policy!:        strings.MinRunes(1)
				success_teardown!: strings.MinRunes(1)
			})
			authority_class?: "public" | "private"
			byte_baselines!: [...close({
				path!:   strings.MinRunes(1)
				sha256!: =~"^[a-f0-9]{64}$"
			})]
			canonical_successors!: list.UniqueItems() & [...strings.MinRunes(1)]
			command!: close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				cwd!:        strings.MinRunes(1)
				risk_class!: "read-only" | "bounded-write" | "browser" | "network"
			})
			dependencies!: list.UniqueItems() & [...strings.MinRunes(1)]
			execution_outputs!: list.UniqueItems() & [...strings.MinRunes(1)]
			lifecycle_owner?: strings.MinRunes(1)
			material_package!: close({
				declared_sha256!: null | =~"^[a-f0-9]{64}$"
				package_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				producer_owner_ref!: null | strings.MinRunes(1)
				producer_receipt_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				schema_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				target_inventory_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
			})
			material_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			output_contracts!: [...matchN(1, [{
				schema_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
			}, {
				semantic_predicate!: string
			}]) & close({
				disposition!:      "create" | "update" | "delete" | "transient"
				expected_path!:    strings.MinRunes(1)
				failure_behavior!: "block-before-successor"
				producer_id!:      strings.MinRunes(1)
				schema_ref!: matchN(1, [close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				}), null])
				semantic_predicate!: null | strings.MinRunes(1)
				validation_phase!:   "post-produce" | "closeout"
			})]
			producer_id!:       strings.MinRunes(1)
			publication_class?: "public" | "private" | "internal"
			swu_id?:            strings.MinRunes(1)
			target_dispositions!: [...close({
				baseline_obligation!: "none" | "required-at-admission"
				collision_policy!:    "fail-if-exists" | "replace-declared" | "not-applicable"
				disposition!:         "create" | "update" | "delete" | "read" | "transient"
				parent_path!:         strings.MinRunes(1)
				path!:                strings.MinRunes(1)
				producer_id!:         null | strings.MinRunes(1)
			})] & [_, ...]
			task_id?: strings.MinRunes(1)
			unit_id!: strings.MinRunes(1)
			validation_contracts!: [...close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				command_id!:       strings.MinRunes(1)
				cwd!:              strings.MinRunes(1)
				max_output_bytes!: int & <=16777216 & >=1
				phase!:            "pre-execution" | "post-produce" | "closeout"
				timeout_seconds!:  int & <=86400 & >=1
			})] & [_, ...]
		})] & [_, ...]
		execution_entry_closure?: close({
			closure_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			rehearsal_effect!: "deterministic-no-effect"
			units_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			validator_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!:   strings.MinRunes(1)
				binding_mode!: "opaque-exact-artifact"
				owner_ref!:    strings.MinRunes(1)
			})
		})
		execution_policy?: close({
			allowed_routes!: [...close({
				capability!:       strings.MinRunes(1)
				effect_class!:     "repository-local-reversible"
				expected_receipt!: strings.MinRunes(1)
				frontier_swu!:     strings.MinRunes(1)
				mode!:             strings.MinRunes(1)
				required_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
				route_id!: strings.MinRunes(1)
				target!:   strings.MinRunes(1)
				write_scope!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			})] & [_, ...]
			allowed_routes_digest!: =~"^[a-f0-9]{64}$"
			automatic_decisions!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			route_policy!: "automatic-in-scope"
			scope_source!: "exact-work-pack-and-captured-frontier"
			stop_decisions!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			validation_policy!: "owner-gates-remain-mandatory"
			work_pack_id!:      strings.MinRunes(1)
		})
		expected_material_digests?: [string]: =~"^[a-f0-9]{64}$"
		expected_semantic_digest?:        null | =~"^[a-f0-9]{64}$"
		expected_source_snapshot_digest?: null | =~"^[a-f0-9]{64}$"
		lifecycle_status_refs!: close({
			approval_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			audit_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			chain_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			plan_artifact_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
		})
		objective_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		receipt_bindings!: close({
			expected_receipt_refs!: [...close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})] & [_, ...]
			semantic_validator_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!:   strings.MinRunes(1)
				binding_mode!: "opaque-exact-artifact"
				owner_ref!:    strings.MinRunes(1)
			}), null])
			terminal_schema_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
		})
		repository_root!: "."
		runtime_binding!: close({
			requested_task_session_execution_mode!: strings.MinRunes(1)
			task_session_admission_receipt_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
		})
		schema_version!: "2.0.0"
		status_receipt_refs!: close({
			artifact_authored_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			audit_verdict!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			mutation_runtime_ready_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
			registry_released_status!: close({
				owner_ref!: strings.MinRunes(1)
				receipt_ref!: close({
					artifact_ref!: close({
						path!:       strings.MinRunes(1)
						sha256!:     =~"^[a-f0-9]{64}$"
						size_bytes!: int & >=0
					})
					binding_id!: strings.MinRunes(1)
					owner_ref!:  strings.MinRunes(1)
					selector!:   string
				})
				value!: strings.MinRunes(1)
			})
		})
		task_session_closeout_contracts?: [...close({
			continuation_router_schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			continuity_schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			declared_owner_receipt_schema_identity!: strings.MinRunes(1)
			expected_owner_receipt_schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			final_terminal_schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			precloseout_execution_schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			receipt_profile!: "precloseout-execution-v1"
			unit_id!:         strings.MinRunes(1)
		})] & [_, ...]
	})

	#allowedRoute: close({
		capability!:       strings.MinRunes(1)
		effect_class!:     "repository-local-reversible"
		expected_receipt!: strings.MinRunes(1)
		frontier_swu!:     strings.MinRunes(1)
		mode!:             strings.MinRunes(1)
		required_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		route_id!: strings.MinRunes(1)
		target!:   strings.MinRunes(1)
		write_scope!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
	})

	#attemptContract: close({
		collision_policy!: strings.MinRunes(1)
		failure_teardown!: strings.MinRunes(1)
		id_policy!:        strings.MinRunes(1)
		success_teardown!: strings.MinRunes(1)
	})

	#bindingRef: close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		binding_id!: strings.MinRunes(1)
		owner_ref!:  strings.MinRunes(1)
		selector!:   string
	})

	#byteBaseline: close({
		path!:   strings.MinRunes(1)
		sha256!: =~"^[a-f0-9]{64}$"
	})

	#command: close({
		argv!: [...strings.MinRunes(1)] & [_, ...]
		cwd!:        strings.MinRunes(1)
		risk_class!: "read-only" | "bounded-write" | "browser" | "network"
	})

	#compensation: matchN(1, [close({
		mode!:      "none"
		rationale!: strings.MinRunes(1)
	}), close({
		contract_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		mode!:      "owner-routed"
		owner_ref!: strings.MinRunes(1)
	})])

	#exactArtifactRef: close({
		path!:       strings.MinRunes(1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#executionBinding: close({
		allowed_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
		attempt_contract?: close({
			collision_policy!: strings.MinRunes(1)
			failure_teardown!: strings.MinRunes(1)
			id_policy!:        strings.MinRunes(1)
			success_teardown!: strings.MinRunes(1)
		})
		authority_class?: "public" | "private"
		byte_baselines!: [...close({
			path!:   strings.MinRunes(1)
			sha256!: =~"^[a-f0-9]{64}$"
		})]
		canonical_successors!: list.UniqueItems() & [...strings.MinRunes(1)]
		command!: close({
			argv!: [...strings.MinRunes(1)] & [_, ...]
			cwd!:        strings.MinRunes(1)
			risk_class!: "read-only" | "bounded-write" | "browser" | "network"
		})
		dependencies!: list.UniqueItems() & [...strings.MinRunes(1)]
		execution_outputs!: list.UniqueItems() & [...strings.MinRunes(1)]
		lifecycle_owner?: strings.MinRunes(1)
		material_package!: close({
			declared_sha256!: null | =~"^[a-f0-9]{64}$"
			package_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			producer_owner_ref!: null | strings.MinRunes(1)
			producer_receipt_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			schema_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			target_inventory_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
		})
		material_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
		output_contracts!: [...matchN(1, [{
			schema_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
		}, {
			semantic_predicate!: string
		}]) & close({
			disposition!:      "create" | "update" | "delete" | "transient"
			expected_path!:    strings.MinRunes(1)
			failure_behavior!: "block-before-successor"
			producer_id!:      strings.MinRunes(1)
			schema_ref!: matchN(1, [close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			}), null])
			semantic_predicate!: null | strings.MinRunes(1)
			validation_phase!:   "post-produce" | "closeout"
		})]
		producer_id!:       strings.MinRunes(1)
		publication_class?: "public" | "private" | "internal"
		swu_id?:            strings.MinRunes(1)
		target_dispositions!: [...close({
			baseline_obligation!: "none" | "required-at-admission"
			collision_policy!:    "fail-if-exists" | "replace-declared" | "not-applicable"
			disposition!:         "create" | "update" | "delete" | "read" | "transient"
			parent_path!:         strings.MinRunes(1)
			path!:                strings.MinRunes(1)
			producer_id!:         null | strings.MinRunes(1)
		})] & [_, ...]
		task_id?: strings.MinRunes(1)
		unit_id!: strings.MinRunes(1)
		validation_contracts!: [...close({
			argv!: [...strings.MinRunes(1)] & [_, ...]
			command_id!:       strings.MinRunes(1)
			cwd!:              strings.MinRunes(1)
			max_output_bytes!: int & <=16777216 & >=1
			phase!:            "pre-execution" | "post-produce" | "closeout"
			timeout_seconds!:  int & <=86400 & >=1
		})] & [_, ...]
	})

	#executionPolicy: close({
		allowed_routes!: [...close({
			capability!:       strings.MinRunes(1)
			effect_class!:     "repository-local-reversible"
			expected_receipt!: strings.MinRunes(1)
			frontier_swu!:     strings.MinRunes(1)
			mode!:             strings.MinRunes(1)
			required_inputs!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
			route_id!: strings.MinRunes(1)
			target!:   strings.MinRunes(1)
			write_scope!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		})] & [_, ...]
		allowed_routes_digest!: =~"^[a-f0-9]{64}$"
		automatic_decisions!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		route_policy!: "automatic-in-scope"
		scope_source!: "exact-work-pack-and-captured-frontier"
		stop_decisions!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		validation_policy!: "owner-gates-remain-mandatory"
		work_pack_id!:      strings.MinRunes(1)
	})

	#joinedOwnerCloseoutEvidence: close({
		binding_id!: strings.MinRunes(1)
		continuation_cursor_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		evidence_profile!: "task-session-joined-owner-closeout-v1"
		joined_owner_receipt_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		owner_receipt_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		owner_ref!: "task-session"
		terminal_receipt_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
	})

	#lifecycleRefs: close({
		approval_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		audit_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		chain_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		plan_artifact_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
	})

	#materialPackage: close({
		declared_sha256!: null | =~"^[a-f0-9]{64}$"
		package_ref!: matchN(1, [close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		}), null])
		producer_owner_ref!: null | strings.MinRunes(1)
		producer_receipt_ref!: matchN(1, [close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		}), null])
		schema_ref!: matchN(1, [close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		}), null])
		target_inventory_ref!: matchN(1, [close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		}), null])
	})

	#nullableBindingRef: matchN(1, [close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		binding_id!: strings.MinRunes(1)
		owner_ref!:  strings.MinRunes(1)
		selector!:   string
	}), null])

	#nullableSemanticValidatorBindingRef: matchN(1, [close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		binding_id!: strings.MinRunes(1)
		owner_ref!:  strings.MinRunes(1)
		selector!:   string
	}), close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		binding_id!:   strings.MinRunes(1)
		binding_mode!: "opaque-exact-artifact"
		owner_ref!:    strings.MinRunes(1)
	}), null])

	#opaqueExactArtifactBindingRef: close({
		artifact_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		binding_id!:   strings.MinRunes(1)
		binding_mode!: "opaque-exact-artifact"
		owner_ref!:    strings.MinRunes(1)
	})

	#outputContract: matchN(1, [{
		schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
	}, {
		semantic_predicate!: string
	}]) & close({
		disposition!:      "create" | "update" | "delete" | "transient"
		expected_path!:    strings.MinRunes(1)
		failure_behavior!: "block-before-successor"
		producer_id!:      strings.MinRunes(1)
		schema_ref!: matchN(1, [close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		}), null])
		semantic_predicate!: null | strings.MinRunes(1)
		validation_phase!:   "post-produce" | "closeout"
	})

	#status: close({
		owner_ref!: strings.MinRunes(1)
		receipt_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		value!: strings.MinRunes(1)
	})

	#statusRefs: close({
		artifact_authored_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		audit_verdict!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		mutation_runtime_ready_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
		registry_released_status!: close({
			owner_ref!: strings.MinRunes(1)
			receipt_ref!: close({
				artifact_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				binding_id!: strings.MinRunes(1)
				owner_ref!:  strings.MinRunes(1)
				selector!:   string
			})
			value!: strings.MinRunes(1)
		})
	})

	#structuredValidationCommand: close({
		argv!: [...strings.MinRunes(1)] & [_, ...]
		command_id!:       strings.MinRunes(1)
		cwd!:              strings.MinRunes(1)
		max_output_bytes!: int & <=16777216 & >=1
		phase!:            "pre-execution" | "post-produce" | "closeout"
		timeout_seconds!:  int & <=86400 & >=1
	})

	#targetDisposition: close({
		baseline_obligation!: "none" | "required-at-admission"
		collision_policy!:    "fail-if-exists" | "replace-declared" | "not-applicable"
		disposition!:         "create" | "update" | "delete" | "read" | "transient"
		parent_path!:         strings.MinRunes(1)
		path!:                strings.MinRunes(1)
		producer_id!:         null | strings.MinRunes(1)
	})

	#taskSessionCloseoutContract: close({
		continuation_router_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		continuity_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		declared_owner_receipt_schema_identity!: strings.MinRunes(1)
		expected_owner_receipt_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		final_terminal_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		precloseout_execution_schema_ref!: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			binding_id!: strings.MinRunes(1)
			owner_ref!:  strings.MinRunes(1)
			selector!:   string
		})
		receipt_profile!: "precloseout-execution-v1"
		unit_id!:         strings.MinRunes(1)
	})
}

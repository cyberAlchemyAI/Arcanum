// WorkPackReadinessAuditConfig
package prototype

import (
	"strings"
	"list"
	"struct"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/work-pack-readiness-audit/config/1-0-0")
	close({
		audit_id!:        strings.MinRunes(1)
		authority_class!: "public" | "private"
		closeout_directory!: close({
			create_if_missing!: bool
			path!:              strings.MinRunes(1)
		})
		control_artifacts!: list.UniqueItems() & [...close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})] & [_, ...]
		handoff_state?: close({
			artifact_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			expected_fields!: struct.MinFields(1)
		})
		immutable_paths!: list.UniqueItems() & [...strings.MinRunes(1)]
		next_owner!:        "invoke:refresh"
		publication_class!: "public" | "private" | "internal"
		refresh_targets!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		repository_root!: "."
		schema_version!:  "1.0.0"
		shared_write_owners!: [...close({
			ordered_units!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, _, ...]
			owner!: strings.MinRunes(1)
			path!:  strings.MinRunes(1)
		})]
		source_selectors!: list.UniqueItems() & [...strings.MinRunes(1)] & [_, ...]
		task_session_request_schema!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		terminal_receipt_schema!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		terminal_receipt_semantic_validator?: matchN(1, [close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		}), null])
		units!: [...close({
			allowed_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			attempt!: close({
				collision_policy!: "fail-if-exists" | "append-only"
				id_algorithm!:     string
				required!:         bool
				retention_policy!: "retain-receipt-only" | "retain-all" | "ephemeral"
				teardown_on_failure!: [...close({
					argv!: [...strings.MinRunes(1)] & [_, ...]
					cwd!: strings.MinRunes(1)
					environment!: [string]: string
					expected_exit_code!: int
					risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
					runtime_identity!: close({
						executable!:     strings.MinRunes(1)
						hash_policy!:    strings.MinRunes(1)
						version_policy!: strings.MinRunes(1)
					})
					timeout_seconds!: int & >=1
				})]
				teardown_on_success!: [...close({
					argv!: [...strings.MinRunes(1)] & [_, ...]
					cwd!: strings.MinRunes(1)
					environment!: [string]: string
					expected_exit_code!: int
					risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
					runtime_identity!: close({
						executable!:     strings.MinRunes(1)
						hash_policy!:    strings.MinRunes(1)
						version_policy!: strings.MinRunes(1)
					})
					timeout_seconds!: int & >=1
				})]
			})
			closeout_receipt!: strings.MinRunes(1)
			contract_kind!:    "full-task" | "row-only"
			contract_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			dependencies!: list.UniqueItems() & [...strings.MinRunes(1)]
			dependency_receipts!: [...close({
				dependency_id!:    strings.MinRunes(1)
				expected_status!:  "pass"
				expected_step_id!: strings.MinRunes(1)
				expected_unit_id!: strings.MinRunes(1)
				receipt_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				work_pack_sha256!: =~"^[a-f0-9]{64}$"
			})]
			dispatch_step!: strings.MinRunes(1)
			execution_outputs!: list.UniqueItems() & [...strings.MinRunes(1)]
			material_package?: matchN(1, [close({
				package_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
				receipt_ref!: close({
					path!:       strings.MinRunes(1)
					sha256!:     =~"^[a-f0-9]{64}$"
					size_bytes!: int & >=0
				})
			}), null])
			material_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
			requested_execution_mode!: "routed-mutation" | "reusable-mutation" | "standalone-nonmutating"
			state!:                    "planned" | "complete" | "blocked"
			successor!:                null | strings.MinRunes(1)
			task_class!:               "material-mutation" | "output-only" | "audit-only" | "read-only-validation"
			terminal_receipt!:         strings.MinRunes(1)
			unit_id!:                  strings.MinRunes(1)
			validation_commands!: [...close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				cwd!: strings.MinRunes(1)
				environment!: [string]: string
				expected_exit_code!: int
				risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
				runtime_identity!: close({
					executable!:     strings.MinRunes(1)
					hash_policy!:    strings.MinRunes(1)
					version_policy!: strings.MinRunes(1)
				})
				timeout_seconds!: int & >=1
			})]
		})] & [_, ...]
		work_pack!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
	})

	#attempt: close({
		collision_policy!: "fail-if-exists" | "append-only"
		id_algorithm!:     string
		required!:         bool
		retention_policy!: "retain-receipt-only" | "retain-all" | "ephemeral"
		teardown_on_failure!: [...close({
			argv!: [...strings.MinRunes(1)] & [_, ...]
			cwd!: strings.MinRunes(1)
			environment!: [string]: string
			expected_exit_code!: int
			risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
			runtime_identity!: close({
				executable!:     strings.MinRunes(1)
				hash_policy!:    strings.MinRunes(1)
				version_policy!: strings.MinRunes(1)
			})
			timeout_seconds!: int & >=1
		})]
		teardown_on_success!: [...close({
			argv!: [...strings.MinRunes(1)] & [_, ...]
			cwd!: strings.MinRunes(1)
			environment!: [string]: string
			expected_exit_code!: int
			risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
			runtime_identity!: close({
				executable!:     strings.MinRunes(1)
				hash_policy!:    strings.MinRunes(1)
				version_policy!: strings.MinRunes(1)
			})
			timeout_seconds!: int & >=1
		})]
	})

	#command: close({
		argv!: [...strings.MinRunes(1)] & [_, ...]
		cwd!: strings.MinRunes(1)
		environment!: [string]: string
		expected_exit_code!: int
		risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
		runtime_identity!: close({
			executable!:     strings.MinRunes(1)
			hash_policy!:    strings.MinRunes(1)
			version_policy!: strings.MinRunes(1)
		})
		timeout_seconds!: int & >=1
	})

	#dependencyReceipt: close({
		dependency_id!:    strings.MinRunes(1)
		expected_status!:  "pass"
		expected_step_id!: strings.MinRunes(1)
		expected_unit_id!: strings.MinRunes(1)
		receipt_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		work_pack_sha256!: =~"^[a-f0-9]{64}$"
	})

	#exactArtifactRef: close({
		path!:       strings.MinRunes(1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})

	#unit: close({
		allowed_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
		attempt!: close({
			collision_policy!: "fail-if-exists" | "append-only"
			id_algorithm!:     string
			required!:         bool
			retention_policy!: "retain-receipt-only" | "retain-all" | "ephemeral"
			teardown_on_failure!: [...close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				cwd!: strings.MinRunes(1)
				environment!: [string]: string
				expected_exit_code!: int
				risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
				runtime_identity!: close({
					executable!:     strings.MinRunes(1)
					hash_policy!:    strings.MinRunes(1)
					version_policy!: strings.MinRunes(1)
				})
				timeout_seconds!: int & >=1
			})]
			teardown_on_success!: [...close({
				argv!: [...strings.MinRunes(1)] & [_, ...]
				cwd!: strings.MinRunes(1)
				environment!: [string]: string
				expected_exit_code!: int
				risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
				runtime_identity!: close({
					executable!:     strings.MinRunes(1)
					hash_policy!:    strings.MinRunes(1)
					version_policy!: strings.MinRunes(1)
				})
				timeout_seconds!: int & >=1
			})]
		})
		closeout_receipt!: strings.MinRunes(1)
		contract_kind!:    "full-task" | "row-only"
		contract_ref!: close({
			path!:       strings.MinRunes(1)
			sha256!:     =~"^[a-f0-9]{64}$"
			size_bytes!: int & >=0
		})
		dependencies!: list.UniqueItems() & [...strings.MinRunes(1)]
		dependency_receipts!: [...close({
			dependency_id!:    strings.MinRunes(1)
			expected_status!:  "pass"
			expected_step_id!: strings.MinRunes(1)
			expected_unit_id!: strings.MinRunes(1)
			receipt_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			work_pack_sha256!: =~"^[a-f0-9]{64}$"
		})]
		dispatch_step!: strings.MinRunes(1)
		execution_outputs!: list.UniqueItems() & [...strings.MinRunes(1)]
		material_package?: matchN(1, [close({
			package_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
			receipt_ref!: close({
				path!:       strings.MinRunes(1)
				sha256!:     =~"^[a-f0-9]{64}$"
				size_bytes!: int & >=0
			})
		}), null])
		material_writes!: list.UniqueItems() & [...strings.MinRunes(1)]
		requested_execution_mode!: "routed-mutation" | "reusable-mutation" | "standalone-nonmutating"
		state!:                    "planned" | "complete" | "blocked"
		successor!:                null | strings.MinRunes(1)
		task_class!:               "material-mutation" | "output-only" | "audit-only" | "read-only-validation"
		terminal_receipt!:         strings.MinRunes(1)
		unit_id!:                  strings.MinRunes(1)
		validation_commands!: [...close({
			argv!: [...strings.MinRunes(1)] & [_, ...]
			cwd!: strings.MinRunes(1)
			environment!: [string]: string
			expected_exit_code!: int
			risk_class!:         "read-only" | "bounded-write" | "browser" | "network" | "destructive"
			runtime_identity!: close({
				executable!:     strings.MinRunes(1)
				hash_policy!:    strings.MinRunes(1)
				version_policy!: strings.MinRunes(1)
			})
			timeout_seconds!: int & >=1
		})]
	})
}

// TaskSessionUntilBlockerChainConfig
package prototype

import (
	"list"
	"strings"
)

#Root: {
	@jsonschema(schema="https://json-schema.org/draft/2020-12/schema")
	@jsonschema(id="https://arcanum.dev/schemas/task-session-until-blocker/chain-config/1-0-0")
	matchN(2, [matchIf({
		admission_window!: _
	}, {
		finite_frontier?: null | bool | number | string | list.MaxItems(1) | {}
		run_budget?: null | bool | number | string | [...] | {
			max_task_session_requests?: 1
		}
		audit_report_ref!: _
		wpra_v2!:          _
	}, _) & {}, matchIf({
		frontier_binding_mode!: _
	}, matchN(0, [null | bool | number | string | [...] | {
		admission_window!: _
	}]) & {}, _) & {}]) & close({
		schema_version!:   "1.0.0"
		chain_id!:         =~"^[A-Za-z0-9][A-Za-z0-9._-]+$"
		repository_root!:  "."
		state_directory!:  strings.MinRunes( 1)
		scope_id!:         strings.MinRunes( 1)
		manifest_ref!:     #exactArtifactRef
		audit_report_ref?: #exactArtifactRef
		wpra_v2?: close({
			audit_config_ref!:              #exactArtifactRef
			execution_contracts_ref!:       #exactArtifactRef
			selection_handoff_ref!:         #exactArtifactRef
			initial_selection_request_ref!: #exactArtifactRef
			initial_selection_receipt_ref!: #exactArtifactRef
		})
		frontier_binding_mode?: "accepted-policy-frontier"
		admission_window?: close({
			mode!:                           "fresh-current-unit"
			supervisor_id!:                  =~"^[A-Za-z0-9][A-Za-z0-9._-]+$"
			epoch_ordinal!:                  int & >=1
			selected_unit!:                  strings.MinRunes( 1)
			supervisor_frontier_digest!:     =~"^[a-f0-9]{64}$"
			observed_ready_frontier_digest!: =~"^[a-f0-9]{64}$"
		})
		audit_verdict!: "pass" | "flag"
		audit_flags!: list.UniqueItems() & [..."observability-residue"]
		approved_epoch!: close({
			epoch_id!:                           =~"^epoch-[a-f0-9]{24}$"
			audit_projection_digest!:            =~"^[a-f0-9]{64}$"
			canonical_semantic_digest!:          =~"^[a-f0-9]{64}$"
			source_snapshot_digest!:             =~"^[a-f0-9]{64}$"
			decision_gate_approval_receipt_ref!: #exactArtifactRef
			approval_owner_ref!:                 strings.MinRunes( 1)
			approval_status!:                    "approved"
		})
		finite_frontier!: list.UniqueItems() & [_, ...] & [...strings.MinRunes( 1)]
		run_budget!: close({
			max_task_session_requests!: int & >=1
		})
		risk_ceiling!: "read-only" | "bounded-write" | "browser" | "network"
		allowed_task_session_flags!: list.UniqueItems() & [..."observability-residue"]
		persistence!: close({
			mode!:             "append-only-hash-chain"
			collision_policy!: "exclusive-create"
		})
		compensation!: #compensation
	})

	#compensation: matchN(1, [close({
		mode!:      "none"
		rationale!: strings.MinRunes( 1)
	}), close({
		mode!:         "owner-routed"
		owner_ref!:    strings.MinRunes( 1)
		contract_ref!: #exactArtifactRef
	})])

	#exactArtifactRef: close({
		path!:       strings.MinRunes( 1)
		sha256!:     =~"^[a-f0-9]{64}$"
		size_bytes!: int & >=0
	})
}

#!/usr/bin/env python3
"""Validate approved-epoch, cursor, NO_OP, and compensation chain behavior."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = SPELL_ROOT / "scripts" / "run_chain.py"
SPEC = importlib.util.spec_from_file_location("run_chain", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {RUNNER_PATH}")
CHAIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHAIN)


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class ChainFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        self.epoch_id = f"epoch-{'1' * 24}"
        self.projection_digest = "2" * 64
        self.semantic_digest = "3" * 64
        self.snapshot_digest = "4" * 64
        for name, payload in {
            "approval.json": {"status": "approved"},
            "terminal-U1.json": {"status": "PASS"},
            "terminal-U2.json": {"status": "PASS"},
            "owner-U1.json": {"status": "PASS"},
            "router-U1.json": {"status": "verified"},
            "router-U2.json": {"status": "verified"},
            "closeout-U1.json": {"unit": "U1"},
            "closeout-U2.json": {"unit": "U2"},
        }.items():
            (self.root / name).write_text(json.dumps(payload), encoding="utf-8")
        manifest = {
            "authority_effect": "none",
            "mutation_ready": False,
            "selected_unit": None,
            "epoch_binding": {
                "epoch_id": self.epoch_id,
                "audit_projection_digest": self.projection_digest,
                "canonical_semantic_digest": self.semantic_digest,
                "source_snapshot_digest": self.snapshot_digest,
            },
            "canonical_plan_graph": {"finite_frontier": ["U1", "U2"]},
            "execution_bindings": [
                {"unit_id": "U1", "command": {"risk_class": "bounded-write"}},
                {"unit_id": "U2", "command": {"risk_class": "bounded-write"}},
            ],
            "closeout_bindings": [
                {
                    "unit_id": "U1",
                    "owner_receipt_contract_ref": {
                        "artifact_ref": self.exact("closeout-U1.json")
                    },
                },
                {
                    "unit_id": "U2",
                    "owner_receipt_contract_ref": {
                        "artifact_ref": self.exact("closeout-U2.json")
                    },
                },
            ],
        }
        (self.root / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True), encoding="utf-8"
        )

    def close(self) -> None:
        self.temp.cleanup()

    def exact(self, path: str) -> dict[str, object]:
        content = (self.root / path).read_bytes()
        return {
            "path": path,
            "sha256": sha256(content),
            "size_bytes": len(content),
        }

    def camel_exact(self, path: str) -> dict[str, object]:
        reference = self.exact(path)
        return {
            "path": reference["path"],
            "sha256": reference["sha256"],
            "sizeBytes": reference["size_bytes"],
        }

    def config(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "chain_id": "synthetic-chain",
            "repository_root": ".",
            "state_directory": "state/synthetic-chain",
            "scope_id": "synthetic-work-pack",
            "manifest_ref": self.exact("manifest.json"),
            "audit_verdict": "pass",
            "audit_flags": [],
            "approved_epoch": {
                "epoch_id": self.epoch_id,
                "audit_projection_digest": self.projection_digest,
                "canonical_semantic_digest": self.semantic_digest,
                "source_snapshot_digest": self.snapshot_digest,
                "decision_gate_approval_receipt_ref": self.exact("approval.json"),
                "approval_owner_ref": "decision-gate",
                "approval_status": "approved",
            },
            "finite_frontier": ["U1", "U2"],
            "run_budget": {"max_task_session_requests": 2},
            "risk_ceiling": "bounded-write",
            "allowed_task_session_flags": ["observability-residue"],
            "persistence": {
                "mode": "append-only-hash-chain",
                "collision_policy": "exclusive-create",
            },
            "compensation": {
                "mode": "none",
                "rationale": "Synthetic fixture has no reversible side effect.",
            },
        }

    def v2_config(
        self,
        *,
        fragment_targets: bool = False,
        include_closeout_routes: bool = True,
    ) -> dict[str, object]:
        frontier = ["U1", "U2"]
        routes = []
        for unit_id in frontier:
            target = f"product/{unit_id}#{unit_id}" if fragment_targets else unit_id
            routes.append(
                {
                    "route_id": f"task-session-{unit_id}",
                    "frontier_swu": unit_id,
                    "capability": "task-session",
                    "mode": "execute",
                    "target": target,
                    "write_scope": [f"product/{unit_id}"],
                    "effect_class": "repository-local-reversible",
                    "required_inputs": [f"contract/{unit_id}"],
                    "expected_receipt": f"receipt/{unit_id}",
                }
            )
            if include_closeout_routes:
                routes.append(
                    {
                        "route_id": f"closeout-{unit_id}",
                        "frontier_swu": unit_id,
                        "capability": "invoke",
                        "mode": "refresh-apply-approved",
                        "target": f"{unit_id}-closeout",
                        "write_scope": [f"plan/{unit_id}"],
                        "effect_class": "repository-local-reversible",
                        "required_inputs": [f"receipt/{unit_id}"],
                        "expected_receipt": f"closeout/{unit_id}",
                    }
                )
        manifest = {
            "manifest_id": f"psm-{self.projection_digest[:24]}",
            "plan_epoch_id": self.epoch_id,
            "canonical_semantic_digest": self.semantic_digest,
            "source_snapshot_digest": self.snapshot_digest,
            "ready_frontier": frontier,
            "completion_continuity": {
                "plan_epoch_id": self.epoch_id,
                "work_pack_semantic_digest": self.semantic_digest,
                "next_unit": "U1",
                "authority_effect": "none",
            },
            "allowed_routes": routes,
            "allowed_routes_digest": CHAIN.digest(routes),
            "authority_effect": "none",
            "mutation_ready": False,
            "selected_unit": None,
        }
        (self.root / "manifest-v2.json").write_text(
            json.dumps(manifest, sort_keys=True), encoding="utf-8"
        )
        report = {
            "verdict": "pass",
            "flags": [],
            "audit_projection_digest": self.projection_digest,
            "canonical_semantic_digest": self.semantic_digest,
            "source_snapshot": {"digest": self.snapshot_digest},
            "manifest": manifest,
        }
        (self.root / "report-v2.json").write_text(
            json.dumps(report, sort_keys=True), encoding="utf-8"
        )
        config = self.config()
        config["manifest_ref"] = self.exact("manifest-v2.json")
        config["audit_report_ref"] = self.exact("report-v2.json")
        return config

    def write_json(self, path: str, payload: dict[str, object]) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")

    def current_v2_config(self) -> dict[str, object]:
        frontier = ["U1", "U2"]
        units = []
        execution_bindings = []
        routes = []
        for index, unit_id in enumerate(frontier):
            swu_id = f"SWU-{index + 1}"
            task_id = f"TASK-{index + 1}"
            successor = f"SWU-{index + 2}" if index + 1 < len(frontier) else None
            dependencies = [] if index == 0 else ["SWU-1"]
            dependency_units = [] if index == 0 else ["U1"]
            command = {
                "argv": ["task-session", "--task", task_id, "--swu", swu_id],
                "cwd": ".",
                "risk_class": "bounded-write",
            }
            validation = [{
                "command_id": f"V-{unit_id}",
                "argv": ["python3", "-m", "json.tool", f"receipt/{unit_id}.json"],
                "cwd": ".",
                "timeout_seconds": 30,
                "max_output_bytes": 4096,
            }]
            material_writes: list[str] = []
            execution_outputs = [f"receipt/{unit_id}.json"]
            allowed_writes = execution_outputs.copy()
            closeout_inventory = [f"closeout/{unit_id}.json", f"next/{unit_id}.json"]
            contract = {
                "unit_id": unit_id,
                "ordinal_id": unit_id,
                "swu_id": swu_id,
                "task_id": task_id,
                "objective": f"Synthetic objective {unit_id}",
                "dependencies": dependencies,
                "canonical_successor": successor,
                "lifecycle_owner": "task-session",
                "authority_class": "private",
                "publication_class": "private",
                "command": {"contract_type": "native-capability-handle", **command},
                "material_writes": material_writes,
                "execution_outputs": execution_outputs,
                "allowed_writes": allowed_writes,
                "attempt_contract": {
                    "id_policy": "attempt-id-equals-task-session-run-id",
                    "collision_policy": "reject-any-existing-target-or-baseline-drift",
                    "success_teardown": "retain-terminal-receipt-and-await-closeout",
                    "failure_teardown": "retain-first-terminal-or-block-receipt",
                },
                "gate_contract": {
                    "selection_requires": [] if index == 0 else [
                        "U1-closeout-pass", "U1-owner-acceptance-receipt"
                    ],
                    "execution_requires": [f"exact-input-{unit_id}"],
                    "on_unsatisfied": "block",
                    "completion_rule": f"complete-{unit_id}",
                },
                "terminal_write_policy": {
                    "create_mode": "exclusive-create",
                    "first_terminal": "preserve-never-overwrite",
                    "validation_failure": "block-before-success-receipt",
                    "successor_execution": False,
                },
                "validation_contracts": [
                    {"source_text": "synthetic", "adapter": "direct-command", **validation[0]}
                ],
                "terminal_modes": ["PASS", "BLOCK"],
                "receipt_contract": {"path": f"receipt/{unit_id}.json"},
                "closeout_contract": {
                    "route": "invoke:refresh:apply-approved",
                    "target_inventory": closeout_inventory,
                    "expected_owner_receipt": f"closeout/{unit_id}.json",
                    "allowed_delta_policy": "evidence-only",
                    "successor_policy": successor or "none",
                },
                "check_parameters": {},
            }
            units.append(contract)
            execution_bindings.append({
                "unit_id": unit_id,
                "task_id": task_id,
                "swu_id": swu_id,
                "lifecycle_owner": "task-session",
                "authority_class": "private",
                "publication_class": "private",
                "attempt_contract": contract["attempt_contract"],
                "dependencies": dependency_units,
                "canonical_successors": [] if successor is None else [f"U{index + 2}"],
                "command": command,
                "validation_contracts": validation,
                "material_writes": contract["material_writes"],
                "execution_outputs": contract["execution_outputs"],
                "allowed_writes": allowed_writes,
                "material_package": {
                    "package_ref": None,
                    "producer_owner_ref": "material-owner",
                    "producer_receipt_ref": None,
                    "schema_ref": None,
                    "declared_sha256": None,
                    "target_inventory_ref": None,
                },
                "byte_baselines": [],
            })
            routes.extend([
                {
                    "route_id": f"task-{unit_id}",
                    "frontier_swu": unit_id,
                    "capability": "task-session",
                    "mode": "execute-one-swu",
                    "target": f"work-pack/tasks/{unit_id}.md",
                    "write_scope": allowed_writes,
                    "effect_class": "repository-local-reversible",
                    "required_inputs": [
                        "manifest-current.json",
                        f"admission/{unit_id}/SELECTION-RECEIPT.json",
                        f"admission/{unit_id}/MUTATION-ADMISSION-RECEIPT.json",
                    ] + (["receipt/U1.json"] if index else []),
                    "expected_receipt": f"receipt/{unit_id}.json",
                },
                {
                    "route_id": f"closeout-{unit_id}",
                    "frontier_swu": unit_id,
                    "capability": "invoke",
                    "mode": "refresh",
                    "target": "synthetic-work-pack",
                    "write_scope": closeout_inventory,
                    "effect_class": "repository-local-reversible",
                    "required_inputs": [f"receipt/{unit_id}.json"],
                    "expected_receipt": f"closeout/{unit_id}.json",
                },
            ])
        contracts = {
            "schema_version": "synthetic.execution-contracts/v1",
            "status": "candidate-unapproved",
            "authority_effect": "none",
            "mutation_ready": False,
            "admission_timing": "selected-unit-at-task-session",
            "execution_policy": {"work_pack_id": "synthetic-work-pack", "allowed_routes": routes},
            "units": units,
        }
        self.write_json("contracts.json", contracts)
        closeout_bindings = [{
            "unit_id": unit_id,
            "owner_receipt_contract_ref": {
                "artifact_ref": self.exact("contracts.json"),
                "selector": f"/units/{index}/closeout_contract",
            },
            "compensation": {"mode": "none", "rationale": "synthetic"},
        } for index, unit_id in enumerate(frontier)]
        audit_config = {
            "schema_version": "2.0.0",
            "admission_timing": "selected-unit-at-task-session",
            "execution_policy": {"work_pack_id": "synthetic-work-pack", "allowed_routes": routes},
            "execution_bindings": execution_bindings,
            "closeout_bindings": closeout_bindings,
        }
        self.write_json("audit-config.json", audit_config)
        unit_digests = {"U1": "a" * 64, "U2": "b" * 64}
        manifest = {
            "schema_version": "1.0.0",
            "manifest_id": f"psm-{self.projection_digest[:24]}",
            "audit_id": "synthetic-audit",
            "work_pack_id": "synthetic-work-pack",
            "normalizer_version": "1.0.0",
            "admission_timing": "selected-unit-at-task-session",
            "plan_epoch_id": self.epoch_id,
            "canonical_semantic_digest": self.semantic_digest,
            "semantic_component_digests": {"work_pack": self.semantic_digest},
            "source_snapshot_digest": self.snapshot_digest,
            "ready_frontier": frontier,
            "completion_continuity": {
                "source_audit_id": "synthetic-audit",
                "source_projection_digest": self.projection_digest,
                "plan_epoch_id": self.epoch_id,
                "work_pack_semantic_digest": self.semantic_digest,
                "completed_prefix": [],
                "next_unit": "U1",
                "authority_effect": "none",
                "continuity_digest": "c" * 64,
            },
            "allowed_routes": routes,
            "allowed_routes_digest": CHAIN.digest(routes),
            "unit_contract_digests": unit_digests,
            "selection_required": True,
            "runtime_admission_status": "pending-selection",
            "approval_status": "unapproved",
            "execution_entry": {
                "entry_state": "selection-ready",
                "selected_unit": None,
                "route_id": None,
                "next_owner": {
                    "capability": "implementation-readiness",
                    "mode": "execute",
                    "target": "synthetic-work-pack",
                },
                "blocker_code": None,
            },
            "authority_effect": "none",
            "mutation_ready": False,
            "selected_unit": None,
        }
        self.write_json("manifest-current.json", manifest)
        self.write_json("report-current.json", {
            "verdict": "pass", "flags": [],
            "audit_projection_digest": self.projection_digest,
            "canonical_semantic_digest": self.semantic_digest,
            "source_snapshot": {"digest": self.snapshot_digest},
            "manifest": manifest,
        })
        self.write_json("handoff.json", {
            "plan_epoch_id": self.epoch_id,
            "ready_frontier": frontier,
            "allowed_routes_digest": manifest["allowed_routes_digest"],
            "authority_effect": "none", "mutation_ready": False,
            "selection_required": True,
        })
        self.write_json(
            "initial-lifecycle.json", {"status": "selection-confirmed"}
        )
        selection_request = {
            "schemaVersion": "1.0.0",
            "manifestRef": self.exact("manifest-current.json"),
            "auditConfigPath": "audit-config.json",
            "taskId": "TASK-1", "swuId": "SWU-1",
            "explicitConfirmation": {"confirmed": True, "confirmedBy": "owner", "confirmationId": "selection-1"},
            "dependencyReceipts": [],
            "lifecycleEligibility": {
                "eligible": True,
                "state": "selection-ready",
                "evidenceRefs": [self.exact("initial-lifecycle.json")],
            },
        }
        self.write_json("selection-request.json", selection_request)
        selection_receipt = {
            "schemaVersion": "1.0.0", "selectionVerdict": "select",
            "terminalCode": "SELECTION_READY", "planEpochId": self.epoch_id,
            "canonicalSemanticDigest": self.semantic_digest,
            "manifestDigest": self.exact("manifest-current.json")["sha256"],
            "unitContractDigest": unit_digests["U1"], "taskId": "TASK-1", "swuId": "SWU-1",
            "dependencyReceiptDigests": [],
            "explicitConfirmationDigest": CHAIN.digest(selection_request["explicitConfirmation"]),
            "selectionIntentDigest": CHAIN.digest(selection_request["explicitConfirmation"]),
            "selectionIntentSource": "explicit-confirmation",
            "lifecycleEligibilityDigest": CHAIN.digest(selection_request["lifecycleEligibility"]),
            "requestDigest": CHAIN.digest(selection_request),
            "authorityEffect": "none", "mutationReady": False, "reasons": [],
        }
        self.write_json("selection-receipt.json", selection_receipt)
        approval = {
            "schema_version": "task-session-until-blocker.epoch-approval/v1",
            "approval_status": "approved", "approval_owner_ref": "decision-gate",
            "plan_epoch_id": self.epoch_id,
            "audit_projection_digest": self.projection_digest,
            "canonical_semantic_digest": self.semantic_digest,
            "source_snapshot_digest": self.snapshot_digest,
            "manifest_ref": self.exact("manifest-current.json"),
            "audit_config_ref": self.exact("audit-config.json"),
            "execution_contracts_ref": self.exact("contracts.json"),
            "authority_effect": "chain-selection-only",
        }
        self.write_json("approval-current.json", approval)
        config = self.config()
        config["manifest_ref"] = self.exact("manifest-current.json")
        config["audit_report_ref"] = self.exact("report-current.json")
        config["approved_epoch"]["decision_gate_approval_receipt_ref"] = self.exact("approval-current.json")
        config["finite_frontier"] = frontier
        config["wpra_v2"] = {
            "audit_config_ref": self.exact("audit-config.json"),
            "execution_contracts_ref": self.exact("contracts.json"),
            "selection_handoff_ref": self.exact("handoff.json"),
            "initial_selection_request_ref": self.exact("selection-request.json"),
            "initial_selection_receipt_ref": self.exact("selection-receipt.json"),
        }
        return config

    def refresh_nested_v2_refs(
        self, config: dict[str, object]
    ) -> dict[str, object]:
        manifest = json.loads(
            (self.root / "manifest-nested.json").read_text(encoding="utf-8")
        )
        manifest["allowed_routes_digest"] = CHAIN.digest(
            manifest["allowed_routes"]
        )
        self.write_json("manifest-nested.json", manifest)

        source = json.loads(
            (self.root / "source-nested.json").read_text(encoding="utf-8")
        )
        source["execution_contracts"]["execution_policy"][
            "allowed_routes"
        ] = copy.deepcopy(manifest["allowed_routes"])
        self.write_json("source-nested.json", source)
        source_ref = self.exact("source-nested.json")

        audit = json.loads(
            (self.root / "audit-config-nested.json").read_text(encoding="utf-8")
        )
        audit["execution_policy"]["allowed_routes"] = copy.deepcopy(
            manifest["allowed_routes"]
        )
        for index, binding in enumerate(audit["closeout_bindings"]):
            binding["owner_receipt_contract_ref"] = {
                "artifact_ref": source_ref,
                "selector": f"/execution_contracts/units/{index}/closeout_contract",
            }
            binding["allowed_delta_policy_ref"] = {
                "artifact_ref": source_ref,
                "selector": (
                    f"/execution_contracts/units/{index}/"
                    "closeout_contract/allowed_delta_classes"
                ),
            }
        self.write_json("audit-config-nested.json", audit)

        report = json.loads(
            (self.root / "report-nested.json").read_text(encoding="utf-8")
        )
        report["manifest"] = manifest
        self.write_json("report-nested.json", report)
        handoff = json.loads(
            (self.root / "handoff-nested.json").read_text(encoding="utf-8")
        )
        handoff["allowed_routes_digest"] = manifest["allowed_routes_digest"]
        self.write_json("handoff-nested.json", handoff)

        request = json.loads(
            (self.root / "selection-request-nested.json").read_text(
                encoding="utf-8"
            )
        )
        request["manifestRef"] = self.exact("manifest-nested.json")
        request["auditConfigPath"] = "audit-config-nested.json"
        self.write_json("selection-request-nested.json", request)
        selection = json.loads(
            (self.root / "selection-receipt-nested.json").read_text(
                encoding="utf-8"
            )
        )
        selection["manifestDigest"] = self.exact("manifest-nested.json")[
            "sha256"
        ]
        selection["requestDigest"] = CHAIN.digest(request)
        self.write_json("selection-receipt-nested.json", selection)

        approval = json.loads(
            (self.root / "approval-nested.json").read_text(encoding="utf-8")
        )
        approval["manifest_ref"] = self.exact("manifest-nested.json")
        approval["audit_config_ref"] = self.exact("audit-config-nested.json")
        approval["execution_contracts_ref"] = source_ref
        self.write_json("approval-nested.json", approval)

        config["manifest_ref"] = self.exact("manifest-nested.json")
        config["audit_report_ref"] = self.exact("report-nested.json")
        config["approved_epoch"][
            "decision_gate_approval_receipt_ref"
        ] = self.exact("approval-nested.json")
        config["wpra_v2"] = {
            "audit_config_ref": self.exact("audit-config-nested.json"),
            "execution_contracts_ref": source_ref,
            "selection_handoff_ref": self.exact("handoff-nested.json"),
            "initial_selection_request_ref": self.exact(
                "selection-request-nested.json"
            ),
            "initial_selection_receipt_ref": self.exact(
                "selection-receipt-nested.json"
            ),
        }
        return config

    def nested_selected_unit_v2_config(self) -> dict[str, object]:
        config = self.current_v2_config()
        contracts = json.loads(
            (self.root / "contracts.json").read_text(encoding="utf-8")
        )
        routes = [
            {
                **route,
                "mode": "execute",
                "target": (
                    f"work-pack/tasks/{route['frontier_swu']}.md#"
                    f"{route['frontier_swu'].lower()}"
                ),
            }
            for route in contracts["execution_policy"]["allowed_routes"]
            if route["capability"] == "task-session"
        ]
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
        }
        schema_refs = {}
        for name in ("precloseout", "terminal", "owner", "continuation", "router"):
            self.write_json(f"schemas/{name}.json", schema)
            schema_refs[name] = self.exact(f"schemas/{name}.json")
        allowed_deltas = [
            "evidence_added",
            "blocker_opened",
            "blocker_resolved",
            "status_changed",
            "route_changed",
        ]
        for unit in contracts["units"]:
            unit_id = unit["unit_id"]
            continuation_path = f"continuation/{unit_id}.json"
            unit["receipt_contract"] = {
                "receipt_profile": "precloseout-execution-v1",
                "path": f"receipt/{unit_id}.json",
                "precloseout_execution_receipt_path": (
                    f"precloseout/{unit_id}.json"
                ),
                "precloseout_execution_schema_ref": schema_refs["precloseout"],
                "final_terminal_schema_ref": schema_refs["terminal"],
            }
            unit["closeout_contract"] = {
                "route": "invoke:refresh:apply-approved",
                "target_inventory": [
                    f"plan/{unit_id}.json",
                    continuation_path,
                ],
                "target_inventory_path": f"inventory/{unit_id}.json",
                "expected_owner_receipt": f"closeout/{unit_id}.json",
                "expected_owner_receipt_schema_ref": schema_refs["owner"],
                "continuation_state_path": continuation_path,
                "continuation_state_schema_ref": schema_refs["continuation"],
                "continuation_router_verification_receipt": (
                    f"router/{unit_id}.json"
                ),
                "continuation_router_schema_ref": schema_refs["router"],
                "allowed_delta_classes": allowed_deltas,
                "continuation_policy": "emit-cursor-never-execute-successor",
                "successor_policy": unit["canonical_successor"] or "reviewed-promotion",
                "validation_commands": [
                    {
                        "command_id": f"closeout-{unit_id}",
                        "argv": ["validate-closeout", unit_id],
                        "cwd": ".",
                        "timeout_seconds": 30,
                        "max_output_bytes": 4096,
                    }
                ],
            }
        contracts["execution_policy"]["allowed_routes"] = routes
        source = {
            "schema_version": "synthetic.source-contract/v2",
            "execution_contracts": contracts,
        }
        self.write_json("source-nested.json", source)

        audit = json.loads(
            (self.root / "audit-config.json").read_text(encoding="utf-8")
        )
        audit["execution_policy"]["allowed_routes"] = routes
        audit["execution_bindings"][-1]["canonical_successors"] = [
            "__window_complete__"
        ]
        self.write_json("audit-config-nested.json", audit)
        manifest = json.loads(
            (self.root / "manifest-current.json").read_text(encoding="utf-8")
        )
        manifest["allowed_routes"] = routes
        manifest["approval_status"] = "unapproved"
        self.write_json("manifest-nested.json", manifest)
        report = json.loads(
            (self.root / "report-current.json").read_text(encoding="utf-8")
        )
        self.write_json("report-nested.json", report)
        handoff = json.loads(
            (self.root / "handoff.json").read_text(encoding="utf-8")
        )
        self.write_json("handoff-nested.json", handoff)
        request = json.loads(
            (self.root / "selection-request.json").read_text(encoding="utf-8")
        )
        self.write_json("selection-request-nested.json", request)
        selection = json.loads(
            (self.root / "selection-receipt.json").read_text(encoding="utf-8")
        )
        self.write_json("selection-receipt-nested.json", selection)
        approval = json.loads(
            (self.root / "approval-current.json").read_text(encoding="utf-8")
        )
        self.write_json("approval-nested.json", approval)
        return self.refresh_nested_v2_refs(config)

    def transition(
        self,
        selector: str = "U1",
        *,
        ordinal: int = 1,
        previous: str | None = None,
        cursor: str = "cursor-1",
        result: str = "PASS",
        closeout: str = "PASS",
    ) -> dict[str, object]:
        successor = "U2" if selector == "U1" else None
        owner = self.exact("owner-U1.json") if closeout == "PASS" else None
        router_name = "router-U1.json" if selector == "U1" else "router-U2.json"
        router = self.exact(router_name)
        no_op = None
        if closeout == "NO_OP":
            baseline = [{"path": "target.txt", "sha256": "5" * 64}]
            no_op = {
                "schema_version": "1.0.0",
                "proof_id": f"noop-{selector}",
                "unit_id": selector,
                "before_inventory": baseline,
                "after_inventory": copy.deepcopy(baseline),
                "observed_delta": [],
                "closeout_contract_ref": self.exact(
                    f"closeout-{selector}.json"
                ),
                "validator": {
                    "id": "synthetic-noop-validator",
                    "version": "1.0.0",
                    "executable_sha256": "6" * 64,
                },
                "continuation_router_verification": {
                    "receipt_ref": router,
                    "status": "verified",
                    "canonical_successor": successor,
                },
                "authority_effect": "none",
            }
        return {
            "schema_version": "1.0.0",
            "chain_id": "synthetic-chain",
            "transition_id": f"transition-{ordinal}",
            "transition_digest": None,
            "previous_transition_digest": previous,
            "epoch_id": self.epoch_id,
            "cursor": cursor,
            "selector": selector,
            "request_ordinal": ordinal,
            "risk_class": "bounded-write",
            "task_session_result": result,
            "task_session_flags": [],
            "terminal_receipt_ref": self.exact(f"terminal-{selector}.json"),
            "closeout": {
                "result": closeout,
                "owner_receipt_ref": owner,
                "no_op_proof": no_op,
                "continuation_router_verification_receipt_ref": router,
            },
            "successor": {
                "unit_id": successor,
                "candidate_count": 1 if successor else 0,
                "declared": True,
                "dependency_ready": True,
                "scope_digest": self.projection_digest,
            },
            "observed_frontier_digest": CHAIN.digest(["U1", "U2"]),
        }


class ApprovedEpochChainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = ChainFixture()
        self.config = self.fixture.config()
        errors = CHAIN.schema_errors(
            self.config, CHAIN.CONFIG_SCHEMA, "chain config"
        )
        self.assertEqual(errors, [])
        self.manifest, receipt = CHAIN.preflight(self.config, self.fixture.root)
        self.assertIsNotNone(self.manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")

    def tearDown(self) -> None:
        self.fixture.close()

    def test_two_transition_chain_persists_and_completes(self) -> None:
        transitions_dir, state = CHAIN.open_chain_state(
            self.config, self.manifest, self.fixture.root
        )
        admission = CHAIN.admit_next_request(self.config, self.manifest, state)
        self.assertEqual(admission["next_task_session_selector"], "U1")
        first = self.fixture.transition()
        receipt, state = CHAIN.evaluate_transition(
            self.config, self.manifest, first, state
        )
        self.assertEqual(receipt["terminal_code"], "NEXT_SELECTOR_READY")
        self.assertEqual(receipt["next_task_session_selector"], "U2")
        CHAIN.persist_transition(transitions_dir, first, receipt, state)
        _, reloaded = CHAIN.open_chain_state(
            self.config, self.manifest, self.fixture.root
        )
        self.assertEqual(reloaded, state)
        second = self.fixture.transition(
            "U2",
            ordinal=2,
            previous=state["last_transition_digest"],
            cursor="cursor-2",
            closeout="NO_OP",
        )
        receipt, state = CHAIN.evaluate_transition(
            self.config, self.manifest, second, state
        )
        self.assertEqual(receipt["terminal_code"], "CHAIN_COMPLETE")
        self.assertIsNone(receipt["next_task_session_selector"])
        CHAIN.persist_transition(transitions_dir, second, receipt, state)
        with self.assertRaises(FileExistsError):
            CHAIN.persist_transition(transitions_dir, second, receipt, state)

    def test_replay_rejects_state_transition_and_config_ref_tamper(self) -> None:
        def persisted_fixture() -> tuple[ChainFixture, dict, dict, Path]:
            fixture = ChainFixture()
            config = fixture.config()
            manifest, preflight = CHAIN.preflight(config, fixture.root)
            self.assertEqual(preflight["terminal_code"], "CHAIN_PREFLIGHT_READY")
            transitions, state = CHAIN.open_chain_state(
                config, manifest, fixture.root
            )
            transition = fixture.transition()
            receipt, state = CHAIN.evaluate_transition(
                config, manifest, transition, state
            )
            ledger = CHAIN.persist_transition(
                transitions, transition, receipt, state
            )
            return fixture, config, manifest, ledger

        fixture, config, manifest, ledger = persisted_fixture()
        try:
            record = CHAIN.load_json(ledger)
            record["state_after"]["next_selector"] = "U1"
            fixture.write_json(
                str(ledger.relative_to(fixture.root)), record
            )
            with self.assertRaisesRegex(ValueError, "state differs from replay"):
                CHAIN.open_chain_state(config, manifest, fixture.root)
        finally:
            fixture.close()

        fixture, config, manifest, ledger = persisted_fixture()
        try:
            record = CHAIN.load_json(ledger)
            record["transition"]["cursor"] = "tampered-cursor"
            fixture.write_json(
                str(ledger.relative_to(fixture.root)), record
            )
            with self.assertRaisesRegex(ValueError, "differs from replay"):
                CHAIN.open_chain_state(config, manifest, fixture.root)
        finally:
            fixture.close()

        fixture, config, manifest, _ledger = persisted_fixture()
        try:
            drifted = copy.deepcopy(config)
            drifted["approved_epoch"]["decision_gate_approval_receipt_ref"][
                "sha256"
            ] = "f" * 64
            with self.assertRaisesRegex(
                ValueError, "differs from approved configuration"
            ):
                CHAIN.open_chain_state(drifted, manifest, fixture.root)
        finally:
            fixture.close()

    def test_invalid_transitions_expose_no_next_selector(self) -> None:
        base_state = CHAIN.initial_state(self.config)
        cases = [
            (
                "EPOCH_BINDING_MISMATCH",
                lambda t, _s: t.update(epoch_id=f"epoch-{'9' * 24}"),
            ),
            (
                "TRANSITION_LINK_MISMATCH",
                lambda t, _s: t.update(previous_transition_digest="7" * 64),
            ),
            (
                "REQUEST_ORDINAL_MISMATCH",
                lambda t, _s: t.update(request_ordinal=2),
            ),
            (
                "SELECTOR_OUT_OF_ORDER",
                lambda t, _s: t.update(selector="U2"),
            ),
            (
                "CURSOR_REPEATED",
                lambda _t, s: s["cursors"].append("cursor-1"),
            ),
            (
                "FRONTIER_DRIFT",
                lambda t, _s: t.update(observed_frontier_digest="8" * 64),
            ),
            (
                "RISK_CEILING_EXCEEDED",
                lambda t, _s: t.update(risk_class="network"),
            ),
            (
                "SUCCESSOR_NON_UNIQUE",
                lambda t, _s: t["successor"].update(candidate_count=2),
            ),
        ]
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                transition = self.fixture.transition()
                state = copy.deepcopy(base_state)
                mutate(transition, state)
                receipt, _ = CHAIN.evaluate_transition(
                    self.config, self.manifest, transition, state
                )
                self.assertEqual(receipt["terminal_code"], expected)
                self.assertIsNone(receipt["next_task_session_selector"])

    def test_no_op_requires_semantic_inventory_proof(self) -> None:
        state = CHAIN.initial_state(self.config)
        first = self.fixture.transition()
        _, state = CHAIN.evaluate_transition(
            self.config, self.manifest, first, state
        )
        transition = self.fixture.transition(
            "U2",
            ordinal=2,
            previous=state["last_transition_digest"],
            cursor="cursor-2",
            closeout="NO_OP",
        )
        transition["closeout"]["no_op_proof"]["after_inventory"][0][
            "sha256"
        ] = "9" * 64
        receipt, _ = CHAIN.evaluate_transition(
            self.config, self.manifest, transition, state
        )
        self.assertEqual(receipt["terminal_code"], "NO_OP_PROOF_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_budget_and_owner_routed_compensation_stop(self) -> None:
        exhausted = CHAIN.initial_state(self.config)
        exhausted["request_count"] = 2
        receipt = CHAIN.admit_next_request(
            self.config, self.manifest, exhausted
        )
        self.assertEqual(receipt["terminal_code"], "BUDGET_EXHAUSTED")
        self.assertIsNone(receipt["next_task_session_selector"])

        config = copy.deepcopy(self.config)
        config["compensation"] = {
            "mode": "owner-routed",
            "owner_ref": "recovery-owner",
            "contract_ref": self.fixture.exact("closeout-U1.json"),
        }
        transition = self.fixture.transition(result="BLOCK", closeout="BLOCK")
        receipt, _ = CHAIN.evaluate_transition(
            config, self.manifest, transition, CHAIN.initial_state(config)
        )
        self.assertEqual(
            receipt["terminal_code"], "COMPENSATION_OWNER_ROUTE_REQUIRED"
        )
        self.assertEqual(receipt["next_route"], "recovery-owner")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_v2_manifest_binds_the_exact_report_and_routes(self) -> None:
        config = self.fixture.v2_config()
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        self.assertEqual(receipt["next_task_session_selector"], "U1")
        self.assertEqual(manifest["execution_bindings"][0]["command"]["risk_class"], "bounded-write")

    def test_v2_manifest_accepts_fragment_targets_without_inline_closeouts(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        self.assertEqual(receipt["next_task_session_selector"], "U1")
        self.assertEqual(manifest["closeout_bindings"], [])

    def test_v2_fragment_target_must_name_its_frontier_unit(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest_path = self.fixture.root / "manifest-v2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"][0]["target"] = "product/U1#U2"
        manifest["allowed_routes_digest"] = CHAIN.digest(manifest["allowed_routes"])
        manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
        report_path = self.fixture.root / "report-v2.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["manifest"] = manifest
        report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
        config["manifest_ref"] = self.fixture.exact("manifest-v2.json")
        config["audit_report_ref"] = self.fixture.exact("report-v2.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_v2_fragment_target_allows_exactly_one_fragment(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest_path = self.fixture.root / "manifest-v2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"][0]["target"] = "product/U1#U1#extra"
        manifest["allowed_routes_digest"] = CHAIN.digest(manifest["allowed_routes"])
        manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
        report_path = self.fixture.root / "report-v2.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["manifest"] = manifest
        report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
        config["manifest_ref"] = self.fixture.exact("manifest-v2.json")
        config["audit_report_ref"] = self.fixture.exact("report-v2.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_v2_task_routes_must_cover_the_frontier_exactly(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest_path = self.fixture.root / "manifest-v2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"] = [
            route
            for route in manifest["allowed_routes"]
            if route["route_id"] != "task-session-U2"
        ]
        manifest["allowed_routes_digest"] = CHAIN.digest(manifest["allowed_routes"])
        manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
        report_path = self.fixture.root / "report-v2.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["manifest"] = manifest
        report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
        config["manifest_ref"] = self.fixture.exact("manifest-v2.json")
        config["audit_report_ref"] = self.fixture.exact("report-v2.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_v2_partial_inline_closeout_routes_block(self) -> None:
        config = self.fixture.v2_config(fragment_targets=True)
        manifest_path = self.fixture.root / "manifest-v2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"] = [
            route
            for route in manifest["allowed_routes"]
            if route["route_id"] != "closeout-U2"
        ]
        manifest["allowed_routes_digest"] = CHAIN.digest(manifest["allowed_routes"])
        manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
        report_path = self.fixture.root / "report-v2.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["manifest"] = manifest
        report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
        config["manifest_ref"] = self.fixture.exact("manifest-v2.json")
        config["audit_report_ref"] = self.fixture.exact("report-v2.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_v2_pass_closeout_can_advance_without_static_contract(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        receipt, _ = CHAIN.evaluate_transition(
            config,
            manifest,
            self.fixture.transition(closeout="PASS"),
            CHAIN.initial_state(config),
        )
        self.assertEqual(receipt["terminal_code"], "NEXT_SELECTOR_READY")
        self.assertEqual(receipt["next_task_session_selector"], "U2")

    def test_v2_without_exact_closeout_contract_rejects_no_op(self) -> None:
        config = self.fixture.v2_config(
            fragment_targets=True, include_closeout_routes=False
        )
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        transition = self.fixture.transition(closeout="NO_OP")
        receipt, _ = CHAIN.evaluate_transition(
            config, manifest, transition, CHAIN.initial_state(config)
        )
        self.assertEqual(receipt["terminal_code"], "NO_OP_PROOF_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_current_wpra_routes_bind_full_units_deterministically(self) -> None:
        config = self.fixture.current_v2_config()
        errors = CHAIN.schema_errors(config, CHAIN.CONFIG_SCHEMA, "chain config")
        self.assertEqual(errors, [])
        first_manifest, first = CHAIN.preflight(config, self.fixture.root)
        second_manifest, second = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(first, second)
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(first["terminal_code"], "CHAIN_PREFLIGHT_READY")
        self.assertEqual(first["next_task_session_selector"], "U1")
        self.assertTrue(first_manifest["wpra_v2_bound"])
        binding = first_manifest["execution_bindings"][0]
        self.assertEqual(binding["task_route"]["mode"], "execute-one-swu")
        self.assertEqual(binding["closeout_route"]["mode"], "refresh")
        self.assertIn("validation_contracts", binding)
        self.assertIn("material_package", binding)
        self.assertIn("byte_baselines", binding)
        self.assertIn("gate_contract", binding)

    def test_nested_selected_unit_projection_binds_without_inline_closeout(self) -> None:
        config = self.fixture.nested_selected_unit_v2_config()
        errors = CHAIN.schema_errors(config, CHAIN.CONFIG_SCHEMA, "chain config")
        self.assertEqual(errors, [])
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        self.assertTrue(manifest["wpra_v2_bound"])
        binding = manifest["execution_bindings"][0]
        self.assertEqual(binding["contract_projection"], "nested-selected-unit-precloseout-v1")
        self.assertEqual(binding["task_route"]["mode"], "execute")
        self.assertEqual(
            binding["task_route"]["target"], "work-pack/tasks/U1.md#u1"
        )
        self.assertEqual(binding["closeout_route"]["mode"], "refresh")
        self.assertEqual(
            binding["closeout_route"]["required_inputs"],
            ["precloseout/U1.json"],
        )

    def test_nested_selected_unit_anchor_is_strict_and_ascii_only(self) -> None:
        bad_targets = (
            "../tasks/U1.md#u1",
            "/tasks/U1.md#u1",
            "work-pack/tasks/U1.txt#u1",
            "work-pack/tasks/U1.md#u2",
            "work-pack/tasks/U1.md#u1#extra",
            "work-pack/tasks/U1.md#u\u0131",
        )
        for target in bad_targets:
            with self.subTest(target=target):
                config = self.fixture.nested_selected_unit_v2_config()
                manifest_path = self.fixture.root / "manifest-nested.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["allowed_routes"][0]["target"] = target
                self.fixture.write_json("manifest-nested.json", manifest)
                config = self.fixture.refresh_nested_v2_refs(config)
                _, receipt = CHAIN.preflight(config, self.fixture.root)
                self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
                self.assertIsNone(receipt["next_task_session_selector"])

    def test_nested_selected_unit_partial_inline_closeout_blocks(self) -> None:
        config = self.fixture.nested_selected_unit_v2_config()
        manifest_path = self.fixture.root / "manifest-nested.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"].append({
            "route_id": "partial-closeout-U1",
            "frontier_swu": "U1",
            "capability": "invoke",
            "mode": "refresh",
            "target": "synthetic-work-pack",
            "write_scope": ["plan/U1.json", "continuation/U1.json"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["precloseout/U1.json"],
            "expected_receipt": "closeout/U1.json",
        })
        self.fixture.write_json("manifest-nested.json", manifest)
        config = self.fixture.refresh_nested_v2_refs(config)
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_nested_selected_unit_incomplete_closeout_schema_blocks(self) -> None:
        config = self.fixture.nested_selected_unit_v2_config()
        source_path = self.fixture.root / "source-nested.json"
        source = json.loads(source_path.read_text(encoding="utf-8"))
        del source["execution_contracts"]["units"][0]["closeout_contract"][
            "continuation_router_schema_ref"
        ]
        self.fixture.write_json("source-nested.json", source)
        config = self.fixture.refresh_nested_v2_refs(config)
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_generated_sibling_packages_resolve_without_canonical_tree(self) -> None:
        config = self.fixture.current_v2_config()
        skills = self.fixture.root / "skills"
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
        shutil.copytree(
            SPELL_ROOT,
            skills / "task-session-until-blocker",
            ignore=ignore,
        )
        shutil.copytree(
            CHAIN.WPRA_ROOT,
            skills / "work-pack-readiness-audit",
            ignore=ignore,
        )
        shutil.copytree(
            CHAIN.TASK_SESSION_ROOT,
            skills / "task-session",
            ignore=ignore,
        )
        runner = skills / "task-session-until-blocker/scripts/run_chain.py"
        spec = importlib.util.spec_from_file_location("generated_chain", runner)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        generated = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated)
        self.assertEqual(generated.WPRA_ROOT, skills / "work-pack-readiness-audit")
        self.assertEqual(generated.TASK_SESSION_ROOT, skills / "task-session")
        self.assertFalse((self.fixture.root / "arcana").exists())
        self.assertFalse((self.fixture.root / "spells").exists())
        manifest, receipt = generated.preflight(config, self.fixture.root)
        self.assertIsNotNone(manifest)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")

    def test_exact_ref_predicates_reject_unsafe_or_weak_values(self) -> None:
        valid = {"path": "evidence/a.json", "sha256": "a" * 64, "size_bytes": 0}
        self.assertTrue(CHAIN.is_exact_ref(valid))
        for field, value in (
            ("path", ""),
            ("path", "../a.json"),
            ("path", "/a.json"),
            ("sha256", "A" * 64),
            ("sha256", "g" * 64),
            ("size_bytes", True),
        ):
            reference = copy.deepcopy(valid)
            reference[field] = value
            self.assertFalse(CHAIN.is_exact_ref(reference))
        camel = {"path": "evidence/a.json", "sha256": "a" * 64, "sizeBytes": True}
        self.assertFalse(CHAIN.is_camel_exact_ref(camel))

    def test_current_wpra_binding_drift_blocks(self) -> None:
        config = self.fixture.current_v2_config()
        path = self.fixture.root / "audit-config.json"
        audit = json.loads(path.read_text(encoding="utf-8"))
        audit["execution_bindings"][0]["allowed_writes"] = ["drift.txt"]
        self.fixture.write_json("audit-config.json", audit)
        config["wpra_v2"]["audit_config_ref"] = self.fixture.exact("audit-config.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_current_wpra_false_approval_content_blocks(self) -> None:
        config = self.fixture.current_v2_config()
        self.fixture.write_json("approval-current.json", {"status": "approved"})
        config["approved_epoch"]["decision_gate_approval_receipt_ref"] = self.fixture.exact(
            "approval-current.json"
        )
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "EPOCH_APPROVAL_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_current_wpra_nested_lifecycle_evidence_drift_blocks(self) -> None:
        config = self.fixture.current_v2_config()
        self.fixture.write_json(
            "initial-lifecycle.json", {"status": "drifted-after-selection"}
        )
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "SELECTION_EVIDENCE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_current_wpra_erased_dependency_or_gate_blocks(self) -> None:
        for field, value in (("dependencies", []), ("gate_contract", {})):
            with self.subTest(field=field):
                config = self.fixture.current_v2_config()
                path = self.fixture.root / "contracts.json"
                contracts = json.loads(path.read_text(encoding="utf-8"))
                contracts["units"][1][field] = value
                self.fixture.write_json("contracts.json", contracts)
                config["wpra_v2"]["execution_contracts_ref"] = self.fixture.exact(
                    "contracts.json"
                )
                _, receipt = CHAIN.preflight(config, self.fixture.root)
                self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
                self.assertIsNone(receipt["next_task_session_selector"])

    def test_current_wpra_exact_receipts_block_then_admit_u2(self) -> None:
        config = self.fixture.current_v2_config()
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        current = CHAIN.binding_for(manifest, "U1")
        successor = CHAIN.binding_for(manifest, "U2")
        self.assertIsNotNone(current)
        self.assertIsNotNone(successor)

        self.fixture.write_json("evidence/U1-validation.json", {"status": "pass"})
        validation_ref = self.fixture.exact("evidence/U1-validation.json")
        terminal = {
            "schema_version": "synthetic.terminal/v1",
            "receipt_id": "terminal-u1",
            "work_pack_id": "synthetic-work-pack",
            "unit_id": "U1",
            "swu_id": "SWU-1",
            "task_id": "TASK-1",
            "result": "pass",
            "terminal_mode": "PASS",
            "validation": {
                "status": "pass",
                "command_results": [{
                    "command_id": "V-U1",
                    "status": "pass",
                    "evidence_ref": validation_ref,
                }],
            },
            "evidence_refs": [validation_ref],
            "dependency_dispositions": [],
            "blockers": [],
            "successor": {"unit_id": "SWU-2", "execution_started": False},
            "authority_effect": "none",
            "mutation_ready": False,
        }
        self.fixture.write_json("receipt/U1.json", terminal)
        terminal_ref = self.fixture.exact("receipt/U1.json")
        next_route = {
            "unit_id": "SWU-2",
            "capability": "task-session",
            "mode": "execute-one-swu",
        }
        owner = {
            "schema_version": "synthetic.closeout/v1",
            "receipt_id": "closeout-u1",
            "work_pack_id": "synthetic-work-pack",
            "unit_id": "U1",
            "swu_id": "SWU-1",
            "terminal_receipt_ref": terminal_ref,
            "result": "pass",
            "lifecycle_owner_validation": {
                "status": "pass",
                "allowed_delta_policy": "evidence-only",
                "baseline_status": "exact-absent",
            },
            "target_inventory": ["closeout/U1.json", "next/U1.json"],
            "next_route": next_route,
            "blockers": [],
            "authority_effect": "none",
            "successor_executed": False,
        }
        self.fixture.write_json("closeout/U1.json", owner)
        self.fixture.write_json("next/U1.json", next_route)
        transition = self.fixture.transition()
        transition["terminal_receipt_ref"] = terminal_ref
        transition["closeout"]["owner_receipt_ref"] = self.fixture.exact(
            "closeout/U1.json"
        )
        transition["closeout"][
            "continuation_router_verification_receipt_ref"
        ] = self.fixture.exact("next/U1.json")
        result, advanced_state = CHAIN.evaluate_transition(
            config,
            manifest,
            transition,
            CHAIN.initial_state(config),
            self.fixture.root,
        )
        self.assertEqual(result["terminal_code"], "SUCCESSOR_ADMISSION_INVALID")
        self.assertIsNone(result["next_task_session_selector"])

        self.fixture.write_json(
            "evidence/U1-owner-acceptance.json", {"status": "accepted"}
        )
        dependency_receipts = [
            {"dependencyId": "SWU-1", "artifactRef": terminal_ref},
            {
                "dependencyId": "U1-closeout-pass",
                "artifactRef": self.fixture.exact("closeout/U1.json"),
            },
            {
                "dependencyId": "U1-owner-acceptance-receipt",
                "artifactRef": self.fixture.exact(
                    "evidence/U1-owner-acceptance.json"
                ),
            },
        ]
        selection_request = {
            "schemaVersion": "1.0.0",
            "manifestRef": config["manifest_ref"],
            "auditConfigPath": config["wpra_v2"]["audit_config_ref"]["path"],
            "taskId": "TASK-2",
            "swuId": "SWU-2",
            "explicitConfirmation": {
                "confirmed": True,
                "confirmedBy": "synthetic-owner",
                "confirmationId": "select-u2",
            },
            "dependencyReceipts": dependency_receipts,
            "lifecycleEligibility": {
                "eligible": True,
                "state": "closeout-and-owner-accepted",
                "evidenceRefs": [self.fixture.exact(
                    "evidence/U1-owner-acceptance.json"
                )],
            },
        }
        selection_request_path = "admission/U2/SELECTION-REQUEST.json"
        selection_receipt_path = "admission/U2/SELECTION-RECEIPT.json"
        self.fixture.write_json(selection_request_path, selection_request)
        explicit_digest = CHAIN.digest(selection_request["explicitConfirmation"])
        selection_receipt = {
            "schemaVersion": "1.0.0",
            "selectionVerdict": "select",
            "terminalCode": "SELECTION_READY",
            "requestDigest": CHAIN.digest(selection_request),
            "manifestDigest": config["manifest_ref"]["sha256"],
            "planEpochId": self.fixture.epoch_id,
            "canonicalSemanticDigest": self.fixture.semantic_digest,
            "taskId": "TASK-2",
            "swuId": "SWU-2",
            "unitContractDigest": "b" * 64,
            "dependencyReceiptDigests": [
                item["artifactRef"]["sha256"] for item in dependency_receipts
            ],
            "lifecycleEligibilityDigest": CHAIN.digest(
                selection_request["lifecycleEligibility"]
            ),
            "explicitConfirmationDigest": explicit_digest,
            "selectionIntentSource": "explicit-confirmation",
            "selectionIntentDigest": explicit_digest,
            "authorityEffect": "none",
            "mutationReady": False,
            "reasons": [],
        }
        self.fixture.write_json(selection_receipt_path, selection_receipt)

        task_path = self.fixture.root / "work-pack/tasks/U2.md"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text("# Synthetic U2\n", encoding="utf-8")
        self.fixture.write_json("work-pack.json", {"work_pack_id": "synthetic-work-pack"})
        validation_commands = ["synthetic-validation"]
        self.fixture.write_json("context-U2.json", {
            "task_id": "TASK-2",
            "swu_id": "SWU-2",
            "strict_coverage": True,
            "execution_contract": {
                "writeProfile": "execution-output-only",
                "materialWrites": [],
                "executionOutputs": ["receipt/U2.json"],
                "allowedWrites": ["receipt/U2.json"],
                "validationCommands": validation_commands,
                "lifecycleOwner": "task-session",
                "authorityClass": "private",
                "publicationClass": "private",
            },
        })
        self.fixture.write_json(
            "schemas/plan-manifest.json",
            CHAIN.load_json(CHAIN.WPRA_SCHEMA_ROOT / "plan-semantic-manifest.schema.json"),
        )
        self.fixture.write_json(
            "schemas/selection-receipt.json",
            CHAIN.load_json(CHAIN.WPRA_SELECTION_RECEIPT_SCHEMA),
        )
        mutation_dependencies = [{
            "dependencyId": item["dependencyId"],
            "artifactRef": {
                "path": item["artifactRef"]["path"],
                "sha256": item["artifactRef"]["sha256"],
                "sizeBytes": item["artifactRef"]["size_bytes"],
            },
        } for item in dependency_receipts]
        mutation_request = {
            "schemaVersion": "1.2.0",
            "admissionProfile": "plan-once-selected-unit",
            "executionMode": "routed-mutation",
            "taskId": "TASK-2",
            "swuId": "SWU-2",
            "controlArtifacts": [
                {**self.fixture.camel_exact("work-pack/tasks/U2.md"), "role": "task-contract", "authorityClass": "private"},
                {**self.fixture.camel_exact("work-pack.json"), "role": "work-pack", "authorityClass": "private"},
                {**self.fixture.camel_exact("context-U2.json"), "role": "context-pack", "authorityClass": "private"},
            ],
            "dependencyFrontier": mutation_dependencies,
            "materialWrites": [],
            "executionOutputs": ["receipt/U2.json"],
            "allowedWrites": ["receipt/U2.json"],
            "validationCommands": validation_commands,
            "lifecycleOwner": "task-session",
            "authorityClass": "private",
            "publicationClass": "private",
            "planAdmission": {
                "planManifest": self.fixture.camel_exact("manifest-current.json"),
                "planManifestSchema": self.fixture.camel_exact(
                    "schemas/plan-manifest.json"
                ),
                "selectionReceipt": self.fixture.camel_exact(
                    selection_receipt_path
                ),
                "selectionReceiptSchema": self.fixture.camel_exact(
                    "schemas/selection-receipt.json"
                ),
                "planEpochId": self.fixture.epoch_id,
                "unitContractDigest": "b" * 64,
                "attemptId": "synthetic-u2-attempt",
                "targetBaselines": [{
                    "path": "receipt/U2.json",
                    "state": "absent",
                    "sha256": None,
                    "sizeBytes": None,
                }],
                "structuredValidationContracts": successor[
                    "validation_contracts"
                ],
                "validationContractDigest": CHAIN.digest(
                    successor["validation_contracts"]
                ),
            },
        }
        mutation_request_path = "admission/U2/MUTATION-ADMISSION-REQUEST.json"
        mutation_receipt_path = "admission/U2/MUTATION-ADMISSION-RECEIPT.json"
        self.fixture.write_json(mutation_request_path, mutation_request)
        verifier = runpy.run_path(
            str(CHAIN.MUTATION_VERIFIER), run_name="mutation_fixture"
        )
        mutation_receipt = verifier["resolve_mutation_admission"](
            mutation_request,
            self.fixture.root,
            CHAIN.load_json(CHAIN.MUTATION_REQUEST_SCHEMA),
        )
        self.assertEqual(mutation_receipt["admissionVerdict"], "admit")
        self.fixture.write_json(mutation_receipt_path, mutation_receipt)
        transition["wpra_v2_evidence"] = {
            "selection_request_ref": self.fixture.exact(selection_request_path),
            "selection_receipt_ref": self.fixture.exact(selection_receipt_path),
            "mutation_admission_request_ref": self.fixture.exact(
                mutation_request_path
            ),
            "mutation_admission_receipt_ref": self.fixture.exact(
                mutation_receipt_path
            ),
        }
        result, _ = CHAIN.evaluate_transition(
            config,
            manifest,
            transition,
            CHAIN.initial_state(config),
            self.fixture.root,
        )
        self.assertEqual(result["terminal_code"], "NEXT_SELECTOR_READY")
        self.assertEqual(result["next_task_session_selector"], "U2")
        successful_receipt = copy.deepcopy(result)

        transitions, persisted_state = CHAIN.open_chain_state(
            config, manifest, self.fixture.root
        )
        self.assertEqual(persisted_state["request_count"], 0)
        CHAIN.persist_transition(
            transitions, transition, successful_receipt, advanced_state
        )

        self.fixture.write_json(
            "evidence/U1-owner-acceptance.json", {"status": "drifted"}
        )
        result, _ = CHAIN.evaluate_transition(
            config,
            manifest,
            transition,
            CHAIN.initial_state(config),
            self.fixture.root,
        )
        self.assertEqual(result["terminal_code"], "SUCCESSOR_ADMISSION_INVALID")
        self.assertIsNone(result["next_task_session_selector"])
        with self.assertRaisesRegex(ValueError, "differs from replay"):
            CHAIN.open_chain_state(config, manifest, self.fixture.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)

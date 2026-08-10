#!/usr/bin/env python3
"""Validate approved-epoch, cursor, NO_OP, and compensation chain behavior."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
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

    def v2_config(self) -> dict[str, object]:
        frontier = ["U1", "U2"]
        routes = []
        for unit_id in frontier:
            routes.extend(
                [
                    {
                        "route_id": f"task-session-{unit_id}",
                        "frontier_swu": unit_id,
                        "capability": "task-session",
                        "mode": "execute",
                        "target": unit_id,
                        "write_scope": [f"product/{unit_id}"],
                        "effect_class": "repository-local-reversible",
                        "required_inputs": [f"contract/{unit_id}"],
                        "expected_receipt": f"receipt/{unit_id}",
                    },
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
                    },
                ]
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
            self.config, self.fixture.root
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
        _, reloaded = CHAIN.open_chain_state(self.config, self.fixture.root)
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

    def test_v2_manifest_missing_closeout_route_blocks(self) -> None:
        config = self.fixture.v2_config()
        manifest_path = self.fixture.root / "manifest-v2.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["allowed_routes"] = [
            route
            for route in manifest["allowed_routes"]
            if route["route_id"] != "closeout-U2"
        ]
        manifest["allowed_routes_digest"] = CHAIN.digest(manifest["allowed_routes"])
        manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
        config["manifest_ref"] = self.fixture.exact("manifest-v2.json")
        _, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "MANIFEST_SHAPE_INVALID")
        self.assertIsNone(receipt["next_task_session_selector"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

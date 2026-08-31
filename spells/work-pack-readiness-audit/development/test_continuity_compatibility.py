#!/usr/bin/env python3
"""Synthetic compatibility and adversarial tests for typed completion continuity."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


DEVELOPMENT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(DEVELOPMENT_ROOT))

import test_plan_once_selection as PLAN  # noqa: E402


def rewrite_exact_refs(value, path: str, reference: dict[str, object]) -> None:
    if isinstance(value, dict):
        if set(value) == {"path", "sha256", "size_bytes"} and value["path"] == path:
            value.update(reference)
            return
        for child in value.values():
            rewrite_exact_refs(child, path, reference)
    elif isinstance(value, list):
        for child in value:
            rewrite_exact_refs(child, path, reference)


def rewrite_binding_ids(value, suffix: str) -> None:
    if isinstance(value, dict):
        if isinstance(value.get("binding_id"), str):
            value["binding_id"] += suffix
        for child in value.values():
            rewrite_binding_ids(child, suffix)
    elif isinstance(value, list):
        for child in value:
            rewrite_binding_ids(child, suffix)


class TypedContinuityCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan_case = PLAN.PlanOnceSelectionTests()
        self.plan_case.setUp()
        self.root = self.plan_case.fixture.root
        self.config = self.plan_case.config()
        self.owner_path = "receipts/owner-U1.json"
        self.owner_schema_path = "receipts/owner-U1.schema.json"
        self.cursor_path = "receipts/cursor-U1.json"
        self.terminal_path = "receipts/U1.json"
        self._add_second_unit()
        self._write_valid_continuity_artifacts()
        self._install_typed_continuity()

    def tearDown(self) -> None:
        self.plan_case.tearDown()

    def write_json(self, relative: str, value: dict[str, object]) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def load_json(self, relative: str) -> dict[str, object]:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def exact(self, relative: str) -> dict[str, object]:
        return PLAN.exact(self.root, relative)

    def refresh_config_ref(self, relative: str) -> None:
        rewrite_exact_refs(self.config, relative, self.exact(relative))

    def _add_second_unit(self) -> None:
        first = self.config["execution_bindings"][0]
        first["canonical_successors"] = ["U2"]
        second = copy.deepcopy(first)
        rewrite_binding_ids(second, "-U2")
        second.update(
            unit_id="U2",
            task_id="TASK-U2",
            swu_id="SWU-U2",
            dependencies=["U1"],
            canonical_successors=["__complete__"],
            material_writes=["target-U2.txt"],
            execution_outputs=["receipts/U2.json"],
            allowed_writes=["target-U2.txt", "receipts/U2.json"],
        )
        second["validation_contracts"][0]["command_id"] = "verify-U2"
        second["target_dispositions"][0].update(
            path="target-U2.txt", parent_path="."
        )
        second["target_dispositions"][1].update(
            path="receipts/U2.json", parent_path="receipts"
        )
        second["output_contracts"][0]["expected_path"] = "target-U2.txt"
        second["output_contracts"][1]["expected_path"] = "receipts/U2.json"
        self.config["execution_bindings"].append(second)

        second_closeout = copy.deepcopy(self.config["closeout_bindings"][0])
        second_closeout["unit_id"] = "U2"
        rewrite_binding_ids(second_closeout, "-U2")
        self.config["closeout_bindings"].append(second_closeout)

        second_typed = copy.deepcopy(
            self.config["task_session_closeout_contracts"][0]
        )
        second_typed["unit_id"] = "U2"
        rewrite_binding_ids(second_typed, "-U2")
        self.config["task_session_closeout_contracts"].append(second_typed)

        expected = copy.deepcopy(
            self.config["receipt_bindings"]["expected_receipt_refs"][0]
        )
        expected["binding_id"] = "expected-U2"
        self.config["receipt_bindings"]["expected_receipt_refs"].append(expected)

        routes = self.config["execution_policy"]["allowed_routes"]
        for route in copy.deepcopy(routes):
            route["route_id"] = route["route_id"].replace("U1", "U2")
            route["frontier_swu"] = "U2"
            route["target"] = route["target"].replace("U1", "U2")
            route["write_scope"] = [
                item.replace("U1", "U2").replace("target.txt", "target-U2.txt")
                for item in route["write_scope"]
            ]
            route["expected_receipt"] = route["expected_receipt"].replace(
                "U1", "U2"
            )
            routes.append(route)
        self.config["execution_policy"]["allowed_routes_digest"] = (
            PLAN.AUDIT.digest_bytes(PLAN.AUDIT.canonical_bytes(routes))
        )

        evidence = json.loads(
            self.plan_case.fixture.evidence_path.read_text(encoding="utf-8")
        )
        evidence["successor"] = "U2"
        evidence["continuation"] = "U2"
        self.plan_case.fixture.evidence_path.write_text(
            json.dumps(evidence, sort_keys=True), encoding="utf-8"
        )
        PLAN.refresh_evidence_refs(self.config, self.plan_case.fixture.exact())

    def _write_valid_continuity_artifacts(self) -> None:
        owner_schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "schema_version",
                "owner",
                "task_id",
                "swu_id",
                "result",
                "successor",
                "authority_effect",
                "residue",
            ],
            "properties": {
                "schema_version": {"const": "synthetic-owner-closeout.v1"},
                "owner": {"const": "synthetic-owner"},
                "task_id": {"const": "TASK-U1"},
                "swu_id": {"const": "SWU-U1"},
                "result": {"enum": ["pass", "no-op"]},
                "successor": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["unit_id", "selected", "executed"],
                    "properties": {
                        "unit_id": {"const": "U2"},
                        "selected": {"const": False},
                        "executed": {"const": False},
                    },
                },
                "authority_effect": {"const": "none"},
                "residue": {"type": "array", "maxItems": 0},
            },
        }
        owner_receipt = {
            "schema_version": "synthetic-owner-closeout.v1",
            "owner": "synthetic-owner",
            "task_id": "TASK-U1",
            "swu_id": "SWU-U1",
            "result": "no-op",
            "successor": {"unit_id": "U2", "selected": False, "executed": False},
            "authority_effect": "none",
            "residue": [],
        }
        cursor = {"cursor": "U2", "successor_executed": False}
        self.write_json(self.owner_schema_path, owner_schema)
        self.write_json(self.owner_path, owner_receipt)
        self.write_json(self.cursor_path, cursor)
        terminal = {
            "schema_version": "task-session.governance-terminal-receipt.v1",
            "task_id": "TASK-U1",
            "swu_id": "SWU-U1",
            "result": "pass",
            "closeout_join": {
                "required_owner_capabilities": ["synthetic-owner"],
                "joined_owner_receipts": [
                    {
                        "owner_capability": "synthetic-owner",
                        "receipt_ref": self.exact(self.owner_path),
                        "result": "no-op",
                    }
                ],
                "continuation": {
                    "policy": "emit-cursor-never-execute-successor",
                    "cursor_ref": self.exact(self.cursor_path),
                    "successor_executed": False,
                },
            },
        }
        self.write_json(self.terminal_path, terminal)

    def _install_typed_continuity(self) -> None:
        terminal_ref = self.exact(self.terminal_path)
        owner_ref = self.exact(self.owner_path)
        schema_ref = self.exact(self.owner_schema_path)
        cursor_ref = self.exact(self.cursor_path)
        self.config["continuity_projection"] = {
            "cursor": "U2",
            "completed_unit_receipt_refs": [
                {
                    "binding_id": "completed-U1",
                    "owner_ref": "task-session",
                    "artifact_ref": terminal_ref,
                    "selector": "/result",
                }
            ],
            "joined_closeout_receipt_refs": [
                {
                    "evidence_profile": "task-session-joined-owner-closeout-v1",
                    "binding_id": "joined-closeout-U1",
                    "owner_ref": "task-session",
                    "terminal_receipt_ref": terminal_ref,
                    "joined_owner_receipt_ref": owner_ref,
                    "owner_receipt_schema_ref": {
                        "binding_id": "owner-schema-U1",
                        "owner_ref": "synthetic-owner",
                        "artifact_ref": schema_ref,
                        "selector": "",
                    },
                    "continuation_cursor_ref": cursor_ref,
                }
            ],
            "projected_next_successor": {
                "unit_id": "U2",
                "canonical_successor_ref": self.plan_case.fixture.binding(
                    "canonical-successor", "/successor"
                ),
                "projection_owner_ref": "work-pack-readiness-audit",
                "equivalence_validator_ref": self.plan_case.fixture.binding(
                    "equivalence-validator", "/equivalence"
                ),
                "continuation_router_verification_receipt_ref": (
                    self.plan_case.fixture.binding(
                        "continuation-verification", "/continuation"
                    )
                ),
                "authority_effect": "none",
            },
        }

    def audit(self) -> dict[str, object]:
        errors = PLAN.AUDIT.schema_errors(
            self.config,
            PLAN.AUDIT.load_json(PLAN.AUDIT.CONFIG_SCHEMA_V2),
            "typed continuity config",
        )
        self.assertEqual(errors, [])
        return PLAN.AUDIT.audit_v2(self.config, self.root)

    def blocker_codes(self) -> set[str]:
        return {item["code"] for item in self.audit()["blockers"]}

    def rewrite_terminal(self, terminal: dict[str, object]) -> None:
        self.write_json(self.terminal_path, terminal)
        self.refresh_config_ref(self.terminal_path)

    def rewrite_owner(
        self, owner: dict[str, object], *, joined_result: str | None = None
    ) -> None:
        self.write_json(self.owner_path, owner)
        owner_ref = self.exact(self.owner_path)
        closeout = self.config["continuity_projection"][
            "joined_closeout_receipt_refs"
        ][0]
        closeout["joined_owner_receipt_ref"] = owner_ref
        terminal = self.load_json(self.terminal_path)
        joined = terminal["closeout_join"]["joined_owner_receipts"][0]
        joined["receipt_ref"] = owner_ref
        if joined_result is not None:
            joined["result"] = joined_result
        self.rewrite_terminal(terminal)

    def test_valid_joined_owner_no_op_proves_exact_prefix(self) -> None:
        report = self.audit()
        self.assertEqual(report["verdict"], "pass")
        self.assertEqual(report["terminal_code"], "CONTRACT_READY")
        self.assertIsNone(report["selected_unit"])
        self.assertFalse(report["mutation_ready"])
        self.assertEqual(report["authority_effect"], "none")
        self.assertEqual(report["manifest"]["ready_frontier"], ["U2"])
        continuity = report["manifest"]["completion_continuity"]
        self.assertEqual(continuity["next_unit"], "U2")
        self.assertEqual(
            [item["unit_id"] for item in continuity["completed_prefix"]], ["U1"]
        )
        proof = continuity["completed_prefix"][0]
        self.assertEqual(proof["joined_owner_capability"], "synthetic-owner")
        self.assertEqual(proof["joined_owner_result"], "no-op")
        self.assertEqual(proof["canonical_successor"], "U2")

    def test_missing_join_blocks(self) -> None:
        terminal = self.load_json(self.terminal_path)
        terminal.pop("closeout_join")
        self.rewrite_terminal(terminal)
        self.assertIn("CONTINUITY_JOIN_MISSING", self.blocker_codes())

    def test_wrong_owner_capability_blocks(self) -> None:
        terminal = self.load_json(self.terminal_path)
        terminal["closeout_join"]["joined_owner_receipts"][0][
            "owner_capability"
        ] = "other-owner"
        self.rewrite_terminal(terminal)
        self.assertIn(
            "CONTINUITY_OWNER_CAPABILITY_MISMATCH", self.blocker_codes()
        )

    def test_wrong_bound_owner_path_hash_or_size_blocks(self) -> None:
        mutations = {
            "path": "receipts/not-the-owner.json",
            "sha256": "f" * 64,
            "size_bytes": self.exact(self.owner_path)["size_bytes"] + 1,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                terminal = self.load_json(self.terminal_path)
                terminal["closeout_join"]["joined_owner_receipts"][0][
                    "receipt_ref"
                ][field] = value
                self.rewrite_terminal(terminal)
                self.assertIn(
                    "CONTINUITY_OWNER_RECEIPT_REF_MISMATCH",
                    self.blocker_codes(),
                )
                self._write_valid_continuity_artifacts()
                self._install_typed_continuity()

    def test_missing_owner_receipt_blocks_snapshot(self) -> None:
        (self.root / self.owner_path).unlink()
        self.assertIn("FROZEN_INPUT_MISMATCH", self.blocker_codes())

    def test_blocked_or_invalid_owner_receipt_blocks(self) -> None:
        owner = self.load_json(self.owner_path)
        owner["result"] = "block"
        self.rewrite_owner(owner, joined_result="block")
        self.assertIn("CONTINUITY_OWNER_RECEIPT_INVALID", self.blocker_codes())

        self._write_valid_continuity_artifacts()
        self._install_typed_continuity()
        owner = self.load_json(self.owner_path)
        owner.pop("schema_version")
        self.rewrite_owner(owner)
        self.assertIn("CONTINUITY_OWNER_RECEIPT_INVALID", self.blocker_codes())

    def test_successor_execution_boundary_blocks(self) -> None:
        terminal = self.load_json(self.terminal_path)
        terminal["closeout_join"]["continuation"]["successor_executed"] = True
        self.rewrite_terminal(terminal)
        self.assertIn("CONTINUITY_BOUNDARY_INVALID", self.blocker_codes())

    def test_selector_spoof_is_schema_invalid(self) -> None:
        closeout = self.config["continuity_projection"][
            "joined_closeout_receipt_refs"
        ][0]
        closeout["selector"] = "/closeout_join/joined_owner_receipts/0/result"
        errors = PLAN.AUDIT.schema_errors(
            self.config,
            PLAN.AUDIT.load_json(PLAN.AUDIT.CONFIG_SCHEMA_V2),
            "selector spoof",
        )
        self.assertNotEqual(errors, [])

    def test_terminal_owner_and_cursor_replay_blocks(self) -> None:
        continuity = self.config["continuity_projection"]
        completion = copy.deepcopy(continuity["completed_unit_receipt_refs"][0])
        completion["binding_id"] = "completed-U2"
        closeout = copy.deepcopy(continuity["joined_closeout_receipt_refs"][0])
        closeout["binding_id"] = "joined-closeout-U2"
        closeout["owner_receipt_schema_ref"]["binding_id"] = (
            "owner-schema-U2-replay"
        )
        continuity["completed_unit_receipt_refs"].append(completion)
        continuity["joined_closeout_receipt_refs"].append(closeout)
        continuity["cursor"] = "__complete__"
        continuity["projected_next_successor"].update(
            unit_id=None,
            canonical_successor_ref=None,
            continuation_router_verification_receipt_ref=None,
        )
        self.assertIn("CONTINUITY_RECEIPT_REPLAY", self.blocker_codes())

    def test_non_prefix_completion_blocks(self) -> None:
        terminal = self.load_json(self.terminal_path)
        terminal["swu_id"] = "SWU-OTHER"
        self.rewrite_terminal(terminal)
        self.assertIn("CONTINUITY_NON_PREFIX_COMPLETION", self.blocker_codes())

    def test_wrong_next_successor_blocks(self) -> None:
        schema = self.load_json(self.owner_schema_path)
        schema["properties"]["successor"]["properties"]["unit_id"] = {
            "const": "U3"
        }
        self.write_json(self.owner_schema_path, schema)
        self.refresh_config_ref(self.owner_schema_path)
        owner = self.load_json(self.owner_path)
        owner["successor"]["unit_id"] = "U3"
        self.rewrite_owner(owner)
        self.assertIn("CONTINUITY_FRONTIER_MISMATCH", self.blocker_codes())

    def test_legacy_flat_completed_prefix_blocks_fail_closed(self) -> None:
        terminal = self.load_json(self.terminal_path)
        terminal["lifecycle_owner_validation"] = {"status": "pass"}
        self.rewrite_terminal(terminal)
        terminal_ref = self.exact(self.terminal_path)
        self.config["continuity_projection"]["joined_closeout_receipt_refs"] = [
            {
                "binding_id": "legacy-closeout-U1",
                "owner_ref": "task-session",
                "artifact_ref": terminal_ref,
                "selector": "/lifecycle_owner_validation/status",
            }
        ]
        self.assertIn("CONTINUITY_TYPED_JOIN_REQUIRED", self.blocker_codes())


if __name__ == "__main__":
    unittest.main(verbosity=2)

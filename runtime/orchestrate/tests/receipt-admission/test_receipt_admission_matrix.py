#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
JOIN_TEST_PATH = ARCANUM_ROOT / "runtime/orchestrate/tests/native-join/test_native_join_contract.py"
COMPILE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"
REDUCE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/reduce"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"
MATRIX = Path(__file__).resolve().parent / "receipt-admission-matrix.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


coordinator = load_module("native_dispatch_coordinator_admission", COORDINATOR_PATH)
join_contract = load_module("native_join_contract_admission", JOIN_TEST_PATH)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pass_receipts() -> list[dict[str, Any]]:
    return [load_json(path) for path in sorted((REDUCE / "pass").glob("*.json"))]


def mutate_receipts(case: dict[str, Any]) -> list[dict[str, Any]]:
    receipts = copy.deepcopy(pass_receipts())
    operation = case["operation"]
    if operation == "remove_receipt":
        return [receipt for receipt in receipts if receipt["action_id"] != case["action_id"]]
    index = int(case.get("receipt_index", 0))
    if operation == "delete_field":
        del receipts[index][case["field"]]
    elif operation == "set_field":
        receipts[index][case["field"]] = case["value"]
    elif operation == "set_status":
        receipts[index]["status"] = case["status"]
        receipts[index]["validation"] = case["validation"]
        receipts[index]["blockers"] = case["blockers"]
    elif operation == "unexpected_receipt":
        receipts[index]["action_id"] = case["action_id"]
    elif operation == "duplicate_receipt":
        receipts.append(copy.deepcopy(receipts[index]))
    else:
        raise AssertionError(f"unknown operation: {operation}")
    return receipts


class ReceiptAdmissionMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dispatch = load_json(COMPILE / "valid-two-wave.json")
        cls.state = load_json(COMPILE / "expected-state.json")
        cls.run_plan = load_json(COMPILE / "expected-run-plan.json")
        cls.matrix = load_json(MATRIX)
        cls.state_schema = load_json(SCHEMAS / "state.schema.json")
        cls.gate_schema = load_json(SCHEMAS / "gate-decision.schema.json")
        cls.action_set_schema = load_json(SCHEMAS / "action-set.schema.json")

    def test_every_reducer_rejection_blocks_and_emits_zero_dependent_actions(self) -> None:
        for case in self.matrix["cases"]:
            if case["boundary"] != "reducer":
                continue
            with self.subTest(case=case["case_id"]):
                receipts = mutate_receipts(case)
                state, gate, action_set = coordinator.reduce_wave_receipts(
                    self.dispatch, self.state, self.run_plan, receipts
                )
                Draft202012Validator(self.state_schema).validate(state)
                Draft202012Validator(self.gate_schema).validate(gate)
                Draft202012Validator(self.action_set_schema).validate(action_set)
                self.assertEqual(state["state"], "gate_block")
                self.assertEqual(state["eligible_action_ids"], [])
                self.assertEqual(gate["decision"], "gate_block")
                self.assertEqual(gate["next_action_ids"], [])
                self.assertEqual(action_set["decision"], "gate_block")
                self.assertEqual(action_set["actions"], [])
                for blocker in case["expected_blockers"]:
                    self.assertIn(blocker, gate["blockers"])

    def test_agent_identity_mismatch_blocks_at_join_normalization(self) -> None:
        case = next(item for item in self.matrix["cases"] if item["case_id"] == "agent-id-mismatch")
        action = self.run_plan["actions"][0]
        expected_agent = pass_receipts()[0]["agent_id"]
        result = copy.deepcopy(pass_receipts()[0])
        result["agent_id"] = case["value"]
        normalized = join_contract.normalize_result(action, expected_agent, result)
        self.assertEqual(normalized["status"], "block")
        self.assertEqual(normalized["validation"], "block")
        self.assertEqual(normalized["agent_id"], expected_agent)
        self.assertEqual(normalized["blockers"], case["expected_blockers"])

    def test_malformed_or_identity_mismatched_receipts_are_not_admitted(self) -> None:
        receipts = copy.deepcopy(pass_receipts())
        del receipts[0]["agent_id"]
        receipts[1]["role"] = "wrong-role"
        admitted, blockers = coordinator._admit_receipts(
            self.run_plan["actions"], receipts
        )
        self.assertNotIn("spawn-0001", [item["action_id"] for item in admitted])
        self.assertNotIn("spawn-0002", [item["action_id"] for item in admitted])
        self.assertIn("spawn-0003", [item["action_id"] for item in admitted])
        self.assertTrue(any("missing required field 'agent_id'" in item for item in blockers))
        self.assertTrue(any("receipt role 'wrong-role'" in item for item in blockers))

    def test_matrix_covers_required_failure_classes_and_bindings(self) -> None:
        ids = {case["case_id"] for case in self.matrix["cases"]}
        required = {
            "missing-required",
            "malformed-missing-agent-id",
            "dispatch-mismatch",
            "run-mismatch",
            "wave-mismatch",
            "step-mismatch",
            "role-mismatch",
            "capability-mismatch",
            "agent-id-mismatch",
            "timed-out",
            "failed",
            "blocked",
            "non-pass-validation",
        }
        self.assertTrue(required <= ids)


if __name__ == "__main__":
    unittest.main()

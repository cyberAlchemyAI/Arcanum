#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
COMPILE_FIXTURES = Path(__file__).resolve().parent / "fixtures/compile"
REDUCE_FIXTURES = Path(__file__).resolve().parent / "fixtures/reduce"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_reduce", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {SCRIPT}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def pass_receipts():
    return [load_json(path) for path in sorted((REDUCE_FIXTURES / "pass").glob("*.json"))]


def inputs():
    return (
        load_json(COMPILE_FIXTURES / "valid-two-wave.json"),
        load_json(COMPILE_FIXTURES / "expected-state.json"),
        load_json(COMPILE_FIXTURES / "expected-run-plan.json"),
    )


def snapshot(path: Path) -> dict[str, bytes]:
    return {
        str(candidate.relative_to(path)): candidate.read_bytes()
        for candidate in sorted(path.rglob("*"))
        if candidate.is_file()
    }


class ReduceWaveReceiptsTests(unittest.TestCase):
    def test_all_pass_receipts_open_next_wave_exactly(self) -> None:
        dispatch, state, run_plan = inputs()
        next_state, gate, action_set = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        self.assertEqual(gate, load_json(REDUCE_FIXTURES / "expected-pass-gate.json"))
        self.assertEqual(next_state, load_json(REDUCE_FIXTURES / "expected-pass-state.json"))
        self.assertEqual(action_set, load_json(REDUCE_FIXTURES / "expected-pass-actions.json"))

    def test_nonpass_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = pass_receipts()
        receipts[1]["status"] = "block"
        receipts[1]["validation"] = "block"
        receipts[1]["blockers"] = ["deterministic failure"]
        next_state, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate, load_json(REDUCE_FIXTURES / "expected-block-gate.json"))
        self.assertEqual(next_state, load_json(REDUCE_FIXTURES / "expected-block-state.json"))
        self.assertEqual(action_set, load_json(REDUCE_FIXTURES / "expected-block-actions.json"))

    def test_missing_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = [receipt for receipt in pass_receipts() if receipt["action_id"] != "spawn-0002"]
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertIn("missing receipt for action 'spawn-0002'", gate["blockers"])
        self.assertEqual(action_set["actions"], [])

    def test_identity_mismatch_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = copy.deepcopy(pass_receipts())
        receipts[2]["capability_ref"] = "wrong-capability"
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertTrue(any("capability_ref" in blocker for blocker in gate["blockers"]))
        self.assertEqual(action_set["actions"], [])

    def test_malformed_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = copy.deepcopy(pass_receipts())
        del receipts[0]["agent_id"]
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertIn("receipt[0]: missing required field 'agent_id'", gate["blockers"])
        self.assertEqual(action_set["actions"], [])

    def test_reduction_is_byte_stable_for_same_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first"
            second = root / "second"
            args = (
                COMPILE_FIXTURES / "valid-two-wave.json",
                COMPILE_FIXTURES / "expected-state.json",
                COMPILE_FIXTURES / "expected-run-plan.json",
                REDUCE_FIXTURES / "pass",
            )
            coordinator.reduce_to_directory(*args, first)
            coordinator.reduce_to_directory(*args, second)
            self.assertEqual(snapshot(first), snapshot(second))

    def test_receipts_and_outputs_validate_against_runtime_schemas(self) -> None:
        dispatch, state, run_plan = inputs()
        next_state, gate, action_set = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        action_schema = load_json(SCHEMAS / "action.schema.json")
        receipt_schema = load_json(SCHEMAS / "receipt.schema.json")
        state_schema = load_json(SCHEMAS / "state.schema.json")
        gate_schema = load_json(SCHEMAS / "gate-decision.schema.json")
        action_set_schema = load_json(SCHEMAS / "action-set.schema.json")
        resolver = RefResolver.from_schema(
            action_set_schema,
            store={action_schema["$id"]: action_schema, "action.schema.json": action_schema},
        )
        for receipt in pass_receipts():
            Draft202012Validator(receipt_schema).validate(receipt)
        Draft202012Validator(state_schema).validate(next_state)
        Draft202012Validator(gate_schema).validate(gate)
        Draft202012Validator(action_set_schema, resolver=resolver).validate(action_set)


if __name__ == "__main__":
    unittest.main()

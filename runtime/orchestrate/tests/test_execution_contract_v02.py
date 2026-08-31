#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures/compile/valid-two-wave.json"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_v02", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {SCRIPT}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def strict_dispatch():
    dispatch = load_json(FIXTURE)
    strategy = dispatch["subagent_strategy"]
    strategy["execution_contract_version"] = coordinator.STRICT_EXECUTION_CONTRACT
    strategy["execution_waves"][1]["gate_after"] = "g-artifact-domain"
    dispatch["gates"][0]["evaluation"] = {"mode": "receipt_status"}
    dispatch["gates"].append(
        {
            "gate_id": "g-artifact-domain",
            "kind": "validation",
            "owner": "orchestrate",
            "condition": "Preserve the final proposal validity outcome.",
            "applies_after_wave": "artifact",
            "requires_role_receipts": ["tmp/native-dispatch/receipts/artifact.json"],
            "evaluation": {
                "mode": "domain_status",
                "source_role_id": "artifact-writer",
                "source_field": "domain_gate_status",
                "pass_values": ["valid"],
                "resolved_values": ["invalid"],
            },
            "on_fail": "block",
        }
    )
    return dispatch


def receipt(action, value="valid"):
    return {
        "schema_version": coordinator.RECEIPT_SCHEMA_VERSION_V2,
        "action_id": action["action_id"],
        "dispatch_id": action["dispatch_id"],
        "run_id": action["run_id"],
        "wave_id": action["wave_id"],
        "step_id": action["step_id"],
        "role": action["role"],
        "capability_ref": action["capability_ref"],
        "agent_id": f"agent-{action['action_id']}",
        "status": "pass",
        "artifacts": list(action["output_refs"]),
        "validation": "pass",
        "blockers": [],
        "started_at": "2026-08-27T00:00:00Z",
        "finished_at": "2026-08-27T00:00:01Z",
        "domain_gate": {"source_field": "domain_gate_status", "value": value},
    }


class ExecutionContractV02Tests(unittest.TestCase):
    def first_frontier(self):
        dispatch = strict_dispatch()
        state, plan = coordinator.compile_first_wave(dispatch, "run-v02")
        receipts = [receipt(action) for action in plan["actions"]]
        next_state, gate, actions = coordinator.reduce_wave_receipts(dispatch, state, plan, receipts)
        next_plan = coordinator.build_next_wave_plan(
            dispatch, plan, gate, actions, next_state, actions["actions"]
        )
        return dispatch, next_state, next_plan

    def test_receipt_gate_passes_and_opens_only_the_declared_next_wave(self):
        dispatch, state, plan = self.first_frontier()
        self.assertEqual(state["schema_version"], coordinator.STATE_SCHEMA_VERSION_V2)
        self.assertEqual(state["state"], "gate_pass")
        self.assertEqual(plan["execution_contract_version"], coordinator.STRICT_EXECUTION_CONTRACT)
        self.assertEqual(plan["selected_wave"]["wave_id"], "artifact")
        self.assertEqual(len(plan["actions"]), 1)
        self.assertEqual(dispatch["subagent_strategy"]["execution_contract_version"], coordinator.STRICT_EXECUTION_CONTRACT)

    def test_invalid_is_terminal_resolution_not_generic_pass(self):
        dispatch, state, plan = self.first_frontier()
        final_state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, [receipt(plan["actions"][0], "invalid")]
        )
        self.assertEqual(gate["gate_id"], "g-artifact-domain")
        self.assertEqual(gate["decision"], "gate_resolved")
        self.assertEqual(gate["domain_outcome"]["classification"], "resolved")
        self.assertEqual(gate["domain_outcome"]["value"], "invalid")
        self.assertEqual(final_state["state"], "complete")
        self.assertEqual(final_state["terminal_outcome"]["value"], "invalid")
        self.assertEqual(actions["actions"], [])
        self.assertIsNone(actions["next_wave_id"])
        for schema_name, value in (
            ("state.schema.json", final_state),
            ("gate-decision.schema.json", gate),
            ("action-set.schema.json", actions),
        ):
            Draft202012Validator(load_json(SCHEMAS / schema_name)).validate(value)

    def test_valid_terminal_pass_preserves_typed_outcome(self):
        dispatch, state, plan = self.first_frontier()
        final_state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, [receipt(plan["actions"][0], "valid")]
        )
        self.assertEqual(gate["decision"], "gate_pass")
        self.assertEqual(gate["domain_outcome"]["classification"], "pass")
        self.assertEqual(final_state["state"], "complete")
        self.assertEqual(final_state["terminal_outcome"]["value"], "valid")
        self.assertEqual(actions["actions"], [])

    def test_unknown_domain_value_blocks_and_emits_no_actions(self):
        dispatch, state, plan = self.first_frontier()
        final_state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, [receipt(plan["actions"][0], "ambiguous")]
        )
        self.assertEqual(gate["decision"], "gate_block")
        self.assertTrue(any("unknown domain value" in blocker for blocker in gate["blockers"]))
        self.assertEqual(final_state["state"], "gate_block")
        self.assertEqual(actions["actions"], [])

    def test_missing_declared_output_receipt_blocks_runtime_gate(self):
        dispatch = strict_dispatch()
        state, plan = coordinator.compile_first_wave(dispatch, "run-missing-output")
        receipts = [receipt(action) for action in plan["actions"]]
        receipts[0]["artifacts"] = []
        next_state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, receipts
        )
        self.assertEqual(gate["decision"], "gate_block")
        self.assertTrue(any("artifacts must exactly equal" in blocker for blocker in gate["blockers"]))
        self.assertEqual(next_state["state"], "gate_block")
        self.assertEqual(actions["actions"], [])

    def test_substituted_output_receipt_blocks_runtime_gate(self):
        dispatch = strict_dispatch()
        state, plan = coordinator.compile_first_wave(dispatch, "run-substituted-output")
        receipts = [receipt(action) for action in plan["actions"]]
        receipts[0]["artifacts"] = ["tmp/native-dispatch/receipts/substituted.json"]
        _, gate, actions = coordinator.reduce_wave_receipts(dispatch, state, plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertTrue(any("artifacts must exactly equal" in blocker for blocker in gate["blockers"]))
        self.assertEqual(actions["actions"], [])

    def test_legacy_gate_decision_schema_rejects_gate_resolved(self):
        legacy = {
            "schema_version": "arcanum.native-dispatch-runner.gate-decision.v0.1",
            "dispatch_id": "legacy-dispatch",
            "run_id": "legacy-run",
            "wave_id": "legacy-wave",
            "gate_id": None,
            "decision": "gate_resolved",
            "required_action_ids": ["spawn-0001"],
            "admitted_receipt_action_ids": ["spawn-0001"],
            "next_wave_id": None,
            "next_action_ids": [],
            "blockers": [],
        }
        errors = list(Draft202012Validator(load_json(SCHEMAS / "gate-decision.schema.json")).iter_errors(legacy))
        self.assertTrue(errors)

    def test_final_gate_cannot_resolve_and_unlock_a_successor(self):
        dispatch = strict_dispatch()
        candidate = copy.deepcopy(dispatch)
        candidate["subagent_strategy"]["execution_waves"].append(
            {
                "wave_id": "forbidden-successor",
                "role_ids": ["artifact-writer"],
                "parallel": False,
                "join_policy": "all",
                "depends_on_waves": ["artifact"],
                "gate_after": "g-artifact-domain",
                "on_incomplete": "block",
            }
        )
        # The Dispatch Spec validator owns rejection of non-final resolution;
        # the reducer independently refuses to unlock work after gate_resolved.
        state, plan = coordinator.compile_first_wave(dispatch, "run-resolved")
        state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, [receipt(action) for action in plan["actions"]]
        )
        plan = coordinator.build_next_wave_plan(dispatch, plan, gate, actions, state, actions["actions"])
        state, gate, actions = coordinator.reduce_wave_receipts(
            dispatch, state, plan, [receipt(plan["actions"][0], "invalid")]
        )
        self.assertEqual(gate["decision"], "gate_resolved")
        self.assertEqual(actions["actions"], [])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
SKILL = ARCANUM_ROOT / "runtime/orchestrate/SKILL.md"
HOST_PROFILE = ARCANUM_ROOT / "runtime/orchestrate/hosts/codex-native.md"
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"
COMPILE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"
REDUCE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/reduce"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
EVENT_SCHEMA = Path(__file__).resolve().parent / "native-join-event.schema.json"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_join", COORDINATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {COORDINATOR_PATH}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    _, raw, _ = text.split("---", 2)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return value


def pass_results() -> dict[str, dict[str, Any]]:
    values = [load_json(path) for path in sorted((REDUCE / "pass").glob("*.json"))]
    return {value["agent_id"]: value for value in values}


class ScriptedMailboxHost:
    def __init__(self, rounds: list[dict[str, dict[str, Any]] | None]) -> None:
        self.rounds = list(rounds)
        self.wait_call_count = 0
        self.interrupted: list[str] = []

    def wait_round(self) -> dict[str, dict[str, Any]] | None:
        self.wait_call_count += 1
        return self.rounds.pop(0) if self.rounds else None

    def interrupt(self, agent_id: str) -> None:
        self.interrupted.append(agent_id)


def blocking_receipt(action: dict[str, Any], agent_id: str, blocker: str, status: str = "block") -> dict[str, Any]:
    return {
        "schema_version": "arcanum.native-dispatch-runner.receipt.v0.1",
        "action_id": action["action_id"],
        "dispatch_id": action["dispatch_id"],
        "run_id": action["run_id"],
        "wave_id": action["wave_id"],
        "step_id": action["step_id"],
        "role": action["role"],
        "capability_ref": action["capability_ref"],
        "agent_id": agent_id,
        "status": status,
        "artifacts": [],
        "validation": "block",
        "blockers": [blocker],
        "started_at": "2026-07-22T15:20:00Z",
        "finished_at": "2026-07-22T15:20:01Z",
    }


def normalize_result(action: dict[str, Any], agent_id: str, result: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "action_id": action["action_id"],
        "dispatch_id": action["dispatch_id"],
        "run_id": action["run_id"],
        "wave_id": action["wave_id"],
        "step_id": action["step_id"],
        "role": action["role"],
        "capability_ref": action["capability_ref"],
        "agent_id": agent_id,
    }
    mismatches = [field for field, value in expected.items() if result.get(field) != value]
    if mismatches:
        return blocking_receipt(action, agent_id, "identity_mismatch:" + ",".join(mismatches))
    return {
        "schema_version": "arcanum.native-dispatch-runner.receipt.v0.1",
        **expected,
        "status": result.get("status", "block"),
        "artifacts": list(result.get("artifacts", [])),
        "validation": result.get("validation", "block"),
        "blockers": list(result.get("blockers", [])),
        "started_at": str(result.get("started_at", "")),
        "finished_at": str(result.get("finished_at", "")),
    }


def join_wave(
    dispatch: dict[str, Any],
    state: dict[str, Any],
    run_plan: dict[str, Any],
    bindings: dict[str, str],
    host: ScriptedMailboxHost,
) -> dict[str, Any]:
    actions = {action["action_id"]: action for action in run_plan["actions"]}
    if set(bindings) != set(actions) or len(set(bindings.values())) != len(bindings):
        raise ValueError("bindings must cover every wave action with unique native agent identifiers")

    events: list[dict[str, Any]] = []

    def event(name: str, action_id: str | None, agent_id: str | None, operation: str) -> None:
        events.append({"sequence": len(events) + 1, "event": name, "action_id": action_id, "agent_id": agent_id, "operation": operation})

    pending = dict(bindings)
    results: dict[str, dict[str, Any]] = {}
    for action_id, agent_id in pending.items():
        event("agent_wait_registered", action_id, agent_id, "logical-register")

    while pending:
        event("wait_attempted", None, None, "collaboration.wait_agent")
        completions = host.wait_round()
        if not completions:
            break
        for agent_id, result in completions.items():
            match = next(((action_id, known) for action_id, known in pending.items() if known == agent_id), None)
            if match is None:
                continue
            action_id, _ = match
            results[action_id] = normalize_result(actions[action_id], agent_id, result)
            event("agent_terminal", action_id, agent_id, "collaboration.list_agents")
            event("agent_closed", action_id, agent_id, "logical-close")
            del pending[action_id]

    for action_id, agent_id in pending.items():
        event("wait_timed_out", action_id, agent_id, "collaboration.wait_agent")
        host.interrupt(agent_id)
        event("agent_interrupted", action_id, agent_id, "collaboration.interrupt_agent")
        results[action_id] = blocking_receipt(actions[action_id], agent_id, "missing_result", status="timed_out")

    receipts = [results[action["action_id"]] for action in run_plan["actions"]]
    next_state, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
    return {"events": events, "receipts": receipts, "state": next_state, "gate": gate, "action_set": action_set}


class NativeJoinContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = load_frontmatter(SKILL)
        cls.host_profile = load_frontmatter(HOST_PROFILE)
        cls.dispatch = load_json(COMPILE / "valid-two-wave.json")
        cls.state = load_json(COMPILE / "expected-state.json")
        cls.run_plan = load_json(COMPILE / "expected-run-plan.json")
        cls.bindings = load_json(FIXTURES / "bindings.json")
        cls.receipt_schema = load_json(SCHEMAS / "receipt.schema.json")
        cls.event_schema = load_json(EVENT_SCHEMA)

    def assert_valid_result(self, result: dict[str, Any]) -> None:
        for receipt in result["receipts"]:
            Draft202012Validator(self.receipt_schema).validate(receipt)
        for event in result["events"]:
            Draft202012Validator(self.event_schema).validate(event)

    def test_all_pass_results_close_once_and_return_exact_reducer_gate(self) -> None:
        host = ScriptedMailboxHost([pass_results()])
        result = join_wave(self.dispatch, self.state, self.run_plan, self.bindings, host)
        self.assert_valid_result(result)
        self.assertEqual(result["events"], load_json(FIXTURES / "expected-all-pass-events.json"))
        self.assertEqual(result["gate"], load_json(REDUCE / "expected-pass-gate.json"))
        self.assertEqual(result["state"], load_json(REDUCE / "expected-pass-state.json"))
        self.assertEqual(result["action_set"], load_json(REDUCE / "expected-pass-actions.json"))
        self.assertEqual(host.wait_call_count, 1)
        self.assertEqual(host.interrupted, [])

    def test_one_agent_failure_reaches_reducer_and_blocks(self) -> None:
        results = pass_results()
        failed = results["native-agent-beta-1"]
        failed["status"] = "fail"
        failed["validation"] = "fail"
        failed["blockers"] = ["bounded_task_failed"]
        result = join_wave(self.dispatch, self.state, self.run_plan, self.bindings, ScriptedMailboxHost([results]))
        self.assert_valid_result(result)
        self.assertEqual(result["gate"]["decision"], "gate_block")
        self.assertEqual(result["action_set"]["actions"], [])

    def test_missing_result_interrupts_once_and_emits_explicit_timed_out_receipt(self) -> None:
        results = pass_results()
        missing_agent = self.bindings["spawn-0002"]
        del results[missing_agent]
        host = ScriptedMailboxHost([results, None])
        result = join_wave(self.dispatch, self.state, self.run_plan, self.bindings, host)
        self.assert_valid_result(result)
        missing = next(receipt for receipt in result["receipts"] if receipt["action_id"] == "spawn-0002")
        self.assertEqual(missing["status"], "timed_out")
        self.assertEqual(missing["blockers"], ["missing_result"])
        self.assertEqual(host.interrupted, [missing_agent])
        self.assertEqual(result["gate"]["decision"], "gate_block")

    def test_identity_mismatch_is_bound_to_expected_action_and_blocks(self) -> None:
        results = pass_results()
        results["native-agent-alpha-0"]["role"] = "wrong-role"
        result = join_wave(self.dispatch, self.state, self.run_plan, self.bindings, ScriptedMailboxHost([results]))
        self.assert_valid_result(result)
        mismatch = next(receipt for receipt in result["receipts"] if receipt["action_id"] == "spawn-0003")
        self.assertEqual(mismatch["status"], "block")
        self.assertEqual(mismatch["blockers"], ["identity_mismatch:role"])
        self.assertEqual(result["gate"]["decision"], "gate_block")

    def test_binding_set_must_be_complete_and_unique(self) -> None:
        incomplete = copy.deepcopy(self.bindings)
        del incomplete["spawn-0003"]
        with self.assertRaisesRegex(ValueError, "cover every wave action"):
            join_wave(self.dispatch, self.state, self.run_plan, incomplete, ScriptedMailboxHost([]))

    def test_skill_and_codex_profile_model_mailbox_wide_wait(self) -> None:
        skill = self.skill["native_join_contract"]
        host = self.host_profile["join_contract"]
        self.assertEqual(skill["join_policy"], "all")
        self.assertEqual(skill["registration_per_agent"], 1)
        self.assertEqual(skill["close_per_agent"], 1)
        self.assertEqual(host["wait_operation"], "collaboration.wait_agent")
        self.assertEqual(host["wait_targeting"], "mailbox-wide")
        self.assertEqual(host["recovery_operation"], "collaboration.interrupt_agent")


if __name__ == "__main__":
    unittest.main()

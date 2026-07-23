#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml
from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
SKILL = ARCANUM_ROOT / "runtime/orchestrate/SKILL.md"
HOST = ARCANUM_ROOT / "runtime/orchestrate/hosts/codex-native.md"
ACTION_SCHEMA = ARCANUM_ROOT / "runtime/orchestrate/schemas/action.schema.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
RECEIPT_SCHEMA = Path(__file__).resolve().parent / "native-spawn-receipt.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    _, raw, _ = text.split("---", 2)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return value


def compact_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def build_spawn_request(action: dict[str, Any], host: dict[str, Any]) -> dict[str, Any]:
    task_stem = re.sub(r"[^a-z0-9]+", "_", action["role"].lower()).strip("_")
    action_stem = action["action_id"].replace("-", "_")
    lines = [
        "Execute one bounded host-native proof action.",
        f"Action: {action['action_id']}",
        f"Role: {action['role']}",
        f"Capability: {action['capability_ref']}",
        f"Target: {action['target']}",
        f"Mode: {action['mode']}",
        f"Mutation policy: {action['mutation_policy']}",
        f"Write scope: {compact_list(action['write_scope'])}",
        f"Forbidden write scopes: {compact_list(action['forbidden_write_scopes'])}",
        f"Input refs: {compact_list(action['input_refs'])}",
        f"Output refs: {compact_list(action['output_refs'])}",
        "Do not edit or create files. Do not spawn child agents. Read the target and return one compact acknowledgement containing action_id, status, and validation.",
    ]
    return {
        "action_id": action["action_id"],
        "operation": host["spawn_contract"]["operation"],
        "task_name": f"{task_stem}_{action_stem}",
        "fork_turns": host["spawn_contract"]["fork_turns"],
        "message": "\n".join(lines),
    }


class NativeSpawnAdmission:
    def __init__(self, persisted_actions: dict[str, dict[str, Any]]) -> None:
        self.persisted_actions = persisted_actions
        self.attempted: set[str] = set()
        self.events: list[dict[str, Any]] = []

    def execute(self, action_id: str, host_call: Callable[[dict[str, Any]], str], host: dict[str, Any]) -> dict[str, Any]:
        base = {
            "schema_version": "arcanum.native-dispatch-runner.native-spawn-receipt.v0.1",
            "dispatch_id": "fixture-native-spawn-one",
            "run_id": "swu-ndr-004-native",
            "action_id": action_id,
            "operation": host["spawn_contract"]["operation"],
        }
        if action_id not in self.persisted_actions:
            return {**base, "status": "block", "host_call_count": 0, "agent_id": None, "blockers": ["unknown_action"]}
        if action_id in self.attempted:
            return {**base, "status": "block", "host_call_count": 0, "agent_id": None, "blockers": ["action_replay"]}

        action = self.persisted_actions[action_id]
        self.attempted.add(action_id)
        self.events.append({"event": "action_attempted", "action_id": action_id})
        try:
            agent_id = host_call(build_spawn_request(action, host))
            if not agent_id:
                raise RuntimeError("host_returned_no_agent_id")
        except Exception as error:  # host boundary intentionally normalizes failures
            self.events.append({"event": "host_spawn_failed", "action_id": action_id})
            return {**base, "status": "block", "host_call_count": 1, "agent_id": None, "blockers": [str(error)]}

        self.events.append({"event": "host_spawn_returned", "action_id": action_id, "agent_id": agent_id})
        return {**base, "status": "spawned", "host_call_count": 1, "agent_id": agent_id, "blockers": []}


class NativeSpawnContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = load_frontmatter(SKILL)
        cls.host = load_frontmatter(HOST)
        cls.action = load_json(FIXTURES / "action.json")
        cls.receipt_schema = load_json(RECEIPT_SCHEMA)
        Draft202012Validator(load_json(ACTION_SCHEMA)).validate(cls.action)

    def make_admission(self) -> NativeSpawnAdmission:
        return NativeSpawnAdmission({self.action["action_id"]: self.action})

    def test_one_persisted_action_maps_to_exact_bounded_request_and_one_call(self) -> None:
        calls: list[dict[str, Any]] = []

        def host_call(request: dict[str, Any]) -> str:
            calls.append(request)
            return "agent-native-proof-001"

        admission = self.make_admission()
        receipt = admission.execute("spawn-0001", host_call, self.host)
        Draft202012Validator(self.receipt_schema).validate(receipt)
        self.assertEqual(calls, [load_json(FIXTURES / "expected-spawn-request.json")])
        self.assertEqual(receipt["agent_id"], "agent-native-proof-001")
        self.assertEqual([event["event"] for event in admission.events], ["action_attempted", "host_spawn_returned"])

    def test_unknown_action_blocks_before_host_call(self) -> None:
        calls = 0

        def host_call(_: dict[str, Any]) -> str:
            nonlocal calls
            calls += 1
            return "should-not-exist"

        receipt = self.make_admission().execute("spawn-9999", host_call, self.host)
        Draft202012Validator(self.receipt_schema).validate(receipt)
        self.assertEqual(calls, 0)
        self.assertEqual(receipt["blockers"], ["unknown_action"])

    def test_duplicate_or_replay_blocks_before_second_host_call(self) -> None:
        calls = 0

        def host_call(_: dict[str, Any]) -> str:
            nonlocal calls
            calls += 1
            return "agent-native-proof-001"

        admission = self.make_admission()
        first = admission.execute("spawn-0001", host_call, self.host)
        second = admission.execute("spawn-0001", host_call, self.host)
        Draft202012Validator(self.receipt_schema).validate(first)
        Draft202012Validator(self.receipt_schema).validate(second)
        self.assertEqual(calls, 1)
        self.assertEqual(second["blockers"], ["action_replay"])

    def test_host_error_records_attempt_and_blocks_without_retry(self) -> None:
        calls = 0

        def host_call(_: dict[str, Any]) -> str:
            nonlocal calls
            calls += 1
            raise RuntimeError("native_host_error")

        admission = self.make_admission()
        receipt = admission.execute("spawn-0001", host_call, self.host)
        Draft202012Validator(self.receipt_schema).validate(receipt)
        self.assertEqual(calls, 1)
        self.assertEqual(receipt["status"], "block")
        self.assertEqual(receipt["blockers"], ["native_host_error"])
        self.assertEqual([event["event"] for event in admission.events], ["action_attempted", "host_spawn_failed"])

    def test_skill_and_host_contracts_are_consistent(self) -> None:
        skill = self.skill["native_spawn_contract"]
        host = self.host["spawn_contract"]
        self.assertEqual(skill["action"], "spawn")
        self.assertTrue(skill["persisted_action_required"])
        self.assertEqual(skill["calls_per_action"], 1)
        self.assertEqual(host["calls_per_action"], 1)
        self.assertEqual(skill["pre_event"], host["pre_event"])
        self.assertEqual(skill["success_event"], host["success_event"])
        self.assertEqual(skill["failure_event"], host["failure_event"])
        self.assertEqual(host["operation"], "collaboration.spawn_agent")
        self.assertEqual(host["fork_turns"], "none")


if __name__ == "__main__":
    unittest.main()

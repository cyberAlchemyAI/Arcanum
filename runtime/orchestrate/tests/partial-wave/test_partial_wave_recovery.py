#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
RUN_PLAN = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile/expected-run-plan.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
RESULT_SCHEMA = Path(__file__).resolve().parent / "partial-wave-result.schema.json"
SKILL = ARCANUM_ROOT / "runtime/orchestrate/SKILL.md"
HOST_PROFILE = ARCANUM_ROOT / "runtime/orchestrate/hosts/codex-native.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> dict[str, Any]:
    _, raw, _ = path.read_text(encoding="utf-8").split("---", 2)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return value


class PartialWaveHost:
    def __init__(self, completed_during_cleanup: bool = False) -> None:
        self.completed_during_cleanup = completed_during_cleanup
        self.host_calls: list[dict[str, Any]] = []
        self.spawn_count = 0

    def spawn(self, action_id: str) -> str:
        self.spawn_count += 1
        self.host_calls.append({"operation": "collaboration.spawn_agent", "action_id": action_id})
        if self.spawn_count == 1:
            return "native-agent-partial-001"
        raise RuntimeError("native_spawn_failure")

    def wait(self) -> dict[str, str] | None:
        self.host_calls.append({"operation": "collaboration.wait_agent", "action_id": None})
        if self.completed_during_cleanup:
            return {"native-agent-partial-001": "completed"}
        return None

    def interrupt(self, agent_id: str) -> None:
        self.host_calls.append({"operation": "collaboration.interrupt_agent", "agent_id": agent_id})


def recover_partial_wave(actions: list[dict[str, Any]], host: PartialWaveHost) -> dict[str, Any]:
    events: list[dict[str, Any]] = []

    def event(name: str, action_id: str | None, agent_id: str | None, operation: str) -> None:
        events.append({"sequence": len(events) + 1, "event": name, "action_id": action_id, "agent_id": agent_id, "operation": operation})

    known: list[dict[str, str]] = []
    failed_action_id: str | None = None
    attempted: list[str] = []
    for action in actions:
        action_id = action["action_id"]
        attempted.append(action_id)
        event("action_attempted", action_id, None, "collaboration.spawn_agent")
        try:
            agent_id = host.spawn(action_id)
        except RuntimeError:
            failed_action_id = action_id
            event("host_spawn_failed", action_id, None, "collaboration.spawn_agent")
            break
        known.append({"action_id": action_id, "agent_id": agent_id, "terminal_state": "pending"})
        event("host_spawn_returned", action_id, agent_id, "collaboration.spawn_agent")

    if failed_action_id is None:
        raise AssertionError("fixture did not produce a partial-wave failure")

    for item in known:
        event("agent_wait_registered", item["action_id"], item["agent_id"], "logical-register")
    completions = None
    if known:
        event("wait_attempted", None, None, "collaboration.wait_agent")
        completions = host.wait()
    for item in known:
        if completions and completions.get(item["agent_id"]) == "completed":
            item["terminal_state"] = "completed"
            event("agent_terminal", item["action_id"], item["agent_id"], "collaboration.list_agents")
            event("agent_closed", item["action_id"], item["agent_id"], "logical-close")
        else:
            event("wait_timed_out", item["action_id"], item["agent_id"], "collaboration.wait_agent")
            host.interrupt(item["agent_id"])
            item["terminal_state"] = "interrupted"
            event("agent_interrupted", item["action_id"], item["agent_id"], "collaboration.interrupt_agent")

    event("run_blocked", failed_action_id, None, "logical-close")
    unattempted = [action["action_id"] for action in actions if action["action_id"] not in attempted]
    residue = [
        {"action_id": item["action_id"], "agent_id": item["agent_id"], "terminal_state": item["terminal_state"]}
        for item in known
    ]
    return {
        "status": "block",
        "state": "blocked",
        "spawn_attempt_count": host.spawn_count,
        "spawned_action_ids": [item["action_id"] for item in known],
        "failed_action_id": failed_action_id,
        "unattempted_action_ids": unattempted,
        "known_agents": known,
        "dependent_action_ids": [],
        "dependent_actions": [],
        "blockers": [f"partial_wave_spawn_failure:{failed_action_id}"],
        "residue": residue,
        "events": events,
        "host_calls": host.host_calls,
    }


class PartialWaveRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.actions = load_json(RUN_PLAN)["actions"]
        cls.schema = load_json(RESULT_SCHEMA)

    def test_unresolved_sibling_is_interrupted_and_third_action_never_spawns(self) -> None:
        host = PartialWaveHost()
        result = recover_partial_wave(self.actions, host)
        Draft202012Validator(self.schema).validate(result)
        self.assertEqual(result["events"], load_json(FIXTURES / "expected-unresolved-trace.json"))
        self.assertEqual(result["spawn_attempt_count"], 2)
        self.assertEqual(result["spawned_action_ids"], ["spawn-0001"])
        self.assertEqual(result["failed_action_id"], "spawn-0002")
        self.assertEqual(result["unattempted_action_ids"], ["spawn-0003"])
        self.assertEqual(result["known_agents"][0]["terminal_state"], "interrupted")
        self.assertEqual([call["operation"] for call in host.host_calls], ["collaboration.spawn_agent", "collaboration.spawn_agent", "collaboration.wait_agent", "collaboration.interrupt_agent"])
        self.assertEqual(result["dependent_action_ids"], [])
        self.assertEqual(result["dependent_actions"], [])

    def test_completed_sibling_is_closed_without_interrupt_but_run_stays_blocked(self) -> None:
        host = PartialWaveHost(completed_during_cleanup=True)
        result = recover_partial_wave(self.actions, host)
        Draft202012Validator(self.schema).validate(result)
        self.assertEqual(result["known_agents"][0]["terminal_state"], "completed")
        self.assertNotIn("collaboration.interrupt_agent", [call["operation"] for call in host.host_calls])
        self.assertEqual(result["status"], "block")
        self.assertEqual(result["dependent_actions"], [])

    def test_existing_contracts_supply_all_recovery_operations(self) -> None:
        skill = load_frontmatter(SKILL)
        host = load_frontmatter(HOST_PROFILE)
        self.assertEqual(skill["native_spawn_contract"]["failure_event"], "host_spawn_failed")
        self.assertEqual(skill["native_join_contract"]["recovery_operation_from_host_profile"], "interrupt")
        self.assertEqual(host["native_operation_map"]["spawn"], "collaboration.spawn_agent")
        self.assertEqual(host["native_operation_map"]["wait"], "collaboration.wait_agent")
        self.assertEqual(host["native_operation_map"]["interrupt"], "collaboration.interrupt_agent")
        self.assertEqual(host["join_contract"]["interrupt_per_unresolved_agent"], 1)


if __name__ == "__main__":
    unittest.main()

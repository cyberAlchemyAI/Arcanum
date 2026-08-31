#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
DRIVER_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_driver.py"
VALIDATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/validate_run_evidence.py"
COMPILE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"
REDUCE = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/reduce"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


driver = load_module("native_dispatch_driver_test", DRIVER_PATH)
validator = load_module("validate_run_evidence_driver_test", VALIDATOR_PATH)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class NativeDispatchDriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dispatch_path = COMPILE / "valid-two-wave.json"
        cls.state_path = COMPILE / "expected-state.json"
        cls.run_plan_path = COMPILE / "expected-run-plan.json"
        cls.run_plan = load_json(cls.run_plan_path)
        cls.admission_schema = load_json(SCHEMAS / "receipt-admission.schema.yml")
        cls.event_schema = load_json(SCHEMAS / "run-event.schema.json")
        cls.residue_schema = load_json(SCHEMAS / "run-residue.schema.yml")
        cls.partial_closeout_schema = load_json(
            SCHEMAS / "partial-wave-closeout.schema.json"
        )
        cls.action_schema = load_json(SCHEMAS / "action.schema.json")
        cls.run_plan_schema = load_json(SCHEMAS / "run-plan.schema.json")

    def persist_actions(self, root: Path) -> dict[str, Path]:
        paths: dict[str, Path] = {}
        for action in self.run_plan["actions"]:
            path = root / "actions" / f"{action['action_id']}.json"
            write_json(path, action)
            paths[action["action_id"]] = path
        return paths

    def native_agent_id(self, action: dict[str, Any]) -> str:
        return "/root/" + driver._spawn_request(action)["task_name"]

    def fixture_receipts(self) -> dict[str, dict[str, Any]]:
        receipts = {
            value["action_id"]: value
            for value in (
                load_json(path) for path in sorted((REDUCE / "pass").glob("*.json"))
            )
        }
        actions = {
            action["action_id"]: action for action in self.run_plan["actions"]
        }
        for action_id, receipt in receipts.items():
            receipt["agent_id"] = self.native_agent_id(actions[action_id])
        return receipts

    def copy_receipts(self, root: Path) -> Path:
        receipts_dir = root / "receipts"
        for action_id, receipt in self.fixture_receipts().items():
            write_json(receipts_dir / f"{action_id}.json", receipt)
        return receipts_dir

    def build_misbound_wait_stream(
        self, root: Path
    ) -> tuple[dict[str, Any], Path, Path, Path, str, str]:
        action = self.run_plan["actions"][0]
        action_path = self.persist_actions(root)[action["action_id"]]
        request_path = root / "requests" / f"{action['action_id']}.json"
        write_json(request_path, driver._spawn_request(action))
        task_name = load_json(request_path)["task_name"]
        prior_agent_id = "/root/" + task_name.replace("_spawn_0001", "_spawn-0001")
        corrected_agent_id = "/root/" + task_name
        records = [
            {
                "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                "sequence": 1,
                "event": "action_attempted",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": None,
                "operation": "collaboration.spawn_agent",
                "depends_on_gate_id": None,
            },
            {
                "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                "sequence": 2,
                "event": "host_spawn_returned",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": prior_agent_id,
                "operation": "collaboration.spawn_agent",
            },
            {
                "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                "sequence": 3,
                "event": "agent_wait_registered",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": prior_agent_id,
                "operation": "logical-register",
            },
            {
                "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                "sequence": 4,
                "event": "wait_attempted",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": None,
                "agent_id": None,
                "operation": "collaboration.wait_agent",
            },
        ]
        events = root / "events.jsonl"
        events.write_text(
            "".join(
                json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
        return (
            action,
            action_path,
            request_path,
            events,
            prior_agent_id,
            corrected_agent_id,
        )

    def write_raw_results(self, root: Path) -> Path:
        raw_results = root / "raw-results"
        for action in self.run_plan["actions"]:
            briefing = action["briefing_binding"]["briefing"]
            status = briefing["status_semantics"]
            value: dict[str, Any] = {}
            for field in briefing["receipt_shape"]["required_fields"]:
                value[field] = [] if field in {"findings", "artifacts"} else "pass"
            value[status["task_status_field"]] = status["task_complete_value"]
            value[status["domain_gate_status_field"]] = "pass"
            write_json(raw_results / f"{action['action_id']}.json", value)
        return raw_results

    def build_pre_join_stream(self, root: Path) -> Path:
        events = root / "events.jsonl"
        action_paths = self.persist_actions(root)
        receipts = self.fixture_receipts()
        for action in self.run_plan["actions"]:
            action_id = action["action_id"]
            driver.prepare_spawn(
                action_paths[action_id],
                self.run_plan_path,
                events,
                root / "requests" / f"{action_id}.json",
                None,
            )
            driver.record_spawn(
                action_paths[action_id],
                self.run_plan_path,
                root / "requests" / f"{action_id}.json",
                events,
                receipts[action_id]["agent_id"],
            )
        driver.prepare_wait(
            self.run_plan_path, events, root / "requests" / "wait.json"
        )
        terminal_records: list[dict[str, Any]] = []
        for action in self.run_plan["actions"]:
            receipt = receipts[action["action_id"]]
            base = {
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": receipt["agent_id"],
            }
            terminal_records.extend(
                [
                    {
                        **base,
                        "event": "agent_terminal",
                        "operation": "collaboration.list_agents",
                    },
                    {
                        **base,
                        "event": "agent_closed",
                        "operation": "logical-close",
                    },
                ]
            )
        driver.append_causal_records(events, terminal_records)
        return events

    def advance_first_wave(
        self, root: Path
    ) -> tuple[Path, Path, dict[str, Any]]:
        events = self.build_pre_join_stream(root)
        output = root / "advance"
        result = driver.advance_wave(
            self.dispatch_path,
            self.state_path,
            self.run_plan_path,
            self.copy_receipts(root),
            self.write_raw_results(root),
            events,
            output,
        )
        return events, output, result

    def build_partial_stream(
        self, root: Path, *, failure_action_id: str = "spawn-0003"
    ) -> tuple[Path, dict[str, Path], dict[str, dict[str, Any]]]:
        events = root / "events.jsonl"
        action_paths = self.persist_actions(root)
        receipts = self.fixture_receipts()
        for action in self.run_plan["actions"]:
            action_id = action["action_id"]
            driver.prepare_spawn(
                action_paths[action_id],
                self.run_plan_path,
                events,
                root / "requests" / f"{action_id}.json",
                None,
            )
            if action_id == failure_action_id:
                driver.record_spawn(
                    action_paths[action_id],
                    self.run_plan_path,
                    root / "requests" / f"{action_id}.json",
                    events,
                    None,
                )
                break
            driver.record_spawn(
                action_paths[action_id],
                self.run_plan_path,
                root / "requests" / f"{action_id}.json",
                events,
                receipts[action_id]["agent_id"],
            )
        return events, action_paths, receipts

    def append_partial_cleanup_residue(
        self, root: Path, action: dict[str, Any], agent_id: str
    ) -> None:
        driver.append_residue_record(
            root / "residue.jsonl",
            {
                "recorded_at": "2026-08-10T00:00:00Z",
                "kind": "evidence_closure",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": agent_id,
                "summary": "Known partial-wave sibling completed; its raw return remains unjoined evidence.",
                "source_refs": ["events.jsonl"],
            },
        )

    def test_windows_lockfile_fallback_is_exclusive_and_cleans_up(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stream = Path(temp_dir) / "events.jsonl"
            original_fcntl = driver.fcntl
            driver.fcntl = None
            try:
                with stream.open("a+", encoding="utf-8") as handle:
                    lock_path = Path(f"{handle.name}.lock")
                    with driver._exclusive_stream_lock(handle):
                        self.assertTrue(lock_path.is_file())
                        with stream.open("a+", encoding="utf-8") as contender:
                            with self.assertRaises(driver.DriverBlocked):
                                with driver._exclusive_stream_lock(contender):
                                    self.fail("a second Windows lock must not be admitted")
                    self.assertFalse(lock_path.exists())
            finally:
                driver.fcntl = original_fcntl

    def test_windows_lockfile_fallback_supports_causal_append(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            action_path = self.persist_actions(root)["spawn-0001"]
            events = root / "events.jsonl"
            original_fcntl = driver.fcntl
            driver.fcntl = None
            try:
                driver.prepare_spawn(
                    action_path,
                    self.run_plan_path,
                    events,
                    root / "request.json",
                    None,
                )
            finally:
                driver.fcntl = original_fcntl
            self.assertEqual(
                [item["event"] for item in validator.load_events(events)],
                ["action_attempted"],
            )
            self.assertFalse(Path(f"{events}.lock").exists())

    def test_prepare_spawn_persists_pre_event_before_request_and_replay_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            action_path = self.persist_actions(root)["spawn-0001"]
            events = root / "events.jsonl"
            request = root / "request.json"
            driver.prepare_spawn(
                action_path, self.run_plan_path, events, request, None
            )
            self.assertTrue(request.is_file())
            persisted = validator.load_events(events)
            self.assertEqual([item["event"] for item in persisted], ["action_attempted"])
            Draft202012Validator(self.event_schema).validate(persisted[0])
            self.assertTrue(
                validator.validate_events(
                    persisted, str(events), require_complete=False
                )["valid"]
            )

            before = events.read_bytes()
            replay_output = root / "replay-request.json"
            with self.assertRaises(driver.DriverBlocked):
                driver.prepare_spawn(
                    action_path,
                    self.run_plan_path,
                    events,
                    replay_output,
                    None,
                )
            self.assertEqual(events.read_bytes(), before)
            self.assertFalse(replay_output.exists())

    def test_spawn_request_name_is_stable_within_and_distinct_across_runs(self) -> None:
        action = copy.deepcopy(self.run_plan["actions"][0])
        first = driver._spawn_request(action)
        self.assertEqual(first["message"], action["initial_prompt"])
        self.assertEqual(first, driver._spawn_request(action))
        other_run = copy.deepcopy(action)
        other_run["run_id"] = "run-fixture-002"
        second = driver._spawn_request(other_run)
        self.assertNotEqual(first["task_name"], second["task_name"])
        self.assertRegex(first["task_name"], r"^orchestrate_[0-9a-f]{64}_spawn_0001$")
        self.assertNotIn(action["run_id"], first["task_name"])
        self.assertNotIn(action["dispatch_id"], first["task_name"])
        self.assertNotIn(action["role"], first["task_name"])

    def test_record_spawn_rejects_nonverbatim_native_agent_id_without_append(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            action = self.run_plan["actions"][0]
            action_path = self.persist_actions(root)[action["action_id"]]
            events = root / "events.jsonl"
            request_path = root / "request.json"
            request = driver.prepare_spawn(
                action_path,
                self.run_plan_path,
                events,
                request_path,
                None,
            )
            before = events.read_bytes()
            wrong_agent_id = (
                "/root/" + request["task_name"].replace("_spawn_0001", "_spawn-0001")
            )
            with self.assertRaises(driver.DriverBlocked):
                driver.record_spawn(
                    action_path,
                    self.run_plan_path,
                    request_path,
                    events,
                    wrong_agent_id,
                )
            self.assertEqual(events.read_bytes(), before)

            corrected_agent_id = "/root/" + request["task_name"]
            event = driver.record_spawn(
                action_path,
                self.run_plan_path,
                request_path,
                events,
                corrected_agent_id,
            )
            self.assertEqual(event["agent_id"], corrected_agent_id)
            self.assertEqual(
                [item["event"] for item in validator.load_events(events)],
                ["action_attempted", "host_spawn_returned"],
            )

    def test_agent_binding_correction_preserves_history_and_updates_effective_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (
                action,
                action_path,
                request_path,
                events,
                prior_agent_id,
                corrected_agent_id,
            ) = self.build_misbound_wait_stream(root)
            historical_prefix = events.read_bytes()
            correction = driver.correct_agent_binding(
                action_path,
                self.run_plan_path,
                request_path,
                events,
                prior_agent_id,
                corrected_agent_id,
                [2, 3],
            )
            self.assertEqual(correction["event"], "agent_binding_corrected")
            self.assertEqual(correction["supersedes_sequences"], [2, 3])
            self.assertTrue(events.read_bytes().startswith(historical_prefix))

            base = {
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "wave_id": action["wave_id"],
                "action_id": action["action_id"],
                "agent_id": corrected_agent_id,
            }
            driver.append_causal_records(
                events,
                [
                    {
                        **base,
                        "event": "agent_terminal",
                        "operation": "collaboration.list_agents",
                    },
                    {
                        **base,
                        "event": "agent_closed",
                        "operation": "logical-close",
                    },
                    {
                        **base,
                        "event": "receipt_joined",
                        "operation": "orchestrate.receipt-admission",
                        "receipt_status": "pass",
                    },
                ],
            )
            receipt = validator.validate_events(
                validator.load_events(events),
                str(events),
                require_complete=True,
            )
            self.assertTrue(receipt["valid"], receipt["errors"])

            before_duplicate = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.correct_agent_binding(
                    action_path,
                    self.run_plan_path,
                    request_path,
                    events,
                    prior_agent_id,
                    corrected_agent_id,
                    [2, 3],
                )
            self.assertEqual(events.read_bytes(), before_duplicate)

    def test_agent_binding_correction_rejects_wrong_sequences_and_terminal_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (
                action,
                action_path,
                request_path,
                events,
                prior_agent_id,
                corrected_agent_id,
            ) = self.build_misbound_wait_stream(root)
            before = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.correct_agent_binding(
                    action_path,
                    self.run_plan_path,
                    request_path,
                    events,
                    prior_agent_id,
                    corrected_agent_id,
                    [2, 4],
                )
            self.assertEqual(events.read_bytes(), before)

            driver.append_causal_records(
                events,
                [
                    {
                        "event": "agent_terminal",
                        "dispatch_id": action["dispatch_id"],
                        "run_id": action["run_id"],
                        "wave_id": action["wave_id"],
                        "action_id": action["action_id"],
                        "agent_id": prior_agent_id,
                        "operation": "collaboration.list_agents",
                    }
                ],
            )
            before_terminal_correction = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.correct_agent_binding(
                    action_path,
                    self.run_plan_path,
                    request_path,
                    events,
                    prior_agent_id,
                    corrected_agent_id,
                    [2, 3],
                )
            self.assertEqual(events.read_bytes(), before_terminal_correction)

    def test_prepare_wait_registers_complete_wave_before_exposing_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            values = validator.load_events(events)
            wait_index = next(
                index for index, item in enumerate(values) if item["event"] == "wait_attempted"
            )
            registrations = [
                item for item in values[:wait_index] if item["event"] == "agent_wait_registered"
            ]
            self.assertEqual(len(registrations), 3)
            self.assertTrue((root / "requests" / "wait.json").is_file())
            self.assertTrue(
                validator.validate_events(
                    values, str(events), require_complete=False
                )["valid"]
            )

    def test_prepare_wait_reuses_registrations_and_appends_one_wait_per_call(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = root / "events.jsonl"
            action_paths = self.persist_actions(root)
            receipts = self.fixture_receipts()
            for action in self.run_plan["actions"]:
                action_id = action["action_id"]
                driver.prepare_spawn(
                    action_paths[action_id],
                    self.run_plan_path,
                    events,
                    root / "requests" / f"{action_id}.json",
                    None,
                )
                driver.record_spawn(
                    action_paths[action_id],
                    self.run_plan_path,
                    root / "requests" / f"{action_id}.json",
                    events,
                    receipts[action_id]["agent_id"],
                )

            first_path = root / "requests" / "wait-001.json"
            second_path = root / "requests" / "wait-002.json"
            first = driver.prepare_wait(self.run_plan_path, events, first_path)
            second = driver.prepare_wait(self.run_plan_path, events, second_path)
            self.assertEqual(first["pending_agent_ids"], second["pending_agent_ids"])
            values = validator.load_events(events)
            self.assertEqual(
                len([item for item in values if item["event"] == "agent_wait_registered"]),
                3,
            )
            self.assertEqual(
                len([item for item in values if item["event"] == "wait_attempted"]),
                2,
            )
            self.assertTrue(first_path.is_file())
            self.assertTrue(second_path.is_file())
            self.assertTrue(
                validator.validate_events(values, str(events), require_complete=False)["valid"]
            )

            before_replay = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.prepare_wait(self.run_plan_path, events, second_path)
            self.assertEqual(events.read_bytes(), before_replay)

    def test_partial_recovery_closes_completed_known_siblings_and_blocks_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events, action_paths, receipts = self.build_partial_stream(root)
            before_prepare_wait = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.prepare_wait(
                    self.run_plan_path, events, root / "requests" / "wait.json"
                )
            self.assertEqual(events.read_bytes(), before_prepare_wait)

            request = driver.prepare_partial_recovery(
                self.run_plan_path,
                events,
                root / "requests" / "partial-wait.json",
            )
            self.assertEqual(request["pending_agent_ids"], [
                receipts["spawn-0001"]["agent_id"],
                receipts["spawn-0002"]["agent_id"],
            ])
            for action_id in ("spawn-0001", "spawn-0002"):
                action = next(
                    item for item in self.run_plan["actions"] if item["action_id"] == action_id
                )
                driver.record_partial_terminal(
                    action_paths[action_id],
                    self.run_plan_path,
                    events,
                    receipts[action_id]["agent_id"],
                )
                self.append_partial_cleanup_residue(
                    root, action, receipts[action_id]["agent_id"]
                )

            state_before = self.state_path.read_bytes()
            closeout = driver.close_partial_wave(
                self.run_plan_path,
                self.state_path,
                events,
                root / "residue.jsonl",
                root / "partial-closeout.json",
            )
            Draft202012Validator(self.partial_closeout_schema).validate(closeout)
            self.assertEqual(self.state_path.read_bytes(), state_before)
            self.assertEqual(closeout["failed_action_ids"], ["spawn-0003"])
            self.assertEqual(closeout["dependent_action_ids"], [])
            causal = validator.load_events(events)
            self.assertEqual(causal[-1]["event"], "run_blocked")
            self.assertNotIn("receipt_joined", [item["event"] for item in causal])
            self.assertNotIn("gate_decided", [item["event"] for item in causal])
            validation = validator.validate_events(causal, str(events))
            self.assertTrue(validation["valid"], validation)

    def test_partial_recovery_interrupts_an_unresolved_sibling_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events, action_paths, receipts = self.build_partial_stream(root)
            driver.prepare_partial_recovery(
                self.run_plan_path,
                events,
                root / "requests" / "partial-wait.json",
            )
            interrupt = driver.prepare_partial_interrupt(
                action_paths["spawn-0001"],
                self.run_plan_path,
                events,
                receipts["spawn-0001"]["agent_id"],
                root / "requests" / "interrupt.json",
            )
            self.assertEqual(interrupt["operation"], "collaboration.interrupt_agent")
            driver.record_partial_interrupt(
                action_paths["spawn-0001"],
                self.run_plan_path,
                events,
                receipts["spawn-0001"]["agent_id"],
            )
            action_two = next(
                item for item in self.run_plan["actions"] if item["action_id"] == "spawn-0002"
            )
            driver.record_partial_terminal(
                action_paths["spawn-0002"],
                self.run_plan_path,
                events,
                receipts["spawn-0002"]["agent_id"],
            )
            for action_id in ("spawn-0001", "spawn-0002"):
                action = next(
                    item for item in self.run_plan["actions"] if item["action_id"] == action_id
                )
                self.append_partial_cleanup_residue(
                    root, action, receipts[action_id]["agent_id"]
                )
            closeout = driver.close_partial_wave(
                self.run_plan_path,
                self.state_path,
                events,
                root / "residue.jsonl",
                root / "partial-closeout.json",
            )
            self.assertEqual(closeout["status"], "block")
            self.assertTrue(
                validator.validate_events(validator.load_events(events), str(events))["valid"]
            )

    def test_partial_recovery_rejects_missing_cleanup_residue_without_mutating_events(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events, action_paths, receipts = self.build_partial_stream(root)
            driver.prepare_partial_recovery(
                self.run_plan_path,
                events,
                root / "requests" / "partial-wait.json",
            )
            for action_id in ("spawn-0001", "spawn-0002"):
                driver.record_partial_terminal(
                    action_paths[action_id],
                    self.run_plan_path,
                    events,
                    receipts[action_id]["agent_id"],
                )
            (root / "residue.jsonl").write_text("", encoding="utf-8")
            before = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.close_partial_wave(
                    self.run_plan_path,
                    self.state_path,
                    events,
                    root / "residue.jsonl",
                    root / "partial-closeout.json",
                )
            self.assertEqual(events.read_bytes(), before)
            self.assertFalse((root / "partial-closeout.json").exists())

    def test_partial_closeout_without_known_siblings_is_valid_and_no_later_spawn_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events, action_paths, _ = self.build_partial_stream(
                root, failure_action_id="spawn-0001"
            )
            before = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.prepare_spawn(
                    action_paths["spawn-0002"],
                    self.run_plan_path,
                    events,
                    root / "requests" / "spawn-0002-retry.json",
                    None,
                )
            self.assertEqual(events.read_bytes(), before)
            (root / "residue.jsonl").write_text("", encoding="utf-8")
            closeout = driver.close_partial_wave(
                self.run_plan_path,
                self.state_path,
                events,
                root / "residue.jsonl",
                root / "partial-closeout.json",
            )
            self.assertEqual(closeout["cleaned_action_ids"], [])
            self.assertEqual(closeout["unattempted_action_ids"], ["spawn-0002", "spawn-0003"])
            self.assertTrue(
                validator.validate_events(validator.load_events(events), str(events))["valid"]
            )

    def test_later_wave_spawn_failure_closes_without_rewriting_prior_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            advance = driver.advance_wave(
                self.dispatch_path,
                self.state_path,
                self.run_plan_path,
                self.copy_receipts(root),
                self.write_raw_results(root),
                events,
                root / "advance",
            )
            action = advance["action_set"]["actions"][0]
            action_path = root / "artifact" / "actions" / f"{action['action_id']}.json"
            write_json(action_path, action)
            dispatch = load_json(self.dispatch_path)
            wave = next(
                item
                for item in dispatch["subagent_strategy"]["execution_waves"]
                if item["wave_id"] == action["wave_id"]
            )
            run_plan = {
                "schema_version": "arcanum.native-dispatch-runner.run-plan.v0.1",
                "dispatch_id": action["dispatch_id"],
                "run_id": action["run_id"],
                "state": "wave_ready",
                "validation_status": "pass",
                "selected_wave": wave,
                "action_artifacts": [f"actions/{action['action_id']}.json"],
                "actions": [action],
            }
            run_plan_path = root / "artifact" / "run-plan.json"
            state_path = root / "artifact" / "state.json"
            write_json(run_plan_path, run_plan)
            write_json(state_path, advance["state"])
            driver.prepare_spawn(
                action_path,
                run_plan_path,
                events,
                root / "requests" / "spawn-0004.json",
                "g-checks",
            )
            driver.record_spawn(
                action_path,
                run_plan_path,
                root / "requests" / "spawn-0004.json",
                events,
                None,
            )
            (root / "residue.jsonl").write_text("", encoding="utf-8")

            closeout = driver.close_partial_wave(
                run_plan_path,
                state_path,
                events,
                root / "residue.jsonl",
                root / "partial-closeout.json",
            )
            self.assertEqual(closeout["failed_action_ids"], ["spawn-0004"])
            self.assertEqual(closeout["cleaned_action_ids"], [])
            causal = validator.load_events(events)
            self.assertEqual(causal[-1]["event"], "run_blocked")
            self.assertEqual(causal[-1]["wave_id"], "artifact")
            self.assertTrue(any(item["event"] == "gate_decided" for item in causal[:-1]))
            self.assertTrue(
                validator.validate_events(causal, str(events))["valid"]
            )

    def test_later_wave_block_does_not_excuse_missing_earlier_join(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            values = validator.load_events(events)
            first_join = next(
                index for index, item in enumerate(values) if item["event"] == "agent_terminal"
            )
            values = values[:first_join]
            values.extend(
                [
                    {
                        "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                        "sequence": len(values) + 1,
                        "event": "action_attempted",
                        "dispatch_id": self.run_plan["dispatch_id"],
                        "run_id": self.run_plan["run_id"],
                        "wave_id": "artifact",
                        "action_id": "spawn-0004",
                        "agent_id": None,
                        "operation": "collaboration.spawn_agent",
                        "depends_on_gate_id": None,
                    },
                    {
                        "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                        "sequence": len(values) + 2,
                        "event": "host_spawn_failed",
                        "dispatch_id": self.run_plan["dispatch_id"],
                        "run_id": self.run_plan["run_id"],
                        "wave_id": "artifact",
                        "action_id": "spawn-0004",
                        "agent_id": None,
                        "operation": "collaboration.spawn_agent",
                    },
                    {
                        "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
                        "sequence": len(values) + 3,
                        "event": "run_blocked",
                        "dispatch_id": self.run_plan["dispatch_id"],
                        "run_id": self.run_plan["run_id"],
                        "wave_id": "artifact",
                        "action_id": "spawn-0004",
                        "agent_id": None,
                        "operation": "logical-close",
                        "failed_action_ids": ["spawn-0004"],
                        "cleaned_action_ids": [],
                        "blocker_code": "partial_wave_spawn_failure",
                    },
                ]
            )
            receipt = validator.validate_events(values, "missing-earlier-join.jsonl")
            self.assertIn(
                "missing_joined_receipt",
                [item["code"] for item in receipt["errors"]],
            )

    def test_invalid_causal_append_is_byte_stable_and_full_empty_stream_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            before = events.read_bytes()
            with self.assertRaises(driver.DriverBlocked):
                driver.append_causal_records(
                    events,
                    [
                        {
                            "event": "post_hoc_claim",
                            "dispatch_id": "fixture-native-dispatch-two-wave",
                            "run_id": "run-fixture-001",
                            "wave_id": "checks",
                            "action_id": None,
                            "agent_id": None,
                            "operation": "manual-note",
                        }
                    ],
                )
            self.assertEqual(events.read_bytes(), before)
            empty = validator.validate_events([], "empty.jsonl")
            self.assertEqual(empty["status"], "block")
            self.assertEqual(empty["errors"][0]["code"], "empty_event_stream")

    def test_validator_matches_closed_schema_for_unknown_fields_and_unique_gate_arrays(self) -> None:
        event = validator.load_events(
            ARCANUM_ROOT
            / "runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl"
        )[0]
        event["narrative_extra"] = "not causal"
        receipt = validator.validate_events([event], "extra-field.jsonl")
        self.assertEqual(receipt["errors"][0]["code"], "event_schema_violation")

        gate = validator.load_events(
            ARCANUM_ROOT
            / "runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl"
        )[7]
        gate["required_action_ids"] = ["spawn-0001", "spawn-0001"]
        gate["admitted_receipt_action_ids"] = ["spawn-0001", "spawn-0001"]
        self.assertIn("unique", validator.event_shape_violation(gate) or "")

        gate_block_stream = validator.load_events(
            ARCANUM_ROOT
            / "runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl"
        )[:8]
        gate_block_stream[-1]["decision"] = "gate_block"
        duplicate = copy.deepcopy(gate_block_stream[-1])
        duplicate["sequence"] = 9
        duplicate_receipt = validator.validate_events(
            gate_block_stream + [duplicate], "duplicate-gate-block.jsonl"
        )
        self.assertIn(
            "duplicate_gate_decision",
            [item["code"] for item in duplicate_receipt["errors"]],
        )

    def test_exact_receipt_admission_rejects_extra_and_malformed_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            receipts = self.copy_receipts(root)
            write_json(receipts / "governance-sidecar.json", {"status": "pass"})
            _, admission = driver.admit_receipt_directory(self.run_plan, receipts)
            Draft202012Validator(self.admission_schema).validate(admission)
            self.assertEqual(admission["status"], "block")
            self.assertTrue(
                any("unexpected receipt entry" in item for item in admission["blockers"])
            )

            (receipts / "governance-sidecar.json").unlink()
            malformed_path = receipts / "spawn-0001.json"
            malformed = load_json(malformed_path)
            malformed["narrative_extra"] = "not admitted"
            write_json(malformed_path, malformed)
            _, malformed_admission = driver.admit_receipt_directory(
                self.run_plan, receipts
            )
            self.assertEqual(malformed_admission["status"], "block")
            self.assertTrue(
                any("unexpected field" in item for item in malformed_admission["blockers"])
            )

    def test_advance_appends_joins_and_gate_before_exposing_run_global_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            receipts = self.copy_receipts(root)
            output = root / "advance"
            result = driver.advance_wave(
                self.dispatch_path,
                self.state_path,
                self.run_plan_path,
                receipts,
                self.write_raw_results(root),
                events,
                output,
            )
            self.assertEqual(result["gate_decision"]["decision"], "gate_pass")
            self.assertEqual(
                [item["action_id"] for item in result["action_set"]["actions"]],
                ["spawn-0004"],
            )
            self.assertTrue((output / "actions" / "spawn-0004.json").is_file())
            admission = load_json(output / "receipt-admission.json")
            Draft202012Validator(self.admission_schema).validate(admission)
            self.assertEqual(admission["status"], "pass")
            validation = load_json(output / "event-validation.json")
            self.assertEqual(validation["status"], "pass")
            causal = validator.load_events(events)
            self.assertEqual(causal[-1]["event"], "gate_decided")
            self.assertEqual(
                [item["event"] for item in causal[-4:]],
                ["receipt_joined", "receipt_joined", "receipt_joined", "gate_decided"],
            )

    def test_prepare_next_wave_plan_cli_preserves_prefix_and_enables_exact_spawn(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events, advance, result = self.advance_first_wave(root)
            causal_before = events.read_bytes()
            next_plan_path = root / "next-run-plan.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(DRIVER_PATH),
                    "prepare-next-wave-plan",
                    str(self.dispatch_path),
                    "--prior-run-plan",
                    str(self.run_plan_path),
                    "--gate-decision",
                    str(advance / "gate-decision.json"),
                    "--next-actions",
                    str(advance / "next-actions.json"),
                    "--next-state",
                    str(advance / "state.json"),
                    "--events",
                    str(events),
                    "--actions-dir",
                    str(advance / "actions"),
                    "--output",
                    str(next_plan_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            self.assertEqual(json.loads(completed.stdout)["wave_id"], "artifact")
            self.assertEqual(events.read_bytes(), causal_before)

            next_plan = load_json(next_plan_path)
            resolver = RefResolver.from_schema(
                self.run_plan_schema,
                store={
                    self.action_schema["$id"]: self.action_schema,
                    "action.schema.json": self.action_schema,
                },
            )
            Draft202012Validator(
                self.run_plan_schema, resolver=resolver
            ).validate(next_plan)
            self.assertEqual(next_plan["selected_wave"]["depends_on_waves"], ["checks"])
            self.assertEqual(next_plan["actions"], result["action_set"]["actions"])
            action_path = advance / "actions" / "spawn-0004.json"
            self.assertEqual(
                action_path.read_bytes(),
                driver._json_payload(next_plan["actions"][0]).encode("utf-8"),
            )

            before_missing_gate = events.read_bytes()
            with self.assertRaisesRegex(
                driver.DriverBlocked, "requires a non-empty passed gate"
            ):
                driver.prepare_spawn(
                    action_path,
                    next_plan_path,
                    events,
                    root / "requests" / "missing-gate.json",
                    None,
                )
            self.assertEqual(events.read_bytes(), before_missing_gate)
            self.assertFalse((root / "requests" / "missing-gate.json").exists())

            driver.prepare_spawn(
                action_path,
                next_plan_path,
                events,
                root / "requests" / "spawn-0004.json",
                "g-checks",
            )
            causal = validator.load_events(events)
            self.assertEqual(causal[-1]["event"], "action_attempted")
            self.assertEqual(causal[-1]["action_id"], "spawn-0004")
            self.assertEqual(causal[-1]["depends_on_gate_id"], "g-checks")
            self.assertTrue(
                validator.validate_events(
                    causal, str(events), require_complete=False
                )["valid"]
            )

    def test_prepare_next_wave_plan_rejects_bad_frontiers_before_mutation(self) -> None:
        cases = (
            "wrong_gate",
            "missing_action",
            "blocked_gate",
            "replayed_action",
            "terminal_block",
            "mismatched_state",
            "edited_action_bytes",
            "contaminated_actions",
            "duplicate_output",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                events, advance, result = self.advance_first_wave(root)
                gate_path = advance / "gate-decision.json"
                state_path = advance / "state.json"
                action_path = advance / "actions" / "spawn-0004.json"
                output_path = root / "next-run-plan.json"

                if case == "wrong_gate":
                    gate = copy.deepcopy(result["gate_decision"])
                    gate["gate_id"] = "g-wrong"
                    gate_path = root / "wrong-gate.json"
                    write_json(gate_path, gate)
                elif case == "missing_action":
                    action_path.unlink()
                elif case == "blocked_gate":
                    gate = copy.deepcopy(result["gate_decision"])
                    gate["decision"] = "gate_block"
                    gate["blockers"] = ["fixture block"]
                    gate_path = root / "blocked-gate.json"
                    write_json(gate_path, gate)
                elif case == "replayed_action":
                    action = result["action_set"]["actions"][0]
                    driver.append_causal_records(
                        events,
                        [
                            {
                                "event": "action_attempted",
                                "dispatch_id": action["dispatch_id"],
                                "run_id": action["run_id"],
                                "wave_id": action["wave_id"],
                                "action_id": action["action_id"],
                                "agent_id": None,
                                "operation": "collaboration.spawn_agent",
                                "depends_on_gate_id": "g-checks",
                            }
                        ],
                    )
                elif case == "terminal_block":
                    blocked_root = root / "blocked"
                    blocked_events, _, _ = self.build_partial_stream(
                        blocked_root, failure_action_id="spawn-0001"
                    )
                    (blocked_root / "residue.jsonl").write_text(
                        "", encoding="utf-8"
                    )
                    driver.close_partial_wave(
                        self.run_plan_path,
                        self.state_path,
                        blocked_events,
                        blocked_root / "residue.jsonl",
                        blocked_root / "partial-closeout.json",
                    )
                    events = blocked_events
                elif case == "mismatched_state":
                    state = copy.deepcopy(result["state"])
                    state["eligible_action_ids"] = ["spawn-9999"]
                    state_path = root / "mismatched-state.json"
                    write_json(state_path, state)
                elif case == "edited_action_bytes":
                    action_path.write_bytes(action_path.read_bytes() + b" ")
                elif case == "contaminated_actions":
                    write_json(advance / "actions" / "extra.json", {"extra": True})
                elif case == "duplicate_output":
                    output_path.write_text("sentinel\n", encoding="utf-8")

                causal_before = events.read_bytes()
                output_before = (
                    output_path.read_bytes() if output_path.exists() else None
                )
                with self.assertRaises(driver.DriverBlocked):
                    driver.prepare_next_wave_plan(
                        self.dispatch_path,
                        self.run_plan_path,
                        gate_path,
                        advance / "next-actions.json",
                        state_path,
                        events,
                        advance / "actions",
                        output_path,
                    )
                self.assertEqual(events.read_bytes(), causal_before)
                if output_before is None:
                    self.assertFalse(output_path.exists())
                else:
                    self.assertEqual(output_path.read_bytes(), output_before)

    def test_structural_nonpass_receipt_is_admitted_and_blocks_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            receipts = self.copy_receipts(root)
            failed_path = receipts / "spawn-0002.json"
            failed = load_json(failed_path)
            failed["status"] = "fail"
            failed["validation"] = "fail"
            failed["blockers"] = ["bounded_task_failed"]
            write_json(failed_path, failed)
            result = driver.advance_wave(
                self.dispatch_path,
                self.state_path,
                self.run_plan_path,
                receipts,
                self.write_raw_results(root),
                events,
                root / "advance",
            )
            self.assertEqual(result["receipt_admission"]["status"], "pass")
            self.assertEqual(result["gate_decision"]["decision"], "gate_block")
            self.assertEqual(result["action_set"]["actions"], [])
            self.assertEqual(result["event_validation"]["status"], "pass")

    def test_blocked_raw_task_cannot_normalize_as_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            receipts = self.copy_receipts(root)
            raw_results = self.write_raw_results(root)
            blocked = load_json(raw_results / "spawn-0002.json")
            blocked["task_status"] = "blocked"
            write_json(raw_results / "spawn-0002.json", blocked)
            output = root / "advance"
            with self.assertRaises(driver.DriverBlocked) as raised:
                driver.advance_wave(
                    self.dispatch_path,
                    self.state_path,
                    self.run_plan_path,
                    receipts,
                    raw_results,
                    events,
                    output,
                )
            self.assertIn("normalized status=block", str(raised.exception))
            validation = load_json(output / "task-result-validation.json")
            self.assertEqual(validation["status"], "block")
            self.assertFalse((output / "gate-decision.json").exists())
            self.assertNotIn(
                "receipt_joined",
                [event["event"] for event in validator.load_events(events)],
            )

    def test_v02_normalized_domain_value_must_match_raw_task_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dispatch = load_json(self.dispatch_path)
            strategy = dispatch["subagent_strategy"]
            strategy["execution_contract_version"] = driver.coordinator.STRICT_EXECUTION_CONTRACT
            strategy["execution_waves"][1]["gate_after"] = "g-artifact-domain"
            dispatch["gates"][0]["evaluation"] = {"mode": "receipt_status"}
            dispatch["gates"].append({
                "gate_id": "g-artifact-domain", "kind": "validation", "owner": "orchestrate",
                "condition": "Preserve a typed final outcome.", "applies_after_wave": "artifact",
                "requires_role_receipts": ["tmp/native-dispatch/receipts/artifact.json"],
                "evaluation": {
                    "mode": "domain_status", "source_role_id": "artifact-writer",
                    "source_field": "domain_gate_status", "pass_values": ["valid"],
                    "resolved_values": ["invalid"],
                },
                "on_fail": "block",
            })
            state, plan = driver.coordinator.compile_first_wave(dispatch, "run-v02-driver")
            dispatch_path = root / "dispatch.json"
            state_path = root / "state.json"
            plan_path = root / "plan.json"
            write_json(dispatch_path, dispatch)
            write_json(state_path, state)
            write_json(plan_path, plan)

            events = root / "events.jsonl"
            receipts_dir = root / "receipts"
            raw_dir = root / "raw-results"
            for action in plan["actions"]:
                action_path = root / "actions" / f"{action['action_id']}.json"
                request_path = root / "requests" / f"{action['action_id']}.json"
                write_json(action_path, action)
                driver.prepare_spawn(action_path, plan_path, events, request_path, None)
                agent_id = self.native_agent_id(action)
                driver.record_spawn(action_path, plan_path, request_path, events, agent_id)
            driver.prepare_wait(plan_path, events, root / "requests/wait.json")
            terminal_records = []
            for action in plan["actions"]:
                agent_id = self.native_agent_id(action)
                base = {
                    "dispatch_id": action["dispatch_id"], "run_id": action["run_id"],
                    "wave_id": action["wave_id"], "action_id": action["action_id"],
                    "agent_id": agent_id,
                }
                terminal_records.extend([
                    {**base, "event": "agent_terminal", "operation": "collaboration.list_agents"},
                    {**base, "event": "agent_closed", "operation": "logical-close"},
                ])
                receipt = {
                    "schema_version": driver.coordinator.RECEIPT_SCHEMA_VERSION_V2,
                    "action_id": action["action_id"], "dispatch_id": action["dispatch_id"],
                    "run_id": action["run_id"], "wave_id": action["wave_id"],
                    "step_id": action["step_id"], "role": action["role"],
                    "capability_ref": action["capability_ref"], "agent_id": agent_id,
                    "status": "pass", "artifacts": list(action["output_refs"]), "validation": "pass", "blockers": [],
                    "started_at": "2026-08-27T00:00:00Z", "finished_at": "2026-08-27T00:00:01Z",
                    "domain_gate": {"source_field": "domain_gate_status", "value": "normalized-value"},
                }
                write_json(receipts_dir / f"{action['action_id']}.json", receipt)
                briefing = action["briefing_binding"]["briefing"]
                semantics = briefing["status_semantics"]
                raw = {
                    field: ([] if field in {"findings", "artifacts"} else "pass")
                    for field in briefing["receipt_shape"]["required_fields"]
                }
                raw[semantics["task_status_field"]] = semantics["task_complete_value"]
                raw[semantics["domain_gate_status_field"]] = "raw-value"
                write_json(raw_dir / f"{action['action_id']}.json", raw)
            driver.append_causal_records(events, terminal_records)

            output = root / "advance"
            with self.assertRaises(driver.DriverBlocked) as raised:
                driver.advance_wave(dispatch_path, state_path, plan_path, receipts_dir, raw_dir, events, output)
            self.assertIn("normalized domain_gate does not match the raw result field and value", str(raised.exception))
            self.assertFalse((output / "gate-decision.json").exists())
            self.assertNotIn("receipt_joined", [event["event"] for event in validator.load_events(events)])

    def test_residue_is_separate_and_cannot_enter_causal_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events = self.build_pre_join_stream(root)
            causal_before = events.read_bytes()
            residue_path = root / "residue.jsonl"
            residue = driver.append_residue_record(
                residue_path,
                {
                    "recorded_at": "2026-08-10T00:00:00Z",
                    "kind": "governance",
                    "dispatch_id": "fixture-native-dispatch-two-wave",
                    "run_id": "run-fixture-001",
                    "wave_id": "checks",
                    "action_id": None,
                    "agent_id": None,
                    "summary": "Receipt staging note with no causal effect.",
                    "source_refs": ["receipt-admission.json"],
                },
            )
            Draft202012Validator(self.residue_schema).validate(residue)
            self.assertEqual(events.read_bytes(), causal_before)
            causal_receipt = validator.validate_events(
                validator.load_events(residue_path), str(residue_path)
            )
            self.assertEqual(causal_receipt["status"], "block")
            self.assertEqual(
                causal_receipt["errors"][0]["code"], "event_schema_violation"
            )


if __name__ == "__main__":
    unittest.main()

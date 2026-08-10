#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


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

    def persist_actions(self, root: Path) -> dict[str, Path]:
        paths: dict[str, Path] = {}
        for action in self.run_plan["actions"]:
            path = root / "actions" / f"{action['action_id']}.json"
            write_json(path, action)
            paths[action["action_id"]] = path
        return paths

    def copy_receipts(self, root: Path) -> Path:
        receipts = root / "receipts"
        shutil.copytree(REDUCE / "pass", receipts)
        return receipts

    def build_pre_join_stream(self, root: Path) -> Path:
        events = root / "events.jsonl"
        action_paths = self.persist_actions(root)
        receipts = {
            value["action_id"]: value
            for value in (
                load_json(path) for path in sorted((REDUCE / "pass").glob("*.json"))
            )
        }
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
                events,
                root / "advance",
            )
            self.assertEqual(result["receipt_admission"]["status"], "pass")
            self.assertEqual(result["gate_decision"]["decision"], "gate_block")
            self.assertEqual(result["action_set"]["actions"], [])
            self.assertEqual(result["event_validation"]["status"], "pass")

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

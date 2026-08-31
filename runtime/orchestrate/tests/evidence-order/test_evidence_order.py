#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
TEST_ROOT = Path(__file__).resolve().parent
FIXTURES = TEST_ROOT / "fixtures"
SCRIPT = ARCANUM_ROOT / "runtime/orchestrate/scripts/validate_run_evidence.py"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"

SPEC = importlib.util.spec_from_file_location("validate_run_evidence", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class EvidenceOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = load_json(TEST_ROOT / "fixture-matrix.json")
        cls.event_schema = load_json(SCHEMAS / "run-event.schema.json")
        cls.receipt_schema = load_json(SCHEMAS / "evidence-validation-receipt.schema.json")

    def test_fixture_matrix_has_exact_causal_verdicts(self) -> None:
        for case in self.matrix["cases"]:
            with self.subTest(case=case["case_id"]):
                events = validator.load_events(TEST_ROOT / case["source"])
                for event in events:
                    Draft202012Validator(self.event_schema).validate(event)
                receipt = validator.validate_events(events, case["source"])
                Draft202012Validator(self.receipt_schema).validate(receipt)
                self.assertEqual(receipt["valid"], case["valid"])
                self.assertEqual([error["code"] for error in receipt["errors"]], case["expected_error_codes"])

    def test_matrix_covers_complete_join_lifecycle_contract(self) -> None:
        case_ids = {case["case_id"] for case in self.matrix["cases"]}
        required_cases = {
            "valid-terminal-close",
            "valid-timeout-interrupt",
            "registration-before-host-return",
            "duplicate-registration",
            "wait-before-full-registration",
            "terminal-without-wait",
            "close-before-terminal",
            "duplicate-close",
            "interrupt-without-timeout",
            "duplicate-interrupt",
            "joined-before-cleanup",
            "gate-before-required-join",
        }
        self.assertTrue(required_cases.issubset(case_ids))

        event_kinds = set(self.event_schema["properties"]["event"]["enum"])
        self.assertTrue(
            {
                "agent_wait_registered",
                "agent_binding_corrected",
                "wait_attempted",
                "agent_closed",
                "wait_timed_out",
                "agent_interrupted",
            }.issubset(event_kinds)
        )

    def test_valid_stream_has_stable_receipt(self) -> None:
        source = "fixtures/valid-ordered.jsonl"
        receipt = validator.validate_events(validator.load_events(TEST_ROOT / source), source)
        self.assertEqual(receipt, load_json(FIXTURES / "expected-valid-receipt.json"))

    def test_unknown_event_kind_fails_closed_before_causal_reduction(self) -> None:
        event = validator.load_events(FIXTURES / "valid-ordered.jsonl")[0]
        event["event"] = "post_hoc_claim"
        receipt = validator.validate_events([event], "unknown-event.jsonl")
        Draft202012Validator(self.receipt_schema).validate(receipt)
        self.assertEqual([error["code"] for error in receipt["errors"]], ["event_schema_violation"])

    def test_v03_terminal_resolution_is_preserved_and_cannot_unlock_work(self) -> None:
        events = validator.load_events(FIXTURES / "valid-ordered.jsonl")
        resolved = {
            "schema_version": "arcanum.native-dispatch-runner.run-event.v0.3",
            "sequence": 16,
            "event": "gate_decided",
            "dispatch_id": "dispatch-evidence-order",
            "run_id": "run-valid",
            "wave_id": "wave-1",
            "action_id": None,
            "agent_id": None,
            "operation": "orchestrate.reduce",
            "gate_id": "gate-wave-1",
            "decision": "gate_resolved",
            "domain_outcome": {
                "role_id": "validity-skeptic",
                "source_field": "proposal_status",
                "value": "invalid",
                "classification": "resolved",
            },
            "required_action_ids": ["spawn-0002"],
            "admitted_receipt_action_ids": ["spawn-0002"],
        }
        Draft202012Validator(self.event_schema).validate(resolved)
        receipt = validator.validate_events([*events, resolved], "resolved.jsonl")
        self.assertTrue(receipt["valid"], receipt["errors"])

        illegal_successor = {
            "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
            "sequence": 17,
            "event": "action_attempted",
            "dispatch_id": "dispatch-evidence-order",
            "run_id": "run-valid",
            "wave_id": "wave-2",
            "action_id": "spawn-0003",
            "agent_id": None,
            "operation": "collaboration.spawn_agent",
            "depends_on_gate_id": "gate-wave-1",
        }
        blocked = validator.validate_events([*events, resolved, illegal_successor], "resolved-successor.jsonl")
        self.assertFalse(blocked["valid"])
        self.assertTrue(any("gate" in error["code"] for error in blocked["errors"]), blocked["errors"])

    def test_old_event_versions_reject_v03_domain_fields_and_decisions(self) -> None:
        event = {
            "schema_version": "arcanum.native-dispatch-runner.run-event.v0.1",
            "sequence": 1,
            "event": "gate_decided",
            "dispatch_id": "dispatch-old",
            "run_id": "run-old",
            "wave_id": "wave-old",
            "action_id": None,
            "agent_id": None,
            "operation": "orchestrate.reduce",
            "gate_id": "gate-old",
            "decision": "gate_resolved",
            "domain_outcome": {
                "role_id": "role-old", "source_field": "status",
                "value": "invalid", "classification": "resolved",
            },
            "required_action_ids": ["spawn-0001"],
            "admitted_receipt_action_ids": ["spawn-0001"],
        }
        schema_errors = list(Draft202012Validator(self.event_schema).iter_errors(event))
        self.assertTrue(schema_errors)
        receipt = validator.validate_events([event], "old-version-domain.jsonl")
        self.assertEqual(receipt["errors"][0]["code"], "event_schema_violation")

    def test_cli_writes_receipt_and_returns_fail_closed_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "receipt.json"
            valid = subprocess.run(["python3", str(SCRIPT), str(FIXTURES / "valid-ordered.jsonl"), "--output", str(output)], check=False, capture_output=True, text=True)
            self.assertEqual(valid.returncode, 0, valid.stderr or valid.stdout)
            Draft202012Validator(self.receipt_schema).validate(load_json(output))

            invalid = subprocess.run(["python3", str(SCRIPT), str(FIXTURES / "missing-attempt.jsonl"), "--output", str(output)], check=False, capture_output=True, text=True)
            self.assertEqual(invalid.returncode, 1, invalid.stderr or invalid.stdout)
            receipt = load_json(output)
            Draft202012Validator(self.receipt_schema).validate(receipt)
            self.assertEqual(receipt["status"], "block")
            self.assertEqual(receipt["errors"][0]["code"], "missing_action_attempt")


if __name__ == "__main__":
    unittest.main()

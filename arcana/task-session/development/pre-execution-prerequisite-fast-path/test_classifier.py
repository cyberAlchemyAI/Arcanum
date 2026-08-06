#!/usr/bin/env python3
"""Acceptance tests for the pure pre-execution prerequisite classifier."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import time
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "scripts" / "classify-pre-execution-prerequisite.py"
FIXTURES = HERE / "fixtures" / "classifier-cases.json"
SPEC = importlib.util.spec_from_file_location("pre_execution_classifier", SCRIPT)
assert SPEC and SPEC.loader
CLASSIFIER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLASSIFIER
SPEC.loader.exec_module(CLASSIFIER)


TARGETS = [{
    "path": "candidate/RESULT.md",
    "state": "absent",
    "sha256": None,
    "size_bytes": None,
    "lifecycle_owner": "invoke",
    "authority_class": "public",
    "publication_class": "internal",
}]
VALIDATION = [{
    "command_id": "validate-result",
    "argv": ["python3", "validate.py"],
    "cwd": ".",
    "timeout_seconds": 30,
    "max_output_bytes": 65536,
}]


def base_prerequisite() -> dict:
    return {
        "schema_version": "task-session.pre-execution-owner-prerequisite.v1",
        "prerequisite_id": "PEP-001",
        "task_id": "TASK-001",
        "swu_id": "SWU-001",
        "attempt_id": "attempt-001",
        "owner_route": {"capability": "invoke", "mode": "refresh", "mutation_mode": "apply-approved"},
        "trigger": {
            "kind": "declared-owner-prerequisite",
            "source_selectors": [{"path": "WORK-PACK.md", "sha256": "a" * 64, "size_bytes": 10}],
        },
        "target_inventory": copy.deepcopy(TARGETS),
        "validation_contracts": copy.deepcopy(VALIDATION),
        "expected_owner_receipt": {
            "schema_id": "invoke.owner-receipt.v1",
            "owner_capability": "invoke",
            "receipt_selector": "candidate/receipt.json",
        },
        "satisfaction_predicate": {
            "kind": "json-pointer-any-of",
            "receipt_pointer": "/result",
            "accepted_values": ["pass"],
        },
        "authorization_requirement": {
            "required": True,
            "evidence_selector": "current-dispatch-authorization",
            "binding_fields": ["owner_route", "task_id", "swu_id", "attempt_id", "target_inventory", "validation_contracts", "allowed_effect"],
        },
        "resume_point": "task-session:context-build",
        "max_owner_hops": 1,
        "allowed_effect": "pre-execution-prerequisite-resolution",
        "fingerprint_inputs": ["schema_version", "prerequisite_id", "task_id", "swu_id", "attempt_id", "owner_route", "trigger", "target_inventory", "validation_contracts", "expected_owner_receipt", "satisfaction_predicate", "authorization_requirement", "resume_point", "max_owner_hops", "allowed_effect"],
    }


def base_payload() -> dict:
    return {
        "work_pack": {"work_pack_id": "WP-001", "current": True},
        "selected_unit": {
            "work_pack_id": "WP-001",
            "task_id": "TASK-001",
            "swu_id": "SWU-001",
            "attempt_id": "attempt-001",
            "entry_contract_current": True,
            "plan_once_selection_ready": False,
            "target_inventory": copy.deepcopy(TARGETS),
            "validation_contracts": copy.deepcopy(VALIDATION),
        },
        "prerequisite": base_prerequisite(),
        "satisfaction_receipt": None,
        "authorization": None,
        "consumed_attempt_fingerprints": [],
    }


def payload_for(variant: str) -> dict:
    payload = base_payload()
    prerequisite = payload["prerequisite"]
    fingerprint = CLASSIFIER.prerequisite_fingerprint(prerequisite)
    if variant == "no-prerequisite":
        payload["prerequisite"] = None
    elif variant == "plan-once":
        payload["prerequisite"] = None
        payload["selected_unit"]["plan_once_selection_ready"] = True
    elif variant in {"authorized", "authorization-mismatch", "authorization-expanded"}:
        payload["authorization"] = {
            "owner_route": copy.deepcopy(prerequisite["owner_route"]),
            "task_id": "TASK-001",
            "swu_id": "SWU-001",
            "attempt_id": "attempt-001",
            "target_inventory": copy.deepcopy(TARGETS),
            "validation_contracts": copy.deepcopy(VALIDATION),
            "allowed_effect": "pre-execution-prerequisite-resolution",
            "evidence_ref": {"path": "authorization.json", "sha256": "b" * 64, "size_bytes": 20},
        }
        if variant == "authorization-mismatch":
            payload["authorization"]["owner_route"] = {"capability": "invoke", "mode": "refresh", "mutation_mode": "proposal-only"}
        if variant == "authorization-expanded":
            payload["authorization"]["target_inventory"].append({
                "path": "candidate/EXTRA.md",
                "state": "absent",
                "sha256": None,
                "size_bytes": None,
                "lifecycle_owner": "invoke",
                "authority_class": "public",
                "publication_class": "internal",
            })
    elif variant in {"satisfied", "mismatched-receipt"}:
        payload["satisfaction_receipt"] = {
            "schema_id": "invoke.owner-receipt.v1",
            "owner_capability": "invoke",
            "task_id": "TASK-001",
            "swu_id": "SWU-001",
            "attempt_id": "attempt-001",
            "prerequisite_fingerprint": fingerprint,
            "result": "pass",
        }
        if variant == "mismatched-receipt":
            payload["satisfaction_receipt"]["attempt_id"] = "attempt-other"
    elif variant == "ambiguous":
        prerequisite["trigger"]["source_selectors"].append({"path": "TASK.md", "sha256": "c" * 64, "size_bytes": 11})
    elif variant == "stale":
        payload["selected_unit"]["target_inventory"] = []
    elif variant == "invalid":
        payload["prerequisite"] = {"legacy": True}
    elif variant == "repeated":
        payload["consumed_attempt_fingerprints"] = [f"attempt-001:{fingerprint}"]
    return payload


class ClassifierTests(unittest.TestCase):
    def test_fixture_matrix_and_phase_budget(self) -> None:
        cases = json.loads(FIXTURES.read_text(encoding="utf-8"))["cases"]
        started = time.monotonic()
        for case in cases:
            with self.subTest(case=case["case_id"]):
                result = CLASSIFIER.classify(payload_for(case["variant"]))
                receipt = result["classification_receipt"]
                self.assertEqual(receipt["classification"], case["classification"])
                self.assertEqual(result["execution_entry_state"], case["entry_state"])
                self.assertEqual(receipt["permitted_next_action"], case["action"])
                self.assertEqual(receipt["authorization"]["status"], case["authorization_status"])
                self.assertEqual(len(receipt["inputs_read"]), case["read_count"])
                self.assertEqual(len(result["control_inputs"]), case["control_count"])
                self.assertLessEqual(len(receipt["inputs_read"]), 4)
                self.assertFalse(receipt["phase_trace"]["context_builder_entered"])
                self.assertFalse(receipt["phase_trace"]["mutation_admission_entered"])
                self.assertFalse(receipt["phase_trace"]["implementation_inspected"])
                self.assertFalse(receipt["phase_trace"]["target_mutation_entered"])
                self.assertEqual(receipt["phase_trace"]["owner_hops_dispatched"], 0)
        self.assertLess(time.monotonic() - started, 5.0)

    def test_fingerprint_changes_for_every_declared_input(self) -> None:
        prerequisite = base_prerequisite()
        baseline = CLASSIFIER.prerequisite_fingerprint(prerequisite)
        for field in prerequisite["fingerprint_inputs"]:
            changed = copy.deepcopy(prerequisite)
            if field == "max_owner_hops":
                changed[field] = 2
            elif isinstance(changed[field], str):
                changed[field] += "-changed"
            elif isinstance(changed[field], list):
                changed[field] = list(reversed(changed[field])) if len(changed[field]) > 1 else changed[field] + [copy.deepcopy(changed[field][0])]
            else:
                changed[field] = {**changed[field], "_changed": True}
            self.assertNotEqual(CLASSIFIER.prerequisite_fingerprint(changed), baseline, field)


if __name__ == "__main__":
    unittest.main(verbosity=2)

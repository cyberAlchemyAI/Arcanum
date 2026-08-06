#!/usr/bin/env python3
"""Cross-capability canaries for the pre-execution prerequisite entry route."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CLASSIFIER_CASES = load_module("pep_classifier_cases", HERE / "test_classifier.py")
OWNER_CASES = load_module("pep_owner_cases", HERE / "test_owner_resume.py")
CLASSIFIER = CLASSIFIER_CASES.CLASSIFIER


class PreExecutionIntegrationTests(unittest.TestCase):
    def test_plan_once_is_not_an_owner_prerequisite(self) -> None:
        result = CLASSIFIER.classify(CLASSIFIER_CASES.payload_for("plan-once"))
        receipt = result["classification_receipt"]
        self.assertEqual(result["execution_entry_state"], "plan-once-selection-ready")
        self.assertEqual(receipt["permitted_next_action"], "continue-context-build")
        self.assertEqual(receipt["phase_trace"]["owner_hops_dispatched"], 0)
        self.assertFalse(receipt["phase_trace"]["context_builder_entered"])

    def test_unmet_unauthorized_blocks_before_context_or_writes(self) -> None:
        result = CLASSIFIER.classify(CLASSIFIER_CASES.payload_for("unmet"))
        receipt = result["classification_receipt"]
        self.assertEqual(receipt["classification"], "unmet")
        self.assertEqual(receipt["authorization"]["status"], "missing")
        self.assertEqual(receipt["permitted_next_action"], "block-missing-authorization")
        self.assertFalse(receipt["phase_trace"]["context_builder_entered"])
        self.assertFalse(receipt["phase_trace"]["target_mutation_entered"])

    def test_authorized_owner_join_returns_to_same_attempt_once(self) -> None:
        classified = CLASSIFIER.classify(CLASSIFIER_CASES.payload_for("authorized"))
        self.assertEqual(
            classified["classification_receipt"]["permitted_next_action"],
            "route-one-owner-hop",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path, run_dir = OWNER_CASES.build_case(root)
            request = json.loads(request_path.read_text(encoding="utf-8"))
            route_path = root / request["pre_execution_prerequisite"]["continuation_route_receipt_ref"]["path"]
            route = json.loads(route_path.read_text(encoding="utf-8"))
            self.assertEqual(route["source"]["phase"], "pre-execution-prerequisite")
            self.assertEqual(route["control_handle"]["mode"], "resume-same-attempt")
            self.assertIsNone(route["returned_next_route"])
            first = OWNER_CASES.RUNNER.prerequisite_resume(root, request_path, run_dir)
            self.assertEqual(first["result"], "pass")
            self.assertEqual(first["resume_point"], "task-session:context-build")
            self.assertEqual(first["resume_count"], 1)
            replay = OWNER_CASES.RUNNER.prerequisite_resume(root, request_path, run_dir)
            self.assertEqual(replay["result"], "already-resumed")
            self.assertEqual(replay["context_builder_entry_budget"], 0)
            self.assertIsNone(replay["next_action"])

    def test_ambiguous_stale_and_expanded_scope_fail_closed(self) -> None:
        for variant, expected in (
            ("ambiguous", "ambiguous"),
            ("stale", "stale"),
            ("authorization-expanded", "unmet"),
        ):
            with self.subTest(variant=variant):
                result = CLASSIFIER.classify(CLASSIFIER_CASES.payload_for(variant))
                receipt = result["classification_receipt"]
                self.assertEqual(receipt["classification"], expected)
                self.assertEqual(receipt["permitted_next_action"], "block")
                self.assertFalse(receipt["phase_trace"]["context_builder_entered"])
                self.assertFalse(receipt["phase_trace"]["target_mutation_entered"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path, run_dir = OWNER_CASES.build_case(root, "changed-baseline")
            with self.assertRaises(OWNER_CASES.RUNNER.RunnerBlock):
                OWNER_CASES.RUNNER.prerequisite_resume(root, request_path, run_dir)
            self.assertFalse((run_dir / "pre-execution-resume-receipt.json").exists())

    def test_legacy_no_prerequisite_keeps_context_ready_path(self) -> None:
        result = CLASSIFIER.classify(CLASSIFIER_CASES.payload_for("no-prerequisite"))
        receipt = result["classification_receipt"]
        self.assertEqual(receipt["classification"], "satisfied")
        self.assertEqual(result["execution_entry_state"], "context-ready")
        self.assertEqual(receipt["permitted_next_action"], "continue-context-build")
        self.assertEqual(receipt["phase_trace"]["owner_hops_dispatched"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

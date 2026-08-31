#!/usr/bin/env python3
"""Generic regression matrix for execution-entry consumer closure."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPOSITORY_ROOT / "arcanum/arcana/task-session/scripts"))


def load(relative: str, name: str):
    path = REPOSITORY_ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


FIXTURE = load(
    "arcanum/arcana/task-session/development/test_execution_entry_projection.py",
    "invoke_generic_execution_entry_fixture",
)
VALIDATOR = load(
    "arcanum/arcana/task-session/scripts/execution_entry_projection.py",
    "invoke_generic_execution_entry_validator",
)


class ExecutionEntryNegativeCases(unittest.TestCase):
    def assertClosureBlock(self, document):
        self.assertEqual(VALIDATOR.validate_document(document)["closure_result"], "block")

    def test_all_declared_negative_cases(self):
        cases = {}
        value = FIXTURE.document(); value["units"][0]["material_delta_classes"] = ["status_changed"]; cases["delta-axis-substitution"] = value
        value = FIXTURE.document(); contract = value["units"][0]["native_context_projection"]["execution_contract"]; contract["allowed_writes"] = contract.pop("allowedWrites"); cases["snake-camel-mismatch"] = value
        value = FIXTURE.document(); projection = value["units"][0]["native_context_projection"]; projection["admission_schema_version"] = "1.3.0"; cases["missing-required-transientOutputs-v1.3"] = value
        value = FIXTURE.document(); value["units"][0]["native_context_projection"]["execution_contract"]["transientOutputs"] = ["tmp/output"]; cases["forbidden-transientOutputs-v1.2"] = value
        value = FIXTURE.document(); del value["units"][0]["route_scope_partition"]; cases["missing-route-scope-partition"] = value
        value = FIXTURE.document(); value["units"][0]["route_scope_partition"]["exact_union_scope"].pop(); cases["wrong-route-scope-partition"] = value
        value = FIXTURE.document(); lifecycle = value["units"][0]["route_scope_partition"]["lifecycle_owner_scopes"][0]["path"]; value["units"][0]["native_context_projection"]["execution_contract"]["allowedWrites"].append(lifecycle); cases["lifecycle-scope-copied-into-admission"] = value
        value = FIXTURE.document(); value["execution_entry_closure"]["consumer_rehearsal"]["fixture_only_substitution"] = "allowed"; cases["fixture-only-validator-substitution"] = value
        for case_id, document in cases.items():
            with self.subTest(case_id=case_id): self.assertClosureBlock(document)
        self.assertEqual(len(cases), 8)

    def test_stale_exact_evidence_fails(self):
        closure = load(
            "arcanum/spells/invoke/scripts/preacceptance_closure.py",
            "invoke_stale_execution_entry_evidence",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root / "source.json"; path.write_text("{}\n", encoding="utf-8")
            reference = {"path": "source.json", "sha256": "0" * 64, "size_bytes": 3}
            failures = closure.validate_exact_ref(root, reference, "execution-entry source")
            self.assertTrue(any("digest mismatch" in item for item in failures))

    def test_missing_request_eligibility_blocks_request_only(self):
        result = VALIDATOR.validate_document(FIXTURE.document())
        self.assertEqual(result["closure_result"], "pass")
        self.assertEqual(result["request_eligibility_result"], "block")
        self.assertEqual(result["request_eligibility_blockers"], ["REQUEST_EMISSION_ELIGIBILITY_BINDING_MISSING"])
        self.assertEqual(result["owner_acceptance_status"], "pending")
        self.assertEqual(result["selection_admission_authority"], "absent")


if __name__ == "__main__": unittest.main()

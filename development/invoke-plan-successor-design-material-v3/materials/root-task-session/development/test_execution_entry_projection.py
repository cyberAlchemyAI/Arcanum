#!/usr/bin/env python3
"""Regression checks for the execution-entry projection boundary."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/execution_entry_projection.py"


def module():
    spec = importlib.util.spec_from_file_location("execution_entry_projection", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(loaded)
    return loaded


def unit(unit_id: str, owner: str, receipt: str):
    executor = [f"src/{unit_id}.py", f"evidence/{unit_id}/validation.json"]
    lifecycle = [
        {"path": f"evidence/{unit_id}/precloseout.json", "owner_capability": "task-session", "write_class": "precloseout-receipt"},
        {"path": f"evidence/{unit_id}/owner.json", "owner_capability": owner, "write_class": "owner-closeout-receipt"},
    ]
    terminal = f"evidence/{unit_id}/terminal.json"
    contract = {
        "writeProfile": "material-bound", "materialWrites": [f"src/{unit_id}.py"],
        "executionOutputs": [f"evidence/{unit_id}/validation.json"], "allowedWrites": executor,
        "validationCommands": [f"python3 tests/{unit_id}.py"], "lifecycleOwner": owner,
        "authorityClass": "public", "publicationClass": "public",
    }
    return {
        "task_id": f"TASK-{unit_id}", "unit_id": unit_id, "lifecycle_owner": owner,
        "owner_receipt_schema_identity": receipt, "authority_class": "public", "publication_class": "public",
        "material_writes": [f"src/{unit_id}.py"], "executor_outputs": [f"evidence/{unit_id}/validation.json"],
        "validation_contracts": [{"argv": ["python3", f"tests/{unit_id}.py"]}],
        "material_delta_classes": ["declared-add"],
        "lifecycle_closeout_delta_classes": ["evidence_added", "status_changed", "route_changed"],
        "native_context_projection": {"task_id": f"TASK-{unit_id}", "swu_id": unit_id, "strict_coverage": True, "admission_schema_version": "1.2.0", "execution_contract": contract},
        "route_scope_partition": {"schema_version": "task-session.fast-entry-route-scope-partition.v1", "executor_write_scopes": executor, "lifecycle_owner_scopes": lifecycle, "terminal_receipt_scope": terminal, "exact_union_scope": executor + [item["path"] for item in lifecycle] + [terminal]},
        "route_write_scope": executor + [item["path"] for item in lifecycle] + [terminal],
    }


def document():
    return {
        "execution_entry_closure": {
            "schema_version": "execution-entry-closure.v1",
            "consumer_rehearsal": {"effect": "deterministic-no-effect", "exact_finalized_unit": "SWU-001", "fixture_only_substitution": "forbidden", "required_runs": 2, "stages": ["wpra", "implementation-readiness", "context-builder", "mutation-admission", "governance-prepare", "closeout-preflight", "heterogeneous-owner-closeout", "terminal", "continuity"]},
            "material_delta_classes": ["declared-add", "declared-replace", "generated-from-canonical"],
            "lifecycle_closeout_delta_classes": ["evidence_added", "status_changed", "route_changed"],
            "semantic_acceptance_binding": {"required": True, "eligibility_receipt": None, "owner_acceptance_receipt": None},
        },
        "units": [unit("SWU-001", "owner-a", "owner-a.receipt.v1"), unit("SWU-002", "owner-b", "owner-b.receipt.v1")],
    }


class ExecutionEntryProjectionTests(unittest.TestCase):
    def test_single_owner_frontier_passes_when_every_unit_is_typed(self):
        value = document()
        value["units"] = [
            unit("SWU-001", "invoke", "invoke.precloseout-refresh-closeout-receipt.v1"),
            unit("SWU-002", "invoke", "invoke.precloseout-refresh-closeout-receipt.v1"),
        ]
        result = module().validate_document(value)
        self.assertEqual(result["closure_result"], "pass")
        self.assertEqual(result["owner_identities"], ["invoke"])
        self.assertEqual(
            result["owner_receipt_schema_identities"],
            ["invoke.precloseout-refresh-closeout-receipt.v1"],
        )
        self.assertEqual(result["request_eligibility_result"], "block")

    def test_valid_closure_passes_but_request_eligibility_blocks(self):
        result = module().validate_document(document())
        self.assertEqual(result["closure_result"], "pass")
        self.assertEqual(result["request_eligibility_result"], "block")
        self.assertEqual(result["owner_acceptance_status"], "pending")
        self.assertEqual(result["selection_admission_authority"], "absent")

    def test_exact_eligibility_binding_passes_with_owner_acceptance_pending(self):
        value = document()
        value["execution_entry_closure"]["semantic_acceptance_binding"]["eligibility_receipt"] = {
            "path": "evidence/request-eligibility.json",
            "sha256": "a" * 64,
            "size_bytes": 123,
        }
        result = module().validate_document(value)
        self.assertEqual(result["request_eligibility_result"], "pass")
        self.assertEqual(result["owner_acceptance_status"], "pending")
        self.assertEqual(result["selection_admission_authority"], "absent")

    def test_prose_or_empty_eligibility_binding_cannot_pass(self):
        for malformed in ("approved", {}):
            value = document()
            value["execution_entry_closure"]["semantic_acceptance_binding"]["eligibility_receipt"] = malformed
            result = module().validate_document(value)
            self.assertEqual(result["request_eligibility_result"], "block")
        self.assertEqual(result["authority_effect"], "none")

    def test_cross_axis_and_partition_faults_fail_closed(self):
        value = document(); value["units"][0]["material_delta_classes"] = ["status_changed"]
        self.assertEqual(module().validate_document(value)["closure_result"], "block")
        value = document(); value["units"][0]["route_scope_partition"]["executor_write_scopes"].append("evidence/SWU-001/owner.json")
        self.assertEqual(module().validate_document(value)["closure_result"], "block")

    def test_snake_case_and_fixture_substitution_fail_closed(self):
        value = document(); contract = value["units"][0]["native_context_projection"]["execution_contract"]
        contract["allowed_writes"] = contract.pop("allowedWrites")
        self.assertEqual(module().validate_document(value)["closure_result"], "block")
        value = document(); value["execution_entry_closure"]["consumer_rehearsal"]["fixture_only_substitution"] = "allowed"
        self.assertEqual(module().validate_document(value)["closure_result"], "block")

    def test_missing_or_blank_owner_frontier_fails_closed(self):
        cases = (
            ("lifecycle_owner", None),
            ("lifecycle_owner", ""),
            ("owner_receipt_schema_identity", None),
            ("owner_receipt_schema_identity", ""),
        )
        for field, replacement in cases:
            with self.subTest(field=field, replacement=replacement):
                value = document()
                value["units"][0][field] = replacement
                if field == "lifecycle_owner":
                    value["units"][0]["native_context_projection"]["execution_contract"][
                        "lifecycleOwner"
                    ] = replacement
                result = module().validate_document(value)
                self.assertEqual(result["closure_result"], "block")
                self.assertTrue(
                    any("frontier is incomplete" in failure for failure in result["failures"])
                )


if __name__ == "__main__": unittest.main()

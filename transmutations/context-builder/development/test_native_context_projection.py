#!/usr/bin/env python3
"""Generic regressions for machine-first native context projection."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compile_native_context_projection.py"


def load_module():
    specification = importlib.util.spec_from_file_location("context_projection_compiler", SCRIPT)
    module = importlib.util.module_from_spec(specification)
    assert specification and specification.loader
    specification.loader.exec_module(module)
    return module


def source(version: str = "1.2.0", transients: list[str] | None = None):
    material = ["src/feature.py"]
    outputs = ["evidence/result.json"]
    contract = {
        "writeProfile": "material-bound", "materialWrites": material,
        "executionOutputs": outputs, "allowedWrites": material + outputs,
        "validationCommands": ["python3 tests/test_feature.py"],
        "lifecycleOwner": "owner-a", "authorityClass": "public",
        "publicationClass": "public",
    }
    if version == "1.3.0":
        contract["transientOutputs"] = transients or ["evidence/transient.log"]
        outputs += contract["transientOutputs"]
        contract["allowedWrites"] = material + outputs
    lifecycle = [
        {"path": "evidence/precloseout.json", "owner_capability": "task-session", "write_class": "precloseout-receipt"},
        {"path": "evidence/owner.json", "owner_capability": "owner-a", "write_class": "owner-closeout-receipt"},
    ]
    unit = {
        "task_id": "TASK-GENERIC-001", "unit_id": "SWU-GENERIC-001",
        "lifecycle_owner": "owner-a", "owner_receipt_schema_identity": "owner-a.receipt.v1",
        "authority_class": "public", "publication_class": "public",
        "material_writes": material, "executor_outputs": outputs,
        "validation_contracts": [{"argv": ["python3", "tests/test_feature.py"]}],
        "material_delta_classes": ["declared-add"],
        "lifecycle_closeout_delta_classes": ["evidence_added", "status_changed", "route_changed"],
        "native_context_projection": {"task_id": "TASK-GENERIC-001", "swu_id": "SWU-GENERIC-001", "strict_coverage": True, "admission_schema_version": version, "execution_contract": contract},
        "route_scope_partition": {"schema_version": "task-session.fast-entry-route-scope-partition.v1", "executor_write_scopes": material + outputs, "lifecycle_owner_scopes": lifecycle, "terminal_receipt_scope": "evidence/terminal.json", "exact_union_scope": material + outputs + [item["path"] for item in lifecycle] + ["evidence/terminal.json"]},
    }
    unit["route_write_scope"] = unit["route_scope_partition"]["exact_union_scope"]
    second = copy.deepcopy(unit)
    second.update({"task_id": "TASK-GENERIC-002", "unit_id": "SWU-GENERIC-002", "lifecycle_owner": "owner-b", "owner_receipt_schema_identity": "owner-b.receipt.v1"})
    second["native_context_projection"].update({"task_id": "TASK-GENERIC-002", "swu_id": "SWU-GENERIC-002"})
    second["native_context_projection"]["execution_contract"]["lifecycleOwner"] = "owner-b"
    return {"execution_entry_closure": {"schema_version": "execution-entry-closure.v1", "consumer_rehearsal": {"effect": "deterministic-no-effect", "exact_finalized_unit": "SWU-GENERIC-001", "fixture_only_substitution": "forbidden", "required_runs": 2, "stages": ["wpra", "implementation-readiness", "context-builder", "mutation-admission", "governance-prepare", "closeout-preflight", "heterogeneous-owner-closeout", "terminal", "continuity"]}, "material_delta_classes": ["declared-add", "declared-replace", "generated-from-canonical"], "lifecycle_closeout_delta_classes": ["evidence_added", "status_changed", "route_changed"], "semantic_acceptance_binding": {"required": True, "eligibility_receipt": None, "owner_acceptance_receipt": None}}, "units": [unit, second]}


class ProjectionTests(unittest.TestCase):
    def test_compiles_exact_v12_machine_view(self):
        module = load_module()
        result = module.compile_projection(source(), "SWU-GENERIC-001")
        self.assertNotIn("transientOutputs", result["execution_contract"])
        self.assertEqual(result["swu_id"], "SWU-GENERIC-001")

    def test_v12_forbids_transients(self):
        module = load_module(); document = source()
        document["units"][0]["native_context_projection"]["execution_contract"]["transientOutputs"] = ["tmp/out"]
        with self.assertRaises(ValueError): module.compile_projection(document, "SWU-GENERIC-001")

    def test_v13_requires_nonempty_actual_transients(self):
        module = load_module(); document = source("1.3.0")
        self.assertEqual(module.compile_projection(document, "SWU-GENERIC-001")["admission_schema_version"], "1.3.0")
        document["units"][0]["native_context_projection"]["execution_contract"]["transientOutputs"] = []
        with self.assertRaises(ValueError): module.compile_projection(document, "SWU-GENERIC-001")

    def test_rejects_snake_case_and_lifecycle_scope_in_admission(self):
        module = load_module(); document = source(); contract = document["units"][0]["native_context_projection"]["execution_contract"]
        contract["allowed_writes"] = contract.pop("allowedWrites")
        with self.assertRaises(ValueError): module.compile_projection(document, "SWU-GENERIC-001")
        document = source(); lifecycle = document["units"][0]["route_scope_partition"]["lifecycle_owner_scopes"][0]["path"]
        document["units"][0]["native_context_projection"]["execution_contract"]["allowedWrites"].append(lifecycle)
        with self.assertRaises(ValueError): module.compile_projection(document, "SWU-GENERIC-001")


if __name__ == "__main__": unittest.main()

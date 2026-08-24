#!/usr/bin/env python3
"""Validate Refine's consumption of the Invoke-owned readiness receipt."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REFINE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = REFINE_ROOT.parents[2]
VALIDATOR = REFINE_ROOT / "scripts" / "validate-invoke-plan-readiness.py"


class RefineInvokePlanReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_json(self, relative: str, value: dict) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path

    def exact(self, relative: str) -> dict:
        content = (self.root / relative).read_bytes()
        return {
            "path": relative,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
        }

    def valid_receipt(self) -> dict:
        digest = "a" * 64
        return {
            "schema_version": "implementation-readiness.plan-readiness-preflight-receipt/v1",
            "status": "pass",
            "code": "PLAN_IMPLEMENTATION_READY",
            "work_pack_id": "WP-REFINE-001",
            "work_pack_semantic_digest": digest,
            "frontier": ["SWU-001"],
            "initial_unit": "SWU-001",
            "policy_digest": digest,
            "allowed_routes_digest": digest,
            "audit_config_digest": digest,
            "audit_report_digest": digest,
            "route_coverage": [
                {"unit_id": "SWU-001", "route_id": "task-SWU-001"}
            ],
            "validation_contract_digests": [
                {"unit_id": "SWU-001", "digest": digest}
            ],
            "proof_invocation_id": "invoke-plan-refine-001",
            "proof_created_at": "2026-08-24T14:00:00Z",
            "fast_entry_proof": {
                "request_digest": digest,
                "receipt_digest": digest,
                "binding_digest": digest,
                "route_fingerprint": digest,
                "decision": "proceed",
                "code": "TASK_READY",
                "mutation_count": 0,
            },
            "reusable_for_execution": False,
            "mutation_ready": False,
            "authority_effect": "none",
            "claim_ceiling": "Compatibility proof only.",
        }

    def run_validator(self, binding: dict, *, validator: Path = VALIDATOR):
        binding_path = self.write_json("binding.json", binding)
        return subprocess.run(
            [
                sys.executable,
                str(validator),
                "--binding",
                str(binding_path),
                "--repository-root",
                str(self.root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_execution_candidate_requires_exact_valid_invoke_receipt(self) -> None:
        self.write_json("readiness.json", self.valid_receipt())
        binding = {
            "schema_version": "refine.invoke-plan-readiness-binding/v1",
            "execution_designation": "execution-candidate",
            "work_pack_id": "WP-REFINE-001",
            "readiness_receipt_ref": self.exact("readiness.json"),
            "non_execution_reason": None,
            "authority_effect": "none",
        }
        completed = self.run_validator(binding)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["code"], "REFINE_PLAN_IMPLEMENTATION_READY")
        self.assertEqual(result["authority_effect"], "none")

        drifted = self.valid_receipt()
        drifted["claim_ceiling"] = "drifted"
        self.write_json("readiness.json", drifted)
        completed = self.run_validator(binding)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("mismatch", completed.stderr)

    def test_non_executing_plan_is_explicit_and_cannot_carry_receipt(self) -> None:
        binding = {
            "schema_version": "refine.invoke-plan-readiness-binding/v1",
            "execution_designation": "non-executing",
            "work_pack_id": None,
            "readiness_receipt_ref": None,
            "non_execution_reason": "Research synthesis has no mutation-capable Work Pack.",
            "authority_effect": "none",
        }
        completed = self.run_validator(binding)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["code"], "NON_EXECUTING_PLAN")

        invalid = dict(binding)
        invalid["work_pack_id"] = "WP-NOT-ALLOWED"
        completed = self.run_validator(invalid)
        self.assertEqual(completed.returncode, 2)

    def test_generated_host_packages_validate_the_same_exact_binding(self) -> None:
        self.write_json("readiness.json", self.valid_receipt())
        binding = {
            "schema_version": "refine.invoke-plan-readiness-binding/v1",
            "execution_designation": "execution-candidate",
            "work_pack_id": "WP-REFINE-001",
            "readiness_receipt_ref": self.exact("readiness.json"),
            "non_execution_reason": None,
            "authority_effect": "none",
        }
        validators = [
            REPOSITORY_ROOT
            / ".agents/skills/refine/scripts/validate-invoke-plan-readiness.py",
            REPOSITORY_ROOT
            / ".claude/skills/refine/scripts/validate-invoke-plan-readiness.py",
        ]
        for validator in validators:
            with self.subTest(validator=str(validator)):
                completed = self.run_validator(binding, validator=validator)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(
                    json.loads(completed.stdout)["code"],
                    "REFINE_PLAN_IMPLEMENTATION_READY",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Validate Refine's consumption of the Invoke-owned Plan stage receipt."""

from __future__ import annotations

import copy
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
REQUIRED_OUTPUTS = [
    "plan-artifact",
    "work-pack",
    "implementation-layering",
    "distill-validation",
    "invoke-result",
    "implementation-readiness-preflight",
]


def canonical_digest(value: dict) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class RefineInvokePlanReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_json(self, relative: str, value: dict) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        return path

    def write_text(self, relative: str, value: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path

    def exact(self, relative: str) -> dict:
        content = (self.root / relative).read_bytes()
        return {"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content)}

    def valid_readiness(self, work_pack_id: str = "WP-REFINE-001") -> dict:
        digest = "a" * 64
        return {
            "schema_version": "implementation-readiness.plan-readiness-preflight-receipt/v1",
            "status": "pass", "code": "PLAN_IMPLEMENTATION_READY",
            "work_pack_id": work_pack_id, "work_pack_semantic_digest": digest,
            "frontier": ["SWU-001"], "initial_unit": "SWU-001",
            "policy_digest": digest, "allowed_routes_digest": digest,
            "audit_config_digest": digest, "audit_report_digest": digest,
            "route_coverage": [{"unit_id": "SWU-001", "route_id": "task-SWU-001"}],
            "validation_contract_digests": [{"unit_id": "SWU-001", "digest": digest}],
            "proof_invocation_id": "invoke-plan-refine-001",
            "proof_created_at": "2026-08-27T02:00:00Z",
            "fast_entry_proof": {
                "request_digest": digest, "receipt_digest": digest,
                "binding_digest": digest, "route_fingerprint": digest,
                "decision": "proceed", "code": "TASK_READY", "mutation_count": 0,
            },
            "reusable_for_execution": False, "mutation_ready": False,
            "authority_effect": "none", "claim_ceiling": "Compatibility proof only.",
        }

    def build_v2(self) -> tuple[dict, dict]:
        self.write_json("readiness.json", self.valid_readiness())
        outputs = []
        for kind in REQUIRED_OUTPUTS:
            if kind == "implementation-readiness-preflight":
                reference = self.exact("readiness.json")
            else:
                path = f"invoke/{kind}.json"
                self.write_text(path, f"{kind}\n")
                reference = self.exact(path)
            outputs.append({"output_kind": kind, "artifact_ref": reference})
        stage = {
            "schema_version": "refine.invoke-plan-stage-receipt/v1",
            "receipt_id": "invoke-plan-stage-001", "stage_id": "s09-invoke-plan",
            "owner_capability": "invoke", "mode": "plan",
            "terminal_status": "pass", "result": "pass",
            "execution_designation": "execution-candidate",
            "work_pack_id": "WP-REFINE-001", "invoke_outputs": outputs,
            "readiness_receipt_ref": self.exact("readiness.json"),
            "authority_effect": "none",
        }
        stage["receipt_digest"] = canonical_digest(stage)
        self.write_json("invoke-stage.json", stage)
        binding = {
            "schema_version": "refine.invoke-plan-readiness-binding/v2",
            "execution_designation": "execution-candidate",
            "work_pack_id": "WP-REFINE-001",
            "invoke_plan_stage_receipt_ref": self.exact("invoke-stage.json"),
            "invoke_outputs": outputs,
            "readiness_receipt_ref": self.exact("readiness.json"),
            "non_execution_reason": None, "authority_effect": "none",
        }
        return binding, stage

    def run_validator(self, binding: dict, *, validator: Path = VALIDATOR):
        binding_path = self.write_json("binding.json", binding)
        return subprocess.run(
            [sys.executable, str(validator), "--binding", str(binding_path), "--repository-root", str(self.root)],
            check=False, capture_output=True, text=True,
        )

    def rewrite_stage(self, binding: dict, stage: dict) -> None:
        stage.pop("receipt_digest", None)
        stage["receipt_digest"] = canonical_digest(stage)
        self.write_json("invoke-stage.json", stage)
        binding["invoke_plan_stage_receipt_ref"] = self.exact("invoke-stage.json")

    def test_v2_execution_candidate_requires_exact_invoke_owned_stage(self) -> None:
        binding, _ = self.build_v2()
        completed = self.run_validator(binding)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["code"], "REFINE_INVOKE_PLAN_STAGE_READY")
        self.assertEqual(result["authority_effect"], "none")

    def test_stage_owner_mode_and_terminal_negatives(self) -> None:
        cases = {
            "missing-receipt": ("binding", "invoke_plan_stage_receipt_ref", None),
            "refine-self-issued": ("stage", "owner_capability", "refine"),
            "wrong-mode": ("stage", "mode", "design"),
            "block-result": ("stage", "result", "block"),
            "flag-result": ("stage", "result", "flag"),
            "block-terminal": ("stage", "terminal_status", "block"),
        }
        for name, (target, field, value) in cases.items():
            with self.subTest(name=name):
                binding, stage = self.build_v2()
                if target == "binding":
                    binding[field] = value
                else:
                    stage[field] = value
                    self.rewrite_stage(binding, stage)
                self.assertEqual(self.run_validator(binding).returncode, 2)

    def test_cross_document_identity_and_readiness_negatives(self) -> None:
        mutations = ("work-pack", "designation", "readiness-ref", "outputs")
        for name in mutations:
            with self.subTest(name=name):
                binding, stage = self.build_v2()
                if name == "work-pack":
                    stage["work_pack_id"] = "WP-OTHER"
                elif name == "designation":
                    stage["execution_designation"] = "non-executing"
                elif name == "readiness-ref":
                    self.write_json("other-readiness.json", self.valid_readiness())
                    stage["readiness_receipt_ref"] = self.exact("other-readiness.json")
                else:
                    stage["invoke_outputs"] = stage["invoke_outputs"][:-1]
                self.rewrite_stage(binding, stage)
                self.assertEqual(self.run_validator(binding).returncode, 2)

    def test_stale_stage_and_output_exact_refs_block(self) -> None:
        binding, _ = self.build_v2()
        stale_stage = copy.deepcopy(binding)
        stale_stage["invoke_plan_stage_receipt_ref"]["sha256"] = "0" * 64
        self.assertEqual(self.run_validator(stale_stage).returncode, 2)
        self.write_text("invoke/plan-artifact.json", "drifted\n")
        self.assertEqual(self.run_validator(binding).returncode, 2)

    def test_v1_is_non_executing_or_historical_only(self) -> None:
        non_executing = {
            "schema_version": "refine.invoke-plan-readiness-binding/v1",
            "execution_designation": "non-executing", "work_pack_id": None,
            "readiness_receipt_ref": None,
            "non_execution_reason": "Research synthesis has no mutation-capable Work Pack.",
            "authority_effect": "none",
        }
        self.assertEqual(self.run_validator(non_executing).returncode, 0)
        self.write_json("readiness.json", self.valid_readiness())
        bypass = {
            "schema_version": "refine.invoke-plan-readiness-binding/v1",
            "execution_designation": "execution-candidate",
            "work_pack_id": "WP-REFINE-001",
            "readiness_receipt_ref": self.exact("readiness.json"),
            "non_execution_reason": None, "authority_effect": "none",
        }
        completed = self.run_validator(bypass)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("historical-read/non-executing only", completed.stderr)

    def test_generated_host_packages_validate_the_same_v2_binding(self) -> None:
        binding, _ = self.build_v2()
        validators = [
            REPOSITORY_ROOT / ".agents/skills/refine/scripts/validate-invoke-plan-readiness.py",
            REPOSITORY_ROOT / ".claude/skills/refine/scripts/validate-invoke-plan-readiness.py",
        ]
        for validator in validators:
            with self.subTest(validator=str(validator)):
                completed = self.run_validator(binding, validator=validator)
                self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

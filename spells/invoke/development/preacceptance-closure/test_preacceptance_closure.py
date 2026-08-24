#!/usr/bin/env python3
"""Regression tests for Invoke preacceptance consumer closure."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
INVOKE_ROOT = HERE.parents[1]
ARCANUM_ROOT = INVOKE_ROOT.parents[1]
REPOSITORY_ROOT = ARCANUM_ROOT.parent
SOURCE_RUNNER = INVOKE_ROOT / "scripts/preacceptance_closure.py"
SOURCE_SCHEMAS = INVOKE_ROOT / "schemas"
NEGATIVE_CASES = HERE / "fixtures/negative-cases.json"

STAGES = [
    "invoke_material_validation",
    "invoke_file_bound_handoff",
    "work_pack_readiness",
    "task_session_until_blocker_preflight",
    "task_session_fast_entry",
    "task_session_mutation_admission",
    "task_session_governance_runner",
    "precloseout",
    "invoke_closeout",
    "task_session_terminal",
    "continuity",
]

REAL_CONSUMER_ENTRYPOINTS = [
    "arcanum/spells/invoke/scripts/material_package_validator.py",
    "arcanum/spells/invoke/scripts/refresh_material_handoff.py",
    "arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py",
    "arcanum/spells/task-session-until-blocker/scripts/run_chain.py",
    "arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py",
    "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
    "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
    "arcanum/arcana/task-session/scripts/plan-once-material-controller.py",
    "arcanum/spells/invoke/development/validate-precloseout-refresh-closeout.py",
    "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
    "arcanum/arcana/continuation-router/scripts/work_pack_route.py",
]


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


class Fixture:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="preacceptance-test-")
        self.root = Path(self.temporary.name)
        self.invoke = self.root / "arcanum/spells/invoke"
        (self.invoke / "scripts").mkdir(parents=True)
        (self.invoke / "schemas").mkdir(parents=True)
        shutil.copy2(SOURCE_RUNNER, self.invoke / "scripts/preacceptance_closure.py")
        for schema in SOURCE_SCHEMAS.glob("*preacceptance*schema.json"):
            shutil.copy2(schema, self.invoke / "schemas" / schema.name)
        shutil.copy2(
            SOURCE_SCHEMAS / "owner-acceptance-request-v2.schema.json",
            self.invoke / "schemas/owner-acceptance-request-v2.schema.json",
        )
        (self.root / "fixture").mkdir()
        self.write_json("fixture/target.json", {"status": "baseline"})
        self.write_json("fixture/candidate.json", {"status": "final"})
        self.write_json("fixture/projection.json", {"kind": "execution-projection"})
        self.write_json(
            "fixture/schema.json",
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "required": ["kind"],
                "properties": {"kind": {"type": "string"}},
            },
        )
        self.write_text(
            "fixture/consumer.py",
            """#!/usr/bin/env python3
import json
import sys
from pathlib import Path
stage = sys.argv[1]
root = Path(sys.argv[2])
(root / f\"{stage}.json\").write_text(json.dumps({\"result\": \"pass\", \"stage\": stage}, sort_keys=True) + \"\\n\", encoding=\"utf-8\")
""",
        )
        self.write_json("fixture/source-reflection.json", {"proposal": "admission-completeness"})
        self.write_json("fixture/negative-regression.json", {"result": "pass", "cases": 16})
        self.write_json("fixture/cross-capability-regression.json", {"result": "pass", "stages": STAGES})
        self.write_json("fixture/rollout.json", {"scope": "canonical-source-local", "result": "pass"})
        self.write_adoption()
        self.write_manifest(self.base_manifest())
        self.write_json("fixture/base-request.json", {"request_id": "fixture-owner-request", "status": "pending"})

    def cleanup(self) -> None:
        self.temporary.cleanup()

    def path(self, relative: str) -> Path:
        return self.root / relative

    def write_text(self, relative: str, value: str) -> Path:
        path = self.path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    def write_json(self, relative: str, value: Any) -> Path:
        return self.write_text(relative, json.dumps(value, indent=2, sort_keys=True) + "\n")

    def exact_ref(self, relative: str) -> dict[str, Any]:
        content = self.path(relative).read_bytes()
        return {
            "path": relative,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
        }

    def write_adoption(self) -> None:
        adoption: dict[str, Any] = {
            "schema_version": "invoke.preacceptance-closure-adoption.v1",
            "adoption_id": "fixture-adoption",
            "proposal_id": "invoke-admission-completeness",
            "source_reflection_ref": self.exact_ref("fixture/source-reflection.json"),
            "implementation_owner": "spellcraft",
            "target_contract_refs": [
                self.exact_ref("arcanum/spells/invoke/scripts/preacceptance_closure.py")
            ],
            "negative_regression_ref": {
                "artifact_ref": self.exact_ref("fixture/negative-regression.json"),
                "result": "pass",
            },
            "cross_capability_regression_ref": {
                "artifact_ref": self.exact_ref("fixture/cross-capability-regression.json"),
                "result": "pass",
            },
            "rollout_evidence_ref": self.exact_ref("fixture/rollout.json"),
            "later_observability_check": {
                "status": "scheduled",
                "trigger": "first emitted v2 request reaches terminal owner decision",
                "owner": "workflow-reflect",
            },
            "status": "implemented",
            "authority_effect": "none",
            "claim_ceiling": "Local regression adoption evidence only.",
        }
        adoption["receipt_digest"] = canonical_digest(adoption)
        self.write_json("fixture/adoption.json", adoption)

    def base_manifest(self) -> dict[str, Any]:
        runner_ref = self.exact_ref("fixture/consumer.py")
        projection_ref = self.exact_ref("fixture/projection.json")
        schema_ref = self.exact_ref("fixture/schema.json")
        stages = []
        for stage in STAGES:
            stages.append(
                {
                    "stage_id": stage,
                    "projection_ref": projection_ref,
                    "runner_ref": runner_ref,
                    "exercised_runner_ref": runner_ref,
                    "argv": [
                        sys.executable,
                        "fixture/consumer.py",
                        stage,
                        "{rehearsal_root}",
                    ],
                    "cwd": ".",
                    "environment_names": ["PATH"],
                    "environment": {},
                    "timeout_seconds": 30,
                    "strict_exit_propagation": True,
                    "allowed_effect": "isolated-rehearsal-output-only",
                    "schema_checks": [
                        {"document_ref": projection_ref, "schema_ref": schema_ref}
                    ],
                }
            )
        derivations = []
        for receipt_class in [
            "governance_request",
            "execution_ticket",
            "admission_consumption",
            "executor_receipt",
            "reconciliation",
            "material_commit_disposition",
        ]:
            derivations.append(
                {
                    "receipt_class": receipt_class,
                    "schema_ref": schema_ref,
                    "predecessor_classes": [],
                    "authoritative_fields": ["kind"],
                    "dynamic_fields": [],
                    "output_path_pattern": f"{{rehearsal_root}}/{receipt_class}.json",
                    "authority_effect": "none",
                }
            )
        return {
            "schema_version": "invoke.preacceptance-closure-manifest.v1",
            "closure_id": "fixture-closure",
            "authority_effect": "none",
            "repository_root": ".",
            "final_postimages": [
                {
                    "target_path": "fixture/target.json",
                    "operation": "replace",
                    "baseline": {
                        "state": "present",
                        "sha256": self.exact_ref("fixture/target.json")["sha256"],
                        "size_bytes": self.exact_ref("fixture/target.json")["size_bytes"],
                    },
                    "postimage_ref": self.exact_ref("fixture/candidate.json"),
                    "lifecycle_assertions": [
                        {"json_pointer": "/status", "operator": "equals", "value": "final"},
                        {"json_pointer": "/status", "operator": "not_equals", "value": "pending"},
                    ],
                }
            ],
            "normalized_execution_projection": {
                "source_ref": projection_ref,
                "task_id": "TASK-FIXTURE",
                "unit_id": "SWU-FIXTURE-001",
                "current_unit": "SWU-FIXTURE-001",
                "admitted_frontier": ["SWU-FIXTURE-001", "SWU-FIXTURE-002"],
                "routes": [
                    {
                        "capability": "task-session",
                        "mode": "execute",
                        "target": "SWU-FIXTURE-001",
                        "write_scope": [],
                        "effects": ["rehearsal-only"],
                    }
                ],
                "request_budget": 1,
                "risk_ceiling": "read-only",
                "successor_policy": "expose-only",
                "successor_execution_allowed": False,
                "write_partitions": {
                    "material_writes": [],
                    "execution_outputs": [],
                    "transient_outputs": [],
                    "allowed_writes": [],
                    "protected_paths": ["fixture/target.json", "fixture/candidate.json"],
                },
                "runner": {
                    "ref": runner_ref,
                    "argv": [sys.executable, "fixture/consumer.py", "{stage}", "{rehearsal_root}"],
                    "cwd": ".",
                    "environment_names": ["PATH"],
                    "environment": {},
                    "mode": "no-effect-rehearsal",
                    "authority_role": "spellcraft-preacceptance-rehearsal",
                    "timeout_seconds": 30,
                },
                "schemas_and_locators": [
                    {
                        "schema_ref": schema_ref,
                        "canonical_locator": "fixture/schema.json",
                        "document_ref": projection_ref,
                        "json_pointer": "/kind",
                        "expected_json_type": "string",
                        "consumer_stage": "task_session_governance_runner",
                        "resolution_count": 1,
                        "allow_equivalent_path": False,
                    }
                ],
            },
            "runtime_receipt_derivations": derivations,
            "consumer_rehearsal": {
                "mode": "no-effect",
                "external_effects_allowed": False,
                "output_root_policy": "isolated-temporary-directory",
                "determinism_runs": 2,
                "protected_refs": [
                    self.exact_ref("fixture/target.json"),
                    self.exact_ref("fixture/candidate.json"),
                ],
                "stages": stages,
            },
            "requested_effect": {
                "effect_id": "replace-one-governance-target",
                "lifecycle_owner": "spellcraft",
                "human_authorization_provenance": "fixture-human-decision",
                "material_approval_owner": "spellcraft",
                "target_paths": ["fixture/target.json"],
                "authority_write_ceiling": [],
                "allowed_effects": ["request-generation-only"],
                "forbidden_effects": ["apply", "execution", "publication", "external-effect"],
                "postimage_lifecycle_state": "final",
                "renewed_acceptance_triggers": ["postimage-drift", "runner-drift"],
            },
            "reflection_adoption_ref": self.exact_ref("fixture/adoption.json"),
            "claim_ceiling": "Synthetic no-effect preacceptance fixture only.",
        }

    def write_manifest(self, manifest: dict[str, Any]) -> None:
        self.write_json("fixture/manifest.json", manifest)

    def refresh_ref(self, manifest: Any, relative: str) -> None:
        replacement = self.exact_ref(relative)
        if isinstance(manifest, dict):
            if manifest.get("path") == relative and set(manifest) == {
                "path",
                "sha256",
                "size_bytes",
            }:
                manifest.update(replacement)
            else:
                for value in manifest.values():
                    self.refresh_ref(value, relative)
        elif isinstance(manifest, list):
            for value in manifest:
                self.refresh_ref(value, relative)

    def run_rehearsal(self, manifest: dict[str, Any], output: str = "fixture/receipt.json"):
        self.write_manifest(manifest)
        command = [
            sys.executable,
            str(self.invoke / "scripts/preacceptance_closure.py"),
            "--repository-root",
            str(self.root),
            "rehearse",
            "--manifest",
            str(self.path("fixture/manifest.json")),
            "--output",
            str(self.path(output)),
        ]
        return subprocess.run(command, check=False, capture_output=True, text=True)

    def write_review(self, receipt_relative: str = "fixture/receipt.json") -> None:
        receipt = self.exact_ref(receipt_relative)
        manifest = self.exact_ref("fixture/manifest.json")
        receipt_document = json.loads(self.path(receipt_relative).read_text(encoding="utf-8"))
        review: dict[str, Any] = {
            "schema_version": "invoke.preacceptance-closure-review.v1",
            "review_id": "fixture-independent-review",
            "manifest_ref": manifest,
            "closure_receipt_ref": receipt,
            "closure_graph_digest": receipt_document["closure_graph_digest"],
            "reviewer": {
                "identity": "fixture-independent-reviewer",
                "role": "independent-preacceptance-review",
                "independent_from": ["spellcraft-preacceptance-rehearsal"],
            },
            "result": "pass",
            "checks": [
                {"check_id": check_id, "result": "pass", "detail": "verified"}
                for check_id in [
                    "final_postimages",
                    "execution_projection",
                    "consumer_closure",
                    "write_partition",
                    "runner_identity",
                    "schema_locator",
                    "runtime_derivation",
                    "requested_effect",
                    "reflection_adoption",
                    "no_effect_determinism",
                ]
            ],
            "authority_effect": "none",
            "claim_ceiling": "Independent synthetic review only.",
        }
        review["receipt_digest"] = canonical_digest(review)
        self.write_json("fixture/review.json", review)


class PreacceptanceClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = Fixture()

    def tearDown(self) -> None:
        self.fixture.cleanup()

    def mutate_case(self, case_id: str, manifest: dict[str, Any]) -> None:
        projection = manifest["normalized_execution_projection"]
        if case_id == "owner-provenance-conflation":
            manifest["requested_effect"]["material_approval_owner"] = "human-provenance"
        elif case_id == "pending-final-postimage":
            self.fixture.write_json("fixture/candidate.json", {"status": "pending"})
            self.fixture.refresh_ref(manifest, "fixture/candidate.json")
        elif case_id == "split-execution-projection":
            self.fixture.write_json("fixture/other-projection.json", {"kind": "execution-projection"})
            manifest["consumer_rehearsal"]["stages"][0]["projection_ref"] = self.fixture.exact_ref(
                "fixture/other-projection.json"
            )
        elif case_id == "frontier-budget-mismatch":
            projection["request_budget"] = 5
        elif case_id == "missing-admission-binding":
            del projection["risk_ceiling"]
        elif case_id == "double-rooted-locator":
            projection["schemas_and_locators"][0]["resolution_count"] = 2
        elif case_id == "scalar-queried-as-object":
            projection["schemas_and_locators"][0]["expected_json_type"] = "object"
        elif case_id == "exit-status-masking":
            manifest["consumer_rehearsal"]["stages"][0]["strict_exit_propagation"] = False
        elif case_id == "single-run-nondeterminism":
            manifest["consumer_rehearsal"]["determinism_runs"] = 1
        elif case_id == "equivalent-schema-wrong-locator":
            shutil.copy2(
                self.fixture.path("fixture/schema.json"),
                self.fixture.path("fixture/equivalent-schema.json"),
            )
            projection["schemas_and_locators"][0]["schema_ref"] = self.fixture.exact_ref(
                "fixture/equivalent-schema.json"
            )
        elif case_id == "downstream-receipt-schema-failure":
            self.fixture.write_json(
                "fixture/failing-schema.json",
                {"type": "object", "required": ["missing"]},
            )
            manifest["consumer_rehearsal"]["stages"][0]["schema_checks"] = [
                {
                    "document_ref": self.fixture.exact_ref("fixture/projection.json"),
                    "schema_ref": self.fixture.exact_ref("fixture/failing-schema.json"),
                }
            ]
        elif case_id == "missing-causal-receipt-derivation":
            manifest["runtime_receipt_derivations"] = [
                item
                for item in manifest["runtime_receipt_derivations"]
                if item["receipt_class"] != "execution_ticket"
            ]
        elif case_id == "tested-runner-not-authorized-runner":
            shutil.copy2(
                self.fixture.path("fixture/consumer.py"),
                self.fixture.path("fixture/other-consumer.py"),
            )
            stage = manifest["consumer_rehearsal"]["stages"][6]
            stage["exercised_runner_ref"] = self.fixture.exact_ref("fixture/other-consumer.py")
            stage["environment"]["EXERCISED_RUNNER"] = "fixture/other-consumer.py"
        elif case_id == "machine-write-exceeds-owner-ceiling":
            projection["write_partitions"]["execution_outputs"] = ["fixture/output.json"]
            projection["write_partitions"]["allowed_writes"] = ["fixture/output.json"]
        elif case_id == "successor-executed-in-current-unit":
            projection["successor_execution_allowed"] = True
        elif case_id == "create-target-hygiene-failure":
            self.fixture.write_text("fixture/candidate.json", '{"status":"final"}  ')
            self.fixture.refresh_ref(manifest, "fixture/candidate.json")
        else:
            raise AssertionError(f"unknown case {case_id}")

    def test_positive_rehearsal_is_two_run_deterministic_and_idempotent(self) -> None:
        manifest = self.fixture.base_manifest()
        first = self.fixture.run_rehearsal(manifest)
        self.assertEqual(first.returncode, 0, first.stderr)
        first_bytes = self.fixture.path("fixture/receipt.json").read_bytes()
        second = self.fixture.run_rehearsal(manifest)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first_bytes, self.fixture.path("fixture/receipt.json").read_bytes())
        receipt = json.loads(first_bytes)
        self.assertEqual(receipt["result"], "pass")
        self.assertTrue(receipt["determinism"]["byte_stable"])
        self.assertEqual([item["stage_id"] for item in receipt["stage_results"]], STAGES)

    def test_all_sixteen_negative_cases_fail_before_request_generation(self) -> None:
        cases = json.loads(NEGATIVE_CASES.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(len(cases), 16)
        for index, case in enumerate(cases, 1):
            with self.subTest(case_id=case["case_id"]):
                manifest = copy.deepcopy(self.fixture.base_manifest())
                self.mutate_case(case["case_id"], manifest)
                output = f"fixture/negative-{index}.json"
                completed = self.fixture.run_rehearsal(manifest, output)
                self.assertNotEqual(completed.returncode, 0, completed.stderr)
                receipt = json.loads(self.fixture.path(output).read_text(encoding="utf-8"))
                self.assertEqual(receipt["result"], "block")
                joined = "\n".join(receipt["blockers"])
                self.assertIn(case["expected_blocker"], joined)

    def test_request_emission_requires_passing_independent_review(self) -> None:
        manifest = self.fixture.base_manifest()
        completed = self.fixture.run_rehearsal(manifest)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.fixture.write_review()
        review = json.loads(self.fixture.path("fixture/review.json").read_text(encoding="utf-8"))
        review["result"] = "block"
        review["checks"][0]["result"] = "block"
        review["receipt_digest"] = canonical_digest(
            {key: value for key, value in review.items() if key != "receipt_digest"}
        )
        self.fixture.write_json("fixture/blocked-review.json", review)
        command = [
            sys.executable,
            str(self.fixture.invoke / "scripts/preacceptance_closure.py"),
            "--repository-root",
            str(self.fixture.root),
            "emit-request",
            "--manifest",
            str(self.fixture.path("fixture/manifest.json")),
            "--receipt",
            str(self.fixture.path("fixture/receipt.json")),
            "--review",
            str(self.fixture.path("fixture/blocked-review.json")),
            "--adoption",
            str(self.fixture.path("fixture/adoption.json")),
            "--base-request",
            str(self.fixture.path("fixture/base-request.json")),
            "--output",
            str(self.fixture.path("fixture/owner-request-v2.json")),
        ]
        blocked = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse(self.fixture.path("fixture/owner-request-v2.json").exists())

        self.fixture.write_review()
        command[command.index(str(self.fixture.path("fixture/blocked-review.json")))] = str(
            self.fixture.path("fixture/review.json")
        )
        emitted = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(emitted.returncode, 0, emitted.stderr)
        request = json.loads(
            self.fixture.path("fixture/owner-request-v2.json").read_text(encoding="utf-8")
        )
        self.assertEqual(request["emission_gate"], "pass")
        self.assertEqual(request["authority_effect"], "none")

    def test_incomplete_consumer_invocations_fail_at_the_exact_stage(self) -> None:
        self.fixture.write_text(
            "fixture/invocation-guard.py",
            """#!/usr/bin/env python3
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--family", required=True)
parser.add_argument("--fixture", required=True)
parser.add_argument("--schema", required=True)
parser.parse_args()
if not os.environ.get("INVOKE_CANDIDATE_SCHEMA"):
    raise SystemExit(19)
""",
        )
        required_argv = [
            sys.executable,
            "fixture/invocation-guard.py",
            "--family",
            "commit-resume",
            "--fixture",
            "fixture/projection.json",
            "--schema",
            "fixture/schema.json",
        ]
        cases = {
            "missing-family": ["--family", "commit-resume"],
            "missing-fixture": ["--fixture", "fixture/projection.json"],
            "missing-schema": ["--schema", "fixture/schema.json"],
        }
        for index, (case_id, removed) in enumerate(cases.items(), 1):
            with self.subTest(case_id=case_id):
                manifest = copy.deepcopy(self.fixture.base_manifest())
                stage = manifest["consumer_rehearsal"]["stages"][0]
                guard_ref = self.fixture.exact_ref("fixture/invocation-guard.py")
                stage["runner_ref"] = guard_ref
                stage["exercised_runner_ref"] = guard_ref
                stage["argv"] = required_argv[:]
                position = stage["argv"].index(removed[0])
                del stage["argv"][position : position + 2]
                stage["environment"] = {
                    "INVOKE_CANDIDATE_SCHEMA": "fixture/schema.json"
                }
                completed = self.fixture.run_rehearsal(
                    manifest, f"fixture/incomplete-invocation-{index}.json"
                )
                self.assertNotEqual(completed.returncode, 0, completed.stderr)
                receipt = json.loads(
                    self.fixture.path(
                        f"fixture/incomplete-invocation-{index}.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(receipt["result"], "block")
                self.assertIn(
                    "consumer stage failed with exit",
                    "\n".join(receipt["blockers"]),
                )
                self.assertEqual(
                    [item["stage_id"] for item in receipt["stage_results"]],
                    [STAGES[0]],
                )

        with self.subTest(case_id="missing-fixed-environment"):
            manifest = copy.deepcopy(self.fixture.base_manifest())
            stage = manifest["consumer_rehearsal"]["stages"][0]
            guard_ref = self.fixture.exact_ref("fixture/invocation-guard.py")
            stage["runner_ref"] = guard_ref
            stage["exercised_runner_ref"] = guard_ref
            stage["argv"] = required_argv
            stage["environment"] = {}
            completed = self.fixture.run_rehearsal(
                manifest, "fixture/incomplete-invocation-environment.json"
            )
            self.assertNotEqual(completed.returncode, 0, completed.stderr)
            receipt = json.loads(
                self.fixture.path(
                    "fixture/incomplete-invocation-environment.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(receipt["result"], "block")
            self.assertEqual(receipt["stage_results"][0]["exit_code"], 19)

    def test_actual_consumer_entrypoints_are_the_required_public_boundaries(self) -> None:
        self.assertEqual(len(REAL_CONSUMER_ENTRYPOINTS), len(STAGES))
        missing = [
            path for path in REAL_CONSUMER_ENTRYPOINTS if not (REPOSITORY_ROOT / path).is_file()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

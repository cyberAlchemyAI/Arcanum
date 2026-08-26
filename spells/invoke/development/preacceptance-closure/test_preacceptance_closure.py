#!/usr/bin/env python3
"""Regression tests for Invoke preacceptance consumer closure."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


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
    "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json",
    "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
    "arcanum/arcana/continuation-router/scripts/work_pack_route.py",
]

REAL_DRIVER_ENTRYPOINTS = [
    "arcanum/spells/invoke/development/run_material_package_fixtures.py",
    "arcanum/spells/invoke/development/run_material_package_fixtures.py",
    "arcanum/spells/work-pack-readiness-audit/development/test_work_pack_readiness_v2.py",
    "arcanum/spells/task-session-until-blocker/development/validate-chain-v2.py",
    "arcanum/arcana/task-session/development/test_fast_execution_entry_guard.py",
    "arcanum/arcana/task-session/development/validate-mutation-admission.py",
    "arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py",
    "arcanum/arcana/task-session/development/test-plan-once-material-controller.py",
    "arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py",
    "arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py",
    "arcanum/arcana/continuation-router/development/validate-work-pack-route-fixtures.py",
]


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def load_module(path: Path, module_name: str) -> Any:
    specification = importlib.util.spec_from_file_location(module_name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load integration helper: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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
        wpra_schema_target = (
            self.root / "arcanum/spells/work-pack-readiness-audit/schemas"
        )
        wpra_schema_target.mkdir(parents=True, exist_ok=True)
        for schema in (
            REPOSITORY_ROOT / "arcanum/spells/work-pack-readiness-audit/schemas"
        ).glob("*.json"):
            shutil.copy2(schema, wpra_schema_target / schema.name)
        chain_schema_target = (
            self.root / "arcanum/spells/task-session-until-blocker/schemas"
        )
        chain_schema_target.mkdir(parents=True, exist_ok=True)
        for schema in (
            REPOSITORY_ROOT / "arcanum/spells/task-session-until-blocker/schemas"
        ).glob("*.json"):
            shutil.copy2(schema, chain_schema_target / schema.name)
        router_schema_target = (
            self.root / "arcanum/arcana/continuation-router/schemas"
        )
        router_schema_target.mkdir(parents=True, exist_ok=True)
        for schema in (
            REPOSITORY_ROOT / "arcanum/arcana/continuation-router/schemas"
        ).glob("*.json"):
            shutil.copy2(schema, router_schema_target / schema.name)
        support_paths = [
            *REAL_CONSUMER_ENTRYPOINTS,
            "arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py",
            "arcanum/spells/invoke/development/run_material_package_fixtures.py",
            "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
            "arcanum/spells/invoke/development/fixtures/refresh-material-handoff-cases.json",
            "arcanum/spells/invoke/schemas/material-package.schema.json",
            "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
            "arcanum/spells/work-pack-readiness-audit/development/test_work_pack_readiness_v2.py",
            "arcanum/spells/task-session-until-blocker/development/validate-chain-v2.py",
            "arcanum/arcana/continuation-router/development/validate-work-pack-route-fixtures.py",
            "arcanum/arcana/continuation-router/development/work-pack-route-fixtures/admission-cases.json",
            "arcanum/spells/work-pack-readiness-audit/scripts/plan_semantics.py",
            "arcanum/spells/task-session-until-blocker/scripts/task_session_until_blocker_runtime_paths.py",
            "arcanum/arcana/continuation-router/scripts/continuation_router_runtime_paths.py",
            "arcanum/arcana/continuation-router/scripts/admit-work-pack-route.py",
            "arcanum/spells/implementation-readiness/scripts/execution_contracts.py",
            "arcanum/arcana/task-session/schemas/precloseout-execution-receipt.schema.json",
            "arcanum/arcana/task-session/continuity.schema.json",
            "arcanum/arcana/continuation-router/schemas/work-pack-route-admission.schema.json",
        ]
        for relative in support_paths:
            source = REPOSITORY_ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        shutil.copytree(
            REPOSITORY_ROOT / "arcanum/arcana/task-session",
            self.root / "arcanum/arcana/task-session",
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("invoke-runs", "__pycache__"),
        )
        shutil.copytree(
            REPOSITORY_ROOT / "arcanum/spells/implementation-readiness",
            self.root / "arcanum/spells/implementation-readiness",
            dirs_exist_ok=True,
        )
        (self.root / "fixture").mkdir()
        governance_fixtures = load_module(
            self.root
            / "arcanum/arcana/task-session/development/"
            "validate-governance-runner.py",
            "preacceptance_projection_bound_governance_fixtures",
        )
        lifecycle_scopes = [
            {
                "path": "records/lifecycle-status.json",
                "owner_capability": "invoke",
                "write_class": "lifecycle-synchronization",
            },
            {
                "path": "records/precloseout.json",
                "owner_capability": "task-session",
                "write_class": "precloseout-receipt",
            },
            {
                "path": "records/owner-closeout.json",
                "owner_capability": "invoke",
                "write_class": "owner-closeout-receipt",
            },
            {
                "path": "records/continuation.json",
                "owner_capability": "continuation-router",
                "write_class": "continuation-receipt",
            },
            {
                "path": ".runtime/continuity.json",
                "owner_capability": "task-session",
                "write_class": "continuity-cursor",
            },
        ]
        with tempfile.TemporaryDirectory(
            prefix="preacceptance-governance-build-"
        ) as build_root:
            governance_repository = governance_fixtures.plan_fast_entry_scenario(
                Path(build_root),
                self.root / "arcanum/arcana/task-session",
                self.root / "arcanum/arcana/task-session",
                "projection-bound",
                terminal_in_route_scope=True,
                output_only=True,
                lifecycle_owner_scopes=lifecycle_scopes,
            )
            shutil.copytree(governance_repository, self.root, dirs_exist_ok=True)
        governance_request = json.loads(
            self.path("scenario/request.json").read_text(encoding="utf-8")
        )
        fast_entry_request = json.loads(
            self.path("scenario/fast-entry-request.json").read_text(encoding="utf-8")
        )
        selected_route = fast_entry_request["execution_binding"]["current_route"]
        self.execution_identity = {
            "task_id": governance_request["task_id"],
            "unit_id": selected_route["frontier_swu"],
            "current_unit": selected_route["frontier_swu"],
            "admitted_frontier": [selected_route["frontier_swu"]],
            "routes": [
                {
                    "capability": selected_route["capability"],
                    "mode": selected_route["mode"],
                    "target": selected_route["frontier_swu"],
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
        }
        self.write_json("fixture/target.json", {"status": "baseline"})
        self.write_json("fixture/candidate.json", {"status": "final"})
        self.write_json(
            "fixture/projection.json",
            {
                "kind": "execution-projection",
                "preacceptance_identity": self.execution_identity,
                "governance_prepare_rehearsal": {
                    "schema_version": (
                        "invoke.preacceptance-governance-prepare-rehearsal.v1"
                    ),
                    "request_ref": self.exact_ref("scenario/request.json"),
                    "selected_route": selected_route,
                    "route_scope_partition": governance_request[
                        "fast_execution_entry"
                    ]["route_scope_partition"],
                    "run_dir": "rehearsal/task-session-run",
                },
            },
        )
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
        self.write_text("fixture/negative-regression.log", "canonical negative regression: pass\n")
        self.write_text("fixture/cross-capability-regression.log", "canonical cross-capability regression: pass\n")
        self.write_regression_receipt(
            "fixture/negative-regression.json",
            "fixture/negative-regression.log",
            [sys.executable, "test_preacceptance_closure.py", "negative-cases"],
        )
        self.write_regression_receipt(
            "fixture/cross-capability-regression.json",
            "fixture/cross-capability-regression.log",
            [sys.executable, "test_preacceptance_closure.py", "cross-capability"],
        )
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

    def write_regression_receipt(
        self, relative: str, transcript: str, argv: list[str]
    ) -> None:
        receipt: dict[str, Any] = {
            "schema_version": "invoke.preacceptance-regression-execution.v1",
            "runner_ref": self.exact_ref(
                "arcanum/spells/invoke/scripts/preacceptance_closure.py"
            ),
            "argv": argv,
            "exit_code": 0,
            "transcript_ref": self.exact_ref(transcript),
            "result": "pass",
        }
        receipt["receipt_digest"] = canonical_digest(receipt)
        self.write_json(relative, receipt)

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
        adapter_path = (
            "arcanum/spells/invoke/development/preacceptance-closure/"
            "real_consumer_rehearsal.py"
        )
        adapter_ref = self.exact_ref(adapter_path)
        projection_ref = self.exact_ref("fixture/projection.json")
        schema_ref = self.exact_ref("fixture/schema.json")
        stages = []
        for stage, consumer, driver in zip(
            STAGES, REAL_CONSUMER_ENTRYPOINTS, REAL_DRIVER_ENTRYPOINTS, strict=True
        ):
            consumer_ref = self.exact_ref(consumer)
            driver_ref = self.exact_ref(driver)
            runner_ref = adapter_ref
            argv = [
                sys.executable,
                adapter_path,
                "--stage",
                stage,
                "--consumer",
                consumer,
                "--driver",
                driver,
                "--projection",
                projection_ref["path"],
                "--rehearsal-root",
                "{rehearsal_root}",
            ]
            stages.append(
                {
                    "stage_id": stage,
                    "projection_ref": projection_ref,
                    "runner_ref": runner_ref,
                    "driver_ref": driver_ref,
                    "exercised_runner_ref": consumer_ref,
                    "argv": argv,
                    "cwd": ".",
                    "environment_names": ["PATH"],
                    "environment": {
                        "PREACCEPTANCE_PROJECTION_REF": projection_ref["path"]
                    },
                    "timeout_seconds": (
                        90 if stage == "task_session_governance_runner" else 30
                    ),
                    "strict_exit_propagation": True,
                    "allowed_effect": "isolated-rehearsal-output-only",
                    "schema_checks": [
                        {"document_ref": projection_ref, "schema_ref": schema_ref}
                    ],
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
                **copy.deepcopy(self.execution_identity),
                "runner": {
                    "ref": self.exact_ref(
                        "arcanum/arcana/task-session/scripts/"
                        "task-session-governance-runner.py"
                    ),
                    "argv": [
                        sys.executable,
                        "arcanum/arcana/task-session/scripts/"
                        "task-session-governance-runner.py",
                        "prepare",
                        "--repo-root",
                        ".",
                    ],
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
                "task_session_closeout_contract": {
                    "receipt_profile": "precloseout-execution-v1",
                    "precloseout_execution_schema_ref": self.exact_ref(
                        "arcanum/arcana/task-session/schemas/"
                        "precloseout-execution-receipt.schema.json"
                    ),
                    "expected_owner_receipt_schema_ref": self.exact_ref(
                        "arcanum/spells/invoke/schemas/"
                        "precloseout-refresh-closeout-receipt.schema.json"
                    ),
                    "declared_owner_receipt_schema_identity": (
                        "invoke.precloseout-refresh-closeout-receipt.v1"
                    ),
                    "final_terminal_schema_ref": self.exact_ref(
                        "arcanum/arcana/task-session/schemas/"
                        "governance-terminal-receipt.schema.json"
                    ),
                    "continuity_schema_ref": self.exact_ref(
                        "arcanum/arcana/task-session/continuity.schema.json"
                    ),
                    "continuation_router_schema_ref": self.exact_ref(
                        "arcanum/arcana/continuation-router/schemas/"
                        "work-pack-route-admission.schema.json"
                    ),
                },
            },
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
        attestation: dict[str, Any] = {
            "schema_version": "invoke.review-attestation.v1",
            "attestor_identity": "fixture-review-attestor",
            "attestor_role": "closure-bound-review-attestor",
            "declared_separation_from": ["spellcraft-preacceptance-rehearsal"],
            "manifest_ref": manifest,
            "closure_receipt_ref": receipt,
            "review_method": "independent-agent-dispatch-declared",
            "result": "completed",
            "authority_effect": "none",
        }
        attestation["receipt_digest"] = canonical_digest(attestation)
        self.write_json("fixture/review-attestation.json", attestation)
        review: dict[str, Any] = {
            "schema_version": "invoke.preacceptance-closure-review.v1",
            "review_id": "fixture-independent-review",
            "manifest_ref": manifest,
            "closure_receipt_ref": receipt,
            "closure_graph_digest": receipt_document["closure_graph_digest"],
            "reviewer": {
                "identity": "fixture-review-attestor",
                "role": "closure-bound-review-attestor",
                "declared_separation_from": ["spellcraft-preacceptance-rehearsal"],
                "attestation_ref": self.exact_ref("fixture/review-attestation.json"),
            },
            "result": "pass",
            "checks": [
                {
                    "check_id": check_id,
                    "result": "pass",
                    "detail": "verified",
                    "evidence_refs": [manifest, receipt],
                }
                for check_id in [
                    "final_postimages",
                    "execution_projection",
                    "consumer_closure",
                    "write_partition",
                    "runner_identity",
                    "schema_locator",
                    "stage_binding",
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
        elif case_id == "split-source-semantics":
            source = json.loads(
                self.fixture.path("fixture/projection.json").read_text(encoding="utf-8")
            )
            source["preacceptance_identity"]["current_unit"] = "SWU-OTHER"
            self.fixture.write_json("fixture/projection.json", source)
            self.fixture.refresh_ref(manifest, "fixture/projection.json")
        elif case_id == "projection-not-in-stage-invocation":
            stage = manifest["consumer_rehearsal"]["stages"][0]
            stage["environment"].pop("PREACCEPTANCE_PROJECTION_REF")
            projection_index = stage["argv"].index("--projection")
            del stage["argv"][projection_index : projection_index + 2]
        elif case_id == "help-only-consumer":
            manifest["consumer_rehearsal"]["stages"][0]["argv"].append("--help")
        elif case_id == "noncanonical-functional-driver":
            stage = manifest["consumer_rehearsal"]["stages"][0]
            old_driver = stage["driver_ref"]["path"]
            stage["driver_ref"] = self.fixture.exact_ref("fixture/consumer.py")
            stage["argv"] = [
                "fixture/consumer.py" if value == old_driver else value
                for value in stage["argv"]
            ]
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
        elif case_id == "generic-stage-consumer":
            manifest["consumer_rehearsal"]["stages"][0][
                "exercised_runner_ref"
            ] = self.fixture.exact_ref("fixture/consumer.py")
        elif case_id == "skipped-stage":
            manifest["consumer_rehearsal"]["stages"].pop()
        elif case_id == "missing-owner-schema-ref":
            del projection["task_session_closeout_contract"][
                "expected_owner_receipt_schema_ref"
            ]
        elif case_id == "stale-owner-schema-hash":
            projection["task_session_closeout_contract"][
                "expected_owner_receipt_schema_ref"
            ]["sha256"] = "0" * 64
        elif case_id == "wrong-owner-schema-identity":
            owner_path = (
                "arcanum/spells/invoke/schemas/"
                "precloseout-refresh-closeout-receipt.schema.json"
            )
            schema = json.loads(
                self.fixture.path(owner_path).read_text(encoding="utf-8")
            )
            schema["properties"]["schema_version"]["const"] = "wrong.identity.v1"
            self.fixture.write_json(owner_path, schema)
            projection["task_session_closeout_contract"][
                "expected_owner_receipt_schema_ref"
            ] = self.fixture.exact_ref(owner_path)
            manifest["consumer_rehearsal"]["stages"][8][
                "exercised_runner_ref"
            ] = self.fixture.exact_ref(owner_path)
        elif case_id == "accepted-artifacts-without-bundle":
            candidate = {
                "status": "final",
                "accepted_artifacts": [self.fixture.exact_ref("fixture/target.json")],
            }
            self.fixture.write_json("fixture/candidate.json", candidate)
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

    def test_nested_adoption_reference_drift_blocks_before_rehearsal(self) -> None:
        manifest = self.fixture.base_manifest()
        self.fixture.write_text(
            "fixture/negative-regression.log", "tampered transcript\n"
        )
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/nested-adoption-drift-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/nested-adoption-drift-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn(
            "negative-regression-artifact/transcript_ref digest mismatch: "
            "fixture/negative-regression.log",
            receipt["blockers"],
        )

    def test_effect_monitor_blocks_transient_restored_repository_write(self) -> None:
        manifest = self.fixture.base_manifest()
        adapter = (
            "arcanum/spells/invoke/development/preacceptance-closure/"
            "real_consumer_rehearsal.py"
        )
        path = self.fixture.path(adapter)
        content = path.read_text(encoding="utf-8")
        marker = '\nif __name__ == "__main__":\n'
        injection = (
            '\n_transient = Path("fixture/transient-write.txt")\n'
            '_transient.write_text("temporary", encoding="utf-8")\n'
            '_transient.unlink()\n'
        )
        path.write_text(content.replace(marker, injection + marker), encoding="utf-8")
        self.fixture.refresh_ref(manifest, adapter)
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/transient-write-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/transient-write-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("E21_EFFECT_MONITOR observed a denied effect", receipt["blockers"])

    def test_effect_monitor_blocks_network_attempt(self) -> None:
        manifest = self.fixture.base_manifest()
        adapter = (
            "arcanum/spells/invoke/development/preacceptance-closure/"
            "real_consumer_rehearsal.py"
        )
        path = self.fixture.path(adapter)
        content = path.read_text(encoding="utf-8")
        marker = '\nif __name__ == "__main__":\n'
        injection = (
            "\nimport socket as _socket\n"
            '_socket.socket().connect(("127.0.0.1", 9))\n'
        )
        path.write_text(content.replace(marker, injection + marker), encoding="utf-8")
        self.fixture.refresh_ref(manifest, adapter)
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/network-attempt-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/network-attempt-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(receipt["write_observation"]["external_effects_observed"])
        self.assertIn("E21_EFFECT_MONITOR observed a denied effect", receipt["blockers"])

    def test_stdout_nondeterminism_blocks(self) -> None:
        manifest = self.fixture.base_manifest()
        adapter = (
            "arcanum/spells/invoke/development/preacceptance-closure/"
            "real_consumer_rehearsal.py"
        )
        path = self.fixture.path(adapter)
        content = path.read_text(encoding="utf-8")
        marker = '\nif __name__ == "__main__":\n'
        injection = '\nprint(__import__("time").time_ns())\n'
        path.write_text(content.replace(marker, injection + marker), encoding="utf-8")
        self.fixture.refresh_ref(manifest, adapter)
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/stdout-nondeterminism-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/stdout-nondeterminism-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(receipt["determinism"]["byte_stable"])
        self.assertIn(
            "E09_NONDETERMINISM rehearsal result changed across two runs",
            receipt["blockers"],
        )

    def test_governance_stage_requires_projection_bound_request(self) -> None:
        manifest = self.fixture.base_manifest()
        projection_path = self.fixture.path("fixture/projection.json")
        projection = json.loads(projection_path.read_text(encoding="utf-8"))
        del projection["governance_prepare_rehearsal"]
        self.fixture.write_json("fixture/projection.json", projection)
        self.fixture.refresh_ref(manifest, "fixture/projection.json")
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/unbound-governance-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/unbound-governance-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(
            any(
                blocker.startswith("E03_SPLIT_PROJECTION")
                for blocker in receipt["blockers"]
            ),
            receipt["blockers"],
        )

    def test_generated_task_session_runner_is_exact_deployment_surface(self) -> None:
        generated_runner = (
            ".agents/skills/task-session/scripts/"
            "task-session-governance-runner.py"
        )
        shutil.copytree(
            self.fixture.path("arcanum/arcana/task-session"),
            self.fixture.path(".agents/skills/task-session"),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            self.fixture.path("arcanum/spells/implementation-readiness"),
            self.fixture.path(".agents/skills/implementation-readiness"),
            dirs_exist_ok=True,
        )
        manifest = self.fixture.base_manifest()
        governance = manifest["consumer_rehearsal"]["stages"][6]
        canonical_runner = governance["exercised_runner_ref"]["path"]
        governance["exercised_runner_ref"] = self.fixture.exact_ref(
            generated_runner
        )
        governance["argv"] = [
            generated_runner if value == canonical_runner else value
            for value in governance["argv"]
        ]
        projection_runner = manifest["normalized_execution_projection"]["runner"]
        projection_runner["ref"] = self.fixture.exact_ref(generated_runner)
        projection_runner["argv"] = [
            generated_runner if value == canonical_runner else value
            for value in projection_runner["argv"]
        ]
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/generated-runner-receipt.json"
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        receipt = json.loads(
            self.fixture.path("fixture/generated-runner-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(receipt["result"], "pass")

    def test_real_cross_capability_preparation_and_closeout_chain(self) -> None:
        task_session_root = REPOSITORY_ROOT / "arcanum/arcana/task-session"
        governance_fixtures = load_module(
            task_session_root / "development/validate-governance-runner.py",
            "preacceptance_task_session_governance_fixtures",
        )
        invoke_closeout = load_module(
            REPOSITORY_ROOT
            / "arcanum/spells/invoke/development/"
            "validate-precloseout-refresh-closeout.py",
            "preacceptance_invoke_closeout_validator",
        )

        with tempfile.TemporaryDirectory(
            prefix="preacceptance-cross-capability-"
        ) as raw:
            integration_root = Path(raw)
            repository = governance_fixtures.scenario(
                integration_root,
                task_session_root,
                task_session_root,
                "cross-capability",
            )
            schema_paths = (
                "arcanum/arcana/task-session/schemas/"
                "precloseout-execution-receipt.schema.json",
                "arcanum/arcana/task-session/schemas/"
                "governance-terminal-receipt.schema.json",
                "arcanum/spells/invoke/schemas/"
                "precloseout-refresh-closeout-receipt.schema.json",
            )
            for relative in schema_paths:
                source = REPOSITORY_ROOT / relative
                target = repository / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            request_path = repository / "scenario/request.json"
            request = json.loads(request_path.read_text(encoding="utf-8"))
            request["closeout_contract"] = {
                "required_owner_capabilities": ["invoke"],
                "continuation_policy": "emit-cursor-never-execute-successor",
                "terminal_receipt_path": (
                    "project/runs/synthetic/final-terminal-receipt.json"
                ),
                "receipt_profile": "precloseout-execution-v1",
                "precloseout_execution_receipt_path": (
                    "project/work-packs/synthetic/results/"
                    "precloseout-execution-receipt.json"
                ),
                "precloseout_execution_schema_ref": governance_fixtures.exact_ref(
                    repository, repository / schema_paths[0]
                ),
                "expected_owner_receipt_path": (
                    "project/work-packs/synthetic/closeout/"
                    "invoke-refresh-receipt.json"
                ),
                "expected_owner_receipt_schema_ref": governance_fixtures.exact_ref(
                    repository, repository / schema_paths[2]
                ),
                "final_terminal_schema_ref": governance_fixtures.exact_ref(
                    repository, repository / schema_paths[1]
                ),
            }
            governance_fixtures.write_json(request_path, request)

            prepare_command = governance_fixtures.runner_command(
                repository, "prepare", request="scenario/request.json"
            )
            code, payload, stderr = governance_fixtures.invoke(prepare_command)
            self.assertEqual(code, 0, stderr)
            self.assertEqual(payload.get("result"), "pass")
            self.assertEqual(payload.get("current_phase"), "ticketed")
            ticket = json.loads(
                (repository / "runs/run-1/execution-ticket.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(ticket["closeout_contract"], request["closeout_contract"])

            task_identity = {
                "task_id": request["task_id"],
                "run_id": request["run_id"],
                "swu_id": request["swu_id"],
                "attempt_id": "attempt-synthetic-001",
                "idempotency_key": request["idempotency_key"],
            }
            source_path = repository / request["closeout_contract"][
                "precloseout_execution_receipt_path"
            ]
            governance_fixtures.write_json(
                source_path,
                {
                    "schema_version": (
                        "task-session.precloseout-execution-receipt.v1"
                    ),
                    "task_identity": task_identity,
                    "result": "pass",
                },
            )
            source_precloseout = {
                "receipt_ref": governance_fixtures.exact_ref(
                    repository, source_path
                ),
                "schema_ref": request["closeout_contract"][
                    "precloseout_execution_schema_ref"
                ],
                "task_identity": task_identity,
            }
            validation_inventory = []
            for index, kind in enumerate(
                (
                    "source-precloseout",
                    "material-reconciliation",
                    "target-validation",
                ),
                1,
            ):
                evidence_path = repository / f"project/evidence/{kind}.json"
                governance_fixtures.write_json(
                    evidence_path, {"kind": kind, "result": "pass"}
                )
                validation_inventory.append(
                    {
                        "validation_id": f"synthetic-validation-{index}",
                        "kind": kind,
                        "result": "pass",
                        "evidence_ref": governance_fixtures.exact_ref(
                            repository, evidence_path
                        ),
                    }
                )
            closeout_output = {
                "path": request["closeout_contract"][
                    "expected_owner_receipt_path"
                ]
            }
            owner_receipt = {
                "schema_version": (
                    "invoke.precloseout-refresh-closeout-receipt.v1"
                ),
                "receipt_id": "invoke-synthetic-closeout-001",
                "owner_identity": {
                    "capability": "invoke",
                    "mode": "refresh",
                    "mutation_mode": "apply-approved",
                    "activation_source": "delegated",
                    "subject": "invoke:refresh:synthetic-integration",
                },
                "task_identity": task_identity,
                "precloseout_source": source_precloseout,
                "closeout_output": closeout_output,
                "validation_inventory": validation_inventory,
                "result": "pass",
                "final_owner_write": {
                    "write_class": "invoke-closeout-receipt",
                    "owner_capability": "invoke",
                    "completed": True,
                    "output_ref": closeout_output,
                },
            }
            owner_receipt["receipt_digest"] = (
                invoke_closeout.receipt_projection_digest(owner_receipt)
            )
            owner_schema = json.loads(
                (repository / schema_paths[2]).read_text(encoding="utf-8")
            )
            self.assertEqual(
                list(Draft202012Validator(owner_schema).iter_errors(owner_receipt)),
                [],
            )
            self.assertEqual(
                invoke_closeout.semantic_errors(
                    owner_receipt, source_precloseout
                ),
                [],
            )

        downstream_commands = (
            [
                sys.executable,
                str(
                    task_session_root
                    / "development/validate-governance-run-contracts.py"
                ),
                "--task-session-dir",
                str(task_session_root),
            ],
            [
                sys.executable,
                str(
                    REPOSITORY_ROOT
                    / "arcanum/arcana/continuation-router/development/"
                    "validate-work-pack-route-fixtures.py"
                ),
            ],
        )
        for command in downstream_commands:
            completed = subprocess.run(
                command,
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                completed.returncode,
                0,
                f"command={command!r}\nstdout={completed.stdout}\nstderr={completed.stderr}",
            )

    def test_all_negative_cases_fail_before_request_generation(self) -> None:
        cases = json.loads(NEGATIVE_CASES.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(len(cases), 25)
        for index, case in enumerate(cases, 1):
            with self.subTest(case_id=case["case_id"]):
                try:
                    manifest = copy.deepcopy(self.fixture.base_manifest())
                    self.mutate_case(case["case_id"], manifest)
                    output = f"fixture/negative-{index}.json"
                    completed = self.fixture.run_rehearsal(manifest, output)
                    self.assertNotEqual(completed.returncode, 0, completed.stderr)
                    receipt = json.loads(
                        self.fixture.path(output).read_text(encoding="utf-8")
                    )
                    self.assertEqual(receipt["result"], "block")
                    joined = "\n".join(receipt["blockers"])
                    self.assertIn(case["expected_blocker"], joined)
                finally:
                    self.fixture.cleanup()
                    self.fixture = Fixture()

    def test_request_emission_requires_passing_review_attestation(self) -> None:
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
        forged = json.loads(
            self.fixture.path("fixture/review.json").read_text(encoding="utf-8")
        )
        forged["reviewer"]["identity"] = "Mallory"
        forged["reviewer"].pop("attestation_ref")
        for check in forged["checks"]:
            check.pop("evidence_refs")
            check["detail"] = "asserted without evidence"
        forged["receipt_digest"] = canonical_digest(
            {key: value for key, value in forged.items() if key != "receipt_digest"}
        )
        self.fixture.write_json("fixture/forged-review.json", forged)
        command[command.index(str(self.fixture.path("fixture/blocked-review.json")))] = str(
            self.fixture.path("fixture/forged-review.json")
        )
        forged_result = subprocess.run(
            command, check=False, capture_output=True, text=True
        )
        self.assertNotEqual(forged_result.returncode, 0)
        self.assertFalse(self.fixture.path("fixture/owner-request-v2.json").exists())

        self.fixture.write_review()
        command[command.index(str(self.fixture.path("fixture/forged-review.json")))] = str(
            self.fixture.path("fixture/review.json")
        )
        emitted = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(emitted.returncode, 0, emitted.stderr)
        request = json.loads(
            self.fixture.path("fixture/owner-request-v2.json").read_text(encoding="utf-8")
        )
        self.assertEqual(request["emission_gate"], "pass")
        self.assertEqual(request["authority_effect"], "none")

        validate = [
            sys.executable,
            str(self.fixture.invoke / "scripts/preacceptance_closure.py"),
            "--repository-root",
            str(self.fixture.root),
            "validate-request",
            "--request",
            str(self.fixture.path("fixture/owner-request-v2.json")),
        ]
        validated = subprocess.run(validate, check=False, capture_output=True, text=True)
        self.assertEqual(validated.returncode, 0, validated.stderr)

        hand_authored = copy.deepcopy(request)
        hand_authored["preacceptance_closure"]["closure_receipt_ref"] = (
            hand_authored["preacceptance_closure"]["adoption_ref"]
        )
        hand_authored["request_digest"] = canonical_digest(
            {
                key: value
                for key, value in hand_authored.items()
                if key != "request_digest"
            }
        )
        self.fixture.write_json("fixture/hand-authored-v2.json", hand_authored)
        validate[-1] = str(self.fixture.path("fixture/hand-authored-v2.json"))
        bypass = subprocess.run(validate, check=False, capture_output=True, text=True)
        self.assertNotEqual(bypass.returncode, 0)
        self.assertIn("owner request emission proof is invalid", bypass.stderr)

        validate[-1] = str(self.fixture.path("fixture/base-request.json"))
        bypass = subprocess.run(validate, check=False, capture_output=True, text=True)
        self.assertNotEqual(bypass.returncode, 0)
        self.assertIn("OWNER_REQUEST_V2_REQUIRED", bypass.stderr)

    def test_generic_noop_or_ignoring_adapter_cannot_pass(self) -> None:
        self.fixture.write_text(
            "fixture/noop-adapter.py",
            "#!/usr/bin/env python3\nraise SystemExit(0)\n",
        )
        cases = ("generic-noop", "adapter-ignores-consumer")
        for index, case_id in enumerate(cases, 1):
            with self.subTest(case_id=case_id):
                manifest = copy.deepcopy(self.fixture.base_manifest())
                if case_id == "generic-noop":
                    stage = manifest["consumer_rehearsal"]["stages"][0]
                    stage["runner_ref"] = self.fixture.exact_ref(
                        "fixture/noop-adapter.py"
                    )
                    stage["argv"][1] = "fixture/noop-adapter.py"
                else:
                    stage = manifest["consumer_rehearsal"]["stages"][8]
                    consumer_index = stage["argv"].index("--consumer")
                    del stage["argv"][consumer_index : consumer_index + 2]
                completed = self.fixture.run_rehearsal(
                    manifest, f"fixture/noop-adapter-{index}.json"
                )
                self.assertNotEqual(completed.returncode, 0, completed.stderr)
                receipt = json.loads(
                    self.fixture.path(
                        f"fixture/noop-adapter-{index}.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertIn(
                    "E17_CANONICAL_CONSUMER_IDENTITY",
                    "\n".join(receipt["blockers"]),
                )

    def test_actual_consumer_entrypoints_are_the_required_public_boundaries(self) -> None:
        self.assertEqual(len(REAL_CONSUMER_ENTRYPOINTS), len(STAGES))
        missing = [
            path for path in REAL_CONSUMER_ENTRYPOINTS if not (REPOSITORY_ROOT / path).is_file()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Regression tests for Invoke preacceptance consumer closure."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path, PurePosixPath
from typing import Any
from unittest import mock

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
INVOKE_ROOT = HERE.parents[1]
ARCANUM_ROOT = INVOKE_ROOT.parents[1]
REPOSITORY_ROOT = ARCANUM_ROOT.parent
SOURCE_RUNNER = INVOKE_ROOT / "scripts/preacceptance_closure.py"
SOURCE_SCHEMAS = INVOKE_ROOT / "schemas"
SOURCE_ADAPTER = HERE / "real_consumer_rehearsal.py"
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
ENTRY_STAGES = [
    "wpra",
    "implementation-readiness",
    "context-builder",
    "mutation-admission",
    "governance-prepare",
    "closeout-preflight",
    "heterogeneous-owner-closeout",
    "terminal",
    "continuity",
]
ENTRY_CONSUMERS = {
    "wpra": ("work-pack-readiness-audit.v2", ["arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py"]),
    "implementation-readiness": ("implementation-readiness.execution-contracts.v1", ["arcanum/spells/implementation-readiness/scripts/execution_contracts.py"]),
    "context-builder": ("context-builder.native-machine-view.v1", ["arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py"]),
    "mutation-admission": ("task-session.mutation-admission.v1", ["arcanum/arcana/task-session/scripts/verify-mutation-readiness.py"]),
    "governance-prepare": ("task-session.live-execution-entry-preparation.v1", ["arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"]),
    "closeout-preflight": ("task-session.closeout-preflight.v1", ["arcanum/arcana/task-session/scripts/evaluate-governance.py"]),
    "terminal": ("task-session.terminal-schema.v1", ["arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json"]),
    "continuity": ("task-session.continuity-schema.v1", ["arcanum/arcana/task-session/continuity.schema.json"]),
}

REAL_CONSUMER_ENTRYPOINTS = [
    "arcanum/spells/invoke/scripts/material_package_validator.py",
    "arcanum/spells/invoke/scripts/refresh_material_handoff.py",
    "arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py",
    "arcanum/spells/task-session-until-blocker/scripts/run_chain.py",
    "arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py",
    "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
    "arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py",
    "arcanum/arcana/task-session/scripts/plan-once-material-controller.py",
    "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json",
    "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
    "arcanum/arcana/continuation-router/scripts/work_pack_route.py",
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
        shutil.copy2(
            SOURCE_SCHEMAS / "execution-entry-consumer-rehearsal-v1.schema.json",
            self.invoke / "schemas/execution-entry-consumer-rehearsal-v1.schema.json",
        )
        shutil.copy2(
            SOURCE_SCHEMAS / "request-emission-eligibility-receipt-v1.schema.json",
            self.invoke / "schemas/request-emission-eligibility-receipt-v1.schema.json",
        )
        support_paths = [
            *REAL_CONSUMER_ENTRYPOINTS,
            "arcanum/spells/invoke/scripts/validate_owner_acceptance_response.py",
            "arcanum/spells/invoke/scripts/handle_pre_execution_block.py",
            "arcanum/spells/invoke/schemas/owner-acceptance-response-v1.schema.json",
            "arcanum/spells/invoke/schemas/pre-execution-block-owner-receipt-v1.schema.json",
            "arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py",
            "arcanum/spells/work-pack-readiness-audit/scripts/plan_semantics.py",
            "arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py",
            "arcanum/spells/task-session-until-blocker/scripts/task_session_until_blocker_runtime_paths.py",
            "arcanum/arcana/continuation-router/scripts/continuation_router_runtime_paths.py",
            "arcanum/spells/implementation-readiness/scripts/execution_contracts.py",
            "arcanum/arcana/task-session/schemas/precloseout-execution-receipt.schema.json",
            "arcanum/arcana/task-session/continuity.schema.json",
            "arcanum/arcana/continuation-router/schemas/work-pack-route-admission.schema.json",
        ]
        for relative in support_paths:
            source = (
                SOURCE_ADAPTER
                if relative.endswith("preacceptance-closure/real_consumer_rehearsal.py")
                else REPOSITORY_ROOT / relative
            )
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        shutil.copytree(
            REPOSITORY_ROOT / "arcanum/arcana/task-session",
            self.root / "arcanum/arcana/task-session",
            dirs_exist_ok=True,
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
        self.write_json("fixture/target.json", {"status": "baseline"})
        self.write_json("fixture/candidate.json", {"status": "final"})
        self.write_json(
            "fixture/projection.json",
            {
                "kind": "execution-projection",
                "governance_prepare_rehearsal": {
                    "schema_version": (
                        "invoke.preacceptance-governance-prepare-rehearsal.v1"
                    ),
                    "request_ref": self.exact_ref("scenario/request.json"),
                    "selected_route": fast_entry_request["execution_binding"][
                        "current_route"
                    ],
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
        self.write_json("fixture/negative-regression.json", {"result": "pass", "cases": 16})
        self.write_json("fixture/cross-capability-regression.json", {"result": "pass", "stages": STAGES})
        self.write_json("fixture/rollout.json", {"scope": "canonical-source-local", "result": "pass"})
        self.write_adoption()
        self.write_json(
            "fixture/wpra-config.json",
            {
                "task_session_closeout_contracts": [
                    {
                        "expected_owner_receipt_schema_ref": {
                            "artifact_ref": self.exact_ref(
                                "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json"
                            )
                        }
                    },
                    {
                        "expected_owner_receipt_schema_ref": {
                            "artifact_ref": self.exact_ref(
                                "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json"
                            )
                        }
                    },
                ]
            },
        )
        self.write_execution_entry_receipt()
        self.write_eligibility_receipt()
        self.write_manifest(self.base_manifest())
        self.write_json("fixture/base-request.json", {"request_id": "fixture-owner-request", "status": "pending"})
        self.install_live_execution_entry_topology()
        self.write_execution_entry_receipt()
        self.write_eligibility_receipt()
        self.write_manifest(self.base_manifest())

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

    def write_execution_entry_receipt(self) -> None:
        wpra_config = json.loads(
            self.path("fixture/wpra-config.json").read_text(encoding="utf-8")
        )
        owner_refs = sorted(
            (
                item["expected_owner_receipt_schema_ref"]["artifact_ref"]
                for item in wpra_config["task_session_closeout_contracts"]
            ),
            key=lambda item: item["path"],
        )
        stages = []
        for stage_id in ENTRY_STAGES:
            if stage_id == "heterogeneous-owner-closeout":
                identity = "lifecycle-owner.closeout-schema-frontier.v1"
                refs = owner_refs
            else:
                identity, paths = ENTRY_CONSUMERS[stage_id]
                refs = [self.exact_ref(path) for path in paths]
            stages.append(
                {
                    "stage_id": stage_id,
                    "consumer_identity": identity,
                    "consumer_refs": refs,
                    "result": "pass",
                    "projection_digest": canonical_digest({"stage": stage_id}),
                }
            )
        receipt: dict[str, Any] = {
            "schema_version": "invoke.execution-entry-consumer-rehearsal.v1",
            "source_ref": self.exact_ref("fixture/projection.json"),
            "wpra_config_ref": self.exact_ref("fixture/wpra-config.json"),
            "unit_id": "SWU-FIXTURE-001",
            "stages": stages,
            "closure_result": "pass",
            "request_eligibility_result": "block",
            "request_eligibility_blockers": ["REQUEST_EMISSION_ELIGIBILITY_BINDING_MISSING"],
            "owner_acceptance_status": "pending",
            "selection_admission_authority": "absent",
            "effects": {
                "repository_writes": 0,
                "external_effects": False,
                "selection": False,
                "admission_token": False,
                "execution": False,
            },
            "authority_effect": "none",
        }
        receipt["receipt_digest"] = canonical_digest(receipt)
        self.write_json("fixture/execution-entry-rehearsal.json", receipt)

    def requested_effect(self) -> dict[str, Any]:
        return {
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
        }

    def write_eligibility_receipt(self) -> None:
        subject = {
            "source_ref": self.exact_ref("fixture/projection.json"),
            "wpra_config_ref": self.exact_ref("fixture/wpra-config.json"),
            "execution_entry_rehearsal_ref": self.exact_ref("fixture/execution-entry-rehearsal.json"),
            "task_id": "TASK-FIXTURE",
            "unit_id": "SWU-FIXTURE-001",
            "requested_effect_digest": canonical_digest(self.requested_effect()),
        }
        receipt: dict[str, Any] = {
            "schema_version": "invoke.request-emission-eligibility-receipt.v1",
            "eligibility_id": "fixture-request-emission-eligibility",
            "subject": subject,
            "subject_digest": canonical_digest(subject),
            "result": "pass",
            "blockers": [],
            "owner_acceptance_status": "pending",
            "permitted_effects": {
                "owner_request_emission": True,
                "selection": False,
                "admission": False,
                "execution": False,
            },
            "authority_effect": "none",
            "claim_ceiling": "Request-emission eligibility only; owner acceptance remains pending and selection, admission, and execution remain forbidden.",
        }
        receipt["receipt_digest"] = canonical_digest(receipt)
        self.write_json("fixture/request-eligibility.json", receipt)

    def install_live_execution_entry_topology(self) -> None:
        """Bind the projection to the exact first-write coordinator in two modes."""
        request_path = self.path("scenario/request.json")
        request = json.loads(request_path.read_text(encoding="utf-8"))
        fast_request_path = self.path("scenario/fast-entry-request.json")
        fast_request = json.loads(fast_request_path.read_text(encoding="utf-8"))
        attempt = request["run_id"]
        run_dir = "rehearsal/task-session-run"
        producer_path = self.write_text(
            "scenario/readiness-producer/produce-readiness.py",
            "#!/usr/bin/env python3\n"
            "import json, pathlib, sys\n"
            "p=pathlib.Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); "
            "p.write_text(json.dumps({'result':'pass'},sort_keys=True)+'\\n',encoding='utf-8')\n",
        )
        blocker_path = self.write_json(
            "scenario/deliberate-pre-execution-block.json",
            {"code": "DELIBERATE_PRE_EXECUTION_BLOCK"},
        )
        readiness_bytes = (json.dumps({"result": "pass"}, sort_keys=True) + "\n").encode()
        controls: list[dict[str, Any]] = [
            {
                "path": "rehearsal/live/readiness.json",
                "owner_capability": "work-pack-readiness-audit",
                "write_class": "readiness-evidence",
                "attempt_id": attempt,
                "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                "expected_postimage_ref": {
                    "path": "rehearsal/live/readiness.json",
                    "sha256": hashlib.sha256(readiness_bytes).hexdigest(),
                    "size_bytes": len(readiness_bytes),
                },
                "runtime_revalidation": "exact-postimage-before-consume",
            }
        ]
        for index, phase in enumerate(
            ("resolved", "governed", "admitted", "ticketed", "execution-received", "reconciled"),
            start=1,
        ):
            controls.append(
                {
                    "path": f"{run_dir}/checkpoints/{index:02d}-{phase}.json",
                    "owner_capability": "task-session",
                    "write_class": "governance-checkpoint",
                    "attempt_id": attempt,
                    "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                    "runtime_revalidation": "baseline-before-write",
                }
            )
        for path, write_class in (
            (f"{run_dir}/execution-ticket.json", "execution-ticket"),
            (f"{run_dir}/reconciliation.json", "reconciliation-evidence"),
            (f"{run_dir}/commit-journal.json", "commit-evidence"),
            (f"{run_dir}/commit-receipt.json", "commit-evidence"),
        ):
            controls.append(
                {
                    "path": path,
                    "owner_capability": "task-session",
                    "write_class": write_class,
                    "attempt_id": attempt,
                    "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                    "runtime_revalidation": "baseline-before-write",
                }
            )
        controls.append(
            {
                "path": request["plan_admission"]["consumption_ledger_path"],
                "owner_capability": "task-session",
                "write_class": "consumption-ledger",
                "attempt_id": attempt,
                "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                "runtime_revalidation": "baseline-before-write",
            }
        )
        preparation_receipt_path = "rehearsal/live/preparation-receipt.json"
        controls.append(
            {
                "path": preparation_receipt_path,
                "owner_capability": "task-session",
                "write_class": "preparation-receipt",
                "attempt_id": attempt,
                "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                "runtime_revalidation": "baseline-before-write",
            }
        )
        partition = {
            "schema_version": "task-session.live-control-evidence-partition.v1",
            "attempt_id": attempt,
            "repository_root": ".",
            "outputs": controls,
            "exact_union_scope": [item["path"] for item in controls],
        }
        partition_path = self.write_json("scenario/live-control-partition.json", partition)

        route = fast_request["execution_policy"]["allowed_routes"][0]
        terminal_path = request["fast_execution_entry"]["route_scope_partition"]["terminal_receipt_scope"]
        lifecycle = request["fast_execution_entry"]["route_scope_partition"]["lifecycle_owner_scopes"]
        full_route_scope = sorted(
            {
                *request["execution_contract"]["allowed_writes"],
                terminal_path,
                *[item["path"] for item in lifecycle],
                *partition["exact_union_scope"],
            }
        )
        route["write_scope"] = full_route_scope
        fast_request["execution_policy"]["allowed_routes_digest"] = canonical_digest(
            fast_request["execution_policy"]["allowed_routes"]
        )
        fast_request["execution_entry"]["allowed_routes_digest"] = fast_request[
            "execution_policy"
        ]["allowed_routes_digest"]
        contracts = load_module(
            self.path("arcanum/spells/implementation-readiness/scripts/execution_contracts.py"),
            "preacceptance_live_topology_contracts",
        )
        fast_request["execution_binding"] = contracts.build_execution_intent_binding(
            fast_request["execution_policy"],
            fast_request["execution_entry"],
            source_invocation_id="synthetic:preacceptance-live-topology",
            created_at="2026-08-08T00:00:00Z",
            execution_mode="one-unit",
        )
        self.write_json("scenario/fast-entry-request.json", fast_request)
        guard = load_module(
            self.path("arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py"),
            "preacceptance_live_topology_guard",
        )
        self.write_json(
            "scenario/fast-entry-receipt.json", guard.classify_fast_entry(fast_request)
        )

        owner_request, owner_graph_refs = build_canonical_owner_request_fixture(
            self.root,
            request_id="PREACCEPTANCE-FIXTURE-OWNER-REQUEST",
            authority_write_ceiling=full_route_scope,
            fixture_prefix="scenario/owner-proof",
        )
        owner_path = self.path("scenario/owner-proof/owner-request-v2.json")
        owner_ref = self.exact_ref("scenario/owner-proof/owner-request-v2.json")
        owner_response: dict[str, Any] = {
            "schema_version": "invoke.owner-acceptance-response.v1",
            "response_id": "PREACCEPTANCE-FIXTURE-OWNER-RESPONSE",
            "request_ref": owner_ref,
            "request_id": owner_request["request_id"],
            "request_digest": owner_request["request_digest"],
            "decision": "accepted",
            "authorization_token": f"ACCEPT-{owner_request['request_id']}-{owner_request['request_digest']}",
            "actor": {
                "capability": "owner",
                "subject": "synthetic-preacceptance-owner",
                "provenance": "current-user-exact-token",
            },
            "requested_effect_digest": canonical_digest(
                owner_request["base_request"]["requested_effect"]
            ),
            "authority_write_ceiling_digest": canonical_digest(full_route_scope),
            "attempt_id": attempt,
            "one_attempt_ceiling": 1,
            "authority_effect": "accept-exact-request-for-one-attempt-only",
        }
        owner_response["response_digest"] = canonical_digest(owner_response)
        owner_response_path = self.write_json("scenario/owner-proof/owner-response.json", owner_response)

        executable = Path(sys.executable)
        executable_bytes = executable.read_bytes()
        executable_identity = {
            "path": str(executable),
            "sha256": hashlib.sha256(executable_bytes).hexdigest(),
            "size_bytes": len(executable_bytes),
        }
        def ref(path: Path) -> dict[str, Any]:
            return self.exact_ref(path.relative_to(self.root).as_posix())
        closure_builder = load_module(
            self.path("arcanum/arcana/task-session/scripts/invocation_input_closure.py"),
            "preacceptance_invocation_input_closure",
        )
        def invocation(
            runner: Path,
            argv: list[str],
            refs: list[dict[str, Any]],
            owner_roots: list[str] | None = None,
        ) -> dict[str, Any]:
            relative = runner.relative_to(self.root).as_posix()
            if owner_roots is None:
                if relative.startswith("arcanum/arcana/task-session/"):
                    owner_roots = ["arcanum/arcana/task-session"]
                elif relative.startswith("arcanum/spells/invoke/"):
                    owner_roots = ["arcanum/spells/invoke"]
                else:
                    owner_roots = [runner.parent.relative_to(self.root).as_posix()]
            closure_id = "preacceptance-" + hashlib.sha256(
                (relative + json.dumps(refs, sort_keys=True)).encode()
            ).hexdigest()[:16]
            closure = closure_builder.build(self.root, closure_id, owner_roots, refs)
            closure_path = self.write_json(
                f"scenario/input-closures/{closure_id}.json", closure
            )
            return {
                "runner_ref": ref(runner),
                "executable_identity": executable_identity,
                "argv": argv,
                "cwd": ".",
                "input_closure_ref": ref(closure_path),
                "input_refs": closure["input_refs"],
                "environment": {"PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/tmp"},
                "timeout_seconds": 60,
                "max_output_bytes": 1048576,
                "network_allowed": False,
                "external_effects_allowed": False,
            }
        response_validator = self.path("arcanum/spells/invoke/scripts/validate_owner_acceptance_response.py")
        response_inputs = [
            ref(response_validator),
            self.exact_ref("arcanum/spells/invoke/schemas/owner-acceptance-response-v1.schema.json"),
            ref(owner_response_path),
            *owner_graph_refs,
        ]
        producer_invocation = invocation(
            producer_path,
            ["{executable}", "{runner}", "rehearsal/live/readiness.json"],
            [ref(producer_path)],
        )
        runner_path = self.path("arcanum/arcana/task-session/scripts/task-session-governance-runner.py")
        runner_inputs = [
            self.exact_ref(relative)
            for relative in [
                "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
                "arcanum/arcana/task-session/scripts/control_evidence_partition.py",
                "arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py",
                "arcanum/spells/implementation-readiness/scripts/execution_contracts.py",
                "arcanum/spells/implementation-readiness/schemas/execution-policy.schema.json",
                "arcanum/spells/implementation-readiness/schemas/execution-entry-projection.schema.json",
                "arcanum/spells/implementation-readiness/schemas/execution-intent-binding.schema.json",
                "arcanum/arcana/task-session/schemas/governance-run-request.schema.json",
                "arcanum/arcana/task-session/schemas/fast-execution-entry-request.schema.json",
                "arcanum/arcana/task-session/schemas/fast-execution-entry-receipt.schema.json",
                "arcanum/arcana/task-session/schemas/live-control-evidence-partition-v1.schema.json",
                "arcanum/arcana/task-session/schemas/live-execution-entry-preparation-receipt-v1.schema.json",
                "arcanum/arcana/task-session/schemas/execution-ticket.schema.json",
                "arcanum/arcana/task-session/schemas/governance-phase-receipt.schema.json",
                "arcanum/arcana/task-session/schemas/executor-receipt.schema.json",
                "scenario/WORK-PACK.md",
                "scenario/TASK.md",
                "scenario/controls/evaluation.json",
                "scenario/controls/admission.json",
                "scenario/controls/preflight.json",
                "scenario/controls/selection.json",
                "scenario/fast-entry-request.json",
                "scenario/fast-entry-receipt.json",
                "scenario/live-control-partition.json",
            ]
        ]
        governance_invocation = invocation(
            runner_path,
            [
                "{executable}", "{runner}", "prepare", "--repo-root", "{repo_root}",
                "--request", "{request}", "--run-dir", "{run_dir}",
            ],
            runner_inputs,
            ["arcanum/arcana/task-session", "arcanum/spells/implementation-readiness"],
        )
        governance_invocation.pop("cwd")
        governance_invocation["output_paths"] = [
            f"{run_dir}/checkpoints/01-resolved.json",
            f"{run_dir}/checkpoints/02-governed.json",
            f"{run_dir}/checkpoints/03-admitted.json",
            f"{run_dir}/checkpoints/04-ticketed.json",
            f"{run_dir}/execution-ticket.json",
        ]
        preparation: dict[str, Any] = {
            "schema_version": "task-session.live-execution-entry-preparation.v1",
            "attempt_id": attempt,
            "control_evidence_partition_ref": ref(partition_path),
            "owner_acceptance_request_ref": owner_ref,
            "owner_acceptance_response_ref": ref(owner_response_path),
            "authority_write_ceiling_digest": owner_response["authority_write_ceiling_digest"],
            "owner_acceptance_validation": invocation(
                response_validator,
                ["{executable}", "{runner}", "--repo-root", "{repo_root}", "--response", "{owner_response}"],
                response_inputs,
            ),
            "preparation_steps": [
                {
                    "step_id": "readiness",
                    "owner_capability": "work-pack-readiness-audit",
                    "invocation": producer_invocation,
                    "output_paths": ["rehearsal/live/readiness.json"],
                }
            ],
            "governance_runner": governance_invocation,
            "run_dir": run_dir,
            "preparation_receipt_path": preparation_receipt_path,
            "shadow_mode_supported": True,
        }
        preparation_path = self.write_json("scenario/live-preparation.json", preparation)

        route_partition = {
            "schema_version": "task-session.fast-entry-route-scope-partition.v1",
            "executor_write_scopes": request["execution_contract"]["allowed_writes"],
            "terminal_receipt_scope": terminal_path,
            "lifecycle_owner_scopes": lifecycle,
            "control_evidence_partition": partition,
            "exact_union_scope": full_route_scope,
        }
        request["control_evidence_partition"] = partition
        request["live_execution_entry_preparation_ref"] = ref(preparation_path)
        request["live_execution_entry_preparation_receipt_path"] = preparation_receipt_path
        request["fast_execution_entry"] = {
            "request_ref": self.exact_ref("scenario/fast-entry-request.json"),
            "receipt_ref": self.exact_ref("scenario/fast-entry-receipt.json"),
            "route_scope_partition": route_partition,
        }
        request["closeout_contract"]["terminal_receipt_path"] = terminal_path
        failure_profile: dict[str, Any] = {
            "schema_version": "task-session.pre-execution-failure-terminalization.v1",
            "work_pack_id": fast_request["execution_policy"]["work_pack_id"],
            "task_id": request["task_id"],
            "swu_id": request["swu_id"],
            "attempt_id": attempt,
            "owner_acceptance_request_ref": owner_ref,
            "owner_acceptance_response_ref": ref(owner_response_path),
            "control_evidence_partition_ref": ref(partition_path),
            "failure_terminal_schema_ref": self.exact_ref("arcanum/arcana/task-session/schemas/pre-execution-failure-terminal-receipt-v1.schema.json"),
            "invoke_owner_schema_ref": self.exact_ref("arcanum/spells/invoke/schemas/pre-execution-block-owner-receipt-v1.schema.json"),
            "continuity_schema_ref": self.exact_ref("arcanum/arcana/task-session/continuity.schema.json"),
            "blocker_refs": [ref(blocker_path)],
            "control_refs": [controls[0]["expected_postimage_ref"]],
            "terminal_receipt_path": terminal_path,
            "invoke_owner_receipt_path": "records/owner-closeout.json",
            "continuity_cursor_path": ".runtime/continuity.json",
            "continuity_updated_at": "2026-01-01T00:00:00Z",
            "requested_effect": "record-pre-execution-block-with-no-product-effect",
        }
        failure_profile["blocker_fingerprint"] = canonical_digest(
            {
                key: (
                    sorted(
                        failure_profile[key],
                        key=lambda item: (item["path"], item["sha256"], item["size_bytes"]),
                    )
                    if key in {"blocker_refs", "control_refs"}
                    else failure_profile[key]
                )
                for key in (
                    "work_pack_id", "task_id", "swu_id", "attempt_id",
                    "owner_acceptance_request_ref", "owner_acceptance_response_ref",
                    "control_evidence_partition_ref", "failure_terminal_schema_ref",
                    "invoke_owner_schema_ref", "continuity_schema_ref", "blocker_refs",
                    "control_refs",
                )
            }
        )
        request["failure_terminalization"] = failure_profile
        self.write_json("scenario/request.json", request)

        projection = json.loads(self.path("fixture/projection.json").read_text(encoding="utf-8"))
        request_ref = self.exact_ref("scenario/request.json")
        preparation_ref = self.exact_ref("scenario/live-preparation.json")
        budget_adapter = load_module(
            self.path(
                "arcanum/spells/invoke/development/preacceptance-closure/"
                "real_consumer_rehearsal.py"
            ),
            "preacceptance_budget_adapter",
        )
        projection["governance_prepare_rehearsal"] = {
            "schema_version": "invoke.preacceptance-governance-prepare-rehearsal.v2",
            "request_ref": request_ref,
            "preparation_ref": preparation_ref,
            "selected_route": fast_request["execution_binding"]["current_route"],
            "route_scope_partition": route_partition,
            "run_dir": run_dir,
            "failure_stop_after": "readiness",
        }
        projection["governance_prepare_rehearsal"]["live_entry_rehearsal_budget"] = (
            budget_adapter.derive_live_entry_rehearsal_budget(
                request_ref,
                preparation_ref,
                preparation,
                "readiness",
            )
        )
        self.write_json("fixture/projection.json", projection)

    def base_manifest(self) -> dict[str, Any]:
        adapter_path = (
            "arcanum/spells/invoke/development/preacceptance-closure/"
            "real_consumer_rehearsal.py"
        )
        adapter_ref = self.exact_ref(adapter_path)
        projection_ref = self.exact_ref("fixture/projection.json")
        projection_document = json.loads(
            self.path("fixture/projection.json").read_text(encoding="utf-8")
        )
        rehearsal_contract = projection_document.get("governance_prepare_rehearsal", {})
        governance_timeout = rehearsal_contract.get(
            "live_entry_rehearsal_budget", {"stage_timeout_seconds": 90}
        )["stage_timeout_seconds"]
        schema_ref = self.exact_ref("fixture/schema.json")
        stages = []
        for stage, consumer in zip(STAGES, REAL_CONSUMER_ENTRYPOINTS, strict=True):
            consumer_ref = self.exact_ref(consumer)
            if consumer.endswith(".json") or stage == "task_session_governance_runner":
                runner_ref = adapter_ref
                argv = [
                    sys.executable,
                    adapter_path,
                    "--stage",
                    stage,
                    "--consumer",
                    consumer,
                    "--projection",
                    projection_ref["path"],
                    "--rehearsal-root",
                    "{rehearsal_root}",
                ]
            else:
                runner_ref = consumer_ref
                argv = [sys.executable, consumer, "--help"]
            stages.append(
                {
                    "stage_id": stage,
                    "projection_ref": projection_ref,
                    "runner_ref": runner_ref,
                    "exercised_runner_ref": consumer_ref,
                    "argv": argv,
                    "cwd": ".",
                    "environment_names": ["PATH"],
                    "environment": {
                        "PREACCEPTANCE_PROJECTION_REF": projection_ref["path"]
                    },
                    "timeout_seconds": (
                        governance_timeout
                        if stage == "task_session_governance_runner"
                        else 30
                    ),
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
                    "content_kind": "json-object",
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
                "governance_rehearsal_projection_ref": projection_ref,
                "wpra_config_ref": self.exact_ref("fixture/wpra-config.json"),
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
                    "ref": self.exact_ref(
                        "arcanum/arcana/task-session/scripts/"
                        "prepare_live_execution_entry.py"
                    ),
                    "argv": [
                        sys.executable,
                        "arcanum/arcana/task-session/scripts/"
                        "prepare_live_execution_entry.py",
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
                "execution_entry_consumer_rehearsal_ref": self.exact_ref(
                    "fixture/execution-entry-rehearsal.json"
                ),
                "request_emission_eligibility_ref": self.exact_ref(
                    "fixture/request-eligibility.json"
                ),
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
            "requested_effect": self.requested_effect(),
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


def build_canonical_owner_request_fixture(
    repository_root: Path,
    *,
    request_id: str,
    authority_write_ceiling: list[str],
    fixture_prefix: str = "fixture",
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build one compact, canonically re-emittable v2 owner-request graph.

    This builder is deliberately synthetic, but every closure, review, adoption,
    and base-request binding is schema-valid, digest-bound, and accepted by the
    canonical ``validate-request`` implementation.  It is used only to test the
    separate owner-response boundary without hand-authoring a request-shaped JSON
    object.
    """
    fixture = Fixture.__new__(Fixture)
    fixture.root = repository_root
    fixture.invoke = repository_root / "arcanum/spells/invoke"
    prefix = fixture_prefix.strip("/")
    if not prefix or prefix.startswith(".") or ".." in PurePosixPath(prefix).parts:
        raise ValueError("unsafe canonical owner-request fixture prefix")
    default_path = fixture.path
    fixture.path = lambda relative: (
        repository_root / prefix / relative.removeprefix("fixture/")
        if relative == "fixture" or relative.startswith("fixture/")
        else default_path(relative)
    )
    def prefixed_exact_ref(relative: str) -> dict[str, Any]:
        path = fixture.path(relative)
        content = path.read_bytes()
        return {
            "path": path.relative_to(repository_root).as_posix(),
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
        }
    fixture.exact_ref = prefixed_exact_ref
    (repository_root / prefix).mkdir(parents=True, exist_ok=True)
    fixture.write_json("fixture/target.json", {"status": "baseline"})
    fixture.write_json("fixture/candidate.json", {"status": "final"})
    fixture.write_json("fixture/projection.json", {"kind": "execution-projection"})
    fixture.write_json(
        "fixture/schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["kind"],
            "properties": {"kind": {"type": "string"}},
        },
    )
    fixture.write_json("fixture/source-reflection.json", {"proposal": "admission-completeness"})
    fixture.write_json("fixture/negative-regression.json", {"result": "pass", "cases": 16})
    fixture.write_json("fixture/cross-capability-regression.json", {"result": "pass", "stages": STAGES})
    fixture.write_json("fixture/rollout.json", {"scope": "canonical-source-local", "result": "pass"})
    fixture.write_adoption()
    fixture.write_json(
        "fixture/wpra-config.json",
        {
            "task_session_closeout_contracts": [
                {
                    "expected_owner_receipt_schema_ref": {
                        "artifact_ref": fixture.exact_ref(
                            "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json"
                        )
                    }
                },
                {
                    "expected_owner_receipt_schema_ref": {
                        "artifact_ref": fixture.exact_ref(
                            "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json"
                        )
                    }
                },
            ]
        },
    )
    fixture.write_execution_entry_receipt()
    requested_effect = fixture.requested_effect()
    requested_effect["target_paths"] = [f"{prefix}/target.json"]
    requested_effect["authority_write_ceiling"] = list(authority_write_ceiling)
    fixture.requested_effect = lambda: copy.deepcopy(requested_effect)
    fixture.write_eligibility_receipt()
    manifest = fixture.base_manifest()
    def prefix_fixture_locators(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: prefix_fixture_locators(nested) for key, nested in value.items()}
        if isinstance(value, list):
            return [prefix_fixture_locators(nested) for nested in value]
        if isinstance(value, str) and value.startswith("fixture/"):
            return f"{prefix}/{value.removeprefix('fixture/')}"
        return value
    manifest = prefix_fixture_locators(manifest)
    fixture.write_manifest(manifest)
    fixture.write_json(
        "fixture/base-request.json",
        {
            "request_id": request_id,
            "status": "pending",
            "requested_effect": requested_effect,
        },
    )

    graph_digest = canonical_digest(manifest)
    zero = canonical_digest([])
    receipt: dict[str, Any] = {
        "schema_version": "invoke.preacceptance-closure-receipt.v1",
        "closure_id": manifest["closure_id"],
        "manifest_ref": fixture.exact_ref("fixture/manifest.json"),
        "closure_graph_digest": graph_digest,
        "runner_ref": fixture.exact_ref(
            "arcanum/spells/invoke/scripts/preacceptance_closure.py"
        ),
        "result": "pass",
        "blockers": [],
        "stage_results": [
            {
                "stage_id": stage["stage_id"],
                "runner_ref": stage["runner_ref"],
                "invocation_digest": canonical_digest(
                    {"argv": stage["argv"], "environment": stage["environment"]}
                ),
                "exit_code": 0,
                "schema_checks": ["synthetic-boundary-fixture"],
                "result": "pass",
            }
            for stage in manifest["consumer_rehearsal"]["stages"]
        ],
        "protected_inputs": {
            "count": len(manifest["consumer_rehearsal"]["protected_refs"]),
            "before_digest": zero,
            "after_digest": zero,
            "unchanged": True,
        },
        "repository_state": {
            "before_digest": zero,
            "after_digest": zero,
            "unchanged": True,
        },
        "write_observation": {
            "repository_writes": 0,
            "protected_writes": 0,
            "external_effects_observed": False,
        },
        "determinism": {
            "runs": 2,
            "run_result_digest": zero,
            "byte_stable": True,
        },
        "authority_effect": "none",
        "claim_ceiling": "Synthetic canonical owner-response boundary fixture only.",
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    fixture.write_json("fixture/receipt.json", receipt)
    fixture.write_review()

    module = load_module(
        fixture.invoke / "scripts/preacceptance_closure.py",
        f"canonical_owner_request_{hashlib.sha256(str(repository_root).encode()).hexdigest()}",
    )
    request = module.emit_request(
        repository_root,
        fixture.path("fixture/manifest.json"),
        fixture.path("fixture/receipt.json"),
        fixture.path("fixture/review.json"),
        fixture.path("fixture/adoption.json"),
        fixture.path("fixture/base-request.json"),
    )
    fixture.write_json("fixture/owner-request-v2.json", request)
    blockers = module.validate_emitted_request(
        repository_root, fixture.path("fixture/owner-request-v2.json")
    )
    if blockers:
        raise AssertionError("canonical owner-request fixture invalid: " + "; ".join(blockers))

    def collect_refs(value: Any, found: dict[str, dict[str, Any]]) -> None:
        if isinstance(value, dict):
            if set(value) == {"path", "sha256", "size_bytes"} and isinstance(value["path"], str):
                found[value["path"]] = value
            else:
                for nested in value.values():
                    collect_refs(nested, found)
        elif isinstance(value, list):
            for nested in value:
                collect_refs(nested, found)

    refs: dict[str, dict[str, Any]] = {}
    pending = [fixture.exact_ref("fixture/owner-request-v2.json")]
    while pending:
        reference = pending.pop()
        if reference["path"] in refs:
            continue
        refs[reference["path"]] = reference
        path = repository_root / reference["path"]
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        discovered: dict[str, dict[str, Any]] = {}
        collect_refs(document, discovered)
        pending.extend(discovered.values())
    for relative in [
        "arcanum/spells/invoke/scripts/preacceptance_closure.py",
        "arcanum/spells/invoke/schemas/preacceptance-closure-manifest-v1.schema.json",
        "arcanum/spells/invoke/schemas/preacceptance-closure-receipt-v1.schema.json",
        "arcanum/spells/invoke/schemas/preacceptance-closure-review-v1.schema.json",
        "arcanum/spells/invoke/schemas/preacceptance-closure-adoption-v1.schema.json",
        "arcanum/spells/invoke/schemas/owner-acceptance-request-v2.schema.json",
        "arcanum/spells/invoke/schemas/execution-entry-consumer-rehearsal-v1.schema.json",
        "arcanum/spells/invoke/schemas/request-emission-eligibility-receipt-v1.schema.json",
    ]:
        refs[relative] = fixture.exact_ref(relative)
    return request, [refs[path] for path in sorted(refs)]


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
        elif case_id == "projection-not-in-stage-invocation":
            stage = manifest["consumer_rehearsal"]["stages"][0]
            stage["environment"].pop("PREACCEPTANCE_PROJECTION_REF")
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

    def test_mixed_json_and_opaque_text_postimages_are_supported(self) -> None:
        manifest = self.fixture.base_manifest()
        self.fixture.write_text("fixture/candidate.mjs", "export const status = 'final';\n")
        manifest["final_postimages"].append(
            {
                "target_path": "fixture/validator.mjs",
                "operation": "create",
                "content_kind": "opaque-text",
                "baseline": {"state": "absent", "sha256": None, "size_bytes": None},
                "postimage_ref": self.fixture.exact_ref("fixture/candidate.mjs"),
                "lifecycle_assertions": [],
            }
        )
        manifest["requested_effect"]["target_paths"].append("fixture/validator.mjs")
        manifest["requested_effect"]["authority_write_ceiling"].append(
            "fixture/validator.mjs"
        )
        eligibility = json.loads(
            self.fixture.path("fixture/request-eligibility.json").read_text(encoding="utf-8")
        )
        eligibility["subject"]["requested_effect_digest"] = canonical_digest(
            manifest["requested_effect"]
        )
        eligibility["subject_digest"] = canonical_digest(eligibility["subject"])
        eligibility.pop("receipt_digest")
        eligibility["receipt_digest"] = canonical_digest(eligibility)
        self.fixture.write_json("fixture/request-eligibility.json", eligibility)
        self.fixture.refresh_ref(manifest, "fixture/request-eligibility.json")
        result = self.fixture.run_rehearsal(manifest)
        diagnostic = result.stdout + result.stderr
        if self.fixture.path("fixture/receipt.json").is_file():
            diagnostic += self.fixture.path("fixture/receipt.json").read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, diagnostic)

    def test_postimage_content_kind_contract_rejects_invalid_combinations(self) -> None:
        invalid_manifests = []
        missing_kind = self.fixture.base_manifest()
        del missing_kind["final_postimages"][0]["content_kind"]
        invalid_manifests.append(missing_kind)

        unknown_kind = self.fixture.base_manifest()
        unknown_kind["final_postimages"][0]["content_kind"] = "binary"
        invalid_manifests.append(unknown_kind)

        opaque_with_assertions = self.fixture.base_manifest()
        opaque_with_assertions["final_postimages"][0]["content_kind"] = "opaque-text"
        invalid_manifests.append(opaque_with_assertions)

        json_without_assertions = self.fixture.base_manifest()
        json_without_assertions["final_postimages"][0]["lifecycle_assertions"] = []
        invalid_manifests.append(json_without_assertions)

        for manifest in invalid_manifests:
            with self.subTest(manifest=manifest["final_postimages"][0]):
                result = self.fixture.run_rehearsal(manifest)
                self.assertNotEqual(result.returncode, 0)

    def test_governance_stage_requires_projection_bound_request(self) -> None:
        manifest = self.fixture.base_manifest()
        projection_path = self.fixture.path("fixture/projection.json")
        projection = json.loads(projection_path.read_text(encoding="utf-8"))
        del projection["governance_prepare_rehearsal"]
        self.fixture.write_json("fixture/projection.json", projection)
        self.fixture.write_execution_entry_receipt()
        self.fixture.write_eligibility_receipt()
        manifest = self.fixture.base_manifest()
        completed = self.fixture.run_rehearsal(
            manifest, "fixture/unbound-governance-receipt.json"
        )
        self.assertNotEqual(completed.returncode, 0)
        receipt = json.loads(
            self.fixture.path("fixture/unbound-governance-receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn(
            "consumer stage failed with exit 1: task_session_governance_runner",
            receipt["blockers"],
        )

    def test_generated_task_session_runner_is_exact_deployment_surface(self) -> None:
        generated_runner = (
            ".agents/skills/task-session/scripts/"
            "prepare_live_execution_entry.py"
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

    def test_execution_entry_exact_binding_negative_cases(self) -> None:
        cases = (
            "swapped-source-config",
            "wrong-unit",
            "reordered-stage",
            "duplicate-stage",
            "wrong-consumer-ref",
            "owner-acceptance-pre-required",
        )
        for index, case_id in enumerate(cases, 1):
            with self.subTest(case_id=case_id):
                fixture = Fixture()
                try:
                    receipt_path = fixture.path("fixture/execution-entry-rehearsal.json")
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    if case_id == "swapped-source-config":
                        receipt["source_ref"], receipt["wpra_config_ref"] = receipt["wpra_config_ref"], receipt["source_ref"]
                    elif case_id == "wrong-unit":
                        receipt["unit_id"] = "SWU-FIXTURE-999"
                    elif case_id == "reordered-stage":
                        receipt["stages"][0], receipt["stages"][1] = receipt["stages"][1], receipt["stages"][0]
                    elif case_id == "duplicate-stage":
                        receipt["stages"][1] = copy.deepcopy(receipt["stages"][0])
                    elif case_id == "wrong-consumer-ref":
                        receipt["stages"][0]["consumer_refs"] = [fixture.exact_ref("fixture/schema.json")]
                    else:
                        receipt["owner_acceptance_status"] = "present"
                    receipt.pop("receipt_digest")
                    receipt["receipt_digest"] = canonical_digest(receipt)
                    fixture.write_json("fixture/execution-entry-rehearsal.json", receipt)
                    manifest = fixture.base_manifest()
                    completed = fixture.run_rehearsal(
                        manifest, f"fixture/entry-binding-block-{index}.json"
                    )
                    self.assertEqual(completed.returncode, 1)
                    blocked = json.loads(
                        fixture.path(f"fixture/entry-binding-block-{index}.json").read_text(encoding="utf-8")
                    )
                    self.assertIn("E20_EXECUTION_ENTRY_CLOSURE", "\n".join(blocked["blockers"]))
                finally:
                    fixture.cleanup()

    def test_stale_execution_entry_rehearsal_is_rejected(self) -> None:
        manifest = self.fixture.base_manifest()
        receipt_path = self.fixture.path("fixture/execution-entry-rehearsal.json")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["unit_id"] = "SWU-FIXTURE-STALE"
        receipt.pop("receipt_digest")
        receipt["receipt_digest"] = canonical_digest(receipt)
        self.fixture.write_json("fixture/execution-entry-rehearsal.json", receipt)
        completed = self.fixture.run_rehearsal(manifest, "fixture/stale-entry-block.json")
        self.assertEqual(completed.returncode, 1)
        blocked = json.loads(self.fixture.path("fixture/stale-entry-block.json").read_text(encoding="utf-8"))
        self.assertIn("digest mismatch", "\n".join(blocked["blockers"]))

    def test_request_eligibility_exact_binding_negative_cases(self) -> None:
        cases = ("missing", "malformed", "failing", "wrong-subject")
        for index, case_id in enumerate(cases, 1):
            with self.subTest(case_id=case_id):
                fixture = Fixture()
                try:
                    manifest = fixture.base_manifest()
                    if case_id == "missing":
                        del manifest["normalized_execution_projection"]["request_emission_eligibility_ref"]
                    elif case_id == "malformed":
                        fixture.write_json("fixture/request-eligibility.json", {})
                        manifest["normalized_execution_projection"]["request_emission_eligibility_ref"] = fixture.exact_ref("fixture/request-eligibility.json")
                    else:
                        path = fixture.path("fixture/request-eligibility.json")
                        receipt = json.loads(path.read_text(encoding="utf-8"))
                        if case_id == "failing":
                            receipt["result"] = "block"
                            receipt["blockers"] = ["GENERIC_ELIGIBILITY_BLOCK"]
                            receipt["permitted_effects"]["owner_request_emission"] = False
                        else:
                            receipt["subject"]["unit_id"] = "SWU-FIXTURE-999"
                            receipt["subject_digest"] = canonical_digest(receipt["subject"])
                        receipt.pop("receipt_digest")
                        receipt["receipt_digest"] = canonical_digest(receipt)
                        fixture.write_json("fixture/request-eligibility.json", receipt)
                        manifest["normalized_execution_projection"]["request_emission_eligibility_ref"] = fixture.exact_ref("fixture/request-eligibility.json")
                    completed = fixture.run_rehearsal(
                        manifest, f"fixture/eligibility-block-{index}.json"
                    )
                    self.assertEqual(completed.returncode, 1)
                    blocked = json.loads(
                        fixture.path(f"fixture/eligibility-block-{index}.json").read_text(encoding="utf-8")
                    )
                    self.assertTrue(
                        "E21_REQUEST_ELIGIBILITY" in "\n".join(blocked["blockers"])
                        or "request_emission_eligibility_ref" in "\n".join(blocked["blockers"])
                    )
                finally:
                    fixture.cleanup()

    def test_stale_request_eligibility_is_rejected(self) -> None:
        manifest = self.fixture.base_manifest()
        path = self.fixture.path("fixture/request-eligibility.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        receipt["eligibility_id"] = "stale-after-manifest"
        receipt.pop("receipt_digest")
        receipt["receipt_digest"] = canonical_digest(receipt)
        self.fixture.write_json("fixture/request-eligibility.json", receipt)
        completed = self.fixture.run_rehearsal(manifest, "fixture/stale-eligibility-block.json")
        self.assertEqual(completed.returncode, 1)
        blocked = json.loads(self.fixture.path("fixture/stale-eligibility-block.json").read_text(encoding="utf-8"))
        self.assertIn("digest mismatch", "\n".join(blocked["blockers"]))

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
        self.assertEqual(len(cases), 22)
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
        missing_review_command = copy.deepcopy(command)
        review_index = missing_review_command.index("--review")
        del missing_review_command[review_index : review_index + 2]
        missing_review = subprocess.run(
            missing_review_command, check=False, capture_output=True, text=True
        )
        self.assertNotEqual(missing_review.returncode, 0)
        self.assertFalse(self.fixture.path("fixture/owner-request-v2.json").exists())

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
        eligibility = json.loads(
            self.fixture.path("fixture/request-eligibility.json").read_text(encoding="utf-8")
        )
        self.assertEqual(eligibility["owner_acceptance_status"], "pending")
        self.assertEqual(
            eligibility["permitted_effects"],
            {
                "owner_request_emission": True,
                "selection": False,
                "admission": False,
                "execution": False,
            },
        )

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


class StageProcessTeardownTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_unconfirmed_group_returns_unsafe_timeout_outcome(self) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_unconfirmed_group")
        with tempfile.TemporaryDirectory(prefix="preacceptance-unconfirmed-group-") as raw:
            root = Path(raw)
            ready = root / "child-ready"
            program = (
                "import pathlib,sys,time\n"
                "pathlib.Path(sys.argv[1]).write_text('ready')\n"
                "time.sleep(30)\n"
            )
            with mock.patch.object(
                runner,
                "_wait_for_stage_process_group_exit",
                return_value=False,
            ):
                outcome = runner.run_bounded_stage(
                    [sys.executable, "-c", program, str(ready)],
                    cwd=root,
                    environment={
                        **os.environ,
                        "PYTHONDONTWRITEBYTECODE": "1",
                    },
                    timeout_seconds=0.1,
                    startup_ready_path=ready,
                )

            self.assertEqual(outcome.exit_code, 124)
            self.assertTrue(outcome.timed_out)
            self.assertFalse(outcome.cleanup_safe)
            self.assertIn("absence was not confirmed", outcome.teardown_detail)

    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_timeout_kills_stubborn_descendant_before_rehearsal_cleanup(self) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_process_teardown")
        with tempfile.TemporaryDirectory(prefix="preacceptance-process-tree-") as raw:
            root = Path(raw)
            ready = root / "governance-repository" / "child-ready"
            late_write = root / "governance-repository" / "late-write"
            child_program = (
                "import pathlib,signal,sys,time\n"
                "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                "ready=pathlib.Path(sys.argv[1]); late=pathlib.Path(sys.argv[2])\n"
                "ready.parent.mkdir(parents=True,exist_ok=True); ready.write_text('ready')\n"
                "time.sleep(2); late.write_text('late'); time.sleep(30)\n"
            )
            parent_program = (
                "import pathlib,subprocess,sys,time\n"
                "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],sys.argv[3]])\n"
                "ready=pathlib.Path(sys.argv[2])\n"
                "deadline=time.monotonic()+1\n"
                "while not ready.exists() and time.monotonic()<deadline: time.sleep(0.01)\n"
                "time.sleep(30)\n"
            )
            started = time.monotonic()
            outcome = runner.run_bounded_stage(
                [
                    sys.executable,
                    "-c",
                    parent_program,
                    child_program,
                    str(ready),
                    str(late_write),
                ],
                cwd=root,
                environment={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                timeout_seconds=0.25,
                startup_ready_path=ready,
            )
            self.assertEqual(outcome.exit_code, 124)
            self.assertTrue(outcome.timed_out)
            self.assertTrue(outcome.cleanup_safe)
            self.assertTrue(ready.is_file())
            self.assertLess(time.monotonic() - started, 3.0)
            time.sleep(1.1)
            self.assertFalse(late_write.exists())

    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_timeout_kills_closed_pipe_stubborn_descendant(self) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_closed_pipe_teardown")
        with tempfile.TemporaryDirectory(prefix="preacceptance-closed-pipe-") as raw:
            root = Path(raw)
            ready = root / "governance-repository" / "closed-pipe-child-ready"
            late_write = root / "governance-repository" / "closed-pipe-late-write"
            child_program = (
                "import os,pathlib,signal,sys,time\n"
                "ready=pathlib.Path(sys.argv[1]); late=pathlib.Path(sys.argv[2])\n"
                "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                "ready.parent.mkdir(parents=True,exist_ok=True)\n"
                "null=os.open(os.devnull,os.O_RDWR)\n"
                "for descriptor in (0,1,2): os.dup2(null,descriptor)\n"
                "os.close(null) if null > 2 else None\n"
                "ready.write_text('ready')\n"
                "time.sleep(2); late.write_text('late'); time.sleep(30)\n"
            )
            parent_program = (
                "import pathlib,subprocess,sys,time\n"
                "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],sys.argv[3]])\n"
                "ready=pathlib.Path(sys.argv[2])\n"
                "deadline=time.monotonic()+1\n"
                "while not ready.exists() and time.monotonic()<deadline: time.sleep(0.01)\n"
                "time.sleep(30)\n"
            )
            started = time.monotonic()
            outcome = runner.run_bounded_stage(
                [
                    sys.executable,
                    "-c",
                    parent_program,
                    child_program,
                    str(ready),
                    str(late_write),
                ],
                cwd=root,
                environment={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                timeout_seconds=0.25,
                startup_ready_path=ready,
            )
            self.assertEqual(outcome.exit_code, 124)
            self.assertTrue(outcome.timed_out)
            self.assertTrue(outcome.cleanup_safe)
            self.assertTrue(ready.is_file())
            self.assertLess(time.monotonic() - started, 3.0)
            time.sleep(1.1)
            self.assertFalse(late_write.exists())

    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_normal_zero_exit_with_closed_pipe_descendant_blocks_successor_and_cleanup(
        self,
    ) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_normal_exit_residue")
        with tempfile.TemporaryDirectory(
            prefix="preacceptance-normal-exit-residue-"
        ) as raw:
            root = Path(raw)
            rehearsal_root = root / "owned-rehearsal-root"
            ready = rehearsal_root / "governance-repository" / "child-ready"
            late_write = rehearsal_root / "governance-repository" / "late-write"
            successor = rehearsal_root / "successor-ran"
            child_program = (
                "import os,pathlib,signal,sys,time\n"
                "ready=pathlib.Path(sys.argv[1]); late=pathlib.Path(sys.argv[2])\n"
                "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                "ready.parent.mkdir(parents=True,exist_ok=True)\n"
                "null=os.open(os.devnull,os.O_RDWR)\n"
                "for descriptor in (0,1,2): os.dup2(null,descriptor)\n"
                "os.close(null) if null > 2 else None\n"
                "ready.write_text('ready')\n"
                "time.sleep(2); late.write_text('late'); time.sleep(30)\n"
            )
            leader_program = (
                "import pathlib,subprocess,sys,time\n"
                "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],sys.argv[3]])\n"
                "ready=pathlib.Path(sys.argv[2]); deadline=time.monotonic()+5\n"
                "while not ready.exists() and time.monotonic()<deadline: time.sleep(0.01)\n"
                "raise SystemExit(0 if ready.exists() else 70)\n"
            )
            first_stage = {
                "stage_id": "invoke_material_validation",
                "argv": [
                    sys.executable,
                    "-c",
                    leader_program,
                    child_program,
                    "{rehearsal_root}/governance-repository/child-ready",
                    "{rehearsal_root}/governance-repository/late-write",
                ],
                "cwd": ".",
                "environment_names": [],
                "environment": {},
                "runner_ref": {"path": "fixture/runner.py"},
                "exercised_runner_ref": {"path": "fixture/consumer.py"},
                "schema_checks": [],
                "timeout_seconds": 5,
            }
            successor_stage = {
                **first_stage,
                "stage_id": "invoke_file_bound_handoff",
                "argv": [
                    sys.executable,
                    "-c",
                    "import pathlib,sys; pathlib.Path(sys.argv[1]).write_text('ran')",
                    "{rehearsal_root}/successor-ran",
                ],
            }
            manifest = {
                "normalized_execution_projection": {
                    "successor_execution_allowed": False,
                },
                "consumer_rehearsal": {
                    "stages": [first_stage, successor_stage],
                },
            }
            with (
                mock.patch.object(
                    runner.tempfile,
                    "mkdtemp",
                    return_value=str(rehearsal_root),
                ),
                mock.patch.object(
                    runner,
                    "_wait_for_stage_process_group_exit",
                    return_value=False,
                ),
                mock.patch.object(runner.shutil, "rmtree") as remove_root,
            ):
                results, blockers = runner.run_stages(manifest, root)

            self.assertTrue(ready.is_file())
            self.assertEqual(len(results), 1)
            self.assertEqual(
                results[0]["exit_code"], runner.STAGE_PROCESS_RESIDUE_EXIT_CODE
            )
            self.assertEqual(results[0]["result"], "block")
            self.assertTrue(any("leader exited 0" in item for item in blockers))
            self.assertTrue(any("retained without cleanup" in item for item in blockers))
            self.assertFalse(successor.exists())
            remove_root.assert_not_called()
            time.sleep(1.1)
            self.assertFalse(late_write.exists())

    def test_unconfirmed_group_retains_root_and_preserves_timeout_result(self) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_retained_root")
        with tempfile.TemporaryDirectory(prefix="preacceptance-retained-root-test-") as raw:
            root = Path(raw)
            rehearsal_root = root / "owned-rehearsal-root"
            stage = {
                "stage_id": "invoke_material_validation",
                "argv": [sys.executable, "-c", "raise SystemExit(0)"],
                "cwd": ".",
                "environment_names": [],
                "environment": {},
                "runner_ref": {"path": "fixture/runner.py"},
                "exercised_runner_ref": {"path": "fixture/consumer.py"},
                "schema_checks": [],
                "timeout_seconds": 1,
            }
            manifest = {
                "normalized_execution_projection": {
                    "successor_execution_allowed": False,
                },
                "consumer_rehearsal": {"stages": [stage]},
            }
            unsafe_outcome = runner.StageRunOutcome(
                124,
                True,
                False,
                "owned POSIX process-group absence was not confirmed after SIGKILL",
                True,
            )
            with (
                mock.patch.object(
                    runner.tempfile,
                    "mkdtemp",
                    return_value=str(rehearsal_root),
                ),
                mock.patch.object(
                    runner,
                    "run_bounded_stage",
                    return_value=unsafe_outcome,
                ),
                mock.patch.object(runner.shutil, "rmtree") as remove_root,
            ):
                results, blockers = runner.run_stages(manifest, root)

            self.assertEqual(results[0]["exit_code"], 124)
            self.assertEqual(results[0]["result"], "block")
            self.assertTrue(any("retained without cleanup" in item for item in blockers))
            self.assertTrue(any(str(rehearsal_root) in item for item in blockers))
            remove_root.assert_not_called()

    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_normal_nonzero_exit_preserves_exit_with_closed_pipe_residue(self) -> None:
        runner = load_module(SOURCE_RUNNER, "preacceptance_nonzero_exit_residue")
        with tempfile.TemporaryDirectory(
            prefix="preacceptance-nonzero-exit-residue-"
        ) as raw:
            root = Path(raw)
            rehearsal_root = root / "owned-rehearsal-root"
            ready = rehearsal_root / "governance-repository" / "child-ready"
            late_write = rehearsal_root / "governance-repository" / "late-write"
            successor = rehearsal_root / "successor-ran"
            child_program = (
                "import os,pathlib,signal,sys,time\n"
                "ready=pathlib.Path(sys.argv[1]); late=pathlib.Path(sys.argv[2])\n"
                "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                "ready.parent.mkdir(parents=True,exist_ok=True)\n"
                "null=os.open(os.devnull,os.O_RDWR)\n"
                "for descriptor in (0,1,2): os.dup2(null,descriptor)\n"
                "os.close(null) if null > 2 else None\n"
                "ready.write_text('ready')\n"
                "time.sleep(2); late.write_text('late'); time.sleep(30)\n"
            )
            leader_program = (
                "import pathlib,subprocess,sys,time\n"
                "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],sys.argv[3]])\n"
                "ready=pathlib.Path(sys.argv[2]); deadline=time.monotonic()+5\n"
                "while not ready.exists() and time.monotonic()<deadline: time.sleep(0.01)\n"
                "raise SystemExit(7 if ready.exists() else 70)\n"
            )
            first_stage = {
                "stage_id": "invoke_material_validation",
                "argv": [
                    sys.executable,
                    "-c",
                    leader_program,
                    child_program,
                    "{rehearsal_root}/governance-repository/child-ready",
                    "{rehearsal_root}/governance-repository/late-write",
                ],
                "cwd": ".",
                "environment_names": [],
                "environment": {},
                "runner_ref": {"path": "fixture/runner.py"},
                "exercised_runner_ref": {"path": "fixture/consumer.py"},
                "schema_checks": [],
                "timeout_seconds": 5,
            }
            successor_stage = {
                **first_stage,
                "stage_id": "invoke_file_bound_handoff",
                "argv": [
                    sys.executable,
                    "-c",
                    "import pathlib,sys; pathlib.Path(sys.argv[1]).write_text('ran')",
                    "{rehearsal_root}/successor-ran",
                ],
            }
            manifest = {
                "normalized_execution_projection": {
                    "successor_execution_allowed": False,
                },
                "consumer_rehearsal": {
                    "stages": [first_stage, successor_stage],
                },
            }
            group_absence_confirmed: list[bool] = []
            wait_for_group_exit = runner._wait_for_stage_process_group_exit
            remove_tree = shutil.rmtree

            def recording_wait(process_group_id: int, timeout_seconds: float) -> bool:
                result = wait_for_group_exit(process_group_id, timeout_seconds)
                group_absence_confirmed.append(result)
                return result

            def remove_after_confirmed_absence(path: Path) -> None:
                self.assertEqual(group_absence_confirmed, [True])
                remove_tree(path)

            with (
                mock.patch.object(
                    runner.tempfile,
                    "mkdtemp",
                    return_value=str(rehearsal_root),
                ),
                mock.patch.object(
                    runner,
                    "_wait_for_stage_process_group_exit",
                    side_effect=recording_wait,
                ),
                mock.patch.object(
                    runner.shutil,
                    "rmtree",
                    side_effect=remove_after_confirmed_absence,
                ) as remove_root,
            ):
                results, blockers = runner.run_stages(manifest, root)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["exit_code"], 7)
            self.assertEqual(results[0]["result"], "block")
            self.assertTrue(
                any("consumer stage failed with exit 7" in item for item in blockers)
            )
            self.assertTrue(
                any(
                    "owned-group residue blocked closure" in item
                    and "direct stage leader exited 7" in item
                    and "residue was terminated and group absence confirmed" in item
                    for item in blockers
                )
            )
            self.assertFalse(successor.exists())
            self.assertEqual(group_absence_confirmed, [True])
            remove_root.assert_called_once_with(rehearsal_root)
            self.assertFalse(rehearsal_root.exists())
            time.sleep(1.1)
            self.assertFalse(late_write.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

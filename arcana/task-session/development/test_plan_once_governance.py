#!/usr/bin/env python3
"""Governance-runner enforcement for single-use plan admission."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


TASK_SESSION = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


HARNESS = load_module(
    "task_session_governance_harness",
    TASK_SESSION / "development/validate-governance-runner.py",
)
CONTRACTS = load_module(
    "task_session_governance_contracts",
    TASK_SESSION / "development/validate-governance-run-contracts.py",
)
FAST = load_module(
    "task_session_fast_entry_fixture",
    TASK_SESSION / "development/test_fast_execution_entry_guard.py",
)


def canonical_digest(value) -> str:
    return hashlib.sha256(
        json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()


def run(
    repo: Path,
    command: str,
    request: str,
    run_dir: str,
    joined_receipt: str | None = None,
):
    argv = [
        sys.executable,
        str(repo / "arcanum/arcana/task-session/scripts/task-session-governance-runner.py"),
        command,
        "--repo-root",
        str(repo),
        "--run-dir",
        run_dir,
    ]
    if command == "prepare":
        argv.extend(["--request", request])
    if command == "executor-join" and joined_receipt is not None:
        argv.extend(["--receipt", joined_receipt])
    completed = subprocess.run(
        argv,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return completed.returncode, json.loads(completed.stdout)


class PlanOnceGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.temp_root = Path(self.temporary.name)
        self.repo = HARNESS.executor_scenario(
            self.temp_root,
            TASK_SESSION,
            TASK_SESSION,
            "plan-once",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def activate_profile(self) -> tuple[dict, Path]:
        request_path = self.repo / "scenario/request.json"
        request = HARNESS.load_json(request_path)
        epoch = "epoch-" + "c" * 24
        unit_digest = "b" * 64
        selection_path = self.repo / "scenario/controls/selection.json"
        HARNESS.write_json(
            selection_path,
            {
                "schemaVersion": "1.0.0",
                "selectionVerdict": "select",
                "terminalCode": "SELECTION_READY",
                "taskId": request["task_id"],
                "swuId": request["swu_id"],
                "planEpochId": epoch,
                "unitContractDigest": unit_digest,
                "mutationReady": False,
                "authorityEffect": "none",
            },
        )
        validation_digest = canonical_digest(
            request["execution_contract"]["validation_commands"]
        )
        baselines = [
            {
                "path": "outputs/artifact.txt",
                "state": "absent",
                "sha256": None,
                "sizeBytes": None,
            }
        ]
        baseline_digest = canonical_digest(baselines)
        admission_path = self.repo / "scenario/controls/admission.json"
        admission_token = "a" * 64
        HARNESS.write_json(
            admission_path,
            {
                "schemaVersion": "1.2.0",
                "admissionProfile": "plan-once-selected-unit",
                "executionMode": "reusable-mutation",
                "writeProfile": "material-bound",
                "admissionVerdict": "admit",
                "mutationReady": True,
                "taskId": request["task_id"],
                "swuId": request["swu_id"],
                "planEpochId": epoch,
                "unitContractDigest": unit_digest,
                "attemptId": request["run_id"],
                "admissionToken": admission_token,
                "targetBaselineDigest": baseline_digest,
                "targetBaselines": baselines,
                "validationContractDigest": validation_digest,
                "singleUse": True,
                "reasons": [],
            },
        )
        admission_ref = HARNESS.exact_ref(self.repo, admission_path)
        selection_ref = HARNESS.exact_ref(self.repo, selection_path)
        request["control_refs"] = [
            reference
            for reference in request["control_refs"]
            if reference["path"] != "scenario/controls/admission.json"
        ]
        request["control_refs"].extend([admission_ref, selection_ref])
        ledger = (
            "scenario/controls/.admission-consumption/"
            f"{admission_ref['sha256']}.json"
        )
        request["admission_profile"] = "plan-once-selected-unit"
        request["plan_admission"] = {
            "plan_epoch_id": epoch,
            "unit_contract_digest": unit_digest,
            "attempt_id": request["run_id"],
            "selection_receipt_ref": selection_ref,
            "mutation_admission_receipt_ref": admission_ref,
            "admission_token": admission_token,
            "target_baseline_digest": baseline_digest,
            "validation_contract_digest": validation_digest,
            "consumption_ledger_path": ledger,
        }
        HARNESS.write_json(request_path, request)
        return request, request_path

    def activate_fast_profile(
        self,
        route_write_scope: list[str] | None = None,
        entry_state: str = "task-ready",
    ) -> tuple[dict, Path]:
        request, request_path = self.activate_profile()
        work_pack_path = self.repo / request["work_pack_ref"]["path"]
        work_pack_path.write_text(
            work_pack_path.read_text(encoding="utf-8").replace(
                "| selected |\n", "| ready |\n"
            ),
            encoding="utf-8",
        )
        request["work_pack_ref"] = HARNESS.exact_ref(self.repo, work_pack_path)

        terminal_output = request["closeout_contract"]["terminal_receipt_path"]
        route_scope = (
            request["execution_contract"]["allowed_writes"]
            if route_write_scope is None
            else route_write_scope
        )
        routes = [
            {
                "route_id": "route-task",
                "frontier_swu": request["swu_id"],
                "capability": "task-session",
                "mode": "execute",
                "target": request["swu_id"],
                "write_scope": [*route_scope, terminal_output],
                "effect_class": "repository-local-reversible",
                "required_inputs": ["plan-manifest", "selection-receipt"],
                "expected_receipt": request["closeout_contract"][
                    "terminal_receipt_path"
                ],
            }
        ]
        policy = {
            "schema_version": "1.0.0",
            "work_pack_id": "WP-PLAN-ONCE-FAST-ENTRY",
            "work_pack_semantic_digest": canonical_digest(
                {"work_pack": "synthetic-fast-entry"}
            ),
            "frontier": [request["swu_id"]],
            "allowed_routes": routes,
            "allowed_routes_digest": FAST.allowed_routes_digest(routes),
            "automatic_decisions": [
                "internal-tool-selection",
                "capability-owner-routing",
            ],
            "stop_decisions": [
                "scope-expansion",
                "failed-acceptance-critical-validation",
            ],
            "validation_commands": ["python3 validate.py"],
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
            "authority_effect": "none",
        }
        projection = {
            "schema_version": "1.0.0",
            "work_pack_id": policy["work_pack_id"],
            "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
            "allowed_routes_digest": policy["allowed_routes_digest"],
            "entry_state": entry_state,
            "selected_unit": request["swu_id"],
            "route_id": "route-task",
            "next_owner": {
                "capability": "task-session",
                "mode": "execute",
                "target": request["swu_id"],
            },
            "blocker_code": None,
            "authority_effect": "none",
        }
        binding = FAST.build_execution_intent_binding(
            policy,
            projection,
            source_invocation_id="synthetic-fast-entry-001",
            created_at="2026-08-05T00:00:00Z",
            execution_mode="one-unit",
        )
        fast_request = {
            "schema_version": "1.0.0",
            "execution_policy": policy,
            "execution_entry": projection,
            "execution_binding": binding,
            "selected_unit": {
                "work_pack_id": policy["work_pack_id"],
                "swu_id": request["swu_id"],
            },
            "authority_effect": "none",
        }
        fast_request_path = self.repo / "scenario/controls/fast-entry-request.json"
        HARNESS.write_json(fast_request_path, fast_request)
        fast_receipt_path = self.repo / "scenario/controls/fast-entry.json"
        HARNESS.write_json(
            fast_receipt_path, FAST.classify_fast_entry(fast_request)
        )

        selection_path = self.repo / request["plan_admission"][
            "selection_receipt_ref"
        ]["path"]
        selection = HARNESS.load_json(selection_path)
        selection.update(
            {
                "requestDigest": "1" * 64,
                "manifestDigest": "2" * 64,
                "canonicalSemanticDigest": policy["work_pack_semantic_digest"],
                "dependencyReceiptDigests": [],
                "lifecycleEligibilityDigest": "3" * 64,
                "explicitConfirmationDigest": None,
                "selectionIntentSource": "execution-intent-binding",
                "selectionIntentDigest": canonical_digest(
                    {
                        "bindingId": binding["binding_id"],
                        "sourceInvocationId": binding["source_invocation_id"],
                        "workPackId": binding["work_pack_id"],
                        "bindingDigest": binding["binding_digest"],
                        "authorityEffect": "bounded-execution-only",
                    }
                ),
                "reasons": [],
            }
        )
        HARNESS.write_json(selection_path, selection)
        selection_ref = HARNESS.exact_ref(self.repo, selection_path)

        admission_path = self.repo / request["plan_admission"][
            "mutation_admission_receipt_ref"
        ]["path"]
        admission = HARNESS.load_json(admission_path)
        material_writes = request["execution_contract"]["allowed_writes"]
        terminal_output = request["closeout_contract"]["terminal_receipt_path"]
        admission.update(
            {
                "requestDigest": "4" * 64,
                "producerSchemaDigest": "5" * 64,
                "materialReceiptDigest": "6" * 64,
                "materialPackageDigest": "7" * 64,
                "controllingPaths": [request["work_pack_ref"]["path"]],
                "dependencyIds": [],
                "materialWrites": material_writes,
                "executionOutputs": [terminal_output],
                "allowedWrites": material_writes + [terminal_output],
                "validationCommands": ["python3 validate.py"],
                "lifecycleOwner": "task-session",
                "authorityClass": "public",
                "publicationClass": "public",
                "planManifestDigest": "8" * 64,
                "selectionReceiptDigest": selection_ref["sha256"],
                "liveValidationRequired": True,
            }
        )
        HARNESS.write_json(admission_path, admission)
        admission_ref = HARNESS.exact_ref(self.repo, admission_path)

        replaced = {
            request["plan_admission"]["selection_receipt_ref"]["path"]: selection_ref,
            request["plan_admission"]["mutation_admission_receipt_ref"]["path"]: admission_ref,
        }
        request["control_refs"] = [
            replaced.get(reference["path"], reference)
            for reference in request["control_refs"]
        ]
        request["entry_profile"] = "work-pack-fast-entry"
        request["fast_execution_entry"] = {
            "request_ref": HARNESS.exact_ref(self.repo, fast_request_path),
            "receipt_ref": HARNESS.exact_ref(self.repo, fast_receipt_path),
        }
        request["plan_admission"]["selection_receipt_ref"] = selection_ref
        request["plan_admission"]["mutation_admission_receipt_ref"] = admission_ref
        request["plan_admission"]["consumption_ledger_path"] = (
            "scenario/controls/.admission-consumption/"
            f"{admission_ref['sha256']}.json"
        )
        HARNESS.write_json(request_path, request)
        return request, request_path

    def activate_output_only_fast_profile(self) -> tuple[dict, Path]:
        request, request_path = self.activate_fast_profile()
        admission_path = self.repo / request["plan_admission"][
            "mutation_admission_receipt_ref"
        ]["path"]
        admission = HARNESS.load_json(admission_path)
        output_paths = request["execution_contract"]["allowed_writes"]
        admission.update(
            {
                "writeProfile": "execution-output-only",
                "producerSchemaDigest": None,
                "materialReceiptDigest": None,
                "materialPackageDigest": None,
                "materialWrites": [],
                "executionOutputs": output_paths,
                "allowedWrites": output_paths,
            }
        )
        HARNESS.write_json(admission_path, admission)
        admission_ref = HARNESS.exact_ref(self.repo, admission_path)
        request["control_refs"] = [
            admission_ref
            if reference["path"] == admission_ref["path"]
            else reference
            for reference in request["control_refs"]
        ]
        request["plan_admission"]["mutation_admission_receipt_ref"] = admission_ref
        request["plan_admission"]["consumption_ledger_path"] = (
            "scenario/controls/.admission-consumption/"
            f"{admission_ref['sha256']}.json"
        )
        HARNESS.write_json(request_path, request)
        return request, request_path

    def set_executor_behavior(self, behavior: str) -> None:
        request_path = self.repo / "scenario/request.json"
        request = HARNESS.load_json(request_path)
        config_path = self.repo / "scenario/controls/executor-config.json"
        config = HARNESS.load_json(config_path)
        config["argv"][-1] = behavior
        HARNESS.write_json(config_path, config)
        config_ref = HARNESS.exact_ref(self.repo, config_path)
        request["control_refs"] = [
            config_ref if item["path"] == config_ref["path"] else item
            for item in request["control_refs"]
        ]
        HARNESS.write_json(request_path, request)

    def set_executor_receipt_path(self, expected_receipt_path: str) -> None:
        request_path = self.repo / "scenario/request.json"
        request = HARNESS.load_json(request_path)
        config_path = self.repo / "scenario/controls/executor-config.json"
        config = HARNESS.load_json(config_path)
        config["expected_receipt_path"] = expected_receipt_path
        HARNESS.write_json(config_path, config)
        config_ref = HARNESS.exact_ref(self.repo, config_path)
        request["control_refs"] = [
            config_ref if item["path"] == config_ref["path"] else item
            for item in request["control_refs"]
        ]
        HARNESS.write_json(request_path, request)

    def assert_no_executor_or_admission_effects(
        self,
        request: dict,
        *additional_paths: str,
    ) -> None:
        ledger = self.repo / request["plan_admission"][
            "consumption_ledger_path"
        ]
        self.assertFalse(ledger.exists())
        paths = [
            *request["execution_contract"]["allowed_writes"],
            *request["execution_contract"]["declared_outputs"],
            *[
                item["path"]
                for item in request["execution_contract"].get(
                    "transient_outputs", []
                )
            ],
            request["closeout_contract"]["terminal_receipt_path"],
            "runs/run-1/terminal-executor-receipt.json",
            *additional_paths,
        ]
        for relative in paths:
            self.assertFalse(
                (self.repo / relative).exists(),
                f"unexpected executor or admission effect: {relative}",
            )

    def activate_pre_execution_reservation(
        self,
        consumption_ledger_path: str,
        resume_receipt_path: str,
    ) -> tuple[dict, Path]:
        request_path = self.repo / "scenario/request.json"
        request = HARNESS.load_json(request_path)
        source_ref = request["control_refs"][0]
        request["entry_profile"] = "pre-execution-prerequisite"
        request.pop("fast_execution_entry", None)
        request["pre_execution_prerequisite"] = {
            "attempt_id": request["run_id"],
            "prerequisite_fingerprint": "f" * 64,
            "classification_receipt_ref": source_ref,
            "continuation_route_receipt_ref": source_ref,
            "owner_receipt_ref": source_ref,
            "owner_receipt_schema_ref": source_ref,
            "route": "invoke:refresh:apply-approved",
            "target_inventory": [
                {
                    "path": "outputs/artifact.txt",
                    "state": "absent",
                    "sha256": None,
                    "size_bytes": None,
                }
            ],
            "expected_package_id": "synthetic-pre-execution-package",
            "expected_package_digest": "e" * 64,
            "expected_owner_validation_commands": ["python3 validate.py"],
            "satisfaction_predicate": {
                "kind": "json-pointer-any-of",
                "receipt_pointer": "/result",
                "accepted_values": ["pass"],
            },
            "resume_point": "task-session:context-build",
            "max_owner_hops": 1,
            "allowed_effect": "pre-execution-prerequisite-resolution",
            "consumption_ledger_path": consumption_ledger_path,
            "resume_receipt_path": resume_receipt_path,
        }
        HARNESS.write_json(request_path, request)
        return request, request_path

    def activate_transient_fast_profile(self) -> tuple[dict, Path]:
        transient_path = "scratch/cargo-target"
        request, request_path = self.activate_fast_profile(
            route_write_scope=["outputs/artifact.txt", transient_path]
        )
        request["execution_contract"]["transient_outputs"] = [
            {
                "path": transient_path,
                "path_kind": "directory",
                "pre_execution_state": "absent",
                "touch_evidence": "required",
                "cleanup_policy": "remove-before-executor-receipt",
                "terminal_state": "absent",
            }
        ]
        admission_path = self.repo / request["plan_admission"][
            "mutation_admission_receipt_ref"
        ]["path"]
        admission = HARNESS.load_json(admission_path)
        terminal = request["closeout_contract"]["terminal_receipt_path"]
        materials = request["execution_contract"]["allowed_writes"]
        admission.update(
            {
                "schemaVersion": "1.3.0",
                "transientOutputs": [transient_path],
                "executionOutputs": [terminal, transient_path],
                "allowedWrites": [*materials, terminal, transient_path],
            }
        )
        HARNESS.write_json(admission_path, admission)
        admission_ref = HARNESS.exact_ref(self.repo, admission_path)
        request["control_refs"] = [
            admission_ref if item["path"] == admission_ref["path"] else item
            for item in request["control_refs"]
        ]
        request["plan_admission"]["mutation_admission_receipt_ref"] = admission_ref
        request["plan_admission"]["consumption_ledger_path"] = (
            "scenario/controls/.admission-consumption/"
            f"{admission_ref['sha256']}.json"
        )
        HARNESS.write_json(request_path, request)
        return request, request_path

    def rewrite_plan_admission(self, transform) -> tuple[dict, Path]:
        request_path = self.repo / "scenario/request.json"
        request = HARNESS.load_json(request_path)
        admission_path = self.repo / request["plan_admission"][
            "mutation_admission_receipt_ref"
        ]["path"]
        admission = HARNESS.load_json(admission_path)
        transform(admission)
        HARNESS.write_json(admission_path, admission)
        admission_ref = HARNESS.exact_ref(self.repo, admission_path)
        request["control_refs"] = [
            admission_ref if item["path"] == admission_ref["path"] else item
            for item in request["control_refs"]
        ]
        request["plan_admission"]["mutation_admission_receipt_ref"] = admission_ref
        request["plan_admission"]["consumption_ledger_path"] = (
            "scenario/controls/.admission-consumption/"
            f"{admission_ref['sha256']}.json"
        )
        HARNESS.write_json(request_path, request)
        return request, request_path

    def test_ticket_binds_admission_and_atomic_consumption_blocks_second_run(self) -> None:
        request, request_path = self.activate_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(ticket["admission_profile"], "plan-once-selected-unit")
        self.assertEqual(
            ticket["plan_admission"]["admission_token"],
            request["plan_admission"]["admission_token"],
        )
        code, joined = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, joined)
        ledger_path = self.repo / request["plan_admission"]["consumption_ledger_path"]
        self.assertTrue(ledger_path.is_file())

        # Restore the admitted absent target so the second attempt reaches the
        # atomic single-use ledger instead of failing on baseline drift.
        (self.repo / "outputs/artifact.txt").unlink()
        config_path = self.repo / "scenario/controls/executor-config.json"
        config = HARNESS.load_json(config_path)
        config["expected_receipt_path"] = "runs/run-2/terminal-executor-receipt.json"
        HARNESS.write_json(config_path, config)
        second = json.loads(json.dumps(request))
        second["control_refs"] = [
            HARNESS.exact_ref(self.repo, config_path)
            if item["path"] == "scenario/controls/executor-config.json"
            else item
            for item in second["control_refs"]
        ]
        second_path = self.repo / "scenario/request-2.json"
        HARNESS.write_json(second_path, second)
        code, prepared_two = run(
            self.repo, "prepare", "scenario/request-2.json", "runs/run-2"
        )
        self.assertEqual(code, 0, prepared_two)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request-2.json", "runs/run-2"
        )
        self.assertEqual(code, 2, blocked)
        self.assertEqual(blocked["result"], "block")
        self.assertIn("already consumed", " ".join(blocked["diagnostics"]))

    def test_fast_entry_bypasses_only_prose_selector_and_consumes_plan_once(self) -> None:
        request, _ = self.activate_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        self.assertEqual(prepared["entry_profile"], "work-pack-fast-entry")
        self.assertFalse(prepared["selector_resolution_reentered"])
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(ticket["entry_profile"], "work-pack-fast-entry")
        self.assertEqual(
            ticket["fast_execution_entry"]["request_ref"],
            request["fast_execution_entry"]["request_ref"],
        )
        self.assertEqual(
            ticket["fast_execution_entry"]["receipt_ref"],
            request["fast_execution_entry"]["receipt_ref"],
        )
        code, joined = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, joined)
        ledger = self.repo / request["plan_admission"]["consumption_ledger_path"]
        self.assertTrue(ledger.is_file())

    def test_context_entry_runs_full_plan_once_admission_before_mutation(self) -> None:
        request, _ = self.activate_fast_profile(entry_state="context-ready")
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        self.assertEqual(prepared["entry_profile"], "work-pack-fast-entry")
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(ticket["admission_profile"], "plan-once-selected-unit")
        self.assertEqual(
            ticket["plan_admission"]["mutation_admission_receipt_ref"],
            request["plan_admission"]["mutation_admission_receipt_ref"],
        )
        code, joined = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, joined)
        ledger = self.repo / request["plan_admission"]["consumption_ledger_path"]
        self.assertTrue(ledger.is_file())

    def test_fast_entry_output_only_binds_and_consumes_plan_once(self) -> None:
        request, _ = self.activate_output_only_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(ticket["entry_profile"], "work-pack-fast-entry")
        self.assertEqual(ticket["admission_profile"], "plan-once-selected-unit")
        code, joined = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, joined)
        ledger = self.repo / request["plan_admission"]["consumption_ledger_path"]
        self.assertTrue(ledger.is_file())

    def test_fast_entry_output_only_rejects_terminal_receipt_partition(self) -> None:
        request, request_path = self.activate_output_only_fast_profile()
        request["execution_contract"]["allowed_writes"].append(
            request["closeout_contract"]["terminal_receipt_path"]
        )
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("duplicates the terminal receipt", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_is_admitted_touched_cleaned_and_absent(self) -> None:
        request, _ = self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(
            ticket["transient_outputs"],
            request["execution_contract"]["transient_outputs"],
        )
        code, joined = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, joined)
        receipt = HARNESS.load_json(
            self.repo / "runs/run-1/terminal-executor-receipt.json"
        )
        self.assertEqual(
            [item["path"] for item in receipt["transient_results"]],
            ["scratch/cargo-target"],
        )
        self.assertFalse((self.repo / "scratch/cargo-target").exists())

    def test_transient_output_collision_blocks_before_run_write(self) -> None:
        _, _ = self.activate_transient_fast_profile()
        (self.repo / "scratch/cargo-target").mkdir(parents=True)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("pre-execution state", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_overlap_blocks_before_run_write(self) -> None:
        request, request_path = self.activate_transient_fast_profile()
        request["execution_contract"]["transient_outputs"][0]["path"] = "outputs"
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("overlaps durable", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_escape_blocks_before_run_write(self) -> None:
        request, request_path = self.activate_transient_fast_profile()
        request["execution_contract"]["transient_outputs"][0]["path"] = "../escape"
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("escapes repository root", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_symlink_chain_blocks_before_run_write(self) -> None:
        self.activate_transient_fast_profile()
        (self.repo / "scratch-real").mkdir()
        (self.repo / "scratch").symlink_to("scratch-real", target_is_directory=True)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("symbolic link", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_run_directory_overlap_blocks_before_run_write(self) -> None:
        request, request_path = self.activate_transient_fast_profile()
        request["execution_contract"]["transient_outputs"][0]["path"] = (
            "runs/run-1"
        )
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("run directory", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_plan_ledger_overlap_blocks_before_run_write(self) -> None:
        request, request_path = self.activate_transient_fast_profile()
        request["execution_contract"]["transient_outputs"][0]["path"] = request[
            "plan_admission"
        ]["consumption_ledger_path"]
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "plan admission consumption ledger", " ".join(blocked["diagnostics"])
        )
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_prerequisite_ledger_overlap_blocks_before_run_write(
        self,
    ) -> None:
        request, request_path = self.activate_transient_fast_profile()
        ledger = "runs/run-1/pre-execution-consumption.json"
        receipt = "runs/run-1/pre-execution-resume-receipt.json"
        request["execution_contract"]["transient_outputs"][0]["path"] = ledger
        HARNESS.write_json(request_path, request)
        self.activate_pre_execution_reservation(ledger, receipt)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "pre-execution prerequisite consumption ledger",
            " ".join(blocked["diagnostics"]),
        )
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_output_prerequisite_receipt_overlap_blocks_before_run_write(
        self,
    ) -> None:
        request, request_path = self.activate_transient_fast_profile()
        ledger = "runs/run-1/pre-execution-consumption.json"
        receipt = "runs/run-1/pre-execution-resume-receipt.json"
        request["execution_contract"]["transient_outputs"][0]["path"] = receipt
        HARNESS.write_json(request_path, request)
        self.activate_pre_execution_reservation(ledger, receipt)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "pre-execution prerequisite resume receipt",
            " ".join(blocked["diagnostics"]),
        )
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_external_executor_receipt_path_rejected_by_run_scoped_invariant(
        self,
    ) -> None:
        self.activate_fast_profile()
        self.set_executor_receipt_path("scratch/cargo-target")
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("run-scoped terminal path", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_tampered_ticket_executor_receipt_path_blocks_launch(self) -> None:
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket_path = self.repo / "runs/run-1/execution-ticket.json"
        ticket = HARNESS.load_json(ticket_path)
        ticket["executor_contract"]["expected_receipt_path"] = (
            "scratch/external-executor-receipt.json"
        )
        HARNESS.write_json(ticket_path, ticket)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("run-scoped terminal path", " ".join(blocked["diagnostics"]))

    def test_tampered_ticket_prerequisite_reservation_blocks_receipt_join(
        self,
    ) -> None:
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        self.assertEqual(HARNESS.run_executor_helper(self.repo), 0)
        ticket_path = self.repo / "runs/run-1/execution-ticket.json"
        ticket = HARNESS.load_json(ticket_path)
        ticket["transient_outputs"][0]["path"] = (
            "runs/run-1/pre-execution-consumption.json"
        )
        HARNESS.write_json(ticket_path, ticket)
        code, blocked = run(
            self.repo,
            "executor-join",
            "scenario/request.json",
            "runs/run-1",
            joined_receipt="runs/run-1/terminal-executor-receipt.json",
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "pre-execution prerequisite consumption ledger",
            " ".join(blocked["diagnostics"]),
        )

    def test_ticket_only_transient_substitution_blocks_before_executor_launch(
        self,
    ) -> None:
        request, _ = self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket_path = self.repo / "runs/run-1/execution-ticket.json"
        ticket = HARNESS.load_json(ticket_path)
        substituted = "scratch/non-reserved-substitution"
        ticket["transient_outputs"][0]["path"] = substituted
        HARNESS.write_json(ticket_path, ticket)

        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "TASK_SESSION_TICKET_CHECKPOINT_REF_STALE",
            " ".join(blocked["diagnostics"]),
        )
        self.assert_no_executor_or_admission_effects(request, substituted)

    def test_ticket_and_checkpoint_transient_substitution_blocks_before_launch(
        self,
    ) -> None:
        request, _ = self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket_path = self.repo / "runs/run-1/execution-ticket.json"
        ticket = HARNESS.load_json(ticket_path)
        substituted = "scratch/non-reserved-substitution"
        ticket["transient_outputs"][0]["path"] = substituted
        HARNESS.write_json(ticket_path, ticket)
        ticket_ref = HARNESS.exact_ref(self.repo, ticket_path)

        ticketed_path = self.repo / "runs/run-1/checkpoints/04-ticketed.json"
        ticketed = HARNESS.load_json(ticketed_path)
        ticketed["input_refs"][-1] = ticket_ref
        ticketed["output_refs"] = [ticket_ref]
        HARNESS.write_json(ticketed_path, ticketed)

        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn(
            "TASK_SESSION_TICKET_TRANSIENT_CLOSURE_DRIFT",
            " ".join(blocked["diagnostics"]),
        )
        self.assert_no_executor_or_admission_effects(request, substituted)

    def test_durable_staging_output_cannot_be_mislabeled_transient(self) -> None:
        request, request_path = self.activate_transient_fast_profile()
        request["execution_contract"]["transient_outputs"][0]["path"] = (
            request["execution_contract"]["declared_outputs"][0]
        )
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("overlaps durable", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_admission_omission_blocks_before_run_write(self) -> None:
        self.activate_transient_fast_profile()
        self.rewrite_plan_admission(lambda admission: admission.pop("transientOutputs"))
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("schema invalid", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_transient_admission_inflation_blocks_before_run_write(self) -> None:
        self.activate_transient_fast_profile()

        def inflate(admission):
            admission["transientOutputs"].append("scratch/extra")
            admission["executionOutputs"].append("scratch/extra")
            admission["allowedWrites"].append("scratch/extra")

        self.rewrite_plan_admission(inflate)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("transient", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_missing_transient_evidence_blocks_join(self) -> None:
        self.set_executor_behavior("missing-transient-evidence")
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("lacks transient", " ".join(blocked["diagnostics"]))

    def test_substituted_transient_evidence_blocks_join(self) -> None:
        self.set_executor_behavior("substituted-transient-evidence")
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("differs from ticket", " ".join(blocked["diagnostics"]))

    def test_transient_residue_blocks_join(self) -> None:
        self.set_executor_behavior("transient-residue")
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("residue", " ".join(blocked["diagnostics"]))

    def test_false_transient_cleanup_evidence_blocks_join(self) -> None:
        self.set_executor_behavior("false-transient-cleanup")
        self.activate_transient_fast_profile()
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        code, blocked = run(
            self.repo, "executor-join", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("schema invalid", " ".join(blocked["diagnostics"]))

    def test_fast_entry_narrows_directory_route_scope_to_exact_material_file(self) -> None:
        request, _ = self.activate_fast_profile(route_write_scope=["outputs"])
        code, prepared = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 0, prepared)
        ticket = HARNESS.load_json(self.repo / "runs/run-1/execution-ticket.json")
        self.assertEqual(ticket["allowed_writes"], ["outputs/artifact.txt"])
        self.assertEqual(
            request["execution_contract"]["allowed_writes"],
            ["outputs/artifact.txt"],
        )

    def test_stale_fast_entry_receipt_blocks_before_run_writes(self) -> None:
        request, request_path = self.activate_fast_profile()
        request["fast_execution_entry"]["receipt_ref"]["sha256"] = "0" * 64
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_stale_fast_entry_request_blocks_before_run_writes(self) -> None:
        request, request_path = self.activate_fast_profile()
        request["fast_execution_entry"]["request_ref"]["sha256"] = "0" * 64
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_fast_entry_identity_mismatch_blocks_before_run_writes(self) -> None:
        request, request_path = self.activate_fast_profile()
        receipt_path = self.repo / request["fast_execution_entry"]["receipt_ref"][
            "path"
        ]
        receipt = HARNESS.load_json(receipt_path)
        receipt["selected_unit"] = "SWU-FOREIGN-002"
        HARNESS.write_json(receipt_path, receipt)
        request["fast_execution_entry"]["receipt_ref"] = HARNESS.exact_ref(
            self.repo, receipt_path
        )
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_fast_entry_write_expansion_blocks_before_run_writes(self) -> None:
        request, request_path = self.activate_fast_profile()
        request["execution_contract"]["allowed_writes"].append(
            "outputs/expanded.txt"
        )
        HARNESS.write_json(request_path, request)
        code, blocked = run(
            self.repo, "prepare", "scenario/request.json", "runs/run-1"
        )
        self.assertEqual(code, 2, blocked)
        self.assertIn("governance route", " ".join(blocked["diagnostics"]))
        self.assertFalse((self.repo / "runs/run-1").exists())

    def test_terminal_contract_requires_consumed_admission_identity(self) -> None:
        documents = CONTRACTS.build_documents()
        request = documents["governance-run-request"]
        ticket = documents["execution-ticket"]
        terminal = documents["governance-terminal-receipt"]
        admission_ref = CONTRACTS.exact_ref("run/admission.json", "7", 117)
        selection_ref = CONTRACTS.exact_ref("run/selection.json", "8", 118)
        common = {
            "plan_epoch_id": "epoch-" + "c" * 24,
            "unit_contract_digest": "b" * 64,
            "attempt_id": request["run_id"],
            "selection_receipt_ref": selection_ref,
            "mutation_admission_receipt_ref": admission_ref,
            "admission_token": "a" * 64,
            "target_baseline_digest": "d" * 64,
            "validation_contract_digest": "e" * 64,
            "consumption_ledger_path": "run/.admission-consumption/receipt.json",
        }
        request["admission_profile"] = "plan-once-selected-unit"
        request["plan_admission"] = common
        ticket["admission_profile"] = "plan-once-selected-unit"
        ticket["plan_admission"] = {
            **common,
            "target_baselines": [
                {
                    "path": "src/module.py",
                    "state": "absent",
                    "sha256": None,
                    "size_bytes": None,
                }
            ],
        }
        terminal["admission_profile"] = "plan-once-selected-unit"
        terminal["consumed_admission"] = {
            "receipt_ref": admission_ref,
            "admission_token": common["admission_token"],
            "attempt_id": common["attempt_id"],
            "consumption_ledger_ref": CONTRACTS.exact_ref(
                "run/.admission-consumption/receipt.json", "9", 119
            ),
        }
        fast_request_ref = CONTRACTS.exact_ref(
            "run/fast-entry-request.json", "a", 120
        )
        fast_ref = CONTRACTS.exact_ref("run/fast-entry.json", "b", 121)
        provenance = {
            "request_ref": fast_request_ref,
            "receipt_ref": fast_ref,
            "binding_id": "wpeb-" + "c" * 24,
            "binding_digest": "c" * 64,
            "route_fingerprint": "d" * 64,
            "work_pack_semantic_digest": "e" * 64,
        }
        request["entry_profile"] = "work-pack-fast-entry"
        request["fast_execution_entry"] = {
            "request_ref": fast_request_ref,
            "receipt_ref": fast_ref,
        }
        ticket["entry_profile"] = "work-pack-fast-entry"
        ticket["fast_execution_entry"] = provenance
        terminal["entry_profile"] = "work-pack-fast-entry"
        terminal["fast_execution_entry"] = provenance
        for name in (
            "governance-run-request",
            "execution-ticket",
            "governance-terminal-receipt",
        ):
            schema = json.loads(
                (TASK_SESSION / f"schemas/{name}.schema.json").read_text()
            )
            self.assertEqual(
                list(Draft202012Validator(schema).iter_errors(documents[name])),
                [],
            )
        self.assertEqual(CONTRACTS.semantic_errors(documents), [])

        terminal.pop("consumed_admission")
        schema = json.loads(
            (TASK_SESSION / "schemas/governance-terminal-receipt.schema.json").read_text()
        )
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(terminal)))


if __name__ == "__main__":
    unittest.main(verbosity=2)

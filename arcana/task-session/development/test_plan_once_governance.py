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


def run(repo: Path, command: str, request: str, run_dir: str):
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
        self, route_write_scope: list[str] | None = None
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

        routes = [
            {
                "route_id": "route-task",
                "frontier_swu": request["swu_id"],
                "capability": "task-session",
                "mode": "execute",
                "target": request["swu_id"],
                "write_scope": (
                    request["execution_contract"]["allowed_writes"]
                    if route_write_scope is None
                    else route_write_scope
                ),
                "effect_class": "repository-local-reversible",
                "required_inputs": ["plan-manifest", "selection-receipt"],
                "expected_receipt": request["closeout_contract"][
                    "terminal_receipt_path"
                ],
            }
        ]
        policy = {
            "schema_version": "1.0.0",
            "work_pack_id": request["work_pack_ref"]["path"],
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
            "entry_state": "task-ready",
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

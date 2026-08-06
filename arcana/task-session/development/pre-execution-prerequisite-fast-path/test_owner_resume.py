#!/usr/bin/env python3
"""Acceptance tests for joined owner receipt verification and same-attempt resume."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RUNNER_PATH = REPO / "arcana" / "task-session" / "scripts" / "task-session-governance-runner.py"
SPEC = importlib.util.spec_from_file_location("task_session_governance_runner", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUNNER
SPEC.loader.exec_module(RUNNER)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ref(root: Path, path: Path) -> dict:
    return RUNNER.exact_ref(root, path)


def build_case(root: Path, variant: str = "pass") -> tuple[Path, Path]:
    controls = root / "controls"
    controls.mkdir(parents=True, exist_ok=True)
    owner_schema_path = controls / "owner-receipt.schema.json"
    owner_schema_path.write_text(
        (REPO / "spells" / "invoke" / "schemas" / "material-package-receipt.schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    auth_path = controls / "authorization.json"
    write_json(auth_path, {"authorization": "exact-prerequisite-route"})
    auth_ref = ref(root, auth_path)

    target_inventory = [{"path": "target.txt", "state": "absent", "sha256": None, "size_bytes": None}]
    validation_contracts = [{
        "command_id": "validate-target",
        "argv": ["python3", "validate.py"],
        "cwd": ".",
        "timeout_seconds": 30,
        "max_output_bytes": 65536,
    }]
    predicate = {"kind": "json-pointer-any-of", "receipt_pointer": "/patchVerdict", "accepted_values": ["pass"]}
    fingerprint = "a" * 64
    attempt = "attempt-owner-resume-001"

    classification_path = controls / "classification.json"
    classification = {
        "schema_version": "task-session.pre-execution-prerequisite-receipt.v1",
        "receipt_id": "classification-owner-resume-001",
        "prerequisite_id": "PEP-GENERIC-001",
        "task_id": "TASK-GENERIC-001",
        "swu_id": "SWU-GENERIC-001",
        "attempt_id": attempt,
        "classification": "unmet",
        "prerequisite_fingerprint": fingerprint,
        "inputs_read": ["work-pack", "selected-unit", "prerequisite"],
        "authorization": {"status": "matched", "evidence_ref": auth_ref},
        "permitted_next_action": "route-one-owner-hop",
        "phase_trace": {
            "resolved": True,
            "prerequisite_classified": True,
            "context_builder_entered": False,
            "mutation_admission_entered": False,
            "implementation_inspected": False,
            "target_mutation_entered": False,
            "owner_hops_dispatched": 0,
        },
        "reasons": [],
    }
    write_json(classification_path, classification)
    classification_ref = ref(root, classification_path)

    package_digest = "4" * 64
    owner_path = controls / "owner-receipt.json"
    owner_receipt = {
        "schemaVersion": "1.0.0",
        "packageId": "package-generic-001",
        "patchVerdict": "pass",
        "mutationHandoff": "ready",
        "packageDigest": package_digest,
        "validatedPaths": ["target.txt"],
        "dependencyResult": "pass",
        "ownerBoundaryResult": "pass",
        "publicationBoundaryResult": "pass",
        "validationCommands": ["python3 validate.py"],
        "lifecycleOwner": "invoke",
        "authorityClass": "public",
        "publicationClass": "internal",
        "reasons": [],
    }
    if variant == "owner-not-ready":
        owner_receipt["mutationHandoff"] = "gated"
    if variant == "expanded-package-target":
        owner_receipt["validatedPaths"].append("extra.txt")
    write_json(owner_path, owner_receipt)
    owner_ref = ref(root, owner_path)

    target_digest = RUNNER.sha256(RUNNER.canonical_bytes(target_inventory))
    validation_digest = RUNNER.sha256(RUNNER.canonical_bytes(validation_contracts))
    predicate_digest = RUNNER.sha256(RUNNER.canonical_bytes(predicate))
    common = {
        "task_id": "TASK-GENERIC-001",
        "swu_id": "SWU-GENERIC-001",
        "attempt_id": attempt,
        "prerequisite_fingerprint": fingerprint,
        "target_inventory_digest": target_digest,
        "validation_contract_digest": validation_digest,
        "satisfaction_predicate_digest": predicate_digest,
        "resume_point": "task-session:context-build",
        "max_owner_hops": 1,
        "allowed_effect": "pre-execution-prerequisite-resolution",
    }
    route_path = controls / "route.json"
    route_auth_ref = auth_ref
    if variant == "swapped-authorization-evidence":
        replacement_auth = controls / "replacement-authorization.json"
        write_json(replacement_auth, {"authorization": "different-artifact"})
        route_auth_ref = ref(root, replacement_auth)
    route = {
        "schema_version": "arcanum.continuation_route.v2",
        "route_id": "route-owner-resume-001",
        "source": {
            "phase": "pre-execution-prerequisite",
            "capability": "task-session",
            "mode": "execute",
            "result": "unmet",
            "receipt": "controls/classification.json",
            "blocker_fingerprint": "sha256:owner-resume",
            "legacy_adaptation": False,
            "pre_execution_context": {
                **common,
                "classification_receipt_ref": classification_ref,
                "declared_owner_route": "invoke:refresh:apply-approved",
                "consumed_attempt_fingerprints": [],
            },
        },
        "authorization": {
            "requested": True,
            "exact_route": "invoke:refresh:apply-approved",
            "evidence": "Exact route and scope authorization.",
            "binding": {**common, "route": "invoke:refresh:apply-approved", "evidence_ref": route_auth_ref},
        },
        "candidates": [{
            "rank": 1,
            "capability": "invoke",
            "mode": "refresh",
            "mutation_mode": "apply-approved",
            "owner": "invoke",
            "evidence": ["Typed prerequisite owner."],
            "required_inputs": ["exact authorization"],
            "missing_inputs": [],
            "mutation_risk": "medium",
            "approval_required": True,
            "authorization_status": "matched",
            "expected_receipt": "Digest-bound Invoke owner receipt.",
            "fallback": "Block on owner validation failure.",
        }],
        "selection": {"status": "selected", "candidate_rank": 1, "reason": "Exact owner and authorization."},
        "dispatch": {
            "status": "completed",
            "runtime": "bounded-helper",
            "owner_receipt": "controls/owner-receipt.json",
            "owner_receipt_ref": owner_ref,
            "join_validation": "pass",
            "helper_closeout": "pass",
            "dispatch_count": 1,
            "join_count": 1,
            "router_mutations": [],
        },
        "owner_boundary": "pass",
        "control_handle": {
            "return_to": "task-session",
            "mode": "resume-same-attempt",
            **common,
            "route": "invoke:refresh:apply-approved",
            "owner_receipt_ref": owner_ref,
        },
        "returned_next_route": None,
    }
    if variant == "recursive-route":
        route["returned_next_route"] = {"capability": "task-session", "mode": "execute", "target": "SWU-GENERIC-001"}
    if variant == "unjoined-helper":
        route["dispatch"]["helper_closeout"] = "block"
    if variant == "mismatched-control-handle":
        route["control_handle"]["prerequisite_fingerprint"] = "9" * 64
    write_json(route_path, route)
    route_ref = ref(root, route_path)

    work_pack_path = controls / "WORK-PACK.md"
    work_pack_path.write_text("| `SWU-GENERIC-001` | task | selected |\n", encoding="utf-8")
    swu_path = controls / "TASK.md"
    swu_path.write_text("SWU-GENERIC-001\n", encoding="utf-8")
    request_path = controls / "request.json"
    request = {
        "schema_version": "task-session.governance-run-request.v1",
        "entry_profile": "pre-execution-prerequisite",
        "request_id": "request-owner-resume-001",
        "run_id": attempt,
        "work_pack_ref": ref(root, work_pack_path),
        "swu_ref": ref(root, swu_path),
        "task_id": "TASK-GENERIC-001",
        "swu_id": "SWU-GENERIC-001",
        "control_refs": [auth_ref],
        "execution_contract": {
            "allowed_writes": ["target.txt"],
            "declared_outputs": ["staged-target.txt"],
            "validation_commands": validation_contracts,
            "timeout_seconds": 30,
            "max_output_bytes": 65536,
        },
        "owner_identity": {"capability": "task-session", "subject": "owner-resume-test"},
        "idempotency_key": "owner-resume-001",
        "closeout_contract": {
            "required_owner_capabilities": ["invoke"],
            "continuation_policy": "emit-cursor-never-execute-successor",
            "terminal_receipt_path": "run/terminal.json",
        },
        "pre_execution_prerequisite": {
            "attempt_id": attempt,
            "prerequisite_fingerprint": fingerprint,
            "classification_receipt_ref": classification_ref,
            "continuation_route_receipt_ref": route_ref,
            "owner_receipt_ref": owner_ref,
            "owner_receipt_schema_ref": ref(root, owner_schema_path),
            "route": "invoke:refresh:apply-approved",
            "target_inventory": target_inventory,
            "expected_package_id": "package-generic-001",
            "expected_package_digest": package_digest,
            "expected_owner_validation_commands": ["python3 validate.py"],
            "satisfaction_predicate": predicate,
            "resume_point": "task-session:context-build",
            "max_owner_hops": 1,
            "allowed_effect": "pre-execution-prerequisite-resolution",
            "consumption_ledger_path": "run/pre-execution-consumption.json",
            "resume_receipt_path": "run/pre-execution-resume-receipt.json",
        },
    }
    write_json(request_path, request)

    if variant == "stale-owner-receipt":
        owner_receipt["reasons"] = ["tampered after join"]
        write_json(owner_path, owner_receipt)
    if variant == "stale-classification-receipt":
        classification["reasons"] = ["tampered after routing"]
        write_json(classification_path, classification)
    if variant == "changed-baseline":
        (root / "target.txt").write_text("changed\n", encoding="utf-8")
    if variant == "reused-attempt-fingerprint":
        write_json(root / "run" / "pre-execution-consumption.json", {"already": "consumed"})
    return request_path, root / "run"


class OwnerResumeTests(unittest.TestCase):
    def test_same_attempt_resumes_once_and_replays_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request, run_dir = build_case(root)
            first = RUNNER.prerequisite_resume(root, request, run_dir)
            self.assertEqual(first["result"], "pass")
            self.assertEqual(first["resume_point"], "task-session:context-build")
            self.assertEqual(first["resume_count"], 1)
            self.assertEqual(first["writes_performed"], 2)
            second = RUNNER.prerequisite_resume(root, request, run_dir)
            self.assertTrue(second["idempotent_replay"])
            self.assertEqual(second["result"], "already-resumed")
            self.assertEqual(second["resume_count"], 1)
            self.assertEqual(second["context_builder_entry_budget"], 0)
            self.assertIsNone(second["next_action"])
            self.assertEqual(second["writes_performed"], 0)
            receipt = json.loads((run_dir / "pre-execution-resume-receipt.json").read_text(encoding="utf-8"))
            self.assertFalse(receipt["selector_resolution_reentered"])
            self.assertEqual(receipt["context_builder_entry_budget"], 1)

    def test_adversarial_cases_block_before_resume(self) -> None:
        variants = (
            "owner-not-ready",
            "stale-owner-receipt",
            "stale-classification-receipt",
            "expanded-package-target",
            "changed-baseline",
            "reused-attempt-fingerprint",
            "recursive-route",
            "unjoined-helper",
            "mismatched-control-handle",
            "swapped-authorization-evidence",
        )
        for variant in variants:
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                request, run_dir = build_case(root, variant)
                with self.assertRaises(RUNNER.RunnerBlock):
                    RUNNER.prerequisite_resume(root, request, run_dir)
                self.assertFalse((run_dir / "pre-execution-resume-receipt.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

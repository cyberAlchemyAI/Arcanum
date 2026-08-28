#!/usr/bin/env python3
"""End-to-end producer and replay-admission tests for Invoke Design W3."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


INVOKE = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


W2_TESTS = load_module("w3_w2_fixture", Path(__file__).with_name("test_compile_design_candidate.py"))
W3 = load_module("w3_compiler", INVOKE / "scripts/compile_design_source_v2.py")
ADMISSION = load_module("w3_admission", INVOKE / "scripts/validate_design_bundle_admission.py")
PROJECTOR = load_module("w3_bundle_projector", INVOKE / "scripts/project_design_bundle.py")
CAPABILITY = load_module("w3_capability_resolver", INVOKE / "scripts/capability_status_resolver.py")


def digest_without(document: dict, field: str) -> str:
    return hashlib.sha256(json.dumps({key: value for key, value in document.items() if key != field}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class DesignBundleV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = W2_TESTS.DesignCandidateTests(methodName="runTest")
        self.fixture.setUp()
        self.repo = self.fixture.repo
        self.schemas = self.fixture.schemas
        self.assertEqual(0, self.fixture.compile("w2-candidate"))
        self.w2_dir = self.repo / "w2-candidate"
        self.artifact_path = self.w2_dir / "DESIGN.json"
        self.candidate_receipt_path = self.w2_dir / "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json"
        self.distill_dir = self.repo / "distill"
        self.distill_dir.mkdir()
        self.closure_path = self.repo / "DESIGN-BUNDLE-CLOSURE.json"
        self.closure = self.make_closure()
        self.write_closure(self.closure)

    def tearDown(self) -> None:
        self.fixture.tearDown()

    @staticmethod
    def write_json(path: Path, document: dict) -> None:
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def exact(self, path: Path) -> dict:
        data = path.read_bytes()
        return {"path": path.relative_to(self.repo).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}

    def size_ref(self, path: Path) -> dict:
        ref = self.exact(path)
        return {"path": ref["path"], "sha256": ref["sha256"], "size_bytes": ref["size"]}

    def make_distill(self, verdict: str = "pass", validation_status: str = "pass") -> dict:
        request_path = self.distill_dir / "DISTILL-RUN-REQUEST.json"
        events_path = self.distill_dir / "DISTILL-EVENTS.jsonl"
        receipt_path = self.distill_dir / "DISTILL-EXECUTION-RECEIPT.json"
        validation_path = self.distill_dir / "DISTILL-VALIDATION-RESULT.json"
        reviewed = [self.size_ref(self.artifact_path), self.size_ref(self.candidate_receipt_path)]
        request = {
            "schema_version": "1.0.0",
            "run_id": "distill:w3-fixture",
            "parent_invoke_run_id": "invoke:w3-fixture",
            "invoke_mode": "design",
            "distill_mode": "coherent-unit",
            "round_budget": {"max_rounds": 1, "max_role_invocations": 2},
            "reviewed_inputs": reviewed,
            "requested_techniques": ["smallest-coherent-unit"],
        }
        self.write_json(request_path, request)
        payload = self.size_ref(self.artifact_path)
        specs = [
            ("probe", "capability_probe", None),
            ("proposer-start", "role_start", "proposer"),
            ("proposer-result", "role_result", "proposer"),
            ("balancer-start", "role_start", "balancer"),
            ("balancer-result", "role_result", "balancer"),
            ("termination", "termination", None),
        ]
        events = [{
            "schema_version": "1.0.0",
            "event_id": f"event:{name}",
            "run_id": request["run_id"],
            "sequence": sequence,
            "event_type": event_type,
            "execution_path": "role_simulation",
            "role": role,
            "invocation_ref": None,
            "payload_ref": copy.deepcopy(payload),
            "emitted_at": f"2026-08-27T20:00:{sequence:02d}Z",
        } for sequence, (name, event_type, role) in enumerate(specs)]
        events_path.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for item in events), encoding="utf-8")
        gaps = [] if verdict == "pass" else ["Distill did not close the coherent unit."]
        receipt = {
            "schema_version": "1.0.0",
            "receipt_id": "distill-receipt:w3-fixture",
            "run_id": request["run_id"],
            "request_ref": self.size_ref(request_path),
            "event_refs": [item["event_id"] for item in events],
            "role_trace": [
                {"role": "proposer", "execution_path": "role_simulation", "invocation_ref": None, "evidence_refs": ["event:proposer-start", "event:proposer-result"], "result_ref": copy.deepcopy(payload)},
                {"role": "balancer", "execution_path": "role_simulation", "invocation_ref": None, "evidence_refs": ["event:balancer-start", "event:balancer-result"], "result_ref": copy.deepcopy(payload)},
            ],
            "objections": [],
            "reconciliations": [],
            "technique_trace": [{"technique": "smallest-coherent-unit", "status": "applied", "evidence_refs": ["event:proposer-result", "event:balancer-result"]}],
            "termination": {"reason": "round budget closed with stable agreement", "round_count": 1},
            "verdict": verdict,
            "gaps": gaps,
            "recomposition": {"summary": "The candidate remains one coherent Design bundle unit.", "result_ref": copy.deepcopy(payload)},
            "next_route": {"capability": "invoke-design-bundle-producer", "status": "ready" if verdict == "pass" else "blocked"},
            "reviewed_input_provenance": copy.deepcopy(reviewed),
        }
        self.write_json(receipt_path, receipt)
        diagnostics = [] if validation_status == "pass" else ["Independent validation did not pass."]
        validation = {
            "schema_version": "1.0.0",
            "validation_result_id": "distill-validation:w3-fixture",
            "validator_version": "0.2.0",
            "receipt_ref": self.size_ref(receipt_path),
            "status": validation_status,
            "checks": [{"check_id": "semantic-and-provenance-closure", "status": validation_status, "evidence_refs": ["event:termination"]}],
            "diagnostics": diagnostics,
            "owned_gaps": [] if validation_status == "pass" else ["distill-validation-gap"],
            "mutation_handoff_allowed": False,
        }
        self.write_json(validation_path, validation)
        return {
            "request_ref": self.exact(request_path),
            "events_ref": self.exact(events_path),
            "execution_receipt_ref": self.exact(receipt_path),
            "validation_result_ref": self.exact(validation_path),
        }

    def make_closure(self, verdict: str = "pass", validation_status: str = "pass") -> dict:
        artifact = json.loads(self.artifact_path.read_text())
        closure = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-bundle-closure/v1",
            "schema_version": "invoke.design-bundle-closure.v1",
            "closure_id": "design-bundle-closure:w3-fixture",
            "target_id": artifact["target_id"],
            "candidate_receipt_ref": self.exact(self.candidate_receipt_path),
            "distill_evidence": self.make_distill(verdict, validation_status),
            "output_contracts": copy.deepcopy(W3.OUTPUT_CONTRACTS),
            "authority_effect": "none",
            "closure_digest": "0" * 64,
        }
        closure["closure_digest"] = digest_without(closure, "closure_digest")
        return closure

    def write_closure(self, closure: dict) -> None:
        closure["closure_digest"] = digest_without(closure, "closure_digest")
        self.write_json(self.closure_path, closure)

    def compile(self, name: str, late=None) -> int:
        return W3.compile_bundle(self.closure_path, self.repo, self.repo / name, self.repo / f"{name}.attempt.json", self.schemas, late)

    def assert_valid_attempt(self, name: str) -> dict:
        self.assertFalse((self.repo / name).exists())
        receipt = json.loads((self.repo / f"{name}.attempt.json").read_text())
        schema = json.loads((self.schemas / "design-bundle-attempt-receipt-v1.schema.json").read_text())
        self.assertEqual([], [error.message for error in Draft202012Validator(schema).iter_errors(receipt)])
        self.assertEqual("block", receipt["result"])
        return receipt

    def test_real_w1_w2_w3_is_atomic_and_deterministic(self) -> None:
        self.assertEqual(0, self.compile("w3-first"))
        self.assertEqual(0, self.compile("w3-second"))
        first = {item.name: item.read_bytes() for item in (self.repo / "w3-first").iterdir()}
        second = {item.name: item.read_bytes() for item in (self.repo / "w3-second").iterdir()}
        self.assertEqual(first, second)
        self.assertEqual({name for _, name in W3.OUTPUTS} | {W3.STAGE_NAME}, set(first))
        stage = json.loads((self.repo / "w3-first" / W3.STAGE_NAME).read_text())
        self.assertEqual("invoke.design-stage-receipt.v2", stage["schema_version"])
        self.assertEqual("design-stage-pass", stage["evidence_state"])
        self.assertEqual("plan-evidence-pending", stage["plan_evidence_state"])
        self.assertEqual("plan", stage["next_route"])

    def test_distill_flag_and_block_leave_only_valid_attempt_receipt(self) -> None:
        for verdict, validation in (("flag", "flag"), ("block", "block")):
            with self.subTest(verdict=verdict):
                self.closure = self.make_closure(verdict, validation)
                self.write_closure(self.closure)
                name = f"distill-{verdict}"
                self.assertEqual(1, self.compile(name))
                receipt = self.assert_valid_attempt(name)
                self.assertEqual("DISTILL_NOT_PASSING", receipt["blockers"][0]["code"])

    def test_stale_candidate_and_late_projection_changes_block(self) -> None:
        stale = copy.deepcopy(self.closure)
        stale["candidate_receipt_ref"]["sha256"] = "0" * 64
        self.write_closure(stale)
        self.assertEqual(1, self.compile("stale-candidate"))
        self.assert_valid_attempt("stale-candidate")

        self.write_closure(self.closure)
        def alter(staging: Path) -> None:
            with (staging / "ARCHITECTURE.md").open("ab") as handle:
                handle.write(b"altered")
        self.assertEqual(1, self.compile("late-projection", alter))
        self.assert_valid_attempt("late-projection")

    def test_wrong_target_and_distill_provenance_block(self) -> None:
        wrong_target = copy.deepcopy(self.closure)
        wrong_target["target_id"] = "target:wrong"
        self.write_closure(wrong_target)
        self.assertEqual(1, self.compile("wrong-target"))
        self.assert_valid_attempt("wrong-target")

        self.closure = self.make_closure()
        request_path = self.repo / self.closure["distill_evidence"]["request_ref"]["path"]
        request = json.loads(request_path.read_text())
        request["reviewed_inputs"] = request["reviewed_inputs"][:1]
        self.write_json(request_path, request)
        self.closure["distill_evidence"]["request_ref"] = self.exact(request_path)
        self.write_closure(self.closure)
        self.assertEqual(1, self.compile("bad-provenance"))
        receipt = self.assert_valid_attempt("bad-provenance")
        self.assertIn(receipt["blockers"][0]["code"], {"DISTILL_BINDING_MISMATCH", "DISTILL_REQUEST_INVALID"})

    def test_symlinked_distill_evidence_blocks_without_publication(self) -> None:
        events = self.repo / self.closure["distill_evidence"]["events_ref"]["path"]
        preserved = events.with_name("DISTILL-EVENTS-PRESERVED.jsonl")
        shutil.copy2(events, preserved)
        events.unlink()
        events.symlink_to(preserved.name)
        self.closure["distill_evidence"]["events_ref"] = self.exact(events)
        self.write_closure(self.closure)
        self.assertEqual(1, self.compile("symlink-distill"))
        receipt = self.assert_valid_attempt("symlink-distill")
        self.assertEqual("PATH_UNSAFE", receipt["blockers"][0]["code"])

    def test_route_derivation_is_deterministic_and_owner_exclusive(self) -> None:
        artifact = json.loads(self.artifact_path.read_text())
        artifact["unresolved_gaps"] = []
        artifact["selected_outputs"] = ["architecture", "spell:fixture"]
        self.assertEqual("spellcraft", PROJECTOR.derive_next_route(artifact))
        artifact["selected_outputs"] = ["architecture", "sigil:fixture"]
        self.assertEqual("sigil-development", PROJECTOR.derive_next_route(artifact))
        artifact["unresolved_gaps"] = [{"gap_id": "gap:deferred", "severity": "flag", "owner": "design-author", "repair_route": "design-follow-up", "effect": "Plan routing remains deferred."}]
        self.assertEqual("deferred", PROJECTOR.derive_next_route(artifact))
        artifact["unresolved_gaps"] = []
        artifact["selected_outputs"] = ["architecture", "spell:fixture", "sigil:fixture"]
        with self.assertRaisesRegex(ValueError, "Spellcraft"):
            PROJECTOR.derive_next_route(artifact)

    def test_zero_and_multiple_companions_render_as_one_sorted_aggregate(self) -> None:
        artifact = json.loads(self.artifact_path.read_text())
        artifact["selected_companions"] = []
        empty = PROJECTOR.render_selected_companions(artifact).decode("utf-8")
        self.assertIn("No companion output was selected.", empty)

        fact = artifact["facts"][0]
        requirement_ref = fact["requirement_refs"][0]
        artifact["selected_companions"] = [
            {
                "output_id": "ux:second",
                "fact_ids": [fact["fact_id"]],
                "requirement_refs": [requirement_ref],
            },
            {
                "output_id": "research:first",
                "fact_ids": [fact["fact_id"]],
                "requirement_refs": [requirement_ref],
            },
        ]
        aggregate = PROJECTOR.render_selected_companions(artifact).decode("utf-8")
        self.assertEqual(1, aggregate.count("## `research:first`"))
        self.assertEqual(1, aggregate.count("## `ux:second`"))
        self.assertLess(aggregate.index("## `research:first`"), aggregate.index("## `ux:second`"))
        self.assertEqual(2, aggregate.count(f"`{fact['fact_id']}`"))

    def test_historical_replay_admission_validates_but_cannot_open_new_pass(self) -> None:
        self.assertEqual(0, self.compile("w3-admit"))
        bundle = self.repo / "w3-admit"
        output = self.repo / "w3-admission.json"
        self.assertEqual(0, ADMISSION.validate_bundle(bundle, self.repo, output, self.schemas))
        admission = json.loads(output.read_text())
        self.assertEqual("pass", admission["result"])
        self.assertTrue(admission["evidence_ceiling"]["artifact_authored"])
        capability_path = INVOKE / "mode-capabilities.json"
        request = {
            "schema_version": "invoke.capability-status.request.v1",
            "mode": "design",
            "artifact_receipt": {
                "receipt_id": "artifact-axis:w3-real",
                "axis": "artifact_authored",
                "mode": "design",
                "status": "pass",
                "evidence": ["w3-admit/INVOKE-DESIGN-STAGE-RECEIPT.json"],
                "producer_receipt": json.loads((bundle / W3.STAGE_NAME).read_text()),
                "producer_admission_receipt": copy.deepcopy(admission),
            },
        }
        status = CAPABILITY.resolve_capability_status(
            request,
            json.loads(capability_path.read_text()),
            hashlib.sha256(capability_path.read_bytes()).hexdigest(),
            json.loads((INVOKE / "schemas/capability-status-request.schema.json").read_text()),
            json.loads((INVOKE / "schemas/capability-status-result.schema.json").read_text()),
            json.loads((INVOKE / "schemas/material-package-receipt.schema.json").read_text()),
        )
        self.assertEqual("block", status["artifact_authored"]["status"])
        self.assertTrue(
            any(
                "historical/read-only" in diagnostic
                for diagnostic in status["artifact_authored"]["diagnostics"]
            )
        )
        self.assertFalse(status["registry_released"]["status"])
        self.assertFalse(status["mutation_runtime_ready"]["status"])

        tampered = self.repo / "w3-tampered"
        shutil.copytree(bundle, tampered)
        (tampered / "ARCHITECTURE.md").write_text((tampered / "ARCHITECTURE.md").read_text() + "\nTampered.\n")
        before = {item.name: item.read_bytes() for item in tampered.iterdir()}
        blocked_output = self.repo / "w3-tampered-admission.json"
        self.assertEqual(1, ADMISSION.validate_bundle(tampered, self.repo, blocked_output, self.schemas))
        after = {item.name: item.read_bytes() for item in tampered.iterdir()}
        self.assertEqual(before, after)
        self.assertEqual("block", json.loads(blocked_output.read_text())["result"])

    def test_preexisting_destination_is_invocation_error_without_attempt(self) -> None:
        destination = self.repo / "preexisting-w3"
        destination.mkdir()
        with self.assertRaises(ValueError):
            W3.compile_bundle(self.closure_path, self.repo, destination, self.repo / "preexisting-w3.attempt.json", self.schemas)
        self.assertFalse((self.repo / "preexisting-w3.attempt.json").exists())

    def test_genuine_v2_bundle_is_admitted_as_one_evolution_predecessor(self) -> None:
        self.assertEqual(0, self.compile("w3-predecessor"))
        predecessor_dir = self.repo / "w3-predecessor"
        predecessor_artifact = predecessor_dir / "DESIGN.json"
        predecessor_receipt = predecessor_dir / W3.STAGE_NAME
        w1 = self.fixture.fixture
        boundary = copy.deepcopy(w1.boundary)
        boundary["roots"].append(w1.directory_binding("root:prior-design", "w3-predecessor"))
        boundary["discovery_rules"].append({
            "rule_id": "rule:prior-design",
            "root_id": "root:prior-design",
            "input_class": "current-design",
            "include_globs": ["DESIGN.json"],
        })
        boundary["required_input_classes"].append("current-design")
        material = {key: value for key, value in boundary.items() if key != "boundary_digest"}
        boundary["boundary_digest"] = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        w1.write_approval(w1.approval_path, boundary)
        closure = copy.deepcopy(w1.closure)
        closure["discovery_boundary"] = copy.deepcopy(boundary)
        closure["activation"]["approval_ref"] = w1.file_ref(
            w1.approval_path,
            "public",
            "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1",
            "invoke.design-input-boundary-approval.v1",
        )
        prior_id = "input:prior-design"
        closure["input_catalog"].append({
            "input_id": prior_id,
            "kind": "current-design",
            "authority_class": "historical",
            "authority_owner": w1.owner,
            "applicability_owner": w1.owner,
            "classification": "required",
            "selector": "file:w3-predecessor/DESIGN.json",
            "source_ref": w1.file_ref(
                predecessor_artifact,
                "public",
                "https://arcanum.dev/schemas/invoke/design-artifact/v1",
                "invoke.design-artifact.v1",
            ),
            "freshness": {"status": "current", "observed_epoch": w1.epoch},
            "applies_to": ["design-evolution"],
            "exclusion_evidence_ref": None,
        })
        closure["design_kind"] = {
            "kind": "evolution",
            "prior_design_artifact_ref": w1.file_ref(predecessor_artifact, "public", None, None),
            "prior_design_stage_receipt_ref": w1.file_ref(predecessor_receipt, "public", None, None),
            "current_state_input_ids": [prior_id],
            "declared_delta_ids": ["delta:preserve-system"],
        }
        closure["constraints"].append({
            "obligation_id": "constraint:prior-design-bound",
            "class": "constraint",
            "statement": "The evolution binds exactly one admitted v2 predecessor.",
            "source_input_ids": [prior_id],
            "owner": w1.owner,
        })
        w1.closure = closure
        w1.write_closure(closure)
        w1_result = w1.compile_at("w1-evolution")
        self.assertTrue(
            (self.repo / "w1-evolution/DESIGN-INPUT-PRODUCTION-RECEIPT.json").is_file(),
            json.dumps(w1_result, indent=2),
        )

        self.fixture.w1_dir = self.repo / "w1-evolution"
        source = self.fixture.make_source()
        source["design_kind"] = {
            "kind": "evolution",
            "predecessor_artifact_ref": self.exact(predecessor_artifact),
            "predecessor_stage_receipt_ref": self.exact(predecessor_receipt),
            "deltas": [{
                "delta_id": "delta:preserve-system",
                "change": "preserved",
                "prior_fact_id": "system:w1-target",
                "current_fact_id": "system:w1-target",
                "decision_ref": None,
                "rationale": "The owner-approved evolution preserves the target-system fact.",
            }],
        }
        self.fixture.source = source
        w2_code = self.fixture.compile("w2-evolution", source)
        w2_attempt = self.repo / "w2-evolution.attempt.json"
        self.assertEqual(0, w2_code, w2_attempt.read_text() if w2_attempt.exists() else "no attempt receipt")
        receipt = json.loads((self.repo / "w2-evolution/DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json").read_text())
        self.assertEqual("pass", receipt["result"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

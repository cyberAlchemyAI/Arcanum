#!/usr/bin/env python3
"""Regression tests for the deterministic Invoke Plan v2 successor."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INVOKE = ROOT / "spells" / "invoke"
REPO = ROOT.parent
SCHEMAS = INVOKE / "schemas"
COMPILER = INVOKE / "scripts" / "compile_plan_bundle_v2.py"
ADMISSION = INVOKE / "scripts" / "validate_plan_bundle_admission.py"
DESIGN_STAGE = ROOT / "development" / "invoke-plan-successor-design" / "design-bundle-v6" / "INVOKE-DESIGN-STAGE-RECEIPT.json"
DESIGN_ADMISSION = ROOT / "development" / "invoke-plan-successor-design" / "DESIGN-BUNDLE-ADMISSION-V6.json"


def ref(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def source() -> dict:
    return {
        "$schema": "https://arcanum.dev/schemas/invoke/plan-source/v2", "schema_version": "invoke.plan-source.v2",
        "source_id": "plan-source:test", "profile_id": "invoke.generic-plan-baseline.v2", "target_id": "test:plan-successor",
        "design_binding": {"stage_receipt": ref(DESIGN_STAGE), "admission_receipt": ref(DESIGN_ADMISSION)},
        "summary": "Implement one deterministic Plan successor canary.", "mutation_capable": True,
        "objectives": [{"id": "objective:test", "statement": "Produce an admitted deterministic bundle.", "success_criteria": ["Two compilations are byte-identical."]}],
        "slices": [{"id": "slice:test", "objective_ids": ["objective:test"], "description": "Cross the complete producer and admission path."}],
        "layers": [{"id": "layer:test", "name": "Deterministic core", "exit_evidence": ["Admission passes."]}],
        "waves": [{"id": "wave:test", "slice_ids": ["slice:test"], "layer_id": "layer:test", "depends_on": [], "task_ids": ["task:test"], "gate_id": "gate:test"}],
        "tasks": [{"id": "task:test", "wave_id": "wave:test", "slice_id": "slice:test", "title": "Build the canary", "owner": "invoke-plan-owner", "swu_ids": ["swu:test"], "validation_ids": ["validation:test"], "status": "ready", "next_action": "Implement the bounded canary."}],
        "swus": [{"id": "swu:test", "task_id": "task:test", "description": "Compile and admit the plan.", "write_scope": ["arcanum/spells/invoke/plan.md"], "validation_ids": ["validation:test"]}],
        "implementation_details": [{"id": "detail:test", "task_id": "task:test", "description": "Use absent outputs and canonical JSON."}],
        "validation_obligations": [{"id": "validation:test", "description": "Run deterministic replay.", "command": "python3 test_plan_successor_v2.py", "expected_result": "PASS"}],
        "gates": [{"id": "gate:test", "after_wave": "wave:test", "required_validation_ids": ["validation:test"], "pass_condition": "All validation obligations pass.", "failure_route": "repair-plan-source"}],
        "blockers": [], "gaps": [],
        "execution_entries": [{"id": "entry:test", "unit_id": "swu:test", "route": "task-session", "delegated": True, "bounded_context_execution": True, "expected_receipt_ref": "arcanum/spells/invoke/development/swu-test-receipt.json", "transient_outputs": ["arcanum/spells/invoke/development/canary-output.json"]}],
        "closeout_obligations": [{"id": "closeout:test", "description": "Preserve validation results.", "evidence": ["PLAN-STAGE-RECEIPT.json"]}],
        "consumer_inputs": {"dispatch": {"multi_owner": True, "delegated": True, "protected_scope": False, "reusable_graph": False}, "observability": {"configured": True, "observer_contract_admitted": True}},
        "authority_effect": "none"
    }


class PlanSuccessorTest(unittest.TestCase):
    def run_compiler(self, source_path: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(COMPILER), str(source_path), "--repo-root", str(REPO), "--schema-dir", str(SCHEMAS), "--output-dir", str(output)], text=True, capture_output=True, check=False)

    def test_compile_replay_and_admission(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); source_path = temp / "source.json"; source_path.write_text(json.dumps(source(), indent=2) + "\n", encoding="utf-8")
            first = temp / "first"; second = temp / "second"
            first_run = self.run_compiler(source_path, first)
            second_run = self.run_compiler(source_path, second)
            self.assertEqual(first_run.returncode, 0, first_run.stderr)
            self.assertEqual(second_run.returncode, 0, second_run.stderr)
            first_rows = [(path.relative_to(first), path.read_bytes()) for path in sorted(first.rglob("*")) if path.is_file()]
            second_rows = [(path.relative_to(second), path.read_bytes()) for path in sorted(second.rglob("*")) if path.is_file()]
            self.assertEqual(first_rows, second_rows)
            applicability = json.loads((first / "CONSUMER-APPLICABILITY.json").read_text())
            self.assertEqual([row["consumer"] for row in applicability["consumers"]], ["wpra", "implementation-readiness", "task-session", "context-builder", "dispatch-spec", "goal", "signal-observer"])
            self.assertTrue(all(row["result"] in {"pass", "negative_evidence"} for row in applicability["consumers"]))
            self.assertTrue(all(len(row["validator"]["sha256"]) == 64 and row["validator"]["size"] > 0 for row in applicability["consumers"]))
            self.assertEqual(next(row for row in applicability["consumers"] if row["consumer"] == "goal")["result"], "negative_evidence")
            wpra_row = next(row for row in applicability["consumers"] if row["consumer"] == "wpra")
            self.assertIn("consumers/wpra/rehearsal-root/EVIDENCE.json", wpra_row["projection_paths"])
            self.assertTrue((first / "consumers/wpra/run-1/plan-semantic-manifest.json").is_file())
            self.assertTrue((first / "consumers/wpra/run-1/selection-handoff.json").is_file())
            self.assertEqual(json.loads((first / "consumers/context-builder/VALIDATION-RESULT-1.json").read_text())["admission_schema_version"], "1.3.0")
            admission = temp / "admission.json"
            completed = subprocess.run([sys.executable, str(ADMISSION), "--repo-root", str(REPO), "--bundle-root", str(first), "--schema-dir", str(SCHEMAS), "--output", str(admission)], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(admission.read_text())["result"], "pass")

    def test_cycle_blocks_and_creates_no_bundle(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); payload = source(); payload["waves"][0]["depends_on"] = ["wave:test"]
            source_path = temp / "source.json"; source_path.write_text(json.dumps(payload), encoding="utf-8")
            output = temp / "bundle"; completed = self.run_compiler(source_path, output)
            self.assertEqual(completed.returncode, 1); self.assertFalse(output.exists()); self.assertIn("cycle", completed.stderr)

    def test_unadmitted_observer_contract_blocks_before_bundle(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); payload = source(); payload["consumer_inputs"]["observability"]["observer_contract_admitted"] = False
            source_path = temp / "source.json"; source_path.write_text(json.dumps(payload), encoding="utf-8")
            output = temp / "bundle"; completed = self.run_compiler(source_path, output)
            self.assertEqual(completed.returncode, 1); self.assertFalse(output.exists()); self.assertIn("signal-observer applicability blocked", completed.stderr)

    def test_directory_write_scope_blocks_wpra_rehearsal(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); payload = source(); payload["swus"][0]["write_scope"] = ["arcanum/spells/invoke"]
            source_path = temp / "source.json"; source_path.write_text(json.dumps(payload), encoding="utf-8")
            output = temp / "bundle"; completed = self.run_compiler(source_path, output)
            self.assertEqual(completed.returncode, 1); self.assertFalse(output.exists()); self.assertIn("exact file write scopes", completed.stderr)

    def test_duplicate_execution_unit_blocks_before_bundle(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); payload = source(); duplicate = dict(payload["execution_entries"][0]); duplicate["id"] = "entry:duplicate"; payload["execution_entries"].append(duplicate)
            source_path = temp / "source.json"; source_path.write_text(json.dumps(payload), encoding="utf-8")
            output = temp / "bundle"; completed = self.run_compiler(source_path, output)
            self.assertEqual(completed.returncode, 1); self.assertFalse(output.exists()); self.assertIn("only one execution entry", completed.stderr)

    def test_documentation_names_source_consumers_and_authority_limit(self) -> None:
        guide = (INVOKE / "plan-authoring-guide.md").read_text(encoding="utf-8")
        contract = (INVOKE / "plan.md").read_text(encoding="utf-8")
        overview = (INVOKE / "plan/README.md").read_text(encoding="utf-8")
        for text in (guide, contract, overview):
            self.assertIn("Plan", text)
        for required in ("PLAN-SOURCE.json", "observer_contract_admitted", "exact files", "tools/arcanum invoke plan produce bundle"):
            self.assertIn(required, guide)
        for required in ("Work-Pack Readiness Audit", "Task Session", "Context Builder", "Dispatch Spec", "Goal", "Signal Observer", "does not"):
            self.assertIn(required, contract)

    def test_tampering_blocks_admission(self) -> None:
        with tempfile.TemporaryDirectory(dir=INVOKE / "development") as raw:
            temp = Path(raw); source_path = temp / "source.json"; source_path.write_text(json.dumps(source()), encoding="utf-8")
            bundle = temp / "bundle"; compile_run = self.run_compiler(source_path, bundle); self.assertEqual(compile_run.returncode, 0, compile_run.stderr)
            with (bundle / "WORK-PACK.md").open("a", encoding="utf-8") as handle: handle.write("tamper\n")
            receipt = temp / "blocked.json"; completed = subprocess.run([sys.executable, str(ADMISSION), "--repo-root", str(REPO), "--bundle-root", str(bundle), "--schema-dir", str(SCHEMAS), "--output", str(receipt)], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 1); self.assertEqual(json.loads(receipt.read_text())["result"], "block")


if __name__ == "__main__": unittest.main()

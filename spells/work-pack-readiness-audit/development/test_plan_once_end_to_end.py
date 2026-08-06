#!/usr/bin/env python3
"""Cross-capability plan-once route with one audit and no pre-execution Refresh."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = SPELL_ROOT.parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ARCANUM_ROOT / "arcana/task-session/development"))

import test_plan_once_selection as PLAN  # noqa: E402
import test_plan_once_admission as ADMISSION  # noqa: E402


class PlanOnceEndToEndTests(unittest.TestCase):
    def test_continuity_rejects_selector_spoof_and_wrong_successor(self) -> None:
        plan_case = PLAN.PlanOnceSelectionTests()
        plan_case.setUp()
        try:
            wrong_successor = plan_case.config()
            evidence = json.loads(
                plan_case.fixture.evidence_path.read_text(encoding="utf-8")
            )
            evidence["successor"] = "__complete__"
            plan_case.fixture.evidence_path.write_text(
                json.dumps(evidence, sort_keys=True), encoding="utf-8"
            )
            PLAN.refresh_evidence_refs(wrong_successor, plan_case.fixture.exact())
            wrong_successor_report = plan_case.audit(wrong_successor)
            self.assertIn(
                "CONTINUITY_FRONTIER_MISMATCH",
                {item["code"] for item in wrong_successor_report["blockers"]},
            )

            evidence["continuation"] = "__complete__"
            plan_case.fixture.evidence_path.write_text(
                json.dumps(evidence, sort_keys=True), encoding="utf-8"
            )
            selector_spoof = plan_case.config()
            receipt_path = plan_case.fixture.root / "receipts" / "U1.json"
            receipt_path.parent.mkdir()
            receipt_path.write_text(
                json.dumps(
                    {
                        "swu_id": "SWU-U1",
                        "task_id": "TASK-U1",
                        "result": "pass",
                        "lifecycle_owner_validation": {"status": "pass"},
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            receipt_ref = PLAN.exact(plan_case.fixture.root, "receipts/U1.json")
            selector_spoof["continuity_projection"].update(
                cursor="__complete__",
                completed_unit_receipt_refs=[
                    {
                        "binding_id": "completion-U1",
                        "owner_ref": "task-session",
                        "artifact_ref": receipt_ref,
                        "selector": "/lifecycle_owner_validation/status",
                    }
                ],
                joined_closeout_receipt_refs=[
                    {
                        "binding_id": "closeout-U1",
                        "owner_ref": "sigil-development",
                        "artifact_ref": receipt_ref,
                        "selector": "/lifecycle_owner_validation/status",
                    }
                ],
            )
            selector_spoof["continuity_projection"][
                "projected_next_successor"
            ].update(
                unit_id="__complete__",
                continuation_router_verification_receipt_ref=None,
            )
            selector_spoof_report = plan_case.audit(selector_spoof)
            self.assertIn(
                "CONTINUITY_RECEIPT_MISSING",
                {item["code"] for item in selector_spoof_report["blockers"]},
            )
        finally:
            plan_case.tearDown()

    def test_one_audit_selection_material_and_live_admission(self) -> None:
        plan_case = PLAN.PlanOnceSelectionTests()
        admission_case = ADMISSION.PlanOnceAdmissionTests()
        plan_case.setUp()
        admission_case.setUp()
        audit_calls = 0
        refresh_calls = 0
        try:
            config = plan_case.config()
            config_path = plan_case.fixture.root / "plan-config.json"
            config_path.write_text(
                json.dumps(config, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            report = plan_case.audit(config)
            audit_calls += 1
            output = plan_case.fixture.root / "audit-output"
            PLAN.AUDIT.write_outputs_v2(report, output)
            selection_request = {
                "schemaVersion": "1.0.0",
                "manifestRef": PLAN.exact(
                    plan_case.fixture.root,
                    "audit-output/plan-semantic-manifest.json",
                ),
                "auditConfigPath": "plan-config.json",
                "taskId": "TASK-U1",
                "swuId": "SWU-U1",
                "executionIntentBinding": {
                    "bindingId": "wpeb-111111111111111111111111",
                    "sourceInvocationId": "invoke-plan-once-end-to-end",
                    "workPackId": "WP-U1",
                    "bindingDigest": "1" * 64,
                    "authorityEffect": "bounded-execution-only",
                },
                "dependencyReceipts": [],
                "lifecycleEligibility": {
                    "eligible": True,
                    "state": "selected",
                    "evidenceRefs": [plan_case.fixture.exact()],
                },
            }
            selection = PLAN.SELECT.select_unit(
                selection_request,
                plan_case.fixture.root,
                PLAN.AUDIT.load_json(
                    SPELL_ROOT / "schemas/selection-request.schema.json"
                ),
                PLAN.AUDIT.load_json(
                    SPELL_ROOT / "schemas/plan-semantic-manifest.schema.json"
                ),
                PLAN.AUDIT.load_json(PLAN.AUDIT.CONFIG_SCHEMA_V2),
            )
            self.assertEqual(selection["selectionVerdict"], "select")
            self.assertEqual(
                selection["selectionIntentSource"], "execution-intent-binding"
            )
            ADMISSION.write_json(
                plan_case.fixture.root / "selection-receipt.json", selection
            )

            request = admission_case.build_request()
            shutil.copyfile(
                output / "plan-semantic-manifest.json",
                admission_case.root / "plan-manifest.json",
            )
            shutil.copyfile(
                plan_case.fixture.root / "selection-receipt.json",
                admission_case.root / "selection-receipt.json",
            )
            epoch = report["manifest"]["plan_epoch_id"]
            unit_digest = report["manifest"]["unit_contract_digests"]["U1"]
            selection_digest = hashlib.sha256(
                (admission_case.root / "selection-receipt.json").read_bytes()
            ).hexdigest()
            package = json.loads(
                (admission_case.root / "material-package.json").read_text()
            )
            package["plan_binding"].update(
                plan_epoch_id=epoch,
                unit_contract_digest=unit_digest,
                selection_receipt_digest=selection_digest,
            )
            receipt = ADMISSION.PRODUCER.validate_material_package(
                package,
                admission_case.root,
                json.loads(
                    (
                        ADMISSION.INVOKE / "schemas/material-package.schema.json"
                    ).read_text()
                ),
                json.loads(
                    (
                        ADMISSION.INVOKE
                        / "schemas/material-package-receipt.schema.json"
                    ).read_text()
                ),
            )
            self.assertEqual(receipt["patchVerdict"], "pass")
            ADMISSION.write_json(
                admission_case.root / "material-package.json", package
            )
            ADMISSION.write_json(
                admission_case.root / "material-receipt.json", receipt
            )
            request["materialPackage"] = ADMISSION.exact(
                admission_case.root, "material-package.json"
            )
            request["materialReceipt"] = ADMISSION.exact(
                admission_case.root, "material-receipt.json"
            )
            request["planAdmission"].update(
                planManifest=ADMISSION.exact(
                    admission_case.root, "plan-manifest.json"
                ),
                selectionReceipt=ADMISSION.exact(
                    admission_case.root, "selection-receipt.json"
                ),
                planEpochId=epoch,
                unitContractDigest=unit_digest,
            )
            admission = admission_case.resolve(request)
            self.assertEqual(admission["admissionVerdict"], "admit")
            self.assertTrue(admission["mutationReady"])
            self.assertEqual(admission["planEpochId"], epoch)
            self.assertEqual(admission["unitContractDigest"], unit_digest)
            self.assertEqual(audit_calls, 1)
            self.assertEqual(refresh_calls, 0)
        finally:
            admission_case.tearDown()
            plan_case.tearDown()


if __name__ == "__main__":
    unittest.main(verbosity=2)

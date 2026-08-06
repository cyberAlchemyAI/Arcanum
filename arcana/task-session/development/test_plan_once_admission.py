#!/usr/bin/env python3
"""Selected-unit material identity and live-baseline admission tests."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY = Path(__file__).resolve().parents[3]
TASK_SESSION = Path(__file__).resolve().parents[1]
AUDIT = REPOSITORY / "spells/work-pack-readiness-audit"
INVOKE = REPOSITORY / "spells/invoke"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ADMISSION = load_module(
    "task_session_plan_admission", TASK_SESSION / "scripts/verify-mutation-readiness.py"
)
PRODUCER = load_module(
    "invoke_plan_material", INVOKE / "scripts/material_package_validator.py"
)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(value) -> str:
    return hashlib.sha256(
        json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()


def exact(root: Path, relative: str, *, camel: bool = True):
    content = (root / relative).read_bytes()
    result = {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        "sizeBytes" if camel else "size_bytes": len(content),
    }
    return result


class PlanOnceAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".git").mkdir()
        for name, source in (
            ("schemas/plan-manifest.schema.json", AUDIT / "schemas/plan-semantic-manifest.schema.json"),
            ("schemas/selection-receipt.schema.json", AUDIT / "schemas/selection-receipt.schema.json"),
            ("schemas/material-receipt.schema.json", INVOKE / "schemas/material-package-receipt.schema.json"),
        ):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        (self.root / "controls").mkdir()
        (self.root / "staged").mkdir()
        (self.root / "controls/task.md").write_text("# TASK-U1\n", encoding="utf-8")
        (self.root / "controls/work-pack.md").write_text("# Work Pack\n", encoding="utf-8")
        self.validation_commands = ["bash verify.sh"]
        self.structured_validation = [
            {
                "command_id": "verify-U1",
                "argv": ["bash", "verify.sh"],
                "cwd": ".",
                "timeout_seconds": 30,
                "max_output_bytes": 4096,
            }
        ]
        write_json(
            self.root / "controls/context.json",
            {
                "task_id": "TASK-U1",
                "swu_id": "SWU-U1",
                "strict_coverage": True,
                "execution_contract": {
                    "writeProfile": "material-bound",
                    "materialWrites": ["target.txt"],
                    "executionOutputs": ["receipts/U1.json"],
                    "allowedWrites": ["target.txt", "receipts/U1.json"],
                    "validationCommands": self.validation_commands,
                    "lifecycleOwner": "sigil-development",
                    "authorityClass": "public",
                    "publicationClass": "public",
                },
            },
        )
        (self.root / "target.txt").write_text("baseline\n", encoding="utf-8")
        (self.root / "staged/target.txt").write_text("updated\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build_request(self):
        epoch = "epoch-" + "c" * 24
        unit_digest = "b" * 64
        allowed_routes = [
            {
                "route_id": "route-U1-task-session",
                "frontier_swu": "U1",
                "capability": "task-session",
                "mode": "execute",
                "target": "TASK-U1",
                "write_scope": ["target.txt", "receipts/U1.json"],
                "effect_class": "repository-local-reversible",
                "required_inputs": ["plan-manifest", "selection-receipt"],
                "expected_receipt": "governance-terminal-receipt",
            }
        ]
        continuity_payload = {
            "source_audit_id": "fixture-audit",
            "source_projection_digest": digest(
                {"frontier": ["U1"], "completed_count": 0}
            ),
            "work_pack_semantic_digest": "a" * 64,
            "plan_epoch_id": epoch,
            "completed_prefix": [],
            "next_unit": "U1",
            "authority_effect": "none",
        }
        manifest = {
            "schema_version": "1.0.0",
            "manifest_id": "psm-" + "d" * 24,
            "audit_id": "fixture-audit",
            "work_pack_id": "WP-U1",
            "normalizer_version": "1.0.0",
            "admission_timing": "selected-unit-at-task-session",
            "plan_epoch_id": epoch,
            "canonical_semantic_digest": "a" * 64,
            "semantic_component_digests": {"graph": "e" * 64},
            "unit_contract_digests": {"U1": unit_digest},
            "ready_frontier": ["U1"],
            "source_snapshot_digest": "f" * 64,
            "completion_continuity": {
                **continuity_payload,
                "continuity_digest": digest(continuity_payload),
            },
            "selection_required": True,
            "runtime_admission_status": "pending-selection",
            "allowed_routes": allowed_routes,
            "allowed_routes_digest": digest(allowed_routes),
            "execution_entry": {
                "entry_state": "selection-ready",
                "selected_unit": None,
                "route_id": None,
                "next_owner": {
                    "capability": "implementation-readiness",
                    "mode": "execute",
                    "target": "WP-U1",
                },
                "blocker_code": None,
            },
            "authority_effect": "none",
            "selected_unit": None,
            "mutation_ready": False,
        }
        write_json(self.root / "plan-manifest.json", manifest)
        manifest_bytes = (self.root / "plan-manifest.json").read_bytes()
        selection = {
            "schemaVersion": "1.0.0",
            "selectionVerdict": "select",
            "terminalCode": "SELECTION_READY",
            "requestDigest": "1" * 64,
            "manifestDigest": hashlib.sha256(manifest_bytes).hexdigest(),
            "planEpochId": epoch,
            "canonicalSemanticDigest": "a" * 64,
            "taskId": "TASK-U1",
            "swuId": "SWU-U1",
            "unitContractDigest": unit_digest,
            "dependencyReceiptDigests": [],
            "lifecycleEligibilityDigest": "2" * 64,
            "explicitConfirmationDigest": "3" * 64,
            "selectionIntentSource": "explicit-confirmation",
            "selectionIntentDigest": "3" * 64,
            "authorityEffect": "none",
            "mutationReady": False,
            "reasons": [],
        }
        write_json(self.root / "selection-receipt.json", selection)
        selection_digest = hashlib.sha256(
            (self.root / "selection-receipt.json").read_bytes()
        ).hexdigest()
        target_content = (self.root / "target.txt").read_bytes()
        baselines = [
            {
                "path": "target.txt",
                "state": "present",
                "sha256": hashlib.sha256(target_content).hexdigest(),
                "sizeBytes": len(target_content),
            }
        ]
        validation_digest = digest(self.structured_validation)
        controls = [
            {
                **exact(self.root, "controls/task.md"),
                "role": "task-contract",
                "authorityClass": "public",
            },
            {
                **exact(self.root, "controls/work-pack.md"),
                "role": "work-pack",
                "authorityClass": "public",
            },
            {
                **exact(self.root, "controls/context.json"),
                "role": "context-pack",
                "authorityClass": "public",
            },
        ]
        plan_binding = {
            "task_id": "TASK-U1",
            "swu_id": "SWU-U1",
            "plan_epoch_id": epoch,
            "unit_contract_digest": unit_digest,
            "selection_receipt_digest": selection_digest,
            "attempt_id": "attempt-U1-001",
            "validation_contract_digest": validation_digest,
            "validation_contracts": self.structured_validation,
            "target_baselines": [
                {
                    "path": item["path"],
                    "state": item["state"],
                    "sha256": item["sha256"],
                    "size_bytes": item["sizeBytes"],
                }
                for item in baselines
            ],
        }
        package = {
            "schema_version": "1.0.0",
            "package_id": "package-U1",
            "mutation_mode": "apply-approved",
            "mutation_state": "materialized",
            "lifecycle_owner": "sigil-development",
            "authority_class": "public",
            "publication_class": "public",
            "source_artifacts": [
                {
                    "path": item["path"],
                    "sha256": item["sha256"],
                    "size_bytes": item["sizeBytes"],
                    "authority_class": item["authorityClass"],
                }
                for item in controls
            ],
            "changes": [
                {
                    "target_path": "target.txt",
                    "operation": "update",
                    "output_ref": exact(self.root, "staged/target.txt", camel=False),
                }
            ],
            "target_inventory": [
                {
                    "target_path": "target.txt",
                    "lifecycle_owner": "sigil-development",
                    "authority_class": "public",
                    "publication_class": "public",
                    "dependency_ids": [],
                }
            ],
            "dependencies": [],
            "mirror_groups": [],
            "approval": {
                "class": "explicit-apply",
                "owner": "sigil-development",
                "scope_paths": ["target.txt"],
                "authority_classes": ["public"],
                "publication_classes": ["public"],
            },
            "validation_commands": self.validation_commands,
            "plan_binding": plan_binding,
        }
        receipt = PRODUCER.validate_material_package(
            package,
            self.root,
            json.loads((INVOKE / "schemas/material-package.schema.json").read_text()),
            json.loads((INVOKE / "schemas/material-package-receipt.schema.json").read_text()),
        )
        self.assertEqual(receipt["patchVerdict"], "pass")
        write_json(self.root / "material-package.json", package)
        write_json(self.root / "material-receipt.json", receipt)
        return {
            "schemaVersion": "1.2.0",
            "admissionProfile": "plan-once-selected-unit",
            "executionMode": "routed-mutation",
            "taskId": "TASK-U1",
            "swuId": "SWU-U1",
            "controlArtifacts": controls,
            "dependencyFrontier": [],
            "materialPackage": exact(self.root, "material-package.json"),
            "materialReceipt": exact(self.root, "material-receipt.json"),
            "producerReceiptSchema": exact(self.root, "schemas/material-receipt.schema.json"),
            "materialWrites": ["target.txt"],
            "executionOutputs": ["receipts/U1.json"],
            "allowedWrites": ["target.txt", "receipts/U1.json"],
            "validationCommands": self.validation_commands,
            "lifecycleOwner": "sigil-development",
            "authorityClass": "public",
            "publicationClass": "public",
            "planAdmission": {
                "planManifest": exact(self.root, "plan-manifest.json"),
                "planManifestSchema": exact(self.root, "schemas/plan-manifest.schema.json"),
                "selectionReceipt": exact(self.root, "selection-receipt.json"),
                "selectionReceiptSchema": exact(self.root, "schemas/selection-receipt.schema.json"),
                "planEpochId": epoch,
                "unitContractDigest": unit_digest,
                "attemptId": "attempt-U1-001",
                "targetBaselines": baselines,
                "structuredValidationContracts": self.structured_validation,
                "validationContractDigest": validation_digest,
            },
        }

    def resolve(self, request):
        request_schema = json.loads(
            (TASK_SESSION / "schemas/mutation-admission-request.schema.json").read_text()
        )
        receipt_schema = json.loads(
            (TASK_SESSION / "schemas/mutation-admission-receipt.schema.json").read_text()
        )
        result = ADMISSION.resolve_mutation_admission(request, self.root, request_schema)
        errors = list(Draft202012Validator(receipt_schema).iter_errors(result))
        self.assertEqual([error.message for error in errors], [])
        return result

    def test_exact_plan_identity_and_live_baseline_admit(self) -> None:
        result = self.resolve(self.build_request())
        self.assertEqual(result["admissionVerdict"], "admit")
        self.assertTrue(result["mutationReady"])
        self.assertTrue(result["singleUse"])
        self.assertIsNotNone(result["admissionToken"])

    def test_live_target_change_blocks_before_mutation(self) -> None:
        request = self.build_request()
        (self.root / "target.txt").write_text("concurrent drift\n", encoding="utf-8")
        result = self.resolve(request)
        self.assertEqual(result["admissionVerdict"], "block")
        self.assertFalse(result["mutationReady"])
        self.assertIn("target baseline digest mismatch: target.txt", result["reasons"])

    def test_cross_attempt_package_reuse_blocks(self) -> None:
        request = self.build_request()
        request["planAdmission"]["attemptId"] = "attempt-U1-002"
        result = self.resolve(request)
        self.assertEqual(result["admissionVerdict"], "block")
        self.assertIn("material package plan binding mismatch", result["reasons"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

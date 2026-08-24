#!/usr/bin/env python3
"""Plan-once audit and explicit selection regression tests."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPELL_ROOT / "scripts"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_module("wpra_audit_plan_once", SPELL_ROOT / "scripts/audit_work_pack.py")
SELECT = load_module(
    "wpra_select_plan_once", SPELL_ROOT / "scripts/verify_plan_selection.py"
)
BASE = load_module(
    "wpra_v2_fixture", SPELL_ROOT / "development/test_work_pack_readiness_v2.py"
)


def exact(root: Path, relative: str) -> dict[str, object]:
    content = (root / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def refresh_evidence_refs(value, reference):
    if isinstance(value, dict):
        if set(value) == {"path", "sha256", "size_bytes"} and value["path"] == "evidence.json":
            value.update(reference)
        else:
            for child in value.values():
                refresh_evidence_refs(child, reference)
    elif isinstance(value, list):
        for child in value:
            refresh_evidence_refs(child, reference)


class PlanOnceSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = BASE.V2Fixture()
        evidence = json.loads(self.fixture.evidence_path.read_text(encoding="utf-8"))
        evidence["mutableStatus"] = {"cursor": "planned"}
        self.fixture.evidence_path.write_text(
            json.dumps(evidence, sort_keys=True), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.fixture.close()

    def config(self):
        config = self.fixture.config()
        refresh_evidence_refs(config, self.fixture.exact())
        config["admission_timing"] = "selected-unit-at-task-session"
        unit = config["execution_bindings"][0]
        unit["task_id"] = "TASK-U1"
        unit["swu_id"] = "SWU-U1"
        unit["lifecycle_owner"] = "sigil-development"
        unit["authority_class"] = "public"
        unit["publication_class"] = "public"
        unit["attempt_contract"] = {
            "id_policy": "attempt-id-equals-task-session-run-id",
            "collision_policy": "reject-existing-different-ticket",
            "success_teardown": "retain-terminal-receipt",
            "failure_teardown": "retain-block-receipt",
        }
        unit["validation_contracts"] = [
            {
                "command_id": "verify-U1",
                "argv": ["false"],
                "cwd": ".",
                "timeout_seconds": 30,
                "max_output_bytes": 4096,
            }
        ]
        unit["material_package"].update(
            package_ref=None,
            producer_receipt_ref=None,
            schema_ref=None,
            declared_sha256=None,
            target_inventory_ref=None,
        )
        unit["byte_baselines"] = []
        config["runtime_binding"]["task_session_admission_receipt_ref"] = None
        routes = [
            {
                "route_id": "task-session-U1",
                "frontier_swu": "U1",
                "capability": "task-session",
                "mode": "execute",
                "target": "SWU-U1",
                "write_scope": unit["allowed_writes"],
                "effect_class": "repository-local-reversible",
                "required_inputs": [
                    "plan-semantic-manifest.json",
                    "selection-receipt.json",
                ],
                "expected_receipt": "receipts/U1.json",
            },
            {
                "route_id": "invoke-refresh-U1",
                "frontier_swu": "U1",
                "capability": "invoke",
                "mode": "refresh",
                "target": config["audit_id"],
                "write_scope": ["planning/"],
                "effect_class": "repository-local-reversible",
                "required_inputs": ["work-pack-readiness-report-v2.json"],
                "expected_receipt": "receipts/refresh-U1.json",
            },
        ]
        config["execution_policy"] = {
            "work_pack_id": "WP-U1",
            "route_policy": "automatic-in-scope",
            "allowed_routes": routes,
            "allowed_routes_digest": AUDIT.digest_bytes(AUDIT.canonical_bytes(routes)),
            "automatic_decisions": [
                "internal-tool-selection",
                "capability-owner-routing",
                "fresh-task-session-resumption",
            ],
            "stop_decisions": [
                "product-or-semantic-choice",
                "scope-expansion",
                "destructive-or-irreversible-effect",
                "failed-acceptance-critical-validation",
            ],
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
        }
        for section in ("status_receipt_refs", "lifecycle_status_refs"):
            for key, status in config[section].items():
                status["receipt_ref"]["selector"] = "/mutableStatus"
                status["receipt_ref"]["binding_id"] = f"{section}-{key}"
        return config

    def audit(self, config):
        errors = AUDIT.schema_errors(
            config, AUDIT.load_json(AUDIT.CONFIG_SCHEMA_V2), "v2 config"
        )
        self.assertEqual(errors, [])
        return AUDIT.audit_v2(config, self.fixture.root)

    def test_no_material_is_pending_selection_not_refresh(self) -> None:
        report = self.audit(self.config())
        self.assertEqual(report["verdict"], "pass")
        self.assertEqual(report["terminal_code"], "PLAN_SEMANTIC_READY")
        self.assertEqual(report["runtime_admission_status"], "pending-selection")
        self.assertEqual(report["next_owner"], "implementation-readiness:execute")
        self.assertEqual(report["execution_entry"]["entry_state"], "selection-ready")
        self.assertEqual(
            report["execution_entry"]["next_owner"]["capability"],
            "implementation-readiness",
        )
        self.assertFalse(report["mutation_ready"])
        self.assertIsNone(report["selected_unit"])
        self.assertEqual(report["manifest"]["authority_effect"], "none")

        output = self.fixture.root / "audit-output"
        AUDIT.write_outputs_v2(report, output)
        manifest_path = output / "plan-semantic-manifest.json"
        handoff_path = output / "selection-handoff.json"
        self.assertTrue(manifest_path.is_file())
        self.assertTrue(handoff_path.is_file())
        self.assertFalse((output / "objective-execution-manifest.json").exists())

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["approval_status"], "unapproved")
        self.assertEqual(handoff["approval_status"], "unapproved")
        self.assertIsNone(manifest["selected_unit"])
        self.assertIsNone(handoff["execution_entry"]["selected_unit"])
        self.assertFalse(manifest["mutation_ready"])
        self.assertFalse(handoff["mutation_ready"])

    def test_closeout_only_effect_subtype_is_schema_invalid(self) -> None:
        config = self.config()
        routes = config["execution_policy"]["allowed_routes"]
        routes[1]["effect_class"] = (
            "repository-local-reversible-closeout-only"
        )
        config["execution_policy"]["allowed_routes_digest"] = AUDIT.digest_bytes(
            AUDIT.canonical_bytes(routes)
        )
        errors = AUDIT.schema_errors(
            config, AUDIT.load_json(AUDIT.CONFIG_SCHEMA_V2), "v2 config"
        )
        self.assertTrue(
            any(
                "execution_policy/allowed_routes/1/effect_class" in error
                and "repository-local-reversible" in error
                for error in errors
            )
        )

    def test_status_only_bytes_preserve_epoch_but_command_drift_does_not(self) -> None:
        config = self.config()
        first = self.audit(config)["manifest"]
        evidence = json.loads(self.fixture.evidence_path.read_text(encoding="utf-8"))
        evidence["mutableStatus"]["cursor"] = "selected"
        self.fixture.evidence_path.write_text(
            json.dumps(evidence, sort_keys=True), encoding="utf-8"
        )
        refresh_evidence_refs(config, self.fixture.exact())
        second = self.audit(config)["manifest"]
        self.assertEqual(first["plan_epoch_id"], second["plan_epoch_id"])
        self.assertNotEqual(
            first["source_snapshot_digest"], second["source_snapshot_digest"]
        )

        drifted = copy.deepcopy(config)
        drifted["execution_bindings"][0]["command"]["cwd"] = "changed"
        third = self.audit(drifted)["manifest"]
        self.assertNotEqual(first["plan_epoch_id"], third["plan_epoch_id"])
        self.assertNotEqual(
            first["unit_contract_digests"]["U1"],
            third["unit_contract_digests"]["U1"],
        )

    def test_semantic_drift_emits_exact_refresh_entry(self) -> None:
        config = self.config()
        config["expected_semantic_digest"] = "f" * 64
        report = self.audit(config)
        self.assertEqual(report["verdict"], "block")
        self.assertEqual(report["next_owner"], "invoke:refresh")
        self.assertEqual(report["runtime_admission_status"], "block")
        self.assertEqual(
            report["execution_entry"]["entry_state"], "owner-prerequisite"
        )
        self.assertEqual(report["execution_entry"]["selected_unit"], "U1")
        self.assertEqual(report["execution_entry"]["route_id"], "invoke-refresh-U1")
        self.assertEqual(
            report["execution_entry"]["next_owner"],
            {
                "capability": "invoke",
                "mode": "refresh",
                "target": config["audit_id"],
            },
        )
        self.assertIsNone(report["execution_entry"]["blocker_code"])

    def test_selection_recomputes_epoch_and_binds_current_eligibility(self) -> None:
        config = self.config()
        config_path = self.fixture.root / "plan-config.json"
        config_path.write_text(
            json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        report = self.audit(config)
        output = self.fixture.root / "audit-output"
        AUDIT.write_outputs_v2(report, output)
        request = {
            "schemaVersion": "1.0.0",
            "manifestRef": exact(self.fixture.root, "audit-output/plan-semantic-manifest.json"),
            "auditConfigPath": "plan-config.json",
            "taskId": "TASK-U1",
            "swuId": "SWU-U1",
            "executionIntentBinding": {
                "bindingId": "wpeb-111111111111111111111111",
                "sourceInvocationId": "invoke-public-fixture",
                "workPackId": "WP-U1",
                "bindingDigest": "1" * 64,
                "authorityEffect": "bounded-execution-only",
            },
            "dependencyReceipts": [],
            "lifecycleEligibility": {
                "eligible": True,
                "state": "selected",
                "evidenceRefs": [self.fixture.exact()],
            },
        }
        receipt = SELECT.select_unit(
            request,
            self.fixture.root,
            AUDIT.load_json(SPELL_ROOT / "schemas/selection-request.schema.json"),
            AUDIT.load_json(SPELL_ROOT / "schemas/plan-semantic-manifest.schema.json"),
            AUDIT.load_json(AUDIT.CONFIG_SCHEMA_V2),
        )
        self.assertEqual(receipt["selectionVerdict"], "select")
        self.assertEqual(receipt["terminalCode"], "SELECTION_READY")
        self.assertFalse(receipt["mutationReady"])
        self.assertEqual(receipt["selectionIntentSource"], "execution-intent-binding")
        self.assertIsNone(receipt["explicitConfirmationDigest"])
        self.assertEqual(
            receipt["unitContractDigest"],
            report["manifest"]["unit_contract_digests"]["U1"],
        )

        changed = copy.deepcopy(config)
        changed["execution_bindings"][0]["command"]["cwd"] = "drifted"
        config_path.write_text(
            json.dumps(changed, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        blocked = SELECT.select_unit(
            request,
            self.fixture.root,
            AUDIT.load_json(SPELL_ROOT / "schemas/selection-request.schema.json"),
            AUDIT.load_json(SPELL_ROOT / "schemas/plan-semantic-manifest.schema.json"),
            AUDIT.load_json(AUDIT.CONFIG_SCHEMA_V2),
        )
        self.assertEqual(blocked["selectionVerdict"], "block")
        self.assertIn(blocked["terminalCode"], {"PLAN_EPOCH_STALE", "PLAN_COMPONENT_CHANGED"})

    def test_each_immutable_unit_contract_family_invalidates_epoch(self) -> None:
        baseline_config = self.config()
        baseline = self.audit(baseline_config)["manifest"]
        mutations = {
            "graph": lambda c: c["execution_bindings"][0].update(
                canonical_successors=["__different_terminal__"]
            ),
            "writes": lambda c: c["execution_bindings"][0].update(
                material_writes=["other.txt"],
                allowed_writes=["other.txt", "receipts/U1.json"],
            ),
            "owner": lambda c: c["execution_bindings"][0].update(
                lifecycle_owner="other-owner"
            ),
            "authority": lambda c: c["execution_bindings"][0].update(
                authority_class="private"
            ),
            "publication": lambda c: c["execution_bindings"][0].update(
                publication_class="internal"
            ),
            "attempt": lambda c: c["execution_bindings"][0][
                "attempt_contract"
            ].update(collision_policy="reject-all-existing"),
            "validation": lambda c: c["execution_bindings"][0][
                "validation_contracts"
            ][0].update(timeout_seconds=31),
            "receipt": lambda c: c["receipt_bindings"][
                "semantic_validator_ref"
            ].update(owner_ref="other-validator-owner"),
            "closeout": lambda c: c["closeout_bindings"][0][
                "compensation"
            ].update(rationale="Different no-side-effect rationale."),
            "runtime": lambda c: c["runtime_binding"].update(
                requested_task_session_execution_mode="reusable-mutation"
            ),
            "risk": lambda c: c["approval_policy"]["run_budget"].update(
                max_task_session_requests=2
            ),
            "execution-policy": lambda c: c["execution_policy"].update(
                automatic_decisions=[
                    "internal-tool-selection",
                    "capability-owner-routing",
                    "declared-fallback",
                ]
            ),
        }
        for family, mutate in mutations.items():
            with self.subTest(family=family):
                current_config = copy.deepcopy(baseline_config)
                mutate(current_config)
                current = self.audit(current_config)["manifest"]
                self.assertNotEqual(
                    baseline["plan_epoch_id"], current["plan_epoch_id"]
                )
                self.assertNotEqual(
                    baseline["unit_contract_digests"]["U1"],
                    current["unit_contract_digests"]["U1"],
                )

    def test_normalizer_rejects_duplicate_bindings_unknown_selectors_and_floats(self) -> None:
        duplicate = self.config()
        duplicate["closure_receipt_refs"][1]["binding_id"] = duplicate[
            "closure_receipt_refs"
        ][0]["binding_id"]
        report = self.audit(duplicate)
        self.assertEqual(report["verdict"], "block")
        self.assertTrue(
            any(
                item["code"] == "PLAN_SEMANTIC_NORMALIZATION_FAILED"
                and "duplicate binding id" in item["claim"]
                for item in report["blockers"]
            )
        )

        unknown = self.config()
        unknown["authority_bindings"]["semantic_bindings"]["owner"][
            "selector"
        ] = "/does-not-exist"
        report = self.audit(unknown)
        self.assertEqual(report["verdict"], "block")
        self.assertTrue(
            any(item["code"] == "BINDING_SELECTOR_UNRESOLVED" for item in report["blockers"])
        )

        floating = self.config()
        evidence = json.loads(self.fixture.evidence_path.read_text(encoding="utf-8"))
        evidence["objective"]["weight"] = 0.5
        self.fixture.evidence_path.write_text(
            json.dumps(evidence, sort_keys=True), encoding="utf-8"
        )
        refresh_evidence_refs(floating, self.fixture.exact())
        report = self.audit(floating)
        self.assertEqual(report["verdict"], "block")
        self.assertTrue(
            any(
                item["code"] == "PLAN_SEMANTIC_NORMALIZATION_FAILED"
                and "floating-point" in item["claim"]
                for item in report["blockers"]
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

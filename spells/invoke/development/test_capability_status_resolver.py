#!/usr/bin/env python3
"""Causal fixtures for Invoke's three independent capability ceilings."""

from __future__ import annotations

import hashlib
import copy
import importlib.util
import json
import unittest
from pathlib import Path


INVOKE = Path(__file__).parents[1]
SCRIPT = INVOKE / "scripts" / "capability_status_resolver.py"
SPEC = importlib.util.spec_from_file_location("capability_status_resolver", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CapabilityStatusResolverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capability_path = INVOKE / "mode-capabilities.json"
        cls.capabilities = json.loads(cls.capability_path.read_text(encoding="utf-8"))
        cls.capability_sha = hashlib.sha256(cls.capability_path.read_bytes()).hexdigest()
        cls.request_schema = json.loads(
            (INVOKE / "schemas" / "capability-status-request.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.result_schema = json.loads(
            (INVOKE / "schemas" / "capability-status-result.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.material_schema = json.loads(
            (INVOKE / "schemas" / "material-package-receipt.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def artifact(self, mode, status="pass"):
        artifact = {
            "receipt_id": f"artifact-{mode}",
            "axis": "artifact_authored",
            "mode": mode,
            "status": status,
            "evidence": [f"{mode}.md"],
        }
        if mode == "define" and status == "pass":
            artifact["producer_receipt"] = self.define_producer_receipt()
            artifact["producer_admission_receipt"] = self.define_admission_receipt(
                artifact["producer_receipt"]
            )
        if mode == "design" and status == "pass":
            artifact["producer_receipt"] = self.design_producer_receipt()
            artifact["producer_admission_receipt"] = self.design_admission_receipt(
                artifact["producer_receipt"]
            )
        return artifact

    def design_producer_receipt(self):
        exact = lambda path, digest, size=1: {"path": path, "sha256": digest, "size": size}
        output_specs = list(MODULE.design_stage_contract.OUTPUTS) if hasattr(MODULE, "design_stage_contract") else [
            ("design-artifact", "DESIGN.json"),
            ("architecture", "ARCHITECTURE.md"),
            ("selected-companions", "SELECTED-COMPANIONS.md"),
            ("glossary-consistency", "GLOSSARY-CONSISTENCY-REPORT.json"),
            ("planned-witnesses", "PLANNED-WITNESS-CONTRACTS.json"),
            ("layering", "IMPLEMENTATION-LAYERING.md"),
            ("template-selection", "TEMPLATE-SELECTION-RECEIPT.json"),
            ("dispatch-trace", "DISPATCH-TRACE.json"),
            ("distill", "DISTILL-RECEIPT.json"),
            ("scope-manifest", "DESIGN-SCOPE-MANIFEST.json"),
            ("denominator-receipt", "DESIGN-DENOMINATOR-RECEIPT.json"),
            ("selection-result", "DESIGN-SELECTION-RESULT.json"),
            ("coherence-receipt", "DESIGN-COHERENCE-RECEIPT.json"),
            ("transport", "DESIGN-TRANSPORT-REPORT.json"),
        ]
        closure_ref = exact("fixture/DESIGN-BUNDLE-CLOSURE.json", "1" * 64)
        candidate_ref = exact("fixture/W2/DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json", "2" * 64)
        receipt = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-result/v3",
            "schema_version": "invoke.design-stage-receipt.v3",
            "receipt_id": "design-w3:fixture:receipt",
            "owner_capability": "invoke",
            "mode": "design",
            "target_id": "design-target:fixture",
            "producer": {
                "identity": "invoke.compile-design-source.v3",
                "owner": "invoke-design-producer",
                "path": "arcanum/spells/invoke/scripts/compile_design_source_v3.py",
                "sha256": hashlib.sha256((INVOKE / "scripts" / "compile_design_source_v3.py").read_bytes()).hexdigest(),
            },
            "profile_id": "invoke.generic-design-baseline.v1",
            "activation_kind": "normal",
            "bindings": {
                "bundle_closure_ref": closure_ref,
                "process_ref": exact("fixture/process.json", "3" * 64),
                "profile_ref": exact("fixture/profile.json", "4" * 64),
                "coherence_policy_ref": exact("fixture/policy.json", "5" * 64),
                "w1_production_receipt_ref": exact("fixture/W1/receipt.json", "6" * 64),
                "candidate_production_receipt_ref": candidate_ref,
                "design_source_ref": exact("fixture/DESIGN-SOURCE.json", "7" * 64),
                "design_artifact_ref": exact("fixture/W2/DESIGN.json", "8" * 64),
                "coherence_receipt_ref": exact("fixture/W2/coherence.json", "9" * 64),
                "distill_evidence": {
                    "request_ref": exact("fixture/distill/request.json", "a" * 64),
                    "events_ref": exact("fixture/distill/events.jsonl", "b" * 64),
                    "execution_receipt_ref": exact("fixture/distill/receipt.json", "c" * 64),
                    "validation_result_ref": exact("fixture/distill/validation.json", "d" * 64),
                },
            },
            "outputs": [
                {"kind": kind, "path": path, "sha256": hashlib.sha256(kind.encode()).hexdigest(), "size": len(kind)}
                for kind, path in output_specs
            ],
            "result": "pass",
            "selection_evidence_state": "design-validator-pass",
            "coherence_state": "pass",
            "human_views_state": "pass",
            "distill_state": "pass",
            "evidence_state": "design-stage-pass",
            "plan_evidence_state": "plan-evidence-pending",
            "next_route": "plan",
            "evidence_ceiling": {
                "artifact_authored": True,
                "coherence_validated": True,
                "human_views_produced": True,
                "design_stage_pass": True,
                "plan_evidence": False,
                "registry_released": False,
                "mutation_runtime_ready": False,
                "acceptance": False,
                "execution": False,
                "publication": False,
                "deployment": False,
                "external_effect": False,
            },
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = MODULE.canonical_digest(receipt, "receipt_digest")
        return receipt

    def design_admission_receipt(self, producer):
        inventory = [
            {**item, "path": f"fixture/W3/{item['path']}"}
            for item in producer["outputs"]
        ]
        stage_digest = "e" * 64
        inventory.append({
            "kind": "stage-receipt",
            "path": "fixture/W3/INVOKE-DESIGN-STAGE-RECEIPT.json",
            "sha256": stage_digest,
            "size": 10,
        })
        receipt = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2",
            "schema_version": "invoke.design-bundle-admission-receipt.v2",
            "receipt_id": "design-admission:fixture",
            "validator": {
                "identity": "invoke.validate-design-bundle-admission.v2",
                "owner": "invoke-design-bundle-admission-validator",
                "path": "arcanum/spells/invoke/scripts/validate_design_bundle_admission_v2.py",
                "sha256": hashlib.sha256((INVOKE / "scripts" / "validate_design_bundle_admission_v2.py").read_bytes()).hexdigest(),
            },
            "bundle_root": "fixture/W3",
            "stage_receipt_ref": {
                "path": "fixture/W3/INVOKE-DESIGN-STAGE-RECEIPT.json",
                "sha256": stage_digest,
                "size": 10,
            },
            "producer_binding": {
                "receipt_id": producer["receipt_id"],
                "receipt_digest": producer["receipt_digest"],
                "profile_id": producer["profile_id"],
                "producer": copy.deepcopy(producer["producer"]),
            },
            "output_inventory": inventory,
            "checks": [
                {"check_id": check_id, "status": "pass", "evidence_refs": [copy.deepcopy(producer["bindings"]["bundle_closure_ref"])], "causal_blocker_ids": []}
                for check_id in ("stage-receipt-validation", "producer-identity", "bundle-closure-binding", "output-inventory", "projection-replay", "distill-evidence", "authority-ceiling")
            ],
            "replay": {
                "bundle_closure_ref": copy.deepcopy(producer["bindings"]["bundle_closure_ref"]),
                "candidate_receipt_ref": copy.deepcopy(producer["bindings"]["candidate_production_receipt_ref"]),
                "comparison": "pass",
                "output_inventory_digest": hashlib.sha256(json.dumps(inventory, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "differences": [],
            },
            "result": "pass",
            "blockers": [],
            "evidence_ceiling": {
                "artifact_authored": True,
                "registry_released": False,
                "mutation_runtime_ready": False,
                "acceptance": False,
                "execution": False,
                "publication": False,
                "deployment": False,
                "external_effect": False,
            },
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = MODULE.canonical_digest(receipt, "receipt_digest")
        return receipt

    def define_producer_receipt(self):
        kinds = [
            ("semantic-context", "DEFINE-SEMANTIC-CONTEXT.json"),
            ("semantic-closure-receipt", "DEFINE-SEMANTIC-CLOSURE-RECEIPT.json"),
            ("spec", "SPEC.md"),
            ("definitions", "DEFINITIONS.json"),
            ("definitions-view", "DEFINITIONS.md"),
            ("glossary", "GLOSSARY.md"),
            ("layering", "IMPLEMENTATION-LAYERING.md"),
            ("template-selection", "TEMPLATE-SELECTION-RECEIPT.json"),
            ("dispatch-trace", "DISPATCH-TRACE.json"),
            ("distill", "DISTILL-RECEIPT.json"),
            ("identity-denominator", "IDENTITY-DENOMINATOR-RECEIPT.json"),
            ("transport", "DEFINE-TRANSPORT-REPORT.json"),
        ]
        exact = lambda path, digest: {"path": path, "sha256": digest, "size": 1}
        receipt = {
            "$schema": "https://arcanum.dev/schemas/invoke/define-result/v3",
            "schema_version": "invoke.define-stage-receipt.v3",
            "receipt_id": "define-v3:fixture:receipt",
            "owner_capability": "invoke",
            "mode": "define",
            "producer": {
                "identity": "invoke.compile-define-source.v3",
                "path": "arcanum/spells/invoke/scripts/compile_define_source_v3.py",
                "sha256": hashlib.sha256(
                    (INVOKE / "scripts" / "compile_define_source_v3.py").read_bytes()
                ).hexdigest(),
            },
            "schema_bindings": {
                "source_schema_ref": exact("schemas/source.json", "1" * 64),
                "profile_schema_ref": exact("schemas/profile.json", "2" * 64),
                "definitions_v1_schema_ref": exact("schemas/definitions-v1.json", "3" * 64),
                "definitions_v2_schema_ref": exact("schemas/definitions-v2.json", "4" * 64),
                "result_schema_ref": exact("schemas/result.json", "5" * 64),
            },
            "profile_id": "invoke.generic-definitions-baseline.v3",
            "source_ref": exact("fixture/source.json", "a" * 64),
            "semantic_evidence": {
                "context_ref": exact("fixture/context.json", "b" * 64),
                "closure_receipt_ref": exact("fixture/closure.json", "c" * 64),
            },
            "structural_schema_refs": [],
            "semantic_outcome": "mixed",
            "outputs": [
                {
                    "kind": kind,
                    "path": path,
                    "sha256": hashlib.sha256(kind.encode()).hexdigest(),
                    "size": len(kind),
                }
                for kind, path in kinds
            ],
            "result": "pass",
            "next_route": "design",
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = MODULE.canonical_digest(receipt, "receipt_digest")
        return receipt

    def define_admission_receipt(self, producer):
        exact = lambda path, digest, size=1: {"path": path, "sha256": digest, "size": size}
        inventory = [
            {
                "kind": item["kind"],
                "path": f"fixture/bundle/{item['path']}",
                "sha256": item["sha256"],
                "size": item["size"],
            }
            for item in producer["outputs"]
        ]
        stage_digest = "d" * 64
        inventory.append(
            {
                "kind": "stage-receipt",
                "path": "fixture/bundle/INVOKE-DEFINE-STAGE-RECEIPT.json",
                "sha256": stage_digest,
                "size": 10,
            }
        )
        receipt = {
            "$schema": "https://arcanum.dev/schemas/invoke/define-bundle-admission-receipt/v1",
            "schema_version": "invoke.define-bundle-admission-receipt.v1",
            "receipt_id": "admission:fixture:receipt",
            "validator": {
                "identity": "invoke.validate-define-bundle-admission.v1",
                "path": "arcanum/spells/invoke/scripts/validate_define_bundle_admission.py",
                "sha256": hashlib.sha256(
                    (INVOKE / "scripts" / "validate_define_bundle_admission.py").read_bytes()
                ).hexdigest(),
            },
            "schema_bindings": {
                "admission_schema_ref": exact("schemas/admission.json", "1" * 64),
                "result_schema_ref": exact("schemas/result.json", "2" * 64),
                "definitions_schema_ref": exact("schemas/definitions.json", "3" * 64),
                "context_schema_ref": exact("schemas/context.json", "4" * 64),
                "closure_schema_ref": exact("schemas/closure.json", "5" * 64),
            },
            "bundle_root": "fixture/bundle",
            "bundle_digest": MODULE.canonical_value_digest(inventory),
            "stage_receipt_ref": exact(
                "fixture/bundle/INVOKE-DEFINE-STAGE-RECEIPT.json", stage_digest, 10
            ),
            "producer_binding": {
                "receipt_id": producer["receipt_id"],
                "receipt_digest": producer["receipt_digest"],
                "profile_id": producer["profile_id"],
                "producer": copy.deepcopy(producer["producer"]),
            },
            "output_inventory": inventory,
            "structural_schema_refs": [],
            "replay": {
                "source_ref": copy.deepcopy(producer["source_ref"]),
                "discovery_roots": ["fixture"],
                "public_roots": ["fixture"],
                "clean_bundle_digest": "e" * 64,
                "comparison": "pass",
            },
            "drift_analysis": {
                "compile_window": "current",
                "prior_admission": "not_provided",
                "summary": {
                    "evidence_state": "current",
                    "semantic_state": "unchanged",
                    "authority_state": "unchanged",
                    "topology_state": "unchanged",
                    "projection_state": "unchanged",
                    "overall": "current",
                },
                "differences": [],
            },
            "checks": [
                {"check_id": check_id, "status": "pass", "detail": "fixture admission passes"}
                for check_id in MODULE.DEFINE_ADMISSION_CHECK_IDS
            ],
            "blockers": [],
            "result": "pass",
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = MODULE.canonical_digest(receipt, "receipt_digest")
        return receipt

    def define_v2_producer_receipt(self):
        kinds = [
            "spec",
            "definitions",
            "definitions-view",
            "glossary",
            "layering",
            "template-selection",
            "dispatch-trace",
            "distill",
            "identity-denominator",
            "transport",
        ]
        receipt = {
            "schema_version": "invoke.define-stage-receipt.v2",
            "receipt_id": "define:fixture:receipt",
            "owner_capability": "invoke",
            "mode": "define",
            "producer": {
                "identity": "invoke.compile-define-source.v2",
                "path": "arcanum/spells/invoke/scripts/compile_define_source_v2.py",
                "sha256": hashlib.sha256(
                    (INVOKE / "scripts" / "compile_define_source_v2.py").read_bytes()
                ).hexdigest(),
            },
            "profile_id": "invoke.generic-definitions-baseline.v2",
            "source_ref": {"path": "fixture/source.json", "sha256": "a" * 64, "size": 1},
            "outputs": [{"kind": kind, "path": f"{kind}.out", "sha256": hashlib.sha256(kind.encode()).hexdigest(), "size": len(kind)} for kind in kinds],
            "result": "pass",
            "next_route": "design",
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        projection = copy.deepcopy(receipt)
        projection.pop("receipt_digest")
        receipt["receipt_digest"] = hashlib.sha256(json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return receipt

    def define_v1_producer_receipt(self):
        kinds = [
            "spec",
            "glossary",
            "layering",
            "template-selection",
            "dispatch-trace",
            "distill",
            "identity-denominator",
            "transport",
        ]
        receipt = {
            "schema_version": "invoke.define-stage-receipt.v1",
            "receipt_id": "define:fixture:v1-receipt",
            "owner_capability": "invoke",
            "mode": "define",
            "producer": {
                "identity": "invoke.compile-define-source.v1",
                "path": "arcanum/spells/invoke/scripts/compile_define_source.py",
                "sha256": hashlib.sha256(
                    (INVOKE / "scripts" / "compile_define_source.py").read_bytes()
                ).hexdigest(),
            },
            "profile_id": "invoke.generic-spec-baseline.v1",
            "source_ref": {
                "path": "fixture/source.json",
                "sha256": "a" * 64,
                "size": 1,
            },
            "outputs": [
                {
                    "kind": kind,
                    "path": f"{kind}.out",
                    "sha256": hashlib.sha256(kind.encode()).hexdigest(),
                    "size": len(kind),
                }
                for kind in kinds
            ],
            "result": "pass",
            "next_route": "design",
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        projection = copy.deepcopy(receipt)
        projection.pop("receipt_digest")
        receipt["receipt_digest"] = hashlib.sha256(
            json.dumps(
                projection,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()
        return receipt

    def registry(self, mode, digest=None):
        return {
            "receipt_id": f"registry-{mode}",
            "axis": "registry_released",
            "mode": mode,
            "status": "released",
            "owner": "invoke-owner",
            "capability_sha256": digest or self.capability_sha,
            "deterministic_validation": {
                "status": "pass",
                "evidence": "deterministic-validation.json",
            },
            "live_regime": {
                "status": "pass",
                "evidence": "live-regime.json",
            },
        }

    def material(self):
        return {
            "schemaVersion": "1.0.0",
            "packageId": "package-1",
            "patchVerdict": "pass",
            "mutationHandoff": "ready",
            "packageDigest": "a" * 64,
            "validatedPaths": ["target.md"],
            "dependencyResult": "pass",
            "ownerBoundaryResult": "pass",
            "publicationBoundaryResult": "pass",
            "validationCommands": ["test target"],
            "lifecycleOwner": "invoke-owner",
            "authorityClass": "public",
            "publicationClass": "public",
            "reasons": [],
        }

    def runtime(self, mode, digest=None, gates=None):
        required = self.capabilities["modes"][mode]["runtime_required_gates"]
        return {
            "receipt_id": f"runtime-{mode}",
            "axis": "mutation_runtime_ready",
            "mode": mode,
            "status": "ready",
            "capability_sha256": digest or self.capability_sha,
            "material_package_id": "package-1",
            "material_package_digest": "a" * 64,
            "gates": gates or [
                {"gate": gate, "status": "pass", "evidence": f"{gate}.json"}
                for gate in required
            ],
        }

    def resolve(self, request):
        return MODULE.resolve_capability_status(
            request,
            self.capabilities,
            self.capability_sha,
            self.request_schema,
            self.result_schema,
            self.material_schema,
        )

    def base(self, mode):
        return {
            "schema_version": "invoke.capability-status.request.v1",
            "mode": mode,
        }

    def test_all_active_modes_support_artifact_only_without_later_axes(self):
        for mode in ("define", "design", "plan", "handoff", "refresh"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request["artifact_receipt"] = self.artifact(mode)
                result = self.resolve(request)
                self.assertEqual("pass", result["artifact_authored"]["status"])
                self.assertFalse(result["registry_released"]["status"])
                self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_define_generic_self_assertion_cannot_open_new_pass(self):
        request = self.base("define")
        receipt = self.artifact("define")
        receipt.pop("producer_receipt")
        request["artifact_receipt"] = receipt
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])

    def test_design_generic_self_assertion_cannot_open_new_pass(self):
        request = self.base("design")
        receipt = self.artifact("design")
        receipt.pop("producer_receipt")
        receipt.pop("producer_admission_receipt")
        request["artifact_receipt"] = receipt
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])

    def test_design_forged_producer_or_admission_validator_blocks(self):
        for mutation in ("producer", "admission-validator"):
            with self.subTest(mutation=mutation):
                request = self.base("design")
                receipt = self.artifact("design")
                if mutation == "producer":
                    receipt["producer_receipt"]["producer"]["sha256"] = "0" * 64
                else:
                    receipt["producer_admission_receipt"]["validator"]["sha256"] = "0" * 64
                request["artifact_receipt"] = receipt
                self.assertEqual("block", self.resolve(request)["artifact_authored"]["status"])

    def test_valid_v1_design_receipt_is_historical_and_cannot_open_new_pass(self):
        family = json.loads((
            INVOKE
            / "development/whole-invoke-repair-plan/design-process/fixtures/schema-family/positive-family.json"
        ).read_text(encoding="utf-8"))
        request = self.base("design")
        receipt = self.artifact("design")
        receipt["producer_receipt"] = family["design_result"]
        request["artifact_receipt"] = receipt
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(any("historical/read-only" in item for item in result["artifact_authored"]["diagnostics"]))

    def test_design_v2_receipt_is_historical_and_cannot_open_new_pass(self):
        request = self.base("design")
        receipt = self.artifact("design")
        receipt["producer_receipt"] = {
            "schema_version": "invoke.design-stage-receipt.v2"
        }
        request["artifact_receipt"] = receipt
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(
            any(
                "historical/read-only" in item
                for item in result["artifact_authored"]["diagnostics"]
            )
        )

    def test_define_fake_producer_and_digest_drift_block(self):
        for mutation in ("producer", "digest"):
            with self.subTest(mutation=mutation):
                request = self.base("define")
                receipt = self.artifact("define")
                if mutation == "producer":
                    receipt["producer_receipt"]["producer"]["sha256"] = "0" * 64
                else:
                    receipt["producer_receipt"]["receipt_digest"] = "0" * 64
                request["artifact_receipt"] = receipt
                self.assertEqual("block", self.resolve(request)["artifact_authored"]["status"])

    def test_valid_v1_define_producer_is_historical_and_cannot_open_new_pass(self):
        request = self.base("define")
        receipt = self.artifact("define")
        receipt["producer_receipt"] = self.define_v1_producer_receipt()
        request["artifact_receipt"] = receipt

        result = self.resolve(request)

        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(
            any(
                "historical/read-only" in diagnostic
                for diagnostic in result["artifact_authored"]["diagnostics"]
            )
        )

    def test_valid_v2_define_producer_is_historical_and_cannot_open_new_pass(self):
        request = self.base("define")
        receipt = self.artifact("define")
        receipt["producer_receipt"] = self.define_v2_producer_receipt()
        receipt["producer_admission_receipt"] = self.define_admission_receipt(
            receipt["producer_receipt"]
        )
        request["artifact_receipt"] = receipt

        result = self.resolve(request)

        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(
            any(
                "historical/read-only" in diagnostic
                for diagnostic in result["artifact_authored"]["diagnostics"]
            )
        )

    def test_missing_stale_forged_mismatched_or_noncurrent_admission_blocks(self):
        for mutation in (
            "missing",
            "validator",
            "digest",
            "binding",
            "stage_ref",
            "bundle_digest",
            "structural_binding",
            "check_status",
            "check_inventory",
            "overall",
        ):
            with self.subTest(mutation=mutation):
                request = self.base("define")
                artifact = self.artifact("define")
                admission = artifact["producer_admission_receipt"]
                if mutation == "missing":
                    artifact.pop("producer_admission_receipt")
                elif mutation == "validator":
                    admission["validator"]["sha256"] = "0" * 64
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "digest":
                    admission["receipt_digest"] = "0" * 64
                elif mutation == "binding":
                    admission["producer_binding"]["receipt_digest"] = "f" * 64
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "stage_ref":
                    admission["stage_receipt_ref"]["sha256"] = "f" * 64
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "bundle_digest":
                    admission["bundle_digest"] = "f" * 64
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "structural_binding":
                    admission["structural_schema_refs"] = [
                        {
                            "definition_id": "FIX-D1",
                            "path": "fixture/FIX-D1.schema.json",
                            "sha256": "f" * 64,
                            "size": 1,
                        }
                    ]
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "check_status":
                    admission["checks"][0]["status"] = "block"
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                elif mutation == "check_inventory":
                    admission["checks"] = admission["checks"][:-1]
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                else:
                    admission["result"] = "block"
                    admission["drift_analysis"]["compile_window"] = "changed"
                    admission["drift_analysis"]["summary"]["projection_state"] = "changed"
                    admission["drift_analysis"]["summary"]["overall"] = "recompile_required"
                    admission["blockers"] = [
                        {
                            "code": "FIXTURE_BLOCK",
                            "message": "not current",
                            "caused_by": ["check:clean-replay"],
                        }
                    ]
                    admission["receipt_digest"] = MODULE.canonical_digest(admission, "receipt_digest")
                request["artifact_receipt"] = artifact
                self.assertEqual("block", self.resolve(request)["artifact_authored"]["status"])

    def test_all_active_modes_open_all_axes_only_from_matching_receipts(self):
        for mode in ("define", "design", "plan", "handoff", "refresh"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request.update({
                    "artifact_receipt": self.artifact(mode),
                    "registry_receipt": self.registry(mode),
                    "material_package_receipt": self.material(),
                    "runtime_receipt": self.runtime(mode),
                })
                result = self.resolve(request)
                self.assertEqual("pass", result["artifact_authored"]["status"])
                self.assertTrue(result["registry_released"]["status"])
                self.assertTrue(result["mutation_runtime_ready"]["status"])

    def test_deferred_modes_remain_unsupported_with_all_receipts(self):
        for mode in ("full", "validate"):
            with self.subTest(mode=mode):
                request = self.base(mode)
                request.update({
                    "artifact_receipt": self.artifact(mode),
                    "registry_receipt": self.registry(mode),
                    "material_package_receipt": self.material(),
                    "runtime_receipt": {
                        "receipt_id": f"runtime-{mode}",
                        "axis": "mutation_runtime_ready",
                        "mode": mode,
                        "status": "ready",
                        "capability_sha256": self.capability_sha,
                        "material_package_id": "package-1",
                        "material_package_digest": "a" * 64,
                        "gates": [{"gate": "fabricated", "status": "pass", "evidence": "x"}],
                    },
                })
                result = self.resolve(request)
                self.assertEqual("unsupported", result["artifact_authored"]["status"])
                self.assertFalse(result["registry_released"]["status"])
                self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_registry_receipt_opens_only_registry_axis(self):
        request = self.base("plan")
        request["registry_receipt"] = self.registry("plan")
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertTrue(result["registry_released"]["status"])
        self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_runtime_receipts_open_only_runtime_axis(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime("plan"),
        })
        result = self.resolve(request)
        self.assertEqual("block", result["artifact_authored"]["status"])
        self.assertFalse(result["registry_released"]["status"])
        self.assertTrue(result["mutation_runtime_ready"]["status"])

    def test_artifact_flag_does_not_open_later_axes(self):
        request = self.base("plan")
        request["artifact_receipt"] = self.artifact("plan", "flag")
        result = self.resolve(request)
        self.assertEqual("flag", result["artifact_authored"]["status"])
        self.assertFalse(result["registry_released"]["status"])
        self.assertFalse(result["mutation_runtime_ready"]["status"])

    def test_stale_registry_digest_does_not_release(self):
        request = self.base("plan")
        request["registry_receipt"] = self.registry("plan", "b" * 64)
        self.assertFalse(self.resolve(request)["registry_released"]["status"])

    def test_stale_runtime_digest_does_not_open_runtime(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime("plan", "b" * 64),
        })
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_missing_mode_gate_does_not_open_runtime(self):
        request = self.base("plan")
        request.update({
            "material_package_receipt": self.material(),
            "runtime_receipt": self.runtime(
                "plan",
                gates=[{
                    "gate": "material_package",
                    "status": "pass",
                    "evidence": "material.json",
                }],
            ),
        })
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_material_receipt_alone_does_not_open_runtime(self):
        request = self.base("plan")
        request["material_package_receipt"] = self.material()
        self.assertFalse(self.resolve(request)["mutation_runtime_ready"]["status"])

    def test_cross_mode_receipt_does_not_open_artifact_axis(self):
        request = self.base("plan")
        request["artifact_receipt"] = self.artifact("design")
        self.assertEqual("block", self.resolve(request)["artifact_authored"]["status"])

    def test_legacy_collapsed_status_request_fails_explicitly(self):
        request = self.base("plan")
        request["status"] = "ready"
        with self.assertRaisesRegex(
            MODULE.CapabilityStatusError, "Additional properties are not allowed"
        ):
            self.resolve(request)

    def test_result_has_no_collapsed_capability_field(self):
        request = self.base("plan")
        result = self.resolve(request)
        self.assertEqual(
            {
                "schema_version",
                "mode",
                "capability_sha256",
                "artifact_authored",
                "registry_released",
                "mutation_runtime_ready",
            },
            set(result),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Focused structural validation for the twenty-two-schema Invoke Design family.

This test proves structural contracts only. It intentionally does not claim
digest freshness, semantic coherence, producer determinism, atomic publication,
consumer admission, or mirror parity.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


INVOKE_DIR = Path(__file__).resolve().parents[1]
SCHEMA_DIR = INVOKE_DIR / "schemas"
PROCESS_DIR = (
    INVOKE_DIR
    / "development"
    / "whole-invoke-repair-plan"
    / "design-process"
)
FIXTURE_PATH = PROCESS_DIR / "fixtures" / "schema-family" / "positive-family.json"
W2_FIXTURE_PATH = PROCESS_DIR / "fixtures" / "schema-family" / "w2-positive-family.json"

SCHEMA_FILES = {
    "production_process": "design-production-process-v1.schema.json",
    "input_boundary_approval": "design-input-boundary-approval-v1.schema.json",
    "input_closure": "design-input-closure-v1.schema.json",
    "input_closure_receipt": "design-input-closure-receipt-v1.schema.json",
    "input_production_receipt": "design-input-production-receipt-v1.schema.json",
    "profile": "design-profile-v1.schema.json",
    "source": "design-source-v1.schema.json",
    "artifact": "design-artifact-v1.schema.json",
    "coherence_policy": "design-coherence-policy-v1.schema.json",
    "coherence_receipt": "design-coherence-receipt-v1.schema.json",
    "candidate_receipt": "design-candidate-production-receipt-v1.schema.json",
    "result": "design-result-v1.schema.json",
    "bundle_closure": "design-bundle-closure-v1.schema.json",
    "bundle_attempt_receipt": "design-bundle-attempt-receipt-v1.schema.json",
    "result_v2": "design-result-v2.schema.json",
    "bundle_admission_receipt": "design-bundle-admission-receipt-v1.schema.json",
    "glossary_report": "design-glossary-consistency-report-v1.schema.json",
    "planned_witness_contracts": "design-planned-witness-contracts-v1.schema.json",
    "template_selection_receipt": "design-template-selection-receipt-v1.schema.json",
    "dispatch_trace": "design-dispatch-trace-v1.schema.json",
    "transport_report": "design-transport-report-v1.schema.json",
    "validation_matrix": "design-validation-matrix-v1.schema.json",
}

FIXTURE_KEYS = {
    "source": "design_source",
    "artifact": "design_artifact",
    "coherence_receipt": "design_coherence_receipt",
    "candidate_receipt": "design_candidate_receipt",
    "result": "design_result",
    "validation_matrix": "design_validation_matrix",
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROJECTOR = load_module("schema_family_projector", INVOKE_DIR / "scripts/project_design_artifact.py")


def fake_ref(path: str) -> dict:
    return {"path": path, "sha256": "a" * 64, "size": 1}


def current_w2_family(policy: dict) -> dict:
    evidence = fake_ref("fixtures/evidence.json")
    pairs = [{"subject_kind": "selection-concern", "subject_id": "concern:test"}, {"subject_kind": "selected-output", "subject_id": "architecture"}, {"subject_kind": "design-kind", "subject_id": "design-kind:greenfield"}]
    source = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-source/v1", "schema_version": "invoke.design-source.v1", "source_id": "design-source:test", "target_id": "target:test", "activation_kind": "normal",
        "profile_binding": {"profile_id": "invoke.generic-design-baseline.v1", "profile_ref": evidence},
        "upstream_bindings": {"design_input_production_receipt_ref": evidence, "design_input_closure_ref": evidence, "design_input_closure_receipt_ref": evidence, "scope_manifest_ref": evidence, "denominator_receipt_ref": evidence, "selection_result_ref": evidence},
        "design_kind": {"kind": "greenfield", "determination_ref": evidence},
        "applications": [{"subject_kind": item["subject_kind"], "subject_id": item["subject_id"], "disposition": "satisfied", "fact_ids": ["system:test"], "evidence_refs": [], "decision_ref": None, "rationale": "Structural fixture."} for item in pairs],
        "facts": [{"fact_id": "system:test", "fact_kind": "system", "name": "Test system", "owner": "design-owner", "requirement_refs": pairs, "attributes": {"responsibility": "Exercise the structural schema."}}],
        "views": {
            "context": {"view_id": "view:context", "applicability": "applicable", "fact_ids": ["system:test"], "na_evidence_refs": []},
            "high_level_structure": {"view_id": "view:high-level-structure", "applicability": "applicable", "fact_ids": ["system:test"], "na_evidence_refs": []},
            "low_level_components": {"view_id": "view:low-level-components", "applicability": "not-applicable-with-evidence", "fact_ids": [], "na_evidence_refs": [evidence]},
            "workflow_process": {"view_id": "view:workflow-process", "applicability": "not-applicable-with-evidence", "fact_ids": [], "na_evidence_refs": [evidence]},
            "decision_flow": {"view_id": "view:decision-flow", "applicability": "not-applicable-with-evidence", "fact_ids": [], "na_evidence_refs": [evidence]},
            "dependency_interface": {"view_id": "view:dependency-interface", "applicability": "not-applicable-with-evidence", "fact_ids": [], "na_evidence_refs": [evidence]},
        },
        "selected_outputs": ["architecture"], "selected_companions": [],
        "glossary_application": {"source_glossary_ref": evidence, "mappings": [{"term": "test", "fact_ids": ["system:test"]}], "unmapped_terms": []},
        "planned_witnesses": [], "unresolved_gaps": [], "layering": {"kind": "seed", "decision": "One structural unit.", "minimum_unit": "Source to candidate."},
        "template_selection": {"selected_profile_id": "invoke.generic-design-baseline.v1", "evidence_ref": evidence}, "dispatch_trace": {"techniques": ["structural-test"], "evidence_ref": evidence},
        "distill_contract": {"classification": "required", "validator_owner": "distill", "coherent_unit_candidate": "Structural W2 candidate", "split_pressure_question": "Does the schema remain closed?", "expected_receipt": "DISTILL-RECEIPT.json"},
        "transport_policy": {"append_existing_only": True, "upstream_mutation": False, "targets": []}, "next_route": "design-bundle-production", "authority_effect": "none", "source_digest": "b" * 64,
    }
    selection = {"concerns": [{"concern_id": "concern:test", "primary_class": "validation", "disposition": "required", "signal_ids": ["signal:test"], "selected": True, "output_id": "architecture"}], "selected_outputs": ["architecture"]}
    artifact = PROJECTOR.project_design_artifact(source, evidence, evidence, evidence, evidence, selection)
    rules = policy["rule_order"]
    coherence = {"$schema": "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1", "schema_version": "invoke.design-coherence-receipt.v1", "receipt_id": "coherence:test", "validator": {"identity": "invoke.validate-design-coherence.v1", "owner": "invoke-design-coherence-validator", "path": "arcanum/spells/invoke/scripts/validate_design_coherence.py", "sha256": "a" * 64}, "bindings": {"process_ref": evidence, "profile_ref": evidence, "coherence_policy_ref": evidence, "design_input_production_receipt_ref": evidence, "design_input_closure_ref": evidence, "design_input_closure_receipt_ref": evidence, "scope_manifest_ref": evidence, "denominator_receipt_ref": evidence, "selection_result_ref": evidence, "design_source_ref": evidence, "design_artifact_ref": evidence}, "policy_rule_ids": rules, "policy_rule_set_digest": policy["rule_set_digest"], "evaluated_rules": [{"rule_id": item, "status": "pass", "evidence_refs": [evidence], "causal_blocker_ids": []} for item in rules], "verdict": "pass", "diagnostics": [], "selection_evidence_state": "design-validator-pass", "coherence_state": "pass", "design_stage_state": "pending-bundle-closure", "plan_evidence_state": "plan-evidence-pending", "authority_effect": "none", "receipt_digest": "a" * 64}
    candidate = {"$schema": "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1", "schema_version": "invoke.design-candidate-production-receipt.v1", "receipt_id": "candidate:test", "producer": {"identity": "invoke.compile-design-candidate.v1", "owner": "invoke-design-candidate-producer", "path": "arcanum/spells/invoke/scripts/compile_design_candidate.py", "sha256": "a" * 64}, "bindings": {"process": evidence, "profile": evidence, "policy": evidence}, "source_ref": evidence, "w1_production_receipt_ref": evidence, "coherence_block_receipt": None, "stage_results": [{"stage_id": item, "status": "pass", "causal_blocker_ids": []} for item in ["source-validation", "artifact-projection", "coherence-validation", "candidate-output-closure"]], "outputs": [{"kind": "design-artifact", "path": "DESIGN.json", "sha256": "a" * 64, "size": 1}, {"kind": "coherence-receipt", "path": "DESIGN-COHERENCE-RECEIPT.json", "sha256": "a" * 64, "size": 1}], "result": "pass", "next_route": "design-bundle-production", "blockers": [], "evidence_ceiling": {"normal_w1_bound": True, "source_complete": True, "candidate_projected": True, "coherence_validated": True, "human_views_produced": False, "design_stage_pass": False, "plan_evidence": False, "acceptance": False, "execution": False, "publication": False, "deployment": False, "external_effect": False}, "authority_effect": "none", "receipt_digest": "a" * 64}
    return {"design_source": source, "design_artifact": artifact, "design_coherence_receipt": coherence, "design_candidate_receipt": candidate}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def declared_digest(document: dict, field: str) -> str:
    digest_input = copy.deepcopy(document)
    digest_input.pop(field)
    encoded = json.dumps(
        digest_input,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class DesignSchemaFamilyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            key: load_json(SCHEMA_DIR / filename)
            for key, filename in SCHEMA_FILES.items()
        }
        cls.schema_store = {
            schema["$id"]: schema for schema in cls.schemas.values()
        }
        cls.family = load_json(FIXTURE_PATH)
        cls.family.update(load_json(W2_FIXTURE_PATH))

    def validator(self, key: str) -> Draft202012Validator:
        schema = self.schemas[key]
        resolver = RefResolver.from_schema(schema, store=self.schema_store)
        return Draft202012Validator(schema, resolver=resolver)

    def assert_valid(self, schema_key: str, document: dict) -> None:
        errors = sorted(
            self.validator(schema_key).iter_errors(document),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def assert_invalid(self, schema_key: str, document: dict) -> None:
        errors = list(self.validator(schema_key).iter_errors(document))
        self.assertTrue(errors, f"{schema_key} unexpectedly accepted the mutation")

    def fixture(self, schema_key: str) -> dict:
        return copy.deepcopy(self.family[FIXTURE_KEYS[schema_key]])

    def test_exact_twenty_two_schema_family_meta_validates(self) -> None:
        self.assertEqual(22, len(self.schemas))
        for schema in self.schemas.values():
            Draft202012Validator.check_schema(schema)

    def test_canonical_static_contracts_validate_and_match_self_digests(self) -> None:
        process = load_json(PROCESS_DIR / "DESIGN-PRODUCTION-PROCESS.json")
        profile = load_json(PROCESS_DIR / "DESIGN-PROFILE.json")
        policy = load_json(PROCESS_DIR / "DESIGN-COHERENCE-POLICY.json")

        self.assert_valid("production_process", process)
        self.assert_valid("profile", profile)
        self.assert_valid("coherence_policy", policy)
        self.assertEqual(process["process_digest"], declared_digest(process, "process_digest"))
        self.assertEqual(profile["profile_digest"], declared_digest(profile, "profile_digest"))
        self.assertEqual(policy["policy_digest"], declared_digest(policy, "policy_digest"))

    def test_complete_positive_fixture_family_validates(self) -> None:
        self.assertEqual(
            {"design_source", "design_artifact", "design_coherence_receipt", "design_candidate_receipt", "design_validation_matrix"},
            set(load_json(W2_FIXTURE_PATH)),
        )
        for schema_key in FIXTURE_KEYS:
            self.assert_valid(schema_key, self.fixture(schema_key))
        matrix = self.fixture("validation_matrix")
        self.assertEqual(
            matrix["matrix_digest"], declared_digest(matrix, "matrix_digest")
        )

    def test_w2_contract_links_public_authoring_guide_and_executable_example(self) -> None:
        design_contract = (INVOKE_DIR / "design.md").read_text(encoding="utf-8")
        guide = (INVOKE_DIR / "design-source-authoring-guide.md").read_text(encoding="utf-8")
        example = (INVOKE_DIR / "examples" / "design-source-v1" / "README.md").read_text(encoding="utf-8")
        self.assertIn("[design-source-authoring-guide.md](design-source-authoring-guide.md)", design_contract)
        self.assertIn("invoke.generic-design-baseline.v1", guide)
        self.assertIn("tools/arcanum invoke design author source", guide)
        self.assertIn("tools/arcanum invoke design produce candidate", guide)
        self.assertIn("[historical Design source example](examples/design-source-v1/README.md)", guide)
        self.assertIn("test_compile_design_candidate.py", example)
        self.assertIn("real Define v2", example)

    def test_w3_contract_links_bundle_guide_and_executable_example(self) -> None:
        design_contract = (INVOKE_DIR / "design.md").read_text(encoding="utf-8")
        guide = (INVOKE_DIR / "design-bundle-authoring-guide.md").read_text(encoding="utf-8")
        example = (INVOKE_DIR / "examples" / "design-bundle-v1" / "README.md").read_text(encoding="utf-8")
        self.assertIn("[design-bundle-authoring-guide.md](design-bundle-authoring-guide.md)", design_contract)
        self.assertIn("tools/arcanum invoke design produce final-bundle", guide)
        self.assertIn("tools/arcanum invoke design admit admission", guide)
        self.assertIn("[executable W3 example](examples/design-bundle-v1/README.md)", guide)
        self.assertIn("test_compile_design_source_v2.py", example)
        self.assertIn("real Define v2", example)

    def test_source_requires_all_six_view_projections(self) -> None:
        document = self.fixture("source")
        del document["views"]["dependency_interface"]
        self.assert_invalid("source", document)

    def test_changed_input_requires_exact_decision_ref(self) -> None:
        document = self.fixture("source")
        application = document["applications"][0]
        application["disposition"] = "changed-by-exact-decision"
        application["decision_ref"] = None
        self.assert_invalid("source", document)

    def test_source_cannot_self_assert_distill_verdict(self) -> None:
        document = self.fixture("source")
        document["distill_contract"]["verdict"] = "pass"
        self.assert_invalid("source", document)

    def test_artifact_cannot_bind_later_coherence_receipt(self) -> None:
        document = self.fixture("artifact")
        document["evidence_bindings"]["coherence_receipt_ref"] = {
            "path": "fixtures/DESIGN-COHERENCE-RECEIPT.json",
            "sha256": "a" * 64,
            "size": 1,
        }
        self.assert_invalid("artifact", document)

    def test_artifact_cannot_claim_later_authority(self) -> None:
        document = self.fixture("artifact")
        document["authority_effect"] = "registry-release"
        self.assert_invalid("artifact", document)

    def test_coherence_pass_rejects_nonpassing_rule(self) -> None:
        document = self.fixture("coherence_receipt")
        document["evaluated_rules"][0]["status"] = "block"
        document["evaluated_rules"][0]["causal_blocker_ids"] = ["blocker:rule"]
        self.assert_invalid("coherence_receipt", document)

    def test_coherence_pass_rejects_diagnostics(self) -> None:
        document = self.fixture("coherence_receipt")
        document["diagnostics"] = [
            {
                "diagnostic_id": "diagnostic:conflict",
                "code": "DESIGN_CONFLICT",
                "message": "The staged artifact conflicts with an input.",
                "selector": "$.model",
                "owner": "design-owner",
                "repair": "Repair the source and restage it.",
                "causal_blocker_ids": ["blocker:conflict"],
            }
        ]
        self.assert_invalid("coherence_receipt", document)

    def test_stage_receipt_requires_complete_ordered_output_inventory(self) -> None:
        document = self.fixture("result")
        document["outputs"].pop()
        self.assert_invalid("result", document)

    def test_discovery_activation_cannot_receive_normal_stage_pass(self) -> None:
        document = self.fixture("result")
        document["activation_kind"] = "discovery"
        self.assert_invalid("result", document)

    def test_stage_receipt_cannot_claim_plan_evidence(self) -> None:
        document = self.fixture("result")
        document["evidence_ceiling"]["plan_evidence"] = True
        self.assert_invalid("result", document)

    def test_negative_matrix_case_requires_no_publication_assertion(self) -> None:
        document = self.fixture("validation_matrix")
        del document["cases"][1]["no_publication_on_failure"]
        self.assert_invalid("validation_matrix", document)

    def test_validation_matrix_cannot_claim_executed_evidence(self) -> None:
        document = self.fixture("validation_matrix")
        document["execution_state"] = "pass"
        self.assert_invalid("validation_matrix", document)


if __name__ == "__main__":
    unittest.main(verbosity=2)

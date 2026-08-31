#!/usr/bin/env python3
"""Executable W3 tests for independent Define v3 bundle admission."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


DEVELOPMENT_DIR = Path(__file__).resolve().parent
INVOKE_DIR = DEVELOPMENT_DIR.parent
if str(DEVELOPMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEVELOPMENT_DIR))

from define_v3_test_fixture import (  # noqa: E402
    DefineV3RepositoryFixture,
    canonical_bytes,
    write_json,
)


VALIDATOR = INVOKE_DIR / "scripts" / "validate_define_bundle_admission.py"
ADMISSION_SCHEMA = INVOKE_DIR / "schemas" / "define-bundle-admission-receipt-v1.schema.json"
SPEC = importlib.util.spec_from_file_location("validate_define_bundle_admission", VALIDATOR)
assert SPEC is not None and SPEC.loader is not None
ADMISSION_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADMISSION_MODULE)


class AdmissionFixture(DefineV3RepositoryFixture):
    def __init__(self, root: Path, mode: str = "mixed") -> None:
        super().__init__(root, mode)
        (self.schema_dir / ADMISSION_SCHEMA.name).write_bytes(ADMISSION_SCHEMA.read_bytes())
        self.admission_validator = self.script_dir / VALIDATOR.name
        self.admission_validator.write_bytes(VALIDATOR.read_bytes())
        self.admission_count = 0

    def admit(self, prior: Path | None = None) -> tuple[subprocess.CompletedProcess[str], Path]:
        self.admission_count += 1
        output = self.root / f"admission-{self.admission_count}.json"
        command = [
            sys.executable,
            str(self.admission_validator),
            "--repo-root",
            str(self.root),
            "--bundle-root",
            str(self.output_dir),
            "--schema-dir",
            str(self.schema_dir),
            "--output",
            str(output),
        ]
        if prior is not None:
            command.extend(["--prior-admission", str(prior)])
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result, output


class ValidateDefineBundleAdmissionTest(unittest.TestCase):
    def fixture(self, mode: str = "mixed") -> tuple[tempfile.TemporaryDirectory[str], AdmissionFixture]:
        temporary = tempfile.TemporaryDirectory()
        return temporary, AdmissionFixture(Path(temporary.name), mode)

    @staticmethod
    def read(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def compile(self, fixture: AdmissionFixture) -> None:
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)

    def assert_block(
        self,
        fixture: AdmissionFixture,
        *,
        overall: str | None = None,
        category: str | None = None,
        prior: Path | None = None,
    ) -> dict[str, Any]:
        result, output = fixture.admit(prior)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertTrue(output.is_file())
        receipt = self.read(output)
        self.assertEqual("block", receipt["result"])
        self.assertGreater(len(receipt["blockers"]), 0)
        if overall is not None:
            self.assertEqual(overall, receipt["drift_analysis"]["summary"]["overall"])
        if category is not None:
            self.assertIn(category, {item["category"] for item in receipt["drift_analysis"]["differences"]})
        return receipt

    def test_candidate_reference_and_mixed_bundles_pass_initial_admission(self) -> None:
        for mode, outcome in (
            ("candidate-only", "candidate-definitions"),
            ("reference-only", "reference-only"),
            ("mixed", "mixed"),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = AdmissionFixture(Path(directory), mode)
                self.compile(fixture)
                result, output = fixture.admit()
                self.assertEqual(0, result.returncode, result.stderr)
                receipt = self.read(output)
                stage = self.read(fixture.output_dir / "INVOKE-DEFINE-STAGE-RECEIPT.json")
                self.assertEqual("pass", receipt["result"])
                self.assertEqual("current", receipt["drift_analysis"]["summary"]["overall"])
                self.assertEqual("not_provided", receipt["drift_analysis"]["prior_admission"])
                self.assertEqual(13, len(receipt["output_inventory"]))
                self.assertEqual(
                    ADMISSION_MODULE.inventory_digest(receipt["output_inventory"]),
                    receipt["bundle_digest"],
                )
                self.assertEqual(
                    list(ADMISSION_MODULE.CHECK_IDS),
                    [check["check_id"] for check in receipt["checks"]],
                )
                self.assertTrue(all(check["status"] == "pass" for check in receipt["checks"]))
                self.assertEqual(stage["receipt_id"], receipt["producer_binding"]["receipt_id"])
                self.assertEqual(outcome, stage["semantic_outcome"])

    def test_v2_admission_exposes_complete_obligation_chain(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_define_to_v2()
        fixture.add_v2_relationship_obligation()
        self.compile(fixture)
        result, output = fixture.admit()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.read(output)
        self.assertEqual("invoke.define-bundle-admission-receipt.v2", receipt["schema_version"])
        self.assertEqual("invoke.validate-define-bundle-admission.v2", receipt["validator"]["identity"])
        self.assertEqual(list(ADMISSION_MODULE.V2_CHECK_IDS), [item["check_id"] for item in receipt["checks"]])
        coverage = receipt["intent_coverage"]
        self.assertEqual(4, coverage["obligation_count"])
        self.assertEqual(4, coverage["materialized_count"])
        self.assertEqual([], coverage["missing_obligation_ids"])
        relationship = next(
            item for item in coverage["chain"] if item["kind"] == "relationship"
        )
        self.assertEqual("materialized", relationship["status"])
        self.assertEqual(["FIX-D1", "FIX-D2"], relationship["definition_ids"])

    def test_v2_admission_blocks_relation_removed_after_closure(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_define_to_v2()
        fixture.add_v2_relationship_obligation()
        self.compile(fixture)
        definitions = fixture.output_dir / "DEFINITIONS.json"
        artifact = self.read(definitions)
        specialized = next(item for item in artifact["definitions"] if item["id"] == "FIX-D2")
        specialized["relations"] = []
        definitions.write_bytes(canonical_bytes(artifact))
        receipt = self.assert_block(fixture)
        check = next(
            item
            for item in receipt["checks"]
            if item["check_id"] == "check:intent-obligation-materialization"
        )
        self.assertEqual("block", check["status"])
        self.assertEqual(
            ["obligation:feature-contract-depends-on-semantic-closure"],
            receipt["intent_coverage"]["missing_obligation_ids"],
        )

    def test_unchanged_prior_admission_replay_passes_without_semantic_inference(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        first_result, first = fixture.admit()
        self.assertEqual(0, first_result.returncode, first_result.stderr)
        second_result, second = fixture.admit(first)
        self.assertEqual(0, second_result.returncode, second_result.stderr)
        receipt = self.read(second)
        self.assertEqual("current", receipt["drift_analysis"]["prior_admission"])
        self.assertEqual([], receipt["drift_analysis"]["differences"])

    def test_deterministic_view_drift_requires_recompile_not_semantic_reassessment(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        view = fixture.output_dir / "DEFINITIONS.md"
        view.write_bytes(view.read_bytes() + b"\nlate projection drift\n")
        receipt = self.assert_block(fixture, overall="recompile_required", category="generated_projection")
        self.assertEqual("unchanged", receipt["drift_analysis"]["summary"]["semantic_state"])

    def test_missing_view_changes_only_projection_axis_and_requires_recompile(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        (fixture.output_dir / "DEFINITIONS.md").unlink()
        receipt = self.assert_block(fixture, overall="recompile_required", category="bundle_inventory")
        self.assertEqual(
            {
                "evidence_state": "current",
                "semantic_state": "unchanged",
                "authority_state": "unchanged",
                "topology_state": "unchanged",
                "projection_state": "changed",
                "overall": "recompile_required",
            },
            receipt["drift_analysis"]["summary"],
        )

    def test_meaning_change_is_semantic_drift_even_when_counts_and_paths_stay_stable(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        definitions = fixture.output_dir / "DEFINITIONS.json"
        artifact = self.read(definitions)
        artifact["definitions"][0]["voices"]["normative"] += " Changed meaning."
        definitions.write_bytes(canonical_bytes(artifact))
        receipt = self.assert_block(
            fixture, overall="semantic_reassessment_required", category="definition_meaning"
        )
        self.assertEqual("changed", receipt["drift_analysis"]["summary"]["semantic_state"])

    def test_meaning_authority_and_consumer_fields_are_classified_from_real_bundle_drift(self) -> None:
        cases = {
            "label_alias": lambda artifact: artifact["definitions"][0]["aliases"].append("late alias"),
            "boundary": lambda artifact: artifact["definitions"][0]["boundary"]["includes"].append("late boundary"),
            "relation": lambda artifact: artifact["definitions"][1]["relations"][0].update({"type": "references"}),
            "authority": lambda artifact: artifact["authority_bindings"][0]["authority_scope"].update({"ref": "late-scope"}),
            "consumer_topology": lambda artifact: artifact["definitions"][0]["primary_consumers"].append("late-consumer"),
            "selector": lambda artifact: artifact["definitions"][0]["source_refs"][0].update({"selector": "late-selector"}),
        }
        for category, mutate in cases.items():
            with self.subTest(category=category), tempfile.TemporaryDirectory() as directory:
                fixture = AdmissionFixture(Path(directory))
                self.compile(fixture)
                definitions = fixture.output_dir / "DEFINITIONS.json"
                artifact = self.read(definitions)
                mutate(artifact)
                definitions.write_bytes(canonical_bytes(artifact))
                receipt = self.assert_block(
                    fixture,
                    overall="semantic_reassessment_required",
                    category=category,
                )
                if category == "authority":
                    self.assertEqual("changed", receipt["drift_analysis"]["summary"]["authority_state"])
                elif category == "consumer_topology":
                    self.assertEqual("changed", receipt["drift_analysis"]["summary"]["topology_state"])

    def test_root_authority_and_semantic_evidence_fields_use_contract_categories(self) -> None:
        cases = (
            (
                "authority-kind",
                "authority",
                lambda artifact: artifact.update({"authority_kind": "kind.changed"}),
            ),
            (
                "authority-effect",
                "authority",
                lambda artifact: artifact.update({"authority_effect": "changed"}),
            ),
            (
                "semantic-evidence",
                "source_evidence",
                lambda artifact: artifact["semantic_evidence"]["context_ref"].update(
                    {"sha256": "f" * 64}
                ),
            ),
        )
        for name, category, mutate in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                fixture = AdmissionFixture(Path(directory))
                self.compile(fixture)
                definitions = fixture.output_dir / "DEFINITIONS.json"
                artifact = self.read(definitions)
                mutate(artifact)
                definitions.write_bytes(canonical_bytes(artifact))
                receipt = self.assert_block(
                    fixture,
                    overall="semantic_reassessment_required",
                    category=category,
                )
                if category == "authority":
                    self.assertEqual(
                        "changed",
                        receipt["drift_analysis"]["summary"]["authority_state"],
                    )
                else:
                    self.assertEqual(
                        "stale",
                        receipt["drift_analysis"]["summary"]["evidence_state"],
                    )

    def test_identity_denominator_drift_routes_back_to_identity_validator(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        identity = fixture.output_dir / "IDENTITY-DENOMINATOR-RECEIPT.json"
        document = self.read(identity)
        document["rationale"] = "Late identity-denominator change."
        identity.write_bytes(canonical_bytes(document))
        receipt = self.assert_block(
            fixture, overall="semantic_reassessment_required", category="identity_denominator"
        )
        difference = next(item for item in receipt["drift_analysis"]["differences"] if item["category"] == "identity_denominator")
        self.assertEqual("identity_denominator", difference["repair_route"])

    def test_stale_source_bytes_require_semantic_review(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        discovery = fixture.root / "public/discovery.md"
        discovery.write_bytes(discovery.read_bytes() + b"\nMeaning-bearing late evidence.\n")
        receipt = self.assert_block(
            fixture, overall="semantic_reassessment_required", category="source_evidence"
        )
        self.assertEqual("review_required", receipt["drift_analysis"]["summary"]["semantic_state"])

    def test_selector_change_is_reported_separately_from_generic_source_drift(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        fixture.context["concept_probes"][0]["evidence_refs"][0]["selector"] = "Feature Contract"
        fixture.write_context()
        self.assert_block(fixture, overall="semantic_reassessment_required", category="selector")

    def test_registry_and_consumer_membership_changes_are_topology_drift(self) -> None:
        for path, category, content in (
            ("public/late/DEFINITIONS.json", "registry_topology", b'{"definitions":[]}\n'),
            ("public/consumer/HIDDEN.md", "consumer_topology", b"# Hidden\n\nUses contract.\n"),
        ):
            with self.subTest(category=category), tempfile.TemporaryDirectory() as directory:
                fixture = AdmissionFixture(Path(directory))
                self.compile(fixture)
                target = fixture.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                receipt = self.assert_block(
                    fixture, overall="semantic_reassessment_required", category=category
                )
                self.assertEqual("changed", receipt["drift_analysis"]["summary"]["topology_state"])

    def test_registry_and_consumer_removals_are_topology_drift(self) -> None:
        for relative, category in (
            ("public/adjacent/DEFINITIONS.json", "registry_topology"),
            ("public/consumer/SPEC.md", "consumer_topology"),
        ):
            with self.subTest(category=category), tempfile.TemporaryDirectory() as directory:
                fixture = AdmissionFixture(Path(directory))
                self.compile(fixture)
                (fixture.root / relative).unlink()
                receipt = self.assert_block(
                    fixture,
                    overall="semantic_reassessment_required",
                    category=category,
                )
                self.assertEqual("changed", receipt["drift_analysis"]["summary"]["topology_state"])

    def test_changed_valid_structural_schema_requires_prior_semantic_reassessment(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        structural = fixture.root / "public/FIX-D1.schema.json"
        write_json(structural, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"})
        fixture.source["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "FIX-D1-SCHEMA",
            "status": "machine-checkable",
            "ref": "public/FIX-D1.schema.json",
        }
        fixture.write_source()
        self.compile(fixture)
        first_result, first = fixture.admit()
        self.assertEqual(0, first_result.returncode, first_result.stderr)
        write_json(
            structural,
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Changed but valid", "type": "object"},
        )
        receipt = self.assert_block(
            fixture,
            prior=first,
            overall="semantic_reassessment_required",
            category="structural_schema",
        )
        self.assertEqual("review_required", receipt["drift_analysis"]["summary"]["semantic_state"])

    def test_changed_valid_structural_schema_blocks_initial_admission(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        structural = fixture.root / "public/FIX-D1.schema.json"
        write_json(structural, {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"})
        fixture.source["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "FIX-D1-SCHEMA",
            "status": "machine-checkable",
            "ref": "public/FIX-D1.schema.json",
        }
        fixture.write_source()
        self.compile(fixture)
        write_json(
            structural,
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "array"},
        )
        receipt = self.assert_block(
            fixture,
            overall="semantic_reassessment_required",
            category="structural_schema",
        )
        self.assertEqual("review_required", receipt["drift_analysis"]["summary"]["semantic_state"])

    def test_multiple_defects_are_collected_in_one_block_receipt(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        definitions = fixture.output_dir / "DEFINITIONS.json"
        artifact = self.read(definitions)
        artifact["definitions"][0]["aliases"].append("late alias")
        definitions.write_bytes(canonical_bytes(artifact))
        view = fixture.output_dir / "GLOSSARY.md"
        view.write_bytes(view.read_bytes() + b"late view drift\n")
        (fixture.output_dir / "EXTRA.json").write_bytes(b"{}\n")
        receipt = self.assert_block(fixture, overall="semantic_reassessment_required")
        categories = {item["category"] for item in receipt["drift_analysis"]["differences"]}
        self.assertTrue({"label_alias", "generated_projection", "bundle_inventory"}.issubset(categories))
        self.assertGreaterEqual(len(receipt["blockers"]), 3)

    def test_field_classifier_covers_all_meaning_authority_and_topology_axes(self) -> None:
        cases = {
            "/authority_kind": ("authority", "authority_changed"),
            "/authority_effect": ("authority", "authority_changed"),
            "/semantic_evidence/context_ref/sha256": ("source_evidence", "review_required"),
            "/definitions/0/aliases": ("label_alias", "meaning_changed"),
            "/definitions/0/voices/normative": ("definition_meaning", "meaning_changed"),
            "/definitions/0/boundary/inside": ("boundary", "meaning_changed"),
            "/definitions/0/relations": ("relation", "meaning_changed"),
            "/semantic_applications": ("semantic_application", "meaning_changed"),
            "/authority_bindings": ("authority", "authority_changed"),
            "/definitions": ("registry_topology", "topology_changed"),
            "/definitions/0/structural_schema/ref": ("structural_schema", "review_required"),
            "/definitions/0/primary_consumers": ("consumer_topology", "topology_changed"),
            "/definitions/0/source_refs/0/selector": ("selector", "review_required"),
            "/definitions/0/source_refs/0/sha256": ("source_evidence", "review_required"),
            "/definitions/0/definition_version": ("definition_meaning", "review_required"),
        }
        for pointer, expected in cases.items():
            with self.subTest(pointer=pointer):
                category, effect, _route = ADMISSION_MODULE.definition_category(pointer)
                self.assertEqual(expected, (category, effect))

    def test_invalid_prior_basis_blocks_overall_without_collapsing_current_axes(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        first_result, first = fixture.admit()
        self.assertEqual(0, first_result.returncode, first_result.stderr)
        prior = self.read(first)
        prior["receipt_digest"] = "0" * 64
        first.write_bytes(canonical_bytes(prior))
        receipt = self.assert_block(fixture, overall="blocked", prior=first)
        self.assertEqual("not_evaluable", receipt["drift_analysis"]["prior_admission"])
        self.assertEqual(
            {
                "evidence_state": "current",
                "semantic_state": "unchanged",
                "authority_state": "unchanged",
                "topology_state": "unchanged",
                "projection_state": "unchanged",
                "overall": "blocked",
            },
            receipt["drift_analysis"]["summary"],
        )

    def test_symlinked_output_parent_cannot_alias_receipt_into_bundle(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        alias = fixture.root / "bundle-alias"
        alias.symlink_to(fixture.output_dir, target_is_directory=True)
        output = alias / "admission.json"
        result = subprocess.run(
            [
                sys.executable,
                str(fixture.admission_validator),
                "--repo-root",
                str(fixture.root),
                "--bundle-root",
                str(fixture.output_dir),
                "--schema-dir",
                str(fixture.schema_dir),
                "--output",
                str(output),
            ],
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("outside the submitted bundle", result.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(13, len(list(fixture.output_dir.iterdir())))

    def test_invocation_failure_writes_no_receipt_and_returns_two(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.compile(fixture)
        output = fixture.root / "must-remain-absent.json"
        result = subprocess.run(
            [
                sys.executable,
                str(fixture.admission_validator),
                "--repo-root",
                str(fixture.root),
                "--bundle-root",
                str(fixture.root / "missing"),
                "--schema-dir",
                str(fixture.schema_dir),
                "--output",
                str(output),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()

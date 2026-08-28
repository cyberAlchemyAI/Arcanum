#!/usr/bin/env python3
"""Producer-quality W1 tests against real Define v2 and frozen Design consumers."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


INVOKE = Path(__file__).resolve().parents[1]
SCHEMAS = INVOKE / "schemas"
REPOSITORY_ROOT = INVOKE.parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DEFINE = load_module(
    "w1_test_define_compiler", INVOKE / "scripts/compile_define_source_v2.py"
)
W1 = load_module(
    "w1_test_design_input_compiler",
    INVOKE / "scripts/compile_design_input_bundle.py",
)


def canonical_digest(document: object) -> str:
    return hashlib.sha256(
        json.dumps(
            document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def digest_without(document: dict, field: str) -> str:
    return canonical_digest({key: value for key, value in document.items() if key != field})


class DesignInputBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / "arcanum").mkdir()
        self.evidence = self.repo / "arcanum/define-evidence.md"
        self.evidence.write_text(
            "# W1 Target\n\nExact public evidence for the W1 integration fixture.\n",
            encoding="utf-8",
        )
        self.target_id = "w1-design-target"
        self.owner = "design-input-owner"
        self.epoch = "fixture-epoch-001"
        self.define_source = self.repo / "DEFINE-SOURCE.json"
        self.define_output = self.repo / "define-output"
        self.write_json(self.define_source, self.make_define_source())
        self.define_receipt = DEFINE.compile_source(
            self.define_source, self.define_output, self.repo, SCHEMAS
        )
        self.no_prior_path = self.repo / "NO-PRIOR-DESIGN.json"
        no_prior = {
            "schema_version": "invoke.design-no-prior-determination.v1",
            "target_id": self.target_id,
            "observation_epoch": self.epoch,
            "applicable_prior_design_paths": [],
            "determined_by": self.owner,
            "authority_effect": "none",
            "determination_digest": "0" * 64,
        }
        no_prior["determination_digest"] = digest_without(
            no_prior, "determination_digest"
        )
        self.write_json(self.no_prior_path, no_prior)
        self.approval_path = self.repo / "DESIGN-INPUT-BOUNDARY-APPROVAL.json"
        self.closure_path = self.repo / "DESIGN-INPUT-CLOSURE.json"
        self.boundary = self.make_boundary("define-output", "define-artifact", "DEFINITIONS.json")
        self.write_approval(self.approval_path, self.boundary)
        self.closure = self.make_closure(self.boundary, self.approval_path, "normal")
        self.write_closure(self.closure)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def write_json(path: Path, document: dict) -> None:
        path.write_text(
            json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def exact(self, path: Path, label: str | None = None) -> dict:
        data = path.read_bytes()
        return {
            "path": label or path.relative_to(self.repo).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        }

    def file_ref(
        self,
        path: Path,
        visibility: str = "public",
        schema_id: str | None = None,
        schema_version: str | None = None,
        label: str | None = None,
    ) -> dict:
        return {
            **self.exact(path, label),
            "visibility": visibility,
            "expected_schema_id": schema_id,
            "expected_schema_version": schema_version,
        }

    def make_define_source(self) -> dict:
        source_ref = self.exact(self.evidence, "arcanum/define-evidence.md")
        definition_source_ref = {
            "role": "normative",
            "path": source_ref["path"],
            "visibility": "public",
            "selector_type": "heading",
            "selector": "W1 Target",
            "start_line": None,
            "end_line": None,
            "sha256": source_ref["sha256"],
            "size": source_ref["size"],
        }
        return {
            "schema_version": "invoke.define-source.v2",
            "source_id": "W1-DEFINE-FIXTURE-001",
            "target": {
                "id": self.target_id,
                "objective": "Establish exact candidate terms for a real W1 normal activation.",
            },
            "discovery": {"kind": "artifact", "ref": source_ref},
            "template_selection": {
                "profile_id": "invoke.generic-definitions-baseline.v2",
                "selected": "invoke.generic-definitions-baseline.v2",
                "eligible": ["invoke.generic-definitions-baseline.v2"],
                "tie": False,
            },
            "spec_declarations": [
                {
                    "id": "W1-D1",
                    "title": "W1 Candidate Boundary",
                    "statement": "The generated registry remains candidate and authority-free.",
                }
            ],
            "definition_registry": {
                "registry_id": "invoke.w1.fixture",
                "title": "W1 Fixture Candidate Definitions",
                "owner_route": "definitions-governance",
                "authority_scope": {"kind": "project", "ref": self.target_id},
                "visibility": "public",
                "definitions": [
                    {
                        "id": "W1-D001",
                        "term": "approved design input boundary",
                        "aliases": ["design boundary approval"],
                        "status": "candidate",
                        "status_detail": None,
                        "deferred_as": None,
                        "supersedes": [],
                        "superseded_by": None,
                        "source_kinds": ["domain-vocabulary"],
                        "voices": {
                            "normative": "A finite owner-approved discovery surface for Design input closure.",
                            "formal": None,
                            "operational": "Bind roots, rules, classes, exclusions, and one observation epoch.",
                            "plain_language": "The exact area an owner allowed W1 to inspect.",
                            "domain_context": "Used only by this W1 producer fixture.",
                        },
                        "notation": [],
                        "boundary": {
                            "includes": ["Named roots and rules."],
                            "excludes": ["Repository-global completeness."],
                            "conditions": [],
                        },
                        "source_refs": [definition_source_ref],
                        "primary_consumers": ["Design input closure"],
                        "relations": [],
                        "use_carefully": None,
                        "misuse_warning": None,
                        "challenge_contract": None,
                        "promotion_boundary": "Candidate only; no promotion authority is granted.",
                        "drift_route": "definitions-governance",
                        "definition_version": "1",
                        "structural_schema": None,
                    }
                ],
            },
            "layering": {
                "kind": "gap",
                "rationale": "Design and Plan own downstream implementation layering.",
            },
            "dispatch_trace": {
                "techniques": [
                    "sequence",
                    "owner_boundary_check",
                    "concrete_path_evidence",
                ]
            },
            "distill": {
                "classification": "not-required",
                "rationale": "The fixture contains one bounded definition unit.",
            },
            "identity_denominator": {
                "classification": "not-applicable",
                "rationale": "No separate identity denominator is asserted.",
            },
            "output_contracts": {
                "spec": "SPEC.md",
                "definitions": "DEFINITIONS.json",
                "definitions_view": "DEFINITIONS.md",
                "glossary": "GLOSSARY.md",
                "layering": "LAYERING-GAP.md",
                "template_selection": "TEMPLATE-SELECTION-RECEIPT.json",
                "dispatch_trace": "DISPATCH-TRACE.json",
                "distill": "DISTILL-RECEIPT.json",
                "identity_denominator": "IDENTITY-DENOMINATOR-RECEIPT.json",
                "transport": "DEFINE-TRANSPORT-REPORT.json",
                "stage_receipt": "INVOKE-DEFINE-STAGE-RECEIPT.json",
            },
            "transport_policy": {
                "append_existing_only": True,
                "upstream_mutation": False,
                "targets": [],
            },
            "next_route": "design",
        }

    def directory_binding(self, root_id: str, relative: str) -> dict:
        root = self.repo / relative
        records = []
        for child in sorted(root.rglob("*")):
            if child.is_file() and not child.is_symlink():
                data = child.read_bytes()
                records.append(
                    {
                        "relative_path": child.relative_to(root).as_posix(),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "size": len(data),
                    }
                )
        return {
            "root_id": root_id,
            "path": relative,
            "sha256": canonical_digest(records),
            "size": sum(item["size"] for item in records),
        }

    def make_boundary(self, root: str, input_class: str, pattern: str) -> dict:
        material = {
            "observation_epoch": self.epoch,
            "roots": [self.directory_binding("root:inputs", root)],
            "discovery_rules": [
                {
                    "rule_id": "rule:inputs",
                    "root_id": "root:inputs",
                    "input_class": input_class,
                    "include_globs": [pattern],
                }
            ],
            "required_input_classes": [input_class],
            "permitted_exclusions": [],
        }
        return {**material, "boundary_digest": canonical_digest(material)}

    def write_approval(self, path: Path, boundary: dict) -> None:
        approval = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1",
            "schema_version": "invoke.design-input-boundary-approval.v1",
            "approval_id": "approval:w1-input-boundary",
            "target_id": self.target_id,
            "target_visibility": "public",
            "approved_by": self.owner,
            **copy.deepcopy(boundary),
            "authority_effect": "none",
            "approval_digest": "0" * 64,
        }
        approval["approval_digest"] = digest_without(approval, "approval_digest")
        self.write_json(path, approval)

    def manifest_contract_ref(self) -> dict:
        path = INVOKE / "schemas/design-scope-manifest.schema.json"
        return self.file_ref(
            path,
            "public",
            "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0",
            "1.0.0",
            "arcanum/spells/invoke/schemas/design-scope-manifest.schema.json",
        )

    def make_closure(
        self, boundary: dict, approval_path: Path, activation_kind: str
    ) -> dict:
        definitions = self.define_output / "DEFINITIONS.json"
        input_id = "input:define"
        if activation_kind == "normal":
            activation = {
                "kind": "normal",
                "define_stage_receipt_ref": self.file_ref(
                    self.define_output / "INVOKE-DEFINE-STAGE-RECEIPT.json",
                    "public",
                    "https://arcanum.dev/schemas/invoke/define-result-v2",
                    "invoke.define-stage-receipt.v2",
                ),
                "approval_ref": self.file_ref(
                    approval_path,
                    "public",
                    "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1",
                    "invoke.design-input-boundary-approval.v1",
                ),
            }
            input_kind = "define-artifact"
            input_path = definitions
            input_schema = "https://arcanum.dev/schemas/invoke/definitions/v1"
            input_version = "definitions/v1"
        else:
            activation = {
                "kind": "discovery",
                "approval_ref": self.file_ref(
                    approval_path,
                    "public",
                    "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1",
                    "invoke.design-input-boundary-approval.v1",
                ),
                "rationale": "Owner-approved review-only discovery activation.",
            }
            input_id = "input:review"
            input_kind = "other"
            input_path = self.repo / "review-inputs/scope.md"
            input_schema = None
            input_version = None
        selector = f"file:{input_path.relative_to(self.repo).as_posix()}"
        return {
            "$schema": "https://arcanum.dev/schemas/invoke/design-input-closure/v1",
            "schema_version": "invoke.design-input-closure.v1",
            "closure_id": "closure:w1-design-inputs",
            "authored_by": self.owner,
            "target": {
                "id": self.target_id,
                "title": "W1 Design Target",
                "objective": "Close Design inputs inside one owner-approved boundary.",
                "owner": self.owner,
                "visibility": "public",
            },
            "activation": activation,
            "discovery_boundary": copy.deepcopy(boundary),
            "scope_manifest_contract_ref": self.manifest_contract_ref(),
            "input_catalog": [
                {
                    "input_id": input_id,
                    "kind": input_kind,
                    "authority_class": "normative",
                    "authority_owner": self.owner,
                    "applicability_owner": self.owner,
                    "classification": "required",
                    "selector": selector,
                    "source_ref": self.file_ref(
                        input_path, "public", input_schema, input_version
                    ),
                    "freshness": {
                        "status": "current",
                        "observed_epoch": self.epoch,
                    },
                    "applies_to": ["design"],
                    "exclusion_evidence_ref": None,
                }
            ],
            "conditional_input_resolutions": [],
            "constraints": [],
            "invariants": [],
            "prior_decisions": [],
            "exclusions": [],
            "design_kind": {
                "kind": "greenfield",
                "no_prior_design_determination_ref": self.file_ref(
                    self.no_prior_path, "public", None, None
                ),
            },
            "selection_inputs": {
                "authored_concerns": [
                    {
                        "concern_id": "authored:validation",
                        "primary_class": "validation",
                        "disposition": "required",
                        "required_predicate": True,
                        "evidence_selectors": [selector],
                        "ownership": {
                            "accountable_owner": self.owner,
                            "contributing_owners": [self.owner],
                            "artifact_owner": "plan-work-pack-owner",
                            "validator_owner": "invoke-design-selection-validator",
                        },
                        "selected": True,
                        "rationale": "The exact Design input bundle requires validation contracts.",
                        "revisit_condition": None,
                    }
                ],
                "predicate_inputs": [
                    {
                        "predicate_id": "predicate:validation",
                        "concern_id": "authored:validation",
                        "source_input_ids": [input_id],
                        "expected": True,
                    }
                ],
                "planned_witness_requirements": [],
            },
            "input_conflicts": [],
            "scope_signals": {
                "human_actors": [],
                "rendered_surfaces": [],
                "interfaces": [],
                "stores": [],
                "queues": [],
                "writers": [],
                "normative_rules": [
                    {
                        "signal_id": "signal:validate-inputs",
                        "source_input_id": input_id,
                        "rule_id": "rule:validate-inputs",
                        "verb": "validate",
                        "subject": "Design input producer",
                        "object": "approved input closure",
                        "enforcement_hint": "Require an exact passing W1 receipt.",
                    }
                ],
                "effects": [],
                "data_and_log_sinks": [],
                "deployment_targets": [],
                "compatibility_boundaries": [],
                "quality_claims": [],
                "acceptance_and_readiness_claims": [],
            },
            "authority_effect": "none",
            "closure_digest": "0" * 64,
        }

    def write_closure(self, document: dict, recompute: bool = True) -> None:
        if recompute:
            document["closure_digest"] = digest_without(document, "closure_digest")
        self.write_json(self.closure_path, document)

    def compile_at(self, name: str, document: dict | None = None, late=None) -> dict:
        if document is not None:
            self.write_closure(document)
        return W1.compile_bundle(
            self.closure_path,
            self.repo,
            self.repo / name,
            self.repo / f"{name}.attempt.json",
            SCHEMAS,
            late,
        )

    def assert_valid_attempt(self, name: str, receipt: dict) -> None:
        self.assertEqual("block", receipt["result"])
        self.assertFalse((self.repo / name).exists())
        attempt = self.repo / f"{name}.attempt.json"
        self.assertTrue(attempt.is_file())
        self.assertEqual(receipt, json.loads(attempt.read_text(encoding="utf-8")))
        schemas = {
            "closure_receipt": json.loads(
                (SCHEMAS / "design-input-closure-receipt-v1.schema.json").read_text()
            ),
            "production_receipt": json.loads(
                (SCHEMAS / "design-input-production-receipt-v1.schema.json").read_text()
            ),
        }
        W1.validate_production_receipt(receipt, schemas)
        self.assertEqual([], receipt["outputs"])
        self.assertTrue(receipt["blockers"])

    def test_normal_activation_is_atomic_and_byte_deterministic(self) -> None:
        first = self.compile_at("w1-first")
        self.assertEqual("pass", first["result"])
        self.assertEqual("design-authoring", first["next_route"])
        self.assertFalse((self.repo / "w1-first.attempt.json").exists())
        first_bytes = {
            path.name: path.read_bytes() for path in (self.repo / "w1-first").iterdir()
        }
        self.assertEqual(
            {
                "DESIGN-INPUT-CLOSURE-RECEIPT.json",
                "DESIGN-SCOPE-MANIFEST.json",
                "DESIGN-DENOMINATOR-RECEIPT.json",
                "DESIGN-SELECTION-RESULT.json",
                "DESIGN-INPUT-PRODUCTION-RECEIPT.json",
            },
            set(first_bytes),
        )
        second = self.compile_at("w1-second")
        second_bytes = {
            path.name: path.read_bytes() for path in (self.repo / "w1-second").iterdir()
        }
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, second_bytes)

    def test_discovery_activation_routes_only_to_input_review(self) -> None:
        review_root = self.repo / "review-inputs"
        review_root.mkdir()
        (review_root / "scope.md").write_text(
            "# Review input\n\nOwner-approved discovery evidence.\n", encoding="utf-8"
        )
        boundary = self.make_boundary("review-inputs", "other", "scope.md")
        approval = self.repo / "DISCOVERY-APPROVAL.json"
        self.write_approval(approval, boundary)
        document = self.make_closure(boundary, approval, "discovery")
        receipt = self.compile_at("w1-discovery", document)
        self.assertEqual("pass", receipt["result"])
        self.assertEqual("discovery", receipt["activation_kind"])
        self.assertEqual("input-review", receipt["next_route"])
        self.assertTrue(receipt["evidence_ceiling"]["selection_fixed_point"])
        self.assertFalse(receipt["evidence_ceiling"]["artifact_authored"])

    def test_approved_exact_exclusion_closes_discovered_set(self) -> None:
        review_root = self.repo / "review-inputs"
        review_root.mkdir()
        (review_root / "scope.md").write_text(
            "# Included\n\nApplicable Design input.\n", encoding="utf-8"
        )
        excluded = review_root / "excluded.md"
        excluded.write_text(
            "# Excluded\n\nOwner-approved non-applicable input.\n", encoding="utf-8"
        )
        boundary = self.make_boundary("review-inputs", "other", "*.md")
        boundary["permitted_exclusions"] = [
            {
                "path": "review-inputs/excluded.md",
                "evidence_ref": self.exact(self.no_prior_path),
            }
        ]
        material = {key: value for key, value in boundary.items() if key != "boundary_digest"}
        boundary["boundary_digest"] = canonical_digest(material)
        approval = self.repo / "EXCLUSION-APPROVAL.json"
        self.write_approval(approval, boundary)
        document = self.make_closure(boundary, approval, "discovery")
        document["exclusions"] = [
            {
                "exclusion_id": "exclusion:review-input",
                "path": "review-inputs/excluded.md",
                "reason": "The target owner determined this file is not applicable.",
                "evidence_ref": self.file_ref(
                    self.no_prior_path, "public", None, None
                ),
            }
        ]
        receipt = self.compile_at("approved-exclusion", document)
        self.assertEqual("pass", receipt["result"])
        closure_receipt = receipt["input_closure_receipt"]
        self.assertEqual(
            ["review-inputs/excluded.md"],
            closure_receipt["discovery"]["excluded_paths"],
        )
        manifest = json.loads(
            (self.repo / "approved-exclusion/DESIGN-SCOPE-MANIFEST.json").read_text()
        )
        self.assertEqual(
            ["file:review-inputs/excluded.md"],
            [item["selector"] for item in manifest["target_footprint"]["exclusions"]],
        )

    def test_canonical_public_example_passes_real_consumers(self) -> None:
        source = (
            INVOKE
            / "examples/design-input-v1/DESIGN-INPUT-CLOSURE.json"
        )
        output = self.repo / "canonical-example"
        attempt = self.repo / "canonical-example.attempt.json"
        receipt = W1.compile_bundle(
            source,
            REPOSITORY_ROOT,
            output,
            attempt,
            SCHEMAS,
        )
        self.assertEqual("pass", receipt["result"])
        self.assertEqual("input-review", receipt["next_route"])
        self.assertFalse(attempt.exists())
        self.assertEqual(5, len(list(output.iterdir())))

    def test_schema_and_governance_negatives_leave_only_valid_attempt_receipt(self) -> None:
        cases = []

        document = copy.deepcopy(self.closure)
        document["closure_digest"] = "0" * 64
        cases.append(("stale-closure-digest", document, False))

        document = copy.deepcopy(self.closure)
        document["target"]["owner"] = "different-owner"
        cases.append(("approval-mismatch", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["source_ref"]["visibility"] = "private"
        cases.append(("visibility-leak", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["classification"] = "conditional"
        cases.append(("unresolved-conditional", document, True))

        document = copy.deepcopy(self.closure)
        document["input_conflicts"] = [
            {
                "conflict_id": "conflict:one",
                "input_ids": ["input:define"],
                "resolution_status": "unresolved",
                "decision_ref": None,
            }
        ]
        cases.append(("unresolved-conflict", document, True))

        document = copy.deepcopy(self.closure)
        document["scope_signals"]["normative_rules"][0]["source_input_id"] = (
            "input:missing"
        )
        cases.append(("invalid-signal-provenance", document, True))

        document = copy.deepcopy(self.closure)
        document["activation"]["define_stage_receipt_ref"]["sha256"] = "0" * 64
        cases.append(("invalid-define-receipt", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["source_ref"]["sha256"] = "0" * 64
        cases.append(("stale-input-ref", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["source_ref"]["path"] = "../escape.json"
        document["input_catalog"][0]["selector"] = "file:../escape.json"
        cases.append(("path-escape", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["source_ref"] = self.file_ref(
            self.no_prior_path, "public", None, None
        )
        document["input_catalog"][0]["selector"] = (
            "file:NO-PRIOR-DESIGN.json"
        )
        cases.append(("catalog-outside-boundary", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["classification"] = "excluded"
        document["input_catalog"][0]["exclusion_evidence_ref"] = self.file_ref(
            self.no_prior_path, "public", None, None
        )
        cases.append(("unjustified-exclusion", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"][0]["source_ref"]["expected_schema_id"] = (
            "https://arcanum.dev/schemas/invoke/unavailable/v1"
        )
        document["input_catalog"][0]["source_ref"]["expected_schema_version"] = (
            "unavailable.v1"
        )
        cases.append(("schema-identity-mismatch", document, True))

        document = copy.deepcopy(self.closure)
        document["input_catalog"] = []
        cases.append(("omitted-catalog-input", document, True))

        document = copy.deepcopy(self.closure)
        del document["scope_manifest_contract_ref"]
        cases.append(("missing-manifest-contract", document, True))

        document = copy.deepcopy(self.closure)
        document["scope_signals"]["acceptance_and_readiness_claims"] = [
            {
                "signal_id": "signal:illegal-readiness",
                "source_input_id": "input:define",
                "claim_id": "claim:illegal-readiness",
                "selector": "future-validator",
                "evidence_state": "design-validator-pass",
            }
        ]
        cases.append(("illegal-readiness", document, True))

        for name, document, recompute in cases:
            with self.subTest(name=name):
                self.write_closure(document, recompute=recompute)
                receipt = self.compile_at(name)
                self.assert_valid_attempt(name, receipt)

    def test_ambiguous_discovery_and_missing_required_class_block(self) -> None:
        boundary = copy.deepcopy(self.boundary)
        boundary["discovery_rules"].append(
            {
                "rule_id": "rule:duplicate-classification",
                "root_id": "root:inputs",
                "input_class": "define-artifact",
                "include_globs": ["DEFINITIONS.json"],
            }
        )
        material = {key: value for key, value in boundary.items() if key != "boundary_digest"}
        boundary["boundary_digest"] = canonical_digest(material)
        self.write_approval(self.approval_path, boundary)
        document = self.make_closure(boundary, self.approval_path, "normal")
        receipt = self.compile_at("ambiguous-discovery", document)
        self.assert_valid_attempt("ambiguous-discovery", receipt)
        self.assertIn(
            "DISCOVERY_INPUT_AMBIGUOUS",
            {item["code"] for item in receipt["blockers"]},
        )

        boundary = copy.deepcopy(self.boundary)
        boundary["required_input_classes"].append("security-policy")
        material = {key: value for key, value in boundary.items() if key != "boundary_digest"}
        boundary["boundary_digest"] = canonical_digest(material)
        self.write_approval(self.approval_path, boundary)
        document = self.make_closure(boundary, self.approval_path, "normal")
        receipt = self.compile_at("missing-required-class", document)
        self.assert_valid_attempt("missing-required-class", receipt)
        self.assertIn(
            "REQUIRED_INPUT_CLASS_MISSING",
            {item["code"] for item in receipt["blockers"]},
        )

    def prior_design_closure(self, count: int, evolution: bool) -> dict:
        prior_root = self.repo / "prior-designs"
        prior_root.mkdir(exist_ok=True)
        prior_paths = []
        for index in range(count):
            path = prior_root / f"prior-{index + 1}.json"
            self.write_json(path, {"historical_design": index + 1})
            prior_paths.append(path)

        boundary = copy.deepcopy(self.boundary)
        boundary["roots"].append(
            self.directory_binding("root:prior-designs", "prior-designs")
        )
        boundary["discovery_rules"].append(
            {
                "rule_id": "rule:prior-designs",
                "root_id": "root:prior-designs",
                "input_class": "current-design",
                "include_globs": ["*.json"],
            }
        )
        boundary["required_input_classes"].append("current-design")
        material = {key: value for key, value in boundary.items() if key != "boundary_digest"}
        boundary["boundary_digest"] = canonical_digest(material)
        self.write_approval(self.approval_path, boundary)
        document = self.make_closure(boundary, self.approval_path, "normal")
        prior_ids = []
        for index, path in enumerate(prior_paths):
            input_id = f"input:prior-{index + 1}"
            prior_ids.append(input_id)
            relative = path.relative_to(self.repo).as_posix()
            document["input_catalog"].append(
                {
                    "input_id": input_id,
                    "kind": "current-design",
                    "authority_class": "historical",
                    "authority_owner": self.owner,
                    "applicability_owner": self.owner,
                    "classification": "required",
                    "selector": f"file:{relative}",
                    "source_ref": self.file_ref(path, "public", None, None),
                    "freshness": {
                        "status": "current",
                        "observed_epoch": self.epoch,
                    },
                    "applies_to": ["design-evolution"],
                    "exclusion_evidence_ref": None,
                }
            )
        document["constraints"].append(
            {
                "obligation_id": "constraint:prior-designs",
                "class": "constraint",
                "statement": "Every applicable prior Design must be determined explicitly.",
                "source_input_ids": prior_ids,
                "owner": self.owner,
            }
        )
        if evolution:
            document["design_kind"] = {
                "kind": "evolution",
                "prior_design_artifact_ref": self.file_ref(
                    prior_paths[0], "public", None, None
                ),
                "prior_design_stage_receipt_ref": self.file_ref(
                    prior_paths[0], "public", None, None
                ),
                "current_state_input_ids": prior_ids,
                "declared_delta_ids": ["delta:fixture"],
            }
        return document

    def test_false_greenfield_and_ambiguous_predecessor_block(self) -> None:
        document = self.prior_design_closure(1, evolution=False)
        receipt = self.compile_at("false-greenfield", document)
        self.assert_valid_attempt("false-greenfield", receipt)
        self.assertIn(
            "GREENFIELD_CONTRADICTED",
            {item["code"] for item in receipt["blockers"]},
        )

        document = self.prior_design_closure(2, evolution=True)
        receipt = self.compile_at("ambiguous-predecessor", document)
        self.assert_valid_attempt("ambiguous-predecessor", receipt)
        self.assertIn(
            "PRIOR_DESIGN_AMBIGUOUS",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_symlink_candidate_blocks_without_success_directory(self) -> None:
        os.symlink(
            "DEFINITIONS.json", self.define_output / "unexpected-symlink.json"
        )
        receipt = self.compile_at("symlink-block")
        self.assert_valid_attempt("symlink-block", receipt)
        self.assertIn(
            "SYMLINK_UNSUPPORTED", {item["code"] for item in receipt["blockers"]}
        )

    def test_normal_activation_rejects_stale_define_output_inventory(self) -> None:
        (self.define_output / "SPEC.md").write_text(
            "# Mutated after Define receipt\n", encoding="utf-8"
        )
        boundary = self.make_boundary(
            "define-output", "define-artifact", "DEFINITIONS.json"
        )
        self.write_approval(self.approval_path, boundary)
        document = self.make_closure(boundary, self.approval_path, "normal")
        receipt = self.compile_at("stale-define-inventory", document)
        self.assert_valid_attempt("stale-define-inventory", receipt)
        self.assertIn(
            "ACTIVATION_RECEIPT_INVALID",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_predicate_mismatch_is_detected_after_selection(self) -> None:
        document = copy.deepcopy(self.closure)
        document["scope_signals"]["normative_rules"] = []
        document["scope_signals"]["quality_claims"] = [
            {
                "signal_id": "signal:performance",
                "source_input_id": "input:define",
                "claim_id": "claim:performance",
                "source_kind": "owner-constraint",
                "threshold_or_tradeoff": "Bounded repeatability is required.",
                "required": True,
            }
        ]
        concern = document["selection_inputs"]["authored_concerns"][0]
        concern.update(
            {
                "primary_class": "performance",
                "disposition": "recommended",
                "required_predicate": False,
                "selected": False,
                "revisit_condition": "Re-evaluate when the bounded input changes.",
            }
        )
        document["selection_inputs"]["predicate_inputs"][0]["expected"] = False
        receipt = self.compile_at("predicate-mismatch", document)
        self.assert_valid_attempt("predicate-mismatch", receipt)
        self.assertEqual("PREDICATE_ASSERTION_MISMATCH", receipt["blockers"][0]["code"])

    def test_frozen_selection_block_is_wrapped_as_governed_failure(self) -> None:
        document = copy.deepcopy(self.closure)
        concern = document["selection_inputs"]["authored_concerns"][0]
        concern["required_predicate"] = False
        document["selection_inputs"]["predicate_inputs"][0]["expected"] = False
        receipt = self.compile_at("selection-block", document)
        self.assert_valid_attempt("selection-block", receipt)
        self.assertEqual("SELECTION_BLOCKED", receipt["blockers"][0]["code"])

    def test_frozen_extractor_block_is_wrapped_as_governed_failure(self) -> None:
        with mock.patch.object(
            W1,
            "extract_denominator",
            side_effect=W1.ExtractionFailure("MANIFEST_NOT_CLOSED", "injected extractor block"),
        ):
            receipt = self.compile_at("extractor-block")
        self.assert_valid_attempt("extractor-block", receipt)
        self.assertEqual("DENOMINATOR_BLOCKED", receipt["blockers"][0]["code"])

    def test_late_validation_failure_removes_staging_and_blocks(self) -> None:
        receipt = self.compile_at(
            "late-block",
            late=lambda _: (_ for _ in ()).throw(ValueError("injected late failure")),
        )
        self.assert_valid_attempt("late-block", receipt)
        self.assertEqual("LATE_VALIDATION_FAILED", receipt["blockers"][0]["code"])

    def test_late_output_inventory_change_blocks_publication(self) -> None:
        receipt = self.compile_at(
            "late-inventory-block",
            late=lambda stage: (stage / "UNDECLARED.json").write_text(
                "{}\n", encoding="utf-8"
            ),
        )
        self.assert_valid_attempt("late-inventory-block", receipt)
        self.assertEqual(
            "OUTPUT_INVENTORY_MISMATCH", receipt["blockers"][0]["code"]
        )

    def test_preexisting_destination_is_malformed_invocation_without_receipt(self) -> None:
        output = self.repo / "preexisting"
        output.mkdir()
        attempt = self.repo / "preexisting.attempt.json"
        with self.assertRaisesRegex(ValueError, "must both be absent"):
            W1.compile_bundle(
                self.closure_path,
                self.repo,
                output,
                attempt,
                SCHEMAS,
            )
        self.assertFalse(attempt.exists())

    def test_cli_exit_codes_are_zero_one_and_two(self) -> None:
        command = [
            sys.executable,
            str(INVOKE / "scripts/compile_design_input_bundle.py"),
            str(self.closure_path),
            "--repo-root",
            str(self.repo),
        ]
        passing = subprocess.run(
            command
            + [
                "--output-dir",
                str(self.repo / "cli-pass"),
                "--attempt-receipt",
                str(self.repo / "cli-pass.attempt.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, passing.returncode, passing.stdout + passing.stderr)

        blocked_source = copy.deepcopy(self.closure)
        blocked_source["closure_digest"] = "0" * 64
        self.write_closure(blocked_source, recompute=False)
        blocked = subprocess.run(
            command
            + [
                "--output-dir",
                str(self.repo / "cli-block"),
                "--attempt-receipt",
                str(self.repo / "cli-block.attempt.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, blocked.returncode, blocked.stdout + blocked.stderr)
        self.assertFalse((self.repo / "cli-block").exists())
        self.assertTrue((self.repo / "cli-block.attempt.json").is_file())

        malformed_output = self.repo / "cli-malformed"
        malformed_output.mkdir()
        malformed = subprocess.run(
            command
            + [
                "--output-dir",
                str(malformed_output),
                "--attempt-receipt",
                str(self.repo / "cli-malformed.attempt.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, malformed.returncode, malformed.stdout + malformed.stderr)
        self.assertFalse((self.repo / "cli-malformed.attempt.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

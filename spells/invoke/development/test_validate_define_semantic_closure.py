#!/usr/bin/env python3
"""Executable W1 tests for pre-Define semantic closure.

Unlike the schema-family fixtures, these tests construct real repositories,
real selectors, and real SHA-256/size bindings.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


INVOKE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = INVOKE_DIR / "scripts" / "validate_define_semantic_closure.py"
CONTEXT_SCHEMA = INVOKE_DIR / "schemas" / "define-semantic-context-v1.schema.json"
RECEIPT_SCHEMA = INVOKE_DIR / "schemas" / "define-semantic-closure-receipt-v1.schema.json"
CONTEXT_SCHEMA_V2 = INVOKE_DIR / "schemas" / "define-semantic-context-v2.schema.json"
RECEIPT_SCHEMA_V2 = INVOKE_DIR / "schemas" / "define-semantic-closure-receipt-v2.schema.json"

VALIDATOR_SPEC = importlib.util.spec_from_file_location("define_semantic_closure_validator", SCRIPT)
assert VALIDATOR_SPEC is not None and VALIDATOR_SPEC.loader is not None
VALIDATOR_MODULE = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR_MODULE)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


class RepositoryFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.context_schema = root / "schemas" / "context.schema.json"
        self.receipt_schema = root / "schemas" / "receipt.schema.json"
        self.context_path = root / "public" / "DEFINE-SEMANTIC-CONTEXT.json"
        self.context_schema.parent.mkdir(parents=True)
        self.context_schema.write_bytes(CONTEXT_SCHEMA.read_bytes())
        self.receipt_schema.write_bytes(RECEIPT_SCHEMA.read_bytes())
        self._write_sources()
        self.context = self._context()
        self.write_context()

    def _write_sources(self) -> None:
        files = {
            "public/definitions/DEFINITIONS.md": """# Canonical Definitions

Status: active
Owner: definitions-governance

## DEF-ARC-CONTRACT: Contract

Status: active
Term: contract
Aliases: artifact contract

### Plain-Language Voice

A contract is the promise around bounded work.

## DEF-ARC-CONTRACT-OTHER: Contract Other

Status: active
Term: contract other
Aliases:

### DS-D1: Meta-type System
""",
            "public/definitions/DEFINITIONS-INDEX.md": """# Definitions Index

## Terms

| ID | Term | Status | Canonical section | Plain-language intuition |
| --- | --- | --- | --- | --- |
| DEF-ARC-CONTRACT | contract | active | [Contract](DEFINITIONS.md#def-arc-contract-contract) | The promise. |
| DEF-ARC-CONTRACT-OTHER | contract other | active | [Contract Other](DEFINITIONS.md#def-arc-contract-other-contract-other) | Another exact section. |
| DS-D1 | meta-type system | active | [DS-D1](DEFINITIONS.md#ds-d1-meta-type-system) | The vocabulary. |

## Alias Lookup

| Alias | Definition ID |
| --- | --- |
| artifact contract | DEF-ARC-CONTRACT |
""",
            "public/governance.md": "# Definitions Governance\n\nOwner: definitions-governance\n",
            "public/discovery.md": """# Purpose

The feature needs a checked vocabulary boundary.

## Contract

Reuse contract and artifact contract.

## Semantic Closure

Define semantic closure for this feature.

## Feature Contract

Specialize contract as feature contract.
""",
            "public/consumer/SPEC.md": "# Vocabulary\n\nUses contract, semantic closure, and feature contract.\n",
        }
        for relative, content in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        write_json(self.root / "public/adjacent/DEFINITIONS.json", {"definitions": []})

    def ref(
        self,
        relative: str,
        source_format: str,
        selector_type: str,
        selector: str,
        visibility: str = "public",
    ) -> dict[str, Any]:
        data = (self.root / relative).read_bytes()
        return {
            "path": relative,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "format": source_format,
            "selector_type": selector_type,
            "selector": selector,
            "visibility": visibility,
        }

    def canonical_match(self, match_id: str, kind: str = "term") -> dict[str, Any]:
        return {
            "match_id": match_id,
            "kind": kind,
            "authority_class": "canonical",
            "definition_id": "DEF-ARC-CONTRACT",
            "term": "contract",
            "authority_scope": {"kind": "repository", "ref": "fixture-repository"},
            "source_ref": self.ref(
                "public/definitions/DEFINITIONS.md",
                "markdown",
                "anchor",
                "def-arc-contract-contract",
            ),
        }

    def _context(self) -> dict[str, Any]:
        discovery_ref = self.ref("public/discovery.md", "markdown", "heading", "Purpose")
        return {
            "$schema": "https://arcanum.dev/schemas/invoke/define-semantic-context/v1",
            "schema_version": "invoke.define-semantic-context.v1",
            "context_id": "fixture:semantic-context",
            "authored_by": "fixture-context-author",
            "assessed_by": "fixture-semantic-assessor",
            "target": {
                "id": "fixture:target",
                "objective": "Author a drift-aware definition bundle.",
                "authority_scope": {"kind": "feature", "ref": "fixture-feature"},
                "visibility": "public",
            },
            "discovery": {"kind": "artifact", "ref": discovery_ref},
            "discovery_contract": {
                "profile": "semantic-surface-v1",
                "claim_scope": "configured-roots-complete",
                "roots": [
                    {
                        "root_id": "root:public",
                        "path": "public",
                        "registry_globs": ["**/DEFINITIONS.md", "**/DEFINITIONS-INDEX.md", "**/DEFINITIONS.json", "**/GLOSSARY.md"],
                        "consumer_globs": ["**/*.md"],
                        "visibility": "public",
                    }
                ],
            },
            "concept_probes": [
                {
                    "probe_id": "probe:reuse-contract",
                    "term": "contract",
                    "aliases": ["artifact contract"],
                    "intent": "Reuse the repository contract definition.",
                    "intended_scope": {"kind": "feature", "ref": "fixture-feature"},
                    "evidence_refs": [self.ref("public/discovery.md", "markdown", "heading", "Contract")],
                    "proposed_disposition": "reuse-existing",
                    "claimed_matches": [self.canonical_match("match:reuse-contract")],
                    "proposed_basis_ids": ["DEF-ARC-CONTRACT"],
                    "assessment_rationale": "The canonical term and alias are exact matches.",
                },
                {
                    "probe_id": "probe:new-semantic-closure",
                    "term": "semantic closure",
                    "aliases": ["definition context closure"],
                    "intent": "Name the local checked vocabulary boundary.",
                    "intended_scope": {"kind": "feature", "ref": "fixture-feature"},
                    "evidence_refs": [self.ref("public/discovery.md", "markdown", "heading", "Semantic Closure")],
                    "proposed_disposition": "new-scoped-term",
                    "claimed_matches": [],
                    "proposed_basis_ids": [],
                    "assessment_rationale": "No inspected registry owns this local meaning.",
                },
                {
                    "probe_id": "probe:specialize-contract",
                    "term": "feature contract",
                    "aliases": ["scoped contract"],
                    "intent": "Specialize the repository contract for one feature.",
                    "intended_scope": {"kind": "feature", "ref": "fixture-feature"},
                    "evidence_refs": [self.ref("public/discovery.md", "markdown", "heading", "Feature Contract")],
                    "proposed_disposition": "specialize-existing",
                    "claimed_matches": [self.canonical_match("match:specialize-contract", "semantic-overlap")],
                    "proposed_basis_ids": ["DEF-ARC-CONTRACT"],
                    "assessment_rationale": "The feature meaning is a strict narrowing of contract.",
                },
            ],
            "authority_boundary": {
                "declaration": "configured",
                "profile": "markdown-index-v1",
                "declared_owner": "definitions-governance",
                "canonical_scope": {"kind": "repository", "ref": "fixture-repository"},
                "canonical_source_refs": [self.ref("public/definitions/DEFINITIONS.md", "markdown", "heading", "Canonical Definitions")],
                "index_refs": [self.ref("public/definitions/DEFINITIONS-INDEX.md", "markdown", "heading", "Definitions Index")],
                "resolution_evidence_refs": [self.ref("public/governance.md", "markdown", "whole-file", "$")],
            },
            "adjacent_registries": [
                {
                    "registry_id": "registry:adjacent",
                    "authority_class": "candidate",
                    "format_profile": "definitions-json-v1",
                    "source_ref": self.ref("public/adjacent/DEFINITIONS.json", "json", "json-pointer", "/definitions"),
                    "reason_in_scope": "The adjacent feature shares the vocabulary boundary.",
                }
            ],
            "consumer_boundary": {
                "classification": "catalogued",
                "consumers": [
                    {
                        "consumer_id": "consumer:spec",
                        "kind": "narrative",
                        "source_ref": self.ref("public/consumer/SPEC.md", "markdown", "symbol", "Uses contract"),
                        "reason_in_scope": "The feature specification consumes the probed vocabulary.",
                    }
                ],
                "rationale": None,
            },
            "exclusions": [],
            "authority_effect": "none",
        }

    def write_context(self) -> None:
        write_json(self.context_path, self.context)

    def upgrade_to_v2(self) -> None:
        """Upgrade the real repository fixture to the additive intent contract."""

        self.context_schema.write_bytes(CONTEXT_SCHEMA_V2.read_bytes())
        self.receipt_schema.write_bytes(RECEIPT_SCHEMA_V2.read_bytes())
        self.context["$schema"] = "https://arcanum.dev/schemas/invoke/define-semantic-context/v2"
        self.context["schema_version"] = "invoke.define-semantic-context.v2"
        self.context["discovery_contract"] = {
            "profile": "semantic-surface-v2",
            "claim_scope": "configured-roots-complete",
            "registry_roots": [
                {
                    "root_id": "root:public-registries",
                    "path": "public",
                    "globs": [
                        "**/DEFINITIONS.md",
                        "**/DEFINITIONS-INDEX.md",
                        "**/DEFINITIONS.json",
                        "**/GLOSSARY.md",
                    ],
                    "visibility": "public",
                }
            ],
            "consumer_roots": [
                {
                    "root_id": "root:public-consumers",
                    "path": "public",
                    "globs": ["consumer/*.md"],
                    "visibility": "public",
                }
            ],
        }
        evidence_source_id = "intent-source:fixture-discovery"
        obligations = []
        for probe in self.context["concept_probes"]:
            obligation_id = f"obligation:{probe['probe_id'].split(':', 1)[1]}"
            probe["obligation_ids"] = [obligation_id]
            obligations.append(
                {
                    "obligation_id": obligation_id,
                    "kind": "concept",
                    "statement": probe["intent"],
                    "status": "covered",
                    "evidence_source_ids": [evidence_source_id],
                    "probe_ids": [probe["probe_id"]],
                    "relationship": None,
                    "boundary": None,
                    "rationale": "The target objective requires this concept.",
                }
            )
        represented = [item["obligation_id"] for item in obligations]
        self.context["intent_coverage"] = {
            "claim_ceiling": "enumerated-semantic-obligations",
            "evidence_sources": [
                {
                    "source_id": evidence_source_id,
                    "source_class": "current-intent",
                    "source_ref": self.ref(
                        "public/discovery.md", "markdown", "heading", "Purpose"
                    ),
                    "semantic_disposition": "retain",
                    "authority_disposition": "none",
                    "rationale": "The discovery artifact states the current bounded objective.",
                }
            ],
            "facets": [
                {
                    "facet_id": "subject",
                    "status": "represented",
                    "obligation_ids": represented,
                    "evidence_source_ids": [evidence_source_id],
                    "rationale": "The three probed concepts define the fixture subject.",
                },
                *[
                    {
                        "facet_id": facet_id,
                        "status": "not-applicable",
                        "obligation_ids": [],
                        "evidence_source_ids": [evidence_source_id],
                        "rationale": "This bounded vocabulary fixture does not require this facet.",
                    }
                    for facet_id in (
                        "parts",
                        "relationships",
                        "evidence-state",
                        "validation-gates",
                        "execution-handoff",
                        "authority-boundary",
                    )
                ],
            ],
            "obligations": obligations,
        }
        self.write_context()

    def refresh_path(self, relative: str) -> None:
        data = (self.root / relative).read_bytes()
        digest = hashlib.sha256(data).hexdigest()

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                if value.get("path") == relative and "sha256" in value and "size" in value:
                    value["sha256"] = digest
                    value["size"] = len(data)
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.context)
        self.write_context()

    def run(
        self,
        output_name: str = "receipt.json",
        discovery_roots: list[str] | None = None,
        public_roots: list[str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
                sys.executable,
                str(SCRIPT),
                str(self.context_path),
                "--repository-root",
                str(self.root),
                "--context-schema",
                str(self.context_schema),
                "--receipt-schema",
                str(self.receipt_schema),
        ]
        for root in discovery_roots or ["public"]:
            command.extend(["--discovery-root", root])
        effective_public_roots = public_roots if public_roots is not None else ["public"]
        for root in effective_public_roots:
            command.extend(["--public-root", root])
        command.extend(["--output", str(self.root / output_name)])
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )


class DefineSemanticClosureValidatorTest(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], RepositoryFixture]:
        temporary = tempfile.TemporaryDirectory()
        return temporary, RepositoryFixture(Path(temporary.name))

    def assert_receipt(self, fixture: RepositoryFixture, output_name: str = "receipt.json") -> dict[str, Any]:
        receipt = json.loads((fixture.root / output_name).read_text(encoding="utf-8"))
        schema = json.loads(fixture.receipt_schema.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(receipt)
        digest_material = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        self.assertEqual(hashlib.sha256(canonical_bytes(digest_material)).hexdigest(), receipt["receipt_digest"])
        return receipt

    def test_real_mixed_context_is_ready_and_deterministic(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        first = fixture.run("one.json")
        second = fixture.run("two.json")
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual((fixture.root / "one.json").read_bytes(), (fixture.root / "two.json").read_bytes())
        receipt = self.assert_receipt(fixture, "one.json")
        self.assertEqual("ready-for-define", receipt["outcome"])
        self.assertEqual("configured-roots-complete", receipt["claim_scope"])
        self.assertEqual(8, len(receipt["checks"]))
        self.assertTrue(all(check["status"] == "pass" for check in receipt["checks"]))
        self.assertEqual(2, len(receipt["authority_resolution"]["canonical_source_refs"]) + len(receipt["authority_resolution"]["index_refs"]))
        snapshot = receipt["discovery_snapshots"][0]
        self.assertEqual(
            set(snapshot["registry_paths"] + snapshot["consumer_paths"] + snapshot["excluded_paths"]),
            {item["path"] for item in snapshot["content_refs"]},
        )
        for proposal, result in zip(fixture.context["concept_probes"], receipt["probe_results"], strict=True):
            self.assertEqual(proposal["proposed_disposition"], result["disposition"])
            self.assertEqual(proposal["claimed_matches"], result["matches"])
            self.assertEqual(proposal["proposed_basis_ids"], result["basis_ids"])
            self.assertEqual(proposal["assessment_rationale"], result["rationale"])

    def test_v2_intent_complete_context_is_ready_and_deterministic(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_to_v2()
        first = fixture.run("one.json")
        second = fixture.run("two.json")
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(
            (fixture.root / "one.json").read_bytes(),
            (fixture.root / "two.json").read_bytes(),
        )
        receipt = self.assert_receipt(fixture, "one.json")
        self.assertEqual("invoke.define-semantic-closure-receipt.v2", receipt["schema_version"])
        self.assertEqual("invoke.validate-define-semantic-closure.v2", receipt["validator"]["identity"])
        self.assertEqual("ready-for-define", receipt["outcome"])
        self.assertEqual(11, len(receipt["checks"]))
        self.assertTrue(all(item["status"] == "pass" for item in receipt["checks"]))
        self.assertEqual(
            {
                "total": 3,
                "covered": 3,
                "out_of_scope": 0,
                "uncovered": 0,
                "concept": 3,
                "relationship": 0,
                "boundary": 0,
            },
            receipt["intent_coverage"]["summary"],
        )

    def test_v2_uncovered_obligation_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_to_v2()
        obligation = fixture.context["intent_coverage"]["obligations"][0]
        obligation["status"] = "uncovered"
        obligation["probe_ids"] = []
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("INTENT_OBLIGATION_UNCOVERED", codes)

    def test_v2_orphan_probe_blocks_declared_probe_integrity(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_to_v2()
        obligation = fixture.context["intent_coverage"]["obligations"][0]
        obligation["status"] = "out-of-scope"
        obligation["probe_ids"] = []
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("INTENT_PROBE_ORPHANED", codes)
        check = next(
            item
            for item in receipt["checks"]
            if item["check_id"] == "check:declared-probe-integrity"
        )
        self.assertEqual("block", check["status"])

    def test_v2_historical_source_requires_separate_dispositions(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_to_v2()
        source = fixture.context["intent_coverage"]["evidence_sources"][0]
        source["source_class"] = "historical"
        source["semantic_disposition"] = "unspecified"
        source["authority_disposition"] = "unspecified"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("HISTORICAL_EVIDENCE_DISPOSITION_MISSING", codes)

    def test_v2_consumer_topology_is_not_filtered_by_probe_labels(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.upgrade_to_v2()
        hidden = fixture.root / "public/consumer/HIDDEN.md"
        hidden.write_text(
            "# Downstream Usage\n\nThis artifact deliberately omits every selected probe label.\n",
            encoding="utf-8",
        )
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("CONSUMER_COVERAGE_MISMATCH", codes)
        discovered = {
            path
            for snapshot in receipt["discovery_snapshots"]
            for path in snapshot["consumer_paths"]
        }
        self.assertIn("public/consumer/HIDDEN.md", discovered)

    def test_in_memory_api_is_byte_identical_to_cli_receipt(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        cli = fixture.run()
        self.assertEqual(0, cli.returncode, cli.stderr)

        replayed = VALIDATOR_MODULE.evaluate_context(
            context_path=fixture.context_path,
            repository_root=fixture.root,
            context_schema_path=fixture.context_schema,
            receipt_schema_path=fixture.receipt_schema,
            discovery_roots=["public"],
            public_roots=["public"],
        )

        self.assertEqual((fixture.root / "receipt.json").read_bytes(), canonical_bytes(replayed))
        self.assertFalse((fixture.root / ".define-semantic-closure.in-memory.json").exists())

    def test_in_memory_replay_observes_topology_added_after_receipt(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        cli = fixture.run()
        self.assertEqual(0, cli.returncode, cli.stderr)
        original = self.assert_receipt(fixture)
        write_json(
            fixture.root / "public/late/DEFINITIONS.json",
            {"definitions": [{"id": "LATE-D1", "term": "late terminology", "aliases": []}]},
        )

        replayed = VALIDATOR_MODULE.evaluate_context(
            context_path=fixture.context_path,
            repository_root=fixture.root,
            context_schema_path=fixture.context_schema,
            receipt_schema_path=fixture.receipt_schema,
            discovery_roots=["public"],
            public_roots=["public"],
        )

        self.assertNotEqual(canonical_bytes(original), canonical_bytes(replayed))
        self.assertEqual("blocked", replayed["outcome"])
        self.assertIn("REGISTRY_COVERAGE_MISMATCH", {item["code"] for item in replayed["blockers"]})

    def test_all_reuse_context_is_ready_without_candidate_assumption(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"] = [fixture.context["concept_probes"][0]]
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual("ready-for-define", receipt["outcome"])
        self.assertEqual(["reuse-existing"], [item["disposition"] for item in receipt["probe_results"]])

    def test_supported_canonical_change_routes_to_governance(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"][2]["proposed_disposition"] = "canonical-change-proposal"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual("definitions-governance-required", receipt["outcome"])
        self.assertEqual("definitions-governance", receipt["next_route"])
        self.assertEqual([], receipt["blockers"])

    def test_forged_canonical_scope_cannot_support_reuse(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"][0]["claimed_matches"][0]["authority_scope"] = {
            "kind": "repository",
            "ref": "different-repository",
        }
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("UNSUPPORTED_SEMANTIC_MATCH", codes)

    def test_wrong_canonical_section_cannot_support_match(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        source_ref = fixture.context["concept_probes"][0]["claimed_matches"][0]["source_ref"]
        source_ref["selector"] = "ds-d1-meta-type-system"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("UNSUPPORTED_SEMANTIC_MATCH", codes)

    def test_prefix_colliding_canonical_anchor_cannot_support_match(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        source_ref = fixture.context["concept_probes"][0]["claimed_matches"][0]["source_ref"]
        source_ref["selector"] = "def-arc-contract-other-contract-other"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("UNSUPPORTED_SEMANTIC_MATCH", codes)

    def test_trusted_public_root_rejects_author_declared_private_root(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        (fixture.root / "private").mkdir()
        fixture.context["discovery_contract"]["roots"].append(
            {
                "root_id": "root:private-labelled-public",
                "path": "private",
                "registry_globs": ["**/DEFINITIONS.md", "**/DEFINITIONS-INDEX.md", "**/DEFINITIONS.json", "**/GLOSSARY.md"],
                "consumer_globs": ["**/*.md"],
                "visibility": "public",
            }
        )
        fixture.write_context()
        result = fixture.run(discovery_roots=["public", "private"], public_roots=["public"])
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("DISCOVERY_ROOT_OUTSIDE_PUBLIC_BOUNDARY", codes)

    def test_conflicting_exact_reference_is_not_deduplicated(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        conflicting = dict(fixture.context["concept_probes"][1]["evidence_refs"][0])
        conflicting["sha256"] = "0" * 64
        fixture.context["concept_probes"][1]["evidence_refs"].append(conflicting)
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        same_selector = [
            item
            for item in receipt["inspected_sources"]
            if item["declared_path"] == conflicting["path"]
            and item["selector"] == conflicting["selector"]
            and item["role"] == "probe-evidence"
        ]
        self.assertEqual(2, len(same_selector))
        self.assertEqual({"current", "stale"}, {item["status"] for item in same_selector})

    def test_explicit_conflict_is_terminal_and_causal(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"][0]["proposed_disposition"] = "blocked-conflict"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual("blocked", receipt["outcome"])
        self.assertEqual("stop", receipt["next_route"])
        causal = receipt["probe_results"][0]["causal_blocker_ids"]
        self.assertTrue(causal)
        self.assertTrue(set(causal).issubset({item["blocker_id"] for item in receipt["blockers"]}))

    def test_schema_invalid_context_writes_no_receipt(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        del fixture.context["assessed_by"]
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(2, result.returncode)
        self.assertFalse((fixture.root / "receipt.json").exists())

    def test_existing_output_is_never_overwritten(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        output = fixture.root / "receipt.json"
        output.write_bytes(b"owner bytes\n")
        result = fixture.run()
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"owner bytes\n", output.read_bytes())

    def test_output_outside_repository_is_rejected(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        outside = fixture.root.parent / f"{fixture.root.name}-receipt.json"
        self.addCleanup(outside.unlink, missing_ok=True)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(fixture.context_path),
                "--repository-root",
                str(fixture.root),
                "--context-schema",
                str(fixture.context_schema),
                "--receipt-schema",
                str(fixture.receipt_schema),
                "--discovery-root",
                "public",
                "--public-root",
                "public",
                "--output",
                str(outside),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertFalse(outside.exists())

    def test_missing_resolution_evidence_still_emits_blocked_receipt(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        (fixture.root / "public/governance.md").unlink()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual("blocked", receipt["outcome"])
        self.assertEqual("ambiguous", receipt["authority_resolution"]["status"])
        self.assertEqual([], receipt["authority_resolution"]["evidence_refs"])

    def test_stale_consumer_does_not_hide_reachable_canonical_parity(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        consumer = fixture.root / "public/consumer/SPEC.md"
        consumer.write_text("# Vocabulary\n\nUses contract, semantic closure, and feature contract. Changed.\n", encoding="utf-8")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        parity = next(item for item in receipt["checks"] if item["check_id"] == "check:canonical-index-parity")
        freshness = next(item for item in receipt["checks"] if item["check_id"] == "check:source-freshness")
        self.assertEqual("pass", parity["status"])
        self.assertEqual("block", freshness["status"])

    def test_canonical_index_drift_blocks_after_freshness_refresh(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        index = fixture.root / "public/definitions/DEFINITIONS-INDEX.md"
        index.write_text(index.read_text(encoding="utf-8").replace("| contract | active |", "| changed contract | active |"), encoding="utf-8")
        fixture.refresh_path("public/definitions/DEFINITIONS-INDEX.md")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        check = next(item for item in receipt["checks"] if item["check_id"] == "check:canonical-index-parity")
        self.assertEqual("block", check["status"])

    def test_undeclared_registry_and_normalized_match_block(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        write_json(
            fixture.root / "public/hidden/DEFINITIONS.json",
            {"definitions": [{"id": "HIDDEN-D1", "term": "semantic\u00a0closure", "aliases": []}]},
        )
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("REGISTRY_COVERAGE_MISMATCH", codes)

    def test_malformed_declared_registry_profile_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        write_json(
            fixture.root / "public/adjacent/DEFINITIONS.json",
            {"definitions": [{"term": "unidentified term", "aliases": []}]},
        )
        fixture.refresh_path("public/adjacent/DEFINITIONS.json")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("ADJACENT_REGISTRY_PARSE_FAILURE", codes)

    def test_duplicate_definition_ids_inside_adjacent_registry_block(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        write_json(
            fixture.root / "public/adjacent/DEFINITIONS.json",
            {
                "definitions": [
                    {"id": "ADJ-D1", "term": "first unrelated term", "aliases": []},
                    {"id": "ADJ-D1", "term": "second unrelated term", "aliases": []},
                ]
            },
        )
        fixture.refresh_path("public/adjacent/DEFINITIONS.json")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("ADJACENT_REGISTRY_PARSE_FAILURE", codes)

    def test_unreadable_discovered_consumer_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        broken = fixture.root / "public/consumer/BROKEN.md"
        broken.write_bytes(b"# Broken\n\xff\xfe contract\n")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertIn("CONSUMER_DISCOVERY_READ_FAILURE", codes)

    def test_stale_adjacent_registry_makes_collision_not_evaluable(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        write_json(
            fixture.root / "public/adjacent/DEFINITIONS.json",
            {"definitions": [{"id": "ADJ-D1", "term": "unrelated", "aliases": []}]},
        )
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        collision = next(item for item in receipt["checks"] if item["check_id"] == "check:normalized-collision")
        self.assertEqual("not_evaluable", collision["status"])
        self.assertTrue(collision["causal_blocker_ids"])

    def test_duplicate_probe_makes_semantics_not_evaluable(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"][2]["probe_id"] = fixture.context["concept_probes"][0]["probe_id"]
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        semantic = next(item for item in receipt["checks"] if item["check_id"] == "check:semantic-overlap")
        self.assertEqual("not_evaluable", semantic["status"])
        self.assertTrue(semantic["causal_blocker_ids"])

    def test_yaml_path_selector_is_resolved(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        yaml_path = fixture.root / "public/evidence.yaml"
        yaml_path.write_text("purpose:\n  statement: checked\n", encoding="utf-8")
        fixture.context["discovery"]["ref"] = fixture.ref(
            "public/evidence.yaml", "yaml", "yaml-path", "purpose.statement"
        )
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("ready-for-define", self.assert_receipt(fixture)["outcome"])

    def test_duplicate_json_keys_fail_source_freshness(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        registry = fixture.root / "public/adjacent/DEFINITIONS.json"
        registry.write_text('{"definitions":[],"definitions":[]}\n', encoding="utf-8")
        fixture.refresh_path("public/adjacent/DEFINITIONS.json")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        freshness = next(item for item in receipt["checks"] if item["check_id"] == "check:source-freshness")
        self.assertEqual("block", freshness["status"])

    def test_unresolved_json_pointer_fails_source_freshness(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["adjacent_registries"][0]["source_ref"]["selector"] = "/missing"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        freshness = next(item for item in receipt["checks"] if item["check_id"] == "check:source-freshness")
        self.assertEqual("block", freshness["status"])

    def test_duplicate_yaml_keys_fail_source_freshness(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        yaml_path = fixture.root / "public/evidence.yaml"
        yaml_path.write_text("purpose:\n  statement: one\npurpose:\n  statement: two\n", encoding="utf-8")
        fixture.context["discovery"]["ref"] = fixture.ref(
            "public/evidence.yaml", "yaml", "yaml-path", "purpose.statement"
        )
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        freshness = next(item for item in receipt["checks"] if item["check_id"] == "check:source-freshness")
        self.assertEqual("block", freshness["status"])

    def test_private_target_does_not_require_public_root(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["target"]["visibility"] = "private"
        fixture.write_context()
        result = fixture.run(public_roots=[])
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual([], receipt["visibility_boundary"]["public_roots"])

    def test_exact_evidenced_consumer_exclusion_passes(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        hidden = fixture.root / "public/consumer/HIDDEN.md"
        hidden.write_text("# Historical\n\nsemantic closure appears only in archived evidence.\n", encoding="utf-8")
        evidence = fixture.root / "public/exclusion-evidence.md"
        evidence.write_text("# Exclusion Decision\n\nThis archived file is not a current consumer.\n", encoding="utf-8")
        fixture.context["exclusions"] = [
            {
                "exclusion_id": "exclusion:hidden-history",
                "selector": "public/consumer/HIDDEN.md",
                "reason": "The file is immutable historical evidence, not a current semantic consumer.",
                "evidence_ref": fixture.ref("public/exclusion-evidence.md", "markdown", "heading", "Exclusion Decision"),
                "owner": "fixture-exclusion-owner",
            }
        ]
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertIn("public/consumer/HIDDEN.md", receipt["discovery_snapshots"][0]["excluded_paths"])

    def test_public_symlink_escape_blocks_as_stale_source(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        outside = fixture.root.parent / f"{fixture.root.name}-outside.md"
        outside.write_text("# Vocabulary\n\nUses contract.\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        consumer = fixture.root / "public/consumer/SPEC.md"
        consumer.unlink()
        consumer.symlink_to(outside)
        fixture.refresh_path("public/consumer/SPEC.md")
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        source_check = next(item for item in receipt["checks"] if item["check_id"] == "check:source-freshness")
        self.assertEqual("block", source_check["status"])

    def test_collect_all_multidefect_receipt_has_all_checks_and_closed_causes(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["authored_by"] = fixture.context["assessed_by"]
        fixture.context["concept_probes"][2]["probe_id"] = fixture.context["concept_probes"][0]["probe_id"]
        fixture.context["authority_boundary"]["canonical_source_refs"][0]["sha256"] = "0" * 64
        hidden = fixture.root / "public/consumer/HIDDEN.md"
        hidden.write_text("# Hidden\n\nsemantic closure is consumed here.\n", encoding="utf-8")
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        self.assertEqual("blocked", receipt["outcome"])
        self.assertEqual(8, len(receipt["checks"]))
        statuses = {item["status"] for item in receipt["checks"]}
        self.assertIn("block", statuses)
        self.assertIn("not_evaluable", statuses)
        codes = {item["code"] for item in receipt["blockers"]}
        self.assertTrue({
            "SOURCE_FRESHNESS_FAILURE",
            "DUPLICATE_PROBE_ID",
            "CONSUMER_COVERAGE_MISMATCH",
            "INDEPENDENT_OWNER_REQUIRED",
        }.issubset(codes))
        blocker_ids = {item["blocker_id"] for item in receipt["blockers"]}
        used_ids = {
            blocker_id
            for item in [*receipt["checks"], *receipt["probe_results"], *receipt["inspected_sources"]]
            for blocker_id in item["causal_blocker_ids"]
        }
        self.assertEqual(blocker_ids, used_ids)

    def test_context_author_must_not_be_assessor(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["assessed_by"] = fixture.context["authored_by"]
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        check = next(item for item in receipt["checks"] if item["check_id"] == "check:independent-owner")
        self.assertEqual("block", check["status"])

    def test_canonical_owner_must_not_be_semantic_assessor(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["assessed_by"] = "definitions-governance"
        fixture.write_context()
        result = fixture.run()
        self.assertEqual(1, result.returncode, result.stderr)
        receipt = self.assert_receipt(fixture)
        check = next(item for item in receipt["checks"] if item["check_id"] == "check:independent-owner")
        self.assertEqual("block", check["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

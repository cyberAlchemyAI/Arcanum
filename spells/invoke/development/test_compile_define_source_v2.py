#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


INVOKE = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "compile_define_source_v2",
    INVOKE / "scripts/compile_define_source_v2.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DefineV2ProducerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        (self.repo / "inputs").mkdir()
        (self.repo / "arcanum").mkdir()
        self.discovery = self.repo / "inputs/discovery.md"
        self.discovery.write_text("# Purpose\n\nBounded discovery evidence.\n", encoding="utf-8")
        self.public_discovery = self.repo / "arcanum/discovery.md"
        self.public_discovery.write_text("# Purpose\n\nPublic bounded discovery evidence.\n", encoding="utf-8")
        self.source = self.repo / "DEFINE-SOURCE-v2.json"
        self.output = self.repo / "output"
        source_ref = self.ref(self.discovery, "inputs/discovery.md")
        self.base = {
            "schema_version": "invoke.define-source.v2",
            "source_id": "DEFINE-V2-FIXTURE-001",
            "target": {
                "id": "Generic Definitions Capability",
                "objective": "Establish one exact-source-bound candidate definition registry.",
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
                    "id": "D-001",
                    "title": "Candidate Boundary",
                    "statement": "The generated registry remains candidate and authority-free.",
                }
            ],
            "definition_registry": {
                "registry_id": "demo.definitions.v2",
                "title": "Demo Candidate Definitions",
                "owner_route": "definitions-governance",
                "authority_scope": {"kind": "project", "ref": "demo"},
                "visibility": "private",
                "definitions": [self.definition(source_ref)],
            },
            "layering": {
                "kind": "gap",
                "rationale": "Downstream planning owns implementation layering for this fixture.",
            },
            "dispatch_trace": {
                "techniques": ["sequence", "owner_boundary_check", "concrete_path_evidence"]
            },
            "distill": {
                "classification": "not-required",
                "rationale": "The fixture contains one narrow candidate definition unit.",
            },
            "identity_denominator": {
                "classification": "not-applicable",
                "rationale": "No canonical ID-to-label denominator is asserted.",
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
            "next_route": "deferred",
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def ref(path: Path, label: str) -> dict[str, object]:
        data = path.read_bytes()
        return {
            "path": label,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        }

    @staticmethod
    def definition(source_ref: dict[str, object]) -> dict[str, object]:
        return {
            "id": "DEMO-D1",
            "term": "candidate definition",
            "aliases": ["definition candidate"],
            "status": "candidate",
            "status_detail": None,
            "deferred_as": None,
            "supersedes": [],
            "superseded_by": None,
            "source_kinds": ["local-inference"],
            "voices": {
                "normative": "A proposed semantic unit bound to exact project evidence.",
                "formal": None,
                "operational": "Validate it before generating its human views.",
                "plain_language": "A proposed meaning that has not been promoted.",
                "domain_context": "Used only inside the demo candidate registry.",
            },
            "notation": [],
            "boundary": {
                "includes": ["Candidate semantic authoring."],
                "excludes": ["Promotion or runtime authority."],
                "conditions": [],
            },
            "source_refs": [
                {
                    "role": "evidence",
                    "path": source_ref["path"],
                    "visibility": "private",
                    "selector_type": "heading",
                    "selector": "Purpose",
                    "start_line": None,
                    "end_line": None,
                    "sha256": source_ref["sha256"],
                    "size": source_ref["size"],
                }
            ],
            "primary_consumers": ["DEFINITIONS.md", "GLOSSARY.md"],
            "relations": [],
            "use_carefully": None,
            "misuse_warning": None,
            "challenge_contract": None,
            "promotion_boundary": "Candidate only; definitions-governance owns promotion.",
            "drift_route": "definitions-governance",
            "definition_version": "1",
            "structural_schema": None,
        }

    def write(self, document: dict[str, object]) -> None:
        self.source.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def compile(self, document: dict[str, object], late=None):
        self.write(document)
        return MODULE.compile_source(
            self.source,
            self.output,
            self.repo,
            INVOKE / "schemas",
            late,
        )

    def assert_blocked_without_output(self, document: dict[str, object], pattern: str | None = None) -> None:
        self.write(document)
        context = self.assertRaisesRegex(ValueError, pattern) if pattern else self.assertRaises(ValueError)
        with context:
            MODULE.compile_source(
                self.source,
                self.output,
                self.repo,
                INVOKE / "schemas",
            )
        self.assertFalse(self.output.exists())

    def test_positive_is_atomic_deterministic_and_definition_bearing(self) -> None:
        receipt = self.compile(copy.deepcopy(self.base))
        self.assertEqual("pass", receipt["result"])
        self.assertEqual("none", receipt["authority_effect"])
        self.assertEqual(11, len(list(self.output.iterdir())))
        self.assertEqual(
            {
                "definitions",
                "definitions-view",
                "dispatch-trace",
                "distill",
                "glossary",
                "identity-denominator",
                "layering",
                "spec",
                "template-selection",
                "transport",
            },
            {item["kind"] for item in receipt["outputs"]},
        )
        artifact = json.loads((self.output / "DEFINITIONS.json").read_text(encoding="utf-8"))
        self.assertEqual("candidate", artifact["registry_status"])
        self.assertEqual("none", artifact["authority_effect"])
        self.assertEqual("candidate", artifact["definitions"][0]["status"])
        first = {path.name: path.read_bytes() for path in self.output.iterdir()}
        second = self.repo / "second"
        second_receipt = MODULE.compile_source(
            self.source,
            second,
            self.repo,
            INVOKE / "schemas",
        )
        self.assertEqual(first, {path.name: path.read_bytes() for path in second.iterdir()})
        self.assertEqual(receipt, second_receipt)

    def test_source_schema_negatives_leave_output_absent(self) -> None:
        cases = []
        document = copy.deepcopy(self.base)
        del document["definition_registry"]["definitions"][0]["voices"]["domain_context"]
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["voices"]["normative"] = "   "
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["status"] = "active"
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["glossary"] = []
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["source_refs"][0]["sha256"] = None
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["template_selection"]["profile_id"] = "invoke.generic-spec-baseline.v1"
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["output_contracts"]["definitions"] = "RECEIPT.json"
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["receipt_digest"] = "0" * 64
        cases.append(document)
        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["source_refs"][0]["path"] = (
            "https://example.invalid/definition.md"
        )
        cases.append(document)
        for index, document in enumerate(cases):
            with self.subTest(index=index):
                self.output = self.repo / f"schema-negative-{index}"
                self.assert_blocked_without_output(document, "source schema invalid")

    def test_semantic_negatives_leave_output_absent(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = []
        document = copy.deepcopy(self.base)
        duplicate = copy.deepcopy(document["definition_registry"]["definitions"][0])
        duplicate["term"] = "different term"
        duplicate["aliases"] = []
        document["definition_registry"]["definitions"].append(duplicate)
        cases.append(("duplicate definition id", document))

        document = copy.deepcopy(self.base)
        second = copy.deepcopy(document["definition_registry"]["definitions"][0])
        second["id"] = "DEMO-D2"
        second["term"] = "other term"
        second["aliases"] = [" Candidate   Definition "]
        document["definition_registry"]["definitions"].append(second)
        cases.append(("term or alias collision", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["aliases"] = [
            " Candidate   Definition "
        ]
        cases.append(("term or alias collision", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["relations"] = [
            {"id": "MISSING-D1", "type": "references"}
        ]
        cases.append(("relation target is unresolved", document))

        document = copy.deepcopy(self.base)
        reference = document["definition_registry"]["definitions"][0]["source_refs"][0]
        reference.update({"selector_type": "line-span", "selector": "lines 3-2", "start_line": 3, "end_line": 2})
        cases.append(("line-span selector is reversed", document))

        document = copy.deepcopy(self.base)
        reference = document["definition_registry"]["definitions"][0]["source_refs"][0]
        reference.update({"selector_type": "line-span", "selector": "lines 1-99", "start_line": 1, "end_line": 99})
        cases.append(("line-span selector ends after", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["visibility"] = "public"
        document["definition_registry"]["definitions"][0]["source_refs"][0]["visibility"] = "public"
        cases.append(("outside the public repository root", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["source_refs"][0]["sha256"] = "0" * 64
        cases.append(("source SHA-256 is stale", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["source_refs"][0]["size"] += 1
        cases.append(("source size is stale", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["relations"] = [
            {"id": "DEMO-D1", "type": "references"}
        ]
        cases.append(("has a self relation", document))

        document = copy.deepcopy(self.base)
        document["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "DEMO-SCHEMA",
            "status": "machine-checkable",
            "ref": "schemas/missing.schema.json",
        }
        cases.append(("structural schema is invalid", document))

        for index, (pattern, document) in enumerate(cases):
            with self.subTest(index=index, pattern=pattern):
                self.output = self.repo / f"semantic-negative-{index}"
                self.assert_blocked_without_output(document, pattern)

    def test_public_exact_source_under_public_root_passes(self) -> None:
        document = copy.deepcopy(self.base)
        public_ref = self.ref(self.public_discovery, "arcanum/discovery.md")
        document["discovery"]["ref"] = public_ref
        document["definition_registry"]["visibility"] = "public"
        reference = document["definition_registry"]["definitions"][0]["source_refs"][0]
        reference.update(
            {
                "path": public_ref["path"],
                "visibility": "public",
                "sha256": public_ref["sha256"],
                "size": public_ref["size"],
            }
        )
        receipt = self.compile(document)
        self.assertEqual("pass", receipt["result"])

    def test_late_failure_or_view_drift_is_atomic(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "late failure"):
            self.compile(
                copy.deepcopy(self.base),
                lambda _: (_ for _ in ()).throw(RuntimeError("late failure")),
            )
        self.assertFalse(self.output.exists())

        self.output = self.repo / "view-drift"

        def mutate(stage: Path) -> None:
            with (stage / "GLOSSARY.md").open("a", encoding="utf-8") as handle:
                handle.write("drift\n")

        with self.assertRaisesRegex(ValueError, "generated view drift"):
            self.compile(copy.deepcopy(self.base), mutate)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

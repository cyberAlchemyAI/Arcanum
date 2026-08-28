#!/usr/bin/env python3
"""Focused W0 validation for the additive Invoke Define v3 schema family.

This suite proves schema structure only. It intentionally does not claim
semantic-denominator completeness, digest freshness, cross-document equality,
scope narrowing, compiler determinism, atomic publication, consumer admission,
or generated-mirror parity.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


INVOKE_DIR = Path(__file__).resolve().parents[1]
SCHEMA_DIR = INVOKE_DIR / "schemas"
FIXTURE_DIR = (
    INVOKE_DIR
    / "development"
    / "define-v3-semantic-closure"
    / "fixtures"
    / "schema-family"
)
POSITIVE_FIXTURE_PATH = FIXTURE_DIR / "positive-family.json"
NEGATIVE_FIXTURE_PATH = FIXTURE_DIR / "negative-cases.json"

SCHEMA_FILES = {
    "semantic_context": "define-semantic-context-v1.schema.json",
    "semantic_closure_receipt": "define-semantic-closure-receipt-v1.schema.json",
    "definitions_artifact": "definitions-v2.schema.json",
    "define_source": "define-source-v3.schema.json",
    "profile": "define-profile-v3.schema.json",
    "result": "define-result-v3.schema.json",
}

DEPENDENCY_SCHEMA_FILES = {
    "definitions_v1": "definitions.schema.json",
}

FIXTURE_KEYS = {
    "semantic_context": "semantic_context",
    "semantic_closure_receipt": "semantic_closure_receipt",
    "definitions_artifact": "definitions_artifact",
    "define_source": "define_source",
    "profile": "profile",
    "result": "result",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def descend(document: Any, path: list[str | int]) -> Any:
    current = document
    for segment in path:
        current = current[segment]
    return current


def apply_mutation(document: dict, mutation: dict) -> None:
    operation = mutation["operation"]
    path = mutation["path"]
    if operation == "set":
        parent = descend(document, path[:-1])
        parent[path[-1]] = copy.deepcopy(mutation["value"])
        return
    if operation == "remove-last":
        descend(document, path).pop()
        return
    if operation == "remove":
        parent = descend(document, path[:-1])
        del parent[path[-1]]
        return
    raise AssertionError(f"unsupported fixture mutation: {operation}")


class DefineV3SchemaFamilyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            key: load_json(SCHEMA_DIR / filename)
            for key, filename in SCHEMA_FILES.items()
        }
        cls.dependency_schemas = {
            key: load_json(SCHEMA_DIR / filename)
            for key, filename in DEPENDENCY_SCHEMA_FILES.items()
        }
        cls.schema_store = {
            schema["$id"]: schema
            for schema in [*cls.schemas.values(), *cls.dependency_schemas.values()]
        }
        cls.family = load_json(POSITIVE_FIXTURE_PATH)
        cls.negative_cases = load_json(NEGATIVE_FIXTURE_PATH)

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

    def test_exact_six_schema_family_meta_validates(self) -> None:
        self.assertEqual(6, len(self.schemas))
        for schema in self.schemas.values():
            Draft202012Validator.check_schema(schema)

    def test_complete_positive_fixture_family_validates(self) -> None:
        for schema_key in FIXTURE_KEYS:
            with self.subTest(schema=schema_key):
                self.assert_valid(schema_key, self.fixture(schema_key))

    def test_structural_negative_fixture_matrix_rejects_every_case(self) -> None:
        self.assertEqual(33, len(self.negative_cases))
        for case in self.negative_cases:
            with self.subTest(case=case["case_id"]):
                schema_key = case["schema_key"]
                document = self.fixture(schema_key)
                mutations = case.get("mutations", [case.get("mutation")])
                for mutation in mutations:
                    apply_mutation(document, mutation)
                self.assert_invalid(schema_key, document)

    def test_all_reuse_definitions_artifact_is_reference_only_and_valid(self) -> None:
        document = self.fixture("definitions_artifact")
        document["definitions"] = []
        document["authority_bindings"] = [document["authority_bindings"][0]]
        document["semantic_applications"] = [document["semantic_applications"][0]]

        self.assertEqual("reuse-existing", document["semantic_applications"][0]["disposition"])
        self.assert_valid("definitions_artifact", document)

    def test_all_reuse_source_is_reference_only_and_valid(self) -> None:
        document = self.fixture("define_source")
        registry = document["definition_registry"]
        registry["definitions"] = []
        registry["authority_bindings"] = [registry["authority_bindings"][0]]
        document["semantic_applications"] = [document["semantic_applications"][0]]

        self.assertEqual([], registry["definitions"])
        self.assert_valid("define_source", document)

    def test_governance_required_is_a_valid_terminal_closure_outcome(self) -> None:
        document = self.fixture("semantic_closure_receipt")
        document["probe_results"][0]["disposition"] = "canonical-change-proposal"
        document["outcome"] = "definitions-governance-required"
        document["next_route"] = "definitions-governance"

        self.assert_valid("semantic_closure_receipt", document)

    def test_blocked_is_a_valid_terminal_closure_outcome(self) -> None:
        document = self.fixture("semantic_closure_receipt")
        blocker_id = "blocker:semantic-conflict"
        document["probe_results"][0]["disposition"] = "blocked-conflict"
        document["probe_results"][0]["causal_blocker_ids"] = [blocker_id]
        document["checks"][0]["status"] = "block"
        document["checks"][0]["causal_blocker_ids"] = [blocker_id]
        document["blockers"] = [
            {
                "blocker_id": blocker_id,
                "code": "SEMANTIC_CONFLICT",
                "message": "The declared concept conflicts with an existing authority.",
                "owner": "semantic-closure-owner",
                "repair_route": "Resolve the conflict and rerun semantic closure.",
            }
        ]
        document["outcome"] = "blocked"
        document["next_route"] = "stop"

        self.assert_valid("semantic_closure_receipt", document)

    def test_ready_closure_cannot_be_relabelled_as_governance_route(self) -> None:
        document = self.fixture("semantic_closure_receipt")
        document["next_route"] = "definitions-governance"
        self.assert_invalid("semantic_closure_receipt", document)

    def test_public_context_rejects_private_material_across_declared_boundary(self) -> None:
        visibility_paths = [
            ["discovery", "ref", "visibility"],
            ["concept_probes", 0, "evidence_refs", 0, "visibility"],
            ["authority_boundary", "canonical_source_refs", 0, "visibility"],
            ["authority_boundary", "index_refs", 0, "visibility"],
            ["authority_boundary", "resolution_evidence_refs", 0, "visibility"],
            ["adjacent_registries", 0, "source_ref", "visibility"],
            ["consumer_boundary", "consumers", 0, "source_ref", "visibility"],
        ]
        for path in visibility_paths:
            with self.subTest(path=path):
                document = self.fixture("semantic_context")
                apply_mutation(
                    document,
                    {"operation": "set", "path": path, "value": "private"},
                )
                self.assert_invalid("semantic_context", document)

    def test_closure_check_roster_is_complete_and_ordered(self) -> None:
        document = self.fixture("semantic_closure_receipt")
        document["checks"][0], document["checks"][1] = (
            document["checks"][1],
            document["checks"][0],
        )
        self.assert_invalid("semantic_closure_receipt", document)

    def test_result_requires_ordered_semantic_evidence_outputs(self) -> None:
        document = self.fixture("result")
        document["outputs"][0], document["outputs"][1] = (
            document["outputs"][1],
            document["outputs"][0],
        )
        self.assert_invalid("result", document)


if __name__ == "__main__":
    unittest.main(verbosity=2)

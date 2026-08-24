#!/usr/bin/env python3
"""Regression tests for Invoke package contracts and source re-grounding."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ONTOLOGY_ROOT = HERE.parent.parent
ARCANUM_ROOT = ONTOLOGY_ROOT.parents[1]
SCRIPT = ONTOLOGY_ROOT / "scripts" / "ontology_package.py"
PACKAGE = ARCANUM_ROOT / "ontology" / "invoke"
BUSINESS_NODES = PACKAGE / "nodes" / "business.json"
MIGRATION = PACKAGE / "migration" / "preserved-identities.json"
PUBLIC_CONTRACTS = ONTOLOGY_ROOT / "contracts" / "cav2-ontology-contracts.json"
V2_BINDING = "invoke-business-node/public-contract-v2"
CONCEPT_FIELDS = {"name", "role", "meaning", "plain_language"}


def load_module():
    spec = importlib.util.spec_from_file_location("ontology_package", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load ontology_package.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def mutated_errors(module, mutate) -> list[str]:
    with tempfile.TemporaryDirectory() as temporary_directory:
        package_copy = Path(temporary_directory) / "invoke"
        shutil.copytree(PACKAGE, package_copy)
        business = json.loads((package_copy / "nodes/business.json").read_text(encoding="utf-8"))
        migration = json.loads(
            (package_copy / "migration/preserved-identities.json").read_text(encoding="utf-8")
        )
        mutate(business, migration)
        write_json(package_copy / "nodes/business.json", business)
        write_json(package_copy / "migration/preserved-identities.json", migration)
        errors, _ = module.validate_ontology_package(package_copy, ARCANUM_ROOT)
        return errors


def mutated_package_errors(module, mutate) -> list[str]:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        package_copy = temporary_root / "invoke"
        repository_copy = temporary_root / "repository"
        shutil.copytree(PACKAGE, package_copy)
        sources = json.loads((package_copy / "sources.json").read_text(encoding="utf-8"))
        for source in sources["sources"]:
            locator = Path(source["locator"])
            destination = repository_copy / locator
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ARCANUM_ROOT / locator, destination)
        contract_locator = Path("arcana/ontology-vault/contracts/cav2-ontology-contracts.json")
        contract_destination = repository_copy / contract_locator
        contract_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ARCANUM_ROOT / contract_locator, contract_destination)
        mutate(package_copy, repository_copy)
        errors, _ = module.validate_ontology_package(package_copy, repository_copy)
        return errors


def assert_error(errors: list[str], fragment: str, case_id: str) -> None:
    assert any(fragment in error for error in errors), f"{case_id}: {errors}"


def main() -> None:
    module = load_module()
    errors, counts = module.validate_ontology_package(PACKAGE, ARCANUM_ROOT)
    assert errors == [], errors
    assert counts["business_nodes"] == 9

    business = json.loads(BUSINESS_NODES.read_text(encoding="utf-8"))
    assert len(business["nodes"]) == 9
    assert {node["model_binding"] for node in business["nodes"]} == {V2_BINDING}
    for node in business["nodes"]:
        concept = node["concept"]
        assert set(concept) == CONCEPT_FIELDS, node["id"]
        assert all(
            isinstance(concept[field], str) and concept[field].strip()
            for field in CONCEPT_FIELDS
        )
        assert concept["name"] == node["label"], node["id"]
        assert concept["role"] == node["role"], node["id"]

    public_contracts = json.loads(PUBLIC_CONTRACTS.read_text(encoding="utf-8"))
    shared_node_contract = next(
        contract for contract in public_contracts["model_contracts"] if contract["contract_id"] == "node"
    )
    assert {"label", "role"} <= set(shared_node_contract["required_fields"])

    cases = []

    def add_case(case_id, mutate, expected_error):
        cases.append((case_id, mutate, expected_error))

    add_case(
        "missing-concept",
        lambda document, migration: document["nodes"][0].pop("concept"),
        "concept must be an object",
    )
    add_case(
        "non-object-concept",
        lambda document, migration: document["nodes"][0].__setitem__("concept", "not-an-object"),
        "concept must be an object",
    )
    add_case(
        "extra-concept-key",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__("extra", "blocked"),
        "concept keys mismatch",
    )
    add_case(
        "blank-concept-meaning",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__("meaning", "  "),
        "concept.meaning must be a non-empty string",
    )
    add_case(
        "non-string-plain-language",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__("plain_language", []),
        "concept.plain_language must be a non-empty string",
    )
    add_case(
        "name-compatibility-drift",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__("name", "Different name"),
        "concept.name must equal",
    )
    add_case(
        "role-compatibility-drift",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__("role", "policy"),
        "concept.role must equal",
    )
    add_case(
        "mixed-v1-binding",
        lambda document, migration: document["nodes"][0].__setitem__(
            "model_binding", "invoke-business-node/public-contract-v1"
        ),
        "must use the v2 business-node contract",
    )
    add_case(
        "legacy-label-removed",
        lambda document, migration: document["nodes"][0].pop("label"),
        "business nodes[0] keys mismatch",
    )

    def unsupported_role(document, migration):
        document["nodes"][0]["role"] = "unsupported"
        document["nodes"][0]["concept"]["role"] = "unsupported"

    add_case("unsupported-role", unsupported_role, "not an allowed business role")
    add_case(
        "preserved-claim-drift",
        lambda document, migration: document["nodes"][0].__setitem__("claim", "Changed without a new source"),
        "does not preserve its frozen v1 projection",
    )
    add_case(
        "witness-order-drift",
        lambda document, migration: migration["schema_amendments"][0]["affected_node_ids"].reverse(),
        "does not preserve ordered node IDs",
    )
    add_case(
        "missing-witness",
        lambda document, migration: migration.__setitem__("schema_amendments", []),
        "must occur exactly once",
    )
    add_case(
        "duplicate-witness-id",
        lambda document, migration: migration["schema_amendments"].append(
            copy.deepcopy(migration["schema_amendments"][0])
        ),
        "must occur exactly once",
    )
    add_case(
        "authority-inflation",
        lambda document, migration: document["nodes"][0].__setitem__("authority_effect", "promotion"),
        "every node authority_effect must be none",
    )
    add_case(
        "private-path-leak",
        lambda document, migration: document["nodes"][0]["concept"].__setitem__(
            "plain_language", "See projects/private-source.md"
        ),
        "private or unrelated path fragment",
    )

    for case_id, mutate, expected_error in cases:
        assert_error(mutated_errors(module, mutate), expected_error, case_id)

    def insert_before_bound_source(package_copy, repository_copy):
        source_path = repository_copy / "spells/invoke/plan.md"
        source_path.write_text(
            "Inserted line that moves every selector.\n" + source_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    insertion_errors = mutated_package_errors(module, insert_before_bound_source)
    assert_error(insertion_errors, "source digest mismatch: SRC-PLAN", "source-insertion")
    assert_error(insertion_errors, "evidence selector slice digest mismatch", "source-insertion")

    def move_selector(package_copy, repository_copy):
        business_path = package_copy / "nodes/business.json"
        business_document = json.loads(business_path.read_text(encoding="utf-8"))
        business_document["nodes"][0]["evidence_refs"][0] = "SRC-ROOT#L1-L2"
        write_json(business_path, business_document)

    assert_error(
        mutated_package_errors(module, move_selector),
        "evidence selector binding inventory mismatch",
        "moved-selector",
    )

    def remove_identity_gate(package_copy, repository_copy):
        operations_path = package_copy / "extensions/operation-composition.json"
        operations_document = json.loads(operations_path.read_text(encoding="utf-8"))
        define = next(
            operation
            for operation in operations_document["operation_composition"]["operations"]
            if operation["id"] == "OP-DEFINE"
        )
        define["phases"] = [
            phase
            for phase in define["phases"]
            if phase["support"] != "invoke:define-identity-denominator-validator"
        ]
        write_json(operations_path, operations_document)

    assert_error(
        mutated_package_errors(module, remove_identity_gate),
        "Define identity-denominator gate is missing",
        "mandatory-define-gate",
    )

    def remove_plan_readiness_gate(package_copy, repository_copy):
        operations_path = package_copy / "extensions/operation-composition.json"
        operations_document = json.loads(operations_path.read_text(encoding="utf-8"))
        plan = next(
            operation
            for operation in operations_document["operation_composition"]["operations"]
            if operation["id"] == "OP-PLAN"
        )
        plan["phases"] = [
            phase
            for phase in plan["phases"]
            if phase["support"] != "CAP-IMPLEMENTATION-READINESS"
        ]
        write_json(operations_path, operations_document)

    assert_error(
        mutated_package_errors(module, remove_plan_readiness_gate),
        "Plan readiness capability binding is incomplete",
        "mandatory-plan-gate",
    )

    print("PASS Invoke package baseline validation")
    print("PASS all 9 business nodes expose the closed concept v2 contract")
    print("PASS compatibility aliases and frozen v1 projections cannot drift")
    print(f"PASS negative concept and migration cases: {len(cases)}")
    print("PASS selector insertion, moved-selector, and mandatory-gate drift fail closed")


if __name__ == "__main__":
    main()

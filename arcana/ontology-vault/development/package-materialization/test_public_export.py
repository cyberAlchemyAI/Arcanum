#!/usr/bin/env python3
"""Regression tests for the bounded CAV2 public-export contract."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ONTOLOGY_ROOT = HERE.parent.parent
SCRIPT = ONTOLOGY_ROOT / "scripts" / "ontology_package.py"
POLICY = ONTOLOGY_ROOT / "contracts" / "cav2-public-export-policy.json"
CONTRACTS = ONTOLOGY_ROOT / "contracts" / "cav2-ontology-contracts.json"


def load_module():
    spec = importlib.util.spec_from_file_location("ontology_package", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load ontology_package.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_module()
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    assert module.validate_public_export(policy, contracts) == []

    private_path = copy.deepcopy(contracts)
    private_path["public_provenance"]["source_path"] = "cyberAlchemy-v2/ontology/private.md"
    assert any("forbidden public path fragment" in error for error in module.validate_public_export(policy, private_path))

    extra_definition = copy.deepcopy(contracts)
    extra_definition["definitions"].append(
        {
            "origin_id": "CAV2-D999",
            "term": "not allowlisted",
            "artifact_class": "ontology-definition-contract",
            "public_contract": "should block",
            "authority_effect": "none",
        }
    )
    assert any("definition IDs" in error for error in module.validate_public_export(policy, extra_definition))

    authority_claim = copy.deepcopy(contracts)
    authority_claim["ontology_decides_authority"] = True
    assert any("does not decide authority" in error for error in module.validate_public_export(policy, authority_claim))

    forbidden_key = copy.deepcopy(contracts)
    forbidden_key["public_provenance"]["private_source_digest"] = "0" * 64
    assert any("forbidden public key" in error for error in module.validate_public_export(policy, forbidden_key))

    print(f"PASS public definitions allowlist: {len(policy['allowed_definition_ids'])}")
    print(f"PASS public model-contract allowlist: {len(policy['allowed_model_contract_ids'])}")
    print("PASS private paths, non-allowlisted IDs, authority claims, and private digests fail closed")


if __name__ == "__main__":
    main()

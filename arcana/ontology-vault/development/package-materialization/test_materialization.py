#!/usr/bin/env python3
"""Acceptance-critical regression tests for Ontology Vault materialization."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ONTOLOGY_ROOT = HERE.parent.parent
FIXTURES = HERE / "fixtures" / "materialization-cases.json"
SCRIPT = ONTOLOGY_ROOT / "scripts" / "ontology_package.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ontology_package", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load ontology_package.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    module = load_module()
    fixture = json.loads(FIXTURES.read_text(encoding="utf-8"))
    seen: set[str] = set()
    for case in fixture["cases"]:
        case_id = case["case_id"]
        assert case_id not in seen, f"duplicate case {case_id}"
        seen.add(case_id)
        decision = module.classify_materialization(case["request"])
        expected = case["expected"]
        assert decision["result"] == expected["result"], case_id
        assert decision["detected_triggers"] == expected["triggers"], case_id
        assert decision["blockers"] == expected["blockers"], case_id
        assert decision["authority_effect"] == "none", case_id
        assert decision["append_to_prior_run_artifact_allowed"] is False, case_id

    required = {
        "simple-one-off-map",
        "durable-bridge-package",
        "continued-enrichment-cannot-append-to-receipt",
        "public-package-visibility-unresolved",
    }
    assert required <= seen

    legacy_paths = [
        ONTOLOGY_ROOT.parents[2] / ".arcanum/ontology-vault/map-2026-08-20-invoke-business.json",
        ONTOLOGY_ROOT.parents[2] / ".arcanum/ontology-vault/map-2026-08-20-invoke-system.json",
        ONTOLOGY_ROOT.parents[2] / ".arcanum/ontology-vault/map-2026-08-20-invoke.json",
    ]
    before = {path: digest(path) for path in legacy_paths}
    enrichment_case = next(case for case in fixture["cases"] if case["case_id"] == "continued-enrichment-cannot-append-to-receipt")
    decision = module.classify_materialization(enrichment_case["request"])
    after = {path: digest(path) for path in legacy_paths}
    assert decision["result"] == "block"
    assert before == after, "classification changed legacy run-artifact bytes"

    skill = (ONTOLOGY_ROOT / "SKILL.md").read_text(encoding="utf-8")
    for required_text in (
        "<materialization-contract>",
        "single-artifact-allowed",
        "package-required",
        "package_owner_unresolved",
        "Never keep appending product ontology state",
    ):
        assert required_text in skill, f"SKILL.md missing {required_text}"

    print(f"PASS materialization cases: {len(fixture['cases'])}")
    print("PASS simple map remains a single run artifact")
    print("PASS durable, bridged, reusable, and evolving intent requires a package")
    print("PASS unresolved package ownership fails closed")
    print("PASS continued enrichment cannot mutate legacy run receipts")


if __name__ == "__main__":
    main()

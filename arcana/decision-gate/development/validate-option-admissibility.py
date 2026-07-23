#!/usr/bin/env python3
"""Validate Decision Gate option-admissibility routing and runtime parity."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def candidate_catalog() -> dict[str, dict[str, Any]]:
    base = {
        "label": "Candidate",
        "optionKind": "action",
        "structuralStatus": "admissible",
        "reversibility": "reversible",
        "hazardClass": "reversible",
        "ownerGate": None,
        "evidence": ["owner-validator:pass"],
        "rejectionReasons": [],
    }

    def item(option_id: str, **changes: Any) -> dict[str, Any]:
        return {**base, "optionId": option_id, **changes}

    return {
        "safe-action": item("safe-action"),
        "defer": item("defer", optionKind="defer"),
        "stop": item("stop", optionKind="stop"),
        "protected-owned": item(
            "protected-owned",
            hazardClass="publication",
            ownerGate="publication-owner",
        ),
        "protected-unowned": item(
            "protected-unowned",
            hazardClass="publication",
        ),
        "irreversible-unowned": item(
            "irreversible-unowned",
            reversibility="irreversible",
            hazardClass="other",
        ),
        "invalid-a": item(
            "invalid-a",
            structuralStatus="inadmissible",
            evidence=[],
            rejectionReasons=["missing required dependency"],
        ),
        "invalid-b": item(
            "invalid-b",
            structuralStatus="inadmissible",
            evidence=[],
            rejectionReasons=["target escapes scope"],
        ),
        "admissible-without-evidence": item(
            "admissible-without-evidence",
            evidence=[],
        ),
    }


def contract_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"incomplete frontmatter: {path}")
    return parts[2]


def main() -> int:
    canonical_dir = Path(__file__).resolve().parents[1]
    repository_root = canonical_dir.parents[2]
    resolver = load_module(
        "decision_gate_option_prefilter",
        canonical_dir / "scripts/prefilter-options.py",
    )
    request_schema = load_json(
        canonical_dir / "schemas/option-admissibility-request.schema.json"
    )
    receipt_schema = load_json(
        canonical_dir / "schemas/option-admissibility-receipt.schema.json"
    )
    fixtures = load_json(
        canonical_dir
        / "development/fixtures/option-admissibility-cases.json"
    )
    catalog = candidate_catalog()

    passed = 0
    for fixture in fixtures:
        request = {
            "schemaVersion": "1.0.0",
            "decisionId": fixture["id"],
            "candidates": [catalog[item] for item in fixture["candidates"]],
        }
        result = resolver.resolve_option_admissibility(
            request, request_schema
        )
        receipt_errors = list(
            Draft202012Validator(receipt_schema).iter_errors(result)
        )
        ok = (
            not receipt_errors
            and result["routeOutcome"] == fixture["expectedOutcome"]
            and result["admissibleOptionIds"]
            == fixture["expectedAdmissible"]
            and result["presentedOptionIds"]
            == fixture["expectedPresented"]
        )
        if fixture["expectedOutcome"] == "direct":
            ok = ok and result["directOptionId"] == fixture[
                "expectedAdmissible"
            ][0]
        if fixture["expectedOutcome"] == "gate":
            ok = ok and result["directOptionId"] is None
        if not ok:
            print(
                f"FAIL {fixture['id']}: "
                f"{json.dumps(result, sort_keys=True)}"
            )
            return 1
        passed += 1
        print(f"PASS {fixture['id']}: {result['routeOutcome']}")

    canonical_body = contract_body(canonical_dir / "SKILL.md")
    for runtime in (".agents", ".claude"):
        runtime_dir = repository_root / runtime / "skills/decision-gate"
        if contract_body(runtime_dir / "SKILL.md") != canonical_body:
            print(f"FAIL generated contract body drift: {runtime_dir}")
            return 1
        for relative in (
            "README.md",
            "schemas/option-admissibility-request.schema.json",
            "schemas/option-admissibility-receipt.schema.json",
            "schemas/override.schema.json",
            "schemas/override-consumption-request.schema.json",
            "schemas/override-consumption-receipt.schema.json",
            "scripts/prefilter-options.py",
            "scripts/consume-override.py",
        ):
            if (runtime_dir / relative).read_bytes() != (
                canonical_dir / relative
            ).read_bytes():
                print(
                    f"FAIL generated support drift: "
                    f"{runtime_dir / relative}"
                )
                return 1
    print(f"PASS option admissibility fixtures: {passed}/{len(fixtures)}")
    print("PASS canonical/Codex/Claude Decision Gate parity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

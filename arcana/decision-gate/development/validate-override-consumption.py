#!/usr/bin/env python3
"""Validate typed one-use Decision Gate override consumption."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
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


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def base_override() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "override_id": "override-001",
        "target": "decision:example",
        "scope": ["runtime/example.json"],
        "hazard_class": "reversible",
        "issuer": "maintainer",
        "rationale": "Exercise one bounded reversible route.",
        "issued_at": "2020-01-01T00:00:00Z",
        "expires_at": "2999-01-01T00:00:00Z",
        "owner_gate_receipt": None,
        "consumed_by": None,
    }


def base_request() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "run_id": "run-001",
        "target": "decision:example",
        "scope": ["runtime/example.json"],
        "hazard_class": "reversible",
    }


def mutate(
    override: dict[str, Any],
    request: dict[str, Any],
    mutation: str,
) -> None:
    if mutation in ("none", "replay"):
        return
    if mutation == "ambient-assent":
        override.clear()
        override["assent"] = "yes"
    elif mutation == "missing-target":
        del override["target"]
    elif mutation == "stale":
        override["expires_at"] = "2021-01-01T00:00:00Z"
    elif mutation == "target-mismatch":
        request["target"] = "decision:other"
    elif mutation == "scope-mismatch":
        request["scope"] = ["runtime/other.json"]
    elif mutation == "hazard-mismatch":
        request["hazard_class"] = "other"
    elif mutation == "protected-no-owner":
        override["hazard_class"] = "publication"
        request["hazard_class"] = "publication"
    elif mutation == "protected-free-form-owner":
        override["hazard_class"] = "publication"
        override["owner_gate_receipt"] = "receipts/untyped-owner.json"
        request["hazard_class"] = "publication"
    elif mutation == "already-consumed":
        override["consumed_by"] = "prior-run"
    else:
        raise ValueError(f"unknown mutation: {mutation}")


def main() -> int:
    canonical_dir = Path(__file__).resolve().parents[1]
    consumer = load_module(
        "decision_gate_override_consumer",
        canonical_dir / "scripts/consume-override.py",
    )
    override_schema = load_json(canonical_dir / "schemas/override.schema.json")
    request_schema = load_json(
        canonical_dir / "schemas/override-consumption-request.schema.json"
    )
    receipt_schema = load_json(
        canonical_dir / "schemas/override-consumption-receipt.schema.json"
    )
    fixtures = load_json(
        canonical_dir / "development/fixtures/override-consumption-cases.json"
    )
    observed_at = datetime(2026, 7, 23, tzinfo=timezone.utc)

    passed = 0
    with tempfile.TemporaryDirectory(
        prefix="decision-gate-override-"
    ) as temporary:
        root = Path(temporary)
        for fixture in fixtures:
            override = base_override()
            request = base_request()
            mutate(override, request, fixture["mutation"])
            override_path = root / f"{fixture['id']}.json"
            write_json(override_path, override)

            if fixture["mutation"] == "replay":
                first = consumer.consume_override(
                    override_path,
                    request,
                    request_schema,
                    override_schema,
                    observed_at,
                )
                if first["verdict"] != "consumed":
                    print(f"FAIL {fixture['id']}: setup did not consume")
                    return 1
                request["run_id"] = "run-002"

            before = override_path.read_bytes()
            result = consumer.consume_override(
                override_path,
                request,
                request_schema,
                override_schema,
                observed_at,
            )
            after = override_path.read_bytes()
            receipt_errors = list(
                Draft202012Validator(receipt_schema).iter_errors(result)
            )
            ok = not receipt_errors and result["verdict"] == fixture["expected"]
            if result["verdict"] == "block":
                ok = ok and before == after
            else:
                persisted = load_json(override_path)
                ok = (
                    ok
                    and before != after
                    and persisted["consumed_by"] == request["run_id"]
                    and result["consumed_by"] == request["run_id"]
                )
            if fixture["mutation"].startswith("protected"):
                ok = ok and result["owner_route_required"] is True
            if fixture["mutation"] == "replay":
                ok = (
                    ok
                    and load_json(override_path)["consumed_by"] == "run-001"
                )
            if not ok:
                print(
                    f"FAIL {fixture['id']}: "
                    f"{json.dumps(result, sort_keys=True)}"
                )
                return 1
            passed += 1
            print(f"PASS {fixture['id']}: {result['verdict']}")

    print(f"PASS override consumption fixtures: {passed}/{len(fixtures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

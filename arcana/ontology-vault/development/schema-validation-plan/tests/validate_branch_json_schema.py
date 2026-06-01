#!/usr/bin/env python3
"""Validate fixtures against the development-only branch ontology JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "branch-aware-ontology-candidate.schema.yml"
FIXTURES = ROOT / "fixtures"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run() -> int:
    schema = load_schema(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema)
    failures: list[str] = []

    for path in sorted((FIXTURES / "valid").glob("*.json")):
        if path.name == "index.json":
            continue
        errors = sorted(validator.iter_errors(load_json(path)), key=lambda item: item.json_path)
        if errors:
            summary = "; ".join(f"{error.json_path}: {error.message}" for error in errors[:3])
            failures.append(f"VALID fixture failed {path.name}: {summary}")

    for path in sorted((FIXTURES / "invalid").glob("*.json")):
        if path.name == "index.json":
            continue
        errors = list(validator.iter_errors(load_json(path)))
        if not errors:
            failures.append(f"INVALID fixture unexpectedly passed {path.name}")

    if failures:
        print("branch-json-schema-fixtures: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("branch-json-schema-fixtures: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(run())

#!/usr/bin/env python3
"""Validate typed pre-execution prerequisite fixtures deterministically."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = {
    "prerequisite": ROOT / "schemas" / "pre-execution-owner-prerequisite.schema.json",
    "receipt": ROOT / "schemas" / "pre-execution-prerequisite-receipt.schema.json",
}
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "schema-cases.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def set_pointer(document: Any, pointer: str, value: Any) -> None:
    parts = pointer_parts(pointer)
    target = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    leaf = parts[-1]
    if isinstance(target, list):
        target[int(leaf)] = value
    else:
        target[leaf] = value


def delete_pointer(document: Any, pointer: str) -> None:
    parts = pointer_parts(pointer)
    target = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    leaf = parts[-1]
    if isinstance(target, list):
        del target[int(leaf)]
    else:
        del target[leaf]


def materialize(case: dict[str, Any], by_id: dict[str, dict[str, Any]], stack: tuple[str, ...] = ()) -> Any:
    case_id = case["case_id"]
    if case_id in stack:
        raise ValueError(f"fixture inheritance cycle: {' -> '.join((*stack, case_id))}")
    if "document" in case:
        document = copy.deepcopy(case["document"])
    else:
        base_id = case.get("mutate_from")
        if not base_id or base_id not in by_id:
            raise ValueError(f"{case_id}: missing fixture base {base_id!r}")
        document = materialize(by_id[base_id], by_id, (*stack, case_id))
    for pointer, value in case.get("set", {}).items():
        set_pointer(document, pointer, copy.deepcopy(value))
    if "delete" in case:
        delete_pointer(document, case["delete"])
    return document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=["schema"], default="schema")
    args = parser.parse_args()
    del args

    schemas = {name: load_json(path) for name, path in SCHEMAS.items()}
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    fixture_set = load_json(FIXTURES)
    cases = fixture_set["cases"]
    by_id = {case["case_id"]: case for case in cases}
    failures: list[str] = []
    for case in cases:
        document = materialize(case, by_id)
        errors = sorted(
            Draft202012Validator(schemas[case["schema"]]).iter_errors(document),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        observed_valid = not errors
        if observed_valid != case["valid"]:
            detail = "valid" if observed_valid else "; ".join(error.message for error in errors[:3])
            failures.append(f"{case['case_id']}: expected valid={case['valid']}, observed {detail}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS schema fixtures: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

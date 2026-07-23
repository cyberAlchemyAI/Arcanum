#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "schema-fixture-manifest.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def resolve_parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = pointer_parts(pointer)
    if not parts:
        raise ValueError("root mutation is not supported")
    node = document
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, parts[-1]


def apply_operations(base: Any, operations: list[dict[str, Any]]) -> Any:
    document = copy.deepcopy(base)
    for operation in operations:
        parent, key = resolve_parent(document, operation["path"])
        op = operation["op"]
        if isinstance(parent, list):
            index = int(key)
            if op == "remove":
                del parent[index]
            elif op in {"add", "replace"}:
                if op == "add" and index == len(parent):
                    parent.append(operation["value"])
                else:
                    parent[index] = operation["value"]
            else:
                raise ValueError(f"unsupported operation: {op}")
        elif op == "remove":
            del parent[key]
        elif op in {"add", "replace"}:
            parent[key] = operation["value"]
        else:
            raise ValueError(f"unsupported operation: {op}")
    return document


def instance_path(error: Any) -> str:
    if not error.absolute_path:
        return ""
    return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in error.absolute_path)


def normalize_error(error: Any) -> dict[str, str]:
    return {
        "validator": str(error.validator),
        "instance_path": instance_path(error),
        "message": error.message,
    }


def error_matches(error: dict[str, str], expected: dict[str, str]) -> bool:
    return (
        error["validator"] == expected["validator"]
        and error["instance_path"] == expected["instance_path"]
        and expected["message_contains"] in error["message"]
    )


def main() -> int:
    manifest = load_json(MANIFEST)
    schema_cache: dict[str, dict[str, Any]] = {}
    base_cache: dict[str, Any] = {}
    results: list[dict[str, Any]] = []

    for case in manifest["cases"]:
        schema_ref = case["schema"]
        if schema_ref not in schema_cache:
            schema = load_json((ROOT / schema_ref).resolve())
            Draft202012Validator.check_schema(schema)
            schema_cache[schema_ref] = schema
        base_ref = case["base"]
        if base_ref not in base_cache:
            base_cache[base_ref] = load_json((ROOT / base_ref).resolve())

        instance = apply_operations(base_cache[base_ref], case["operations"])
        validator = Draft202012Validator(schema_cache[schema_ref], format_checker=FormatChecker())
        errors = sorted(
            (normalize_error(error) for error in validator.iter_errors(instance)),
            key=lambda item: (item["instance_path"], item["validator"], item["message"]),
        )
        actual = "fail" if errors else "pass"
        expected_error = case.get("expected_error")
        matched_error = None
        if expected_error:
            matched_error = next((error for error in errors if error_matches(error, expected_error)), None)
        case_passes = actual == case["expected"] and (expected_error is None or matched_error is not None)
        matched_summary = None
        if matched_error is not None:
            matched_summary = {
                "validator": matched_error["validator"],
                "instance_path": matched_error["instance_path"],
                "message_contains": expected_error["message_contains"],
            }
        results.append(
            {
                "case_id": case["case_id"],
                "expected": case["expected"],
                "actual": actual,
                "result": "pass" if case_passes else "fail",
                "error_count": len(errors),
                "matched_error": matched_summary,
            }
        )

    overall = "pass" if all(result["result"] == "pass" for result in results) else "fail"
    report = {
        "schema_version": "whisper.editorial_schema_test_report.v0.1",
        "manifest": MANIFEST.name,
        "engine": "jsonschema.Draft202012Validator",
        "result": overall,
        "schema_count": len(schema_cache),
        "case_count": len(results),
        "expected_pass": sum(result["expected"] == "pass" for result in results),
        "expected_fail": sum(result["expected"] == "fail" for result in results),
        "passed": sum(result["result"] == "pass" for result in results),
        "failed": sum(result["result"] == "fail" for result in results),
        "cases": results,
    }
    print(json.dumps(report, indent=2) + "\n", end="")
    return 0 if overall == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())

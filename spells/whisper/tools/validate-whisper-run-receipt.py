#!/usr/bin/env python3
"""Validate a Whisper editorial run receipt and compute its final-status ceiling."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


EVALUATOR_VERSION = "0.1.0"
STRICTNESS = {"pass": 0, "flag": 1, "block": 2}
DEFAULT_SCHEMA = Path(__file__).resolve().parents[1] / "schemas/editorial-run-receipt.schema.json"
FIXTURE_MANIFEST = "status-ceiling-fixtures.json"


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


def json_pointer(parts: Any) -> str:
    values = list(parts)
    if not values:
        return ""
    return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in values)


def normalize_schema_error(error: Any) -> dict[str, str]:
    return {
        "validator": str(error.validator),
        "instance_path": json_pointer(error.absolute_path),
        "message": error.message,
    }


def stricter(left: str, right: str) -> str:
    return left if STRICTNESS[left] >= STRICTNESS[right] else right


def add_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def apply_axis_status(
    ceiling: str,
    reasons: list[str],
    status: str,
    missing_reason: str,
    flag_reason: str,
    block_reason: str,
) -> str:
    if status == "block":
        add_reason(reasons, block_reason)
        return stricter(ceiling, "block")
    if status == "flag":
        add_reason(reasons, flag_reason)
        return stricter(ceiling, "flag")
    if status == "absent":
        add_reason(reasons, missing_reason)
        return stricter(ceiling, "flag")
    return ceiling


def evaluate_receipt(receipt: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(
        (normalize_schema_error(error) for error in validator.iter_errors(receipt)),
        key=lambda item: (item["instance_path"], item["validator"], item["message"]),
    )
    if schema_errors:
        return {
            "schema_valid": False,
            "status_ceiling": "block",
            "final_status": "block",
            "reasons": ["invalid-evidence-envelope"],
            "schema_errors": schema_errors,
        }

    ceiling = "pass"
    reasons: list[str] = []
    transport = receipt["transport_profile"]
    axes = receipt["evidence_axes"]

    proof_status = transport["proof_status"]
    if proof_status == "candidate":
        ceiling = stricter(ceiling, "flag")
        add_reason(reasons, "transport-proof-candidate")
    elif proof_status == "unproven":
        ceiling = stricter(ceiling, "flag")
        add_reason(reasons, "transport-proof-unproven")

    if transport["editorial_approval_required"]:
        ceiling = apply_axis_status(
            ceiling,
            reasons,
            axes["editorial_language_audition"]["status"],
            "editorial-audition-required",
            "editorial-audition-flagged",
            "editorial-audition-blocked",
        )

    comprehension_required = (
        receipt["audience"]["mode"] == "newcomer"
        and transport["comprehension_gate"]["required"]
    )
    if comprehension_required:
        ceiling = apply_axis_status(
            ceiling,
            reasons,
            axes["operator_or_reader_comprehension"]["status"],
            "comprehension-required",
            "comprehension-flagged",
            "comprehension-blocked",
        )

    if transport["post_apply_review_required"]:
        ceiling = apply_axis_status(
            ceiling,
            reasons,
            receipt["post_apply_editorial_verification"]["status"],
            "post-apply-review-required",
            "post-apply-review-flagged",
            "post-apply-review-blocked",
        )

    if receipt["correction_refs"]:
        ceiling = stricter(ceiling, "flag")
        add_reason(reasons, "open-correction-invalidates-receipt")

    source_status = axes["source_and_structure_validation"]["status"]
    if source_status == "flag":
        ceiling = stricter(ceiling, "flag")
        add_reason(reasons, "source-structure-flagged")
    elif source_status == "block":
        ceiling = stricter(ceiling, "block")
        add_reason(reasons, "source-structure-blocked")

    render_status = axes["implementation_render_validation"]["status"]
    if render_status == "flag":
        ceiling = stricter(ceiling, "flag")
        add_reason(reasons, "implementation-render-flagged")
    elif render_status == "block":
        ceiling = stricter(ceiling, "block")
        add_reason(reasons, "implementation-render-blocked")

    if receipt["computed_decisions"]["generation"]["decision"] == "block":
        ceiling = stricter(ceiling, "block")
        add_reason(reasons, "generation-admission-blocked")

    requested_status = receipt["requested"]["status"]
    final_status = stricter(requested_status, ceiling)
    if STRICTNESS[requested_status] > STRICTNESS[ceiling]:
        add_reason(reasons, f"requested-status-{requested_status}")

    return {
        "schema_valid": True,
        "status_ceiling": ceiling,
        "final_status": final_status,
        "reasons": reasons,
        "schema_errors": [],
    }


def run_fixtures(fixtures: Path, schema: dict[str, Any]) -> tuple[dict[str, Any], int]:
    manifest_path = fixtures / FIXTURE_MANIFEST
    manifest = load_json(manifest_path)
    base_cache: dict[str, Any] = {}
    results: list[dict[str, Any]] = []

    for case in manifest["cases"]:
        base_ref = case["base"]
        if base_ref not in base_cache:
            base_cache[base_ref] = load_json((fixtures / base_ref).resolve())
        receipt = apply_operations(base_cache[base_ref], case["operations"])
        evaluation = evaluate_receipt(receipt, schema)
        actual = {
            "status_ceiling": evaluation["status_ceiling"],
            "final_status": evaluation["final_status"],
            "reasons": evaluation["reasons"],
        }
        case_passes = actual == case["expected"] and evaluation["schema_valid"] == case["schema_valid"]
        results.append(
            {
                "case_id": case["case_id"],
                "schema_valid": evaluation["schema_valid"],
                "status_ceiling": actual["status_ceiling"],
                "final_status": actual["final_status"],
                "reasons": actual["reasons"],
                "result": "pass" if case_passes else "fail",
                "schema_error_count": len(evaluation["schema_errors"]),
            }
        )

    overall = "pass" if all(result["result"] == "pass" for result in results) else "fail"
    candidate_case = next(
        result for result in results if result["case_id"] == "status-candidate-all-human-pass"
    )
    report = {
        "schema_version": "whisper.status_ceiling_test_report.v0.1",
        "evaluator_version": EVALUATOR_VERSION,
        "fixture_manifest": FIXTURE_MANIFEST,
        "result": overall,
        "case_count": len(results),
        "passed": sum(result["result"] == "pass" for result in results),
        "failed": sum(result["result"] == "fail" for result in results),
        "candidate_all_human_pass": {
            "status_ceiling": candidate_case["status_ceiling"],
            "final_status": candidate_case["final_status"],
            "reasons": candidate_case["reasons"],
        },
        "cases": results,
    }
    return report, 0 if overall == "pass" else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a typed Whisper run receipt and compute its final-status ceiling."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--receipt", type=Path, help="Validate and evaluate one run-receipt JSON file.")
    target.add_argument("--fixtures", type=Path, help="Run a status-ceiling fixture directory.")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Run-receipt JSON Schema path.")
    parser.add_argument("--version", action="version", version=EVALUATOR_VERSION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    schema = load_json(args.schema)
    Draft202012Validator.check_schema(schema)

    if args.fixtures:
        report, exit_code = run_fixtures(args.fixtures, schema)
        print(json.dumps(report, indent=2) + "\n", end="")
        return exit_code

    receipt = load_json(args.receipt)
    evaluation = evaluate_receipt(receipt, schema)
    result = {
        "schema_version": "whisper.status_ceiling_result.v0.1",
        "evaluator_version": EVALUATOR_VERSION,
        "receipt": str(args.receipt),
        **evaluation,
    }
    print(json.dumps(result, indent=2) + "\n", end="")
    return 0 if evaluation["schema_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())

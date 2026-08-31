#!/usr/bin/env python3
"""Validate the staged production governance evaluator against live policy cases."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REQUEST_SCHEMA_VERSION = "task-session.governance-evaluation-request.v1"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {path}")
    return document


def exact_ref(path: Path, display_path: str) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": display_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        error.message
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def run_evaluator(
    evaluator: Path,
    request_path: Path,
    policy_path: Path,
    request_schema_path: Path,
    receipt_schema_path: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(evaluator),
            "--request",
            str(request_path),
            "--policy",
            str(policy_path),
            "--request-schema",
            str(request_schema_path),
            "--receipt-schema",
            str(receipt_schema_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def build_request(
    request_id: str,
    kind: str,
    fixture_input: dict[str, Any],
    policy_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    return {
        "schema_version": REQUEST_SCHEMA_VERSION,
        "request_id": request_id,
        "evaluation_kind": kind,
        "policy_ref": exact_ref(policy_path, str(policy_path)),
        "input": fixture_input,
        "output_path": str(output_path),
    }


def assert_failed_closed(
    result: subprocess.CompletedProcess[str],
    output_path: Path,
    case_id: str,
    errors: list[str],
) -> None:
    if result.returncode == 0:
        errors.append(f"{case_id}: evaluator unexpectedly passed")
    if output_path.exists():
        errors.append(f"{case_id}: evaluator wrote a receipt while blocking")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-task-session-dir",
        help=(
            "Task Session source directory containing the live policy and golden "
            "fixtures; defaults to the staged/canonical directory of this validator"
        ),
    )
    args = parser.parse_args()

    staged_dir = Path(__file__).resolve().parents[1]
    source_dir = (
        Path(args.source_task_session_dir).resolve()
        if args.source_task_session_dir
        else staged_dir
    )
    evaluator = staged_dir / "scripts/evaluate-governance.py"
    request_schema_path = (
        staged_dir / "schemas/governance-evaluation-request.schema.json"
    )
    receipt_schema_path = (
        staged_dir / "schemas/governance-evaluation-receipt.schema.json"
    )
    fixture_manifest_path = (
        staged_dir / "development/fixtures/governance-evaluation-cases.json"
    )
    policy_path = (source_dir / "decision-validation-policy.json").resolve()
    golden_path = (
        source_dir / "development/fixtures/decision-validation-cases.json"
    ).resolve()

    request_schema = load_json(request_schema_path)
    receipt_schema = load_json(receipt_schema_path)
    manifest = load_json(fixture_manifest_path)
    golden = load_json(golden_path)
    errors: list[str] = []
    parity_rows: list[dict[str, str]] = []
    negative_rows: list[dict[str, str]] = []
    undeclared_outputs: list[str] = []

    expected_golden_ref = manifest["golden_source"]
    actual_golden_ref = exact_ref(golden_path, expected_golden_ref["path"])
    for field in ("sha256", "size_bytes"):
        if actual_golden_ref[field] != expected_golden_ref[field]:
            errors.append(f"golden source {field} drift")
    if len(golden.get("cases", [])) != expected_golden_ref["expected_case_count"]:
        errors.append("golden source case count drift")

    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        for index, case in enumerate(golden.get("cases", [])):
            case_dir = temporary_root / f"golden-{index:03d}"
            case_dir.mkdir()
            request_path = case_dir / "request.json"
            output_path = case_dir / "receipt.json"
            request = build_request(
                case["id"],
                case["kind"],
                case["input"],
                policy_path,
                output_path,
            )
            request_path.write_text(
                json.dumps(request, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            result = run_evaluator(
                evaluator,
                request_path,
                policy_path,
                request_schema_path,
                receipt_schema_path,
            )
            actual = None
            if result.returncode != 0:
                errors.append(
                    f"{case['id']}: evaluator blocked: {result.stderr.strip()}"
                )
            elif not output_path.is_file():
                errors.append(f"{case['id']}: receipt missing")
            else:
                receipt = load_json(output_path)
                receipt_errors = schema_errors(receipt, receipt_schema)
                if receipt_errors:
                    errors.append(
                        f"{case['id']}: receipt schema invalid: "
                        + "; ".join(receipt_errors)
                    )
                actual = receipt.get("outcome")
                if actual != case["expected"]:
                    errors.append(
                        f"{case['id']}: expected {case['expected']}, got {actual}"
                    )
            parity_rows.append(
                {
                    "id": case["id"],
                    "expected": case["expected"],
                    "actual": str(actual),
                    "result": "pass" if actual == case["expected"] else "block",
                }
            )
            unexpected = sorted(
                str(path.relative_to(case_dir))
                for path in case_dir.iterdir()
                if path not in {request_path, output_path}
            )
            undeclared_outputs.extend(
                f"{case['id']}:{path}" for path in unexpected
            )

        negative_base = build_request(
            "negative-base",
            "automatic-choice",
            {
                "consequence": "nonconsequential",
                "reversibility": "reversible",
            },
            policy_path,
            temporary_root / "unused-receipt.json",
        )
        for index, case in enumerate(manifest["negative_cases"]):
            case_dir = temporary_root / f"negative-{index:03d}"
            case_dir.mkdir()
            request_path = case_dir / "request.json"
            output_path = case_dir / "receipt.json"
            request = copy.deepcopy(negative_base)
            request["request_id"] = case["id"]
            request["output_path"] = str(output_path)
            run_policy_path = policy_path

            mutation = case["mutation"]
            if mutation == "remove-output-path":
                del request["output_path"]
            elif mutation == "replace-policy-digest":
                request["policy_ref"]["sha256"] = "0" * 64
            elif mutation == "replace-evaluation-kind":
                request["evaluation_kind"] = "unknown-kind"
            elif mutation == "replace-policy-outcome":
                invalid_policy = copy.deepcopy(load_json(policy_path))
                invalid_policy["automatic_choice"]["admitted_outcome"] = "EXPLODE"
                run_policy_path = case_dir / "invalid-policy.json"
                run_policy_path.write_text(
                    json.dumps(invalid_policy, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                request["policy_ref"] = exact_ref(
                    run_policy_path, str(run_policy_path)
                )
            elif mutation == "output-equals-request-path":
                request["output_path"] = str(request_path)
                output_path = request_path
            else:
                errors.append(f"{case['id']}: unknown negative mutation {mutation}")
                continue

            request_bytes = (
                json.dumps(request, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8")
            request_path.write_bytes(request_bytes)
            result = run_evaluator(
                evaluator,
                request_path,
                run_policy_path,
                request_schema_path,
                receipt_schema_path,
            )
            if mutation == "output-equals-request-path":
                if result.returncode == 0:
                    errors.append(f"{case['id']}: evaluator unexpectedly passed")
                if request_path.read_bytes() != request_bytes:
                    errors.append(f"{case['id']}: evaluator overwrote its request")
            else:
                assert_failed_closed(result, output_path, case["id"], errors)
            negative_rows.append(
                {
                    "id": case["id"],
                    "expected": "BLOCK",
                    "actual": "BLOCK" if result.returncode != 0 else "PASS",
                    "result": "pass" if result.returncode != 0 else "block",
                }
            )
            allowed = {request_path}
            if run_policy_path.parent == case_dir:
                allowed.add(run_policy_path)
            unexpected = sorted(
                str(path.relative_to(case_dir))
                for path in case_dir.iterdir()
                if path not in allowed
            )
            undeclared_outputs.extend(
                f"{case['id']}:{path}" for path in unexpected
            )

    valid_request = build_request(
        "schema-positive",
        "validation",
        {"result": "passed"},
        policy_path,
        Path("/tmp/schema-positive-receipt.json"),
    )
    request_positive = not schema_errors(valid_request, request_schema)
    invalid_request = dict(valid_request)
    invalid_request["unexpected"] = True
    request_negative = bool(schema_errors(invalid_request, request_schema))
    valid_receipt = {
        "schema_version": "task-session.governance-evaluation-receipt.v1",
        "request_id": "schema-positive",
        "evaluation_kind": "validation",
        "policy_ref": exact_ref(policy_path, str(policy_path)),
        "input_sha256": "0" * 64,
        "outcome": "PASS",
        "allowed_outcomes": ["BLOCK", "FLAG", "PASS"],
        "evaluator_sha256": hashlib.sha256(evaluator.read_bytes()).hexdigest(),
        "diagnostics": [],
    }
    receipt_positive = not schema_errors(valid_receipt, receipt_schema)
    invalid_receipt = dict(valid_receipt)
    invalid_receipt["outcome"] = "PROCEED"
    receipt_negative = bool(schema_errors(invalid_receipt, receipt_schema))
    schema_results = [
        request_positive,
        request_negative,
        receipt_positive,
        receipt_negative,
    ]
    if not all(schema_results):
        errors.append("schema positive/negative discrimination failed")
    if undeclared_outputs:
        errors.extend(
            f"undeclared evaluator output: {item}" for item in undeclared_outputs
        )

    parity_passed = sum(row["result"] == "pass" for row in parity_rows)
    negative_passed = sum(row["result"] == "pass" for row in negative_rows)
    print(
        "RESULT "
        f"golden={parity_passed}/{len(parity_rows)} "
        f"negative={negative_passed}/{len(negative_rows)} "
        f"schema={sum(schema_results)}/{len(schema_results)} "
        f"undeclared_outputs={len(undeclared_outputs)}"
    )
    for row in parity_rows:
        print(
            f"PARITY {row['result'].upper()} {row['id']} "
            f"expected={row['expected']} actual={row['actual']}"
        )
    for row in negative_rows:
        print(
            f"NEGATIVE {row['result'].upper()} {row['id']} "
            f"expected={row['expected']} actual={row['actual']}"
        )
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(
        "RESIDUE existing development evaluator remains current authority until "
        "canonical apply; delegate or remove it in a later accepted SWU"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

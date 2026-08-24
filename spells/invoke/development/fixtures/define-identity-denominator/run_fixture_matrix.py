#!/usr/bin/env python3
"""Run public synthetic fixtures for Invoke Define identity validation."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


FIXTURE_DIR = Path(__file__).resolve().parent
INVOKE_DIR = FIXTURE_DIR.parents[2]
VALIDATOR_PATH = INVOKE_DIR / "scripts/define_identity_denominator_validator.py"
REQUEST_SCHEMA_PATH = (
    INVOKE_DIR / "schemas/define-identity-denominator-request.schema.json"
)
RESULT_SCHEMA_PATH = (
    INVOKE_DIR / "schemas/define-identity-denominator-result.schema.json"
)
MATRIX_PATH = FIXTURE_DIR / "fixture-matrix.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "define_identity_denominator_validator", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def markdown_table(rows: list[dict[str, str]]) -> str:
    body = "\n".join(
        f"| {row['id']} | {row['label']} |" for row in rows
    )
    return (
        "| Identifier | Display name |\n"
        "| --- | --- |\n"
        f"{body}\n"
    )


def mutate_rows(
    identities: list[dict[str, str]], mutation: str
) -> list[dict[str, str]]:
    rows = [dict(item) for item in identities]
    if mutation == "pair-swap":
        rows[0]["label"], rows[1]["label"] = rows[1]["label"], rows[0]["label"]
    elif mutation == "four-rotation":
        labels = [row["label"] for row in rows[:4]]
        for index in range(4):
            rows[index]["label"] = labels[(index + 1) % 4]
    elif mutation == "six-permutation":
        labels = [row["label"] for row in rows]
        for index in range(6):
            rows[index]["label"] = labels[(index + 1) % 6]
    elif mutation == "duplicate-id":
        rows.append(dict(rows[0]))
    elif mutation == "duplicate-label":
        rows[1]["label"] = rows[0]["label"]
    elif mutation == "missing-row":
        rows.pop()
    elif mutation == "extra-row":
        rows.append({"id": "ref-007", "label": "Centre"})
    return rows


def artifact_text(
    identities: list[dict[str, str]], mutation: str
) -> str:
    rows = mutate_rows(identities, mutation)
    table = markdown_table(rows)
    if mutation == "missing-section":
        return f"# Synthetic fixture\n\n## Different Identities\n\n{table}"
    if mutation == "ambiguous-section":
        return (
            f"# Synthetic fixture\n\n## Reference Identities\n\n{table}"
            f"\n## Reference Identities\n\n{table}"
        )
    if mutation == "missing-table":
        return (
            "# Synthetic fixture\n\n## Reference Identities\n\n"
            "No table is present.\n"
        )
    if mutation == "ambiguous-table":
        return (
            "# Synthetic fixture\n\n## Reference Identities\n\n"
            f"{table}\n{table}"
        )
    return f"# Synthetic fixture\n\n## Reference Identities\n\n{table}"


def write_authority(path: Path, identities: list[dict[str, str]]) -> None:
    lines = ["records:"]
    for item in identities:
        lines.extend(
            [
                f"  - key: {item['id']}",
                f"    name: {item['label']}",
                "    state: included",
            ]
        )
    lines.extend(
        [
            "  - key: ref-ignored",
            "    name: Ignored",
            "    state: excluded",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_corroborator(
    path: Path, identities: list[dict[str, str]], disagreement: bool
) -> None:
    items = [
        {"identifier": item["id"], "display": item["label"], "status": "current"}
        for item in identities
    ]
    if disagreement:
        items[2]["display"] = "Alternate"
    items.append(
        {"identifier": "ref-ignored", "display": "Ignored", "status": "retired"}
    )
    path.write_text(
        json.dumps({"catalog": {"items": items}}, indent=2) + "\n",
        encoding="utf-8",
    )


def request_document(
    artifact: Path,
    authority: Path,
    corroborator: Path,
    root: Path,
    mutation: str,
) -> dict[str, Any]:
    artifact_digest = sha256(artifact)
    authority_digest = sha256(authority)
    corroborator_digest = sha256(corroborator)
    stale = "0" * 64
    if mutation == "stale-artifact-digest":
        artifact_digest = stale
    if mutation == "stale-authority-digest":
        authority_digest = stale
    if mutation == "stale-corroborator-digest":
        corroborator_digest = stale
    return {
        "schema_version": "invoke.define-identity-denominator-request/v1",
        "request_id": "synthetic-public-fixture",
        "artifact": {
            "path": artifact.relative_to(root).as_posix(),
            "sha256": artifact_digest,
            "format": "markdown",
        },
        "selector": {
            "heading": "Reference Identities",
            "heading_level": 2,
            "id_column": "Identifier",
            "label_column": "Display name",
        },
        "authority_source": {
            "source_id": "synthetic-authority",
            "role": "authority",
            "path": authority.relative_to(root).as_posix(),
            "sha256": authority_digest,
            "format": "yaml",
            "collection_pointer": "/records",
            "fields": {"id": "key", "label": "name"},
            "filters": [{"field": "state", "equals": "included"}],
        },
        "corroborating_sources": [
            {
                "source_id": "synthetic-corroborator",
                "role": "corroborating",
                "path": corroborator.relative_to(root).as_posix(),
                "sha256": corroborator_digest,
                "format": "json",
                "collection_pointer": "/catalog/items",
                "fields": {"id": "identifier", "label": "display"},
                "filters": [{"field": "status", "equals": "current"}],
            }
        ],
        "coverage": "exact",
        "authority_effect": "none",
    }


def materialize_case(
    root: Path, identities: list[dict[str, str]], mutation: str
) -> Path:
    artifact = root / "artifacts/SPEC.md"
    authority = root / "data/authority.yaml"
    corroborator = root / "data/corroborating.json"
    request = root / "requests/identity.json"
    for path in (artifact, authority, corroborator, request):
        path.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(artifact_text(identities, mutation), encoding="utf-8")
    write_authority(authority, identities)
    write_corroborator(
        corroborator,
        identities,
        disagreement=mutation == "source-disagreement",
    )
    document = request_document(
        artifact, authority, corroborator, root, mutation
    )
    request.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return request


def validate_schema(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def forged_blank_pass_errors(
    positive_result: dict[str, Any], result_schema: dict[str, Any]
) -> list[str]:
    forged = json.loads(json.dumps(positive_result))
    for input_binding in [
        forged["request"],
        forged["schemas"]["request_schema"],
        forged["schemas"]["result_schema"],
    ]:
        input_binding["sha256"] = None
        input_binding["expected_sha256"] = None
    forged["inputs"] = {
        "artifact": None,
        "authority_source": None,
        "corroborating_sources": [],
    }
    forged["expected_count"] = 0
    forged["observed_count"] = 0
    forged["matched_count"] = 0
    forged["identities"] = []
    forged["diagnostics"] = []
    forged["verdict"] = "pass"
    return validate_schema(forged, result_schema)


def execute_case(
    case: dict[str, Any],
    identities: list[dict[str, str]],
    execution: str,
    request_schema: dict[str, Any],
    result_schema: dict[str, Any],
    validator: Any,
) -> tuple[int, dict[str, Any], list[str]]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="invoke-define-identity-") as temp:
        root = Path(temp)
        request = materialize_case(root, identities, case["mutation"])
        request_document_value = json.loads(request.read_text(encoding="utf-8"))
        errors.extend(
            f"request schema: {error}"
            for error in validate_schema(request_document_value, request_schema)
        )
        request_digest = (
            "0" * 64
            if case["mutation"] == "stale-request-digest"
            else sha256(request)
        )
        if execution == "cli":
            output = root / "results/receipt.json"
            command = [
                sys.executable,
                str(VALIDATOR_PATH),
                str(request),
                "--repository-root",
                str(root),
                "--request-schema",
                str(REQUEST_SCHEMA_PATH),
                "--result-schema",
                str(RESULT_SCHEMA_PATH),
                "--request-sha256",
                request_digest,
                "--request-schema-sha256",
                sha256(REQUEST_SCHEMA_PATH),
                "--result-schema-sha256",
                sha256(RESULT_SCHEMA_PATH),
                "--output",
                str(output),
            ]
            completed = subprocess.run(command, check=False, capture_output=True, text=True)
            exit_code = completed.returncode
            if not output.is_file():
                errors.append(
                    "CLI did not write its receipt: "
                    f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
                )
                result: dict[str, Any] = {}
            else:
                result = json.loads(output.read_text(encoding="utf-8"))
        else:
            result = validator.validate_request(
                request_path=request,
                repository_root=root,
                request_schema_path=REQUEST_SCHEMA_PATH,
                result_schema_path=RESULT_SCHEMA_PATH,
                request_sha256=request_digest,
                request_schema_sha256=sha256(REQUEST_SCHEMA_PATH),
                result_schema_sha256=sha256(RESULT_SCHEMA_PATH),
            )
            exit_code = 0 if result["verdict"] == "pass" else 1

        errors.extend(
            f"result schema: {error}"
            for error in validate_schema(result, result_schema)
        )
        diagnostic_codes = {
            item["code"] for item in result.get("diagnostics", [])
        }
        missing_codes = sorted(
            set(case["required_diagnostics"]) - diagnostic_codes
        )
        if exit_code != case["expected_exit"]:
            errors.append(
                f"exit {exit_code} != expected {case['expected_exit']}"
            )
        if result.get("matched_count") != case["expected_matched"]:
            errors.append(
                "matched_count "
                f"{result.get('matched_count')} != expected {case['expected_matched']}"
            )
        if missing_codes:
            errors.append(f"missing diagnostics: {missing_codes}")
        return exit_code, result, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--execution", choices=("direct", "cli"), default="direct")
    args = parser.parse_args()

    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    request_schema = json.loads(REQUEST_SCHEMA_PATH.read_text(encoding="utf-8"))
    result_schema = json.loads(RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(request_schema)
    Draft202012Validator.check_schema(result_schema)
    validator = load_validator()
    selected = [
        case
        for case in matrix["cases"]
        if not args.case_ids or case["id"] in args.case_ids
    ]
    if args.case_ids and len(selected) != len(set(args.case_ids)):
        available = sorted(case["id"] for case in matrix["cases"])
        print(f"unknown or duplicate case selector; available={available}", file=sys.stderr)
        return 2

    failures = 0
    positive_result: dict[str, Any] | None = None
    for case in selected:
        exit_code, result, errors = execute_case(
            case,
            matrix["identities"],
            args.execution,
            request_schema,
            result_schema,
            validator,
        )
        codes = sorted({item["code"] for item in result.get("diagnostics", [])})
        status = "PASS" if not errors else "FAIL"
        print(
            f"{status} {case['id']} validator_exit={exit_code} "
            f"verdict={result.get('verdict')} matched={result.get('matched_count')} "
            f"diagnostics={','.join(codes) or 'none'}"
        )
        for error in errors:
            print(f"  {error}")
        failures += bool(errors)
        if case["id"] == "positive-exact-set" and not errors:
            positive_result = result

    if positive_result is None:
        positive_case = next(
            case for case in matrix["cases"] if case["id"] == "positive-exact-set"
        )
        _, positive_result, positive_errors = execute_case(
            positive_case,
            matrix["identities"],
            "direct",
            request_schema,
            result_schema,
            validator,
        )
        if positive_errors:
            print("FAIL forged-blank-pass positive source receipt is invalid")
            for error in positive_errors:
                print(f"  {error}")
            failures += 1

    forged_errors = forged_blank_pass_errors(positive_result, result_schema)
    if forged_errors:
        print(
            "PASS forged-blank-pass schema_rejected=true "
            f"schema_errors={len(forged_errors)}"
        )
    else:
        print("FAIL forged-blank-pass schema_rejected=false")
        failures += 1
    print(f"fixture_summary total={len(selected)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

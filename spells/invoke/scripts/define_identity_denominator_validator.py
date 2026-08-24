#!/usr/bin/env python3
"""Validate an exact Markdown identity denominator from a generic request."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only on runtimes without YAML
    yaml = None


SCHEMA_VERSION = "invoke.define-identity-denominator-result/v1"
VALIDATOR_ID = "invoke-define-identity-denominator-validator"
VALIDATOR_VERSION = "1.0.0"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
DELIMITER_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def diagnostic(
    code: str,
    message: str,
    selector: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "selector": selector,
        "details": details or {},
    }


def binding(path: Path, expected_sha256: str | None) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": None,
        "expected_sha256": expected_sha256,
    }


def read_explicit_input(
    name: str,
    raw_path: str | Path,
    expected_sha256: str | None,
    diagnostics: list[dict[str, Any]],
) -> tuple[Path, bytes | None, dict[str, Any]]:
    path = Path(raw_path).resolve(strict=False)
    result = binding(path, expected_sha256)
    try:
        value = path.read_bytes()
    except (OSError, ValueError) as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_INPUT_READ_ERROR",
                f"cannot read {name}",
                name,
                {"path": str(path), "error": str(error)},
            )
        )
        return path, None, result
    actual = sha256_bytes(value)
    result["sha256"] = actual
    if expected_sha256 is not None and actual != expected_sha256:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_DIGEST_MISMATCH",
                f"{name} does not match the caller-bound SHA-256",
                name,
                {
                    "path": str(path),
                    "expected_sha256": expected_sha256,
                    "actual_sha256": actual,
                },
            )
        )
    return path, value, result


def normalized_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in {"", "."}
    ):
        raise ValueError(f"path is not a repository-relative input: {raw}")
    return str(path)


def resolve_in_root(repository_root: Path, raw: str) -> tuple[str, Path]:
    relative = normalized_relative_path(raw)
    root = repository_root.resolve()
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"path resolves outside repository root: {raw}") from error
    return relative, candidate


def repo_input_binding(
    source: dict[str, Any],
    path: Path,
    actual_sha256: str | None,
) -> dict[str, Any]:
    result = {
        "path": str(path),
        "sha256": actual_sha256,
        "expected_sha256": source["sha256"],
    }
    if "source_id" in source:
        result.update(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "format": source["format"],
                "collection_pointer": source["collection_pointer"],
                "fields": source["fields"],
                "filters": source["filters"],
            }
        )
    else:
        result["format"] = source["format"]
    return result


def read_repo_input(
    source: dict[str, Any],
    repository_root: Path,
    selector: str,
    diagnostics: list[dict[str, Any]],
) -> tuple[bytes | None, dict[str, Any]]:
    try:
        _, path = resolve_in_root(repository_root, source["path"])
    except ValueError as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_INPUT_PATH_INVALID",
                str(error),
                selector,
                {"path": source.get("path")},
            )
        )
        fallback = Path(repository_root) / str(source.get("path", "invalid"))
        return None, repo_input_binding(source, fallback, None)
    try:
        value = path.read_bytes()
    except OSError as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_INPUT_READ_ERROR",
                "cannot read request-bound repository input",
                selector,
                {"path": str(path), "error": str(error)},
            )
        )
        return None, repo_input_binding(source, path, None)
    actual = sha256_bytes(value)
    if actual != source["sha256"]:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_DIGEST_MISMATCH",
                "request-bound repository input SHA-256 is stale",
                selector,
                {
                    "path": str(path),
                    "expected_sha256": source["sha256"],
                    "actual_sha256": actual,
                },
            )
        )
    return value, repo_input_binding(source, path, actual)


def schema_errors(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> list[dict[str, str]]:
    return [
        {
            "path": "/".join(map(str, error.path)) or "<root>",
            "message": error.message,
        }
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def load_schema(
    name: str,
    value: bytes | None,
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        document = json.loads(value.decode("utf-8"))
        if not isinstance(document, dict):
            raise ValueError("schema root must be an object")
        Draft202012Validator.check_schema(document)
        return document
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
        SchemaError,
    ) as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SCHEMA_INVALID",
                f"{name} is not a valid Draft 2020-12 JSON Schema",
                name,
                {"error": str(error)},
            )
        )
        return None


def json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError("JSON Pointer must be empty or start with '/'")
    current = document
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise ValueError(f"JSON Pointer token is missing: {token}")
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit() or int(token) >= len(current):
                raise ValueError(f"JSON Pointer array index is invalid: {token}")
            current = current[int(token)]
        else:
            raise ValueError(f"JSON Pointer cannot traverse token: {token}")
    return current


def load_source_document(
    source: dict[str, Any],
    value: bytes | None,
    diagnostics: list[dict[str, Any]],
) -> Any:
    if value is None:
        return None
    try:
        text = value.decode("utf-8")
        if source["format"] == "json":
            return json.loads(text)
        if yaml is None:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_YAML_UNAVAILABLE",
                    "YAML input requires an available safe YAML loader",
                    source["source_id"],
                )
            )
            return None
        return yaml.safe_load(text)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SOURCE_INVALID",
                "identity source cannot be parsed",
                source["source_id"],
                {"format": source["format"], "error": str(error)},
            )
        )
        return None
    except Exception as error:
        if yaml is not None and isinstance(error, yaml.YAMLError):
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_SOURCE_INVALID",
                    "identity source cannot be parsed",
                    source["source_id"],
                    {"format": source["format"], "error": str(error)},
                )
            )
            return None
        raise


def json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    return left == right


def extract_source_identities(
    source: dict[str, Any],
    value: bytes | None,
    diagnostics: list[dict[str, Any]],
) -> dict[str, str]:
    document = load_source_document(source, value, diagnostics)
    if document is None:
        return {}
    try:
        collection = json_pointer(document, source["collection_pointer"])
    except ValueError as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SOURCE_INVALID",
                "identity source collection cannot be resolved",
                source["source_id"],
                {"pointer": source["collection_pointer"], "error": str(error)},
            )
        )
        return {}
    if not isinstance(collection, list):
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SOURCE_INVALID",
                "identity source collection must resolve to an array",
                source["source_id"],
                {"pointer": source["collection_pointer"]},
            )
        )
        return {}

    identities: dict[str, str] = {}
    labels: dict[str, str] = {}
    for index, item in enumerate(collection):
        item_selector = f"{source['source_id']}#{source['collection_pointer']}/{index}"
        if not isinstance(item, dict):
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_SOURCE_INVALID",
                    "identity source row must be an object",
                    item_selector,
                )
            )
            continue
        if not all(
            field["field"] in item
            and json_equal(item[field["field"]], field["equals"])
            for field in source["filters"]
        ):
            continue
        id_field = source["fields"]["id"]
        label_field = source["fields"]["label"]
        meta_id = item.get(id_field)
        label = item.get(label_field)
        if (
            not isinstance(meta_id, str)
            or not meta_id.strip()
            or not isinstance(label, str)
            or not label.strip()
        ):
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_SOURCE_INVALID",
                    "filtered identity rows require non-empty string ID and label fields",
                    item_selector,
                    {"id_field": id_field, "label_field": label_field},
                )
            )
            continue
        meta_id = meta_id.strip()
        label = label.strip()
        label_key = label.casefold()
        if meta_id in identities:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_DUPLICATE_ID",
                    "identity source contains a duplicate filtered ID",
                    item_selector,
                    {"source_id": source["source_id"], "id": meta_id},
                )
            )
            continue
        if label_key in labels:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_DUPLICATE_LABEL",
                    "identity source contains a duplicate filtered label",
                    item_selector,
                    {"source_id": source["source_id"], "label": label},
                )
            )
            continue
        identities[meta_id] = label
        labels[label_key] = meta_id
    if not identities:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SOURCE_INVALID",
                "identity source filter selected no valid identities",
                source["source_id"],
            )
        )
    return identities


def compare_sources(
    authority_id: str,
    authority: dict[str, str],
    corroborators: list[tuple[str, dict[str, str]]],
    diagnostics: list[dict[str, Any]],
) -> None:
    if not authority:
        return
    authority_ids = set(authority)
    for source_id, identities in corroborators:
        if not identities:
            continue
        source_ids = set(identities)
        missing = sorted(authority_ids - source_ids)
        extra = sorted(source_ids - authority_ids)
        label_mismatches = [
            {
                "id": meta_id,
                "authority_label": authority[meta_id],
                "corroborating_label": identities[meta_id],
            }
            for meta_id in sorted(authority_ids & source_ids)
            if authority[meta_id] != identities[meta_id]
        ]
        if missing or extra or label_mismatches:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_SOURCE_DISAGREEMENT",
                    "corroborating identity source disagrees with the declared authority source",
                    source_id,
                    {
                        "authority_source_id": authority_id,
                        "missing_ids": missing,
                        "extra_ids": extra,
                        "label_mismatches": label_mismatches,
                    },
                )
            )


def table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def parse_markdown_denominator(
    value: bytes | None,
    selector: dict[str, Any],
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if value is None:
        return []
    try:
        lines = value.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_TABLE_INVALID",
                "Markdown artifact is not valid UTF-8",
                selector["heading"],
                {"error": str(error)},
            )
        )
        return []

    level = selector["heading_level"]
    heading_pattern = re.compile(rf"^{'#' * level}\s+(.+?)\s*#*\s*$")
    end_pattern = re.compile(rf"^#{{1,{level}}}\s+")
    heading_indexes = [
        index
        for index, line in enumerate(lines)
        if (match := heading_pattern.match(line.strip()))
        and match.group(1).strip() == selector["heading"]
    ]
    if not heading_indexes:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SECTION_MISSING",
                "Markdown artifact does not contain the exact requested section",
                selector["heading"],
            )
        )
        return []
    if len(heading_indexes) != 1:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_SECTION_AMBIGUOUS",
                "Markdown artifact contains more than one requested section",
                selector["heading"],
                {"lines": [index + 1 for index in heading_indexes]},
            )
        )
        return []

    start = heading_indexes[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if end_pattern.match(lines[index].strip()):
            end = index
            break
    section = lines[start:end]

    tables: list[tuple[int, list[str], list[tuple[int, list[str]]]]] = []
    index = 0
    while index + 1 < len(section):
        header = table_cells(section[index])
        delimiter = table_cells(section[index + 1])
        if (
            header is not None
            and delimiter is not None
            and len(header) == len(delimiter)
            and header
            and all(DELIMITER_CELL_PATTERN.fullmatch(cell) for cell in delimiter)
        ):
            rows: list[tuple[int, list[str]]] = []
            cursor = index + 2
            while cursor < len(section):
                cells = table_cells(section[cursor])
                if cells is None:
                    break
                rows.append((start + cursor + 1, cells))
                cursor += 1
            tables.append((start + index + 1, header, rows))
            index = cursor
            continue
        index += 1

    if not tables:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_TABLE_MISSING",
                "requested section contains no Markdown table",
                selector["heading"],
            )
        )
        return []
    if len(tables) != 1:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_TABLE_AMBIGUOUS",
                "requested section must contain exactly one Markdown table",
                selector["heading"],
                {"header_lines": [table[0] for table in tables]},
            )
        )
        return []

    header_line, header, raw_rows = tables[0]
    id_column = selector["id_column"]
    label_column = selector["label_column"]
    if (
        len(set(header)) != len(header)
        or id_column not in header
        or label_column not in header
    ):
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_TABLE_INVALID",
                "Markdown table lacks unique requested ID and label columns",
                selector["heading"],
                {"header_line": header_line, "columns": header},
            )
        )
        return []
    if not raw_rows:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_TABLE_INVALID",
                "Markdown identity table has no data rows",
                selector["heading"],
            )
        )
        return []

    id_index = header.index(id_column)
    label_index = header.index(label_column)
    rows: list[dict[str, Any]] = []
    seen_ids: dict[str, int] = {}
    seen_labels: dict[str, int] = {}
    for line_number, cells in raw_rows:
        if len(cells) != len(header):
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_ROW_INVALID",
                    "Markdown table row cell count differs from its header",
                    selector["heading"],
                    {"row": line_number, "expected": len(header), "actual": len(cells)},
                )
            )
            continue
        meta_id = cells[id_index].strip()
        label = cells[label_index].strip()
        if not meta_id or not label:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_ROW_INVALID",
                    "Markdown identity rows require non-empty ID and label cells",
                    selector["heading"],
                    {"row": line_number},
                )
            )
            continue
        if meta_id in seen_ids:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_DUPLICATE_ID",
                    "Markdown denominator contains a duplicate ID",
                    selector["heading"],
                    {"id": meta_id, "first_row": seen_ids[meta_id], "row": line_number},
                )
            )
        else:
            seen_ids[meta_id] = line_number
        label_key = label.casefold()
        if label_key in seen_labels:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_DUPLICATE_LABEL",
                    "Markdown denominator contains a duplicate label",
                    selector["heading"],
                    {"label": label, "first_row": seen_labels[label_key], "row": line_number},
                )
            )
        else:
            seen_labels[label_key] = line_number
        rows.append({"id": meta_id, "label": label, "row": line_number})
    return rows


def compare_artifact(
    rows: list[dict[str, Any]],
    authority: dict[str, str],
    corroborators: list[tuple[str, dict[str, str]]],
    selector: dict[str, Any],
    diagnostics: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    observed_ids = {row["id"] for row in rows}
    expected_ids = set(authority)
    missing = sorted(expected_ids - observed_ids)
    extra = sorted(observed_ids - expected_ids)
    if authority and (missing or extra):
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_COVERAGE_MISMATCH",
                "Markdown denominator does not equal the authority identity set",
                selector["heading"],
                {"missing_ids": missing, "extra_ids": extra},
            )
        )

    identities = []
    matched = 0
    for row in rows:
        expected_label = authority.get(row["id"])
        authority_match = expected_label is not None and row["label"] == expected_label
        corroborating_matches = [
            {"source_id": source_id, "match": values.get(row["id"]) == row["label"]}
            for source_id, values in corroborators
        ]
        complete_match = authority_match and all(
            item["match"] for item in corroborating_matches
        )
        if complete_match:
            matched += 1
        else:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_MISMATCH",
                    "Markdown label does not match the exact ID identity across declared sources",
                    selector["heading"],
                    {
                        "row": row["row"],
                        "id": row["id"],
                        "actual_label": row["label"],
                        "authority_label": expected_label,
                        "corroborating_labels": {
                            source_id: values.get(row["id"])
                            for source_id, values in corroborators
                        },
                    },
                )
            )
        identities.append(
            {
                "id": row["id"],
                "label": row["label"],
                "row": row["row"],
                "expected_label": expected_label,
                "authority_match": authority_match,
                "corroborating_matches": corroborating_matches,
            }
        )
    return identities, matched


def base_result(
    request_binding: dict[str, Any],
    request_schema_binding: dict[str, Any],
    result_schema_binding: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "validator": {"id": VALIDATOR_ID, "version": VALIDATOR_VERSION},
        "request": request_binding,
        "schemas": {
            "request_schema": request_schema_binding,
            "result_schema": result_schema_binding,
        },
        "selector": None,
        "inputs": {
            "artifact": None,
            "authority_source": None,
            "corroborating_sources": [],
        },
        "expected_count": 0,
        "observed_count": 0,
        "matched_count": 0,
        "identities": [],
        "verdict": "block",
        "diagnostics": [],
        "authority_effect": "none",
    }


def validate_request(
    *,
    request_path: str | Path,
    repository_root: str | Path,
    request_schema_path: str | Path,
    result_schema_path: str | Path,
    request_sha256: str | None = None,
    request_schema_sha256: str | None = None,
    result_schema_sha256: str | None = None,
) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    root = Path(repository_root).resolve(strict=False)
    request_resolved = Path(request_path).resolve(strict=False)
    try:
        request_resolved.relative_to(root.resolve())
    except ValueError:
        diagnostics.append(
            diagnostic(
                "DEFINE_IDENTITY_INPUT_PATH_INVALID",
                "request must resolve inside the supplied repository root",
                "request",
                {"path": str(request_resolved), "repository_root": str(root)},
            )
        )
    _, request_bytes, request_input = read_explicit_input(
        "request", request_resolved, request_sha256, diagnostics
    )
    _, request_schema_bytes, request_schema_input = read_explicit_input(
        "request_schema", request_schema_path, request_schema_sha256, diagnostics
    )
    _, result_schema_bytes, result_schema_input = read_explicit_input(
        "result_schema", result_schema_path, result_schema_sha256, diagnostics
    )
    result = base_result(request_input, request_schema_input, result_schema_input)
    request_schema = load_schema(
        "request_schema", request_schema_bytes, diagnostics
    )
    result_schema = load_schema("result_schema", result_schema_bytes, diagnostics)

    request: dict[str, Any] | None = None
    if request_bytes is not None:
        try:
            parsed = json.loads(request_bytes.decode("utf-8"))
            if not isinstance(parsed, dict):
                raise ValueError("request root must be an object")
            request = parsed
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_REQUEST_INVALID",
                    "request is not a valid JSON object",
                    "request",
                    {"error": str(error)},
                )
            )

    if request is not None and request_schema is not None:
        failures = schema_errors(request, request_schema, "request")
        if failures:
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_REQUEST_INVALID",
                    "request does not satisfy its schema",
                    "request",
                    {"errors": failures},
                )
            )
            request = None

    if request is not None:
        source_ids = [
            request["authority_source"]["source_id"],
            *[
                source["source_id"]
                for source in request["corroborating_sources"]
            ],
        ]
        if len(source_ids) != len(set(source_ids)):
            diagnostics.append(
                diagnostic(
                    "DEFINE_IDENTITY_REQUEST_INVALID",
                    "authority and corroborating source IDs must be unique",
                    "request#/authority_source",
                    {"source_ids": source_ids},
                )
            )

        result["selector"] = {
            **request["selector"],
            "coverage": request["coverage"],
        }
        artifact_bytes, artifact_input = read_repo_input(
            request["artifact"], root, "artifact", diagnostics
        )
        authority_bytes, authority_input = read_repo_input(
            request["authority_source"], root, "authority_source", diagnostics
        )
        corroborating_bytes_and_inputs = [
            (
                source,
                *read_repo_input(
                    source,
                    root,
                    f"corroborating_sources/{index}",
                    diagnostics,
                ),
            )
            for index, source in enumerate(request["corroborating_sources"])
        ]
        result["inputs"] = {
            "artifact": artifact_input,
            "authority_source": authority_input,
            "corroborating_sources": [
                item[2] for item in corroborating_bytes_and_inputs
            ],
        }

        authority = extract_source_identities(
            request["authority_source"], authority_bytes, diagnostics
        )
        corroborators = [
            (
                source["source_id"],
                extract_source_identities(source, value, diagnostics),
            )
            for source, value, _ in corroborating_bytes_and_inputs
        ]
        compare_sources(
            request["authority_source"]["source_id"],
            authority,
            corroborators,
            diagnostics,
        )
        rows = parse_markdown_denominator(
            artifact_bytes, request["selector"], diagnostics
        )
        identities, matched = compare_artifact(
            rows,
            authority,
            corroborators,
            request["selector"],
            diagnostics,
        )
        result["expected_count"] = len(authority)
        result["observed_count"] = len(rows)
        result["matched_count"] = matched
        result["identities"] = identities

    result["diagnostics"] = diagnostics
    result["verdict"] = "pass" if not diagnostics else "block"
    if result_schema is not None:
        failures = schema_errors(result, result_schema, "result")
        if failures:
            result["verdict"] = "block"
            result["diagnostics"].append(
                diagnostic(
                    "DEFINE_IDENTITY_RECEIPT_SCHEMA_INVALID",
                    "validation result does not satisfy its bound result schema",
                    "result_schema",
                    {"errors": failures},
                )
            )
    return result


def valid_expected_digest(value: str) -> str:
    normalized = value.lower()
    if not SHA256_PATTERN.fullmatch(normalized):
        raise argparse.ArgumentTypeError(
            "expected SHA-256 must be 64 lowercase hexadecimal characters"
        )
    return normalized


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Validate a request-bound exact Markdown identity denominator."
    )
    parser.add_argument("request")
    parser.add_argument("--repository-root", required=True)
    parser.add_argument(
        "--request-schema",
        default=script_dir.parent
        / "schemas/define-identity-denominator-request.schema.json",
    )
    parser.add_argument(
        "--result-schema",
        default=script_dir.parent
        / "schemas/define-identity-denominator-result.schema.json",
    )
    parser.add_argument("--request-sha256", type=valid_expected_digest)
    parser.add_argument("--request-schema-sha256", type=valid_expected_digest)
    parser.add_argument("--result-schema-sha256", type=valid_expected_digest)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        result = validate_request(
            request_path=args.request,
            repository_root=args.repository_root,
            request_schema_path=args.request_schema,
            result_schema_path=args.result_schema,
            request_sha256=args.request_sha256,
            request_schema_sha256=args.request_schema_sha256,
            result_schema_sha256=args.result_schema_sha256,
        )
    except Exception as error:  # pragma: no cover - final machine failure boundary
        empty = binding(Path(args.request).resolve(strict=False), args.request_sha256)
        result = base_result(
            empty,
            binding(
                Path(args.request_schema).resolve(strict=False),
                args.request_schema_sha256,
            ),
            binding(
                Path(args.result_schema).resolve(strict=False),
                args.result_schema_sha256,
            ),
        )
        result["diagnostics"] = [
            diagnostic(
                "DEFINE_IDENTITY_INTERNAL_ERROR",
                "validator stopped on an unexpected internal error",
                "validator",
                {"error_type": type(error).__name__, "error": str(error)},
            )
        ]

    output = Path(args.output).resolve(strict=False)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except OSError as error:
        print(
            json.dumps(
                diagnostic(
                    "DEFINE_IDENTITY_OUTPUT_WRITE_ERROR",
                    "cannot write validation result",
                    "output",
                    {"path": str(output), "error": str(error)},
                ),
                sort_keys=True,
            )
        )
        return 2
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

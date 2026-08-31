#!/usr/bin/env python3
"""Project one validated Design input closure into the frozen scope manifest v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


PRODUCER_ID = "invoke-design-input-producer"
FIELD_ID = {
    "human_actors": "actor_id",
    "rendered_surfaces": "surface_id",
    "interfaces": "interface_id",
    "stores": "store_id",
    "queues": "queue_id",
    "writers": "writer_id",
    "normative_rules": "rule_id",
    "effects": "effect_id",
    "data_and_log_sinks": "sink_id",
    "deployment_targets": "deployment_id",
    "compatibility_boundaries": "boundary_id",
    "quality_claims": "claim_id",
    "acceptance_and_readiness_claims": "claim_id",
}


class ProjectionFailure(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionFailure(f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def normalized_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or raw != normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in ("", ".")
        or str(path) != normalized
    ):
        raise ProjectionFailure(f"unsafe repository-relative path: {raw}")
    return str(path)


def resolve_inside(repository_root: Path, raw: str) -> Path:
    relative = normalized_relative_path(raw)
    root = repository_root.resolve()
    candidate = root / relative
    cursor = candidate
    while cursor != root:
        if cursor.is_symlink():
            raise ProjectionFailure(f"symlink is unsupported: {raw}")
        cursor = cursor.parent
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ProjectionFailure(f"path resolves outside repository root: {raw}") from error
    if not candidate.exists():
        raise ProjectionFailure(f"missing projection input: {raw}")
    return candidate


def legacy_consumer_digest(path: Path) -> str:
    """Match the frozen extractor's file/directory digest contract exactly."""
    if path.is_symlink():
        raise ProjectionFailure(f"symlink is unsupported: {path}")
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir():
        members: list[dict[str, str]] = []
        for child in sorted(path.rglob("*")):
            if child.is_symlink():
                raise ProjectionFailure(f"symlink is unsupported: {child}")
            if child.is_file():
                members.append(
                    {
                        "path": child.relative_to(path).as_posix(),
                        "sha256": hashlib.sha256(child.read_bytes()).hexdigest(),
                    }
                )
        return canonical_digest(members)
    raise ProjectionFailure(f"projection root is not a file or directory: {path}")


def schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def included_input_ids(closure: dict[str, Any]) -> set[str]:
    conditional = {
        item["input_id"]: item["outcome"]
        for item in closure["conditional_input_resolutions"]
    }
    result: set[str] = set()
    for item in closure["input_catalog"]:
        if item["classification"] == "required":
            result.add(item["input_id"])
        elif item["classification"] == "conditional" and conditional.get(
            item["input_id"]
        ) == "included":
            result.add(item["input_id"])
    return result


def project_scope_manifest(
    closure: dict[str, Any],
    closure_receipt: dict[str, Any],
    repository_root: Path,
    manifest_schema: dict[str, Any],
    enforce_receipt_binding: bool = True,
) -> dict[str, Any]:
    if closure_receipt.get("verdict") != "pass":
        raise ProjectionFailure("input closure receipt is not passing")
    expected = closure_receipt.get("expected_manifest")
    if enforce_receipt_binding and not isinstance(expected, dict):
        raise ProjectionFailure("input closure receipt lacks expected manifest binding")

    catalog = {item["input_id"]: item for item in closure["input_catalog"]}
    selected_ids = included_input_ids(closure)
    selected = sorted(
        (catalog[input_id] for input_id in selected_ids),
        key=lambda item: (item["source_ref"]["path"], item["input_id"]),
    )

    roots = []
    for root in sorted(
        closure["discovery_boundary"]["roots"], key=lambda item: item["root_id"]
    ):
        path = normalized_relative_path(root["path"])
        roots.append(
            {
                "path": path,
                "digest": legacy_consumer_digest(resolve_inside(repository_root, path)),
            }
        )

    inclusions = [
        {
            "selector": item["selector"],
            "path": normalized_relative_path(item["source_ref"]["path"]),
            "digest": item["source_ref"]["sha256"],
        }
        for item in selected
    ]
    source_contracts = [
        {
            "source_id": item["input_id"],
            "selector": item["selector"],
            "path": normalized_relative_path(item["source_ref"]["path"]),
            "digest": item["source_ref"]["sha256"],
        }
        for item in selected
    ]

    approved_paths = {
        normalized_relative_path(item["path"])
        for item in closure["discovery_boundary"]["permitted_exclusions"]
    }
    exclusions = []
    for item in sorted(closure["exclusions"], key=lambda entry: entry["path"]):
        path = normalized_relative_path(item["path"])
        if path not in approved_paths:
            raise ProjectionFailure(f"exclusion is not boundary-approved: {path}")
        exclusions.append(
            {
                "selector": f"file:{path}",
                "reason": item["reason"],
                "evidence_ref": item["evidence_ref"]["path"],
            }
        )

    projected_signals: dict[str, list[dict[str, Any]]] = {}
    for field, id_field in FIELD_ID.items():
        records = []
        for authored in sorted(
            closure["scope_signals"][field], key=lambda item: item["signal_id"]
        ):
            source = catalog.get(authored["source_input_id"])
            if source is None or source["input_id"] not in selected_ids:
                raise ProjectionFailure(
                    f"scope signal source is not an included input: {authored['signal_id']}"
                )
            record = {
                key: value
                for key, value in authored.items()
                if key not in {"signal_id", "source_input_id"}
            }
            if id_field not in record:
                raise ProjectionFailure(
                    f"scope signal lacks manifest id field: {authored['signal_id']}"
                )
            record["source_selector"] = normalized_relative_path(
                source["source_ref"]["path"]
            )
            record["source_digest"] = source["source_ref"]["sha256"]
            records.append(record)
        projected_signals[field] = records

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_id": f"{closure['closure_id']}:scope-manifest:v1",
        "target_id": closure["target"]["id"],
        "target_footprint": {
            "roots": roots,
            "inclusions": inclusions,
            "exclusions": exclusions,
        },
        "source_contracts": source_contracts,
        **projected_signals,
        "unknowns": [],
        "input_digest": "0" * 64,
        "authored_by": PRODUCER_ID,
    }
    manifest["input_digest"] = canonical_digest(
        {key: value for key, value in manifest.items() if key != "input_digest"}
    )

    errors = schema_errors(manifest, manifest_schema)
    if errors:
        raise ProjectionFailure("manifest schema invalid: " + "; ".join(errors))
    if enforce_receipt_binding:
        assert isinstance(expected, dict)
        if manifest["manifest_id"] != expected["manifest_id"]:
            raise ProjectionFailure("manifest id differs from the independent receipt")
        if manifest["input_digest"] != expected["input_digest"]:
            raise ProjectionFailure("manifest digest differs from the independent receipt")
    return manifest


def atomic_write_json(path: Path, document: dict[str, Any]) -> None:
    if path.exists():
        raise ProjectionFailure(f"output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("closure", type=Path)
    parser.add_argument("closure_receipt", type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--manifest-schema", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    schema = args.manifest_schema or (
        Path(__file__).resolve().parent.parent
        / "schemas/design-scope-manifest.schema.json"
    )
    try:
        manifest = project_scope_manifest(
            load_json(args.closure),
            load_json(args.closure_receipt),
            args.repository_root,
            load_json(schema),
        )
        atomic_write_json(args.output, manifest)
    except (OSError, json.JSONDecodeError, ProjectionFailure) as error:
        print(f"BLOCK: {error}")
        return 1
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate bidirectional Inventory source and projection conformance."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ARRAY_MAP_FIELDS = {
    "by_type": "type",
    "by_tag": "tags",
    "by_source": "sources",
    "by_status": "status",
    "by_evidence_card": "evidence_card_ids",
    "by_evidence_set": "evidence_set_ids",
    "by_namespace": "namespace",
    "by_record_class": "record_class",
    "by_concept": "concepts",
}

FACET_MAP_NAMES = {"by_namespace", "by_record_class", "by_concept"}
DEFAULT_RECORD_CLASSES = {
    "research", "review", "invoke", "task-session", "maintenance", "runtime",
    "decision", "evidence", "synthesis",
}
FACET_TOKEN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

DEFAULT_CONFIG = {
    "schema_version": "inventory.projection-conformance.config.v1",
    "governed_sources": [
        {"root": "entries", "patterns": ["**/*.md"]},
        {"root": "wiki", "patterns": ["**/*.md"]},
        {"root": "lint", "patterns": ["**/*.md"]},
        {"root": "raw/manifests", "patterns": ["**/*.md"]},
    ],
    "human_indexed_prefixes": ["entries/", "wiki/", "queries/", "lint/"],
    "uncontrolled_tags": "warn",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def result(status: str, errors: list[str], warnings: list[str], **details: Any) -> dict[str, Any]:
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        **details,
    }


def fail_or_pass(errors: list[str]) -> str:
    return "fail" if errors else "pass"


def repository_root(inventory_root: Path, declared_root: str) -> Path:
    parts = PurePosixPath(declared_root).parts
    candidate = inventory_root
    for _ in parts:
        candidate = candidate.parent
    if (candidate / declared_root).resolve() == inventory_root.resolve():
        return candidate.resolve()
    return Path.cwd().resolve()


def contained_path(base: Path, relative: str, boundary: Path) -> tuple[Path | None, str | None]:
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(boundary)
    except ValueError:
        return None, f"path escapes repository boundary: {relative}"
    return candidate, None


def enumerate_sources(inventory_root: Path, config: dict[str, Any]) -> tuple[set[str], list[str]]:
    paths: set[str] = set()
    errors: list[str] = []
    for rule in config.get("governed_sources", []):
        root_value = rule.get("root")
        patterns = rule.get("patterns", [])
        if not isinstance(root_value, str) or not root_value:
            errors.append("governed source rule has no non-empty root")
            continue
        if not isinstance(patterns, list) or not patterns:
            errors.append(f"governed source rule has no patterns: {root_value}")
            continue
        root = inventory_root / root_value
        if not root.is_dir():
            errors.append(f"governed source root is missing: {root_value}")
            continue
        for pattern in patterns:
            if not isinstance(pattern, str) or not pattern:
                errors.append(f"governed source pattern is invalid under {root_value}")
                continue
            for candidate in root.glob(pattern):
                if candidate.is_file():
                    paths.add(candidate.relative_to(inventory_root).as_posix())
    return paths, errors


def under_governed_root(path: str, config: dict[str, Any]) -> bool:
    for rule in config.get("governed_sources", []):
        root = str(rule.get("root", "")).strip("/")
        if root and (path == root or path.startswith(root + "/")):
            return True
    return False


def embedded_source_id(path: Path) -> str | None:
    if path.suffix.lower() != ".md":
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    match = re.search(r"(?m)^id:\s*[\"']?([^\"'\n]+)", text[4:end])
    return match.group(1).strip() if match else None


def expected_maps(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    maps: dict[str, dict[str, Any]] = {"by_id": {}}
    maps.update({name: {} for name in ARRAY_MAP_FIELDS})
    for entry in entries:
        entry_id = entry.get("id")
        maps["by_id"][entry_id] = entry.get("path")
        for map_name, field in ARRAY_MAP_FIELDS.items():
            raw = entry.get(field, [])
            values = raw if isinstance(raw, list) else [raw]
            for value in values:
                if not isinstance(value, str) or not value:
                    continue
                bucket = maps[map_name].setdefault(value, [])
                if entry_id not in bucket:
                    bucket.append(entry_id)
    return maps


def validate_facets(
    entries: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    facet_config = config.get("facets", {})
    allowed_namespaces = set(facet_config.get("namespaces", []))
    allowed_classes = set(
        facet_config.get("record_classes", sorted(DEFAULT_RECORD_CLASSES))
    )
    faceted_count = 0
    for entry in entries:
        present = [
            field for field in ("namespace", "record_class", "concepts")
            if field in entry
        ]
        if not present:
            continue
        faceted_count += 1
        entry_id = entry.get("id")
        if len(present) != 3:
            errors.append(f"partial facet metadata: {entry_id}")
            continue
        namespace = entry.get("namespace")
        record_class = entry.get("record_class")
        concepts = entry.get("concepts")
        if not isinstance(namespace, str) or not FACET_TOKEN_RE.fullmatch(namespace):
            errors.append(f"invalid facet namespace: {entry_id}")
        elif allowed_namespaces and namespace not in allowed_namespaces:
            errors.append(f"unconfigured facet namespace: {entry_id}: {namespace}")
        if not isinstance(record_class, str) or not FACET_TOKEN_RE.fullmatch(record_class):
            errors.append(f"invalid facet record class: {entry_id}")
        elif record_class not in allowed_classes:
            errors.append(f"uncontrolled facet record class: {entry_id}: {record_class}")
        if (
            not isinstance(concepts, list)
            or not concepts
            or any(not isinstance(value, str) or not FACET_TOKEN_RE.fullmatch(value)
                   for value in concepts)
        ):
            errors.append(f"invalid facet concepts: {entry_id}")
        elif concepts != sorted(set(concepts)):
            errors.append(f"facet concepts are not unique and byte-sorted: {entry_id}")
        expected_path = f"entries/{namespace}/{record_class}/{entry_id}.md"
        if entry.get("path") != expected_path:
            errors.append(
                f"faceted path mismatch: {entry_id}: "
                f"{entry.get('path')} != {expected_path}"
            )
    return result(
        fail_or_pass(errors),
        errors,
        [],
        faceted_entry_count=faceted_count,
    )


def parse_human_rows(path: Path) -> tuple[dict[str, str], list[str]]:
    rows: dict[str, str] = {}
    errors: list[str] = []
    row_re = re.compile(
        r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|"
    )
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = row_re.match(line)
        if not match:
            continue
        label, target, entry_type = (part.strip() for part in match.groups())
        if label != target:
            errors.append(
                f"human row label/target mismatch at line {line_number}: {label} != {target}"
            )
        if target in rows:
            errors.append(f"duplicate human path at line {line_number}: {target}")
        rows[target] = entry_type
    return rows, errors


def controlled_tags(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return set(re.findall(r"(?m)^\|\s*`([^`]+)`\s*\|", path.read_text(encoding="utf-8")))


def validate(index_path: Path) -> dict[str, Any]:
    index_path = index_path.resolve()
    inventory_root = index_path.parent
    raw_index = index_path.read_bytes()
    index = json.loads(raw_index)
    config = (
        index.get("validation", {}).get("projection_conformance")
        or DEFAULT_CONFIG
    )
    repo_root = repository_root(inventory_root, index.get("inventory_root", ".arcanum/inventory"))
    entries = index.get("entries", [])
    entry_paths = [entry.get("path") for entry in entries]
    entry_ids = [entry.get("id") for entry in entries]

    source_paths, source_errors = enumerate_sources(inventory_root, config)
    machine_source_paths = {
        path for path in entry_paths
        if isinstance(path, str) and under_governed_root(path, config)
    }
    missing_rows = sorted(source_paths - machine_source_paths)
    orphan_rows = sorted(machine_source_paths - source_paths)
    source_errors.extend(f"source has no machine row: {path}" for path in missing_rows)
    source_errors.extend(f"machine row has no governed source: {path}" for path in orphan_rows)
    source_check = result(
        fail_or_pass(source_errors),
        source_errors,
        [],
        governed_source_count=len(source_paths),
        indexed_governed_source_count=len(machine_source_paths),
        missing_source_rows=missing_rows,
        orphan_machine_rows=orphan_rows,
    )

    identity_errors: list[str] = []
    if len(entry_ids) != len(set(entry_ids)):
        identity_errors.append("entry IDs are not unique")
    if len(entry_paths) != len(set(entry_paths)):
        identity_errors.append("entry paths are not unique")
    expected = expected_maps(entries)
    actual_by_id = index.get("indexes", {}).get("by_id", {})
    if actual_by_id != expected["by_id"]:
        identity_errors.append("by_id does not exactly equal entry ID/path pairs")
    embedded_checked = 0
    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str):
            continue
        candidate, boundary_error = contained_path(inventory_root, relative, repo_root)
        if boundary_error or candidate is None or not candidate.is_file():
            continue
        source_id = embedded_source_id(candidate)
        if source_id is not None:
            embedded_checked += 1
            if source_id != entry.get("id"):
                identity_errors.append(
                    f"embedded source ID mismatch for {relative}: "
                    f"{source_id} != {entry.get('id')}"
                )
    identity_check = result(
        fail_or_pass(identity_errors),
        identity_errors,
        [],
        entry_count=len(entries),
        embedded_source_ids_checked=embedded_checked,
    )

    facet_check = validate_facets(entries, config)

    existence_errors: list[str] = []
    for relative in entry_paths:
        if not isinstance(relative, str):
            existence_errors.append("indexed path is not a string")
            continue
        candidate, boundary_error = contained_path(inventory_root, relative, repo_root)
        if boundary_error:
            existence_errors.append(boundary_error)
        elif candidate is None or not candidate.is_file():
            existence_errors.append(f"indexed path is missing: {relative}")
    existence_check = result(
        fail_or_pass(existence_errors),
        existence_errors,
        [],
        indexed_path_count=len(entry_paths),
    )

    map_errors: list[str] = []
    actual_maps = index.get("indexes", {})
    facet_maps_active = (
        facet_check["faceted_entry_count"] > 0
        or any(name in actual_maps for name in FACET_MAP_NAMES)
    )
    for map_name, expected_map in expected.items():
        if map_name in FACET_MAP_NAMES and not facet_maps_active:
            continue
        if actual_maps.get(map_name) != expected_map:
            map_errors.append(f"derived map is not exact: {map_name}")
    map_check = result(
        fail_or_pass(map_errors),
        map_errors,
        [],
        checked_maps=list(expected),
    )

    human_errors: list[str] = []
    human_relative = index.get("human_index")
    if not isinstance(human_relative, str) or not human_relative:
        human_errors.append("human_index is not declared")
        human_rows: dict[str, str] = {}
    else:
        human_path, boundary_error = contained_path(inventory_root, human_relative, repo_root)
        if boundary_error:
            human_errors.append(boundary_error)
            human_rows = {}
        elif human_path is None or not human_path.is_file():
            human_errors.append(f"human index is missing: {human_relative}")
            human_rows = {}
        else:
            human_rows, parse_errors = parse_human_rows(human_path)
            human_errors.extend(parse_errors)
    prefixes = tuple(config.get("human_indexed_prefixes", []))
    represented = {
        entry["path"]: entry
        for entry in entries
        if isinstance(entry.get("path"), str) and entry["path"].startswith(prefixes)
    }
    missing_human = sorted(set(represented) - set(human_rows))
    extra_human = sorted(
        path for path in human_rows
        if path.startswith(prefixes) and path not in represented
    )
    human_errors.extend(f"machine row missing from human index: {path}" for path in missing_human)
    human_errors.extend(f"human row missing from machine index: {path}" for path in extra_human)
    for path, entry in represented.items():
        if path in human_rows and human_rows[path] != entry.get("type"):
            human_errors.append(
                f"human/machine type mismatch for {path}: "
                f"{human_rows[path]} != {entry.get('type')}"
            )
    human_check = result(
        fail_or_pass(human_errors),
        human_errors,
        [],
        represented_machine_rows=len(represented),
        human_rows=len(human_rows),
    )

    freshness_errors: list[str] = []
    enabled = [
        projection for projection in index.get("projections", [])
        if projection.get("enabled", True)
    ]
    source_digest = hashlib.sha256(raw_index).hexdigest()
    generated_at = index.get("generated_at")
    try:
        dt.datetime.fromisoformat(str(generated_at).replace("Z", "+00:00"))
    except ValueError:
        freshness_errors.append(f"generated_at is not ISO-8601: {generated_at}")
    for projection in enabled:
        projection_path = projection.get("path")
        metadata_path = projection.get("metadata")
        if projection.get("source") != "index.json":
            freshness_errors.append(f"projection source is not index.json: {projection_path}")
        if not isinstance(projection.get("purpose"), str) or not projection["purpose"]:
            freshness_errors.append(f"projection purpose is missing: {projection_path}")
        if projection.get("freshness") != "generated-from-current-index":
            freshness_errors.append(f"projection freshness policy is invalid: {projection_path}")
        if not isinstance(projection_path, str) or not isinstance(metadata_path, str):
            freshness_errors.append(f"projection path/metadata is missing: {projection_path}")
            continue
        artifact, artifact_boundary = contained_path(inventory_root, projection_path, repo_root)
        metadata, metadata_boundary = contained_path(inventory_root, metadata_path, repo_root)
        if artifact_boundary:
            freshness_errors.append(artifact_boundary)
            continue
        if metadata_boundary:
            freshness_errors.append(metadata_boundary)
            continue
        if artifact is None or not artifact.is_file():
            freshness_errors.append(f"projection artifact is missing: {projection_path}")
            continue
        if metadata is None or not metadata.is_file():
            freshness_errors.append(f"projection metadata is missing: {metadata_path}")
            continue
        try:
            projection_meta = json.loads(metadata.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            freshness_errors.append(f"projection metadata is invalid: {metadata_path}: {error}")
            continue
        if projection_meta.get("source_sha256") != source_digest:
            freshness_errors.append(f"projection source digest is stale: {projection_path}")
        if projection_meta.get("source_generated_at") != generated_at:
            freshness_errors.append(f"projection source timestamp is stale: {projection_path}")
        if projection_meta.get("projection_sha256") != sha256(artifact):
            freshness_errors.append(f"projection artifact digest is stale: {projection_path}")
    freshness_check = result(
        fail_or_pass(freshness_errors),
        freshness_errors,
        [],
        enabled_projection_count=len(enabled),
        source_sha256=source_digest,
        source_generated_at=generated_at,
    )

    tag_warnings: list[str] = []
    controlled = controlled_tags(inventory_root / "tags.md")
    if config.get("uncontrolled_tags", "warn") == "warn" and controlled:
        unknown = sorted({
            tag
            for entry in entries
            for tag in entry.get("tags", [])
            if tag not in controlled
        })
        tag_warnings.extend(f"uncontrolled tag: {tag}" for tag in unknown)
    tags_check = result(
        "pass",
        [],
        tag_warnings,
        controlled_tag_count=len(controlled),
        warning_count=len(tag_warnings),
    )

    checks = {
        "source_coverage": source_check,
        "identity": identity_check,
        "facet_admission": facet_check,
        "existence": existence_check,
        "derived_maps": map_check,
        "human_view": human_check,
        "freshness": freshness_check,
        "tags": tags_check,
    }
    overall = "pass" if all(item["status"] == "pass" for item in checks.values()) else "fail"
    return {
        "schema_version": "inventory.projection-conformance.report.v1",
        "overall": overall,
        "lookup_readiness": "ready" if overall == "pass" else "blocked",
        "index": str(index_path),
        "index_sha256": source_digest,
        "checks": checks,
        "failure_count": sum(len(item["errors"]) for item in checks.values()),
        "warning_count": sum(len(item["warnings"]) for item in checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index_json", nargs="?", default=".arcanum/inventory/index.json")
    parser.add_argument("--report", help="write the full structured report to this path")
    parser.add_argument("--json", action="store_true", help="print the full JSON report")
    args = parser.parse_args()

    try:
        report = validate(Path(args.index_json))
    except (OSError, json.JSONDecodeError, TypeError) as error:
        print(f"FAIL: projection conformance could not run: {error}", file=sys.stderr)
        return 1

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for name, check in report["checks"].items():
            print(
                f"{check['status'].upper()}: {name} "
                f"({len(check['errors'])} errors, {len(check['warnings'])} warnings)"
            )
        print(
            f"RESULT: {report['overall']} "
            f"(lookup_readiness={report['lookup_readiness']}, "
            f"failures={report['failure_count']}, warnings={report['warning_count']})"
        )
    return 0 if report["overall"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

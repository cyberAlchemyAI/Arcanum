#!/usr/bin/env python3
"""Validate x-ray visual component and pattern library YAML."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMPONENTS = ROOT / "library" / "components.yml"
DEFAULT_PATTERNS = ROOT / "library" / "patterns.yml"
DEFAULT_COMPONENT_SCHEMA = ROOT / "schemas" / "xray-component-library.schema.yml"
DEFAULT_PATTERN_SCHEMA = ROOT / "schemas" / "xray-pattern-library.schema.yml"


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top-level YAML must be an object: {path}")
    return data


def schema_payload(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    schema = data.get("schema")
    if not isinstance(schema, dict):
        raise ValueError(f"schema YAML must contain a schema object: {path}")
    return schema


def string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return []


def require_schema_list(schema: dict[str, Any], field: str) -> list[str]:
    value = schema.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"schema.{field} must be a list of strings")
    return value


def validate_collection(data: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    required_top_level = require_schema_list(schema, "required_top_level")
    required_artifact_fields = require_schema_list(schema, "required_artifact_fields")
    required_entry_fields = require_schema_list(schema, "required_entry_fields")
    collection_key = schema.get("collection_key")
    list_fields = set(require_schema_list(schema, "list_fields"))
    id_prefixes = tuple(require_schema_list(schema, "id_prefixes"))

    for field in required_top_level:
        if field not in data:
            errors.append(f"{label}: missing top-level field: {field}")

    artifact = data.get("artifact")
    if not isinstance(artifact, dict):
        errors.append(f"{label}: artifact must be an object")
    else:
        for field in required_artifact_fields:
            if field not in artifact:
                errors.append(f"{label}: artifact missing {field}")

    if not isinstance(collection_key, str):
        errors.append(f"{label}: schema.collection_key must be a string")
        return errors

    entries = data.get(collection_key)
    if not isinstance(entries, list) or not entries:
        errors.append(f"{label}: {collection_key} must be a non-empty list")
        return errors

    allowed_lanes = set(string_list(schema.get("allowed_lanes")))
    allowed_modes = set(string_list(schema.get("allowed_modes")))
    allowed_families = set(string_list(schema.get("allowed_families")))

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"{label}: {collection_key}[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: entry must be an object")
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            errors.append(f"{prefix}: missing id")
        elif not entry_id.startswith(id_prefixes):
            errors.append(f"{prefix}: id has unsupported prefix: {entry_id}")
        elif entry_id in seen_ids:
            errors.append(f"{prefix}: duplicate id: {entry_id}")
        else:
            seen_ids.add(entry_id)

        for field in required_entry_fields:
            if field not in entry:
                errors.append(f"{prefix}: missing {field}")
                continue
            if field in list_fields and not string_list(entry[field]):
                errors.append(f"{prefix}: {field} must be a non-empty string list")
            elif field not in list_fields and not isinstance(entry[field], str):
                errors.append(f"{prefix}: {field} must be a string")

        family = entry.get("family")
        if allowed_families and family not in allowed_families:
            errors.append(f"{prefix}: unsupported family: {family}")

        lanes = string_list(entry.get("intended_lane")) or string_list(entry.get("required_lanes"))
        for lane in lanes:
            if allowed_lanes and lane not in allowed_lanes:
                errors.append(f"{prefix}: unsupported lane: {lane}")

        for mode in string_list(entry.get("target_modes")):
            if allowed_modes and mode not in allowed_modes:
                errors.append(f"{prefix}: unsupported mode: {mode}")

    return errors


def validate_pattern_references(patterns: dict[str, Any], component_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for index, pattern in enumerate(patterns.get("patterns", [])):
        if not isinstance(pattern, dict):
            continue
        for component_id in string_list(pattern.get("recommended_components")):
            if component_id not in component_ids:
                errors.append(f"patterns: patterns[{index}]: unknown recommended component: {component_id}")
    return errors


def component_ids(components: dict[str, Any]) -> set[str]:
    return {
        entry["id"]
        for entry in components.get("components", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--components", type=Path, default=DEFAULT_COMPONENTS)
    parser.add_argument("--patterns", type=Path, default=DEFAULT_PATTERNS)
    parser.add_argument("--component-schema", type=Path, default=DEFAULT_COMPONENT_SCHEMA)
    parser.add_argument("--pattern-schema", type=Path, default=DEFAULT_PATTERN_SCHEMA)
    parser.add_argument("--components-only", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        component_schema = schema_payload(args.component_schema)
        components = load_yaml(args.components)
        errors.extend(validate_collection(components, component_schema, "components"))

        if not args.components_only:
            pattern_schema = schema_payload(args.pattern_schema)
            patterns = load_yaml(args.patterns)
            errors.extend(validate_collection(patterns, pattern_schema, "patterns"))
            errors.extend(validate_pattern_references(patterns, component_ids(components)))
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        print("XRAY_LIBRARY_VALIDATION=block")
        for error in errors:
            print(f"BLOCK: {error}")
        return 1

    print("XRAY_LIBRARY_VALIDATION=pass")
    print(f"COMPONENTS={args.components}")
    if not args.components_only:
        print(f"PATTERNS={args.patterns}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

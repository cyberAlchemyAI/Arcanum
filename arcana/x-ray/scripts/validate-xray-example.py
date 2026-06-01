#!/usr/bin/env python3
"""Validate a static x-ray example lane model and HTML artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "xray-lane-model.schema.yml"

REQUIRED_CONTROLS = {
    "toggle-surface",
    "toggle-flow",
    "toggle-deps",
    "toggle-risk",
}


class XrayHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data_lanes: list[str] = []
        self.input_ids: set[str] = set()
        self.remote_refs: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        if "data-lane" in attr_map:
            self.data_lanes.extend(attr_map["data-lane"].split())
        if tag == "input" and attr_map.get("id"):
            self.input_ids.add(attr_map["id"])
        for attr_name in ("src", "href"):
            ref = attr_map.get(attr_name)
            if ref and re.match(r"https?://", ref):
                self.remote_refs.append(ref)

    def handle_data(self, data: str) -> None:
        stripped = " ".join(data.split())
        if stripped:
            self.text_chunks.append(stripped)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top-level JSON must be an object: {path}")
    return data


def load_schema(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML schema: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top-level schema YAML must be an object: {path}")
    schema = data.get("schema")
    if not isinstance(schema, dict):
        raise ValueError(f"schema YAML must contain a schema object: {path}")
    return schema


def require_string_list(schema: dict[str, Any], field: str) -> list[str]:
    value = schema.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"schema.{field} must be a list of strings")
    return value


def validate_lanes(data: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top_level = require_string_list(schema, "required_top_level")
    required_lanes = set(require_string_list(schema, "required_lanes"))
    required_lane_fields = require_string_list(schema, "required_lane_fields")
    allowed_modes = set(require_string_list(schema, "allowed_modes"))
    allowed_renderer_levels = set(require_string_list(schema, "allowed_renderer_levels"))
    non_empty_evidence_except = set(require_string_list(schema, "non_empty_evidence_except"))

    for field in required_top_level:
        if field not in data:
            errors.append(f"missing top-level field: {field}")

    lanes = data.get("lanes")
    if not isinstance(lanes, dict):
        return ["lanes must be an object"]

    missing = sorted(required_lanes - set(lanes))
    if missing:
        errors.append(f"missing required lanes: {', '.join(missing)}")

    for lane_id in sorted(required_lanes & set(lanes)):
        lane = lanes[lane_id]
        if not isinstance(lane, dict):
            errors.append(f"{lane_id}: lane must be an object")
            continue
        for field in required_lane_fields:
            if field not in lane:
                errors.append(f"{lane_id}: missing {field}")
        handle = lane.get("handle")
        if not isinstance(handle, str) or not handle:
            errors.append(f"{lane_id}: missing handle")
        for field in ("evidence", "inference"):
            value = lane.get(field)
            if not isinstance(value, list):
                errors.append(f"{lane_id}: {field} must be a list")
                continue
            if field == "evidence" and lane_id not in non_empty_evidence_except and not value:
                errors.append(f"{lane_id}: evidence must not be empty")

    if data.get("renderer_level") not in allowed_renderer_levels:
        errors.append(f"renderer_level must be one of: {', '.join(sorted(allowed_renderer_levels))}")
    if data.get("mode") not in allowed_modes:
        errors.append("mode is missing or unsupported")
    return errors


def validate_html(path: Path) -> list[str]:
    errors: list[str] = []
    parser = XrayHTMLParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()

    missing_controls = sorted(REQUIRED_CONTROLS - parser.input_ids)
    if missing_controls:
        errors.append(f"missing layer controls: {', '.join(missing_controls)}")

    data_lane_set = set(parser.data_lanes)
    for required in ("surface", "flow", "risk_questions"):
        if required not in data_lane_set:
            errors.append(f"HTML missing data-lane '{required}'")
    if not {"internal_dependencies", "external_dependencies"} <= data_lane_set:
        errors.append("HTML dependency layer must include internal_dependencies and external_dependencies")

    text = "\n".join(parser.text_chunks).lower()
    for required_text in ("source-backed", "inference", "l0 static html/svg"):
        if required_text not in text:
            errors.append(f"HTML missing text marker: {required_text}")

    if parser.remote_refs:
        errors.append(f"HTML must not require remote refs: {', '.join(parser.remote_refs)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lanes", type=Path, required=True)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--lanes-only", action="store_true")
    args = parser.parse_args()

    try:
        schema = load_schema(args.schema)
        errors = validate_lanes(load_json(args.lanes), schema)
    except ValueError as exc:
        errors = [str(exc)]

    if not args.lanes_only:
        if not args.html:
            errors.append("--html is required unless --lanes-only is set")
        else:
            errors.extend(validate_html(args.html))

    if errors:
        print("XRAY_EXAMPLE_VALIDATION=block")
        for error in errors:
            print(f"BLOCK: {error}")
        return 1

    print("XRAY_EXAMPLE_VALIDATION=pass")
    print(f"SCHEMA={args.schema}")
    print(f"LANES={args.lanes}")
    if args.html:
        print(f"HTML={args.html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

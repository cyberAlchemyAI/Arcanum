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
    allowed_reader_baselines = set(require_string_list(schema, "allowed_reader_baselines"))
    required_reader_contract_fields = require_string_list(schema, "required_reader_contract_fields")
    required_opening_contract_fields = require_string_list(schema, "required_opening_contract_fields")
    required_reader_term_fields = require_string_list(schema, "required_reader_term_fields")
    allowed_reader_term_authority = set(require_string_list(schema, "allowed_reader_term_authority"))
    required_layer_reader_outcome_fields = require_string_list(schema, "required_layer_reader_outcome_fields")
    required_readability_dynamics_fields = require_string_list(schema, "required_readability_dynamics_fields")

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

    reader_contract = data.get("reader_contract")
    if not isinstance(reader_contract, dict):
        errors.append("reader_contract must be an object")
    else:
        for field in required_reader_contract_fields:
            if field not in reader_contract:
                errors.append(f"reader_contract: missing {field}")
        if reader_contract.get("reader_baseline") not in allowed_reader_baselines:
            errors.append(
                "reader_contract.reader_baseline must be one of: "
                + ", ".join(sorted(allowed_reader_baselines))
            )
        for field in ("target_public", "reader_reward"):
            value = reader_contract.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"reader_contract.{field} must be a non-empty string")
        assumed = reader_contract.get("assumed_knowledge")
        if not isinstance(assumed, list) or not all(isinstance(item, str) and item.strip() for item in assumed):
            errors.append("reader_contract.assumed_knowledge must be a non-empty string list")
        opening_contract = reader_contract.get("opening_contract")
        if not isinstance(opening_contract, dict):
            errors.append("reader_contract.opening_contract must be an object")
        else:
            for field in required_opening_contract_fields:
                if field not in opening_contract:
                    errors.append(f"reader_contract.opening_contract: missing {field}")
            for field in ("must_start_with", "must_not_start_with"):
                value = opening_contract.get(field)
                if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                    errors.append(f"reader_contract.opening_contract.{field} must be a non-empty string list")
            failure = opening_contract.get("failure_message")
            if not isinstance(failure, str) or not failure.strip():
                errors.append("reader_contract.opening_contract.failure_message must be a non-empty string")

    reader_terms = data.get("reader_terms")
    if not isinstance(reader_terms, list) or not reader_terms:
        errors.append("reader_terms must be a non-empty list")
    else:
        seen_terms: set[str] = set()
        for index, term in enumerate(reader_terms, start=1):
            if not isinstance(term, dict):
                errors.append(f"reader_terms[{index}]: must be an object")
                continue
            for field in required_reader_term_fields:
                if field not in term:
                    errors.append(f"reader_terms[{index}]: missing {field}")
            term_name = term.get("term")
            if isinstance(term_name, str) and term_name.strip():
                normalized = term_name.strip().lower()
                if normalized in seen_terms:
                    errors.append(f"reader_terms[{index}]: duplicate term `{term_name}`")
                seen_terms.add(normalized)
            for field in ("term", "plain_meaning", "why_it_matters", "source_or_lane", "misuse_warning"):
                value = term.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"reader_terms[{index}].{field} must be a non-empty string")
            if term.get("authority") not in allowed_reader_term_authority:
                errors.append(
                    f"reader_terms[{index}].authority must be one of: "
                    + ", ".join(sorted(allowed_reader_term_authority))
                )

    layer_reader_outcomes = data.get("layer_reader_outcomes")
    if not isinstance(layer_reader_outcomes, list) or not layer_reader_outcomes:
        errors.append("layer_reader_outcomes must be a non-empty list")
    else:
        covered_layers: set[str] = set()
        for index, outcome in enumerate(layer_reader_outcomes, start=1):
            if not isinstance(outcome, dict):
                errors.append(f"layer_reader_outcomes[{index}]: must be an object")
                continue
            for field in required_layer_reader_outcome_fields:
                if field not in outcome:
                    errors.append(f"layer_reader_outcomes[{index}]: missing {field}")
            layer = outcome.get("layer")
            if isinstance(layer, str) and layer.strip():
                covered_layers.add(layer.strip())
                if layer not in required_lanes:
                    errors.append(f"layer_reader_outcomes[{index}].layer is not a required lane: {layer}")
            for field in ("as_a_reader", "should_understand", "because_it_matters_for"):
                value = outcome.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"layer_reader_outcomes[{index}].{field} must be a non-empty string")
        expected_outcome_layers = {
            "surface",
            "flow",
            "internal_dependencies",
            "external_dependencies",
            "risk_questions",
        }
        missing_outcome_layers = sorted(expected_outcome_layers - covered_layers)
        if missing_outcome_layers:
            errors.append(f"layer_reader_outcomes missing layers: {', '.join(missing_outcome_layers)}")

    readability = data.get("readability_dynamics")
    if not isinstance(readability, dict):
        errors.append("readability_dynamics must be an object")
    else:
        for field in required_readability_dynamics_fields:
            if field not in readability:
                errors.append(f"readability_dynamics: missing {field}")
        for field in ("max_words_per_paragraph", "max_consecutive_dense_blocks", "require_scan_anchor_every_n_blocks"):
            value = readability.get(field)
            if not isinstance(value, int) or value < 1:
                errors.append(f"readability_dynamics.{field} must be a positive integer")
        treatments = readability.get("allowed_visual_treatments")
        if not isinstance(treatments, list) or not all(isinstance(item, str) and item.strip() for item in treatments):
            errors.append("readability_dynamics.allowed_visual_treatments must be a non-empty string list")
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
    for required_text in (
        "source-backed",
        "inference",
        "l0 static html/svg",
        "reader terms",
        "reader outcomes",
        "why it matters",
    ):
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

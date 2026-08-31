#!/usr/bin/env python3
"""Validate an Invoke-authored Work-Pack execution-entry projection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = SPELL_ROOT / "schemas" / "work-pack-execution-entry.schema.json"


class ProjectionError(ValueError):
    """One stable fail-closed projection diagnostic."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _reject_noncanonical(value: Any, location: str = "$") -> None:
    if isinstance(value, float):
        raise ProjectionError(
            "EXECUTION_ENTRY_NONCANONICAL_JSON",
            f"floating-point value is forbidden at {location}",
        )
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_noncanonical(child, f"{location}/{index}")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ProjectionError(
                    "EXECUTION_ENTRY_NONCANONICAL_JSON",
                    f"non-string key at {location}",
                )
            _reject_noncanonical(child, f"{location}/{key}")
        return
    raise ProjectionError(
        "EXECUTION_ENTRY_NONCANONICAL_JSON",
        f"unsupported {type(value).__name__} at {location}",
    )


def canonical_digest(value: Any) -> str:
    _reject_noncanonical(value)
    payload = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _validate_schema(document: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(map(str, error.absolute_path)) or "<root>"
        raise ProjectionError(
            "EXECUTION_ENTRY_SCHEMA_INVALID", f"{location}: {error.message}"
        )


def _validate_relative_path(raw: str, location: str) -> None:
    posix = PurePosixPath(raw)
    windows = PureWindowsPath(raw)
    if (
        not raw
        or "\\" in raw
        or posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or any(part in {"", ".", ".."} for part in posix.parts)
    ):
        raise ProjectionError("EXECUTION_ENTRY_PATH_INVALID", f"{location}: {raw}")


def _expected_owner(route: dict[str, Any]) -> set[str]:
    short = f"{route['capability']}:{route['mode']}"
    return {short, f"{short}:{route['target']}"}


def _validate_entry_state(
    entry: dict[str, Any], routes: dict[str, dict[str, Any]], frontier: set[str]
) -> None:
    state = entry["state"]
    selected = entry["selected_unit"]
    route_id = entry["route_id"]
    next_owner = entry["next_owner"]
    if selected is not None and selected not in frontier:
        raise ProjectionError("EXECUTION_ENTRY_UNIT_UNKNOWN", selected)
    if state == "selection-ready":
        if (
            selected is not None
            or route_id is not None
            or next_owner != "implementation-readiness:execute"
        ):
            raise ProjectionError(
                "EXECUTION_ENTRY_STATE_CONTRADICTION", "selection-ready"
            )
        return
    if state == "blocked":
        if route_id is not None or next_owner is not None:
            raise ProjectionError("EXECUTION_ENTRY_STATE_CONTRADICTION", "blocked")
        return
    if route_id not in routes:
        raise ProjectionError(
            "EXECUTION_ENTRY_ROUTE_UNKNOWN", str(route_id)
        )
    route = routes[route_id]
    if selected is not None and route["frontier_swu"] != selected:
        raise ProjectionError(
            "EXECUTION_ENTRY_STATE_CONTRADICTION",
            "selected unit differs from route frontier",
        )
    if next_owner not in _expected_owner(route):
        raise ProjectionError(
            "EXECUTION_ENTRY_STATE_CONTRADICTION",
            "next owner differs from selected route",
        )
    if state == "task-ready" and (
        selected is None or route["capability"] != "task-session"
    ):
        raise ProjectionError(
            "EXECUTION_ENTRY_STATE_CONTRADICTION", "task-ready"
        )


def validate_projection(document: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic receipt or raise one stable error."""

    _validate_schema(document)
    policy = document["execution_policy"]
    routes = policy["allowed_routes"]
    route_ids: set[str] = set()
    route_map: dict[str, dict[str, Any]] = {}
    frontier = set(document["frontier"])
    for index, route in enumerate(routes):
        route_id = route["route_id"]
        if route_id in route_ids:
            raise ProjectionError("EXECUTION_ENTRY_ROUTE_DUPLICATE", route_id)
        route_ids.add(route_id)
        route_map[route_id] = route
        if route["frontier_swu"] not in frontier:
            raise ProjectionError(
                "EXECUTION_ENTRY_ROUTE_FRONTIER_UNKNOWN", route["frontier_swu"]
            )
        for path_index, raw in enumerate(route["write_scope"]):
            _validate_relative_path(
                raw, f"allowed_routes/{index}/write_scope/{path_index}"
            )
        _validate_relative_path(
            route["expected_receipt"],
            f"allowed_routes/{index}/expected_receipt",
        )
    actual_digest = canonical_digest(routes)
    if actual_digest != policy["allowed_routes_digest"]:
        raise ProjectionError(
            "EXECUTION_ENTRY_ROUTES_DIGEST_STALE",
            f"expected {actual_digest}, got {policy['allowed_routes_digest']}",
        )
    decisions = set(policy["automatic_decisions"])
    declared_retry = policy.get("declared_retry")
    if ("declared-retry" in decisions) != (declared_retry is not None):
        raise ProjectionError(
            "EXECUTION_ENTRY_RETRY_CONTRADICTION",
            "declared-retry decision and contract must appear together",
        )
    overlap = decisions & set(policy["stop_decisions"])
    if overlap:
        raise ProjectionError(
            "EXECUTION_ENTRY_DECISION_OVERLAP", ",".join(sorted(overlap))
        )
    _validate_entry_state(document["execution_entry"], route_map, frontier)
    return {
        "schema_version": "1.0.0",
        "status": "pass",
        "work_pack_id": document["work_pack_id"],
        "frontier": document["frontier"],
        "allowed_routes_digest": actual_digest,
        "route_count": len(routes),
        "authority_effect": "none",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.projection.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ProjectionError(
                "EXECUTION_ENTRY_SCHEMA_INVALID", "<root>: object required"
            )
        result = validate_projection(document)
    except (OSError, json.JSONDecodeError, ProjectionError) as error:
        sys.stderr.write(f"{error}\n")
        return 1
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

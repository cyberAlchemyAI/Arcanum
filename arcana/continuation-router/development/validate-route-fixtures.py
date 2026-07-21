#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PACKAGE / "continuation-route.schema.json"
FIXTURE_DIR = PACKAGE / "development" / "route-fixtures"
KNOWN_ROUTES = {
    ("invoke", "refresh"),
    ("decision-gate", "blocker"),
    ("task-session", "execute"),
    ("refine", "standard"),
    ("goal", "execute"),
    ("stop", "user-input"),
    ("review", "inspect"),
}
PRIVATE_TOKENS = ("domainspec", "cyberalchemy-v2", "iolm", "bte-")


def fail(path: Path, message: str) -> None:
    raise AssertionError(f"{path.name}: {message}")


def validate_semantics(path: Path, payload: dict) -> None:
    candidates = payload["candidates"]
    ranks = [candidate["rank"] for candidate in candidates]
    if ranks != list(range(1, len(candidates) + 1)):
        fail(path, "candidate ranks must be consecutive and ordered")

    selection = payload["selection"]
    selected = None
    if selection["candidate_rank"] is not None:
        selected = next(
            (candidate for candidate in candidates if candidate["rank"] == selection["candidate_rank"]),
            None,
        )
        if selected is None:
            fail(path, "selection references a missing candidate rank")

    if selection["status"] == "selected" and selected is None:
        fail(path, "selected status requires a candidate rank")

    dispatch = payload["dispatch"]
    if dispatch["status"] == "completed":
        if selection["status"] != "selected":
            fail(path, "completed dispatch requires a selected route")
        if not dispatch["owner_receipt"]:
            fail(path, "completed dispatch requires a separate owner receipt")
        if dispatch["helper_closeout"] != "pass":
            fail(path, "completed dispatch requires joined helper closeout")
        if payload["owner_boundary"] != "pass":
            fail(path, "completed dispatch requires a passing owner boundary")
        if selected and selected["approval_required"]:
            exact = ":".join(
                part
                for part in (selected["capability"], selected["mode"], selected["mutation_mode"])
                if part
            )
            if selected["authorization_status"] != "matched":
                fail(path, "approved dispatch requires matched candidate authorization")
            if payload["authorization"]["exact_route"] != exact:
                fail(path, "authorization tuple does not match the selected owner route")
            if not payload["authorization"]["evidence"]:
                fail(path, "approved dispatch requires authorization evidence")

    if payload["source"]["legacy_adaptation"]:
        if any(candidate["authorization_status"] == "matched" for candidate in candidates):
            fail(path, "legacy adaptation must not silently create matched authorization")

    for candidate in candidates:
        route = (candidate["capability"], candidate["mode"])
        if route not in KNOWN_ROUTES and selection["status"] != "blocked":
            fail(path, "unknown capability or mode must block selection")

    if path.name == "route-repeated-fingerprint-block.json":
        if selection["status"] != "blocked" or dispatch["status"] != "blocked":
            fail(path, "repeated fingerprint must block source re-entry")

    normalized = json.dumps(payload).lower()
    for token in PRIVATE_TOKENS:
        if token in normalized:
            fail(path, f"public fixture contains private token: {token}")


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    fixtures = sorted(FIXTURE_DIR.glob("route-*.json"))
    if len(fixtures) < 6:
        raise AssertionError("expected at least six route fixtures")

    for path in fixtures:
        payload = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
        if errors:
            fail(path, "; ".join(error.message for error in errors))
        validate_semantics(path, payload)
        print(f"PASS: {path.name}")

    print("ROUTE_FIXTURES=pass")
    print(f"ROUTE_FIXTURE_COUNT={len(fixtures)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print("ROUTE_FIXTURES=block", file=sys.stderr)
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

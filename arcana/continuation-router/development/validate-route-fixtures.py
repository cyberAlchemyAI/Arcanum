#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PACKAGE / "schemas" / "continuation-route.schema.json"
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
            if selected["authorization_status"] != "matched":
                fail(path, "approved dispatch requires matched candidate authorization")
            authorization = payload["authorization"]
            if authorization.get("source") == "work-pack-binding":
                if authorization["requested"]:
                    fail(path, "Work-Pack-bound dispatch must not request per-route authorization")
                if authorization.get("authorization_prompt_required"):
                    fail(path, "Work-Pack-bound dispatch must not require an authorization prompt")
                if authorization["exact_route"] is not None:
                    fail(path, "Work-Pack-bound dispatch must not masquerade as ad hoc authorization")
                if not authorization.get("work_pack_binding"):
                    fail(path, "Work-Pack-bound dispatch requires validated admission evidence")
            else:
                exact = ":".join(
                    part
                    for part in (
                        selected["capability"],
                        selected["mode"],
                        selected["mutation_mode"],
                    )
                    if part
                )
                if authorization["exact_route"] != exact:
                    fail(path, "authorization tuple does not match the selected owner route")
            if not authorization["evidence"]:
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

    if path.name in {
        "route-work-pack-owner-failure-block.json",
        "route-work-pack-missing-join-block.json",
    }:
        if selection["status"] != "blocked" or dispatch["status"] != "blocked":
            fail(path, "owner failure or missing join must block Work-Pack continuation")
        if payload["returned_next_route"] is not None:
            fail(path, "blocked Work-Pack continuation cannot return an executable route")

    phase = payload["source"].get("phase", "terminal")
    if phase == "pre-execution-prerequisite":
        if payload["schema_version"] != "arcanum.continuation_route.v2":
            fail(path, "pre-execution prerequisite routes require schema v2")
        context = payload["source"]["pre_execution_context"]
        dispatch_count = payload["dispatch"]["dispatch_count"]
        join_count = payload["dispatch"]["join_count"]
        if payload["dispatch"]["router_mutations"]:
            fail(path, "router must not perform owner mutation")
        consumed_key = f"{context['attempt_id']}:{context['prerequisite_fingerprint']}"
        if consumed_key in context["consumed_attempt_fingerprints"]:
            if selection["status"] != "blocked" or dispatch["status"] != "blocked":
                fail(path, "consumed attempt/fingerprint must block")
        if dispatch["status"] == "completed":
            if dispatch_count != 1 or join_count != 1:
                fail(path, "completed prerequisite route requires exactly one dispatch and join")
            if len(candidates) != 1:
                fail(path, "completed prerequisite route requires one unambiguous owner")
            if payload["returned_next_route"] is not None:
                fail(path, "prerequisite route must not recursively return a next route")
            owner_receipt_ref = dispatch.get("owner_receipt_ref")
            if not owner_receipt_ref:
                fail(path, "completed prerequisite route requires an exact owner receipt reference")
            if owner_receipt_ref["path"] != dispatch["owner_receipt"]:
                fail(path, "owner receipt path string does not match its exact reference")
            if dispatch.get("join_validation") != "pass":
                fail(path, "completed prerequisite route requires current owner receipt validation")
            binding = payload["authorization"].get("binding")
            if not binding:
                fail(path, "completed prerequisite route requires exact authorization binding")
            selected_route = ":".join(
                part for part in (selected["capability"], selected["mode"], selected["mutation_mode"]) if part
            )
            exact_pairs = (
                ("route", selected_route),
                ("task_id", context["task_id"]),
                ("swu_id", context["swu_id"]),
                ("attempt_id", context["attempt_id"]),
                ("prerequisite_fingerprint", context["prerequisite_fingerprint"]),
                ("target_inventory_digest", context["target_inventory_digest"]),
                ("validation_contract_digest", context["validation_contract_digest"]),
                ("satisfaction_predicate_digest", context["satisfaction_predicate_digest"]),
                ("resume_point", context["resume_point"]),
                ("max_owner_hops", context["max_owner_hops"]),
                ("allowed_effect", context["allowed_effect"]),
            )
            for field, expected in exact_pairs:
                if binding.get(field) != expected:
                    fail(path, f"authorization binding mismatch: {field}")
            handle = payload.get("control_handle")
            if not handle:
                fail(path, "completed prerequisite route requires same-attempt control handle")
            for field in (
                "task_id", "swu_id", "attempt_id", "prerequisite_fingerprint",
                "target_inventory_digest", "validation_contract_digest",
                "satisfaction_predicate_digest", "resume_point", "max_owner_hops",
                "allowed_effect",
            ):
                if handle[field] != context[field]:
                    fail(path, f"control handle mismatch: {field}")
            if handle["route"] != context["declared_owner_route"]:
                fail(path, "control handle route does not match the declared owner route")
            if handle["owner_receipt_ref"] != owner_receipt_ref:
                fail(path, "control handle must bind the exact joined owner receipt reference")
        else:
            if dispatch_count != 0 or join_count != 0:
                fail(path, "non-completed prerequisite route cannot claim dispatch or join")
            if payload.get("control_handle") is not None:
                fail(path, "blocked prerequisite route cannot emit a control handle")

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

    adversarial = sorted((FIXTURE_DIR / "adversarial").glob("*.json"))
    if len(adversarial) < 2:
        raise AssertionError("expected at least two adversarial route fixtures")
    for path in adversarial:
        payload = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
        try:
            if errors:
                raise AssertionError("; ".join(error.message for error in errors))
            validate_semantics(path, payload)
        except AssertionError:
            print(f"PASS_REJECTED: {path.name}")
        else:
            fail(path, "adversarial fixture was accepted")

    print("ROUTE_FIXTURES=pass")
    print(f"ROUTE_FIXTURE_COUNT={len(fixtures)}")
    print(f"ROUTE_ADVERSARIAL_FIXTURE_COUNT={len(adversarial)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print("ROUTE_FIXTURES=block", file=sys.stderr)
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

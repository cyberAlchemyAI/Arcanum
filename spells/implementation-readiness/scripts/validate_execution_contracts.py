#!/usr/bin/env python3
"""Validate public Work-Pack execution-contract fixtures."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SPELL_ROOT = SCRIPT_ROOT.parent
sys.path.insert(0, str(SCRIPT_ROOT))

from execution_contracts import (  # noqa: E402
    ExecutionContractError,
    allowed_routes_digest,
    build_execution_intent_binding,
    match_bound_route,
    validate_execution_binding,
    validate_execution_entry,
    validate_execution_policy,
)


FIXTURE = (
    SPELL_ROOT
    / "development/fixtures/execution-contracts/execution-contract-cases.json"
)
CREATED_AT = "2026-08-04T20:00:00Z"


def hydrated_policy(raw: dict) -> dict:
    policy = copy.deepcopy(raw)
    policy["allowed_routes_digest"] = allowed_routes_digest(policy["allowed_routes"])
    return policy


def selection_entry(policy: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "selection-ready",
        "selected_unit": None,
        "route_id": None,
        "next_owner": {
            "capability": "implementation-readiness",
            "mode": "execute",
            "target": policy["work_pack_id"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }


def task_entry(policy: dict) -> dict:
    route = policy["allowed_routes"][0]
    return {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "task-ready",
        "selected_unit": route["frontier_swu"],
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }


def owner_entry(policy: dict) -> dict:
    route = policy["allowed_routes"][1]
    return {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "owner-prerequisite",
        "selected_unit": route["frontier_swu"],
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }


def expect_code(expected: str, action) -> None:
    try:
        action()
    except ExecutionContractError as error:
        if error.code != expected:
            raise AssertionError(f"expected {expected}, got {error.code}: {error}") from error
        return
    raise AssertionError(f"expected {expected}, action passed")


def run_invalid_case(name: str, expected: str, base_policy: dict) -> None:
    policy = copy.deepcopy(base_policy)
    entry = task_entry(policy)
    binding = build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id="invoke-public-fixture",
        created_at=CREATED_AT,
        execution_mode="finite-frontier",
    )
    candidate = copy.deepcopy(binding["current_route"])

    if name == "unknown-frontier":
        policy["allowed_routes"][0]["frontier_swu"] = "SWU-UNKNOWN"
        policy["allowed_routes_digest"] = allowed_routes_digest(policy["allowed_routes"])
        action = lambda: validate_execution_policy(policy)
    elif name == "escaping-path":
        policy["allowed_routes"][0]["write_scope"] = ["../escape"]
        policy["allowed_routes_digest"] = allowed_routes_digest(policy["allowed_routes"])
        action = lambda: validate_execution_policy(policy)
    elif name == "missing-validation":
        policy["validation_commands"] = []
        action = lambda: validate_execution_policy(policy)
    elif name == "protected-effect":
        policy["allowed_routes"][0]["effect_class"] = "publication-or-deployment"
        policy["allowed_routes_digest"] = allowed_routes_digest(policy["allowed_routes"])
        action = lambda: validate_execution_policy(policy)
    elif name == "stale-route-digest":
        policy["allowed_routes_digest"] = "f" * 64
        action = lambda: validate_execution_policy(policy)
    elif name == "stale-work-pack":
        changed = copy.deepcopy(policy)
        changed["work_pack_semantic_digest"] = "2" * 64
        action = lambda: validate_execution_binding(binding, changed, entry)
    elif name == "contradictory-entry":
        entry["next_owner"]["target"] = "different-target"
        action = lambda: validate_execution_entry(entry, policy)
    elif name == "undeclared-route":
        candidate["route_id"] = "unknown"
        action = lambda: match_bound_route(binding, candidate)
    elif name == "target-mismatch":
        candidate["target"] = "expanded-target"
        action = lambda: match_bound_route(binding, candidate)
    elif name == "write-expansion":
        candidate["write_scope"] = [*candidate["write_scope"], "extra/"]
        action = lambda: match_bound_route(binding, candidate)
    elif name == "effect-mismatch":
        candidate["effect_class"] = "external-network-or-message"
        action = lambda: match_bound_route(binding, candidate)
    elif name == "input-mismatch":
        candidate["required_inputs"] = ["other.json"]
        action = lambda: match_bound_route(binding, candidate)
    elif name == "receipt-mismatch":
        candidate["expected_receipt"] = "receipts/other.json"
        action = lambda: match_bound_route(binding, candidate)
    elif name == "frontier-replay":
        binding["captured_frontier"] = ["SWU-U1"]
        payload = {key: value for key, value in binding.items() if key != "binding_digest"}
        from execution_contracts import canonical_digest

        binding["binding_digest"] = canonical_digest(payload)
        action = lambda: validate_execution_binding(binding, policy, entry)
    else:
        raise AssertionError(f"unknown fixture mutation: {name}")
    expect_code(expected, action)


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    policy = hydrated_policy(fixture["base_policy"])
    validate_execution_policy(policy)
    for entry in (selection_entry(policy), owner_entry(policy), task_entry(policy)):
        validate_execution_entry(entry, policy)

    task = task_entry(policy)
    binding = build_execution_intent_binding(
        policy,
        task,
        source_invocation_id="invoke-public-fixture",
        created_at=CREATED_AT,
        execution_mode="finite-frontier",
    )
    if "approval" in json.dumps(binding).lower():
        raise AssertionError("execution binding must not contain an approval gate")
    match = match_bound_route(binding, copy.deepcopy(binding["current_route"]))
    if match["authorization_prompt_required"] is not False:
        raise AssertionError("bound route unexpectedly requires an authorization prompt")

    for case in fixture["invalid_cases"]:
        run_invalid_case(case["mutation"], case["expected_code"], policy)
        print(f"PASS: {case['mutation']} -> {case['expected_code']}")

    print("EXECUTION_CONTRACTS=pass")
    print("VALID_ENTRY_STATES=3")
    print(f"NEGATIVE_CASES={len(fixture['invalid_cases'])}")
    print("AUTHORIZATION_PROMPT_COUNT=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ExecutionContractError, json.JSONDecodeError) as error:
        print("EXECUTION_CONTRACTS=block", file=sys.stderr)
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

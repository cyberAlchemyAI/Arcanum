#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))
sys.path.insert(
    0, str(ARCANUM_ROOT / "spells" / "implementation-readiness" / "scripts")
)

from execution_contracts import (  # noqa: E402
    allowed_routes_digest,
    build_execution_intent_binding,
    canonical_digest,
)
from work_pack_route import evaluate_work_pack_route, validate_admission_receipt  # noqa: E402


CASES_PATH = (
    PACKAGE_ROOT
    / "development"
    / "work-pack-route-fixtures"
    / "admission-cases.json"
)


def assign_path(target: dict, path: list[str], value: object) -> None:
    current = target
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def base_request() -> dict:
    unit_id = "SWU-GENERIC-001"
    route = {
        "route_id": "route-generic-owner",
        "frontier_swu": unit_id,
        "capability": "invoke",
        "mode": "refresh",
        "target": "generic local package",
        "write_scope": ["packages/example/"],
        "effect_class": "repository-local-reversible",
        "required_inputs": ["task.md"],
        "expected_receipt": "receipts/SWU-GENERIC-001.json",
    }
    semantic_digest = canonical_digest({"work_pack": "generic"})
    continuity_payload = {
        "source_audit_id": "synthetic-router-fixture-audit",
        "source_projection_digest": canonical_digest(
            {"frontier": [unit_id], "completed_count": 0}
        ),
        "work_pack_semantic_digest": semantic_digest,
        "plan_epoch_id": f"epoch-{canonical_digest([unit_id])[:24]}",
        "completed_prefix": [],
        "next_unit": unit_id,
        "authority_effect": "none",
    }
    policy = {
        "schema_version": "1.1.0",
        "work_pack_id": "WP-GENERIC-001",
        "work_pack_semantic_digest": semantic_digest,
        "frontier": [unit_id],
        "completion_continuity": {
            **continuity_payload,
            "continuity_digest": canonical_digest(continuity_payload),
        },
        "allowed_routes": [route],
        "allowed_routes_digest": allowed_routes_digest([route]),
        "automatic_decisions": [
            "internal-tool-selection",
            "capability-owner-routing",
        ],
        "stop_decisions": [
            "scope-expansion",
            "failed-acceptance-critical-validation",
        ],
        "validation_commands": ["python3 validate.py"],
        "scope_source": "exact-work-pack-and-captured-frontier",
        "validation_policy": "owner-gates-remain-mandatory",
        "authority_effect": "none",
    }
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "owner-prerequisite",
        "selected_unit": unit_id,
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }
    binding = build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id="invoke-generic-001",
        created_at="2026-08-04T00:00:00Z",
        execution_mode="until-real-blocker",
    )
    return {
        "schema_version": "1.0.0",
        "execution_policy": policy,
        "execution_entry": entry,
        "execution_binding": binding,
        "candidate_routes": [copy.deepcopy(route)],
        "installed_owner_routes": [{"capability": "invoke", "mode": "refresh"}],
        "available_inputs": ["task.md"],
        "consumed_route_fingerprints": [],
        "authorization_flag": None,
        "authority_effect": "none",
    }


def apply_mutation(request: dict, mutation: dict | None) -> None:
    if mutation is None:
        return
    target_name = mutation["target"]
    path = mutation["path"]
    value = mutation["value"]
    if target_name == "candidate":
        assign_path(request["candidate_routes"][0], path, value)
        if path in (["capability"], ["mode"]):
            candidate = request["candidate_routes"][0]
            request["installed_owner_routes"].append(
                {
                    "capability": candidate["capability"],
                    "mode": candidate["mode"],
                }
            )
    elif target_name == "policy":
        assign_path(request["execution_policy"], path, value)
    elif target_name == "binding":
        assign_path(request["execution_binding"], path, value)
    elif target_name == "request" and path == ["duplicate_candidate"]:
        request["candidate_routes"].append(copy.deepcopy(request["candidate_routes"][0]))
    elif target_name == "request" and path == ["consume_current_fingerprint"]:
        request["consumed_route_fingerprints"] = [
            request["execution_binding"]["route_fingerprint"]
        ]
    elif target_name == "request":
        assign_path(request, path, value)
    else:
        raise AssertionError(f"unsupported mutation target: {target_name}")


def main() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]
    prompt_count = 0
    for case in cases:
        request = base_request()
        apply_mutation(request, case["mutation"])
        receipt = evaluate_work_pack_route(request)
        validate_admission_receipt(receipt)
        if receipt["verdict"] != case["expected_verdict"]:
            raise AssertionError(
                f"{case['name']}: expected {case['expected_verdict']}, got {receipt['verdict']}"
            )
        if receipt["code"] != case["expected_code"]:
            raise AssertionError(
                f"{case['name']}: expected {case['expected_code']}, got {receipt['code']}"
            )
        if receipt["authorization_prompt_required"]:
            prompt_count += 1
        if receipt["verdict"] == "pass":
            if receipt["authorization_source"] != "work-pack-binding":
                raise AssertionError(f"{case['name']}: wrong authorization source")
            if not receipt["dispatch_allowed"]:
                raise AssertionError(f"{case['name']}: admitted route cannot dispatch")
        else:
            if receipt["dispatch_allowed"]:
                raise AssertionError(f"{case['name']}: blocked route can dispatch")
        print(f"PASS: {case['name']} -> {receipt['code']}")

    if prompt_count != 0:
        raise AssertionError("Work-Pack admission must never request per-route authorization")

    with tempfile.TemporaryDirectory(prefix="wpeg-router-") as temporary:
        temp_root = Path(temporary)
        request_path = temp_root / "request.json"
        receipt_path = temp_root / "receipt.json"
        request_path.write_text(
            json.dumps(base_request(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        command = [
            sys.executable,
            str(PACKAGE_ROOT / "scripts" / "admit-work-pack-route.py"),
            "--request",
            str(request_path),
            "--output",
            str(receipt_path),
        ]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            raise AssertionError(f"CLI admission failed: {completed.stderr}")
        cli_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        validate_admission_receipt(cli_receipt)
        if cli_receipt["code"] != "ROUTE_ADMITTED":
            raise AssertionError("CLI did not admit the exact bound route")
        print("PASS: CLI exact bound route -> ROUTE_ADMITTED")

    print("WORK_PACK_ROUTE_FIXTURES=pass")
    print(f"WORK_PACK_ROUTE_CASE_COUNT={len(cases)}")
    print(f"AUTHORIZATION_PROMPT_COUNT={prompt_count}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as error:
        print("WORK_PACK_ROUTE_FIXTURES=block", file=sys.stderr)
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

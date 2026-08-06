#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
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
from fast_execution_entry_guard import (  # noqa: E402
    classify_fast_entry,
    validate_fast_entry_receipt,
)


def base_policy() -> dict:
    unit_id = "SWU-GENERIC-001"
    routes = [
        {
            "route_id": "route-owner",
            "frontier_swu": unit_id,
            "capability": "invoke",
            "mode": "refresh",
            "target": "repair generic unit",
            "write_scope": ["packages/generic/"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["owner-input.json"],
            "expected_receipt": "receipts/owner.json",
        },
        {
            "route_id": "route-task",
            "frontier_swu": unit_id,
            "capability": "task-session",
            "mode": "execute",
            "target": "execute generic unit",
            "write_scope": ["packages/generic/"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["task-input.json"],
            "expected_receipt": "receipts/task.json",
        },
    ]
    semantic_digest = canonical_digest({"work_pack": "fast-guard"})
    continuity_payload = {
        "source_audit_id": "synthetic-fast-guard-audit",
        "source_projection_digest": canonical_digest(
            {"frontier": [unit_id], "completed_count": 0}
        ),
        "work_pack_semantic_digest": semantic_digest,
        "plan_epoch_id": f"epoch-{canonical_digest([unit_id])[:24]}",
        "completed_prefix": [],
        "next_unit": unit_id,
        "authority_effect": "none",
    }
    return {
        "schema_version": "1.1.0",
        "work_pack_id": "WP-GENERIC-FAST-GUARD",
        "work_pack_semantic_digest": semantic_digest,
        "frontier": [unit_id],
        "completion_continuity": {
            **continuity_payload,
            "continuity_digest": canonical_digest(continuity_payload),
        },
        "allowed_routes": routes,
        "allowed_routes_digest": allowed_routes_digest(routes),
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


def entry(policy: dict, state: str) -> dict:
    if state == "task-ready":
        route_id = "route-task"
        owner = {
            "capability": "task-session",
            "mode": "execute",
            "target": "execute generic unit",
        }
        selected = "SWU-GENERIC-001"
        blocker = None
    elif state == "owner-prerequisite":
        route_id = "route-owner"
        owner = {
            "capability": "invoke",
            "mode": "refresh",
            "target": "repair generic unit",
        }
        selected = "SWU-GENERIC-001"
        blocker = None
    elif state == "selection-ready":
        route_id = None
        owner = {
            "capability": "implementation-readiness",
            "mode": "execute",
            "target": policy["work_pack_id"],
        }
        selected = None
        blocker = None
    else:
        route_id = None
        owner = None
        selected = "SWU-GENERIC-001"
        blocker = "PRODUCT_DECISION_REQUIRED"
    return {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": state,
        "selected_unit": selected,
        "route_id": route_id,
        "next_owner": owner,
        "blocker_code": blocker,
        "authority_effect": "none",
    }


def request(state: str) -> dict:
    policy = base_policy()
    projection = entry(policy, state)
    binding = build_execution_intent_binding(
        policy,
        projection,
        source_invocation_id="invoke-fast-guard-001",
        created_at="2026-08-04T00:00:00Z",
        execution_mode="one-unit",
    )
    return {
        "schema_version": "1.0.0",
        "execution_policy": policy,
        "execution_entry": projection,
        "execution_binding": binding,
        "selected_unit": {
            "work_pack_id": policy["work_pack_id"],
            "swu_id": "SWU-GENERIC-001",
        },
        "authority_effect": "none",
    }


def assert_fast_boundary(receipt: dict) -> None:
    validate_fast_entry_receipt(receipt)
    assert receipt["authorization_prompt_required"] is False
    assert receipt["logical_inputs_read"] == [
        "work-pack",
        "selected-unit",
        "execution-binding",
        "execution-entry-projection",
    ]
    assert receipt["read_count"] == 4
    assert receipt["phase_count"] == 1
    assert receipt["mutation_count"] == 0
    trace = receipt["phase_trace"]
    assert trace["entry_guard_entered"] is True
    assert trace["context_builder_entered"] is False
    assert trace["deep_material_check_entered"] is False
    assert trace["mutation_admission_entered"] is False
    assert trace["target_mutation_entered"] is False
    assert trace["owner_hops_dispatched"] == 0


def main() -> int:
    task_ready = classify_fast_entry(request("task-ready"))
    assert_fast_boundary(task_ready)
    assert task_ready["decision"] == "proceed"
    assert task_ready["permitted_next_action"] == "enter-context-builder"
    print("PASS: task-ready -> proceed to existing Context Builder path")

    owner_request = request("owner-prerequisite")
    owner = classify_fast_entry(owner_request)
    assert_fast_boundary(owner)
    assert owner["decision"] == "route-owner"
    assert owner["owner_packet"]["route_id"] == "route-owner"
    assert owner["authorization_source"] == "work-pack-binding"
    print("PASS: owner-prerequisite -> exact owner packet without prompt")

    selection = classify_fast_entry(request("selection-ready"))
    assert_fast_boundary(selection)
    assert selection["decision"] == "block"
    assert selection["code"] == "SELECTION_NOT_MATERIALIZED"

    blocked = classify_fast_entry(request("blocked"))
    assert_fast_boundary(blocked)
    assert blocked["decision"] == "block"
    assert blocked["code"] == "PRODUCT_DECISION_REQUIRED"

    untyped = request("blocked")
    untyped["execution_entry"]["blocker_code"] = "owner.blocked"
    untyped_receipt = classify_fast_entry(untyped)
    assert_fast_boundary(untyped_receipt)
    assert untyped_receipt["code"] == "EXECUTION_ENTRY_BLOCKED"
    assert "owner.blocked" in untyped_receipt["blocker_detail"]
    print("PASS: selection-ready and blocked entries stop before deep phases")

    stale = request("task-ready")
    stale["execution_binding"]["work_pack_semantic_digest"] = "0" * 64
    stale_receipt = classify_fast_entry(stale)
    assert_fast_boundary(stale_receipt)
    assert stale_receipt["decision"] == "block"
    assert stale_receipt["code"] == "WORK_PACK_SEMANTIC_STALE"

    wrong_unit = request("task-ready")
    wrong_unit["selected_unit"]["swu_id"] = "SWU-FOREIGN-002"
    wrong_receipt = classify_fast_entry(wrong_unit)
    assert_fast_boundary(wrong_receipt)
    assert wrong_receipt["decision"] == "block"
    assert wrong_receipt["code"] == "SELECTED_UNIT_OUTSIDE_FRONTIER"

    wrong_pack = request("owner-prerequisite")
    wrong_pack["selected_unit"]["work_pack_id"] = "WP-OTHER"
    wrong_pack_receipt = classify_fast_entry(wrong_pack)
    assert_fast_boundary(wrong_pack_receipt)
    assert wrong_pack_receipt["code"] == "WORK_PACK_ID_MISMATCH"

    forged = copy.deepcopy(owner)
    forged["owner_packet"]["target"] = "expanded target"
    try:
        validate_fast_entry_receipt(forged, owner_request)
    except Exception:
        pass
    else:
        raise AssertionError("forged owner packet was accepted")
    print("PASS: stale binding and identity mismatches block")

    with tempfile.TemporaryDirectory(prefix="wpeg-fast-guard-") as temporary:
        root = Path(temporary)
        input_path = root / "request.json"
        input_path.write_text(
            json.dumps(request("owner-prerequisite"), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(PACKAGE_ROOT / "scripts" / "classify-fast-execution-entry.py"),
                "--input",
                str(input_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise AssertionError(f"fast guard CLI failed: {completed.stderr}")
        cli_receipt = json.loads(completed.stdout)
        assert_fast_boundary(cli_receipt)
        assert cli_receipt["decision"] == "route-owner"
        assert sorted(path.name for path in root.iterdir()) == ["request.json"]
    print("PASS: CLI returns an exact fast-path receipt")

    with tempfile.TemporaryDirectory(prefix="generated-fast-guard-") as temporary:
        root = Path(temporary)
        generated = root / ".agents/skills/task-session"
        readiness = root / ".agents/skills/implementation-readiness"
        for relative in (
            "scripts/fast_execution_entry_guard.py",
            "scripts/classify-fast-execution-entry.py",
            "schemas/fast-execution-entry-request.schema.json",
            "schemas/fast-execution-entry-receipt.schema.json",
        ):
            target = generated / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PACKAGE_ROOT / relative, target)
        readiness_source = (
            ARCANUM_ROOT / "spells/implementation-readiness"
        )
        for relative in (
            "scripts/execution_contracts.py",
            "schemas/execution-policy.schema.json",
            "schemas/execution-entry-projection.schema.json",
            "schemas/execution-intent-binding.schema.json",
        ):
            target = readiness / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(readiness_source / relative, target)
        input_path = root / "request.json"
        input_path.write_text(
            json.dumps(request("task-ready"), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(generated / "scripts/classify-fast-execution-entry.py"),
                "--input",
                str(input_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"generated-layout fast guard failed: {completed.stderr}"
            )
        generated_receipt = json.loads(completed.stdout)
        assert generated_receipt["decision"] == "proceed"
        assert generated_receipt["code"] == "TASK_READY"
    print("PASS: generated skill layout resolves implementation-readiness sibling")

    print("FAST_EXECUTION_ENTRY_GUARD=pass")
    print("LOGICAL_READ_COUNT=4")
    print("PHASE_COUNT=1")
    print("AUTHORIZATION_PROMPT_COUNT=0")
    print("MUTATION_COUNT=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as error:
        print("FAST_EXECUTION_ENTRY_GUARD=block", file=sys.stderr)
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

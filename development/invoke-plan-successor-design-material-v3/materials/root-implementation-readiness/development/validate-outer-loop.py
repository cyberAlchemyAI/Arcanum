#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPELL_ROOT / "scripts"))

from execution_contracts import allowed_routes_digest, canonical_digest  # noqa: E402
from execution_loop import (  # noqa: E402
    OuterLoopError,
    decide_next_action,
    initialize_outer_loop,
    join_event,
    set_stop_decision,
    validate_outer_loop_state,
)


STOP_DECISIONS = [
    "product-or-semantic-choice",
    "scope-expansion",
    "destructive-or-irreversible-effect",
    "credentials-or-secret-access",
    "external-message-or-network-effect",
    "cost-policy-or-risk-acceptance",
    "authority-promotion-publication-deployment",
    "failed-acceptance-critical-validation",
]


def route(
    route_id: str,
    swu: str,
    capability: str,
    mode: str,
    target: str,
    required_input: str,
) -> dict:
    return {
        "route_id": route_id,
        "frontier_swu": swu,
        "capability": capability,
        "mode": mode,
        "target": target,
        "write_scope": [f"packages/{swu.lower()}/"],
        "effect_class": "repository-local-reversible",
        "required_inputs": [required_input],
        "expected_receipt": f"receipts/{route_id}.json",
    }


def completion_continuity(
    frontier: list[str], work_pack_semantic_digest: str, completed_count: int = 0
) -> dict:
    completed_prefix = [
        {
            "unit_id": unit,
            "unit_contract_digest": canonical_digest({"unit": unit}),
            "completion_binding_id": f"completion-{unit}",
            "completion_artifact_ref": {
                "path": f"receipts/{unit}.json",
                "sha256": canonical_digest({"receipt": unit}),
                "size_bytes": len(unit),
            },
            "closeout_binding_id": f"closeout-{unit}",
        }
        for unit in frontier[:completed_count]
    ]
    payload = {
        "source_audit_id": "synthetic-outer-loop-audit",
        "source_projection_digest": canonical_digest(
            {"frontier": frontier, "completed_count": completed_count}
        ),
        "work_pack_semantic_digest": work_pack_semantic_digest,
        "plan_epoch_id": f"epoch-{canonical_digest(frontier)[:24]}",
        "completed_prefix": completed_prefix,
        "next_unit": (
            frontier[completed_count] if completed_count < len(frontier) else None
        ),
        "authority_effect": "none",
    }
    return {**payload, "continuity_digest": canonical_digest(payload)}


def base_policy(frontier: list[str] | None = None) -> dict:
    units = frontier or ["SWU-GENERIC-001", "SWU-GENERIC-002"]
    semantic_digest = canonical_digest(
        {"work_pack": "generic-outer-loop", "frontier": units}
    )
    routes: list[dict] = []
    for index, unit in enumerate(units, start=1):
        routes.append(
            route(
                f"route-task-{index}",
                unit,
                "task-session",
                "execute",
                f"execute {unit}",
                f"task-input-{index}",
            )
        )
        routes.append(
            route(
                f"route-owner-{index}",
                unit,
                "invoke",
                "refresh",
                f"repair {unit}",
                f"owner-input-{index}",
            )
        )
    policy = {
        "schema_version": "1.1.0",
        "work_pack_id": "WP-GENERIC-OUTER-LOOP",
        "work_pack_semantic_digest": semantic_digest,
        "frontier": copy.deepcopy(units),
        "completion_continuity": completion_continuity(units, semantic_digest),
        "allowed_routes": routes,
        "allowed_routes_digest": allowed_routes_digest(routes),
        "automatic_decisions": [
            "internal-tool-selection",
            "capability-owner-routing",
            "reversible-local-default",
            "declared-fallback",
            "fresh-task-session-resumption",
        ],
        "stop_decisions": copy.deepcopy(STOP_DECISIONS),
        "validation_commands": ["python3 validate-generic.py"],
        "scope_source": "exact-work-pack-and-captured-frontier",
        "validation_policy": "owner-gates-remain-mandatory",
        "authority_effect": "none",
    }
    return policy


def entry(policy: dict, state: str, unit_index: int = 0) -> dict:
    unit = policy["frontier"][unit_index]
    if state == "selection-ready":
        selected_unit = None
        route_id = None
        owner = {
            "capability": "implementation-readiness",
            "mode": "execute",
            "target": policy["work_pack_id"],
        }
        blocker = None
    elif state == "owner-prerequisite":
        selected_unit = unit
        route_id = f"route-owner-{unit_index + 1}"
        selected_route = next(
            item for item in policy["allowed_routes"] if item["route_id"] == route_id
        )
        owner = {
            "capability": selected_route["capability"],
            "mode": selected_route["mode"],
            "target": selected_route["target"],
        }
        blocker = None
    elif state == "task-ready":
        selected_unit = unit
        route_id = f"route-task-{unit_index + 1}"
        selected_route = next(
            item for item in policy["allowed_routes"] if item["route_id"] == route_id
        )
        owner = {
            "capability": selected_route["capability"],
            "mode": selected_route["mode"],
            "target": selected_route["target"],
        }
        blocker = None
    else:
        selected_unit = unit
        route_id = None
        owner = None
        blocker = "PRODUCT_DECISION_REQUIRED"
    return {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": state,
        "selected_unit": selected_unit,
        "route_id": route_id,
        "next_owner": owner,
        "blocker_code": blocker,
        "authority_effect": "none",
    }


def init(
    policy: dict,
    initial_entry: dict,
    *,
    execution_mode: str = "one-unit",
    step_budget: int = 8,
) -> dict:
    return initialize_outer_loop(
        policy,
        initial_entry,
        source_invocation_id="invoke-generic-outer-loop-001",
        created_at="2026-08-04T00:00:00Z",
        execution_mode=execution_mode,
        step_budget=step_budget,
    )


def installed() -> list[dict[str, str]]:
    return [
        {"capability": "invoke", "mode": "refresh"},
        {"capability": "task-session", "mode": "execute"},
    ]


def event(
    action: dict,
    state: dict,
    *,
    event_type: str,
    result: str,
    next_entry: dict | None,
    receipt_id: str | None = None,
    stop_decision: str | None = None,
    blocker_code: str | None = None,
) -> dict:
    return {
        "schema_version": "1.1.0",
        "action_id": action["action_id"],
        "event_type": event_type,
        "receipt_id": receipt_id,
        "session_id": action["task_session_id"],
        "result": result,
        "selected_unit": action["selected_unit"],
        "route_fingerprint": (
            None
            if event_type == "selection-materialized"
            else state["current_binding"]["route_fingerprint"]
        ),
        "next_entry": copy.deepcopy(next_entry),
        "stop_decision": stop_decision,
        "blocker_code": blocker_code,
        "authority_effect": "none",
    }


def assert_zero_prompt(state: dict, action: dict) -> None:
    if state["authorization_prompt_count"] != 0:
        raise AssertionError("outer loop recorded an authorization prompt")
    if action["authorization_prompt_required"]:
        raise AssertionError("outer-loop action requested authorization")


def test_selection_to_one_unit() -> None:
    policy = base_policy()
    state = init(policy, entry(policy, "selection-ready"))
    state, select_action = decide_next_action(
        state, policy, available_inputs=[], installed_owner_routes=installed()
    )
    assert select_action["action_type"] == "select-unit"
    assert_zero_prompt(state, select_action)
    state = join_event(
        state,
        policy,
        event(
            select_action,
            state,
            event_type="selection-materialized",
            result="pass",
            next_entry=entry(policy, "task-ready", 0),
        ),
    )
    state, task_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    assert task_action["action_type"] == "start-task-session"
    assert task_action["authorization_source"] == "work-pack-binding"
    assert_zero_prompt(state, task_action)
    state = join_event(
        state,
        policy,
        event(
            task_action,
            state,
            event_type="task-session-joined",
            result="pass",
            next_entry=None,
            receipt_id="receipt-task-one-unit",
        ),
    )
    validate_outer_loop_state(state, policy)
    assert state["phase"] == "complete"
    assert state["visited_units"] == ["SWU-GENERIC-001"]
    assert len(state["task_session_receipts"]) == 1
    assert state["owner_receipts"] == []
    print("PASS: selection-ready reaches one fresh Task Session without Refresh")


def test_owner_then_task() -> None:
    policy = base_policy()
    state = init(policy, entry(policy, "owner-prerequisite"))
    state, owner_action = decide_next_action(
        state,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert owner_action["action_type"] == "route-owner"
    assert_zero_prompt(state, owner_action)
    state = join_event(
        state,
        policy,
        event(
            owner_action,
            state,
            event_type="owner-joined",
            result="pass",
            next_entry=entry(policy, "task-ready", 0),
            receipt_id="receipt-owner-one",
        ),
    )
    state, task_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    state = join_event(
        state,
        policy,
        event(
            task_action,
            state,
            event_type="task-session-joined",
            result="pass",
            next_entry=None,
            receipt_id="receipt-task-after-owner",
        ),
    )
    assert state["phase"] == "complete"
    assert len(state["owner_receipts"]) == 1
    assert len(state["task_session_receipts"]) == 1
    assert state["owner_receipts"][0]["receipt_id"] != state["task_session_receipts"][0]["receipt_id"]
    print("PASS: owner and Task Session receipts remain separate")


def test_two_unit_frontier() -> None:
    policy = base_policy()
    state = init(
        policy,
        entry(policy, "task-ready", 0),
        execution_mode="finite-frontier",
    )
    state, first_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    state = join_event(
        state,
        policy,
        event(
            first_action,
            state,
            event_type="task-session-joined",
            result="pass",
            next_entry=entry(policy, "task-ready", 1),
            receipt_id="receipt-task-frontier-one",
        ),
    )
    state, second_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-2"],
        installed_owner_routes=installed(),
    )
    assert first_action["task_session_id"] != second_action["task_session_id"]
    state = join_event(
        state,
        policy,
        event(
            second_action,
            state,
            event_type="task-session-joined",
            result="pass",
            next_entry=None,
            receipt_id="receipt-task-frontier-two",
        ),
    )
    assert state["phase"] == "complete"
    assert state["visited_units"] == policy["frontier"]
    assert len({item["session_id"] for item in state["task_session_receipts"]}) == 2
    print("PASS: finite frontier uses two distinct fresh Task Sessions")


def test_historical_completion_continuity() -> None:
    frontier = ["SWU-GENERIC-001", "SWU-GENERIC-002", "SWU-GENERIC-003"]
    policy = base_policy(frontier)
    policy["completion_continuity"] = completion_continuity(
        frontier, policy["work_pack_semantic_digest"], completed_count=2
    )
    state = init(policy, entry(policy, "selection-ready"))
    assert state["visited_units"] == []
    assert [
        item["unit_id"]
        for item in state["completion_continuity"]["completed_prefix"]
    ] == frontier[:2]
    state, action = decide_next_action(
        state, policy, available_inputs=[], installed_owner_routes=installed()
    )
    assert action["action_type"] == "select-unit"
    assert action["selected_unit"] == frontier[2]

    try:
        init(policy, entry(policy, "task-ready", unit_index=0))
    except OuterLoopError as error:
        assert error.code == "CONTINUITY_CURSOR_CONTRADICTION"
    else:
        raise AssertionError("historically completed unit was accepted for replay")

    completed_policy = base_policy(frontier)
    completed_policy["completion_continuity"] = completion_continuity(
        frontier,
        completed_policy["work_pack_semantic_digest"],
        completed_count=len(frontier),
    )
    completed_state = init(
        completed_policy, entry(completed_policy, "selection-ready")
    )
    completed_state, completed_action = decide_next_action(
        completed_state,
        completed_policy,
        available_inputs=[],
        installed_owner_routes=installed(),
    )
    assert completed_state["phase"] == "complete"
    assert completed_action["stop_reason"] == "FRONTIER_COMPLETE"

    tampered = copy.deepcopy(state)
    tampered["completion_continuity"]["completed_prefix"].reverse()
    try:
        validate_outer_loop_state(tampered, policy)
    except OuterLoopError as error:
        assert error.code in {
            "CONTINUITY_POLICY_STATE_MISMATCH",
            "CONTINUITY_NON_PREFIX_COMPLETION",
        }
    else:
        raise AssertionError("tampered historical completion prefix was accepted")
    print("PASS: historical completion stays separate and advances one cursor")


def test_stop_classes() -> None:
    policy = base_policy()
    for decision in STOP_DECISIONS:
        state = init(policy, entry(policy, "selection-ready"))
        state = set_stop_decision(state, policy, decision)
        state, action = decide_next_action(
            state, policy, available_inputs=[], installed_owner_routes=installed()
        )
        assert state["phase"] == "blocked"
        assert action["action_type"] == "stop"
        assert action["stop_reason"] == decision
        assert state["steps_used"] == 0
        assert_zero_prompt(state, action)
        print(f"PASS: stop class -> {decision}")


def test_router_blocks_and_cycles() -> None:
    policy = base_policy()
    missing = init(policy, entry(policy, "owner-prerequisite"))
    missing, action = decide_next_action(
        missing, policy, available_inputs=[], installed_owner_routes=installed()
    )
    assert missing["phase"] == "blocked"
    assert action["stop_reason"] == "ROUTE_INPUT_MISSING"
    assert missing["steps_used"] == 0

    unknown = init(policy, entry(policy, "owner-prerequisite"))
    unknown, action = decide_next_action(
        unknown,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=[{"capability": "task-session", "mode": "execute"}],
    )
    assert unknown["phase"] == "blocked"
    assert action["stop_reason"] == "OWNER_ROUTE_UNKNOWN"

    cycle = init(policy, entry(policy, "owner-prerequisite"))
    cycle, owner_action = decide_next_action(
        cycle,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    cycle = join_event(
        cycle,
        policy,
        event(
            owner_action,
            cycle,
            event_type="owner-joined",
            result="pass",
            next_entry=entry(policy, "owner-prerequisite"),
            receipt_id="receipt-owner-cycle",
        ),
    )
    cycle, action = decide_next_action(
        cycle,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert cycle["phase"] == "blocked"
    assert action["stop_reason"] == "ROUTE_FINGERPRINT_REPEATED"
    print("PASS: missing input, unknown owner, and repeated route all block")


def test_budget_join_and_correlation() -> None:
    policy = base_policy()
    state = init(policy, entry(policy, "owner-prerequisite"), step_budget=1)
    state, owner_action = decide_next_action(
        state,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    awaiting = copy.deepcopy(state)
    awaiting, stop_action = decide_next_action(
        awaiting,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert awaiting["phase"] == "blocked"
    assert stop_action["stop_reason"] == "JOIN_REQUIRED"

    mismatch = event(
        owner_action,
        state,
        event_type="owner-joined",
        result="pass",
        next_entry=entry(policy, "task-ready", 0),
        receipt_id="receipt-owner-correlation",
    )
    mismatch["action_id"] = "wpoa-000000000000000000000000"
    try:
        join_event(state, policy, mismatch)
    except OuterLoopError as error:
        assert error.code == "ACTION_CORRELATION_MISMATCH"
    else:
        raise AssertionError("mismatched action correlation was accepted")

    state = join_event(
        state,
        policy,
        event(
            owner_action,
            state,
            event_type="owner-joined",
            result="pass",
            next_entry=entry(policy, "task-ready", 0),
            receipt_id="receipt-owner-budget",
        ),
    )
    state, action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    assert state["phase"] == "blocked"
    assert action["stop_reason"] == "STEP_BUDGET_EXHAUSTED"
    print("PASS: missing join, action mismatch, and budget exhaustion block")


def test_owner_failure_and_frontier_absorption() -> None:
    policy = base_policy()
    state = init(policy, entry(policy, "owner-prerequisite"))
    state, owner_action = decide_next_action(
        state,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    failed = join_event(
        state,
        policy,
        event(
            owner_action,
            state,
            event_type="owner-joined",
            result="block",
            next_entry=None,
            receipt_id="receipt-owner-failed",
            blocker_code="OWNER_VALIDATION_FAILED",
        ),
    )
    assert failed["phase"] == "blocked"
    assert failed["owner_receipts"][0]["result"] == "block"

    state = init(
        policy,
        entry(policy, "task-ready", 0),
        execution_mode="finite-frontier",
    )
    state, task_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    foreign = copy.deepcopy(entry(policy, "task-ready", 1))
    foreign["selected_unit"] = "SWU-FOREIGN-003"
    try:
        join_event(
            state,
            policy,
            event(
                task_action,
                state,
                event_type="task-session-joined",
                result="pass",
                next_entry=foreign,
                receipt_id="receipt-task-foreign",
            ),
        )
    except OuterLoopError as error:
        assert error.code == "FRONTIER_ABSORPTION_BLOCKED"
    else:
        raise AssertionError("outer loop absorbed an uncaptured unit")
    print("PASS: owner failure blocks and captured frontier cannot expand")


def test_failed_critical_validation_and_cli() -> None:
    policy = base_policy()
    state = init(policy, entry(policy, "task-ready", 0))
    state, task_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    state = join_event(
        state,
        policy,
        event(
            task_action,
            state,
            event_type="task-session-joined",
            result="block",
            next_entry=None,
            receipt_id="receipt-task-critical-failure",
            stop_decision="failed-acceptance-critical-validation",
            blocker_code="CRITICAL_VALIDATION_FAILED",
        ),
    )
    assert state["phase"] == "blocked"
    assert state["stop_reason"] == "failed-acceptance-critical-validation"

    with tempfile.TemporaryDirectory(prefix="wpeg-outer-loop-") as temporary:
        root = Path(temporary)
        request_path = root / "request.json"
        output_path = root / "output.json"
        request_path.write_text(
            json.dumps(
                {
                    "operation": "initialize",
                    "policy": policy,
                    "entry": entry(policy, "selection-ready"),
                    "source_invocation_id": "invoke-cli-generic-001",
                    "created_at": "2026-08-04T00:00:00Z",
                    "execution_mode": "one-unit",
                    "step_budget": 4,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(SPELL_ROOT / "scripts" / "run_execution_loop.py"),
                "--request",
                str(request_path),
                "--output",
                str(output_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise AssertionError(f"outer-loop CLI failed: {completed.stderr}")
        result = json.loads(output_path.read_text(encoding="utf-8"))
        validate_outer_loop_state(result["state"], policy)
    print("PASS: failed critical validation stops and CLI initializes current state")


def test_one_declared_same_route_retry() -> None:
    policy = base_policy(["SWU-GENERIC-001"])
    policy["automatic_decisions"].append("declared-retry")
    state = init(policy, entry(policy, "owner-prerequisite"), step_budget=4)
    state, owner_action = decide_next_action(
        state,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert state["steps_used"] == 1
    original_binding = copy.deepcopy(state["current_binding"])
    original_route = copy.deepcopy(owner_action["owner_route"])
    original_unit = owner_action["selected_unit"]
    retry_entry = copy.deepcopy(state["current_entry"])
    state = join_event(
        state,
        policy,
        event(
            owner_action,
            state,
            event_type="owner-joined",
            result="retry",
            next_entry=retry_entry,
            receipt_id="receipt-owner-repairable-one",
            blocker_code="REPAIRABLE_OWNER_CONDITION",
        ),
    )
    pending_retry = state["pending_retry"]
    assert pending_retry is not None
    fingerprint = pending_retry["route_fingerprint"]
    assert state["phase"] == "ready"
    assert state["route_retry_counts"] == {fingerprint: 1}
    assert fingerprint in state["consumed_route_fingerprints"]
    assert pending_retry["blocker_code"] == "REPAIRABLE_OWNER_CONDITION"
    assert pending_retry["owner_receipt_id"] == "receipt-owner-repairable-one"
    pending_state = copy.deepcopy(state)
    preserved_history = copy.deepcopy(state["consumed_route_fingerprints"])

    state, retry_action = decide_next_action(
        state,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert retry_action["action_type"] == "route-owner"
    assert retry_action["automatic_decision"] == "declared-retry"
    assert retry_action["authorization_prompt_required"] is False
    assert retry_action["owner_route"] == original_route
    assert retry_action["selected_unit"] == original_unit
    assert state["current_binding"] == original_binding
    assert state["steps_used"] == 2
    assert state["automatic_decisions"][-1]["decision_class"] == "declared-retry"
    assert state["consumed_route_fingerprints"] == preserved_history
    assert state["pending_retry"] is None
    state = join_event(
        state,
        policy,
        event(
            retry_action,
            state,
            event_type="owner-joined",
            result="pass",
            next_entry=entry(policy, "task-ready"),
            receipt_id="receipt-owner-retry-passed",
        ),
    )
    state, task_action = decide_next_action(
        state,
        policy,
        available_inputs=["task-input-1"],
        installed_owner_routes=installed(),
    )
    state = join_event(
        state,
        policy,
        event(
            task_action,
            state,
            event_type="task-session-joined",
            result="pass",
            next_entry=None,
            receipt_id="receipt-task-after-declared-retry",
        ),
    )
    assert state["phase"] == "complete"
    assert [item["result"] for item in state["owner_receipts"]] == [
        "retry",
        "pass",
    ]

    exhausted = init(policy, entry(policy, "owner-prerequisite"), step_budget=4)
    exhausted, first_action = decide_next_action(
        exhausted,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    exhausted = join_event(
        exhausted,
        policy,
        event(
            first_action,
            exhausted,
            event_type="owner-joined",
            result="retry",
            next_entry=copy.deepcopy(exhausted["current_entry"]),
            receipt_id="receipt-owner-repairable-budget-one",
            blocker_code="REPAIRABLE_OWNER_CONDITION",
        ),
    )
    exhausted, second_action = decide_next_action(
        exhausted,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    exhausted = join_event(
        exhausted,
        policy,
        event(
            second_action,
            exhausted,
            event_type="owner-joined",
            result="retry",
            next_entry=copy.deepcopy(exhausted["current_entry"]),
            receipt_id="receipt-owner-repairable-budget-two",
            blocker_code="REPAIRABLE_OWNER_CONDITION",
        ),
    )
    assert exhausted["phase"] == "blocked"
    assert exhausted["stop_reason"] == "DECLARED_RETRY_EXHAUSTED"
    assert exhausted["steps_used"] == 2
    assert len(exhausted["owner_receipts"]) == 2
    assert len(
        [
            decision
            for decision in exhausted["automatic_decisions"]
            if decision["action_type"] == "route-owner"
        ]
    ) == 2
    assert exhausted["consumed_route_fingerprints"] == [
        exhausted["current_binding"]["route_fingerprint"]
    ]
    terminal_state, no_third_dispatch = decide_next_action(
        exhausted,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert no_third_dispatch["action_type"] == "stop"
    assert terminal_state["steps_used"] == 2
    assert len(terminal_state["owner_receipts"]) == 2

    budgeted = init(
        policy,
        entry(policy, "owner-prerequisite"),
        step_budget=1,
    )
    budgeted, budget_action = decide_next_action(
        budgeted,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    budgeted = join_event(
        budgeted,
        policy,
        event(
            budget_action,
            budgeted,
            event_type="owner-joined",
            result="retry",
            next_entry=copy.deepcopy(budgeted["current_entry"]),
            receipt_id="receipt-owner-repairable-step-budget",
            blocker_code="REPAIRABLE_OWNER_CONDITION",
        ),
    )
    budgeted_history = copy.deepcopy(budgeted["consumed_route_fingerprints"])
    budgeted, budget_stop = decide_next_action(
        budgeted,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    assert budget_stop["action_type"] == "stop"
    assert budget_stop["stop_reason"] == "STEP_BUDGET_EXHAUSTED"
    assert budgeted["steps_used"] == 1
    assert budgeted["consumed_route_fingerprints"] == budgeted_history

    undeclared_policy = base_policy(["SWU-GENERIC-001"])
    undeclared = init(
        undeclared_policy, entry(undeclared_policy, "owner-prerequisite")
    )
    undeclared, undeclared_action = decide_next_action(
        undeclared,
        undeclared_policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    undeclared = join_event(
        undeclared,
        undeclared_policy,
        event(
            undeclared_action,
            undeclared,
            event_type="owner-joined",
            result="retry",
            next_entry=copy.deepcopy(undeclared["current_entry"]),
            receipt_id="receipt-owner-undeclared-retry",
            blocker_code="REPAIRABLE_OWNER_CONDITION",
        ),
    )
    assert undeclared["phase"] == "blocked"
    assert undeclared["stop_reason"] == "RETRY_UNDECLARED"

    wrong_unit = init(policy, entry(policy, "owner-prerequisite"))
    wrong_unit, wrong_unit_action = decide_next_action(
        wrong_unit,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    wrong_unit_event = event(
        wrong_unit_action,
        wrong_unit,
        event_type="owner-joined",
        result="retry",
        next_entry=copy.deepcopy(wrong_unit["current_entry"]),
        receipt_id="receipt-owner-wrong-unit-retry",
        blocker_code="REPAIRABLE_OWNER_CONDITION",
    )
    wrong_unit_event["selected_unit"] = "SWU-GENERIC-FOREIGN"
    try:
        join_event(wrong_unit, policy, wrong_unit_event)
    except OuterLoopError as error:
        assert error.code == "OWNER_UNIT_MISMATCH"
    else:
        raise AssertionError("declared retry changed the selected unit")

    changed = init(policy, entry(policy, "owner-prerequisite"))
    changed, changed_action = decide_next_action(
        changed,
        policy,
        available_inputs=["owner-input-1"],
        installed_owner_routes=installed(),
    )
    try:
        join_event(
            changed,
            policy,
            event(
                changed_action,
                changed,
                event_type="owner-joined",
                result="retry",
                next_entry=entry(policy, "task-ready"),
                receipt_id="receipt-owner-changed-retry",
                blocker_code="REPAIRABLE_OWNER_CONDITION",
            ),
        )
    except OuterLoopError as error:
        assert error.code == "RETRY_ROUTE_CHANGED"
    else:
        raise AssertionError("declared retry changed the bound route")

    tampered = copy.deepcopy(pending_state)
    tampered["pending_retry"] = {
        "route_fingerprint": fingerprint,
        "blocker_code": "REPAIRABLE_OWNER_CONDITION",
        "owner_receipt_id": "receipt-owner-does-not-exist",
    }
    try:
        validate_outer_loop_state(tampered, policy)
    except OuterLoopError as error:
        assert error.code == "PENDING_RETRY_INVALID"
    else:
        raise AssertionError("pending retry accepted an uncorrelated owner receipt")
    print("PASS: one declared same-route retry is automatic and bounded")


def main() -> int:
    test_selection_to_one_unit()
    test_owner_then_task()
    test_two_unit_frontier()
    test_historical_completion_continuity()
    test_stop_classes()
    test_router_blocks_and_cycles()
    test_budget_join_and_correlation()
    test_owner_failure_and_frontier_absorption()
    test_failed_critical_validation_and_cli()
    test_one_declared_same_route_retry()
    print("OUTER_LOOP_VALIDATION=pass")
    print("AUTHORIZATION_PROMPT_COUNT=0")
    print("STOP_CLASS_COUNT=8")
    print("FRESH_TASK_SESSION_COUNT=4")
    print("DECLARED_RETRY_LIMIT=1")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OuterLoopError, json.JSONDecodeError) as error:
        print("OUTER_LOOP_VALIDATION=block", file=sys.stderr)
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

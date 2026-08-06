#!/usr/bin/env python3
"""Public-safe causal proof for Work-Pack-bound execution without hop prompts."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


INTEGRATION_ROOT = Path(__file__).resolve().parent
OBSERVABILITY_PATH = INTEGRATION_ROOT / "work-pack-execution-observability.json"
READINESS_ROOT = INTEGRATION_ROOT.parents[1]
ARCANUM_ROOT = READINESS_ROOT.parents[1]
OUTER_VALIDATOR_PATH = READINESS_ROOT / "development" / "validate-outer-loop.py"
READINESS_EXECUTION_PATH = READINESS_ROOT / "scripts" / "readiness_execution.py"
PLAN_ONCE_PATH = (
    ARCANUM_ROOT
    / "spells"
    / "work-pack-readiness-audit"
    / "development"
    / "test_plan_once_end_to_end.py"
)
FAST_GUARD_PATH = (
    ARCANUM_ROOT
    / "arcana"
    / "task-session"
    / "scripts"
    / "fast_execution_entry_guard.py"
)
ROUTER_PATH = (
    ARCANUM_ROOT
    / "arcana"
    / "continuation-router"
    / "scripts"
    / "work_pack_route.py"
)
ROUTER_ROOT = ARCANUM_ROOT / "arcana" / "continuation-router"
LEGACY_VALIDATOR_PATH = ROUTER_ROOT / "development" / "validate-route-fixtures.py"
FRESH_SESSION_TEST_PATH = (
    ARCANUM_ROOT
    / "spells"
    / "task-session-until-blocker"
    / "development"
    / "test-fresh-session-resume.py"
)


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# Load in dependency order so canonical modules, rather than similarly named
# development helpers, own the bare imports used by the packages.
OUTER = load_module("wpeg_integration_outer", OUTER_VALIDATOR_PATH)
READINESS = load_module("wpeg_integration_readiness", READINESS_EXECUTION_PATH)
PLAN_ONCE = load_module("wpeg_integration_plan_once", PLAN_ONCE_PATH)
FAST_GUARD = load_module("wpeg_integration_fast_guard", FAST_GUARD_PATH)
ROUTER = load_module("wpeg_integration_router", ROUTER_PATH)
LEGACY = load_module("wpeg_integration_legacy_router", LEGACY_VALIDATOR_PATH)
FRESH = load_module("wpeg_integration_fresh_session", FRESH_SESSION_TEST_PATH)


def assert_no_prompt(test: unittest.TestCase, state: dict, *actions: dict) -> None:
    test.assertEqual(state["authorization_prompt_count"], 0)
    for action in actions:
        test.assertFalse(action["authorization_prompt_required"])


def route_request(
    policy: dict,
    state: dict,
    candidate: dict,
    *,
    available_inputs: list[str],
) -> dict:
    return {
        "schema_version": "1.0.0",
        "execution_policy": copy.deepcopy(policy),
        "execution_entry": copy.deepcopy(state["current_entry"]),
        "execution_binding": copy.deepcopy(state["current_binding"]),
        "candidate_routes": [copy.deepcopy(candidate)],
        "installed_owner_routes": OUTER.installed(),
        "available_inputs": copy.deepcopy(available_inputs),
        "consumed_route_fingerprints": [],
        "authorization_flag": None,
        "authority_effect": "none",
    }


def build_plan_once_selection_and_admission(
    plan_case,
    admission_case,
    config: dict,
    report: dict,
    execution_binding: dict,
    *,
    output_name: str = "audit-output",
) -> tuple[dict, dict]:
    """Produce real selection and live mutation-admission evidence for one audit."""

    config_path = plan_case.fixture.root / "plan-config.json"
    config_path.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    output = plan_case.fixture.root / output_name
    PLAN_ONCE.PLAN.AUDIT.write_outputs_v2(report, output)
    selection_request = {
        "schemaVersion": "1.0.0",
        "manifestRef": PLAN_ONCE.PLAN.exact(
            plan_case.fixture.root, f"{output_name}/plan-semantic-manifest.json"
        ),
        "auditConfigPath": "plan-config.json",
        "taskId": "TASK-U1",
        "swuId": "SWU-U1",
        "executionIntentBinding": READINESS.selection_intent_projection(
            execution_binding
        ),
        "dependencyReceipts": [],
        "lifecycleEligibility": {
            "eligible": True,
            "state": "selected",
            "evidenceRefs": [plan_case.fixture.exact()],
        },
    }
    selection = PLAN_ONCE.PLAN.SELECT.select_unit(
        selection_request,
        plan_case.fixture.root,
        PLAN_ONCE.PLAN.AUDIT.load_json(
            PLAN_ONCE.SPELL_ROOT / "schemas/selection-request.schema.json"
        ),
        PLAN_ONCE.PLAN.AUDIT.load_json(
            PLAN_ONCE.SPELL_ROOT / "schemas/plan-semantic-manifest.schema.json"
        ),
        PLAN_ONCE.PLAN.AUDIT.load_json(PLAN_ONCE.PLAN.AUDIT.CONFIG_SCHEMA_V2),
    )
    PLAN_ONCE.ADMISSION.write_json(
        plan_case.fixture.root / "selection-receipt.json", selection
    )

    request = admission_case.build_request()
    shutil.copyfile(
        output / "plan-semantic-manifest.json",
        admission_case.root / "plan-manifest.json",
    )
    shutil.copyfile(
        plan_case.fixture.root / "selection-receipt.json",
        admission_case.root / "selection-receipt.json",
    )
    epoch = report["manifest"]["plan_epoch_id"]
    unit_digest = report["manifest"]["unit_contract_digests"]["U1"]
    selection_digest = hashlib.sha256(
        (admission_case.root / "selection-receipt.json").read_bytes()
    ).hexdigest()
    package_path = admission_case.root / "material-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package["plan_binding"].update(
        plan_epoch_id=epoch,
        unit_contract_digest=unit_digest,
        selection_receipt_digest=selection_digest,
    )
    producer_receipt = PLAN_ONCE.ADMISSION.PRODUCER.validate_material_package(
        package,
        admission_case.root,
        json.loads(
            (
                PLAN_ONCE.ADMISSION.INVOKE
                / "schemas/material-package.schema.json"
            ).read_text(encoding="utf-8")
        ),
        json.loads(
            (
                PLAN_ONCE.ADMISSION.INVOKE
                / "schemas/material-package-receipt.schema.json"
            ).read_text(encoding="utf-8")
        ),
    )
    PLAN_ONCE.ADMISSION.write_json(package_path, package)
    PLAN_ONCE.ADMISSION.write_json(
        admission_case.root / "material-receipt.json", producer_receipt
    )
    request["materialPackage"] = PLAN_ONCE.ADMISSION.exact(
        admission_case.root, "material-package.json"
    )
    request["materialReceipt"] = PLAN_ONCE.ADMISSION.exact(
        admission_case.root, "material-receipt.json"
    )
    request["planAdmission"].update(
        planManifest=PLAN_ONCE.ADMISSION.exact(
            admission_case.root, "plan-manifest.json"
        ),
        selectionReceipt=PLAN_ONCE.ADMISSION.exact(
            admission_case.root, "selection-receipt.json"
        ),
        planEpochId=epoch,
        unitContractDigest=unit_digest,
    )
    admission = admission_case.resolve(request)
    return selection, admission


class WorkPackExecutionIntegrationTests(unittest.TestCase):
    def test_01_plan_once_selects_and_admits_without_pre_execution_refresh(self) -> None:
        plan_case = PLAN_ONCE.PLAN.PlanOnceSelectionTests()
        admission_case = PLAN_ONCE.ADMISSION.PlanOnceAdmissionTests()
        plan_case.setUp()
        admission_case.setUp()
        try:
            config = plan_case.config()
            report = plan_case.audit(config)
            policy, state = READINESS.initialize_from_readiness(
                config,
                report,
                source_invocation_id="invoke-plan-once-integration-001",
                created_at="2026-08-04T00:00:00Z",
                execution_mode="one-unit",
                step_budget=4,
            )
            self.assertEqual(state["current_entry"]["entry_state"], "selection-ready")
            state, select_action = OUTER.decide_next_action(
                state,
                policy,
                available_inputs=[],
                installed_owner_routes=OUTER.installed(),
            )
            selection_binding = copy.deepcopy(state["current_binding"])
            selection, admission = build_plan_once_selection_and_admission(
                plan_case,
                admission_case,
                config,
                report,
                selection_binding,
            )
            task_entry = READINESS.compile_plan_once_task_entry(
                policy,
                config,
                report,
                selection,
                admission,
                selection_binding,
            )
            state = OUTER.join_event(
                state,
                policy,
                OUTER.event(
                    select_action,
                    state,
                    event_type="selection-materialized",
                    result="pass",
                    next_entry=task_entry,
                ),
            )
            task_route = state["current_binding"]["current_route"]
            state, task_action = OUTER.decide_next_action(
                state,
                policy,
                available_inputs=task_route["required_inputs"],
                installed_owner_routes=OUTER.installed(),
            )
            state = OUTER.join_event(
                state,
                policy,
                OUTER.event(
                    task_action,
                    state,
                    event_type="task-session-joined",
                    result="pass",
                    next_entry=None,
                    receipt_id="task-plan-once-integration-001",
                ),
            )
            self.assertEqual(state["phase"], "complete")
            self.assertEqual(state["source_invocation_id"], "invoke-plan-once-integration-001")
            self.assertEqual(state["owner_receipts"], [])
            self.assertEqual(len(state["task_session_receipts"]), 1)
            self.assertEqual(
                selection["selectionIntentDigest"],
                READINESS.canonical_digest(
                    READINESS.selection_intent_projection(selection_binding)
                ),
            )
            self.assertFalse(
                any(
                    item["action_type"] == "route-owner"
                    for item in state["automatic_decisions"]
                )
            )
            assert_no_prompt(self, state, select_action, task_action)
        finally:
            admission_case.tearDown()
            plan_case.tearDown()

    def test_02_semantic_drift_routes_refresh_rejoins_and_starts_task(self) -> None:
        plan_case = PLAN_ONCE.PLAN.PlanOnceSelectionTests()
        admission_case = PLAN_ONCE.ADMISSION.PlanOnceAdmissionTests()
        plan_case.setUp()
        admission_case.setUp()
        try:
            current_config = plan_case.config()
            current_report = plan_case.audit(current_config)
            expected_digest = current_report["canonical_semantic_digest"]

            drifted_config = copy.deepcopy(current_config)
            drifted_config["execution_bindings"][0]["command"]["cwd"] = "changed"
            drifted_config["expected_semantic_digest"] = expected_digest
            drifted_report = plan_case.audit(drifted_config)
            self.assertEqual(
                {item["code"] for item in drifted_report["blockers"]},
                {"EPOCH_INVALIDATED_SEMANTIC_CHANGE"},
            )
            policy, state = READINESS.initialize_from_readiness(
                drifted_config,
                drifted_report,
                source_invocation_id="invoke-semantic-repair-integration-001",
                created_at="2026-08-04T00:00:00Z",
                execution_mode="one-unit",
                step_budget=5,
            )
            self.assertEqual(state["current_entry"]["entry_state"], "owner-prerequisite")
            owner_route = state["current_binding"]["current_route"]
            state, owner_action = OUTER.decide_next_action(
                state,
                policy,
                available_inputs=owner_route["required_inputs"],
                installed_owner_routes=OUTER.installed(),
            )
            self.assertEqual(owner_action["action_type"], "route-owner")
            self.assertEqual(owner_action["owner_route"]["route_id"], "invoke-refresh-U1")
            self.assertEqual(owner_action["owner_route"]["capability"], "invoke")
            self.assertEqual(owner_action["owner_route"]["mode"], "refresh")

            repaired_config = copy.deepcopy(current_config)
            repaired_config["expected_semantic_digest"] = expected_digest
            repaired_report = plan_case.audit(repaired_config)
            repaired_entry = READINESS.compile_readiness_entry(
                policy, repaired_report
            )
            state = OUTER.join_event(
                state,
                policy,
                OUTER.event(
                    owner_action,
                    state,
                    event_type="owner-joined",
                    result="pass",
                    next_entry=repaired_entry,
                    receipt_id="owner-semantic-refresh-001",
                ),
            )
            state, select_action = OUTER.decide_next_action(
                state,
                policy,
                available_inputs=[],
                installed_owner_routes=OUTER.installed(),
            )
            selection, admission = build_plan_once_selection_and_admission(
                plan_case,
                admission_case,
                repaired_config,
                repaired_report,
                state["current_binding"],
            )
            with self.assertRaises(READINESS.ReadinessExecutionError) as stale_intent:
                READINESS.compile_plan_once_task_entry(
                    policy,
                    repaired_config,
                    repaired_report,
                    selection,
                    admission,
                    state["current_binding"],
                )
            self.assertEqual(
                stale_intent.exception.code, "CONTINUITY_POLICY_STATE_MISMATCH"
            )

            repaired_policy, repaired_state = READINESS.initialize_from_readiness(
                repaired_config,
                repaired_report,
                source_invocation_id="invoke-semantic-repair-integration-002",
                created_at="2026-08-04T00:01:00Z",
                execution_mode="one-unit",
                step_budget=5,
            )
            repaired_state, repaired_select_action = OUTER.decide_next_action(
                repaired_state,
                repaired_policy,
                available_inputs=[],
                installed_owner_routes=OUTER.installed(),
            )
            repaired_selection, repaired_admission = (
                build_plan_once_selection_and_admission(
                    plan_case,
                    admission_case,
                    repaired_config,
                    repaired_report,
                    repaired_state["current_binding"],
                    output_name="audit-output-repaired",
                )
            )
            task_entry = READINESS.compile_plan_once_task_entry(
                repaired_policy,
                repaired_config,
                repaired_report,
                repaired_selection,
                repaired_admission,
                repaired_state["current_binding"],
            )
            repaired_state = OUTER.join_event(
                repaired_state,
                repaired_policy,
                OUTER.event(
                    repaired_select_action,
                    repaired_state,
                    event_type="selection-materialized",
                    result="pass",
                    next_entry=task_entry,
                ),
            )
            task_route = repaired_state["current_binding"]["current_route"]
            repaired_state, task_action = OUTER.decide_next_action(
                repaired_state,
                repaired_policy,
                available_inputs=task_route["required_inputs"],
                installed_owner_routes=OUTER.installed(),
            )
            repaired_state = OUTER.join_event(
                repaired_state,
                repaired_policy,
                OUTER.event(
                    task_action,
                    repaired_state,
                    event_type="task-session-joined",
                    result="pass",
                    next_entry=None,
                    receipt_id="task-after-semantic-refresh-001",
                ),
            )
            self.assertEqual(repaired_state["phase"], "complete")
            self.assertEqual(len(state["owner_receipts"]), 1)
            self.assertEqual(len(repaired_state["task_session_receipts"]), 1)
            self.assertNotEqual(
                state["owner_receipts"][0]["receipt_id"],
                repaired_state["task_session_receipts"][0]["receipt_id"],
            )
            self.assertEqual(
                repaired_state["source_invocation_id"],
                "invoke-semantic-repair-integration-002",
            )
            assert_no_prompt(self, state, owner_action, select_action)
            assert_no_prompt(
                self, repaired_state, repaired_select_action, task_action
            )
        finally:
            admission_case.tearDown()
            plan_case.tearDown()

    def test_03_mechanical_selection_owner_and_task_choices_never_prompt(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "selection-ready"))
        actions = []

        state, action = OUTER.decide_next_action(
            state, policy, available_inputs=[], installed_owner_routes=OUTER.installed()
        )
        actions.append(action)
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                action,
                state,
                event_type="selection-materialized",
                result="pass",
                next_entry=OUTER.entry(policy, "owner-prerequisite"),
            ),
        )
        state, action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["owner-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        actions.append(action)
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                action,
                state,
                event_type="owner-joined",
                result="pass",
                next_entry=OUTER.entry(policy, "task-ready"),
                receipt_id="owner-mechanical-001",
            ),
        )
        state, action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["task-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        actions.append(action)
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                action,
                state,
                event_type="task-session-joined",
                result="pass",
                next_entry=None,
                receipt_id="task-mechanical-001",
            ),
        )
        self.assertEqual(
            [item["action_type"] for item in state["automatic_decisions"]],
            ["select-unit", "route-owner", "start-task-session"],
        )
        observability = json.loads(OBSERVABILITY_PATH.read_text(encoding="utf-8"))
        self.assertFalse(observability["authoritative"])
        self.assertEqual(observability["authority_effect"], "none")
        self.assertEqual(observability["authorization_prompt_count"], 0)
        self.assertEqual(observability["protected_effect_count"], 0)
        self.assertEqual(len(observability["entry_states"]), 4)
        self.assertEqual(len(observability["automatic_decisions"]), 4)
        self.assertEqual(len(observability["stop_decisions"]), 8)
        self.assertEqual(
            observability["fast_guard"],
            {
                "logical_read_count": 4,
                "phase_count": 1,
                "mutation_count": 0,
                "owner_hops_dispatched": 0,
            },
        )
        self.assertEqual(
            observability["causal_lanes"]["declared_owner_retry"],
            {
                "route_hop_count": 3,
                "owner_join_count": 2,
                "declared_retry_count": 1,
                "task_session_join_count": 1,
                "fingerprint_history_release_count": 0,
                "authorization_prompt_count": 0,
            },
        )
        assert_no_prompt(self, state, *actions)

    def test_04_two_unit_frontier_uses_two_distinct_task_sessions(self) -> None:
        historical_frontier = [
            "SWU-GENERIC-001",
            "SWU-GENERIC-002",
            "SWU-GENERIC-003",
        ]
        historical_policy = OUTER.base_policy(historical_frontier)
        historical_policy["completion_continuity"] = OUTER.completion_continuity(
            historical_frontier,
            historical_policy["work_pack_semantic_digest"],
            completed_count=2,
        )
        historical_state = OUTER.init(
            historical_policy,
            OUTER.entry(historical_policy, "selection-ready"),
            execution_mode="finite-frontier",
        )
        self.assertEqual(
            READINESS.expected_fresh_resume_session_budget(historical_state),
            {
                "captured_max_task_sessions": 1,
                "current_max_task_sessions": 1,
                "task_sessions_started": 0,
            },
        )

        policy = OUTER.base_policy()
        state = OUTER.init(
            policy,
            OUTER.entry(policy, "task-ready", 0),
            execution_mode="finite-frontier",
        )
        sessions = []
        for index in range(2):
            state, action = OUTER.decide_next_action(
                state,
                policy,
                available_inputs=[f"task-input-{index + 1}"],
                installed_owner_routes=OUTER.installed(),
            )
            sessions.append(action["task_session_id"])
            next_entry = (
                OUTER.entry(policy, "task-ready", 1) if index == 0 else None
            )
            state = OUTER.join_event(
                state,
                policy,
                OUTER.event(
                    action,
                    state,
                    event_type="task-session-joined",
                    result="pass",
                    next_entry=next_entry,
                    receipt_id=f"task-frontier-{index + 1}",
                ),
            )
            assert_no_prompt(self, state, action)
        self.assertEqual(state["phase"], "complete")
        self.assertEqual(state["visited_units"], policy["frontier"])
        self.assertEqual(len(set(sessions)), 2)
        self.assertEqual(len(state["task_session_receipts"]), 2)

    def test_05_product_choice_stops_before_any_effect(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "selection-ready"))
        state = OUTER.set_stop_decision(
            state, policy, "product-or-semantic-choice"
        )
        state, action = OUTER.decide_next_action(
            state, policy, available_inputs=[], installed_owner_routes=OUTER.installed()
        )
        self.assertEqual(action["action_type"], "stop")
        self.assertEqual(state["steps_used"], 0)
        self.assertEqual(state["owner_receipts"], [])
        self.assertEqual(state["task_session_receipts"], [])
        assert_no_prompt(self, state, action)

    def test_06_scope_expansion_stops_before_any_effect(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "selection-ready"))
        state = OUTER.set_stop_decision(state, policy, "scope-expansion")
        state, action = OUTER.decide_next_action(
            state, policy, available_inputs=[], installed_owner_routes=OUTER.installed()
        )
        self.assertEqual(action["stop_reason"], "scope-expansion")
        self.assertEqual(state["steps_used"], 0)
        self.assertEqual(state["consumed_route_fingerprints"], [])

        frontier_policy = OUTER.base_policy()
        frontier_state = OUTER.init(
            frontier_policy, OUTER.entry(frontier_policy, "selection-ready")
        )
        frontier_state, select_action = OUTER.decide_next_action(
            frontier_state,
            frontier_policy,
            available_inputs=[],
            installed_owner_routes=OUTER.installed(),
        )
        with self.assertRaises(OUTER.OuterLoopError) as absorption:
            OUTER.join_event(
                frontier_state,
                frontier_policy,
                OUTER.event(
                    select_action,
                    frontier_state,
                    event_type="selection-materialized",
                    result="pass",
                    next_entry=OUTER.entry(frontier_policy, "task-ready", 1),
                ),
            )
        self.assertEqual(absorption.exception.code, "FRONTIER_ABSORPTION_BLOCKED")
        self.assertEqual(frontier_state["owner_receipts"], [])
        self.assertEqual(frontier_state["task_session_receipts"], [])

    def test_07_protected_destructive_external_and_authority_actions_stop(self) -> None:
        decisions = [
            "destructive-or-irreversible-effect",
            "credentials-or-secret-access",
            "external-message-or-network-effect",
            "cost-policy-or-risk-acceptance",
            "authority-promotion-publication-deployment",
        ]
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        for decision in decisions:
            with self.subTest(decision=decision):
                state = OUTER.init(policy, OUTER.entry(policy, "selection-ready"))
                state = OUTER.set_stop_decision(state, policy, decision)
                state, action = OUTER.decide_next_action(
                    state,
                    policy,
                    available_inputs=[],
                    installed_owner_routes=OUTER.installed(),
                )
                self.assertEqual(state["phase"], "blocked")
                self.assertEqual(action["stop_reason"], decision)
                self.assertEqual(state["steps_used"], 0)
                self.assertEqual(state["owner_receipts"], [])
                self.assertEqual(state["task_session_receipts"], [])

        protected_effects = [
            "destructive-or-irreversible",
            "external-network-or-message",
            "authority-or-promotion",
            "publication-or-deployment",
        ]
        for effect in protected_effects:
            with self.subTest(effect=effect):
                protected_policy = copy.deepcopy(policy)
                protected_policy["allowed_routes"][0]["effect_class"] = effect
                protected_policy["allowed_routes_digest"] = (
                    READINESS.allowed_routes_digest(
                        protected_policy["allowed_routes"]
                    )
                )
                with self.assertRaises(ValueError) as rejected:
                    READINESS.validate_execution_policy(protected_policy)
                self.assertEqual(rejected.exception.code, "PROTECTED_ROUTE_EFFECT")

    def test_08_failed_critical_validation_stops_before_follow_on_effect(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "task-ready"))
        state, action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["task-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                action,
                state,
                event_type="task-session-joined",
                result="block",
                next_entry=None,
                receipt_id="task-critical-failure-001",
                stop_decision="failed-acceptance-critical-validation",
                blocker_code="CRITICAL_VALIDATION_FAILED",
            ),
        )
        self.assertEqual(state["phase"], "blocked")
        self.assertEqual(
            state["stop_reason"], "failed-acceptance-critical-validation"
        )
        self.assertEqual(len(state["task_session_receipts"]), 1)
        self.assertEqual(state["task_session_receipts"][0]["result"], "block")
        stopped, stop_action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["task-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        self.assertEqual(stopped["phase"], "blocked")
        self.assertEqual(stop_action["action_type"], "stop")
        self.assertEqual(len(stopped["task_session_receipts"]), 1)

    def test_09_legacy_ad_hoc_router_keeps_explicit_gate(self) -> None:
        fixture_path = (
            ROUTER_ROOT
            / "development"
            / "route-fixtures"
            / "route-legacy-no-silent-approval.json"
        )
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        schema = json.loads(LEGACY.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])
        LEGACY.validate_semantics(fixture_path, payload)
        self.assertEqual(payload["selection"]["status"], "blocked")
        self.assertIsNone(payload["authorization"]["exact_route"])

        silently_authorized = copy.deepcopy(payload)
        silently_authorized["candidates"][0]["authorization_status"] = "matched"
        with self.assertRaises(AssertionError):
            LEGACY.validate_semantics(fixture_path, silently_authorized)

    def test_10_fast_guard_observes_four_reads_one_phase_and_zero_mutation(self) -> None:
        fixture = FRESH.FreshSessionFixture()
        try:
            for request, expected in (
                (fixture.original_request, "route-owner"),
                (fixture.current_request, "proceed"),
            ):
                receipt = FAST_GUARD.classify_fast_entry(request)
                FAST_GUARD.validate_fast_entry_receipt(receipt, request)
                self.assertEqual(receipt["decision"], expected)
                self.assertEqual(receipt["read_count"], 4)
                self.assertEqual(receipt["phase_count"], 1)
                self.assertEqual(receipt["mutation_count"], 0)
                self.assertEqual(receipt["authorization_prompt_required"], False)
                self.assertEqual(
                    receipt["logical_inputs_read"],
                    [
                        "work-pack",
                        "selected-unit",
                        "execution-binding",
                        "execution-entry-projection",
                    ],
                )
                self.assertEqual(
                    receipt["phase_trace"],
                    {
                        "entry_guard_entered": True,
                        "context_builder_entered": False,
                        "deep_material_check_entered": False,
                        "mutation_admission_entered": False,
                        "target_mutation_entered": False,
                        "owner_hops_dispatched": 0,
                    },
                )
                self.assertEqual(
                    receipt["owner_packet"],
                    (
                        request["execution_binding"]["current_route"]
                        if expected == "route-owner"
                        else None
                    ),
                )
        finally:
            fixture.close()

    def test_11_undeclared_route_target_and_write_expansion_block(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "task-ready"))
        declared = copy.deepcopy(state["current_binding"]["current_route"])
        variants = []
        unknown = copy.deepcopy(declared)
        unknown["route_id"] = "route-undeclared"
        variants.append((unknown, "ROUTE_UNDECLARED", "route_id"))
        expanded_target = copy.deepcopy(declared)
        expanded_target["target"] = "execute generic unit plus foreign target"
        variants.append(
            (expanded_target, "ROUTE_TARGET_MISMATCH", declared["route_id"])
        )
        expanded_write = copy.deepcopy(declared)
        expanded_write["write_scope"].append("packages/foreign/")
        variants.append(
            (expanded_write, "ROUTE_WRITE_SCOPE_EXPANDED", declared["route_id"])
        )

        for candidate, code, detail in variants:
            with self.subTest(code=code):
                receipt = ROUTER.evaluate_work_pack_route(
                    route_request(
                        policy,
                        state,
                        candidate,
                        available_inputs=["task-input-1"],
                    )
                )
                self.assertEqual(receipt["verdict"], "block")
                self.assertEqual(receipt["code"], code)
                self.assertEqual(receipt["blocking_detail"], detail)
                self.assertFalse(receipt["dispatch_allowed"])
                self.assertEqual(receipt["authorization_prompt_required"], False)

    def test_12_binding_replay_after_work_pack_or_frontier_change_blocks(self) -> None:
        original_policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(
            original_policy, OUTER.entry(original_policy, "task-ready")
        )

        foreign_policy = copy.deepcopy(original_policy)
        foreign_policy["work_pack_id"] = "WP-GENERIC-FOREIGN"
        with self.assertRaises(OUTER.OuterLoopError) as work_pack_error:
            OUTER.decide_next_action(
                state,
                foreign_policy,
                available_inputs=["task-input-1"],
                installed_owner_routes=OUTER.installed(),
            )
        self.assertEqual(work_pack_error.exception.code, "WORK_PACK_ID_MISMATCH")

        expanded_policy = OUTER.base_policy(
            ["SWU-GENERIC-001", "SWU-GENERIC-002"]
        )
        with self.assertRaises(OUTER.OuterLoopError) as frontier_error:
            OUTER.decide_next_action(
                state,
                expanded_policy,
                available_inputs=["task-input-1"],
                installed_owner_routes=OUTER.installed(),
            )
        self.assertIn(
            frontier_error.exception.code,
            {"WORK_PACK_SEMANTIC_STALE", "FRONTIER_STALE"},
        )

    def test_13_repeated_owner_and_session_fingerprints_block_without_reentry(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        state = OUTER.init(policy, OUTER.entry(policy, "owner-prerequisite"))
        state, owner_action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["owner-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                owner_action,
                state,
                event_type="owner-joined",
                result="pass",
                next_entry=OUTER.entry(policy, "owner-prerequisite"),
                receipt_id="owner-cycle-001",
            ),
        )
        state, repeated_owner = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["owner-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        self.assertEqual(repeated_owner["action_type"], "stop")
        self.assertEqual(repeated_owner["stop_reason"], "ROUTE_FINGERPRINT_REPEATED")
        self.assertEqual(len(state["owner_receipts"]), 1)

        fresh_policy = FRESH.policy()
        fresh_policy["schema_version"] = "1.1.0"
        fresh_policy["completion_continuity"] = OUTER.completion_continuity(
            fresh_policy["frontier"], fresh_policy["work_pack_semantic_digest"]
        )
        original_policy_factory = FRESH.policy
        FRESH.policy = lambda: copy.deepcopy(fresh_policy)
        fixture = FRESH.FreshSessionFixture()
        try:
            bridge_policy = fixture.execution_policy
            bridge_state = OUTER.initialize_outer_loop(
                bridge_policy,
                fixture.original_request["execution_entry"],
                source_invocation_id="invoke-fresh-session-001",
                created_at="2026-08-04T00:00:00Z",
                execution_mode="one-unit",
                step_budget=4,
            )
            bridge_state, bridge_owner_action = OUTER.decide_next_action(
                bridge_state,
                bridge_policy,
                available_inputs=["owner-input.json"],
                installed_owner_routes=OUTER.installed(),
            )
            bridge_state = OUTER.join_event(
                bridge_state,
                bridge_policy,
                OUTER.event(
                    bridge_owner_action,
                    bridge_state,
                    event_type="owner-joined",
                    result="pass",
                    next_entry=fixture.current_request["execution_entry"],
                    receipt_id=fixture.owner_receipt["receipt_id"],
                ),
            )
            self.assertEqual(
                bridge_state["current_binding"],
                fixture.current_request["execution_binding"],
            )
            request = fixture.request("state/integration-bridge")
            request["loop_id"] = bridge_state["loop_id"]
            request["loop_state_digest"] = READINESS.fresh_resume_loop_state_digest(
                bridge_state
            )
            ready_state = copy.deepcopy(bridge_state)
            bridge_state, task_action, admission = (
                READINESS.decide_task_session_with_fresh_resume(
                    bridge_state,
                    bridge_policy,
                    request,
                    fixture.root,
                    available_inputs=["task-input.json"],
                    installed_owner_routes=OUTER.installed(),
                )
            )
            self.assertEqual(admission["decision"], "start-fresh-session")
            self.assertEqual(admission["fresh_task_session_start_count"], 1)
            self.assertEqual(admission["evidence_write_count"], 1)
            self.assertEqual(admission["authorization_prompt_count"], 0)
            self.assertFalse(admission["recursive_resume"])
            self.assertEqual(
                task_action["task_session_id"],
                admission["fresh_task_session"]["session_id"],
            )
            self.assertEqual(
                bridge_state["pending_task_session_id"],
                admission["fresh_task_session"]["session_id"],
            )
            bridge_state = OUTER.join_event(
                bridge_state,
                bridge_policy,
                OUTER.event(
                    task_action,
                    bridge_state,
                    event_type="task-session-joined",
                    result="pass",
                    next_entry=None,
                    receipt_id="task-fresh-bridge-001",
                ),
            )
            self.assertEqual(bridge_state["phase"], "complete")
            self.assertNotEqual(
                bridge_state["owner_receipts"][0]["receipt_id"],
                bridge_state["task_session_receipts"][0]["receipt_id"],
            )
            assert_no_prompt(self, bridge_state, bridge_owner_action, task_action)

            with self.assertRaises(READINESS.ReadinessExecutionError) as replay:
                READINESS.decide_task_session_with_fresh_resume(
                    ready_state,
                    bridge_policy,
                    request,
                    fixture.root,
                    available_inputs=["task-input.json"],
                    installed_owner_routes=OUTER.installed(),
                )
            self.assertEqual(
                replay.exception.code, "FRESH_SESSION_ADMISSION_BLOCKED"
            )
            self.assertIn("FRESH_SESSION_REPLAY", replay.exception.detail)

            cursor_cycle = fixture.request("state/integration-cursor-cycle")
            cursor_cycle["loop_id"] = request["loop_id"]
            cursor_cycle["loop_state_digest"] = request["loop_state_digest"]
            cursor_cycle["visited_session_cursors"].append(
                admission["fresh_task_session"]["cursor"]
            )
            cursor_block = FRESH.RESUME.admit_fresh_task_session(
                cursor_cycle, fixture.root
            )
            self.assertEqual(cursor_block["decision"], "block")
            self.assertEqual(cursor_block["code"], "TASK_SESSION_CURSOR_REPEATED")
        finally:
            fixture.close()
            FRESH.policy = original_policy_factory

    def test_14_declared_repairable_owner_condition_retries_once_without_prompt(self) -> None:
        policy = OUTER.base_policy(["SWU-GENERIC-001"])
        policy["automatic_decisions"].append("declared-retry")
        state = OUTER.init(
            policy,
            OUTER.entry(policy, "owner-prerequisite"),
            step_budget=4,
        )
        state, first_owner = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["owner-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        first_binding = copy.deepcopy(state["current_binding"])
        first_route = copy.deepcopy(first_owner["owner_route"])
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                first_owner,
                state,
                event_type="owner-joined",
                result="retry",
                next_entry=copy.deepcopy(state["current_entry"]),
                receipt_id="owner-repairable-integration-001",
                blocker_code="REPAIRABLE_OWNER_CONDITION",
            ),
        )
        fingerprint = first_binding["route_fingerprint"]
        self.assertIn(fingerprint, state["consumed_route_fingerprints"])
        self.assertEqual(state["route_retry_counts"], {fingerprint: 1})
        self.assertEqual(
            state["pending_retry"]["owner_receipt_id"],
            "owner-repairable-integration-001",
        )

        preserved_history = copy.deepcopy(state["consumed_route_fingerprints"])
        state, retried_owner = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["owner-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        self.assertEqual(retried_owner["automatic_decision"], "declared-retry")
        self.assertEqual(retried_owner["owner_route"], first_route)
        self.assertEqual(retried_owner["selected_unit"], first_owner["selected_unit"])
        self.assertEqual(state["current_binding"], first_binding)
        self.assertEqual(state["consumed_route_fingerprints"], preserved_history)
        self.assertEqual(state["steps_used"], 2)

        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                retried_owner,
                state,
                event_type="owner-joined",
                result="pass",
                next_entry=OUTER.entry(policy, "task-ready"),
                receipt_id="owner-repaired-integration-002",
            ),
        )
        state, task_action = OUTER.decide_next_action(
            state,
            policy,
            available_inputs=["task-input-1"],
            installed_owner_routes=OUTER.installed(),
        )
        state = OUTER.join_event(
            state,
            policy,
            OUTER.event(
                task_action,
                state,
                event_type="task-session-joined",
                result="pass",
                next_entry=None,
                receipt_id="task-after-retry-integration-001",
            ),
        )
        self.assertEqual(state["phase"], "complete")
        self.assertEqual(
            [receipt["result"] for receipt in state["owner_receipts"]],
            ["retry", "pass"],
        )
        self.assertEqual(
            [
                decision["decision_class"]
                for decision in state["automatic_decisions"]
            ],
            [
                "capability-owner-routing",
                "declared-retry",
                "fresh-task-session-resumption",
            ],
        )
        assert_no_prompt(self, state, first_owner, retried_owner, task_action)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        WorkPackExecutionIntegrationTests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        print("WORK_PACK_EXECUTION_INTEGRATION=block", file=sys.stderr)
        return 1
    print("WORK_PACK_EXECUTION_INTEGRATION=pass")
    print(f"INTEGRATION_CASE_COUNT={result.testsRun}")
    print("ENTRY_STATE_COUNT=4")
    print("AUTOMATIC_DECISION_CLASS_COUNT=4")
    print("STOP_DECISION_COUNT=8")
    print("FAST_GUARD_PHASE_COUNT=1")
    print("AUTHORIZATION_PROMPT_COUNT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

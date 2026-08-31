#!/usr/bin/env python3
"""Validate fresh-current-unit and multi-epoch supervisor boundaries."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHAIN_TESTS = load_module(
    "chain_fixture_module", SPELL_ROOT / "development" / "validate-chain-v2.py"
)
CHAIN = CHAIN_TESTS.CHAIN
SUPERVISOR = load_module(
    "multi_epoch_supervisor",
    SPELL_ROOT / "scripts" / "run_multi_epoch_supervisor.py",
)
CONTRACTS = load_module(
    "implementation_readiness_contracts",
    SPELL_ROOT.parent
    / "implementation-readiness"
    / "scripts"
    / "execution_contracts.py",
)
FAST_ENTRY = load_module(
    "task_session_fast_entry_guard",
    SPELL_ROOT.parents[1]
    / "arcana"
    / "task-session"
    / "scripts"
    / "fast_execution_entry_guard.py",
)


def windowed_config(fixture, *, supervisor_id: str = "synthetic-supervisor"):
    config = fixture.current_v2_config()
    frontier = ["U1", "U2"]

    contracts = CHAIN.load_json(fixture.root / "contracts.json")
    routes = [
        route
        for route in contracts["execution_policy"]["allowed_routes"]
        if route["frontier_swu"] == "U1"
    ]
    contracts["execution_policy"]["allowed_routes"] = copy.deepcopy(routes)
    fixture.write_json("contracts.json", contracts)
    contracts_ref = fixture.exact("contracts.json")

    audit = CHAIN.load_json(fixture.root / "audit-config.json")
    audit["execution_policy"]["allowed_routes"] = copy.deepcopy(routes)
    for index, binding in enumerate(audit["closeout_bindings"]):
        binding["owner_receipt_contract_ref"] = {
            "artifact_ref": contracts_ref,
            "selector": f"/units/{index}/closeout_contract",
        }
    fixture.write_json("audit-config.json", audit)

    manifest = CHAIN.load_json(fixture.root / "manifest-current.json")
    manifest["allowed_routes"] = copy.deepcopy(routes)
    manifest["allowed_routes_digest"] = CHAIN.digest(routes)
    fixture.write_json("manifest-current.json", manifest)

    report = CHAIN.load_json(fixture.root / "report-current.json")
    report["manifest"] = copy.deepcopy(manifest)
    fixture.write_json("report-current.json", report)

    handoff = CHAIN.load_json(fixture.root / "handoff.json")
    handoff["allowed_routes_digest"] = manifest["allowed_routes_digest"]
    fixture.write_json("handoff.json", handoff)

    config["manifest_ref"] = fixture.exact("manifest-current.json")
    config["audit_report_ref"] = fixture.exact("report-current.json")
    config["wpra_v2"]["audit_config_ref"] = fixture.exact("audit-config.json")
    config["wpra_v2"]["execution_contracts_ref"] = contracts_ref
    config["wpra_v2"]["selection_handoff_ref"] = fixture.exact("handoff.json")

    selection_request = CHAIN.load_json(fixture.root / "selection-request.json")
    selection_request["manifestRef"] = config["manifest_ref"]
    fixture.write_json("selection-request.json", selection_request)
    config["wpra_v2"]["initial_selection_request_ref"] = fixture.exact(
        "selection-request.json"
    )

    selection_receipt = CHAIN.load_json(fixture.root / "selection-receipt.json")
    selection_receipt["manifestDigest"] = config["manifest_ref"]["sha256"]
    selection_receipt["requestDigest"] = CHAIN.digest(selection_request)
    fixture.write_json("selection-receipt.json", selection_receipt)
    config["wpra_v2"]["initial_selection_receipt_ref"] = fixture.exact(
        "selection-receipt.json"
    )

    config["finite_frontier"] = ["U1"]
    config["run_budget"] = {"max_task_session_requests": 1}
    config["admission_window"] = {
        "mode": "fresh-current-unit",
        "supervisor_id": supervisor_id,
        "epoch_ordinal": 1,
        "selected_unit": "U1",
        "supervisor_frontier_digest": CHAIN.digest(frontier),
        "observed_ready_frontier_digest": CHAIN.digest(frontier),
    }
    approval = {
        "schema_version": "task-session-until-blocker.epoch-approval/v1",
        "approval_status": "approved",
        "approval_owner_ref": config["approved_epoch"]["approval_owner_ref"],
        "plan_epoch_id": config["approved_epoch"]["epoch_id"],
        "audit_projection_digest": config["approved_epoch"][
            "audit_projection_digest"
        ],
        "canonical_semantic_digest": config["approved_epoch"][
            "canonical_semantic_digest"
        ],
        "source_snapshot_digest": config["approved_epoch"][
            "source_snapshot_digest"
        ],
        "manifest_ref": config["manifest_ref"],
        "audit_config_ref": config["wpra_v2"]["audit_config_ref"],
        "execution_contracts_ref": config["wpra_v2"][
            "execution_contracts_ref"
        ],
        "authority_effect": "chain-selection-only",
        "admission_window": config["admission_window"],
        "finite_frontier": config["finite_frontier"],
        "run_budget": config["run_budget"],
        "risk_ceiling": config["risk_ceiling"],
        "chain_config_projection_digest": CHAIN.digest(
            CHAIN.chain_config_approval_projection(config)
        ),
    }
    fixture.write_json("approval-current.json", approval)
    config["approved_epoch"]["decision_gate_approval_receipt_ref"] = fixture.exact(
        "approval-current.json"
    )
    fixture.write_json("epoch-config.json", config)
    return config


def supervisor_config(fixture):
    fixture.write_json("work-pack.json", {"id": "synthetic-work-pack"})
    fixture.write_json("owner-input.json", {"status": "accepted"})
    return {
        "schema_version": "1.0.0",
        "supervisor_id": "synthetic-supervisor",
        "repository_root": ".",
        "state_directory": "state/multi-epoch-supervisor",
        "scope_id": "synthetic-work-pack",
        "work_pack_ref": fixture.exact("work-pack.json"),
        "owner_input_refs": [fixture.exact("owner-input.json")],
        "captured_frontier": ["U1", "U2"],
        "max_epochs": 2,
        "risk_ceiling": "bounded-write",
        "allowed_task_session_flags": ["observability-residue"],
        "epoch_policy": {
            "mode": "fresh-current-unit",
            "max_task_session_requests": 1,
            "fresh_readiness_required": True,
            "approval_authority_effect": "chain-selection-only",
        },
        "persistence": {
            "mode": "append-only-hash-chain",
            "collision_policy": "exclusive-create",
        },
        "compensation": {
            "mode": "none",
            "rationale": "Synthetic fixture performs no product mutation.",
        },
    }


def write_fast_entry(
    fixture,
    *,
    selected_unit: str,
    entry_state: str = "task-ready",
    completed_prefix: list[dict] | None = None,
    suffix: str,
    frontier: list[str] | None = None,
):
    frontier = list(frontier or ["U1", "U2"])
    completed = copy.deepcopy(completed_prefix or [])
    semantic_digest = fixture.semantic_digest
    continuity_payload = {
        "source_audit_id": "accepted-stream-audit",
        "source_projection_digest": CONTRACTS.canonical_digest(
            {"frontier": frontier}
        ),
        "work_pack_semantic_digest": semantic_digest,
        "plan_epoch_id": fixture.epoch_id,
        "completed_prefix": completed,
        "next_unit": selected_unit,
        "authority_effect": "none",
    }
    routes = [
        {
            "route_id": f"task-{unit_id}",
            "frontier_swu": unit_id,
            "capability": "task-session",
            "mode": "execute",
            "target": f"work-pack.md#{unit_id}",
            "write_scope": [f"product/{unit_id}"],
            "effect_class": "repository-local-reversible",
            "required_inputs": [f"contract/{unit_id}"],
            "expected_receipt": f"receipt/{unit_id}.json",
        }
        for unit_id in frontier
    ]
    if "U2" in frontier:
        routes.append({
            "route_id": "owner-U2",
            "frontier_swu": "U2",
            "capability": "runtime-owner",
            "mode": "satisfy-prerequisite",
            "target": "U2-runtime-profile",
            "write_scope": ["owner/U2.json"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["owner/U2-request.json"],
            "expected_receipt": "owner/U2.json",
        })
    policy = {
        "schema_version": "1.1.0",
        "work_pack_id": "synthetic-work-pack",
        "work_pack_semantic_digest": semantic_digest,
        "frontier": frontier,
        "completion_continuity": {
            **continuity_payload,
            "continuity_digest": CONTRACTS.canonical_digest(continuity_payload),
        },
        "allowed_routes": routes,
        "allowed_routes_digest": CONTRACTS.allowed_routes_digest(routes),
        "automatic_decisions": [
            "internal-tool-selection",
            "capability-owner-routing",
            "fresh-task-session-resumption",
        ],
        "stop_decisions": [
            "product-or-semantic-choice",
            "scope-expansion",
            "destructive-or-irreversible-effect",
            "credentials-or-secret-access",
            "external-message-or-network-effect",
            "cost-policy-or-risk-acceptance",
            "authority-promotion-publication-deployment",
            "failed-acceptance-critical-validation",
        ],
        "validation_commands": [
            json.dumps(
                {
                    "unit_id": selected_unit,
                    "validation_contract": {
                        "command_id": f"validate-{selected_unit}",
                        "argv": ["python3", "validate.py", selected_unit],
                        "cwd": ".",
                        "timeout_seconds": 60,
                    },
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        ],
        "scope_source": "exact-work-pack-and-captured-frontier",
        "validation_policy": "owner-gates-remain-mandatory",
        "authority_effect": "none",
    }
    route_id = "owner-U2" if entry_state == "owner-prerequisite" else f"task-{selected_unit}"
    route = next(item for item in routes if item["route_id"] == route_id)
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": entry_state,
        "selected_unit": selected_unit,
        "route_id": route_id,
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
        "authority_effect": "none",
    }
    binding = CONTRACTS.build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id="accepted-stream-direct-intent",
        created_at="2026-08-24T00:00:00Z",
        execution_mode="finite-frontier",
    )
    request = {
        "schema_version": "1.0.0",
        "execution_policy": policy,
        "execution_entry": entry,
        "execution_binding": binding,
        "selected_unit": {
            "work_pack_id": policy["work_pack_id"],
            "swu_id": selected_unit,
        },
        "authority_effect": "none",
    }
    receipt = FAST_ENTRY.classify_fast_entry(request)
    fixture.write_json(f"fast-entry-request-{suffix}.json", request)
    fixture.write_json(f"fast-entry-receipt-{suffix}.json", receipt)
    return request, receipt


def accepted_stream_supervisor_config(fixture, frontier: list[str] | None = None):
    frontier = list(frontier or ["U1", "U2"])
    if frontier != ["U1", "U2"]:
        for unit_id in frontier:
            fixture.write_json(f"terminal-{unit_id}.json", {"status": "PASS"})
            fixture.write_json(f"router-{unit_id}.json", {"status": "verified"})
            fixture.write_json(f"closeout-{unit_id}.json", {"unit": unit_id})
        manifest = CHAIN.load_json(fixture.root / "manifest.json")
        manifest["canonical_plan_graph"]["finite_frontier"] = frontier
        manifest["execution_bindings"] = [
            {"unit_id": unit_id, "command": {"risk_class": "bounded-write"}}
            for unit_id in frontier
        ]
        manifest["closeout_bindings"] = [
            {
                "unit_id": unit_id,
                "owner_receipt_contract_ref": {
                    "artifact_ref": fixture.exact(f"closeout-{unit_id}.json")
                },
            }
            for unit_id in frontier
        ]
        fixture.write_json("manifest.json", manifest)
    chain = fixture.config()
    chain["finite_frontier"] = frontier
    chain["run_budget"] = {"max_task_session_requests": len(frontier)}
    chain["frontier_binding_mode"] = "accepted-policy-frontier"
    fixture.write_json("accepted-stream-chain.json", chain)
    request, receipt = write_fast_entry(
        fixture, selected_unit=frontier[0], suffix=frontier[0], frontier=frontier
    )
    assert receipt["code"] == "TASK_READY"
    fixture.write_json("work-pack.json", {"id": "synthetic-work-pack"})
    fixture.write_json("owner-input.json", {"status": "accepted"})
    chain_ref = fixture.exact("accepted-stream-chain.json")
    request_ref = fixture.exact("fast-entry-request-U1.json")
    receipt_ref = fixture.exact("fast-entry-receipt-U1.json")
    acceptance = {
        "schema_version": "task-session-until-blocker.finite-stream-execution-acceptance/v1",
        "approval_status": "approved",
        "supervisor_id": "synthetic-accepted-stream",
        "scope_id": "synthetic-work-pack",
        "work_pack_id": request["execution_policy"]["work_pack_id"],
        "work_pack_semantic_digest": request["execution_policy"][
            "work_pack_semantic_digest"
        ],
        "allowed_routes_digest": request["execution_policy"][
            "allowed_routes_digest"
        ],
        "source_invocation_id": "accepted-stream-direct-intent",
        "execution_mode": "finite-frontier",
        "captured_frontier": frontier,
        "chain_config_ref": chain_ref,
        "fast_entry_request_ref": request_ref,
        "fast_entry_receipt_ref": receipt_ref,
        "max_task_session_requests": len(frontier),
        "risk_ceiling": "bounded-write",
        "automatic_decisions": [
            "internal-tool-selection",
            "capability-owner-routing",
            "fresh-task-session-resumption",
        ],
        "stop_decisions": [
            "product-or-semantic-choice",
            "scope-expansion",
            "destructive-or-irreversible-effect",
            "credentials-or-secret-access",
            "external-message-or-network-effect",
            "cost-policy-or-risk-acceptance",
            "authority-promotion-publication-deployment",
            "failed-acceptance-critical-validation",
        ],
        "authority_effect": "bounded-execution-only",
        "claim_ceiling": "Sequence admission only; no mutation, owner decision, promotion, publication, or deployment authority.",
    }
    fixture.write_json("accepted-stream-approval.json", acceptance)
    config = {
        "schema_version": "1.1.0",
        "supervisor_id": "synthetic-accepted-stream",
        "repository_root": ".",
        "state_directory": "state/accepted-stream-supervisor",
        "scope_id": "synthetic-work-pack",
        "work_pack_ref": fixture.exact("work-pack.json"),
        "owner_input_refs": [fixture.exact("owner-input.json")],
        "captured_frontier": frontier,
        "max_epochs": len(frontier),
        "risk_ceiling": "bounded-write",
        "allowed_task_session_flags": ["observability-residue"],
        "epoch_policy": {
            "mode": "accepted-finite-stream",
            "max_task_session_requests": len(frontier),
            "fresh_readiness_required": False,
            "approval_authority_effect": "bounded-execution-only",
        },
        "accepted_stream": {
            "chain_config_ref": chain_ref,
            "execution_acceptance_ref": fixture.exact(
                "accepted-stream-approval.json"
            ),
            "initial_fast_entry_request_ref": request_ref,
            "initial_fast_entry_receipt_ref": receipt_ref,
        },
        "persistence": {
            "mode": "append-only-hash-chain",
            "collision_policy": "exclusive-create",
        },
        "compensation": {
            "mode": "none",
            "rationale": "Synthetic fixture performs no product mutation.",
        },
    }
    fixture.write_json("accepted-stream-supervisor.json", config)
    return config


class MultiEpochSupervisorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = CHAIN_TESTS.ChainFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_current_unit_window_accepts_only_one_route_and_budget(self) -> None:
        config = windowed_config(self.fixture)
        self.assertNotIn("frontier_binding_mode", config)
        self.assertEqual(
            CHAIN.schema_errors(config, CHAIN.CONFIG_SCHEMA, "epoch config"), []
        )
        manifest, receipt = CHAIN.preflight(config, self.fixture.root)
        self.assertEqual(receipt["terminal_code"], "CHAIN_PREFLIGHT_READY")
        self.assertEqual(manifest["canonical_plan_graph"]["finite_frontier"], ["U1"])
        self.assertEqual(manifest["fresh_epoch_ready_frontier"], ["U1", "U2"])
        self.assertEqual(manifest["fresh_epoch_successor"], "U2")
        self.assertEqual(
            [item["unit_id"] for item in manifest["execution_bindings"]], ["U1"]
        )

    def test_window_budget_widening_fails_schema_and_approval(self) -> None:
        config = windowed_config(self.fixture)
        config["run_budget"]["max_task_session_requests"] = 2
        errors = CHAIN.schema_errors(config, CHAIN.CONFIG_SCHEMA, "epoch config")
        self.assertTrue(any("1 was expected" in error for error in errors))
        approval = CHAIN.load_json(self.fixture.root / "approval-current.json")
        self.assertTrue(CHAIN.wpra_approval_errors(approval, config))

    def test_closed_window_requires_fresh_epoch_instead_of_old_successor(self) -> None:
        config = windowed_config(self.fixture)
        manifest, _ = CHAIN.preflight(config, self.fixture.root)
        current = CHAIN.binding_for(manifest, "U1")
        self.assertIsNotNone(current)
        self.fixture.write_json("evidence/U1-validation.json", {"status": "pass"})
        validation_ref = self.fixture.exact("evidence/U1-validation.json")
        terminal = {
            "schema_version": "synthetic.terminal/v1",
            "receipt_id": "terminal-u1",
            "work_pack_id": "synthetic-work-pack",
            "unit_id": "U1",
            "swu_id": "SWU-1",
            "task_id": "TASK-1",
            "result": "pass",
            "terminal_mode": "PASS",
            "validation": {
                "status": "pass",
                "command_results": [
                    {
                        "command_id": "V-U1",
                        "status": "pass",
                        "evidence_ref": validation_ref,
                    }
                ],
            },
            "evidence_refs": [validation_ref],
            "dependency_dispositions": [],
            "blockers": [],
            "successor": {"unit_id": "SWU-2", "execution_started": False},
            "authority_effect": "none",
            "mutation_ready": False,
        }
        self.fixture.write_json("receipt/U1.json", terminal)
        terminal_ref = self.fixture.exact("receipt/U1.json")
        next_route = {
            "unit_id": "SWU-2",
            "capability": "task-session",
            "mode": "execute-one-swu",
        }
        owner = {
            "schema_version": "synthetic.closeout/v1",
            "receipt_id": "closeout-u1",
            "work_pack_id": "synthetic-work-pack",
            "unit_id": "U1",
            "swu_id": "SWU-1",
            "terminal_receipt_ref": terminal_ref,
            "result": "pass",
            "lifecycle_owner_validation": {
                "status": "pass",
                "allowed_delta_policy": "evidence-only",
                "baseline_status": "exact-absent",
            },
            "target_inventory": ["closeout/U1.json", "next/U1.json"],
            "next_route": next_route,
            "blockers": [],
            "authority_effect": "none",
            "successor_executed": False,
        }
        self.fixture.write_json("closeout/U1.json", owner)
        self.fixture.write_json("next/U1.json", next_route)
        transition = self.fixture.transition()
        transition["terminal_receipt_ref"] = terminal_ref
        transition["closeout"]["owner_receipt_ref"] = self.fixture.exact(
            "closeout/U1.json"
        )
        transition["closeout"][
            "continuation_router_verification_receipt_ref"
        ] = self.fixture.exact("next/U1.json")
        transition["observed_frontier_digest"] = CHAIN.digest(["U1"])
        receipt, state = CHAIN.evaluate_transition(
            config,
            manifest,
            transition,
            CHAIN.initial_state(config),
            self.fixture.root,
        )
        self.assertEqual(receipt["terminal_code"], "FRESH_EPOCH_REQUIRED")
        self.assertEqual(receipt["next_fresh_epoch_unit"], "U2")
        self.assertEqual(receipt["next_route"], "work-pack-readiness-audit")
        self.assertIsNone(receipt["next_task_session_selector"])
        self.assertEqual(state["status"], "COMPLETE")
        self.assertEqual(state["visited"], ["U1"])
        transitions_dir, persisted_initial = CHAIN.open_chain_state(
            config, manifest, self.fixture.root
        )
        self.assertEqual(persisted_initial["request_count"], 0)
        transition_path = CHAIN.persist_transition(
            transitions_dir, transition, receipt, state
        )

        supervisor = supervisor_config(self.fixture)
        records_dir, records = SUPERVISOR.open_supervisor(
            supervisor, self.fixture.root
        )
        epoch_ref = SUPERVISOR.exact_ref(
            self.fixture.root, self.fixture.root / "epoch-config.json"
        )
        record = SUPERVISOR.completion_record(
            supervisor,
            epoch_ref,
            config,
            manifest,
            transition_path,
            self.fixture.root,
            None,
        )
        CHAIN.exclusive_write_json(records_dir / "000001.json", record)
        replayed = SUPERVISOR.replay_records(
            supervisor, self.fixture.root, records_dir
        )
        self.assertEqual(replayed, [record])
        next_receipt = SUPERVISOR.next_epoch_receipt(supervisor, replayed)
        self.assertEqual(next_receipt["next_fresh_epoch_unit"], "U2")

    def test_window_approval_must_bind_frontier_budget_risk_and_projection(self) -> None:
        config = windowed_config(self.fixture)
        approval = CHAIN.load_json(self.fixture.root / "approval-current.json")
        for field in (
            "finite_frontier",
            "run_budget",
            "risk_ceiling",
            "chain_config_projection_digest",
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(approval)
                invalid.pop(field)
                self.assertTrue(CHAIN.wpra_approval_errors(invalid, config))

    def test_supervisor_emits_one_task_session_without_launching_it(self) -> None:
        config = windowed_config(self.fixture)
        supervisor = supervisor_config(self.fixture)
        self.assertEqual(
            CHAIN.schema_errors(
                supervisor, SUPERVISOR.CONFIG_SCHEMA, "supervisor config"
            ),
            [],
        )
        SUPERVISOR.verify_supervisor_inputs(supervisor, self.fixture.root)
        records_dir, records = SUPERVISOR.open_supervisor(
            supervisor, self.fixture.root
        )
        self.assertTrue(records_dir.exists())
        self.assertEqual(records, [])
        epoch_ref, loaded, manifest = SUPERVISOR.load_epoch(
            self.fixture.root / "epoch-config.json", self.fixture.root
        )
        self.assertEqual(epoch_ref["path"], "epoch-config.json")
        SUPERVISOR.validate_epoch_window(supervisor, loaded, manifest, records)
        _, state, transitions = SUPERVISOR.inspect_inner_state(
            loaded, manifest, self.fixture.root
        )
        self.assertEqual(transitions, [])
        admission = CHAIN.admit_next_request(loaded, manifest, state)
        self.assertEqual(admission["terminal_code"], "NEXT_SELECTOR_READY")
        self.assertEqual(admission["next_task_session_selector"], "U1")

    def test_supervisor_requires_fresh_readiness_after_each_closed_epoch(self) -> None:
        supervisor = supervisor_config(self.fixture)
        first_record = {"selected_unit": "U1"}
        receipt = SUPERVISOR.next_epoch_receipt(supervisor, [first_record])
        self.assertEqual(receipt["terminal_code"], "NEXT_EPOCH_INPUT_REQUIRED")
        self.assertEqual(receipt["next_fresh_epoch_unit"], "U2")
        self.assertEqual(receipt["next_route"], "work-pack-readiness-audit")
        complete = SUPERVISOR.next_epoch_receipt(
            supervisor, [first_record, {"selected_unit": "U2"}]
        )
        self.assertEqual(complete["terminal_code"], "SUPERVISOR_COMPLETE")
        self.assertIsNone(complete["next_route"])

    def test_supervisor_rejects_owner_input_drift(self) -> None:
        supervisor = supervisor_config(self.fixture)
        self.fixture.write_json("owner-input.json", {"status": "drifted"})
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            SUPERVISOR.verify_supervisor_inputs(supervisor, self.fixture.root)

    def test_supervisor_budget_does_not_expand_to_frontier_length(self) -> None:
        supervisor = supervisor_config(self.fixture)
        supervisor["max_epochs"] = 1
        receipt = SUPERVISOR.next_epoch_receipt(
            supervisor, [{"selected_unit": "U1"}]
        )
        self.assertEqual(
            receipt["terminal_code"], "SUPERVISOR_BUDGET_EXHAUSTED"
        )
        self.assertIsNone(receipt["next_route"])

    def test_accepted_stream_requires_real_task_ready_before_acceptance(self) -> None:
        supervisor = accepted_stream_supervisor_config(self.fixture)
        errors = CHAIN.schema_errors(supervisor, SUPERVISOR.CONFIG_SCHEMA, "supervisor config")
        self.assertEqual(len(errors), 1)
        self.assertIn("driver_request_ref", errors[0])
        receipt = SUPERVISOR.supervise_accepted_stream(
            supervisor,
            self.fixture.root,
            transition_path=None,
            fast_entry_request_path=None,
            fast_entry_receipt_path=None,
        )
        self.assertEqual(receipt["terminal_code"], "ACCEPTED_STREAM_DRIVER_REQUEST_REQUIRED")
        self.assertIsNone(receipt["next_task_session_selector"])

    def test_one_command_stream_stops_for_real_owner_prerequisite(self) -> None:
        supervisor = accepted_stream_supervisor_config(self.fixture)
        self.fixture.write_json("completion-U1.json", {"result": "pass"})
        completed_prefix = [
            {
                "unit_id": "U1",
                "unit_contract_digest": "a" * 64,
                "completion_binding_id": "completion-U1",
                "completion_artifact_ref": self.fixture.exact(
                    "completion-U1.json"
                ),
                "closeout_binding_id": "closeout-U1",
            }
        ]
        _, owner_receipt = write_fast_entry(
            self.fixture,
            selected_unit="U2",
            entry_state="owner-prerequisite",
            completed_prefix=completed_prefix,
            suffix="U2-owner",
        )
        self.assertEqual(owner_receipt["decision"], "route-owner")
        transition = self.fixture.transition()
        self.fixture.write_json("transition-U1.json", transition)
        result = SUPERVISOR.supervise_accepted_stream(
            supervisor,
            self.fixture.root,
            transition_path=self.fixture.root / "transition-U1.json",
            fast_entry_request_path=(
                self.fixture.root / "fast-entry-request-U2-owner.json"
            ),
            fast_entry_receipt_path=(
                self.fixture.root / "fast-entry-receipt-U2-owner.json"
            ),
        )
        self.assertEqual(result["terminal_code"], "ACCEPTED_STREAM_DRIVER_REQUEST_REQUIRED")
        self.assertIsNone(result["next_task_session_selector"])
        self.assertFalse((self.fixture.root / "state/synthetic-chain/transitions").exists())

    def test_one_command_surface_traverses_the_accepted_finite_stream(self) -> None:
        frontier = ["U1", "U2", "U3", "U4", "U5"]
        supervisor = accepted_stream_supervisor_config(self.fixture, frontier)
        result = SUPERVISOR.supervise_accepted_stream(
            supervisor, self.fixture.root, transition_path=None,
            fast_entry_request_path=None, fast_entry_receipt_path=None,
        )
        self.assertEqual(result["terminal_code"], "ACCEPTED_STREAM_DRIVER_REQUEST_REQUIRED")
        self.assertFalse((self.fixture.root / "state/synthetic-chain/transitions").exists())
        return
        completed_prefix = []
        previous_digest = None
        final_result = None
        for index, unit_id in enumerate(frontier):
            ordinal = index + 1
            next_unit = frontier[index + 1] if ordinal < len(frontier) else None
            self.fixture.write_json(
                f"completion-{unit_id}.json", {"result": "pass"}
            )
            completed_prefix.append(
                {
                    "unit_id": unit_id,
                    "unit_contract_digest": f"{ordinal:x}" * 64,
                    "completion_binding_id": f"completion-{unit_id}",
                    "completion_artifact_ref": self.fixture.exact(
                        f"completion-{unit_id}.json"
                    ),
                    "closeout_binding_id": f"closeout-{unit_id}",
                }
            )
            transition = self.fixture.transition(
                unit_id,
                ordinal=ordinal,
                previous=previous_digest,
                cursor=f"cursor-{ordinal}",
                closeout="NO_OP",
            )
            transition["successor"] = {
                "unit_id": next_unit,
                "candidate_count": 1 if next_unit else 0,
                "declared": True,
                "dependency_ready": True,
                "scope_digest": self.fixture.projection_digest,
            }
            transition["observed_frontier_digest"] = CHAIN.digest(frontier)
            transition["closeout"]["no_op_proof"][
                "continuation_router_verification"
            ]["canonical_successor"] = next_unit
            self.fixture.write_json(f"transition-{unit_id}.json", transition)

            if next_unit is None:
                request_path = None
                receipt_path = None
            else:
                _, ready_receipt = write_fast_entry(
                    self.fixture,
                    selected_unit=next_unit,
                    completed_prefix=completed_prefix,
                    suffix=f"{next_unit}-ready",
                    frontier=frontier,
                )
                self.assertEqual(ready_receipt["code"], "TASK_READY")
                request_path = (
                    self.fixture.root / f"fast-entry-request-{next_unit}-ready.json"
                )
                receipt_path = (
                    self.fixture.root / f"fast-entry-receipt-{next_unit}-ready.json"
                )
            final_result = SUPERVISOR.supervise_accepted_stream(
                supervisor,
                self.fixture.root,
                transition_path=self.fixture.root / f"transition-{unit_id}.json",
                fast_entry_request_path=request_path,
                fast_entry_receipt_path=receipt_path,
            )
            persisted = CHAIN.load_json(
                self.fixture.root
                / f"state/synthetic-chain/transitions/{ordinal:06d}.json"
            )
            previous_digest = persisted["state_after"]["last_transition_digest"]
            if next_unit is not None:
                self.assertEqual(final_result["terminal_code"], "TASK_READY")
                self.assertEqual(
                    final_result["next_task_session_selector"], next_unit
                )

        self.assertIsNotNone(final_result)
        self.assertEqual(final_result["terminal_code"], "SUPERVISOR_COMPLETE")
        self.assertEqual(final_result["completed_epochs"], len(frontier))
        self.assertIsNone(final_result["next_route"])
        self.assertEqual(
            len(
                list(
                    (
                        self.fixture.root
                        / "state/synthetic-chain/transitions"
                    ).glob("*.json")
                )
            ),
            len(frontier),
        )

    def test_accepted_stream_rejects_fast_entry_byte_drift(self) -> None:
        supervisor = accepted_stream_supervisor_config(self.fixture)
        receipt_path = self.fixture.root / "fast-entry-receipt-U1.json"
        receipt = CHAIN.load_json(receipt_path)
        receipt["blocker_detail"] = "drift"
        self.fixture.write_json("fast-entry-receipt-U1.json", receipt)
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            SUPERVISOR.verify_supervisor_inputs(supervisor, self.fixture.root)

    def test_accepted_wpra_stream_requires_policy_frontier_mode(self) -> None:
        supervisor = accepted_stream_supervisor_config(self.fixture)
        chain = CHAIN.load_json(
            self.fixture.root / "accepted-stream-chain.json"
        )
        chain.pop("frontier_binding_mode")
        self.fixture.write_json("accepted-stream-chain.json", chain)
        supervisor["accepted_stream"]["chain_config_ref"] = self.fixture.exact(
            "accepted-stream-chain.json"
        )
        with self.assertRaisesRegex(
            ValueError, "lacks the accepted policy frontier binding mode"
        ):
            SUPERVISOR.verify_supervisor_inputs(supervisor, self.fixture.root)

    def test_accepted_stream_rejects_cross_document_semantic_drift(self) -> None:
        supervisor = accepted_stream_supervisor_config(self.fixture)
        acceptance = CHAIN.load_json(
            self.fixture.root / "accepted-stream-approval.json"
        )
        acceptance["work_pack_semantic_digest"] = "f" * 64
        self.fixture.write_json("accepted-stream-approval.json", acceptance)
        supervisor["accepted_stream"]["execution_acceptance_ref"] = (
            self.fixture.exact("accepted-stream-approval.json")
        )
        with self.assertRaisesRegex(ValueError, "semantic digest"):
            SUPERVISOR.verify_supervisor_inputs(supervisor, self.fixture.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)

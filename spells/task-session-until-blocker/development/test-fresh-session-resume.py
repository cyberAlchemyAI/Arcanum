#!/usr/bin/env python3
"""Validate durable fresh-session admission after a Work-Pack owner prerequisite."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = Path(__file__).resolve().parents[3]
RESUME_PATH = SPELL_ROOT / "scripts" / "fresh_session_resume.py"
CONTRACTS_PATH = (
    ARCANUM_ROOT
    / "spells"
    / "implementation-readiness"
    / "scripts"
    / "execution_contracts.py"
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


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


RESUME = load_module("test_fresh_session_resume_runtime", RESUME_PATH)
CONTRACTS = load_module("test_fresh_session_resume_contracts", CONTRACTS_PATH)
FAST_GUARD = load_module("test_fresh_session_resume_guard", FAST_GUARD_PATH)
ROUTER = load_module("test_fresh_session_resume_router", ROUTER_PATH)


def exact_ref(root: Path, relative: str) -> dict[str, object]:
    content = (root / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def policy() -> dict:
    routes = [
        {
            "route_id": "route-owner",
            "frontier_swu": "SWU-GENERIC-001",
            "capability": "invoke",
            "mode": "refresh",
            "target": "repair generic unit",
            "write_scope": ["packages/generic/"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["owner-input.json"],
            "expected_receipt": "evidence/owner-receipt.json",
        },
        {
            "route_id": "route-task",
            "frontier_swu": "SWU-GENERIC-001",
            "capability": "task-session",
            "mode": "execute",
            "target": "execute generic unit",
            "write_scope": ["packages/generic/"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["task-input.json"],
            "expected_receipt": "evidence/task-receipt.json",
        },
    ]
    return {
        "schema_version": "1.0.0",
        "work_pack_id": "WP-GENERIC-FRESH-SESSION",
        "work_pack_semantic_digest": CONTRACTS.canonical_digest(
            {"work_pack": "fresh-session"}
        ),
        "frontier": ["SWU-GENERIC-001"],
        "allowed_routes": routes,
        "allowed_routes_digest": CONTRACTS.allowed_routes_digest(routes),
        "automatic_decisions": [
            "capability-owner-routing",
            "fresh-task-session-resumption",
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


def entry(execution_policy: dict, state: str) -> dict:
    if state == "owner-prerequisite":
        route_id = "route-owner"
        owner = {
            "capability": "invoke",
            "mode": "refresh",
            "target": "repair generic unit",
        }
    else:
        route_id = "route-task"
        owner = {
            "capability": "task-session",
            "mode": "execute",
            "target": "execute generic unit",
        }
    return {
        "schema_version": "1.0.0",
        "work_pack_id": execution_policy["work_pack_id"],
        "work_pack_semantic_digest": execution_policy["work_pack_semantic_digest"],
        "allowed_routes_digest": execution_policy["allowed_routes_digest"],
        "entry_state": state,
        "selected_unit": "SWU-GENERIC-001",
        "route_id": route_id,
        "next_owner": owner,
        "blocker_code": None,
        "authority_effect": "none",
    }


def guard_request(execution_policy: dict, state: str) -> dict:
    projection = entry(execution_policy, state)
    binding = CONTRACTS.build_execution_intent_binding(
        execution_policy,
        projection,
        source_invocation_id="invoke-fresh-session-001",
        created_at="2026-08-04T00:00:00Z",
        execution_mode="one-unit",
    )
    return {
        "schema_version": "1.0.0",
        "execution_policy": execution_policy,
        "execution_entry": projection,
        "execution_binding": binding,
        "selected_unit": {
            "work_pack_id": execution_policy["work_pack_id"],
            "swu_id": "SWU-GENERIC-001",
        },
        "authority_effect": "none",
    }


class FreshSessionFixture:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="wpeg-fresh-session-")
        self.root = Path(self.temporary.name)
        (self.root / "evidence").mkdir()
        self.execution_policy = policy()
        self.original_request = guard_request(
            self.execution_policy, "owner-prerequisite"
        )
        self.original_receipt = FAST_GUARD.classify_fast_entry(
            self.original_request
        )
        self.current_request = guard_request(self.execution_policy, "task-ready")
        self.current_receipt = FAST_GUARD.classify_fast_entry(self.current_request)
        route_request = {
            "schema_version": "1.0.0",
            "execution_policy": copy.deepcopy(self.execution_policy),
            "execution_entry": copy.deepcopy(
                self.original_request["execution_entry"]
            ),
            "execution_binding": copy.deepcopy(
                self.original_request["execution_binding"]
            ),
            "candidate_routes": [
                copy.deepcopy(self.original_receipt["owner_packet"])
            ],
            "installed_owner_routes": [
                {"capability": "invoke", "mode": "refresh"}
            ],
            "available_inputs": ["owner-input.json"],
            "consumed_route_fingerprints": [],
            "authorization_flag": None,
            "authority_effect": "none",
        }
        self.route_request = route_request
        self.route_receipt = ROUTER.evaluate_work_pack_route(route_request)
        self.owner_receipt = {
            "schema_version": "1.0.0",
            "receipt_id": "owner-receipt-001",
            "result": "pass",
            "work_pack_id": self.execution_policy["work_pack_id"],
            "selected_unit": "SWU-GENERIC-001",
            "binding_id": self.original_receipt["binding_id"],
            "binding_digest": self.original_receipt["binding_digest"],
            "route_fingerprint": self.original_receipt["route_fingerprint"],
            "route": copy.deepcopy(self.original_receipt["owner_packet"]),
            "authorization_prompt_required": False,
            "authority_effect": "none",
        }
        self._write_owner()

    def close(self) -> None:
        self.temporary.cleanup()

    def _write_owner(self) -> None:
        (self.root / "evidence" / "owner-receipt.json").write_text(
            json.dumps(self.owner_receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def request(self, state_directory: str = "state/default") -> dict:
        state_projection = {
            "chain_id": "chain-fresh-session-001",
            "loop_id": "wpol-111111111111111111111111",
            "work_pack_id": self.execution_policy["work_pack_id"],
            "frontier": self.execution_policy["frontier"],
            "selected_unit": "SWU-GENERIC-001",
            "session_budget": 1,
        }
        return {
            "schema_version": "1.0.0",
            "chain_id": state_projection["chain_id"],
            "loop_id": state_projection["loop_id"],
            "loop_state_digest": RESUME.canonical_digest(state_projection),
            "repository_root": ".",
            "resume_state_directory": state_directory,
            "work_pack_id": self.execution_policy["work_pack_id"],
            "work_pack_semantic_digest": self.execution_policy[
                "work_pack_semantic_digest"
            ],
            "captured_frontier": ["SWU-GENERIC-001"],
            "selected_unit": "SWU-GENERIC-001",
            "original_task_session": {
                "session_id": "task-session-blocked-001",
                "cursor": "cursor-blocked-001",
            },
            "original_guard": {
                "request": copy.deepcopy(self.original_request),
                "receipt": copy.deepcopy(self.original_receipt),
            },
            "route_admission": {
                "request": copy.deepcopy(self.route_request),
                "receipt": copy.deepcopy(self.route_receipt),
            },
            "owner_join": {
                "receipt_ref": exact_ref(
                    self.root, "evidence/owner-receipt.json"
                ),
                "receipt": copy.deepcopy(self.owner_receipt),
            },
            "reclassification": {
                "request": copy.deepcopy(self.current_request),
                "receipt": copy.deepcopy(self.current_receipt),
            },
            "resumed_route_fingerprints": [],
            "visited_task_session_ids": ["task-session-blocked-001"],
            "visited_session_cursors": ["cursor-blocked-001"],
            "task_session_receipts": [],
            "session_budget": {
                "captured_max_task_sessions": 1,
                "current_max_task_sessions": 1,
                "task_sessions_started": 0,
            },
            "authority_effect": "none",
        }

    def rewrite_owner(self, request: dict) -> None:
        self._write_owner()
        request["owner_join"] = {
            "receipt_ref": exact_ref(self.root, "evidence/owner-receipt.json"),
            "receipt": copy.deepcopy(self.owner_receipt),
        }


class FreshSessionResumeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = FreshSessionFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_passing_owner_join_admits_one_durable_fresh_session(self) -> None:
        request = self.fixture.request()
        receipt = RESUME.admit_fresh_task_session(request, self.fixture.root)
        RESUME.validate_fresh_session_receipt(receipt, request)
        self.assertEqual(receipt["decision"], "start-fresh-session")
        self.assertEqual(receipt["fresh_task_session_start_count"], 1)
        self.assertEqual(receipt["fresh_task_session"]["selector"], request["selected_unit"])
        self.assertNotEqual(
            receipt["fresh_task_session"]["session_id"],
            request["original_task_session"]["session_id"],
        )
        self.assertEqual(receipt["joined_owner_receipt_count"], 1)
        self.assertEqual(receipt["authorization_prompt_count"], 0)
        self.assertFalse(receipt["recursive_resume"])
        self.assertEqual(receipt["mutation_count"], 0)
        self.assertEqual(receipt["evidence_write_count"], 1)
        ledger = self.fixture.root / receipt["ledger_event_ref"]["path"]
        self.assertTrue(ledger.is_file())

        replay = RESUME.admit_fresh_task_session(request, self.fixture.root)
        self.assertEqual(replay["decision"], "block")
        self.assertEqual(replay["code"], "FRESH_SESSION_REPLAY")
        self.assertEqual(replay["fresh_task_session_start_count"], 0)

    def test_owner_join_failures_block_without_admission(self) -> None:
        cases = []

        missing = self.fixture.request("state/missing")
        missing["owner_join"]["receipt_ref"]["path"] = "evidence/missing.json"
        cases.append(("missing", missing, "JOIN_RECEIPT_MISSING"))

        stale = self.fixture.request("state/stale")
        stale["owner_join"]["receipt_ref"]["sha256"] = "0" * 64
        cases.append(("stale", stale, "JOIN_RECEIPT_STALE"))

        blocked = self.fixture.request("state/blocked")
        self.fixture.owner_receipt["result"] = "block"
        self.fixture.rewrite_owner(blocked)
        cases.append(("blocked", blocked, "OWNER_PREREQUISITE_BLOCKED"))

        for name, request, code in cases:
            with self.subTest(name=name):
                receipt = RESUME.admit_fresh_task_session(request, self.fixture.root)
                self.assertEqual(receipt["decision"], "block")
                self.assertEqual(receipt["code"], code)
                self.assertEqual(receipt["fresh_task_session_start_count"], 0)

    def test_identity_route_and_reclassification_mismatches_block(self) -> None:
        wrong_pack = self.fixture.request("state/wrong-pack")
        wrong_pack["work_pack_id"] = "WP-FOREIGN"

        forged_admission = self.fixture.request("state/forged-admission")
        forged_admission["route_admission"]["receipt"]["matched_route"][
            "target"
        ] = "expanded target"

        unchanged = self.fixture.request("state/unchanged")
        unchanged["reclassification"] = {
            "request": copy.deepcopy(self.fixture.original_request),
            "receipt": copy.deepcopy(self.fixture.original_receipt),
        }

        cases = [
            (wrong_pack, "RESUME_IDENTITY_MISMATCH"),
            (forged_admission, "ROUTE_ADMISSION_RECEIPT_MISMATCH"),
            (unchanged, "UNCHANGED_PREREQUISITE_FINGERPRINT"),
        ]
        for request, expected in cases:
            with self.subTest(expected=expected):
                receipt = RESUME.admit_fresh_task_session(request, self.fixture.root)
                self.assertEqual(receipt["decision"], "block")
                self.assertEqual(receipt["code"], expected)

        mismatched_owner = self.fixture.request("state/mismatched-owner")
        canonical_owner = copy.deepcopy(self.fixture.owner_receipt)
        self.fixture.owner_receipt["binding_digest"] = "9" * 64
        self.fixture.rewrite_owner(mismatched_owner)
        receipt = RESUME.admit_fresh_task_session(
            mismatched_owner, self.fixture.root
        )
        self.assertEqual(receipt["decision"], "block")
        self.assertEqual(receipt["code"], "OWNER_RECEIPT_MISMATCH")
        self.fixture.owner_receipt = canonical_owner
        self.fixture._write_owner()

    def test_fingerprint_cursor_receipt_and_budget_cycles_block(self) -> None:
        repeated_fingerprint = self.fixture.request("state/fingerprint")
        repeated_fingerprint["resumed_route_fingerprints"] = [
            self.fixture.original_receipt["route_fingerprint"]
        ]

        first = RESUME.admit_fresh_task_session(
            self.fixture.request("state/cursor-source"), self.fixture.root
        )
        repeated_cursor = self.fixture.request("state/cursor")
        repeated_cursor["visited_session_cursors"].append(
            first["fresh_task_session"]["cursor"]
        )

        receipt_slot = self.fixture.request("state/receipt-slot")
        receipt_slot["task_session_receipts"] = [
            {
                "unit_id": "SWU-GENERIC-001",
                "session_id": "task-session-existing",
                "receipt_id": "receipt-existing",
            }
        ]
        receipt_slot["session_budget"]["task_sessions_started"] = 1

        budget_drift = self.fixture.request("state/budget-drift")
        budget_drift["session_budget"]["current_max_task_sessions"] = 2

        exhausted = self.fixture.request("state/exhausted")
        exhausted["session_budget"]["task_sessions_started"] = 1

        cases = [
            (repeated_fingerprint, "OWNER_ROUTE_FINGERPRINT_REPEATED"),
            (repeated_cursor, "TASK_SESSION_CURSOR_REPEATED"),
            (receipt_slot, "SESSION_BUDGET_EXHAUSTED"),
            (budget_drift, "SESSION_BUDGET_DRIFT"),
            (exhausted, "SESSION_BUDGET_EXHAUSTED"),
        ]
        for request, expected in cases:
            with self.subTest(expected=expected):
                receipt = RESUME.admit_fresh_task_session(request, self.fixture.root)
                self.assertEqual(receipt["decision"], "block")
                self.assertEqual(receipt["code"], expected)

    def test_cli_is_stdout_only_except_for_declared_admission_event(self) -> None:
        request = self.fixture.request("state/cli")
        input_path = self.fixture.root / "request.json"
        input_path.write_text(
            json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(SPELL_ROOT / "scripts" / "resume-fresh-task-session.py"),
                "--input",
                str(input_path),
                "--repository-root",
                str(self.fixture.root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        receipt = json.loads(completed.stdout)
        self.assertEqual(receipt["decision"], "start-fresh-session")
        self.assertEqual(receipt["evidence_write_count"], 1)
        self.assertTrue(
            (self.fixture.root / receipt["ledger_event_ref"]["path"]).is_file()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Regression tests for Invoke-authored execution-entry admission."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SPELL_ROOT / "scripts" / "validate_work_pack_execution_entry.py"


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "work_pack_execution_entry_validator", SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


def projection() -> dict:
    routes = [
        {
            "route_id": "task-u1",
            "frontier_swu": "SWU-U1",
            "capability": "task-session",
            "mode": "execute",
            "target": "SWU-U1",
            "write_scope": ["packages/u1/source.py"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["planning/work-pack.json#/swus/0"],
            "expected_receipt": "receipts/u1.json",
        },
        {
            "route_id": "closeout-u1",
            "frontier_swu": "SWU-U1",
            "capability": "invoke",
            "mode": "refresh-apply-approved",
            "target": "SWU-U1-closeout",
            "write_scope": ["planning/work-pack.json"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["receipts/u1.json"],
            "expected_receipt": "planning/closeout/u1.json",
        },
    ]
    return {
        "schema_version": "arcanum.work-pack-execution-entry/v1",
        "work_pack_id": "WP-PUBLIC-PROJECTION",
        "admission_timing": "selected-unit-at-task-session",
        "frontier": ["SWU-U1"],
        "execution_policy": {
            "route_policy": "automatic-in-scope",
            "allowed_routes": routes,
            "allowed_routes_digest": VALIDATOR.canonical_digest(routes),
            "digest_algorithm": "sha256 of RFC8785-compatible canonical JSON for allowed_routes",
            "automatic_decisions": [
                "internal-tool-selection",
                "capability-owner-routing",
                "reversible-local-default",
                "declared-fallback",
                "declared-retry",
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
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
            "declared_retry": {
                "max": 1,
                "only_after": "REPAIRABLE_OWNER_CONDITION",
                "same_route_and_binding": True,
            },
        },
        "execution_entry": {
            "state": "selection-ready",
            "selected_unit": None,
            "route_id": None,
            "next_owner": "implementation-readiness:execute",
        },
        "pre_execution_owner_prerequisite": None,
        "continuation_rule": "Only the declared closeout route may advance the frontier.",
        "authority_effect": "none",
    }


class WorkPackExecutionEntryTests(unittest.TestCase):
    def assert_code(self, expected: str, candidate: dict) -> None:
        with self.assertRaises(VALIDATOR.ProjectionError) as raised:
            VALIDATOR.validate_projection(candidate)
        self.assertEqual(raised.exception.code, expected)

    def test_valid_closeout_route_uses_shared_reversible_effect(self) -> None:
        receipt = VALIDATOR.validate_projection(projection())
        self.assertEqual(receipt["status"], "pass")
        self.assertEqual(receipt["route_count"], 2)

    def test_closeout_only_is_not_an_effect_class(self) -> None:
        candidate = projection()
        candidate["execution_policy"]["allowed_routes"][1][
            "effect_class"
        ] = "repository-local-reversible-closeout-only"
        candidate["execution_policy"]["allowed_routes_digest"] = (
            VALIDATOR.canonical_digest(
                candidate["execution_policy"]["allowed_routes"]
            )
        )
        self.assert_code("EXECUTION_ENTRY_SCHEMA_INVALID", candidate)

    def test_unknown_automatic_decision_blocks(self) -> None:
        candidate = projection()
        candidate["execution_policy"]["automatic_decisions"].append(
            "deterministic-declared-successor"
        )
        self.assert_code("EXECUTION_ENTRY_SCHEMA_INVALID", candidate)

    def test_stale_allowed_routes_digest_blocks(self) -> None:
        candidate = projection()
        candidate["execution_policy"]["allowed_routes_digest"] = "f" * 64
        self.assert_code("EXECUTION_ENTRY_ROUTES_DIGEST_STALE", candidate)

    def test_fixture_copy_matches_shipped_runtime_fixture(self) -> None:
        development_fixture = (
            SPELL_ROOT
            / "development/fixtures/execution-contracts/execution-contract-cases.json"
        )
        runtime_fixture = (
            SPELL_ROOT / "fixtures/execution-contracts/execution-contract-cases.json"
        )
        self.assertEqual(development_fixture.read_bytes(), runtime_fixture.read_bytes())


if __name__ == "__main__":
    unittest.main()

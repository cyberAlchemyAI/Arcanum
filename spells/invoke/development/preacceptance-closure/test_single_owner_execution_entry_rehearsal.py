#!/usr/bin/env python3
"""Focused regressions for typed single-owner rehearsal frontiers."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SCRIPT = (
    REPOSITORY_ROOT
    / "arcanum/spells/invoke/scripts/rehearse_execution_entry_consumers.py"
)


def module():
    specification = importlib.util.spec_from_file_location(
        "invoke_single_owner_execution_entry_rehearsal", SCRIPT
    )
    loaded = importlib.util.module_from_spec(specification)
    assert specification and specification.loader
    specification.loader.exec_module(loaded)
    return loaded


def owner_fixture(root: Path):
    identity = "invoke.precloseout-refresh-closeout-receipt.v1"
    schema_path = root / "owner-receipt.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"schema_version": {"const": identity}},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    reference = {
        "path": schema_path.name,
        "sha256": hashlib.sha256(schema_path.read_bytes()).hexdigest(),
        "size_bytes": schema_path.stat().st_size,
    }
    units = [
        {"unit_id": "SWU-001", "owner_receipt_schema_identity": identity},
        {"unit_id": "SWU-002", "owner_receipt_schema_identity": identity},
    ]
    binding = {"artifact_ref": reference, "selector": ""}
    config = {
        "task_session_closeout_contracts": [
            {
                "unit_id": item["unit_id"],
                "expected_owner_receipt_schema_ref": copy.deepcopy(binding),
            }
            for item in units
        ]
    }
    return identity, reference, units, config


class SingleOwnerExecutionEntryRehearsalTests(unittest.TestCase):
    def test_single_owner_closeout_frontier_resolves_every_unit(self):
        rehearsal = module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            identity, reference, units, config = owner_fixture(root)
            rehearsal.REPOSITORY_ROOT = root
            identities, refs = rehearsal.resolve_owner_closeout_frontier(
                units, config
            )
            self.assertEqual(
                identities, {"SWU-001": identity, "SWU-002": identity}
            )
            self.assertEqual(refs, [reference])

    def test_owner_closeout_frontier_missing_mismatched_or_incomplete_fails(self):
        rehearsal = module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, _, units, valid = owner_fixture(root)
            rehearsal.REPOSITORY_ROOT = root
            cases = {
                "missing-binding": {
                    "task_session_closeout_contracts": [
                        {"unit_id": "SWU-001"},
                        valid["task_session_closeout_contracts"][1],
                    ]
                },
                "incomplete-frontier": {
                    "task_session_closeout_contracts": valid[
                        "task_session_closeout_contracts"
                    ][:1]
                },
                "duplicate-frontier": {
                    "task_session_closeout_contracts": [
                        valid["task_session_closeout_contracts"][0],
                        copy.deepcopy(valid["task_session_closeout_contracts"][0]),
                    ]
                },
            }
            for case_id, config in cases.items():
                with self.subTest(case_id=case_id):
                    with self.assertRaises(ValueError):
                        rehearsal.resolve_owner_closeout_frontier(units, config)

            mismatched_units = copy.deepcopy(units)
            mismatched_units[1]["owner_receipt_schema_identity"] = "wrong.identity.v1"
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                rehearsal.resolve_owner_closeout_frontier(mismatched_units, valid)

    def test_task_session_routes_do_not_collapse_invoke_routes(self):
        rehearsal = module()
        task_routes = [
            {
                "frontier_swu": unit_id,
                "capability": "task-session",
                "mode": "execute",
                "write_scope": [f"src/{unit_id}.py"],
            }
            for unit_id in ("SWU-001", "SWU-002")
        ]
        invoke_routes = [
            {
                "frontier_swu": unit_id,
                "capability": "invoke",
                "mode": "refresh",
                "write_scope": [f"evidence/{unit_id}/owner.json"],
            }
            for unit_id in ("SWU-001", "SWU-002")
        ]
        selected = rehearsal.resolve_task_session_execution_routes(
            {
                "allowed_routes": [
                    task_routes[0],
                    invoke_routes[0],
                    invoke_routes[1],
                    task_routes[1],
                ]
            },
            {"SWU-001", "SWU-002"},
        )
        self.assertEqual(set(selected), {"SWU-001", "SWU-002"})
        self.assertTrue(
            all(route["capability"] == "task-session" for route in selected.values())
        )

    def test_missing_duplicate_or_out_of_frontier_task_session_route_fails(self):
        rehearsal = module()
        route = {
            "frontier_swu": "SWU-001",
            "capability": "task-session",
            "mode": "execute",
            "write_scope": ["src/SWU-001.py"],
        }
        cases = {
            "missing": {"allowed_routes": [route]},
            "duplicate": {"allowed_routes": [route, copy.deepcopy(route)]},
            "outside": {
                "allowed_routes": [
                    route,
                    {**copy.deepcopy(route), "frontier_swu": "SWU-999"},
                ]
            },
        }
        for case_id, policy in cases.items():
            with self.subTest(case_id=case_id):
                with self.assertRaises(ValueError):
                    rehearsal.resolve_task_session_execution_routes(
                        policy, {"SWU-001", "SWU-002"}
                    )


if __name__ == "__main__":
    unittest.main()

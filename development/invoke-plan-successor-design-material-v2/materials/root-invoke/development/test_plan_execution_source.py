#!/usr/bin/env python3
"""Integration tests for the canonical Invoke Plan execution source."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path

INVOKE_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = INVOKE_ROOT.parents[1]
COMPILER_PATH = INVOKE_ROOT / "scripts" / "compile_plan_execution_source.py"
WPRA_TEST_PATH = ARCANUM_ROOT / "spells" / "work-pack-readiness-audit" / "development" / "test_work_pack_readiness_v2.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMPILER = load_module("compile_plan_execution_source", COMPILER_PATH)
WPRA_TEST = load_module("wpra_v2_fixture", WPRA_TEST_PATH)


class PlanExecutionSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = WPRA_TEST.V2Fixture()
        config = self.fixture.config()
        unit = config["execution_bindings"][0]
        route = {
            "route_id": "route-u1", "frontier_swu": "U1",
            "capability": "task-session", "mode": "execute", "target": "U1",
            "write_scope": unit["allowed_writes"],
            "effect_class": "repository-local-reversible",
            "required_inputs": ["evidence.json"], "expected_receipt": "receipts/U1.json",
        }
        config["execution_policy"] = {
            "work_pack_id": "WP-SYNTHETIC-001", "route_policy": "automatic-in-scope",
            "allowed_routes": [route], "allowed_routes_digest": COMPILER.digest([route]),
            "automatic_decisions": ["unique-successor-continuation"],
            "stop_decisions": ["semantic-choice"],
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
        }
        self.source = {
            "schema_version": "invoke.plan-execution-source.v1",
            "source_id": "synthetic-plan-source-001",
            "work_pack": {
                "work_pack_id": "WP-SYNTHETIC-001", "title": "Synthetic Plan Source",
                "objective": "Prove one machine source crosses the installed WPRA boundary.",
                "execution_designation": "execution-candidate",
            },
            "requested_effect": {
                "effect_class": "repository-local-reversible", "external_effect": "none",
                "publication": "forbidden", "deployment": "forbidden",
            },
            "route_contracts": [copy.deepcopy(route)],
            "wpra_config": config,
        }

    def tearDown(self) -> None:
        self.fixture.close()

    def test_schema_semantics_human_view_and_real_wpra_two_run(self) -> None:
        self.assertEqual(COMPILER.validate(self.source), [])
        source_path = self.fixture.root / "PLAN-EXECUTION-SOURCE.json"
        source_path.write_text(json.dumps(self.source, indent=2))
        output = self.fixture.root / "compiled"
        completed = subprocess.run(
            [sys.executable, str(COMPILER_PATH), "--source", str(source_path),
             "--output-dir", str(output)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        receipt = json.loads((output / "SOURCE-VALIDATION-RECEIPT.json").read_text())
        self.assertEqual(receipt["wpra_rehearsal"]["runs"], 2)
        self.assertEqual(receipt["wpra_rehearsal"]["verdicts"], ["pass", "pass"])
        self.assertFalse(receipt["wpra_rehearsal"]["configured_commands_executed"])
        self.assertIn("Synthetic Plan Source", (output / "WORK-PACK.md").read_text())
        emitted = json.loads((output / "WPRA-CONFIG.json").read_text())
        self.assertEqual(COMPILER.digest(emitted), COMPILER.digest(self.source["wpra_config"]))

    def test_cross_field_drift_blocks(self) -> None:
        cases = []
        wrong_id = copy.deepcopy(self.source)
        wrong_id["work_pack"]["work_pack_id"] = "WRONG"
        cases.append(wrong_id)
        wrong_budget = copy.deepcopy(self.source)
        wrong_budget["wpra_config"]["approval_policy"]["run_budget"]["max_task_session_requests"] = 2
        cases.append(wrong_budget)
        wrong_writes = copy.deepcopy(self.source)
        wrong_writes["wpra_config"]["execution_policy"]["allowed_routes"][0]["write_scope"] = ["other.txt"]
        cases.append(wrong_writes)
        route_fields = {
            "target": "DIFFERENT-UNIT", "capability": "invoke", "mode": "refresh",
            "required_inputs": ["different.json"], "expected_receipt": "different.json",
        }
        for field, value in route_fields.items():
            drift = copy.deepcopy(self.source)
            drift["wpra_config"]["execution_policy"]["allowed_routes"][0][field] = value
            drift["wpra_config"]["execution_policy"]["allowed_routes_digest"] = COMPILER.digest(
                drift["wpra_config"]["execution_policy"]["allowed_routes"]
            )
            cases.append(drift)
        for source in cases:
            self.assertTrue(COMPILER.validate(source))

        source_path = self.fixture.root / "INVALID-SOURCE.json"
        source_path.write_text(json.dumps(wrong_id, indent=2))
        output = self.fixture.root / "must-not-exist"
        completed = subprocess.run(
            [sys.executable, str(COMPILER_PATH), "--source", str(source_path),
             "--output-dir", str(output)],
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())

    def test_wpra_block_and_second_run_failure_publish_nothing(self) -> None:
        source = copy.deepcopy(self.source)
        source["wpra_config"]["expected_material_digests"]["U1"] = "b" * 64
        source_path = self.fixture.root / "WPRA-BLOCK-SOURCE.json"
        source_path.write_text(json.dumps(source, indent=2))
        blocked_output = self.fixture.root / "blocked-output"
        completed = subprocess.run(
            [sys.executable, str(COMPILER_PATH), "--source", str(source_path),
             "--output-dir", str(blocked_output)],
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(blocked_output.exists())

        pass_report = {"verdict": "pass", "audit_projection_digest": "a" * 64}
        block_report = {"verdict": "block", "audit_projection_digest": None}
        second_output = self.fixture.root / "second-run-block"
        with mock.patch.object(COMPILER, "run_wpra", side_effect=[pass_report, block_report]):
            with self.assertRaises(ValueError):
                COMPILER.compile_source(self.source, second_output)
        self.assertFalse(second_output.exists())

    def test_future_post_produce_validator_is_not_executed(self) -> None:
        command = self.source["wpra_config"]["execution_bindings"][0]["validation_contracts"][0]
        self.assertEqual(command["phase"], "post-produce")
        self.assertFalse((self.fixture.root / command["argv"][0]).exists())
        self.assertEqual(COMPILER.validate(self.source), [])

    def test_runtime_resolves_wpra_as_sibling_package(self) -> None:
        self.assertEqual(COMPILER.WPRA_ROOT.parent, COMPILER.INVOKE_ROOT.parent)
        self.assertTrue(COMPILER.WPRA_SCHEMA.is_file())
        self.assertTrue(COMPILER.WPRA_RUNNER.is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Exercise Invoke Plan's real Implementation Readiness producer boundary."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


INVOKE_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = INVOKE_ROOT.parents[1]
REPOSITORY_ROOT = ARCANUM_ROOT.parent
INTEGRATION_PATH = (
    ARCANUM_ROOT
    / "spells"
    / "implementation-readiness"
    / "development"
    / "integration"
    / "test_work_pack_execution.py"
)
PRODUCER_PATH = INVOKE_ROOT / "scripts" / "prepare_plan_implementation_readiness.py"


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


INTEGRATION = load_module("invoke_plan_readiness_fixture", INTEGRATION_PATH)


class InvokePlanImplementationReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan_case = INTEGRATION.PLAN_ONCE.PLAN.PlanOnceSelectionTests()
        self.plan_case.setUp()
        self.config = self.plan_case.config()
        self.report = self.plan_case.audit(self.config)
        self.root = self.plan_case.fixture.root

    def tearDown(self) -> None:
        self.plan_case.tearDown()

    def write_json(self, name: str, value: dict) -> Path:
        path = self.root / name
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path

    def run_producer(
        self,
        config: dict,
        report: dict,
        output_name: str,
        *,
        producer_path: Path = PRODUCER_PATH,
        run_audit: bool = False,
    ):
        config_path = self.write_json(f"{output_name}-config.json", config)
        output_path = self.root / f"{output_name}-receipt.json"
        command = [
            sys.executable,
            str(producer_path),
            "--audit-config",
            str(config_path),
        ]
        if run_audit:
            command.extend(
                ["--audit-output-dir", str(self.root / f"{output_name}-audit-output")]
            )
        else:
            report_path = self.write_json(f"{output_name}-report.json", report)
            command.extend(["--audit-report", str(report_path)])
        command.extend(
            [
                "--proof-invocation-id",
                f"invoke-plan-{output_name}",
                "--proof-created-at",
                "2026-08-24T14:00:00Z",
                "--output",
                str(output_path),
            ]
        )
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        return completed, output_path

    def test_actual_plan_bytes_produce_non_reusable_task_ready_proof(self) -> None:
        completed, output_path = self.run_producer(
            self.config, self.report, "valid"
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        receipt = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["code"], "PLAN_IMPLEMENTATION_READY")
        self.assertEqual(receipt["fast_entry_proof"]["code"], "TASK_READY")
        self.assertFalse(receipt["reusable_for_execution"])
        self.assertFalse(receipt["mutation_ready"])
        self.assertEqual(receipt["authority_effect"], "none")

    def test_one_command_runs_wpra_then_real_task_ready_proof(self) -> None:
        completed, output_path = self.run_producer(
            self.config, self.report, "one-command", run_audit=True
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        receipt = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["code"], "PLAN_IMPLEMENTATION_READY")
        self.assertEqual(receipt["fast_entry_proof"]["code"], "TASK_READY")
        self.assertTrue(
            (self.root / "one-command-audit-output/selection-handoff.json").is_file()
        )

    def test_one_command_preserves_wpra_failure_status(self) -> None:
        config = copy.deepcopy(self.config)
        config["admission_timing"] = "unsupported"
        completed, output_path = self.run_producer(
            config, self.report, "audit-block", run_audit=True
        )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertIn("Work Pack Readiness Audit failed with exit 1", completed.stderr)
        self.assertFalse(output_path.exists())

    def test_missing_full_frontier_task_route_blocks_without_receipt(self) -> None:
        config = copy.deepcopy(self.config)
        report = copy.deepcopy(self.report)
        routes = copy.deepcopy(config["execution_policy"]["allowed_routes"])
        routes[0]["capability"] = "invoke"
        route_digest = INTEGRATION.READINESS.allowed_routes_digest(routes)
        config["execution_policy"]["allowed_routes"] = routes
        config["execution_policy"]["allowed_routes_digest"] = route_digest
        report["manifest"]["allowed_routes"] = copy.deepcopy(routes)
        report["manifest"]["allowed_routes_digest"] = route_digest
        completed, output_path = self.run_producer(config, report, "invalid")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("PLAN_TASK_SESSION_ROUTE_NOT_UNIQUE", completed.stderr)
        self.assertFalse(output_path.exists())

    def test_generated_host_packages_resolve_readiness_as_a_sibling(self) -> None:
        producers = [
            REPOSITORY_ROOT
            / ".agents/skills/invoke/scripts/prepare_plan_implementation_readiness.py",
            REPOSITORY_ROOT
            / ".claude/skills/invoke/scripts/prepare_plan_implementation_readiness.py",
        ]
        for index, producer in enumerate(producers, 1):
            with self.subTest(producer=str(producer)):
                completed, output_path = self.run_producer(
                    self.config,
                    self.report,
                    f"generated-{index}",
                    producer_path=producer,
                    run_audit=True,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                receipt = json.loads(output_path.read_text(encoding="utf-8"))
                self.assertEqual(receipt["code"], "PLAN_IMPLEMENTATION_READY")
                self.assertFalse(receipt["reusable_for_execution"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

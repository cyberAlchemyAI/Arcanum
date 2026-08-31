#!/usr/bin/env python3
"""Generic regressions for workload-bound live-entry rehearsal deadlines."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
ADAPTER_PATH = HERE / "real_consumer_rehearsal.py"
BUDGET_SCHEMA = (
    HERE.parents[1]
    / "schemas/preacceptance-live-entry-rehearsal-budget-v1.schema.json"
)


def load_adapter() -> Any:
    spec = importlib.util.spec_from_file_location(
        "invoke_live_entry_rehearsal_budget", ADAPTER_PATH
    )
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load the live-entry rehearsal adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ADAPTER = load_adapter()


def reference(path: str, size_bytes: int = 6000) -> dict[str, Any]:
    return {"path": path, "sha256": "a" * 64, "size_bytes": size_bytes}


def invocation(identifier: str, refs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "input_closure_ref": reference(f"closures/{identifier}.json", 1000),
        "input_refs": refs,
        "timeout_seconds": 120,
    }


def large_preparation() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    inputs = [reference(f"inputs/{index:04d}.json") for index in range(1920)]
    chunks = [inputs[index::7] for index in range(7)]
    owner = invocation("owner", chunks[0])
    step_ids = ["readiness", "selection", "fast-entry", "context", "admission"]
    steps = [
        {
            "step_id": step_id,
            "invocation": invocation(step_id, chunks[index + 1]),
            "output_paths": [f"controls/{step_id}.json"],
        }
        for index, step_id in enumerate(step_ids)
    ]
    governance = invocation("governance", chunks[6])
    governance["output_paths"] = [
        f"runs/checkpoints/{index:02d}.json" for index in range(1, 5)
    ] + ["runs/execution-ticket.json"]
    preparation = {
        "owner_acceptance_validation": owner,
        "preparation_steps": steps,
        "governance_runner": governance,
        "preparation_receipt_path": "controls/preparation-receipt.json",
    }
    return reference("request.json", 500000), reference(
        "preparation.json", 500000
    ), preparation


class LiveEntryRehearsalBudgetTests(unittest.TestCase):
    def test_large_exact_workload_derives_a_finite_schema_valid_budget(self) -> None:
        request_ref, preparation_ref, preparation = large_preparation()
        budget = ADAPTER.derive_live_entry_rehearsal_budget(
            request_ref, preparation_ref, preparation, "readiness"
        )
        schema = json.loads(BUDGET_SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(budget)
        self.assertEqual(budget["invocation_count"], 7)
        self.assertGreaterEqual(budget["unique_input_ref_count"], 1929)
        self.assertEqual(budget["exact_output_path_count"], 11)
        self.assertGreater(
            budget["success_coordinator_timeout_seconds"],
            budget["declared_invocation_timeout_seconds"],
        )
        self.assertLessEqual(
            budget["stage_timeout_seconds"], budget["hard_maximum_seconds"]
        )
        self.assertEqual(
            ADAPTER.validate_live_entry_rehearsal_budget(budget, budget), budget
        )

    def test_stale_and_underspecified_budgets_fail_closed(self) -> None:
        request_ref, preparation_ref, preparation = large_preparation()
        expected = ADAPTER.derive_live_entry_rehearsal_budget(
            request_ref, preparation_ref, preparation, "readiness"
        )
        stale = dict(expected)
        stale["unique_input_ref_count"] -= 1
        stale["budget_digest"] = ADAPTER.canonical_digest(
            {key: value for key, value in stale.items() if key != "budget_digest"}
        )
        with self.assertRaisesRegex(ValueError, "stale or underspecified"):
            ADAPTER.validate_live_entry_rehearsal_budget(stale, expected)
        underspecified = dict(expected)
        del underspecified["exact_output_path_count"]
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            ADAPTER.validate_live_entry_rehearsal_budget(underspecified, expected)

    def test_real_overrun_remains_a_hard_timeout(self) -> None:
        started = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            ADAPTER.run_bounded(
                [sys.executable, "-c", "import time; time.sleep(5)"],
                1,
                check=False,
                capture_output=True,
            )
        self.assertLess(time.monotonic() - started, 3)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
SKILL = ARCANUM_ROOT / "runtime/orchestrate/SKILL.md"
HOST = ARCANUM_ROOT / "runtime/orchestrate/hosts/codex-native.md"
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
VALIDATOR = ARCANUM_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"
COMPILE_FIXTURES = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"
PREFLIGHT_FIXTURES = Path(__file__).resolve().parent / "fixtures"
RECEIPT_SCHEMA = Path(__file__).resolve().parent / "preflight-receipt.schema.json"
ACCEPTANCE_RECEIPTS = {
    "expected-invalid.json": "invalid-dispatch.receipt.json",
    "expected-authorization-pending.json": "authorization-pending.receipt.json",
    "expected-missing-host-operation.json": "missing-host-operation.receipt.json",
    "expected-ready.json": "ready.receipt.json",
}

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator", COORDINATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {COORDINATOR_PATH}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    _, raw, _ = text.split("---", 2)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return value


def evaluate_preflight(
    dispatch_path: Path,
    run_id: str,
    available_operations: set[str],
    output_dir: Path,
) -> dict[str, Any]:
    skill = load_frontmatter(SKILL)
    host = load_frontmatter(HOST)
    contract = skill["execute_contract"]
    required = list(host["required_execute_operations"])
    dispatch = load_json(dispatch_path)
    authorization = str((dispatch.get("subagent_strategy") or {}).get("authorization", "unresolved"))
    base = {
        "schema_version": "arcanum.native-dispatch-runner.preflight-receipt.v0.1",
        "command": contract["grammar"],
        "dispatch_id": str(dispatch.get("dispatch_id", "")),
        "run_id": run_id,
        "host_id": host["host_id"],
        "required_operations": required,
        "available_operations": sorted(available_operations),
        "spawn_attempt_count": 0,
    }

    validation = coordinator.validate_dispatch(dispatch_path, VALIDATOR)
    if validation.get("validation") != contract["required_validation_result"]:
        return {
            **base,
            "status": "block",
            "state": "blocked",
            "validation_status": str(validation.get("validation", "block")),
            "authorization_status": "unresolved",
            "missing_operations": [],
            "action_count": 0,
            "run_plan_emitted": False,
            "blockers": ["dispatch_validation_failed"],
        }

    if authorization not in set(contract["authorization_satisfied"]):
        return {
            **base,
            "status": "block",
            "state": "authorization_pending" if authorization == "requires_user_permission" else "blocked",
            "validation_status": "pass",
            "authorization_status": authorization,
            "missing_operations": [],
            "action_count": 0,
            "run_plan_emitted": False,
            "blockers": ["execution_authorization_not_satisfied"],
        }

    missing = [operation for operation in required if operation not in available_operations]
    if missing:
        return {
            **base,
            "status": "block",
            "state": "blocked",
            "validation_status": "pass",
            "authorization_status": authorization,
            "missing_operations": missing,
            "action_count": 0,
            "run_plan_emitted": False,
            "blockers": ["native_host_operations_missing"],
        }

    result = coordinator.compile_to_directory(dispatch_path, run_id, output_dir, VALIDATOR)
    return {
        **base,
        "status": "pass",
        "state": result["state"]["state"],
        "validation_status": "pass",
        "authorization_status": authorization,
        "missing_operations": [],
        "action_count": len(result["run_plan"]["actions"]),
        "run_plan_emitted": True,
        "blockers": [],
    }


class PreflightContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = load_frontmatter(SKILL)
        cls.host = load_frontmatter(HOST)
        cls.schema = load_json(RECEIPT_SCHEMA)
        cls.available = set(cls.host["required_execute_operations"])

    def assert_receipt(self, actual: dict[str, Any], expected_name: str) -> None:
        Draft202012Validator(self.schema).validate(actual)
        self.assertEqual(actual, load_json(PREFLIGHT_FIXTURES / expected_name))
        self.assertEqual(actual, load_json(Path(__file__).resolve().parent / ACCEPTANCE_RECEIPTS[expected_name]))
        self.assertEqual(actual["spawn_attempt_count"], 0)

    def test_execute_grammar_is_exact_and_preflight_cannot_spawn(self) -> None:
        contract = self.skill["execute_contract"]
        self.assertEqual(contract["grammar"], "orchestrate execute <dispatch.json>")
        self.assertEqual(contract["verb"], "execute")
        self.assertEqual(contract["argument_count"], 1)
        self.assertEqual(contract["preflight_spawn_attempt_count"], 0)

    def test_codex_host_requires_native_operations_and_forbids_cli_fallback(self) -> None:
        self.assertEqual(self.host["availability_authority"], "active-host-tool-catalog")
        self.assertEqual(self.host["missing_operation_behavior"], "block")
        self.assertEqual(self.host["nested_model_cli_fallback"], "forbidden")
        self.assertEqual(len(self.host["required_execute_operations"]), 4)

    def test_invalid_dispatch_blocks_without_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            actual = evaluate_preflight(
                COMPILE_FIXTURES / "invalid-dispatch.json",
                "preflight-invalid",
                self.available,
                Path(temp_dir) / "run",
            )
            self.assert_receipt(actual, "expected-invalid.json")
            self.assertFalse((Path(temp_dir) / "run").exists())

    def test_authorization_pending_blocks_without_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dispatch = copy.deepcopy(load_json(COMPILE_FIXTURES / "valid-two-wave.json"))
            dispatch["subagent_strategy"]["authorization"] = "requires_user_permission"
            dispatch_path = root / "authorization-pending.json"
            shutil.copyfile(
                COMPILE_FIXTURES / "confirmed-briefings.json",
                root / "confirmed-briefings.json",
            )
            dispatch_path.write_text(json.dumps(dispatch, indent=2) + "\n", encoding="utf-8")
            actual = evaluate_preflight(dispatch_path, "preflight-auth", self.available, root / "run")
            self.assert_receipt(actual, "expected-authorization-pending.json")
            self.assertFalse((root / "run").exists())

    def test_missing_host_operation_blocks_without_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            available = self.available - {"collaboration.spawn_agent"}
            actual = evaluate_preflight(
                COMPILE_FIXTURES / "valid-two-wave.json",
                "preflight-missing-host",
                available,
                Path(temp_dir) / "run",
            )
            self.assert_receipt(actual, "expected-missing-host-operation.json")
            self.assertFalse((Path(temp_dir) / "run").exists())

    def test_ready_preflight_reaches_wave_ready_without_spawning(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            actual = evaluate_preflight(
                COMPILE_FIXTURES / "valid-two-wave.json",
                "preflight-ready",
                self.available,
                output,
            )
            self.assert_receipt(actual, "expected-ready.json")
            self.assertTrue((output / "run-plan.json").is_file())
            self.assertEqual(len(list((output / "actions").glob("*.json"))), 3)


if __name__ == "__main__":
    unittest.main()

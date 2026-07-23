#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


ARCanum_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ARCanum_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures/compile"
SCHEMAS = ARCanum_ROOT / "runtime/orchestrate/schemas"
VALIDATOR = ARCanum_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {SCRIPT}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def directory_snapshot(path: Path) -> dict[str, bytes]:
    return {
        str(candidate.relative_to(path)): candidate.read_bytes()
        for candidate in sorted(path.rglob("*"))
        if candidate.is_file()
    }


class CompileFirstWaveTests(unittest.TestCase):
    def test_valid_fixture_passes_canonical_validator(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / "valid-two-wave.json"), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(load_json_from_text(completed.stdout), {"validation": "pass", "blocks": [], "flags": []})

    def test_compile_preserves_declared_role_order_and_agent_cardinality(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            result = coordinator.compile_to_directory(
                FIXTURES / "valid-two-wave.json", "run-fixture-001", output, VALIDATOR
            )

            actions = result["run_plan"]["actions"]
            self.assertEqual([action["role"] for action in actions], ["beta-check", "beta-check", "alpha-check"])
            self.assertEqual([action["agent_ordinal"] for action in actions], [0, 1, 0])
            self.assertEqual([action["action_id"] for action in actions], ["spawn-0001", "spawn-0002", "spawn-0003"])
            self.assertEqual({action["wave_id"] for action in actions}, {"checks"})
            self.assertNotIn("artifact-writer", {action["role"] for action in actions})
            self.assertEqual(result["run_plan"], load_json(FIXTURES / "expected-run-plan.json"))
            self.assertEqual(result["state"], load_json(FIXTURES / "expected-state.json"))

    def test_outputs_validate_against_runtime_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            coordinator.compile_to_directory(FIXTURES / "valid-two-wave.json", "run-schema-001", output, VALIDATOR)

            action_schema = load_json(SCHEMAS / "action.schema.json")
            state_schema = load_json(SCHEMAS / "state.schema.json")
            run_plan_schema = load_json(SCHEMAS / "run-plan.schema.json")
            resolver = RefResolver.from_schema(
                run_plan_schema,
                store={
                    action_schema["$id"]: action_schema,
                    "action.schema.json": action_schema,
                },
            )

            Draft202012Validator(state_schema).validate(load_json(output / "state.json"))
            Draft202012Validator(run_plan_schema, resolver=resolver).validate(load_json(output / "run-plan.json"))
            for action_file in sorted((output / "actions").glob("*.json")):
                Draft202012Validator(action_schema).validate(load_json(action_file))

    def test_invalid_dispatch_emits_validation_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            with self.assertRaises(coordinator.CompileBlocked):
                coordinator.compile_to_directory(
                    FIXTURES / "invalid-dispatch.json", "run-invalid-001", output, VALIDATOR
                )

            self.assertEqual(load_json(output / "validation.json")["validation"], "block")
            self.assertFalse((output / "state.json").exists())
            self.assertFalse((output / "run-plan.json").exists())
            self.assertFalse((output / "actions").exists())

    def test_output_is_byte_stable_for_same_dispatch_and_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first"
            second = root / "second"
            coordinator.compile_to_directory(FIXTURES / "valid-two-wave.json", "run-repeat-001", first, VALIDATOR)
            coordinator.compile_to_directory(FIXTURES / "valid-two-wave.json", "run-repeat-001", second, VALIDATOR)
            self.assertEqual(directory_snapshot(first), directory_snapshot(second))


def load_json_from_text(value: str):
    return json.loads(value)


if __name__ == "__main__":
    unittest.main()

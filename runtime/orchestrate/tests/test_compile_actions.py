#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


ARCanum_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ARCanum_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
DRIVER = ARCanum_ROOT / "runtime/orchestrate/scripts/native_dispatch_driver.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures/compile"
PROJECT_ROOT = FIXTURES / "project-root"
SCHEMAS = ARCanum_ROOT / "runtime/orchestrate/schemas"
VALIDATOR = ARCanum_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {SCRIPT}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)

DRIVER_SPEC = importlib.util.spec_from_file_location("native_dispatch_driver_compile_test", DRIVER)
if DRIVER_SPEC is None or DRIVER_SPEC.loader is None:
    raise RuntimeError(f"cannot import driver: {DRIVER}")
driver = importlib.util.module_from_spec(DRIVER_SPEC)
DRIVER_SPEC.loader.exec_module(driver)


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
                FIXTURES / "valid-two-wave.json", "run-fixture-001", output, VALIDATOR, PROJECT_ROOT
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
            coordinator.compile_to_directory(
                FIXTURES / "valid-two-wave.json", "run-schema-001", output, VALIDATOR, PROJECT_ROOT
            )

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
                    FIXTURES / "invalid-dispatch.json", "run-invalid-001", output, VALIDATOR, PROJECT_ROOT
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
            coordinator.compile_to_directory(
                FIXTURES / "valid-two-wave.json", "run-repeat-001", first, VALIDATOR, PROJECT_ROOT
            )
            coordinator.compile_to_directory(
                FIXTURES / "valid-two-wave.json", "run-repeat-001", second, VALIDATOR, PROJECT_ROOT
            )
            self.assertEqual(directory_snapshot(first), directory_snapshot(second))

    def test_confirmed_role_briefing_survives_dispatch_compile_and_host_projection(self) -> None:
        dispatch = load_json(FIXTURES / "valid-two-wave.json")
        role_by_id = {
            role["role_id"]: role for role in dispatch["subagent_strategy"]["roles"]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "compiled"
            result = coordinator.compile_to_directory(
                FIXTURES / "valid-two-wave.json", "run-briefing-fidelity", output, VALIDATOR, PROJECT_ROOT
            )
            role_digests: dict[str, str] = {}
            for action in result["run_plan"]["actions"]:
                expected_agent = role_by_id[action["role"]]["agents"][action["agent_ordinal"]]
                expected = expected_agent["briefing_binding"]
                self.assertEqual(action["briefing_binding"], expected)
                role_digests[action["agent_name"]] = action["briefing_binding"]["briefing_sha256"]
                request = driver._spawn_request(action)
                self.assertEqual(request["briefing_binding"], expected)
                self.assertEqual(request["message"], expected_agent["initial_prompt"])
            self.assertEqual(len(set(role_digests.values())), 3)

            dependent = coordinator._compile_named_wave_actions(
                dispatch, "run-briefing-fidelity", "artifact", 4
            )
            self.assertEqual(
                dependent[0]["briefing_binding"],
                role_by_id["artifact-writer"]["agents"][0]["briefing_binding"],
            )
            self.assertNotIn(
                dependent[0]["briefing_binding"]["briefing_sha256"],
                set(role_digests.values()),
            )

            action = copy.deepcopy(result["run_plan"]["actions"][0])
            action["briefing_binding"]["briefing"]["instructions"] = "mutated after compile"
            run_plan = copy.deepcopy(result["run_plan"])
            run_plan["actions"][0] = action
            action_path = root / "mutated" / "actions" / "spawn-0001.json"
            plan_path = root / "mutated" / "run-plan.json"
            action_path.parent.mkdir(parents=True)
            action_path.write_text(json.dumps(action, indent=2) + "\n", encoding="utf-8")
            plan_path.write_text(json.dumps(run_plan, indent=2) + "\n", encoding="utf-8")
            events = root / "mutated" / "events.jsonl"
            request_path = root / "mutated" / "request.json"
            with self.assertRaises(driver.DriverBlocked):
                driver.prepare_spawn(action_path, plan_path, events, request_path, None)
            self.assertFalse(events.exists())
            self.assertFalse(request_path.exists())

    def test_named_role_blocks_when_briefing_identity_differs(self) -> None:
        dispatch = load_json(FIXTURES / "valid-two-wave.json")
        role = copy.deepcopy(dispatch["subagent_strategy"]["roles"][0])
        role["agents"][0]["briefing_binding"]["briefing"]["agent_identity"] = "Hewitt, Carl"
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator._validated_agent_binding(role, role["role_id"], 0)
        self.assertIn("role briefing agent identity does not match agent_name", raised.exception.blockers[0])

    def test_host_projection_blocks_when_confirmed_prompt_body_differs(self) -> None:
        dispatch = load_json(FIXTURES / "valid-two-wave.json")
        role = dispatch["subagent_strategy"]["roles"][0]
        _, _, binding = coordinator._validated_agent_binding(role, role["role_id"], 0)
        action = {
            "agent_name": role["agents"][0]["agent_name"],
            "initial_prompt": "You are Abramsky, Samson.\n\nDifferent instructions.",
            "briefing_binding": binding,
            "input_refs": role["input_refs"],
            "mutation_policy": role["mutation_policy"],
            "write_scope": role["write_scope"],
            "forbidden_write_scopes": role["forbidden_write_scopes"],
        }
        with self.assertRaises(driver.DriverBlocked) as raised:
            driver._validated_action_briefing(action)
        self.assertIn(
            "persisted action briefing instructions do not match initial_prompt",
            raised.exception.blockers,
        )


def load_json_from_text(value: str):
    return json.loads(value)


if __name__ == "__main__":
    unittest.main()

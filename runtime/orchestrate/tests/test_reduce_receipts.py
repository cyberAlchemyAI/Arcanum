#!/usr/bin/env python3

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
COMPILE_FIXTURES = Path(__file__).resolve().parent / "fixtures/compile"
REDUCE_FIXTURES = Path(__file__).resolve().parent / "fixtures/reduce"
SCHEMAS = ARCANUM_ROOT / "runtime/orchestrate/schemas"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_reduce", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {SCRIPT}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def pass_receipts():
    return [load_json(path) for path in sorted((REDUCE_FIXTURES / "pass").glob("*.json"))]


def pass_receipt_for_action(action):
    return {
        "schema_version": coordinator.RECEIPT_SCHEMA_VERSION,
        "action_id": action["action_id"],
        "dispatch_id": action["dispatch_id"],
        "run_id": action["run_id"],
        "wave_id": action["wave_id"],
        "step_id": action["step_id"],
        "role": action["role"],
        "capability_ref": action["capability_ref"],
        "agent_id": f"native-agent-{action['action_id']}",
        "status": "pass",
        "artifacts": [],
        "validation": "pass",
        "blockers": [],
        "started_at": "2026-07-22T15:00:00Z",
        "finished_at": "2026-07-22T15:00:01Z",
    }


def bind_test_briefing(role):
    instructions = "Read the declared inputs and return the complete bounded review receipt."
    role["agents"] = []
    for ordinal in range(role["agent_count"]):
        agent_name = f"{role['role_id']}-{ordinal + 1}"
        briefing = {
            "agent_identity": agent_name,
            "angle": "Exercise run-global allocation without widening authority.",
            "instructions": instructions,
            "status_semantics": {
                "task_status_field": "task_status",
                "task_complete_value": "completed",
                "task_blocked_value": "blocked",
                "domain_gate_status_field": "domain_gate_status",
                "domain_gate_is_separate": True,
            },
            "read_policy": {
                "input_refs": list(role.get("input_refs", []) or []),
                "allowed_read_scopes": ["tmp/native-dispatch/"],
                "forbidden_read_scopes": [],
                "required_input_refs_readable": True,
            },
            "write_policy": {
                "mutation_policy": role["mutation_policy"],
                "write_scope": list(role.get("write_scope", []) or []),
                "forbidden_write_scopes": list(role.get("forbidden_write_scopes", []) or []),
            },
            "receipt_shape": {
                "required_fields": ["task_status", "domain_gate_status", "findings"],
                "completion_requires_all_fields": True,
            },
            "authority_ceiling": {
                "summary": "Review only the declared frontier.",
                "allowed_actions": ["read_declared_inputs"],
                "forbidden_actions": ["write", "promotion"],
            },
        }
        digest = hashlib.sha256(
            json.dumps(briefing, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        role["agents"].append(
            {
                "agent_name": agent_name,
                "initial_prompt": f"You are {agent_name}.\n\n{instructions}",
                "briefing_binding": {
                    "contract_version": "arcanum.confirmed-role-briefing.v0.1",
                    "source_binding": {
                        "artifact_path": "test-only.json",
                        "artifact_sha256": "0" * 64,
                        "selector": f"/briefings/{ordinal}",
                        "selected_payload_sha256": digest,
                    },
                    "briefing": briefing,
                    "briefing_sha256": digest,
                },
            }
        )


def run_plan_for_wave(dispatch, state, actions):
    wave_id = state["selected_wave_id"]
    wave = next(
        candidate
        for candidate in dispatch["subagent_strategy"]["execution_waves"]
        if candidate["wave_id"] == wave_id
    )
    return {
        "schema_version": coordinator.RUN_PLAN_SCHEMA_VERSION,
        "dispatch_id": dispatch["dispatch_id"],
        "run_id": state["run_id"],
        "state": "wave_ready",
        "validation_status": "pass",
        "selected_wave": wave,
        "action_artifacts": [f"actions/{action['action_id']}.json" for action in actions],
        "actions": actions,
    }


def inputs():
    return (
        load_json(COMPILE_FIXTURES / "valid-two-wave.json"),
        load_json(COMPILE_FIXTURES / "expected-state.json"),
        load_json(COMPILE_FIXTURES / "expected-run-plan.json"),
    )


def snapshot(path: Path) -> dict[str, bytes]:
    return {
        str(candidate.relative_to(path)): candidate.read_bytes()
        for candidate in sorted(path.rglob("*"))
        if candidate.is_file()
    }


class ReduceWaveReceiptsTests(unittest.TestCase):
    def test_all_pass_receipts_open_next_wave_exactly(self) -> None:
        dispatch, state, run_plan = inputs()
        next_state, gate, action_set = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        self.assertEqual(gate, load_json(REDUCE_FIXTURES / "expected-pass-gate.json"))
        self.assertEqual(next_state, load_json(REDUCE_FIXTURES / "expected-pass-state.json"))
        self.assertEqual(action_set, load_json(REDUCE_FIXTURES / "expected-pass-actions.json"))

    def test_nonpass_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = pass_receipts()
        receipts[1]["status"] = "block"
        receipts[1]["validation"] = "block"
        receipts[1]["blockers"] = ["deterministic failure"]
        next_state, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate, load_json(REDUCE_FIXTURES / "expected-block-gate.json"))
        self.assertEqual(next_state, load_json(REDUCE_FIXTURES / "expected-block-state.json"))
        self.assertEqual(action_set, load_json(REDUCE_FIXTURES / "expected-block-actions.json"))

    def test_missing_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = [receipt for receipt in pass_receipts() if receipt["action_id"] != "spawn-0002"]
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertIn("missing receipt for action 'spawn-0002'", gate["blockers"])
        self.assertEqual(action_set["actions"], [])

    def test_identity_mismatch_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = copy.deepcopy(pass_receipts())
        receipts[2]["capability_ref"] = "wrong-capability"
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertTrue(any("capability_ref" in blocker for blocker in gate["blockers"]))
        self.assertEqual(action_set["actions"], [])

    def test_state_and_run_plan_eligible_actions_must_match(self) -> None:
        dispatch, state, run_plan = inputs()
        state["eligible_action_ids"] = ["spawn-0001", "spawn-0002"]
        with self.assertRaisesRegex(
            coordinator.CompileBlocked, "state/run-plan eligible action mismatch"
        ):
            coordinator.reduce_wave_receipts(dispatch, state, run_plan, pass_receipts())

    def test_unknown_or_duplicate_completed_wave_history_blocks(self) -> None:
        dispatch, state, run_plan = inputs()
        for completed_wave_ids, expected_blocker in (
            (["unknown-wave"], "unknown completed wave identifier"),
            (["checks"], "duplicate completed wave identifier"),
        ):
            with self.subTest(completed_wave_ids=completed_wave_ids):
                candidate_state = copy.deepcopy(state)
                candidate_state["completed_wave_ids"] = completed_wave_ids
                with self.assertRaisesRegex(
                    coordinator.CompileBlocked, expected_blocker
                ):
                    coordinator.reduce_wave_receipts(
                        dispatch, candidate_state, run_plan, pass_receipts()
                    )

    def test_action_ids_are_run_global_across_three_waves(self) -> None:
        dispatch, state, run_plan = inputs()
        expected = load_json(REDUCE_FIXTURES / "run-global-action-ids.json")
        dispatch = copy.deepcopy(dispatch)
        final_reviewer = {
                "role_id": "final-reviewer",
                "capability_ref": "sigil-development",
                "capability_target": "final-review",
                "capability_mode": "review",
                "agent_count": 3,
                "mutation_policy": "read-only",
                "write_scope": [],
                "forbidden_write_scopes": ["arcana/", "spells/"],
                "depends_on_roles": ["artifact-writer"],
                "input_refs": ["tmp/native-dispatch/receipts/artifact.json"],
                "output_refs": [],
                "applies_to_steps": ["s-final-review"],
            }
        bind_test_briefing(final_reviewer)
        dispatch["subagent_strategy"]["roles"].append(final_reviewer)
        dispatch["subagent_strategy"]["execution_waves"].append(
            {
                "wave_id": "final-review",
                "role_ids": ["final-reviewer"],
                "parallel": True,
                "join_policy": "all",
                "depends_on_waves": ["artifact"],
                "on_incomplete": "block",
            }
        )
        dispatch["subagent_strategy"]["execution_waves"][1]["gate_after"] = (
            "g-artifact"
        )

        artifact_state, artifact_gate, artifact_actions = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        self.assertEqual(
            [action["action_id"] for action in artifact_actions["actions"]],
            expected["second_wave_action_ids"],
        )

        artifact_run_plan = coordinator.build_next_wave_plan(
            dispatch,
            run_plan,
            artifact_gate,
            artifact_actions,
            artifact_state,
            artifact_actions["actions"],
        )
        reviewer_state, gate, reviewer_actions = coordinator.reduce_wave_receipts(
            dispatch,
            artifact_state,
            artifact_run_plan,
            [pass_receipt_for_action(artifact_actions["actions"][0])],
        )
        reviewer_run_plan = coordinator.build_next_wave_plan(
            dispatch,
            artifact_run_plan,
            gate,
            reviewer_actions,
            reviewer_state,
            reviewer_actions["actions"],
        )

        self.assertEqual(gate["decision"], "gate_pass")
        self.assertEqual(
            [action["action_id"] for action in reviewer_actions["actions"]],
            expected["third_wave_action_ids"],
        )
        self.assertEqual(
            len(
                {
                    *expected["first_wave_action_ids"],
                    *artifact_state["eligible_action_ids"],
                    *gate["next_action_ids"],
                }
            ),
            7,
        )
        self.assertEqual(
            reviewer_run_plan["selected_wave"]["depends_on_waves"],
            ["artifact"],
        )
        self.assertEqual(
            reviewer_run_plan["actions"], reviewer_actions["actions"]
        )

    def test_next_wave_builder_emits_schema_valid_dependent_plan(self) -> None:
        dispatch, state, run_plan = inputs()
        next_state, gate, action_set = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        next_plan = coordinator.build_next_wave_plan(
            dispatch,
            run_plan,
            gate,
            action_set,
            next_state,
            action_set["actions"],
        )
        action_schema = load_json(SCHEMAS / "action.schema.json")
        run_plan_schema = load_json(SCHEMAS / "run-plan.schema.json")
        resolver = RefResolver.from_schema(
            run_plan_schema,
            store={
                action_schema["$id"]: action_schema,
                "action.schema.json": action_schema,
            },
        )
        Draft202012Validator(run_plan_schema, resolver=resolver).validate(next_plan)
        self.assertEqual(next_plan["selected_wave"]["wave_id"], "artifact")
        self.assertEqual(
            next_plan["selected_wave"]["depends_on_waves"], ["checks"]
        )
        self.assertEqual(next_plan["actions"], action_set["actions"])

    def test_run_global_allocator_blocks_out_of_range_and_legacy_reset_ids(self) -> None:
        for value in (0, coordinator.MAX_ACTION_NUMBER + 1):
            with self.subTest(value=value), self.assertRaisesRegex(
                coordinator.CompileBlocked, "exceeds supported range"
            ):
                coordinator._format_action_id(value)

        dispatch, state, run_plan = inputs()
        next_state, _, next_actions = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        legacy_plan = run_plan_for_wave(dispatch, next_state, next_actions["actions"])
        legacy_plan["actions"][0]["action_id"] = "spawn-0001"
        legacy_plan["action_artifacts"] = ["actions/spawn-0001.json"]
        next_state["eligible_action_ids"] = ["spawn-0001"]
        with self.assertRaisesRegex(
            coordinator.CompileBlocked,
            "run-plan action identifiers do not match run-global allocation",
        ):
            coordinator.reduce_wave_receipts(
                dispatch,
                next_state,
                legacy_plan,
                [pass_receipt_for_action(legacy_plan["actions"][0])],
            )

    def test_malformed_receipt_blocks_and_emits_no_actions(self) -> None:
        dispatch, state, run_plan = inputs()
        receipts = copy.deepcopy(pass_receipts())
        del receipts[0]["agent_id"]
        _, gate, action_set = coordinator.reduce_wave_receipts(dispatch, state, run_plan, receipts)
        self.assertEqual(gate["decision"], "gate_block")
        self.assertIn("receipt[0]: missing required field 'agent_id'", gate["blockers"])
        self.assertEqual(action_set["actions"], [])

    def test_reduction_is_byte_stable_for_same_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first"
            second = root / "second"
            args = (
                COMPILE_FIXTURES / "valid-two-wave.json",
                COMPILE_FIXTURES / "expected-state.json",
                COMPILE_FIXTURES / "expected-run-plan.json",
                REDUCE_FIXTURES / "pass",
            )
            coordinator.reduce_to_directory(*args, first)
            coordinator.reduce_to_directory(*args, second)
            self.assertEqual(snapshot(first), snapshot(second))

    def test_receipts_and_outputs_validate_against_runtime_schemas(self) -> None:
        dispatch, state, run_plan = inputs()
        next_state, gate, action_set = coordinator.reduce_wave_receipts(
            dispatch, state, run_plan, pass_receipts()
        )
        action_schema = load_json(SCHEMAS / "action.schema.json")
        receipt_schema = load_json(SCHEMAS / "receipt.schema.json")
        state_schema = load_json(SCHEMAS / "state.schema.json")
        gate_schema = load_json(SCHEMAS / "gate-decision.schema.json")
        action_set_schema = load_json(SCHEMAS / "action-set.schema.json")
        resolver = RefResolver.from_schema(
            action_set_schema,
            store={action_schema["$id"]: action_schema, "action.schema.json": action_schema},
        )
        for receipt in pass_receipts():
            Draft202012Validator(receipt_schema).validate(receipt)
        Draft202012Validator(state_schema).validate(next_state)
        Draft202012Validator(gate_schema).validate(gate)
        Draft202012Validator(action_set_schema, resolver=resolver).validate(action_set)


if __name__ == "__main__":
    unittest.main()

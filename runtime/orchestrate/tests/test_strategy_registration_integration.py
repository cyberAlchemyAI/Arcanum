#!/usr/bin/env python3

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
VALIDATOR = ARCANUM_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"
APPENDER = ARCANUM_ROOT / "arcana/subagent-strategy/scripts/append-dispatch.cjs"
COMPILE_FIXTURES = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator", COORDINATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {COORDINATOR_PATH}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


class StrategyRegistrationIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp.name)
        self.runtime_root = self.project_root / ".arcanum/runtime/subagents-strategy"
        self.runtime_root.mkdir(parents=True)
        self.sheet = self.runtime_root / "2026-08-26-example-review.tmp.json"
        self.close = self.runtime_root / "2026-08-26-example-review.close.tmp.json"
        self.dispatch = self.project_root / "runtime-dispatch.json"
        shutil.copyfile(
            COMPILE_FIXTURES / "confirmed-briefings.json",
            self.project_root / "confirmed-briefings.json",
        )
        runtime_dispatch = copy.deepcopy(
            load_json(COMPILE_FIXTURES / "valid-two-wave.json")
        )
        runtime_dispatch["dispatch_id"] = "2026-08-26-example-review"
        projection_sha = coordinator.strategy_execution_projection_sha256(runtime_dispatch)
        write_json(
            self.sheet,
            {
                "dispatch_id": "2026-08-26-example-review",
                "schema_version": "0.7.0",
                "dispatch_type": "review",
                "goal": "Exercise registered native strategy binding.",
                "context": "A synthetic integration sheet whose topology matches the executable runtime waves.",
                "max_loops": 1,
                "final_approver": "parent",
                "anti_bias_global": "independent checks versus dependent artifact",
                "output_mode": "inline",
                "execution_projection_sha256": projection_sha,
                "groups": [
                    {
                        "group_id": "checks",
                        "n": 3,
                        "anti_bias": "independent check angle",
                        "predicted_disagreements": [
                            {"between": [0, 1], "question": "Which check controls the gate?"},
                            {"between": [0, 2], "question": "Can the third check overturn the first?"},
                            {"between": [1, 2], "question": "Can the third check overturn the second?"},
                        ],
                        "agents": [
                            {"agent_name": "Abramsky, Samson", "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "beta", "initial_prompt": "You are Abramsky, Samson.\n\nRun beta check."},
                            {"agent_name": "Hewitt, Carl", "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "beta peer", "initial_prompt": "You are Hewitt, Carl.\n\nRun beta peer check."},
                            {"agent_name": "Peirce, Charles Sanders", "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "alpha", "initial_prompt": "You are Peirce, Charles Sanders.\n\nRun alpha check."},
                        ],
                    },
                    {
                        "group_id": "artifact",
                        "agents": [
                            {"agent_name": "Shannon, Claude", "role": "writer", "model": "gpt-5.6-sol", "token_budget": 800, "initial_prompt": "You are Shannon, Claude.\n\nWrite the dependent artifact."}
                        ],
                    },
                ],
                "connections": [{"from": "checks", "to": "artifact", "type": "sequential"}],
            },
        )
        self.sheet_sha = hashlib.sha256(self.sheet.read_bytes()).hexdigest()
        runtime_dispatch["subagent_strategy"]["registration"] = {
            "schema_version": "arcanum.subagent-strategy-registration.v0.3",
            "ledger": ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml",
            "sheet_schema_version": "0.7.0",
            "sheet_sha256": self.sheet_sha,
            "execution_projection_sha256": projection_sha,
            "temporary_sheet": ".arcanum/runtime/subagents-strategy/2026-08-26-example-review.tmp.json",
            "temporary_close": ".arcanum/runtime/subagents-strategy/2026-08-26-example-review.close.tmp.json",
        }
        write_json(self.dispatch, runtime_dispatch)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def appender(self, record: Path) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["ARCANUM_PROJECT_DIR"] = str(self.project_root)
        return subprocess.run(
            ["node", str(APPENDER), "--consume", str(record)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def test_register_consume_compile_close_consume_verify(self) -> None:
        registered = self.appender(self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        self.assertFalse(self.sheet.exists())

        output = self.project_root / "run"
        compiled = coordinator.compile_to_directory(
            self.dispatch,
            "strategy-registration-integration",
            output,
            VALIDATOR,
            self.project_root,
        )
        self.assertEqual(compiled["status"], "pass")
        registration = load_json(output / "strategy-registration.json")
        self.assertTrue(registration["dispatch_registered"])
        self.assertFalse(registration["close_registered"])
        self.assertTrue(registration["temporary_sheet_consumed"])

        write_json(
            self.close,
            {
                "close_of": "2026-08-26-example-review",
                "exit_reason": "resolved",
                "agents_spawned": {
                    "planned_total": 4,
                    "total": 4,
                    "not_launched": 0,
                    "tree": {"explorer": 3, "writer": 1, "helpers": 0},
                    "loops_used": 0,
                },
                "feedback_prompts": [],
                "invoked_by": "runtime-integration@example.invalid",
            },
        )
        closed = self.appender(self.close)
        self.assertEqual(closed.returncode, 0, closed.stderr)
        self.assertFalse(self.close.exists())

        receipt = coordinator.verify_strategy_registration(
            load_json(self.dispatch),
            self.dispatch,
            self.project_root,
            require_close=True,
        )
        self.assertTrue(receipt["dispatch_registered"])
        self.assertTrue(receipt["close_registered"])
        self.assertTrue(receipt["temporary_close_consumed"])
        cli = subprocess.run(
            [
                sys.executable,
                str(COORDINATOR_PATH),
                "verify-close",
                str(self.dispatch),
                "--project-root",
                str(self.project_root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(cli.returncode, 0, cli.stdout + cli.stderr)
        self.assertTrue(json.loads(cli.stdout)["close_registered"])

    def test_compile_blocks_before_registration_and_preserves_sheet(self) -> None:
        output = self.project_root / "run"
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.compile_to_directory(
                self.dispatch,
                "strategy-registration-missing",
                output,
                VALIDATOR,
                self.project_root,
            )
        self.assertIn(
            "confirmed strategy sheet was not consumed before preflight",
            raised.exception.blockers,
        )
        self.assertTrue(self.sheet.exists())
        self.assertFalse((output / "run-plan.json").exists())

    def test_registered_digest_mismatch_blocks_without_actions(self) -> None:
        registered = self.appender(self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        runtime_dispatch = load_json(self.dispatch)
        runtime_dispatch["subagent_strategy"]["registration"]["sheet_sha256"] = "0" * 64
        write_json(self.dispatch, runtime_dispatch)
        output = self.project_root / "run"
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.compile_to_directory(
                self.dispatch,
                "strategy-registration-digest-mismatch",
                output,
                VALIDATOR,
                self.project_root,
            )
        self.assertIn("registered strategy sheet digest mismatch", raised.exception.blockers)
        self.assertFalse((output / "run-plan.json").exists())

    def test_execution_projection_change_blocks_without_actions(self) -> None:
        registered = self.appender(self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        runtime_dispatch = load_json(self.dispatch)
        runtime_dispatch["subagent_strategy"]["execution_owner"] = "different-owner"
        write_json(self.dispatch, runtime_dispatch)
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.compile_to_directory(
                self.dispatch,
                "strategy-projection-mismatch",
                self.project_root / "run",
                VALIDATOR,
                self.project_root,
            )
        self.assertIn(
            "strategy registration execution projection digest mismatch",
            raised.exception.blockers,
        )

    def test_registered_topology_mismatch_blocks_without_actions(self) -> None:
        registered = self.appender(self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        ledger = self.project_root / ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml"
        text = ledger.read_text(encoding="utf-8")
        text = text.replace('"group_id":"checks","n":3', '"group_id":"renamed-checks","n":3')
        ledger.write_text(text, encoding="utf-8")
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.compile_to_directory(
                self.dispatch,
                "strategy-topology-mismatch",
                self.project_root / "run",
                VALIDATOR,
                self.project_root,
            )
        self.assertIn(
            "registered strategy topology does not match executable runtime waves",
            raised.exception.blockers,
        )

    def test_registered_initial_prompt_mismatch_blocks_without_actions(self) -> None:
        registered = self.appender(self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        ledger = self.project_root / ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml"
        text = ledger.read_text(encoding="utf-8")
        text = text.replace("Run beta check.", "Run a different beta check.")
        ledger.write_text(text, encoding="utf-8")
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.compile_to_directory(
                self.dispatch,
                "strategy-prompt-mismatch",
                self.project_root / "run",
                VALIDATOR,
                self.project_root,
            )
        self.assertIn(
            "registered strategy topology does not match executable runtime waves",
            raised.exception.blockers,
        )

    def test_briefing_artifact_digest_is_equal_for_lf_and_crlf(self) -> None:
        source = self.project_root / "confirmed-briefings.json"
        lf = source.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        source.write_bytes(lf.replace(b"\n", b"\r\n"))
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(self.dispatch), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()

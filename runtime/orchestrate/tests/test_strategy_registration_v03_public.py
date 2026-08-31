#!/usr/bin/env python3

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
VALIDATOR = ARCANUM_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"
RUNTIME = ARCANUM_ROOT / "arcana/subagent-strategy/scripts/strategy-runtime.cjs"
PUBLIC_PROFILE = ARCANUM_ROOT / "arcana/subagent-strategy/profiles/arcanum.json"
FIXTURES = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_v03_public", COORDINATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {COORDINATOR_PATH}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def exact_ref(root: Path, path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size": len(payload),
    }


class PublicStrategyRegistrationV03Tests(unittest.TestCase):
    dispatch_id = "public-v03-example"

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime_root = self.root / ".arcanum/runtime/subagents-strategy"
        self.runtime_root.mkdir(parents=True)
        self.sheet = self.runtime_root / f"{self.dispatch_id}.tmp.json"
        self.close = self.runtime_root / f"{self.dispatch_id}.close.tmp.json"
        self.dispatch_path = self.root / "canonical.dispatch.json"
        self.entry_path = self.root / "runtime/execution-entry.json"
        self.profile_path = self.root / "profiles/arcanum.json"
        self.profile_path.parent.mkdir(parents=True)
        shutil.copyfile(PUBLIC_PROFILE, self.profile_path)
        shutil.copyfile(FIXTURES / "confirmed-briefings.json", self.root / "confirmed-briefings.json")

        profile_ref = exact_ref(self.root, self.profile_path)
        dispatch = copy.deepcopy(load_json(FIXTURES / "valid-two-wave.json"))
        dispatch["dispatch_id"] = self.dispatch_id
        strategy = dispatch["subagent_strategy"]
        strategy["authorization"] = "requires_user_permission"
        strategy.pop("registration", None)
        strategy["registration_intent"] = {
            "schema_version": "arcanum.subagent-strategy-registration-intent.v0.1",
            "profile_id": "arcanum.subagent-strategy.public.v1",
            "profile_ref": profile_ref,
            "confirmation_mode": "exact_sheet",
            "source_lifecycle": "consumed",
            "registration_schema_version": "arcanum.subagent-strategy-registration.v0.3",
        }
        write_json(self.dispatch_path, dispatch)

        approved = copy.deepcopy(dispatch)
        approved["subagent_strategy"]["authorization"] = "approved"
        projection_sha = coordinator.strategy_execution_projection_v03_sha256(approved)
        write_json(
            self.sheet,
            {
                "dispatch_id": self.dispatch_id,
                "schema_version": "0.6.1",
                "dispatch_type": "review",
                "goal": "Exercise exact-sheet public registration v0.3.",
                "context": "A synthetic public profile whose topology matches the executable waves.",
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
                            {"agent_name": None, "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "beta", "initial_prompt": "Run beta check."},
                            {"agent_name": None, "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "beta peer", "initial_prompt": "Run beta peer check."},
                            {"agent_name": None, "role": "explorer", "model": "gpt-5.6-sol", "token_budget": 800, "angle": "alpha", "initial_prompt": "Run alpha check."},
                        ],
                    },
                    {
                        "group_id": "artifact",
                        "agents": [
                            {"agent_name": None, "role": "writer", "model": "gpt-5.6-sol", "token_budget": 800, "initial_prompt": "Write the dependent artifact."}
                        ],
                    },
                ],
                "connections": [{"from": "checks", "to": "artifact", "type": "sequential"}],
            },
        )
        source_ref = exact_ref(self.root, self.sheet)
        confirmation = {
            "mode": "exact_sheet",
            "handle": "CONFIRM PUBLIC V03 EXAMPLE",
            "binding_sha256": source_ref["sha256"],
            "material_equivalence_ref": None,
        }
        registration = {
            "schema_version": "arcanum.subagent-strategy-registration.v0.3",
            "profile_id": "arcanum.subagent-strategy.public.v1",
            "profile_ref": profile_ref,
            "ledger": ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml",
            "sheet_schema_version": "0.6.1",
            "source_sheet_ref": source_ref,
            "source_lifecycle": "consumed",
            "registration_envelope_ref": source_ref,
            "confirmation": confirmation,
            "admission_receipt_ref": None,
            "execution_projection_sha256": projection_sha,
            "temporary_close": self.close.relative_to(self.root).as_posix(),
        }
        write_json(
            self.entry_path,
            {
                "schema_version": "arcanum.subagent-strategy-execution-entry.v0.1",
                "canonical_dispatch_ref": exact_ref(self.root, self.dispatch_path),
                "authorization": "approved",
                "confirmation_handle": confirmation["handle"],
                "registration": registration,
            },
        )
        registered = self.runtime("register", self.sheet)
        self.assertEqual(registered.returncode, 0, registered.stdout + registered.stderr)
        self.assertFalse(self.sheet.exists())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def runtime(self, mode: str, record: Path) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["ARCANUM_PROJECT_DIR"] = str(self.root)
        return subprocess.run(
            ["node", str(RUNTIME), mode, str(record), "--profile", str(self.profile_path)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def close_record(self, path: Path | None = None) -> tuple[Path, str]:
        target = path or self.close
        write_json(
            target,
            {
                "close_of": self.dispatch_id,
                "exit_reason": "resolved",
                "agents_spawned": {
                    "total": 4,
                    "tree": {"explorer": 3, "writer": 1},
                    "loops_used": 0,
                },
                "feedback_prompts": [],
                "invoked_by": "public-v03-test@example.invalid",
            },
        )
        return target, hashlib.sha256(target.read_bytes()).hexdigest()

    def verify(self, *, require_close: bool = False):
        return coordinator.verify_strategy_registration_v03(
            load_json(self.dispatch_path),
            self.dispatch_path,
            self.entry_path,
            self.root,
            require_close=require_close,
        )

    def test_register_compile_close_and_verify_exact_close_digest(self) -> None:
        output = self.root / "run"
        result = coordinator.compile_to_directory(
            self.dispatch_path,
            "public-v03",
            output,
            VALIDATOR,
            self.root,
            self.entry_path,
        )
        self.assertEqual(result["status"], "pass")
        receipt = load_json(output / "strategy-registration.json")
        self.assertTrue(receipt["registration_envelope_consumed"])
        self.assertFalse(receipt["temporary_close_consumed"])

        close_path, close_sha = self.close_record()
        closed = self.runtime("close", close_path)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        self.assertFalse(close_path.exists())
        _, close_receipt = self.verify(require_close=True)
        self.assertEqual(
            close_receipt["temporary_close_ref"],
            {"path": self.close.relative_to(self.root).as_posix(), "sha256": close_sha},
        )

    def test_confirmation_or_source_digest_mutation_blocks(self) -> None:
        entry = load_json(self.entry_path)
        entry["registration"]["confirmation"]["binding_sha256"] = "f" * 64
        write_json(self.entry_path, entry)
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            self.verify()
        self.assertIn(
            "exact-sheet confirmation does not bind the source sheet digest",
            raised.exception.blockers,
        )

    def test_wrong_close_path_blocks(self) -> None:
        wrong = self.runtime_root / f"{self.dispatch_id}.wrong.close.tmp.json"
        self.close_record(wrong)
        closed = self.runtime("close", wrong)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            self.verify(require_close=True)
        self.assertIn(
            "strategy close row is not bound to the registered temporary close path",
            raised.exception.blockers,
        )

    def test_malformed_close_digest_blocks(self) -> None:
        close_path, close_sha = self.close_record()
        closed = self.runtime("close", close_path)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        ledger = self.root / ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml"
        ledger.write_text(
            ledger.read_text(encoding="utf-8").replace(close_sha, "not-a-sha256"),
            encoding="utf-8",
        )
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            self.verify(require_close=True)
        self.assertIn("strategy close row has no content digest", raised.exception.blockers)


if __name__ == "__main__":
    unittest.main()

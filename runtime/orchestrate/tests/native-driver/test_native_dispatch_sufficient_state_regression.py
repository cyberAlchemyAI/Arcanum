#!/usr/bin/env python3

from __future__ import annotations

import importlib
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from typing import Any


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
FROZEN_COMMIT = "f475b4af9926a159a411791629aa39fc598a83fc"
FROZEN_SCRIPTS = (
    "native_dispatch_coordinator.py",
    "validate_run_evidence.py",
    "native_dispatch_driver.py",
)
SCHEMA_VERSION = "arcanum.native-dispatch-runner.run-event.v0.1"
DISPATCH_ID = "fixture-native-dispatch-two-wave"
RUN_ID = "run-fixture-001"
WAVE_ID = "checks"
OPERATION = "collaboration.spawn_agent"

A = "spawn-0001"
B = "spawn-0002"


def git_bytes(object_name: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ARCANUM_ROOT), "show", object_name],
        check=True,
        capture_output=True,
    ).stdout


def raw_attempt(action_id: str) -> dict[str, Any]:
    return {
        "event": "action_attempted",
        "dispatch_id": DISPATCH_ID,
        "run_id": RUN_ID,
        "wave_id": WAVE_ID,
        "action_id": action_id,
        "agent_id": None,
        "operation": OPERATION,
        "depends_on_gate_id": None,
    }


def raw_return(action_id: str, agent_id: str = "agent-1") -> dict[str, Any]:
    return {
        "event": "host_spawn_returned",
        "dispatch_id": DISPATCH_ID,
        "run_id": RUN_ID,
        "wave_id": WAVE_ID,
        "action_id": action_id,
        "agent_id": agent_id,
        "operation": OPERATION,
    }


class FrozenNativeDispatchSufficientStateRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        resolved = subprocess.run(
            [
                "git",
                "-C",
                str(ARCANUM_ROOT),
                "rev-parse",
                "--verify",
                f"{FROZEN_COMMIT}^{{commit}}",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if resolved != FROZEN_COMMIT:
            raise AssertionError(f"frozen commit mismatch: {resolved}")

        cls._source_temp = tempfile.TemporaryDirectory()
        cls.frozen_script_dir = Path(cls._source_temp.name)
        for filename in FROZEN_SCRIPTS:
            object_name = (
                f"{FROZEN_COMMIT}:runtime/orchestrate/scripts/{filename}"
            )
            (cls.frozen_script_dir / filename).write_bytes(git_bytes(object_name))

        driver_source = (
            cls.frozen_script_dir / "native_dispatch_driver.py"
        ).read_text(encoding="utf-8")
        if "prospective = existing + prepared" not in driver_source:
            raise AssertionError("frozen driver lacks prospective prefix assembly")
        if (
            "prospective, str(stream), require_complete=False"
            not in driver_source
        ):
            raise AssertionError("frozen driver lacks prospective validator call")

        cls._prior_modules = {
            name: sys.modules.get(name)
            for name in (
                "fcntl",
                "native_dispatch_coordinator",
                "validate_run_evidence",
                "native_dispatch_driver",
            )
        }
        for name in (
            "native_dispatch_coordinator",
            "validate_run_evidence",
            "native_dispatch_driver",
        ):
            sys.modules.pop(name, None)
        try:
            importlib.import_module("fcntl")
            cls.runtime_adapter = "native-posix-fcntl"
        except ModuleNotFoundError:
            fcntl_adapter = types.ModuleType("fcntl")
            fcntl_adapter.LOCK_EX = 2
            fcntl_adapter.LOCK_UN = 8
            fcntl_adapter.flock = lambda _fd, _operation: None
            sys.modules["fcntl"] = fcntl_adapter
            cls.runtime_adapter = "single-process-noop-fcntl-adapter"
        sys.path.insert(0, str(cls.frozen_script_dir))
        cls.driver = importlib.import_module("native_dispatch_driver")
        cls.validator = importlib.import_module("validate_run_evidence")

    @classmethod
    def tearDownClass(cls) -> None:
        if str(cls.frozen_script_dir) in sys.path:
            sys.path.remove(str(cls.frozen_script_dir))
        for name, module in cls._prior_modules.items():
            sys.modules.pop(name, None)
            if module is not None:
                sys.modules[name] = module
        cls._source_temp.cleanup()

    def load_stream(self, stream: Path) -> list[dict[str, Any]]:
        return self.validator.load_events(stream) if stream.exists() else []

    def execute_call(
        self,
        fixture_id: str,
        call_number: int,
        stream: Path,
        raw_batch: list[dict[str, Any]],
    ) -> dict[str, Any]:
        self.assertTrue(raw_batch)
        for raw in raw_batch:
            self.assertNotIn("schema_version", raw)
            self.assertNotIn("sequence", raw)

        pre_stream = self.load_stream(stream)
        try:
            prepared = self.driver.append_causal_records(stream, raw_batch)
            outcome = "Append"
            blocker_codes: list[str] = []
        except self.driver.DriverBlocked as exc:
            prepared = []
            outcome = "Block"
            blocker_codes = [
                blocker.split("@", 1)[0] if "@" in blocker else blocker
                for blocker in exc.blockers
            ]
        post_stream = self.load_stream(stream)
        newly_persisted = post_stream[len(pre_stream) :]

        if outcome == "Append":
            self.assertEqual(prepared, newly_persisted)
        else:
            self.assertEqual(prepared, [])
            self.assertEqual(post_stream, pre_stream)

        for expected_sequence, event in enumerate(post_stream, start=1):
            self.assertEqual(event["schema_version"], SCHEMA_VERSION)
            self.assertEqual(event["sequence"], expected_sequence)

        return {
            "fixture_id": fixture_id,
            "call": call_number,
            "raw_batch": raw_batch,
            "pre_stream": pre_stream,
            "prepared_events_observed": newly_persisted,
            "post_stream": post_stream,
            "outcome": outcome,
            "blocker_codes": blocker_codes,
        }

    def run_fixture(
        self,
        root: Path,
        fixture_id: str,
        calls: list[list[dict[str, Any]]],
        expected: list[tuple[str, list[str]]],
    ) -> list[dict[str, Any]]:
        stream = root / fixture_id / "events.jsonl"
        evidence = [
            self.execute_call(fixture_id, ordinal, stream, raw_batch)
            for ordinal, raw_batch in enumerate(calls, start=1)
        ]
        self.assertEqual(
            [(item["outcome"], item["blocker_codes"]) for item in evidence],
            expected,
        )
        return evidence

    def test_frozen_runtime_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixtures = {
                "RT-01-matching-return": self.run_fixture(
                    root,
                    "RT-01-matching-return",
                    [[raw_attempt(A)], [raw_return(A)]],
                    [("Append", []), ("Append", [])],
                ),
                "RT-02-missing-attempt": self.run_fixture(
                    root,
                    "RT-02-missing-attempt",
                    [[raw_return(A)]],
                    [("Block", ["missing_action_attempt"])],
                ),
                "RT-03-duplicate-attempt": self.run_fixture(
                    root,
                    "RT-03-duplicate-attempt",
                    [[raw_attempt(A)], [raw_attempt(A)]],
                    [("Append", []), ("Block", ["duplicate_action_attempt"])],
                ),
                "RT-04-duplicate-return": self.run_fixture(
                    root,
                    "RT-04-duplicate-return",
                    [[raw_attempt(A)], [raw_return(A)], [raw_return(A)]],
                    [
                        ("Append", []),
                        ("Append", []),
                        ("Block", ["duplicate_host_result"]),
                    ],
                ),
                "RT-05-agent-one": self.run_fixture(
                    root,
                    "RT-05-agent-one",
                    [[raw_attempt(A)], [raw_return(A, "agent-1")]],
                    [("Append", []), ("Append", [])],
                ),
                "RT-05-agent-two": self.run_fixture(
                    root,
                    "RT-05-agent-two",
                    [[raw_attempt(A)], [raw_return(A, "agent-2")]],
                    [("Append", []), ("Append", [])],
                ),
                "RT-06-order-AB": self.run_fixture(
                    root,
                    "RT-06-order-AB",
                    [[raw_attempt(A)], [raw_attempt(B)], [raw_return(A)]],
                    [("Append", []), ("Append", []), ("Append", [])],
                ),
                "RT-06-order-BA": self.run_fixture(
                    root,
                    "RT-06-order-BA",
                    [[raw_attempt(B)], [raw_attempt(A)], [raw_return(A)]],
                    [("Append", []), ("Append", []), ("Append", [])],
                ),
                "RT-07-count-A": self.run_fixture(
                    root,
                    "RT-07-count-A",
                    [[raw_attempt(A)], [raw_return(A)]],
                    [("Append", []), ("Append", [])],
                ),
                "RT-07-count-B": self.run_fixture(
                    root,
                    "RT-07-count-B",
                    [[raw_attempt(B)], [raw_return(A)]],
                    [("Append", []), ("Block", ["missing_action_attempt"])],
                ),
            }

        self.assertEqual(
            fixtures["RT-05-agent-one"][-1]["outcome"],
            fixtures["RT-05-agent-two"][-1]["outcome"],
        )
        self.assertEqual(
            fixtures["RT-06-order-AB"][-1]["raw_batch"],
            fixtures["RT-06-order-BA"][-1]["raw_batch"],
        )
        self.assertEqual(
            fixtures["RT-06-order-AB"][-1]["outcome"],
            fixtures["RT-06-order-BA"][-1]["outcome"],
        )
        self.assertEqual(
            fixtures["RT-07-count-A"][-1]["raw_batch"],
            fixtures["RT-07-count-B"][-1]["raw_batch"],
        )
        self.assertNotEqual(
            fixtures["RT-07-count-A"][-1]["outcome"],
            fixtures["RT-07-count-B"][-1]["outcome"],
        )

        receipt = {
            "frozen_commit": FROZEN_COMMIT,
            "driver": "runtime/orchestrate/scripts/native_dispatch_driver.py",
            "entry_point": "append_causal_records",
            "validator": "runtime/orchestrate/scripts/validate_run_evidence.py",
            "runtime_adapter": self.runtime_adapter,
            "fixtures": fixtures,
        }
        print("FROZEN_RUNTIME_BRIDGE_EVIDENCE=" + json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)

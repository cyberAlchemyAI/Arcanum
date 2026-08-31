#!/usr/bin/env python3
"""Run the Dispatch Spec fixture matrix on Windows and POSIX hosts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"
FIXTURES = ROOT / "formulae/dispatch-spec/development/fixtures"
CASES = [
    ("pass", FIXTURES / "pass-refine-dispatch.json"),
    ("block", FIXTURES / "block-missing-validation-evidence.json"),
    ("flag", FIXTURES / "flag-unused-technique.json"),
    ("pass", FIXTURES / "pass-route-menu-overlay.json"),
    ("block", FIXTURES / "block-dialectic-missing-roles.json"),
    ("block", FIXTURES / "block-tournament-missing-convergence.json"),
    ("block", FIXTURES / "block-xray-missing-handle.json"),
    ("block", FIXTURES / "block-toy-game-missing-evidence.json"),
    ("pass", FIXTURES / "pass-memory-protected-overlay.json"),
    ("block", FIXTURES / "block-subagent-strategy-missing-roles.json"),
    ("pass", FIXTURES / "pass-subagent-lifecycle-closeout.json"),
    ("block", FIXTURES / "block-subagent-lifecycle-open-agent.json"),
    ("pass", FIXTURES / "pass-boundary-evidence.json"),
    ("flag", FIXTURES / "flag-boundary-technique-no-schema.json"),
    ("block", FIXTURES / "block-boundary-unknown-step.json"),
    ("block", FIXTURES / "block-promotion-split-violation.json"),
    ("pass", FIXTURES / "pass-native-stage-receipts.json"),
    ("block", FIXTURES / "block-command-interface-active-proof.json"),
    ("pass", ROOT / "formulae/dispatch-spec/examples/capability-bound-artifact-repair.json"),
    ("block", FIXTURES / "block-capability-bound-dependency-same-wave.json"),
    ("pass", ROOT / "arcana/refine/templates/refine-dispatch.json"),
    ("pass", ROOT / "runtime/orchestrate/tests/fixtures/compile/valid-two-wave.json"),
]


def validation_status(output: str) -> str | None:
    for line in reversed(output.splitlines()):
        if line.startswith("VALIDATION="):
            return line.split("=", 1)[1].strip()
    return None


def main() -> int:
    failed = 0
    for expected, path in CASES:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
        output = completed.stdout + completed.stderr
        actual = validation_status(output)
        passed = actual == expected
        print(
            f"DISPATCH_FIXTURE={'pass' if passed else 'block'} "
            f"EXPECTED={expected} ACTUAL={actual or 'missing'} PATH={path.relative_to(ROOT)}"
        )
        if not passed:
            failed += 1
            print(output.rstrip())

    child_scripts = [
        ROOT / "formulae/dispatch-spec/development/run-capability-bound-mutation-tests.py",
        ROOT / "formulae/dispatch-spec/development/run-execution-contract-v02-tests.py",
        ROOT / "formulae/dispatch-spec/development/run-confirmed-role-briefing-tests.py",
    ]
    for script in child_scripts:
        completed = subprocess.run([sys.executable, str(script)], check=False)
        if completed.returncode != 0:
            failed += 1

    status = "pass" if failed == 0 else "block"
    print(f"DISPATCH_SPEC_VALIDATION={status}")
    print(f"VALIDATION={status}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Prove Task Session's validation wrapper propagates child failures without stopping."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


WRAPPER = Path(__file__).resolve().with_name("run-validation-fixtures.sh")


def run_matrix(*statuses: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(WRAPPER), "--exit-propagation-fixture", *(str(item) for item in statuses)],
        check=False,
        capture_output=True,
        text=True,
    )


class ValidationWrapperExitPropagationTests(unittest.TestCase):
    def test_all_passing_children_return_zero(self) -> None:
        completed = run_matrix(0, 0, 0)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("children=3 aggregate_exit=0", completed.stdout)
        self.assertNotIn("TASK_SESSION_VALIDATION_CHILD_FAILED", completed.stderr)

    def test_failing_child_is_propagated_and_later_child_still_runs(self) -> None:
        completed = run_matrix(0, 7, 0)
        self.assertEqual(completed.returncode, 7, completed.stderr)
        self.assertIn("children=3 aggregate_exit=7", completed.stdout)
        self.assertIn("child=2 exit=7", completed.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

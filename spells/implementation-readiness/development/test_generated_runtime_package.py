#!/usr/bin/env python3
"""Prove the generated package resolves all shipped runtime dependencies."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
ARCANUM_ROOT = SPELL_ROOT.parents[1]
BOOTSTRAP = ARCANUM_ROOT / "tools" / "bootstrap_arcanum.sh"


class GeneratedRuntimePackageTests(unittest.TestCase):
    def test_generated_codex_package_runs_both_cli_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            subprocess.run(
                [
                    str(BOOTSTRAP),
                    "--target",
                    str(target),
                    "--sigils",
                    "continuation-router,task-session",
                    "--spells",
                    "implementation-readiness,work-pack-readiness-audit,task-session-until-blocker",
                    "--profiles",
                    "repo-codex",
                    "--force",
                    "--no-necronomicon",
                ],
                cwd=ARCANUM_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            package = target / ".agents" / "skills" / "implementation-readiness"
            for script, args in (
                ("run_execution_loop.py", ["--help"]),
                ("validate_execution_contracts.py", []),
            ):
                subprocess.run(
                    ["python3", str(package / "scripts" / script), *args],
                    cwd=target,
                    check=True,
                    capture_output=True,
                    text=True,
                )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Regression checks for the Plan-successor Design Boundary V6 evidence filter."""

from __future__ import annotations

import fnmatch
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
BASE = REPO / "arcanum/development/invoke-plan-successor-design"
SOURCE = BASE / "BOUNDARY-AUTHORING-REQUEST-V4.json"
PREPARER = BASE / "prepare_boundary_v6_source_request.py"
SNAPSHOT = REPO / "arcanum/development/invoke-plan-successor-design-material-v3"


class BoundaryV6EvidenceFilterTest(unittest.TestCase):
    def test_live_rules_exclude_generated_evidence_before_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "request.json"
            subprocess.run(
                [
                    "python3",
                    str(PREPARER),
                    "--source",
                    str(SOURCE),
                    "--output",
                    str(output),
                ],
                cwd=REPO,
                check=True,
            )
            document = json.loads(output.read_text(encoding="utf-8"))["document"]

        roots = {item["root_id"]: item["path"] for item in document["roots"]}
        selected: set[str] = set()
        for rule in document["discovery_rules"]:
            root = REPO / roots[rule["root_id"]]
            for child in root.rglob("*"):
                if not child.is_file() or child.is_symlink():
                    continue
                relative = child.relative_to(root).as_posix()
                if any(
                    fnmatch.fnmatchcase(relative, pattern)
                    for pattern in rule["include_globs"]
                ):
                    selected.add(f"{roots[rule['root_id']]}/{relative}")

        self.assertTrue(selected)
        self.assertFalse(
            any(
                "/__pycache__/" in path
                or path.endswith((".pyc", ".pyo", ".pyd"))
                for path in selected
            )
        )
        self.assertNotIn(
            "arcanum/spells/invoke/development/fixtures/define-intent-coverage/results/latest-summary.json",
            selected,
        )
        self.assertIn(
            "arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py",
            selected,
        )

    def test_frozen_inventory_contains_no_generated_evidence(self) -> None:
        inventory = json.loads(
            (SNAPSHOT / "SOURCE-INVENTORY.json").read_text(encoding="utf-8")
        )
        paths = [item["origin_path"] for item in inventory["entries"]]
        self.assertEqual(inventory["entry_count"], len(paths))
        self.assertFalse(
            any(
                "/__pycache__/" in path
                or path.endswith((".pyc", ".pyo", ".pyd"))
                or path.endswith(
                    "development/fixtures/define-intent-coverage/results/latest-summary.json"
                )
                for path in paths
            )
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Causal fixtures for Inventory projection conformance."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_projection_conformance.py"
SPEC = importlib.util.spec_from_file_location("projection_conformance", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def maps(entries):
    return MODULE.expected_maps(entries)


class ProjectionConformanceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.root = self.repo / ".arcanum" / "inventory"
        (self.root / "entries").mkdir(parents=True)
        (self.root / "wiki").mkdir()
        (self.root / "lint").mkdir()
        (self.root / "raw" / "manifests").mkdir(parents=True)
        (self.root / "entries" / "a.md").write_text(
            "---\nid: entry-a\ntype: synthesis\nstatus: candidate\n"
            "tags: [known]\n---\n# A\n",
            encoding="utf-8",
        )
        (self.root / "tags.md").write_text(
            "| Tag | Meaning |\n| --- | --- |\n| `known` | fixture |\n",
            encoding="utf-8",
        )
        self.entry = {
            "id": "entry-a",
            "path": "entries/a.md",
            "kind": "entry",
            "type": "synthesis",
            "title": "A",
            "summary": "fixture",
            "tags": ["known"],
            "sources": [],
            "updated": "2026-07-23",
            "status": "candidate",
            "confidence": "high",
            "selectors": [],
            "evidence_card_ids": [],
            "evidence_set_ids": [],
            "residue": [],
        }
        self.index = {
            "schema_version": "inventory.index.v0.1",
            "inventory_root": ".arcanum/inventory",
            "generated_at": "2026-07-23T00:00:00Z",
            "human_index": "index.md",
            "entries": [self.entry],
            "indexes": maps([self.entry]),
            "projections": [],
            "validation": {
                "parseable": True,
                "source_coverage": "complete",
                "validation_boundary": "inventory-read-model-only",
                "projection_conformance": MODULE.DEFAULT_CONFIG,
            },
        }
        self.write_human("synthesis")
        self.write_index()

    def tearDown(self):
        self.temp.cleanup()

    def write_human(self, entry_type):
        (self.root / "index.md").write_text(
            "# Inventory\n\n## Entries\n\n"
            "| Entry | Type | Tags | Summary |\n"
            "| --- | --- | --- | --- |\n"
            f"| [entries/a.md](entries/a.md) | {entry_type} | `known` | fixture |\n",
            encoding="utf-8",
        )

    def write_index(self):
        (self.root / "index.json").write_text(
            json.dumps(self.index, indent=2) + "\n",
            encoding="utf-8",
        )

    def report(self):
        return MODULE.validate(self.root / "index.json")

    def test_complete_fixture_passes(self):
        self.assertEqual("pass", self.report()["overall"])

    def test_missing_source_row_fails(self):
        (self.root / "entries" / "b.md").write_text("# B\n", encoding="utf-8")
        report = self.report()
        self.assertEqual("fail", report["checks"]["source_coverage"]["status"])
        self.assertIn(
            "entries/b.md",
            report["checks"]["source_coverage"]["missing_source_rows"],
        )

    def test_orphan_machine_row_fails(self):
        orphan = dict(self.entry, id="entry-b", path="entries/b.txt", title="B")
        (self.root / "entries" / "b.txt").write_text("B\n", encoding="utf-8")
        self.index["entries"].append(orphan)
        self.index["indexes"] = maps(self.index["entries"])
        self.write_index()
        report = self.report()
        self.assertEqual("fail", report["checks"]["source_coverage"]["status"])
        self.assertIn(
            "entries/b.txt",
            report["checks"]["source_coverage"]["orphan_machine_rows"],
        )

    def test_missing_indexed_path_fails(self):
        self.entry["path"] = "../../missing.md"
        self.index["indexes"] = maps(self.index["entries"])
        self.write_index()
        self.assertEqual("fail", self.report()["checks"]["existence"]["status"])

    def test_by_id_mismatch_fails(self):
        self.index["indexes"]["by_id"]["entry-a"] = "entries/wrong.md"
        self.write_index()
        self.assertEqual("fail", self.report()["checks"]["identity"]["status"])

    def test_derived_map_drift_fails(self):
        self.index["indexes"]["by_tag"] = {}
        self.write_index()
        self.assertEqual("fail", self.report()["checks"]["derived_maps"]["status"])

    def test_human_machine_identity_mismatch_fails(self):
        self.write_human("wrong-type")
        self.assertEqual("fail", self.report()["checks"]["human_view"]["status"])

    def test_stale_projection_digest_and_timestamp_fail(self):
        projection = self.root / "projections" / "index.csv"
        projection.parent.mkdir()
        projection.write_text("id,path\nentry-a,entries/a.md\n", encoding="utf-8")
        metadata = projection.with_suffix(".meta.json")
        metadata.write_text(
            json.dumps({
                "source_sha256": "stale",
                "source_generated_at": "2026-07-22T00:00:00Z",
                "projection_sha256": hashlib.sha256(projection.read_bytes()).hexdigest(),
            }),
            encoding="utf-8",
        )
        self.index["projections"] = [{
            "path": "projections/index.csv",
            "metadata": "projections/index.meta.json",
            "format": "csv",
            "source": "index.json",
            "purpose": "fixture",
            "freshness": "generated-from-current-index",
            "enabled": True,
        }]
        self.write_index()
        self.assertEqual("fail", self.report()["checks"]["freshness"]["status"])

    def test_current_projection_passes(self):
        projection = self.root / "projections" / "index.csv"
        projection.parent.mkdir()
        projection.write_text("id,path\nentry-a,entries/a.md\n", encoding="utf-8")
        self.index["projections"] = [{
            "path": "projections/index.csv",
            "metadata": "projections/index.meta.json",
            "format": "csv",
            "source": "index.json",
            "purpose": "fixture",
            "freshness": "generated-from-current-index",
            "enabled": True,
        }]
        self.write_index()
        source_digest = hashlib.sha256((self.root / "index.json").read_bytes()).hexdigest()
        (self.root / "projections" / "index.meta.json").write_text(
            json.dumps({
                "source_sha256": source_digest,
                "source_generated_at": self.index["generated_at"],
                "projection_sha256": hashlib.sha256(projection.read_bytes()).hexdigest(),
            }),
            encoding="utf-8",
        )
        self.assertEqual("pass", self.report()["checks"]["freshness"]["status"])

    def test_uncontrolled_tag_warns_without_blocking(self):
        self.entry["tags"] = ["known", "historical"]
        self.index["indexes"] = maps(self.index["entries"])
        self.write_index()
        report = self.report()
        self.assertEqual("pass", report["overall"])
        self.assertEqual(1, report["checks"]["tags"]["warning_count"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
